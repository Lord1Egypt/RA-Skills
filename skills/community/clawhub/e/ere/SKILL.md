---
name: ere
description: >-
  Editorial Refinement Engine — transforms LLM-generated text into
  editorially refined prose: more natural, less predictable, with varied
  rhythm, lexicon, structure and style, preserving facts, entities and
  quotes. English and Portuguese (pt-BR). / Transforma texto gerado por
  LLMs em prosa editorial refinada: mais natural, menos previsível, com
  variação de ritmo, léxico, estrutura e estilo, preservando fatos,
  entidades e citações. Inglês e português (pt-BR).
version: 1.4.0
author: Gabi (Hermes Agent) + Rickk Barbosa
license: MIT
platforms: [linux, darwin]
tags: [editorial, refinement, writing, humanization, text-quality, bilingual]
metadata:
  hermes:
    tags: [editorial, refinement, writing, humanization, text-quality, bilingual]
    category: productivity
    related_skills: []
    requires_toolsets: [terminal]
  openclaw:
    os: [linux, darwin]
    requires:
      bins: [python3]
      optional_bins: []
    install:
      pip: null
---

# ERE — Editorial Refinement Engine

Transforms AI text into professional editorial content — without fabricating
facts, losing information, or sounding like "robot text". Works in **English**
and **Portuguese (pt-BR)**. / Transforma texto de IA em conteúdo editorial
profissional — sem fabricar fatos, sem perder informações, sem soar como
"texto de robô". Funciona em **inglês** e **português (pt-BR)**.

## What it does / O que faz

- **Preserves facts:** entities, numbers, dates and quotes are frozen before any transformation / entidades, números, datas e citações são congelados antes da transformação
- **Applies editorial engines:** style, structure, rhythm, lexicon, connectors, intro, context / aplica motores editoriais: estilo, estrutura, ritmo, léxico, conectores, introdução, contexto
- **Removes AI patterns:** 33 catalogued patterns (clichés, repetitions, mechanical language) / 33 padrões catalogados (clichês, repetições, linguagem mecânica)
- **Quantitative metrics:** readability (Flesch), diff, composite quality score / métricas quantitativas: legibilidade (Flesch), diff, score de qualidade composto
- **5 profiles:** default (journalistic), technical, corporate, creative, minimal / 5 perfis: default (jornalístico), technical, corporate, creative, minimal

## Difference from traditional humanizer / Diferença do humanizer tradicional

| Humanizer (blader/humanizer) | ERE |
|---|---|
| Removes 33 "AI writing" patterns / remove 33 padrões de "AI writing" | Applies editorial engines: style, rhythm, lexicon, structure / aplica motores editoriais |
| Focus: not sounding like AI / foco: não parecer IA | Focus: editorial quality + readability + naturalness / foco: qualidade editorial + legibilidade + naturalidade |
| Single pass / única passagem | Pipeline with quantitative analysis / pipeline com análise quantitativa |
| No editorial profile / sem perfil editorial | 5 profiles / 5 perfis |

## When to use / Quando usar

- "Refine this text" / "Refina este texto" — "Improve the editorial quality of this article" / "Melhora a qualidade editorial deste artigo"
- "Humanize this content while keeping the facts" / "Humaniza este conteúdo mantendo os fatos"
- "Apply a journalistic profile to this technical text" / "Aplica perfil jornalístico neste texto técnico"
- "ERE: refine with creative profile level 75" / "ERE: refina com perfil creative nível 75"

## When NOT to use / Quando NÃO usar

- Translation / tradução (use a translation tool)
- Simple grammar correction / correção gramatical simples (use a spell-checker)
- Generating content from scratch / geração de conteúdo do zero (use the base model)
- Text that depends on exact formatting (code, tables, JSON) / textos que dependem de formatação exata (código, tabelas, JSON)

## How to use / Como usar

### Basic invocation / Invocação básica

```
ERE: refina este texto com perfil default     (PT)
ERE: refine this text with default profile    (EN)
[cole o texto aqui / paste the text here]
```

### With profile and level / Com perfil e nível

```
ERE: perfil technical, nível 40               (PT)
ERE: technical profile, level 40              (EN)
[texto técnico / technical text]
```

### With quality analysis / Com análise de qualidade

```
ERE: refina e analisa                         (PT)
ERE: refine and analyze                       (EN)
[texto / text]
```

## Refinement Pipeline / Pipeline de Refinamento

