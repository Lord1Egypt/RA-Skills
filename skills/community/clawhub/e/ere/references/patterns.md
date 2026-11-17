# Catálogo de Padrões de IA — ERE

Baseado no guia "Signs of AI writing" (Wikipedia) e na skill humanizer (blader/humanizer).
Classificados em 4 categorias. O ERE detecta e remove estes padrões durante o refinamento.

## 1. Padrões de Conteúdo (8)

| # | Padrão | Exemplo IA | Correção |
|---|--------|-----------|----------|
| 1 | Inflação de importância | "um momento crucial na história" | "um momento importante" |
| 2 | Name-dropping de notabilidade | "segundo especialistas, pesquisadores e analistas" | Cite fonte específica ou remova |
| 3 | Análises com -ndo superficiais | "simbolizando a mudança, refletindo a era, mostrando a evolução" | Descreva o fato, não o símbolo |
| 4 | Linguagem promocional | "deslumbrante, imperdível, revolucionário" | Adjetivos factuais ou nenhum |
| 5 | Atribuições vagas | "Especialistas acreditam que..." | "Segundo [fonte], ..." ou remova |
| 6 | Desafios formulaicos | "Apesar dos desafios... continua a prosperar" | Descreva os desafios reais ou remova |
| 7 | Conclusões genéricas | "O futuro parece promissor" | Conclusão específica ou omita |
| 8 | Falsos arcos narrativos | "Da antiguidade aos dias de hoje..." | Recorte temporal preciso |

## 2. Padrões de Linguagem (10)

| # | Padrão | Exemplo IA | Correção |
|---|--------|-----------|----------|
| 9 | Vocabulário de IA | "ademais, outrossim, destarte, hodiernamente" | Conectores naturais: "também", "ainda", "já" |
| 10 | Evitar cópula | "serve como" → "é"; "boasts" → "tem" | Use verbos diretos |
| 11 | Paralelismos negativos | "não apenas X, mas também Y" | "X e Y" ou reestruture |
| 12 | Regra de três forçada | "inovador, disruptivo e transformador" | Um adjetivo preciso |
| 13 | Ciclo de sinônimos | "o projeto... a iniciativa... o empreendimento" | Use o nome ou pronome |
| 14 | Falsos intervalos | "da física quântica à astrofísica" | Escopo real |
| 15 | Voz passiva excessiva | "foi desenvolvido pela equipe" | "a equipe desenvolveu" |
| 16 | "Através de" genérico | "através da implementação de" | "implementando" ou "com" |
| 17 | "Enquanto" repetido | "Enquanto X, enquanto Y, enquanto Z" | Varie: "já", "ao passo que", "por outro lado" |
| 18 | "Não só... como também" | Estrutura binária forçada | Simplifique |

## 3. Padrões de Comunicação (5)

| # | Padrão | Exemplo IA | Correção |
|---|--------|-----------|----------|
| 19 | Artefatos de chatbot | "Espero que isso ajude! Me avise se..." | Remova completamente |
| 20 | Ressalvas de corte | "Embora os detalhes sejam limitados..." | "Os detalhes disponíveis indicam..." |
| 21 | Tom bajulador | "Ótima pergunta! Você está absolutamente certo!" | Responda diretamente |
| 22 | Anúncios de roteiro | "Vamos explorar...", "Vamos mergulhar em..." | Vá direto ao ponto |
| 23 | Falsa humildade | "Como um modelo de IA, não posso..." | Evite metacomentários |

## 4. Padrões de Estilo (10)

| # | Padrão | Exemplo IA | Correção |
|---|--------|-----------|----------|
| 24 | Travessões excessivos | "— como já mencionado — o projeto" | Vírgulas, parênteses ou reestruture |
| 25 | Negrito como muleta | `**etapa 1:** fazer X` | Prosa natural ou lista numerada |
| 26 | Headers com dois-pontos | `**Título:** explicação` | Frase completa |
| 27 | Title Case em títulos | "Como Implementar um Sistema" | "Como implementar um sistema" |
| 28 | Emojis decorativos | 🚀✨💡 | Remova (texto profissional) |
| 29 | Aspas curvas | "\u201ctexto\u201d" | Aspas retas: "texto" |
| 30 | Hífens desnecessários | "cross-functional", "real-time" | "cross functional", "real time" (pt-BR: sem hífen) |
| 31 | Frases de efeito forçadas | "Simetria é a linguagem da confiança" | Escreva o que quer dizer de forma direta |
| 32 | Dramas em staccato | "O resultado? Surpreendente." | "O resultado foi surpreendente." |
| 33 | Perguntas retóricas vazias | "Mas o que isso significa, de fato?" | Explique diretamente |

## Como o ERE aplica este catálogo

O agente segue o pipeline do SKILL.md:

1. **Preservação:** entidades e fatos são congelados antes da transformação
2. **Motores editoriais:** ritmo, léxico, conectores e estilo atuam em sequência
3. **Revisão:** AI Auditor verifica cada padrão antes da entrega

O `ere.py analyze` complementa com métricas objetivas:
- Densidade de conectores (padrões 9, 11, 17)
- Voz passiva (padrão 15)
- Comprimento e variação de frases (ritmo geral)
- Flesch Reading Ease (legibilidade)
