# OpenClaw GEO Content Ops

> Languages: [简体中文](../../README.md) | [English](README_en.md) | [日本語](README_ja.md) | [Español](README_es.md) | [Русский](README_ru.md) | [Português (BR)](README_pt_BR.md)

> OpenClaw GEO Content Ops は、GEO（Generative Engine Optimization）を継続的なコンテンツ資産運用として扱うための軽量 Skill と運用モデルです。信頼できる知識ソース、topic clusters、content tasks、AI Search 向け執筆、SEO/GEO workflow receipts、公開先、LLM-friendly artifacts、visibility analytics をひとつの監査可能なループに接続します。

[![Skill](https://img.shields.io/badge/OpenClaw-Skill-0F766E)](#quick-start)
[![GEO](https://img.shields.io/badge/GEO-Content%20Ops-blue)](#what-it-does)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

MIT License で公開されています。

---

## What It Does

| Layer | 管理するもの |
| --- | --- |
| Knowledge sources | ブランド文書、製品事実、receipts、URL、顧客メモ、競合メモ、wiki ページ |
| Topic clusters | 質問、キーワード、エンティティ、比較軸、FAQ の長期マップ |
| Content tasks | 読者、核心クエリ、source evidence、公開範囲、成功指標をつなぐ brief |
| Writing handoff | AI Search 向け執筆との境界を明確にし、引用しやすい記事にする |
| SEO/GEO workflow | Hunter/Tony/Peter の実行、publish gates、receipts との境界 |
| Publication targets | ClawLite blog、WordPress REST、static GEO site、X posts、Feishu docs |
| GEO artifacts | `llms.txt`、sitemap、TXT maps、Schema、Open Graph、canonical URLs |
| Receipts | 生成、監査、公開、deploy、live QA、patrol、analytics の証拠 |
| Visibility analytics | AI crawler hits、indexing、citation checks、top content、rescue tasks |

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

本番公開、indexing、AI crawler visits、ranking、AI citation は receipt なしで主張しないでください。

---

## License

MIT