When ERE is invoked, follow this pipeline in sequence. / Quando o ERE é
invocado, siga este pipeline em sequência.

### 1. PRESERVATION / PRESERVAÇÃO (Fact Preservation)

**Before any transformation**, identify and freeze: / **ANTES de qualquer transformação**, identifique e congele:

- **Named entities / entidades nomeadas:** people, companies, products, places / pessoas, empresas, produtos, locais
- **Numbers and dates / números e datas:** values, percentages, years, times / valores, percentuais, anos, horários
- **Literal quotes / citações literais:** text in quotation marks, attributed speech / texto entre aspas, falas atribuídas
- **Technical terms / termos técnicos:** acronyms, domain jargon / siglas, jargão do domínio

**Rule / Regra:** this information CANNOT be altered, paraphrased or omitted. If it appears in the original, it must appear identically in the refined text. / estas informações NÃO podem ser alteradas, parafraseadas ou omitidas.

### 2. STYLE / ESTILO (Style Selector)

Adjust register according to the profile / Ajuste o registro conforme o perfil:

| Profile / Perfil | Register / Registro | Tone example / Exemplo de tom |
|--------|----------|----------------|
| default (journalistic) | Neutral-professional / neutro-profissional | "The project was launched in March" / "O projeto foi lançado em março" |
| technical | Objective-technical / objetivo-técnico | "The API returns HTTP 200 with a JSON payload" / "A API retorna HTTP 200 com payload JSON" |
| corporate | Formal-business / formal-empresarial | "The organization implemented the initiative" / "A organização implementou a iniciativa" |
| creative | Expressive-engaging / expressivo-envolvente | "March brought the project to life" / "Março trouxe o projeto à vida" |
| minimal | Direct-lean / direto-enxuto | "Project launched in March" / "Projeto lançado em março" |

### 3. STRUCTURE / ESTRUTURA (Structure Engine)

- Vary the opening: do not always start with subject + verb / varie a abertura: não comece sempre com sujeito + verbo
- Alternate descriptive and analytical paragraphs / alterne entre parágrafos descritivos e analíticos
- If the original has 3 background paragraphs, condense to 1-2 / se o original tem 3 parágrafos de background, condense em 1-2
- If the original jumps straight to details without context, add 1 framing sentence / se o original pula direto para detalhes sem contexto, adicione 1 frase de abertura
- Respect the profile's `paragraph_size` / respeite o `paragraph_size` do perfil

### 4. RHYTHM / RITMO (Rhythm Engine)

- **Vary sentence length / varie o comprimento das frases.** If the original has 5 sentences of ~20 words, produce something like: 8, 22, 5, 18, 12 words
- Break very long periods (>40 words in pt-BR, >35 in EN) / quebre períodos muito longos (>40 palavras em pt-BR, >35 em en)
- Join consecutive ultra-short fragments if they sound telegraphic / una fragmentos muito curtos consecutivos se soarem telegráficos
- Avoid more than 3 sentences with the same syntactic structure in a row / evite mais de 3 frases com mesma estrutura sintática em sequência
- Target: standard deviation between 5 and 12 words (measured by `ere.py analyze`) / alvo: desvio padrão entre 5 e 12 palavras (medido pelo `ere.py analyze`)

### 5. LEXICON / LÉXICO (Lexical Engine)

- **Replace repeated words** within nearby paragraphs (distance < 50 words) / **substitua palavras repetidas** em parágrafo próximo (distância < 50 palavras)
- **Eliminate AI clichés / elimine clichês de IA:**
  - "it is important to note that" → remove or use "note that" / "é importante notar que" → remova ou use "note que"
  - "plays a fundamental role" → "is essential for" / "desempenha um papel fundamental" → "é essencial para"
  - "in today's world" / "no mundo de hoje" → remove / remova
  - "it is worth noting" / "vale ressaltar" → remove / remova
  - "not only... but also" / "não apenas... mas também" → simplify / simplifique
  - "through" (non-physical) → "by means of" / "através de" (não físico) → "por meio de" ou "com"
- **Vocabulary / vocabulário:** use the profile's `verbosity` field — low: lean, no flourish / enxuto; high: rich, precise synonyms / rico, com sinônimos precisos

### 6. CONNECTORS / CONECTORES (Connector Engine)

- **Vary connectors / varie conectores.** If the original uses "furthermore" 3 times, use "also", "moreover", "in addition" / se o original usa "além disso" 3 vezes, use "também", "ainda", "ademais"
- **Reduce density / reduza densidade.** Target: 1 connector every 3-4 sentences (verified by `ere.py analyze`) / alvo: 1 conector a cada 3-4 frases
- **Avoid / evite:** "firstly... secondly... finally" (mechanical) / "primeiramente... segundamente... finalmente" (mecânico)

