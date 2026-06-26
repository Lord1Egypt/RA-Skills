# OpenClaw GEO Content Ops

> Languages: [简体中文](../../README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Español](README_es.md) | [Русский](README_ru.md) | [Português (BR)](README_pt_BR.md)

> OpenClaw GEO Content Ops é uma skill leve e um modelo operacional para GEO (Generative Engine Optimization). Ela conecta fontes confiáveis, topic clusters, tarefas de conteúdo, escrita para AI Search, receipts do workflow SEO/GEO, destinos de publicação, artifacts compatíveis com LLM e analytics de visibilidade em um ciclo auditável.

[![Skill](https://img.shields.io/badge/OpenClaw-Skill-0F766E)](#quick-start)
[![GEO](https://img.shields.io/badge/GEO-Content%20Ops-blue)](#what-it-does)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

Publicado sob a [MIT License](../../LICENSE).

---

## What It Does

| Layer | O que gerencia |
| --- | --- |
| Knowledge sources | Docs de marca, fatos do produto, receipts, URLs, notas de clientes, concorrentes e wiki |
| Topic clusters | Mapas duráveis de perguntas, keywords, entidades, comparações e FAQ |
| Content tasks | Briefs que conectam leitor, pergunta central, evidência, escopo de publicação e sinais de sucesso |
| Writing handoff | Fronteira com escrita para AI Search: resposta direta, entidades claras e estrutura citável |
| SEO/GEO workflow | Fronteira com Hunter/Tony/Peter, publish gates, receipts e patrol |
| Publication targets | ClawLite blog, WordPress REST, static GEO sites, X posts, Feishu docs |
| GEO artifacts | `llms.txt`, sitemap, TXT maps, Schema, Open Graph e canonical URLs |
| Receipts | Evidência para geração, auditoria, publicação, deploy, live QA, patrol e analytics |
| Visibility analytics | AI crawler hits, indexing, citation checks, top content e rescue tasks |

---

## Running Structure

```text
knowledge_sources
    ↓
topic_clusters
    ↓
content_tasks
    ↓
AI-search content writing
    ↓
SEO/GEO workflow receipts
    ↓
publication_targets
    ↓
GEO artifacts
    ↓
visibility analytics
    ↓
source/wiki promotion
```

---

## Quick Start

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/X-RayLuan/openclaw-geo-content-ops.git ~/.codex/skills/openclaw-geo-content-ops
```

```text
Use openclaw-geo-content-ops to design this week's GEO content operating plan.
```

---

## Core Contracts

- Source catalog: `examples/sources.example.jsonl`
- Task brief: `examples/task.example.json`
- Receipt contract: `examples/receipt.example.json`
- Integration notes: `references/openclaw-integration.md`
- GEOFlow patterns: `references/geoflow-patterns.md`

Não declare publicação em produção, indexing, AI crawler visits, rankings ou AI citations sem receipts.

---

## License

MIT
