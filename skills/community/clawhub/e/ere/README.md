# ERE — Editorial Refinement Engine

Multi-agent skill that transforms LLM-generated text into editorially refined
content. Compatible with **Hermes Agent**, **OpenClaw**, **Claude Code** and
**Codex**. Bilingual instructions: **English** and **Portuguese (pt-BR)**. /
Skill multi-agente que transforma texto gerado por LLMs em conteúdo
editorialmente refinado. Compatível com **Hermes Agent**, **OpenClaw**,
**Claude Code** e **Codex**. Instruções bilíngues: **inglês** e **português (pt-BR)**.

## What it does / O que faz

- **Preserves facts / preserva fatos:** entities, numbers, dates and quotes are frozen before transformation / entidades, números, datas e citações são congelados antes da transformação
- **Applies editorial engines / aplica motores editoriais:** style, structure, rhythm, lexicon, connectors, intro, context / estilo, estrutura, ritmo, léxico, conectores, introdução, contexto
- **Removes AI patterns / remove padrões de IA:** 33 catalogued patterns (clichés, repetitions, mechanical language) / 33 padrões catalogados
- **Quantitative metrics / métricas quantitativas:** readability (Flesch), diff, composite quality score / legibilidade (Flesch), diff, score composto
- **5 profiles / 5 perfis:** default (journalistic), technical, corporate, creative, minimal

## Difference from traditional humanizer / Diferença do humanizer tradicional

The original humanizer focuses on removing AI-detection patterns. ERE goes
further: it applies real editorial techniques (rhythm variation, paragraph
structure, lexical richness) to produce text with human-editor quality — not
just "undetectable". / O humanizer original foca em remover padrões de
detecção de IA. O ERE vai além: aplica técnicas editoriais reais para
produzir texto com qualidade de editor humano — não apenas "indetectável".

## Installation / Instalação

### Hermes Agent

```bash
cp -r ere/ ~/.hermes/skills/ere/
```

### OpenClaw

```bash
cp -r ere/ ~/.openclaw/skills/ere/
# or package as .skill (tar.gz of the directory)
```

### Claude Code

```bash
mkdir -p .claude/skills/ere
cp -r ere/* .claude/skills/ere/
```

### Codex

```bash
mkdir -p .agents/skills/ere
cp -r ere/* .agents/skills/ere/
```

## Usage / Uso

```
ERE: refina este texto com perfil default       (PT)
ERE: refine this text with default profile      (EN)
[text / texto]

ERE: perfil technical, nível 40                 (PT)
ERE: technical profile, level 40                (EN)
[texto técnico / technical text]

ERE: refina e analisa                           (PT)
ERE: refine and analyze                         (EN)
[text / texto]
```

## Structure / Estrutura

```
ere/
├── SKILL.md                    # Agent instructions, bilingual / instruções para o agente (bilíngue)
├── CLAUDE.md                   # Context for Claude Code / Codex (bilingual)
├── AGENTS.md                   # Workspace rules (bilingual)
├── scripts/
│   └── ere.py                 # Quantitative analysis (stdlib) / análise quantitativa
├── profiles/
│   └── default.yaml            # Editorial profiles / perfis editoriais
├── references/
│   ├── patterns.md             # 33 AI patterns / padrões de IA
│   ├── writing-principles.md   # Classics' principles / princípios dos clássicos (Gopen & Swan, Strunk & White, Othon Garcia)
│   ├── portuguese-writing-principles.md  # pt-BR language rules / regras do português pt-BR
│   └── ERE.md                  # Architecture (SDD) / SDD original
├── manifest.json               # Distribution metadata / metadados de distribuição
├── release.json                # Release changelog / changelog de releases
└── README.md
```

## Requirements / Requisitos

- Python 3.10+ (stdlib only — no external dependencies / stdlib apenas — sem dependências externas)
- Any agent harness supporting Markdown skills / qualquer harness de agente que suporte skills em Markdown

## Compatibility / Compatibilidade

| Agent / Agente | Entry file / Arquivo de entrada |
|--------------------|--------------------|
| Hermes Agent | `SKILL.md` (metadata.hermes) |
| OpenClaw | `SKILL.md` (metadata.openclaw) |
| Claude Code | `SKILL.md` + `CLAUDE.md` |
| Codex | `SKILL.md` + `AGENTS.md` |

## License / Licença

MIT
