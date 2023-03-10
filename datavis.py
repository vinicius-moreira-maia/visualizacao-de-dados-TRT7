import csv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw

def main():
    dados = []

    num = get_num()

    # só o que interessa é a primeira parte do arquivo
    with open("tabela.csv") as file:
        reader = csv.DictReader(file)
        for line in reader:
                dados.append(line)
                if len(dados) >= 6:
                     break

    # deletando um par chave-valor vazio
    for dicio in dados:
        del dicio['']

    # assegurando que o total é 1167, assim como consta na tabela original
    total = 0
    for dicio in dados:
        for v in dicio.values():
            try:
               total += int(v)
            except ValueError:
                pass
    # print(total)

    # transformando a lista de dicionarios em listas de tuplas
    dados2 = []
    for dicio in dados:
        dados2.append(list(dicio.items()))

    teste = dados2[num] # teste recebe uma lista de pares chave-valor por vez (é o que é escolhido via input)
    legenda = teste[0][1] # a legenda é o segundo elemento (elemento 1) do primeiro par chave-valor (sempre)

    # os nome 'data' e 'recipe' são só por conveniência, já estava assim no exemplo do 'matplotlib'
    recipe = []
    data = []

    # criando as listas pulando o primeiro elemento (que é apenas o título de cada gráfico)
    for i in range(1, len(teste)):
        recipe.append(teste[i][0].title()) # capitalizando os nomes dos meses
        data.append(int(teste[i][1])) # transformando os dígitos em inteiros (pode dar ValueError)

    # gráfico sem título
    create_chart(recipe, data, legenda)

    # adicionando título com a biblioteca 'PIL'
    imagem = Image.open("teste.png")
    title_text = legenda
    font = ImageFont.truetype('Myriad Pro Semibold.ttf', 38) # 'setando' a fonte e o tamanho
    image_editable = ImageDraw.Draw(imagem) # transformando a imagem em editável
    image_editable.text((15,15), title_text, (0, 0, 0), font=font) # posicionando o texto
    imagem.save(f"{num}.png")

def create_chart(recipe, data, legenda):
    '''
       a implementação dessa função não importa tanto quanto saber o que eu devo fornecer e o que ela fornece
    '''
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

    print(legenda) # para aparecer no terminal apenas como feedback
    plt.savefig(f"teste.png", format="png", dpi=400)

def get_num():
    while True:
        try:
            num = int(input("digitar de 0 a 5 >> "))
            if num > 5 or num < 0:
                raise ValueError
            else:
                return num
        except ValueError:
            print("número inválido")
            pass

if __name__ == "__main__":
    main()