### 7. INTRODUCTION / INTRODUÇÃO (Intro Generator)

- Vary the opening pattern / varie o padrão de abertura:
  - **Fact / fato:** "In March 2026, the project reached 10,000 users" / "Em março de 2026, o projeto atingiu 10 mil usuários"
  - **Question / pergunta:** "What happens when an open-source tool reaches maturity?" / "O que acontece quando uma ferramenta open source atinge maturidade?"
  - **Scene / cena:** "It was a deploy morning when the alert fired" / "Era uma manhã de deploy quando o alerta disparou"
  - **Contrast / contraste:** "While the market bet on proprietary AI, the team went the other way" / "Enquanto o mercado apostava em IA proprietária, a equipe foi na direção oposta"
  - **Direct / direto:** "The project launched. The results surprised." / "O projeto foi lançado. Os resultados surpreenderam."
- The opening must match the profile (creative varies more; technical is more direct) / a abertura deve corresponder ao perfil (creative usa mais variação; technical é mais direto)

### 8. CONTEXT / CONTEXTO (Context Engine)

- If the profile has `context: true`, enrich with information implicit in the text itself / se o perfil tem `context: true`, enriqueça com informações implícitas no próprio texto
- **NEVER invent facts, data, quotes or external references / NUNCA invente fatos, dados, citações ou referências externas**
- Use only information already in the text or general undisputed knowledge / use apenas informações que já estão no texto ou são de conhecimento geral e indiscutível
- Example / exemplo: if the text mentions "Docker", you may add "the container platform" as an apposition — general knowledge, not invention / se o texto menciona "Docker", pode adicionar "a plataforma de containers" como aposição — conhecimento geral, não invenção

### 9. REVIEW / REVISÃO (AI Auditor)

After refinement, verify / após o refinamento, verifique:

- [ ] Names, numbers and dates identical to the original? / nomes, números e datas estão idênticos ao original?
- [ ] Literal quotes not paraphrased? / citações literais não foram parafraseadas?
- [ ] No information added that was not in the original? / nenhuma informação foi adicionada que não estava no original?
- [ ] No repeated words in adjacent paragraphs? / não há repetição de palavras em parágrafos adjacentes?
- [ ] Sentences vary in length? / as frases variam em comprimento?
- [ ] No AI clichés? / o texto não contém clichês de IA?
- [ ] Tone matches the requested profile? / o tom corresponde ao perfil solicitado?

## Quantitative Analysis / Análise Quantitativa

After generating the refined text, run the helper for metrics / após gerar o texto refinado, execute o helper para métricas:

```bash
# Save original and refined / salvar original e refinado
echo "$ORIGINAL" > /tmp/ere_original.txt
echo "$REFINED" > /tmp/ere_refined.txt

# Analyze / analisar
python3 scripts/ere.py analyze /tmp/ere_refined.txt
python3 scripts/ere.py diff /tmp/ere_original.txt /tmp/ere_refined.txt
```

### Score interpretation / Interpretação dos scores

| Score | Meaning / Significado |
|-------|-------------|
| 90-100 | Excellent — ready to publish / excelente — pronto para publicação |
| 75-89 | Good — minor improvements possible / bom — pequenas melhorias possíveis |
| 60-74 | Fair — review rhythm and lexicon / regular — revisar ritmo e léxico |
| <60 | Unsatisfactory — reapply refinement / insatisfatório — reaplicar refinamento |

## Profiles / Perfis

| Profile / Perfil | Default level / Nível padrão | Ideal for / Ideal para |
|--------|-------------|------------|
| `default` | 60 | Articles, blog posts, general content / artigos, blog posts, conteúdo geral |
| `technical` | 40 | Documentation, tutorials, specs / documentação, tutoriais, specs |
| `corporate` | 50 | Announcements, reports, presentations / comunicados, relatórios, apresentações |
| `creative` | 75 | Storytelling, marketing, opinion / storytelling, marketing, opinião |
| `minimal` | 25 | Summaries, bullet points, notes / resumos, bullet points, notas |

Usage / uso: `ERE: creative profile level 80` / `ERE: perfil creative nível 80`

## Refinement levels / Níveis de refinamento

