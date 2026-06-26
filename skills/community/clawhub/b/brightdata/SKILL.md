---
name: brightdata
description: Google search results and web page scraping via Bright Data APIs. Use when the agent needs structured search results, paginated SERP retrieval, or clean markdown from any URL.
version: 1.0.0
metadata:
  openclaw:
    skillKey: brightdata
    emoji: "🔍"
    requires:
      bins:
        - bash
        - curl
        - sed
      env:
        - BRIGHTDATA_API_KEY
        - BRIGHTDATA_SERP_ZONE
        - BRIGHTDATA_UNLOCKER_ZONE
    primaryEnv: BRIGHTDATA_API_KEY
---

# Bright Data — Web Search & Scraping

Two tools: **search** (Google SERP results as JSON) and **scrape** (any URL to clean markdown). Both bypass bot detection and CAPTCHAs.

## Tools

### `search.sh` — Google Search
```bash
bash scripts/search.sh "<query>" [cursor]
```
- `query`: Search terms (required).
- `cursor`: Page number, 0-indexed (optional, default `0`). Each page returns ~10 results.

**Returns** JSON with an `organic` array:
```json
{
  "organic": [
    {"link": "https://...", "title": "...", "description": "..."}
  ]
}
```

### `scrape.sh` — Web Page Scraping
```bash
bash scripts/scrape.sh "<url>"
```
- `url`: Any public URL (required).

**Returns** the page content as clean markdown.

## Agent Strategy Guide

### When to search
- You need to discover URLs, find information across the web, or locate specific pages.
- Always craft **specific, targeted queries**. Include key terms, dates, or domain constraints. Vague single-word queries waste API calls and return noise.
- Good: `"site:github.com openai whisper python library"`
- Bad: `"AI"`

### When to scrape
- You already have a URL and need its full content (not just the snippet from search).
- The search result snippet is insufficient to answer the user's question.
- You need to extract structured data, read documentation, or parse a specific page.

### When to paginate
- The current page of search results has relevant hits but you need more. Increment `cursor` (0 → 1 → 2 → ...).
- Stop paginating when results become irrelevant to the query or you have enough information to proceed.

### When to stop
- You have gathered enough information to answer the user's question — do not over-fetch.
- Search results have become irrelevant (diminishing returns after 2-3 pages is typical).
- A scrape returns an error or empty content — skip that URL and move on, do not retry.

### General principles
- **Search first, scrape second.** Use search to find the right URLs, then scrape only the promising ones.
- **Be specific in queries.** The more precise your search query, the fewer API calls you need.
- **Summarize as you go.** After each search or scrape, extract what you need immediately rather than batching all processing to the end.
