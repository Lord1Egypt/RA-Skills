# OpenClaw GEO Content Ops

> Languages: [简体中文](../../README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Español](README_es.md) | [Русский](README_ru.md) | [Português (BR)](README_pt_BR.md)

> OpenClaw GEO Content Ops — это легкий skill и операционная модель для GEO (Generative Engine Optimization). Он связывает надежные источники знаний, topic clusters, задачи контента, AI Search writing, receipts SEO/GEO workflow, цели публикации, LLM-friendly artifacts и visibility analytics в один проверяемый цикл.

[![Skill](https://img.shields.io/badge/OpenClaw-Skill-0F766E)](#quick-start)
[![GEO](https://img.shields.io/badge/GEO-Content%20Ops-blue)](#what-it-does)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

Проект распространяется по лицензии [MIT](../../LICENSE).

---

## What It Does

| Layer | Что управляет |
| --- | --- |
| Knowledge sources | Документы бренда, факты продукта, receipts, URL, заметки клиентов, конкуренты и wiki |
| Topic clusters | Устойчивые карты вопросов, keywords, entities, сравнений и FAQ |
| Content tasks | Briefs, связывающие читателя, запрос, evidence, publish scope и success signals |
| Writing handoff | Граница с AI Search writing: прямой ответ, ясные entities, цитируемая структура |
| SEO/GEO workflow | Граница с Hunter/Tony/Peter, publish gates, receipts и patrol |
| Publication targets | ClawLite blog, WordPress REST, static GEO sites, X posts, Feishu docs |
| GEO artifacts | `llms.txt`, sitemap, TXT maps, Schema, Open Graph и canonical URLs |
| Receipts | Evidence для generation, audit, publish, deploy, live QA, patrol и analytics |
| Visibility analytics | AI crawler hits, indexing, citation checks, top content и rescue tasks |

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

Не заявляйте production publish, indexing, AI crawler visits, rankings или AI citations без receipts.

---

## License

MIT