| Level / Nível | Effect / Efeito |
|-------|--------|
| 0-25 | Light corrections: rhythm, clichés, repeated connectors / correções leves: ritmo, clichês, conectores repetidos |
| 25-50 | Moderate restructuring: vary paragraphs, improve lexicon / reestruturação moderada: varia parágrafos, melhora léxico |
| 50-75 | Full editorial style: intro, structure, context / estilo editorial completo: intro, estrutura, contexto |
| 75-100 | Deep rewrite: preserves only facts and entities / reescrita profunda: preserva apenas fatos e entidades |

## Golden Rules / Regras de ouro

1. **NEVER invent / NUNCA invente.** No facts, data, quotes or references not in the original / sem fatos, dados, citações ou referências que não estejam no original.
2. **NEVER omit / NUNCA omita.** Every factual piece of the original must appear in the refined text / toda informação factual do original deve aparecer no refinado.
3. **NEVER alter entities / NUNCA altere entidades.** Names, numbers, dates are sacred / nomes, números, datas são sagrados.
4. **ALWAYS vary / SEMPRE varie.** Rhythm, lexicon, connectors, structure — variation is what makes text human / ritmo, léxico, conectores, estrutura — a variação é o que torna o texto humano.
5. **The refined text must be indistinguishable from text written by a good human editor** — not an AI trying not to sound like AI / **o texto refinado deve ser indistinguível de um texto escrito por um bom editor humano** — não por uma IA tentando não parecer IA.

## Classics' writing principles / Princípios dos clássicos de escrita

ERE incorporates guidance from three reference works on writing refinement.
The full catalogue (46 principles + anti-pattern checklist, organized by
category) is in `references/writing-principles.md`. Sources / fontes:
**[GS]** *The Science of Scientific Writing* (Gopen & Swan),
**[SW]** *The Elements of Style* (Strunk & White), **[OG]** *Comunicação em
Prosa Moderna* (Othon M. Garcia).

### Pipeline mapping / Mapeamento para o pipeline

| Pipeline stage / Etapa | Applicable principles / Princípios aplicáveis |
|---|---|
| 1. Preservation / preservação | F1, F2 (facts vs. clues; validity of claims) |
| 2. Style / estilo | D1 (active voice), D2 (positive statements), D3 (background), C7 (nouns/verbs), C6 (plain words) |
| 3. Structure / estrutura | A1 (planning), A2 (paragraph unit), A3 (topic sentence), A4 (development), A5 (coherence), A7 (one design) |
| 4. Rhythm / ritmo | B5 (one unit, one point), B8 (unfold labyrinthine periods), E3 (clause boundaries) |
| 5. Lexicon / léxico | C2 (precision), C3 (generalization+specification), C4 (concrete), C5 (omit words), C8 (qualifiers) |
| 6. Connectors / conectores | A5 (transition), E3 (boundary punctuation) |
| 7. Introduction / introdução | A3 (topic sentence), B7 (context before new) |
| 8. Context / contexto | C3 (specification), B7 (context first) |
| 9. Review / revisão | B2 (stress position), B3 (topic position), B4 (given-new), F4 (fallacies), F5 (logical gaps) |

### Golden rules of the classics (most transformative) / Regras de ouro dos clássicos (as mais transformadoras)

1. **Subject followed by the verb** [GS] — nothing longer than ~8-10 words between them; interposed material reads as interruption / **sujeito seguido do verbo** — nada com mais de ~8-10 palavras entre eles.
2. **Stress position at the end** [GS][SW] — close each sentence with the new information that deserves emphasis; never with a weak verb / **posição de ênfase no fim** — feche cada frase com a informação nova que merece destaque.
3. **Given at the start, new at the end** [GS] — topic position = already-mentioned info; stress position = novelty / **dado no início, novo no fim** — posição de tópico = informação já mencionada.
4. **One unit, one point** [GS] — "sentence too long" = more stress candidates than positions. Split or create secondary positions (; and :) / **uma unidade, um ponto** — divida ou crie posições secundárias.
5. **Unfold labyrinthine periods** [OG] — >35-40 words or 3+ subordinate clauses before the main one: rewrite, don't punctuate / **desdobre períodos labirínticos** — reescreva, não pontue.
6. **Keep related terms close** [OG][SW] — modifier far from modified creates ambiguity; when emphasis conflicts with clarity, clarity wins / **aproxime termos relacionados** — quando conflitar ênfase vs. clareza, a clareza vence.
7. **Every generalization needs specification** [OG] — general claim needs fact, data, example or reason right after / **toda generalização exige especificação** — tópico frasal + desenvolvimento é o padrão.
8. **Omit needless words** [SW] — "every word tell"; cut "the question of whether", fillers (very, really) / **omita palavras desnecessárias** — corte enchimentos e qualificadores.
9. **Positive statements** [SW] — say what is, not what is not; remove hesitant conditionals (could, maybe) without real uncertainty / **declarações positivas** — diga o que é, não o que não é.
10. **Clarity above form** [OG] — empty elegance falsifies ideas; if the meaning needs re-reading, rewrite / **clareza acima da forma** — se o sentido exigir releitura, reescreva.
11. **Action in the verb** [GS] — "who does what?"; action hidden in nominalization loses structural cues / **ação no verbo** — ação central escondida em nominalização perde as pistas estruturais.
12. **Facts ≠ clues** [OG] — clue-level evidence needs "seems/probably/suggests"; inference stated as fact is fallacy / **fatos ≠ indícios** — inferência apresentada como fato é falácia.

