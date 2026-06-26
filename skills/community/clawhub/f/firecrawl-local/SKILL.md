---
name: firecrawl-local
description: |
  Use this skill whenever you need to scrape web pages, crawl websites, or map site
  structure using a self-hosted Firecrawl instance. Triggers on requests to extract
  web content, build RAG pipelines from docs, bulk ingest documentation, discover
  site URLs, or get clean markdown from any webpage. Assumes Firecrawl is already
  running at localhost:3002 (no Docker startup). Falls back gracefully if unavailable.
  Use even if the user just says "scrape this", "crawl the docs", or "get content from X".
tags: [web-scraping, rag, documentation, local-first]
---

# Firecrawl Local Skill

Self-hosted Firecrawl integration using the **v1 REST API**. Tests connectivity first, 
executes scrape/crawl/map, handles async crawl polling automatically.

## Setup (one-time)

```bash
mkdir -p ~/.openclaw/skills/firecrawl-local
cp run.sh ~/.openclaw/skills/firecrawl-local/run.sh
chmod +x ~/.openclaw/skills/firecrawl-local/run.sh
```

The script lives at `scripts/run.sh` in this skill folder — copy it into place as above.

**Prerequisites:** `curl`, `jq` installed. Firecrawl running at `localhost:3002`.

**Optional env vars:**
```bash
export FIRECRAWL_LOCAL_URL="http://localhost:3002"  # default
export FIRECRAWL_API_KEY="fc-your-key"              # only needed if auth enabled
```

---

## Commands

### Default — scrape a single page (URL only, no subcommand needed)
```bash
firecrawl-local https://docs.example.com/api
```

### Scrape — explicit, with format options
```bash
firecrawl-local scrape https://docs.example.com/api
firecrawl-local scrape https://docs.example.com/api --formats markdown,html
```

### Map — discover all URLs on a site
```bash
firecrawl-local map https://docs.example.com
firecrawl-local map https://docs.example.com --limit 200
```

### Crawl — bulk extract multiple pages (async, auto-polled)
```bash
firecrawl-local crawl https://docs.example.com
firecrawl-local crawl https://docs.example.com --limit 30 --max-depth 2
firecrawl-local crawl https://docs.example.com --include /docs --exclude /blog
```

---

## Agent Instructions

### When to use each command

| Goal | Command |
|------|---------|
| Get content from one URL (quickest) | `firecrawl-local <url>` |
| Discover what pages exist | `map` |
| Get content from one URL with format control | `scrape` |
| Ingest an entire docs site | `crawl` |
| RAG pipeline ingestion | `map` → targeted `scrape` or `crawl` |

### Optimal workflows

**Documentation RAG pipeline:**
```
1. map https://docs.example.com          → get full URL list
2. scrape <specific key pages>           → targeted extraction
3. Pass markdown to embedding pipeline
```

**Full site ingestion:**
```
1. crawl https://docs.example.com --limit 50 --max-depth 3
2. Results auto-polled and returned as JSON array of {url, markdown}
```

### Parameters

| Flag | Applies to | Description |
|------|-----------|-------------|
| `--limit N` | map, crawl | Max pages (default: 50 for crawl, 500 for map) |
| `--max-depth N` | crawl | How deep to follow links (default: 2) |
| `--include /path` | crawl | Only crawl URLs matching this path prefix |
| `--exclude /path` | crawl | Skip URLs matching this path prefix |
| `--formats list` | scrape | Comma-separated: `markdown`, `html`, `rawHtml`, `links` |

### Reading the output

- **scrape**: Returns `{success, data: {markdown, html, metadata}}`
- **map**: Returns `{success, links: [...]}`
- **crawl**: Returns `{success, data: [{url, markdown, metadata}, ...]}`  ← after polling completes

### Failure signals and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Local Firecrawl unavailable` | Service not running | Start Firecrawl, check port 3002 |
| `success: false` | Bad URL or blocked | Check URL is reachable, try `--formats html` |
| Empty `markdown` field | JS-rendered page | Firecrawl handles most JS — check if site blocks bots |
| Crawl times out | Site is large | Reduce `--limit` or `--max-depth` |

---

## Script reference

See `scripts/run.sh` for the full implementation. Key design decisions:
- Health check uses `/health` endpoint with 3s timeout
- Auth header only sent when `FIRECRAWL_API_KEY` is set
- Crawl polling retries every 5s up to 60 attempts (5 minutes)
- All parameters are passed via `jq` to prevent shell injection in JSON
