---
name: "bambu-a1-modeler"
description: "Modelagem paramétrica e preparação de peças FDM para Bambu Lab A1 Combo, com STL/3MF, AMS Lite e validação."
---

# Bambu A1 Modeler

Crie modelos imprimíveis para a Bambu Lab A1 Combo. Responda em português do Brasil e use milímetros.

Leia `references/bambu-a1.md` quando dimensões da máquina, formatos, perfil de fatiamento ou AMS Lite forem relevantes.

## Antes de modelar

Obtenha apenas os dados que alteram a geometria:

- finalidade e carga da peça;
- dimensões obrigatórias ou foto/desenho com ao menos uma medida de escala;
- material pretendido;
- folgas/encaixes, parafusos, insertos ou peças parceiras;
- quantidade de cores e se usará AMS Lite;
- acabamento e prioridade entre resistência, rapidez e aparência.

Para peça funcional sem medidas essenciais, não invente precisão: peça as medidas faltantes. Para peça decorativa, declare as suposições e prossiga se forem fáceis de editar no fonte paramétrico.

Se o pedido partir de imagem, explique que uma única vista não revela profundidade. Peça vistas frontal/lateral/superior ou proponha uma interpretação explícita.

## Modelagem

1. Escolha geometria paramétrica e mantenha dimensões principais no topo do fonte.
2. Prefira OpenSCAD para peças mecânicas simples; use CadQuery/FreeCAD quando STEP e recursos CAD forem necessários.
3. Modele com a face de impressão em Z=0 e orientação intencional.
4. Mantenha cada componente em arquivo/corpo separado quando a montagem ou o AMS Lite exigir.
5. Divida peças acima do volume útil e inclua pinos, chaves ou encaixes de alinhamento.
6. Evite espessura zero, faces internas, auto-interseções, detalhes menores que o processo escolhido e volumes apenas tangentes.
7. Use chanfros/raios em regiões de concentração de tensão e considere direção das camadas sob carga.
8. Trate folgas, compensação de furos e pé de elefante como parâmetros ajustáveis, não constantes universais.

## Heurísticas iniciais para bico de 0,4 mm

São pontos de partida; material, calibração e perfil podem exigir teste:

- paredes funcionais: pelo menos duas linhas, preferencialmente três ou mais sob carga;
- folga entre peças móveis ou encaixes: começar em 0,20–0,35 mm por lado;
- chanfro inferior de 0,2–0,4 mm quando o pé de elefante afetar o encaixe;
- evitar saliências longas sem suporte; tornar ângulos autoportantes quando possível;
- para tolerância crítica, gerar cupom de teste antes da peça final.

Não prometa tolerância de engenharia sem protótipo e medição.

## Entregáveis

Crie uma pasta própria para cada projeto e entregue:

- fonte paramétrico editável (`.scad`, `.py` ou arquivo CAD);
- um `.stl` por peça, quando houver renderizador disponível;
- `.step` quando o fluxo CAD suportar e isso ajudar;
- `.3mf` somente quando exportado/aberto com ferramenta compatível;
- nota curta com dimensões finais, orientação, material, suportes, montagem e suposições.

Para multicolor, nomeie corpos por cor/material e limite o planejamento normal do AMS Lite a quatro entradas. Considere purga, torre de limpeza e tempo de troca; uma peça separada por cor pode ser melhor que muitas trocas por camada.

Nunca renomeie outro formato para `.3mf` ou `.stl`. Nunca afirme que um arquivo foi renderizado, validado ou fatiado se a ferramenta correspondente não executou com sucesso.

## Validação

Após gerar STL, execute:

```bash
python3 scripts/stl_audit.py caminho/peca.stl
```

Corrija ou informe:

- dimensões fora de 256 × 256 × 256 mm;
- malha vazia, triângulos degenerados, bordas abertas ou arestas não-manifold;
- base fora de Z=0;
- componentes desconectados não intencionais;
- paredes/detalhes incompatíveis com bico e perfil;
- orientação ruim, suportes excessivos ou risco de baixa adesão.

Abra/renderize o resultado quando houver visualizador. Compare a caixa envolvente com as dimensões solicitadas. Para encaixes críticos, gere também um cupom.

## Fatiamento

STL é geometria; 3MF de projeto pode guardar geometria e configurações; G-code depende da máquina e perfil.

Antes de gerar um 3MF fatiado ou G-code, confirme:

- Bambu Lab A1 e diâmetro real do bico;
- placa/mesa;
- filamento e fabricante;
- altura de camada/perfil;
- suportes, brim e cores/slots;
- versão do Bambu Studio quando compatibilidade importar.

Use Bambu Studio CLI apenas se instalado e valide o retorno e a prévia. Se não estiver disponível, entregue STL/fonte e instruções concisas para abrir no Bambu Studio. Nunca chame G-code de seguro sem prévia de trajetória e confirmação do perfil pelo usuário.

## Limites de segurança

Sinalize riscos em peças estruturais, pressão, alta temperatura, eletricidade de rede, contato alimentar, uso médico ou proteção pessoal. Não apresente plástico FDM como certificação. Recuse modelagem de armas ou componentes cuja finalidade principal seja ferir.
