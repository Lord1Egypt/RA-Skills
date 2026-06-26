---
name: firecrawl-cli
description: "Web scraping, crawling, searching, and browser automation via the Firecrawl CLI (firecrawl). Use when scraping URLs to markdown/HTML, crawling entire websites, discovering all URLs on a site, running web searches with optional scraping, launching cloud browser sessions for automation, or using the AI agent for natural-language web queries. Requires firecrawl-cli installed (npm install -g firecrawl-cli) and authentication (firecrawl login or FIRECRAWL_API_KEY env var). Triggers on: scrape URL, crawl site, map website URLs, firecrawl search, browser automation with firecrawl, web agent query."
---

# Firecrawl CLI

## Installation & Auth

```bash
npm install -g firecrawl-cli
firecrawl login --browser        # Recommended for agents
# or
export FIRECRAWL_API_KEY=fc-YOUR-KEY
firecrawl --status               # Verify: shows credits + concurrency
```

## Commands Summary

| Command | Purpose |
|---------|---------|
| `firecrawl scrape <url>` | Scrape single URL |
| `firecrawl search "<query>"` | Web search (+ optional scrape) |
| `firecrawl map <url>` | Discover all URLs on a site |
| `firecrawl crawl <url>` | Crawl entire website (async job) |
| `firecrawl browser` | Cloud browser sandbox automation |
| `firecrawl agent "<prompt>"` | NL-driven web agent queries |

## Key Patterns

**Scrape (most common):**
```bash
firecrawl https://example.com --only-main-content          # Clean markdown
firecrawl https://example.com --format markdown,links      # Multiple formats → JSON
firecrawl https://example.com -o output.md                 # Save to file
```

**Crawl a docs site:**
```bash
firecrawl crawl https://docs.example.com --limit 50 --max-depth 2 --wait --progress -o docs.json
```

**Browser automation (AI agents):**
```bash
firecrawl browser launch-session
firecrawl browser execute "open https://example.com"
firecrawl browser execute "snapshot"     # Returns @ref IDs
firecrawl browser execute "click @e5"
firecrawl browser execute "scrape"
firecrawl browser close
```

**AI agent query:**
```bash
firecrawl agent "Find top 5 AI startups and funding" --wait
firecrawl agent "Compare pricing" --urls https://a.com,https://b.com --wait
```

## Full Reference

See [references/commands.md](references/commands.md) for all commands, options, and examples.

## Tips

- Use `--only-main-content` for clean article content (removes nav/footer)
- `crawl` returns a job ID immediately — use `--wait` to block or poll with job ID later
- Browser `execute` default mode is agent-browser (bash) — 40+ commands, best for agents
- `spark-1-mini` (default) is 60% cheaper than `spark-1-pro` for agent queries
- Check concurrency limit with `--status` before parallelizing scrape jobs
- Self-hosted instances skip API key auth automatically when `--api-url` is set
