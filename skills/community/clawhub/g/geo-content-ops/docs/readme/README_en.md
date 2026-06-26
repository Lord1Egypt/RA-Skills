# OpenClaw GEO Content Ops

> Languages: [简体中文](../../README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Español](README_es.md) | [Русский](README_ru.md) | [Português (BR)](README_pt_BR.md)

> OpenClaw GEO Content Ops is a lightweight skill and operating model for GEO (Generative Engine Optimization). It connects trusted knowledge sources, topic clusters, content tasks, AI-search writing, SEO/GEO workflow receipts, publication targets, LLM-friendly artifacts, and visibility analytics into one auditable content-asset loop.

[![Skill](https://img.shields.io/badge/OpenClaw-Skill-0F766E)](#quick-start)
[![GEO](https://img.shields.io/badge/GEO-Content%20Ops-blue)](#what-it-does)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

Released under the [MIT License](../../LICENSE).

---

## What It Does

| Layer | What it manages |
| --- | --- |
| Knowledge sources | Brand docs, product facts, receipts, URLs, customer notes, competitor notes, and wiki pages |
| Topic clusters | Durable question, keyword, entity, comparison, and FAQ maps |
| Content tasks | Briefs that connect reader, core query, source evidence, publish scope, and success signals |
| Writing handoff | Boundary with AI-search writing so each article is answer-first, citeable, and extractable |
| SEO/GEO workflow | Boundary with Hunter/Tony/Peter delivery, publish gates, and receipts |
| Publication targets | ClawLite blog, WordPress REST, static GEO sites, X posts, Feishu docs, and future providers |
| GEO artifacts | `llms.txt`, sitemap, TXT maps, Schema, Open Graph, canonical URLs, and evidence blocks |
| Receipts | Evidence for generation, audit, publish, deploy, live QA, patrol, and analytics |
| Visibility analytics | AI crawler hits, indexing state, sitemap coverage, citation checks, top content, stale pages, and rescue tasks |

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

## How It Coordinates Skills

| Skill | Owns |
| --- | --- |
| `openclaw-geo-content-ops` | Sources, topics, tasks, targets, artifacts, receipts, analytics |
| `openclaw-seo-geo-workflow` | Daily Hunter/Tony/Peter execution, publish gates, receipts, patrol |
| `ai-search-visibility-content-writing` | Single-page quality, direct answer, entity clarity, citeable structure |
| `claw-wiki` | Readable wiki pages generated from canonical sources |

---

## Quick Start

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/X-RayLuan/openclaw-geo-content-ops.git ~/.codex/skills/openclaw-geo-content-ops
```

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/X-RayLuan/openclaw-geo-content-ops.git ~/.openclaw/workspace/skills/openclaw-geo-content-ops
```

Use:

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

Do not claim production publish, indexing, AI crawler visits, rankings, or AI citations without receipts.

---

## License

MIT
