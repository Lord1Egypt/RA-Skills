---
name: ai-product-monitor
description: One-click AI product launch monitoring pipeline — RSS monitoring, product info search, screenshot capture, and trend analysis. Run the full workflow or individual stages.
version: 1.0.0
author: openclaw
tags: [rss, ai, product-launch, monitoring, screenshot, trend-analysis, pipeline]
requires_bins: [python3]
requires_env: []
requires_config: []
---

# AI Product Monitor

One-click pipeline that runs four stages sequentially:

1. **RSS Monitor** — Fetch configured RSS feeds, extract AI product launch posts
2. **Product Search** — Enrich each launch with web search details
3. **Screenshot Capture** — Take screenshots of product landing pages
4. **Trend Analysis** — Analyze launch trends and generate a summary report

## Quick Start (Full Pipeline)

```bash
python3 scripts/pipeline.py
```

## Individual Stages

```bash
# Stage 1 only — RSS monitoring
python3 scripts/pipeline.py --stage rss

# Stage 2 only — Product info search
python3 scripts/pipeline.py --stage search

# Stage 3 only — Screenshot capture
python3 scripts/pipeline.py --stage screenshot

# Stage 4 only — Trend analysis
python3 scripts/pipeline.py --stage trends
```

## Configuration

Edit `references/feeds.yaml` to customize RSS sources. Default feeds include OpenAI, Google AI, Anthropic, Meta AI, and Hugging Face blogs.

## Output

| File | Description |
|------|-------------|
| `data/raw_launches.json` | Raw RSS items from stage 1 |
| `data/enriched_launches.json` | Launches with search-enriched info |
| `data/screenshots/` | Landing page screenshots (PNG) |
| `data/trend_report.md` | Final trend analysis report |

## Pipeline Flow

```
RSS Feeds → raw_launches.json → enriched_launches.json → screenshots/ → trend_report.md
```

Each stage reads the previous stage's output, so stages can be re-run independently after editing earlier results.