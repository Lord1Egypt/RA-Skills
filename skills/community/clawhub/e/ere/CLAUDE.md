# ERE — Editorial Refinement Engine

Editorial refinement skill for Claude Code / Codex. Transforms LLM-generated
text into quality editorial prose, preserving facts, entities and quotes.
Bilingual: English and Portuguese (pt-BR). / Skill de refinamento editorial
para Claude Code / Codex. Transforma texto gerado por LLMs em prosa
editorial de qualidade, preservando fatos, entidades e citações. Bilíngue:
inglês e português (pt-BR).

## How to use / Como usar

When asked to refine ("refine this text", "humanize", "apply an editorial
profile"), follow the 9-stage pipeline in `SKILL.md` / ao receber um pedido
de refinamento ("refina este texto", "humaniza", "aplica perfil editorial"),
siga o pipeline de 9 etapas documentado em `SKILL.md`:

1. **Preservation / preservação** — freeze entities, numbers, dates and quotes first / congele entidades, números, datas e citações antes de tudo
2. **Style / estilo** — adjust register to the profile (default/technical/corporate/creative/minimal)
3. **Structure / estrutura** — vary opening and paragraph organization
4. **Rhythm / ritmo** — vary sentence length
5. **Lexicon / léxico** — remove AI clichés and repetitions
6. **Connectors / conectores** — vary and reduce density
7. **Introduction / introdução** — vary the opening pattern
8. **Context / contexto** — enrich only with undisputed general knowledge
9. **Review / revisão** — audit against the original

## Golden rules / Regras de ouro

1. NEVER invent facts, data, quotes or references / NUNCA invente.
2. NEVER omit factual information from the original / NUNCA omita.
3. NEVER alter entities, numbers or dates / NUNCA altere entidades.
4. ALWAYS vary rhythm, lexicon, connectors and structure / SEMPRE varie.
5. The result must read like a good human editor wrote it / o resultado deve parecer escrito por um bom editor humano.

## Profiles / Perfis

| Profile / Perfil | Level / Nível | Use / Uso |
|-------|-----|-------|
| default | 60 | Articles, blog posts / artigos, blog posts |
| technical | 40 | Documentation, tutorials, specs / documentação, tutoriais, specs |
| corporate | 50 | Announcements, reports / comunicados, relatórios |
| creative | 75 | Storytelling, marketing / storytelling, marketing |
| minimal | 25 | Summaries, notes, bullets / resumos, notas, bullets |

## Quantitative analysis (optional) / Análise quantitativa (opcional)

```bash
python3 scripts/ere.py analyze arquivo.txt      # quality metrics / métricas de qualidade
python3 scripts/ere.py diff original.txt refined.txt  # comparison / comparação
python3 scripts/ere.py profile technical         # inspect profile / inspeciona perfil
```

Requires Python 3.10+ (stdlib only). Architecture document in
`references/ERE.md`; AI patterns catalogue in `references/patterns.md`;
classics' writing principles (Gopen & Swan, Strunk & White, Othon Garcia) in
`references/writing-principles.md` — consult when refining structure, clarity,
precision or argumentation. For Portuguese text, also consult
`references/portuguese-writing-principles.md` (word order, pronoun placement,
verb government, gerund, language vices).

Requires Python 3.10+ (stdlib apenas). Documento de arquitetura em
`references/ERE.md`; catálogo de padrões de IA em `references/patterns.md`;
princípios dos clássicos (Gopen & Swan, Strunk & White, Othon Garcia) em
`references/writing-principles.md`. Para texto em português, consulte também
`references/portuguese-writing-principles.md` (ordem de colocação, colocação
pronominal, regência, gerúndio, vícios de linguagem).
