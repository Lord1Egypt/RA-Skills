---
name: anycrawl
description: |
  Web scraping, search, crawling, and site mapping via the AnyCrawl CLI. Use when the user wants to search the web, scrape a page, find URLs on a site, or bulk extract content. Returns clean LLM-optimized markdown. Must be pre-installed and authenticated.
allowed-tools:
  - Bash(anycrawl *)
  - Bash(npx anycrawl *)
---

# AnyCrawl CLI

Web scraping, search, and crawling CLI. Returns clean markdown optimized for LLM context windows. Default engine: playwright.

Run `anycrawl --help` or `anycrawl <command> --help` for full option details.

## Prerequisites

Must be installed and authenticated. Run `anycrawl login` or set `ANYCRAWL_API_KEY`.

If not ready, see [rules/install.md](rules/install.md). For output handling guidelines, see [rules/security.md](rules/security.md).

## Commands

- **Search** - No specific URL yet. Find pages, answer questions. Use `--scrape` to get full page content with results.
- **Scrape** - Have a URL. Extract its content directly.
- **Map** - Need to locate a specific page on a site. Discover URLs, then scrape the ones you need.
- **Crawl** - Need bulk content from a site or section. Use `crawl` directly — no need for map first.

| Need                        | Command  | When                               |
| --------------------------- | -------- | ---------------------------------- |
| Find pages on a topic       | `search` | No specific URL yet                |
| Get a page's content        | `scrape` | Have a URL                         |
| Find URLs within a site     | `map`    | Need to locate a specific subpage  |
| Bulk extract a site section | `crawl`  | Need many pages (e.g., all /docs/) |

For detailed command reference, run `anycrawl <command> --help` (e.g., `anycrawl search`, `anycrawl scrape`).

**Avoid redundant fetches:** `search --scrape` already fetches full page content. Don't re-scrape those URLs. Check `.anycrawl/` for existing data before fetching again.

## Output & Organization

Write results to `.anycrawl/` with `-o`. Add `.anycrawl/` to `.gitignore`. Always quote URLs in shell commands. Never read entire output files at once — use `grep`, `head`, or incremental reads.

## Documentation

- [AnyCrawl API Docs](https://docs.anycrawl.dev)
