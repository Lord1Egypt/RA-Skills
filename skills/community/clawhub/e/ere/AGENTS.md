# AGENTS.md — ERE Workspace Rules

This directory contains the **ERE (Editorial Refinement Engine)** skill — a
9-stage pipeline that turns LLM text into quality editorial prose, preserving
facts, entities and quotes. Bilingual: English and Portuguese (pt-BR). /
Este diretório contém a skill **ERE (Editorial Refinement Engine)** — um
pipeline de 9 etapas para transformar texto de LLM em prosa editorial de
qualidade, preservando fatos, entidades e citações. Bilíngue: inglês e
português (pt-BR).

## What this repo is / O que é este repositório

- `SKILL.md` — full pipeline instructions for the agent / instruções completas do pipeline para o agente
- `scripts/ere.py` — quantitative analysis (Python stdlib, zero deps) / análise quantitativa (stdlib Python, zero deps)
- `profiles/default.yaml` — 5 configurable editorial profiles / 5 perfis editoriais configuráveis
- `references/patterns.md` — 33 "AI writing" patterns to avoid / 33 padrões de "AI writing" a evitar
- `references/writing-principles.md` — classics' writing principles (Gopen & Swan, Strunk & White, Othon Garcia) / princípios dos clássicos de escrita
- `references/portuguese-writing-principles.md` — pt-BR specific language rules (Othon Garcia) / regras específicas do português pt-BR
- `references/ERE.md` — SDD / architecture document / documento de arquitetura
- `CLAUDE.md` — context for Claude Code / Codex
- `README.md` — public documentation / documentação pública

## Rules when using this skill / Regras ao usar esta skill

1. **Never alter the reference files unnecessarily** — they are the skill's calibration source / **nunca altere os arquivos de referência sem necessidade** — são a fonte de calibração da skill.
2. **`ere.py` is read-only by design** (analyzes, never modifies text) / **o script `ere.py` é read-only por design** (analisa, não modifica texto).
3. **No secrets in this directory.** If the skill is distributed, credentials come via environment variables, never in files / **não armazene segredos** neste diretório.
4. **Language / idioma:** the skill instructions are bilingual (EN + PT); the refinement target can be English or Portuguese. The pt-BR catalogue is necessarily in Portuguese because it describes Portuguese language rules / as instruções são bilíngues (EN + PT); o alvo do refinamento pode ser inglês ou português. O catálogo pt-BR é necessariamente em português porque descreve regras da língua portuguesa.
5. If you find a bug in `ere.py`, fix it and add a test case — never remove functionality silently / ao encontrar um bug no `ere.py`, corrija e adicione um caso de teste — nunca remova funcionalidade silenciosamente.

## Quick verification / Verificação rápida

```bash
python3 scripts/ere.py profile default   # JSON with the profile / deve imprimir JSON com o perfil
python3 scripts/ere.py analyze arquivo.txt  # quality metrics / métricas de qualidade
```

Both must exit with code 0 / ambos devem sair com exit code 0.
