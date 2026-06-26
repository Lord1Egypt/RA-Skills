# OpenClaw GEO Content Ops

> Languages: [简体中文](../../README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Español](README_es.md) | [Русский](README_ru.md) | [Português (BR)](README_pt_BR.md)

> OpenClaw GEO Content Ops es una skill ligera y un modelo operativo para GEO (Generative Engine Optimization). Conecta fuentes confiables, topic clusters, tareas de contenido, escritura para AI Search, receipts del workflow SEO/GEO, destinos de publicación, artifacts compatibles con LLM y analytics de visibilidad en un ciclo auditable.

[![Skill](https://img.shields.io/badge/OpenClaw-Skill-0F766E)](#quick-start)
[![GEO](https://img.shields.io/badge/GEO-Content%20Ops-blue)](#what-it-does)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

Publicado bajo la [MIT License](../../LICENSE).

---

## What It Does

| Layer | Qué gestiona |
| --- | --- |
| Knowledge sources | Documentos de marca, hechos de producto, receipts, URLs, notas de clientes, competidores y wiki |
| Topic clusters | Mapas duraderos de preguntas, keywords, entidades, comparaciones y FAQ |
| Content tasks | Briefs que conectan lector, pregunta, evidencia, alcance de publicación y señales de éxito |
| Writing handoff | Límite con escritura para AI Search: respuesta directa, entidades claras y estructura citable |
| SEO/GEO workflow | Límite con Hunter/Tony/Peter, publish gates, receipts y patrol |
| Publication targets | ClawLite blog, WordPress REST, static GEO sites, X posts, Feishu docs |
| GEO artifacts | `llms.txt`, sitemap, TXT maps, Schema, Open Graph y canonical URLs |
| Receipts | Evidencia de generación, auditoría, publicación, deploy, live QA, patrol y analytics |
| Visibility analytics | AI crawler hits, indexing, citation checks, top content y rescue tasks |

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

No declares publicación en producción, indexing, AI crawler visits, rankings o AI citations sin receipts.

---

## License

MIT
