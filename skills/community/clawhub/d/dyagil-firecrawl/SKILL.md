---
name: dyagil-firecrawl
description: Scrape, search, map, and crawl the web for AI agents via the Firecrawl API. Use when your agent needs clean markdown from JS-heavy or SPA sites, search results with full page content, site URL mapping, or deep documentation crawls — i.e. anywhere basic HTTP fetching fails.
version: 1.0.0
license: MIT
author: dyagil
---

# Firecrawl Skill — Web Data for Agents

## Principle

Firecrawl is a managed API for the three cases where a basic `web_fetch` agent tool falls short:

1. **JS-heavy sites** — React/SPA pages that need a real browser to render.
2. **Search with full content** — standard search APIs return only snippets; Firecrawl returns rendered markdown per result.
3. **Map / Crawl** — list every URL on a site, mirror a docs tree, etc.

## When to Use

| Task | Recommended |
|---|---|
| Plain HTML article | `web_fetch` (free, fast) |
| Quick search | basic web search tool (free) |
| **JS-heavy / SPA page** | `fc scrape` |
| **Search + full content** | `fc search --scrape` |
| **Full doc-site crawl** | `fc crawl` |
| **URL inventory of a site** | `fc map` |
| **Page needing clicks / login** | `fc interact` (REST only, see below) |

**Rule of thumb:** if `web_fetch` returns empty markup or noise, escalate to `fc scrape`.

## Commands

### scrape — single page

```bash
fc scrape https://example.com                            # markdown to stdout
fc scrape https://example.com --format html --out a.html
fc scrape https://example.com --out ~/scraped/page.md
```

### search

```bash
fc search "best running shoes 2026" --limit 5
fc search "topic" --limit 3 --scrape           # include full content of each hit
fc search "..." --out results.json
```

### map — list URLs on a site

```bash
fc map https://docs.example.com --limit 200
fc map https://example.com --out urls.txt
```

### crawl — deep crawl of many pages

```bash
fc crawl https://docs.example.com --limit 50 --out ~/docs-mirror/
```

⚠️ Takes minutes. Each page = 1 credit. Don't blast it on a tight free-tier budget.

### ask / docs — debug and help

```bash
fc ask "why did my scrape return empty?" --jobId abc123
fc docs "how do I bypass cloudflare?"
```

### status

```bash
fc status   # prints key prefix + a smoke-test scrape
```

## Pricing (Remember This)

- **Free tier:** 500 credits / month.
- Each **scrape** or **search result** ≈ 1 credit.
- Each **crawl page** = 1 credit.
- Past the free tier you pay.

Before large `crawl`/`map` calls with high `--limit`, warn the user about credit cost.

## Recommended Patterns

### Pattern 1 — Regular article

```bash
# Try the free tool first.
# If it returns empty / unreadable:
fc scrape <url> --out /tmp/article.md
```

### Pattern 2 — Research on a topic

```bash
fc search "<topic>" --limit 5 --scrape --out /tmp/research.json
# Then parse the JSON and pull what you need.
```

### Pattern 3 — Whole docs site

```bash
fc map https://docs.example.com --limit 100    # get the URL list
# Pick relevant URLs and:
fc scrape <selected_urls>...
# Or in bulk:
fc crawl https://docs.example.com --limit 20 --out ~/mirror/
```

## Credentials

- **Key:** store at `~/.openclaw/credentials/firecrawl/api_key` (`chmod 600`).
- **Base URL:** `https://api.firecrawl.dev/v2`
- **Auth:** `Authorization: Bearer fc-...`
- **CLI:** `~/bin/fc` → your local `fc.cjs` (Node CommonJS, zero dependencies).

Get a key at: https://firecrawl.dev (free tier available).

## Direct REST (when the CLI isn't enough)

Example — `interact` (clicks / form-fill) which isn't wrapped in the CLI yet:

```bash
KEY=$(cat ~/.openclaw/credentials/firecrawl/api_key)
curl -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/login",
    "formats": ["markdown"],
    "actions": [
      {"type": "wait", "milliseconds": 1000},
      {"type": "click", "selector": "#login-button"},
      {"type": "write", "selector": "#email", "text": "..."}
    ]
  }'
```

Full docs: https://docs.firecrawl.dev

## Don'ts

- Don't crawl a whole site without `--limit` — credits burn fast.
- Don't reach for Firecrawl when `web_fetch` works — wasteful.
- Don't commit the API key to git.
- Don't use Firecrawl for YouTube transcripts — use a dedicated transcription tool.