### Most frequent anti-patterns / Anti-padrões mais frequentes

- Comma splice and broken sentence mid-dependent-clause [SW]
- Sentence ending with weak material in the stress position [GS]
- New information opening in the topic position [GS]
- Generic terms where a specific word fits ("tree" → "palm") [OG]
- Gratuitous superlatives and "one of the most" [SW]
- Begging the question: the claim used as proof [OG]
- False causality: correlation treated as cause [OG]
- Agentless passive when the agent is known [SW][GS]

## Portuguese (pt-BR) / Português (pt-BR)

Refining text in Portuguese demands language-specific rules — word order,
pronoun placement, verb government, gerund usage, language vices. The full
catalogue (33 principles organized in G/H/I/J/K + pt-BR anti-pattern
checklist) is in `references/portuguese-writing-principles.md`, extracted
from *Comunicação em Prosa Moderna* (Othon M. Garcia). / Refinar texto em
português exige regras próprias da língua — ordem de colocação, colocação
pronominal, regência, gerúndio, vícios de linguagem. O catálogo completo
está em `references/portuguese-writing-principles.md`.

### Portuguese golden rules / Regras de ouro do português

1. **Direct order is the norm; inversion only with purpose** [G1] — front a term only for emphasis, clarity, rhythm or euphony; gratuitous inversion sounds stilted / **ordem direta é a norma; inversão só com propósito**.
2. **Fronted object/predicative? Resume with a pronoun** [G2] — "o homem... fê-lo"; without the resumption the inversion is truncated / **antepôs objeto/predicativo? retome com pronome**.
3. **"E" is not always addition** [G5] — false coordination: cause → "porque", consequence → "por isso", opposition → "mas" / **"e" nem sempre é adição** — explicite a relação lógica.
4. **Tense period: main clause at the end for suspense; loose: main clause first for direct text** [G3] / **período tenso: principal no fim para suspense; frouxo: principal primeiro para texto direto**.
5. **Drag-on sentences and litany are defects** [G7][G8] — "Então... mas aí... então..."; paragraphs chained by "e" — subordinate and vary connectors / **frase de arrastão e ladainha são defeitos**.
6. **Gerund: secondary action, never adjective** [I1] — "tendo objeto próprio" → "com objeto próprio"; avoid "vou estar fazendo" / **gerúndio: ação secundária, nunca adjetivo**.
7. **Amphibology: the reader must know who does what** [J3] — "O pai viu o filho sair" is ambiguous; pronoun with a single referent / **anfibolia: o leitor precisa saber quem faz o quê**.
8. **Vicious pleonasm is an error; intentional is emphasis** [J4] — cut "subir para cima", "planejamento prévio"; keep "vi com meus próprios olhos" only with real expressive weight / **pleonasmo vicioso é erro; intencional é ênfase**.
9. **Preciosity is a vice, not a virtue** [J5] — "óbito" → "morte"; if the word requires a dictionary and there is a common synonym, replace / **preciosismo é vício, não virtude**.
10. **Cacophony and echo break reading** [K1] — read aloud: "boca dela", "ção" series / **cacofonia e eco quebram a leitura** — leia em voz alta.
11. **Pronoun placement: cultured norm without artificiality** [I5] — proclisis after negatives/adverbs/relatives; enclisis at start / **colocação pronominal: norma culta sem artificialidade**.
12. **Evaluative load contaminates objective text** [J8] — "burocrata" vs. "funcionário"; use the neutral term if the fact doesn't support the judgment / **carga valorativa contamina texto objetivo**.

