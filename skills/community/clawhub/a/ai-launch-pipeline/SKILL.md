---
name: ai-launch-pipeline
description: One-click automated pipeline for AI product launch monitoring — RSS monitoring, product search enrichment, screenshot capture, and trend analysis
version: 1.0.0
author: ClawdBot
tags: [rss, ai, product-launches, pipeline, automation, monitoring, trends]
requires_bins: [python3]
requires_env: []
requires_config: [config/rss_feeds.yaml]
---

# AI Launch Pipeline

One-click end-to-end workflow for monitoring AI product launches. Runs four stages in sequence: RSS monitoring → product search → screenshot capture → trend analysis.

## Quick Start

```bash
# Full pipeline (one click)
python scripts/run_pipeline.py

# Skip screenshot stage (no Playwright needed)
python scripts/run_pipeline.py --skip-screenshot

# Run a single stage
python scripts/run_pipeline.py --stage rss
python scripts/run_pipeline.py --stage search
python scripts/run_pipeline.py --stage screenshot
python scripts/run_pipeline.py --stage analysis
```

## Stages

| # | Stage | What it does | Output |
|---|-------|-------------|--------|
| 1 | RSS Monitor | Fetches configured RSS feeds, detects new AI launch posts | `data/raw_launches.json` |
| 2 | Product Search | Enriches each launch with DuckDuckGo search results | `data/enriched_launches.json` |
| 3 | Screenshot | Captures full-page screenshots of product pages (optional) | `screenshots/*.png`, `data/screenshot_results.json` |
| 4 | Trend Analysis | Identifies keywords, top organizations, source distribution | `analysis/trends.json`, `analysis/launch_analysis_report.md` |

## Configuration

Edit `config/rss_feeds.yaml` to add or remove RSS feeds:

```yaml
feeds:
  - name: OpenAI Blog
    url: https://openai.com/blog/rss.xml
    category: llm
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PIPELINE_BASE_DIR` | skill root | Base directory for all outputs |
| `PIPELINE_DATA_DIR` | `{BASE}/data` | JSON data output directory |
| `PIPELINE_SCREENSHOT_DIR` | `{BASE}/screenshots` | Screenshot output directory |
| `PIPELINE_ANALYSIS_DIR` | `{BASE}/analysis` | Analysis report directory |
| `PIPELINE_CONFIG` | `config/rss_feeds.yaml` | RSS feed config path |

## Dependencies

- **Python 3.10+**
- **PyYAML** — `pip install pyyaml`
- **Playwright** (optional, for screenshots) — `pip install playwright && playwright install chromium`

## Output

After a full run:
```
data/
  raw_launches.json          # Stage 1 output
  seen_ids.json              # Dedup state
  enriched_launches.json     # Stage 2 output
  screenshot_results.json    # Stage 3 output
screenshots/
  *.png                      # Captured screenshots
analysis/
  trends.json                # Structured trend data
  launch_analysis_report.md  # Human-readable report
```

## Scheduling

Pair with OpenClaw cron for automated daily runs:

```bash
# Add via cron tool
schedule: { kind: "cron", expr: "0 8 * * *" }
payload: { kind: "agentTurn", message: "Run the AI launch pipeline: python ~/.openclaw/skills/ai-launch-pipeline/scripts/run_pipeline.py --skip-screenshot, then summarize the analysis report." }
```
