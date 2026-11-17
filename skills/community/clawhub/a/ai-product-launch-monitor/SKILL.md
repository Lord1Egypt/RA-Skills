---
name: ai-product-launch-monitor
description: "One-command AI product launch monitoring pipeline. Use when the user wants to track, discover, or analyze new AI product launches, releases, or announcements. Runs four stages automatically - RSS feed monitoring, web search enrichment, page screenshots, and trend analysis/scoring. Outputs a markdown report and structured JSON. Triggers on phrases like monitor AI product launches, track AI releases, AI launch report, what new AI products launched, product hunt AI monitoring, AI news roundup."
---

# AI Product Launch Monitor

End-to-end pipeline that collects AI product launches from RSS feeds, enriches them with web search, captures screenshots, and scores trends — all in one command.

## Quick Start

```bash
python3 scripts/monitor.py --output ./output -v
```

This runs all four stages and produces `output/report.md` + `output/launches.json`.

## Pipeline Stages

| Stage | What it does |
|-------|-------------|
| 1. RSS monitoring | Fetches AI/tech RSS feeds, filters for launch signals, dedupes |
| 2. Product search | Enriches each launch with web search results (Brave API or DDG fallback) |
| 3. Screenshots | Headless Chromium screenshots of each product page via Playwright |
| 4. Trend analysis | Categorizes, scores, and ranks launches; generates report |

## Usage

```bash
# Default run (3-day lookback, all stages)
python3 scripts/monitor.py --output ./output

# Custom lookback window
python3 scripts/monitor.py --days 7 --output ./weekly

# Use a config file
python3 scripts/monitor.py --config assets/default-config.json --output ./output

# Override feeds
python3 scripts/monitor.py --feeds https://example.com/feed.xml https://other.com/rss

# Skip screenshots (faster, no browser needed)
python3 scripts/monitor.py --no-screenshots --output ./quick

# Verbose mode
python3 scripts/monitor.py -v --output ./output
```

## Configuration

Copy `assets/default-config.json` and customize:

```json
{
  "feeds": ["https://..."],
  "query_terms": ["AI product launch"],
  "days": 3
}
```

### Environment Variables

- `BRAVE_API_KEY` — set to use Brave Search API (better results). Without it, falls back to DuckDuckGo HTML scraping.

## Output

- **`report.md`** — human-readable trend report with category breakdown, top launches, and full entry list
- **`launches.json`** — structured data for downstream automation
- **`screenshots/*.png`** — page screenshots (named by URL hash)

## Dependencies

- Python 3.10+
- `feedparser`, `requests`, `beautifulsoup4` (auto-installed)
- `playwright` + Chromium (for screenshots; skip with `--no-screenshots`)

Install Playwright browsers:
```bash
python3 -m playwright install chromium
```

## How Scoring Works

Each launch gets a trend score (0–100+):
- **+30** — strong launch keyword in title/summary
- **+5 per search result** (max 25) — external corroboration
- **+10** — screenshot captured (page was reachable)
- **Recency bonus** — newer launches score higher (up to +35)

Categories: LLM/Foundation Models, Image/Video Gen, Agent/Automation, Developer Tools, Enterprise/B2B, Consumer/App, Healthcare/Science, Other.

## Agent Integration

When using this skill in an agent workflow:

1. Run the script with `--output` pointing to a temp or workspace directory
2. Read `report.md` for a summary to present to the user
3. Parse `launches.json` for structured data (e.g., filtering by category or score threshold)
4. Screenshots can be attached or referenced in responses