### Most frequent pt-BR anti-patterns / Anti-padrões pt-BR mais frequentes

- False coordination: "e" hiding cause/consequence/opposition [G5]
- Drag-on sentence: "Então... mas aí... então... aí..." [G7]
- Vicious fragment: gerund isolated by a period by carelessness [G10]
- Broken correlations: "não tanto... mas também" [H2]
- Solecisms: "haviam pessoas", "fazem cinco anos", "a gente vamos" [I3]
- Wrong government: "assistir o filme", "preferir X do que Y" [I4]
- Vicious pleonasm: "subir para cima", "entrar para dentro", "surpresa inesperada" [J4]
- Clichés: "vale ressaltar", "cabe destacar", "frio de rachar" [J6]
- Rhetorical crutches: "no que tange a", "com vistas a", "faz-se mister" [J9]
- Cacophony: "boca dela", "cada lado" [K1]

## Example / Exemplo

### Input / Entrada (PT)

```
O projeto de automação residencial foi desenvolvido pela equipe em 2025.
O projeto utiliza sensores IoT para monitorar o ambiente. Além disso,
o projeto conta com um aplicativo mobile para controle remoto. É importante
notar que o projeto foi premiado na feira de tecnologia. O projeto também
oferece integração com assistentes virtuais como Alexa e Google Home.
```

### Output / Saída (default profile, level 60 / perfil default, nível 60)

```
Premiado na feira de tecnologia de 2025, o projeto de automação residencial
nasceu com uma proposta ambiciosa: integrar sensores IoT, controle mobile
e assistentes virtuais em uma única plataforma.

A equipe desenvolveu um sistema que monitora o ambiente em tempo real
usando sensores conectados. O aplicativo mobile complementa a experiência
com controle remoto, enquanto a compatibilidade com Alexa e Google Home
elimina a fricção de aprender uma nova interface.

O resultado é uma casa que responde — sem que o morador precise pensar nisso.
```

### Metrics / Métricas

- Original: 5 sentences, ~11 words/sentence (monotonous) / 5 frases, ~11 palavras/frase (monótono)
- Refined: 6 sentences, lengths 8, 22, 18, 14, 17, 12 (varied) / 6 frases, comprimentos 8, 22, 18, 14, 17, 12 (variado)
- Word "projeto": 6x in the original, 1x in the refined / 6x no original, 1x no refinado
- Flesch: 45 → 62

## Pitfalls

### YAML Parser: inline comments not stripped

The simple YAML subset parser in `ere.py` does NOT strip inline comments by default.
A value like `"journalistic  # comment"` will include the comment as part of the value.
This was fixed in v1.0.0 by adding `value.split("#")[0].strip()` after parsing.

### Profile not found: falls back to default

If the requested profile name doesn't exist in `profiles/default.yaml`, the loader
returns the `default` profile silently. Verify with `ere.py profile <name>` before using.

### pgpy not available on Python 3.13+

The `pgpy` library fails with `ModuleNotFoundError: No module named 'imghdr'` because
`imghdr` was removed from stdlib in Python 3.13. ERE uses only stdlib for this reason.

## Files / Arquivos

| File / Arquivo | Function / Função |
|---------|--------|
| `scripts/ere.py` | Quantitative analysis / análise quantitativa: readability, diff, quality score |
| `profiles/default.yaml` | Editorial profiles / perfis editoriais: default, technical, corporate, creative, minimal |
| `references/patterns.md` | AI patterns to avoid / padrões de IA a evitar (33 padrões) |
| `references/writing-principles.md` | Classics' writing principles / princípios dos clássicos: 46 rules + anti-patterns (Gopen & Swan, Strunk & White, Othon Garcia) |
| `references/portuguese-writing-principles.md` | pt-BR language rules / português pt-BR: 33 regras da língua + anti-padrões (Othon Garcia) |
| `references/ERE.md` | Architecture document (original SDD) / documento de arquitetura completo (SDD original) |

## Agent compatibility / Compatibilidade entre agentes

| Agent / Agente | How it loads / Como carrega |
|--------|--------------|
| Hermes Agent | `SKILL.md` (metadata.hermes) |
| OpenClaw | `SKILL.md` (metadata.openclaw) |
| Claude Code | `.claude/skills/ere/SKILL.md` + `CLAUDE.md` |
| Codex | `.agents/skills/ere/SKILL.md` + `AGENTS.md` |
