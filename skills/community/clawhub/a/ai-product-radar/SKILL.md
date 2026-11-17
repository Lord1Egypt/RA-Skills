---
name: ai-product-radar
description: One-click AI product launch monitoring pipeline. Use when tracking new AI product releases, monitoring competitor launches, generating trend reports from tech RSS feeds, or running automated product discovery. Integrates RSS monitoring, product info enrichment, screenshot capture, and trend analysis into a single command. Triggers on "product radar", "AI launch monitor", "track new AI products", "product release tracking", "AI trend report", or similar product intelligence workflows.
---

# AI Product Radar

Automated pipeline that monitors AI product launches across tech RSS feeds, enriches product data, captures screenshots, and produces a ranked trend report.

## Quick Start

```bash
python3 scripts/ai_product_radar.py --output ./radar-output
```

Output:
- `report.md` — human-readable trend report with ranked products, categories, themes
- `products.json` — full structured data (all products, scores, categories)
- `screenshots/` — product page screenshots (or info cards if no browser)
- `raw/rss_items.json` — raw feed items

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output, -o` | `./ai-radar-output` | Output directory |
| `--feeds, -f` | built-in list | JSON file with custom RSS URLs |
| `--limit, -l` | 15 | Max screenshots to capture |
| `--days, -d` | 3 | RSS lookback window |
| `--no-screenshots` | off | Skip screenshot stage |
| `--query, -q` | AI auto-detect | Filter term (narrows results) |

## Pipeline Stages

1. **RSS Monitoring** — Fetches 7 built-in feeds (Product Hunt, TechCrunch AI, The Verge AI, VentureBeat AI, HN Show, MIT Tech Review, Ars Technica), deduplicates, and filters for AI relevance via keyword matching.
2. **Product Enrichment** — Extracts product name, detects categories (LLM, image gen, dev tools, agents, enterprise, etc.), scores launch signals.
3. **Screenshot Capture** — Captures product pages with Playwright if available; falls back to generated info cards.
4. **Trend Analysis** — Ranks products by signal score + recency, aggregates category/source distributions, extracts key themes.

## Custom Feeds

Create a JSON file:
```json
["https://example.com/feed.xml", "https://another.com/rss"]
```
Then pass `--feeds my-feeds.json`.

## Scheduling

Set up a cron job for daily monitoring:
```bash
# Every day at 9:00 AM
python3 /path/to/scripts/ai_product_radar.py -o ~/radar/$(date +%Y-%m-%d)
```

## Extending

- Add RSS feeds to `DEFAULT_FEEDS` in the script or use `--feeds`.
- Adjust `AI_KEYWORDS` for broader/narrower filtering.
- Add categories in `category_patterns` inside `search_product_info()`.
- The script uses only Python stdlib + optional Playwright; no API keys required.
