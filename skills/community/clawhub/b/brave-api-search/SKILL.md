---
name: brave-api-search
description: Real-time web search, autosuggest, and AI-powered answers using the official Brave Search API. Use for searching documentation, facts, current events, or any web content. Supports AI grounded answers with citations and query autosuggest. Requires BRAVE_SEARCH_API_KEY and BRAVE_ANSWERS_API_KEY.
license: MIT
metadata:
  author: Broedkrummen
  version: 4.2.0
---

# Brave API Search v4.2.0 — Significant Update

Real-time web search, autosuggest, spellcheck, and AI-powered answers using the official Brave Search API. Four tools:
- `brave_search` — web results with titles, URLs, descriptions, optional AI summary
- `brave_suggest` — query autosuggestions as users type with optional rich metadata
- `brave_spellcheck` — spell correction and "Did you mean?" suggestions
- `brave_answers` — AI-grounded answers with inline citations powered by live web search
  | **NEW — v4.2.0:** Full entity extraction via `enable-entities` flag

## Setup

Set your Brave API keys in a local `.env` file (recommended):

```bash
# .env (do not commit)
BRAVE_SEARCH_API_KEY=your_key_here
BRAVE_ANSWERS_API_KEY=your_key_here
AUTOSUGGEST_API_KEY=your_key_here   # optional, for autosuggest only
BRAVE_SPELLCHECK_API_KEY=your_key_here   # optional, for spellcheck only
```

Get your keys at: https://api-dashboard.search.brave.com

**Key routing:**
- `brave_search` → `BRAVE_SEARCH_API_KEY`
- `brave_answers` → `BRAVE_ANSWERS_API_KEY`
- `brave_suggest` → `AUTOSUGGEST_API_KEY` → `BRAVE_AUTOSUGGEST_API_KEY` → `BRAVE_SEARCH_API_KEY` (tries in order)
- `brave_spellcheck` → `BRAVE_SPELLCHECK_API_KEY` → `BRAVE_SEARCH_API_KEY` (tries in order)

> Note: `brave_answers` uses streaming by default. Streaming is required for citations, entities, and research mode.

## When to Use This Skill

**Use `brave_search` when:**
- Searching for current information, news, or recent events
- Looking up documentation or technical references
- Need ranked results with URLs to follow up on
- Want an AI summary of search results

**Use `brave_suggest` when:**
- Power autocomplete in search interfaces
- Help users formulate better queries faster
- Need query completions as users type
- Want rich metadata (titles, descriptions, images) for suggestions

**Use `brave_answers` when:**
- Need a synthesized answer with cited sources
- Researching topics that benefit from multiple sources
- Want AI-grounded responses with inline citations
- Deep research mode needed (multi-search)

**Don't use this skill for:**
- Questions already answered from context or memory
- Tasks that don't require external information

## Tools

### brave_search

Web search returning ranked results with titles, URLs, and descriptions.

```bash
brave_search --query "latest Node.js release" --count 5
brave_search --query "TypeScript generics" --extra-snippets true
brave_search --query "current weather Copenhagen" --freshness pd
brave_search --query "React Server Components" --summary true
```

**Parameters:**
- `query` (required) — Search query, supports operators: `site:`, `"exact phrase"`, `-exclude`
- `count` — Results to return (1-20, default: 10)
- `country` — 2-letter country code (default: `us`)
- `freshness` — Date filter: `pd` (24h), `pw` (7 days), `pm` (31 days), `py` (1 year)
- `extra-snippets` — Include up to 5 extra text excerpts per result (default: false)
- `summary` — Fetch Brave AI summarizer result (default: false)
- `offset` — Pagination offset for next page results

**Returns:** Formatted list of results with title, URL, description, optional AI summary, and a hint for next page if `more_results_available`.

### brave_suggest

Query autosuggest API providing intelligent query autocompletion as users type.

```bash
brave_suggest --query "hello"
brave_suggest --query "pyt" --count 5 --country US
brave_suggest --query "einstein" --rich true
```

**Parameters:**
- `query` (required) — Partial query to get suggestions for
- `count` — Number of suggestions (1-10, default: 5)
- `country` — 2-letter country code (default: `US`)
- `rich` — Include enhanced metadata: titles, descriptions, images, entity detection (default: false, requires paid Autosuggest plan)

**Returns:** List of query suggestions, optionally with rich metadata. Results are cached for 60 seconds.

**Best Practices:**
- Implement debouncing (150-300ms) to avoid excessive API calls as users type
- Load suggestions asynchronously without blocking the UI

### brave_spellcheck

Spell checking and query correction for search queries.

```bash
brave_spellcheck --query "articifial inteligence"
brave_spellcheck --query "hello" --country US
```

**Parameters:**
- `query` (required) — Query to check for spelling errors
- `country` — 2-letter country code (default: `US`)

**Returns:** "Did you mean:" suggestion, or confirms no correction needed. Uses dedicated `BRAVE_SPELLCHECK_API_KEY` if available, falls back to `BRAVE_SEARCH_API_KEY`.


### brave_answers

AI-powered answers grounded in live web search with inline citations.

```bash
brave_answers --query "How does React Server Components work?"
brave_answers --query "Compare Postgres vs MySQL for OLAP" --enable-research true
brave_answers --query "Latest Python release notes" --enable-citations true
brave_answers --query "Who is Albert Einstein" --enable-entities true
```

**Parameters:**
- `query` (required) — Question or topic to research
- `country` — Target country for search context (default: `us`)
- `enable-citations` — Include inline source citations (default: true)
- `enable-research` — Multi-search deep research mode (default: false)
- `enable-entities` — Include entity information in responses (default: false, streaming required)
- `stream` — Enable streaming output (default: true — required for citations/entities/research)

**Returns:** AI answer with cited sources extracted from the response, plus token usage and cost breakdown.

> ⚠️ **Citations, entities, and research mode require streaming (`--stream true`, which is the default).** If you disable streaming with `--stream false`, citations and entity data will not be available.

**Streaming mode output:**
- Text streams progressively to stdout
- Entities streamed inline as `<enum_item>` tags are parsed
- **Entities mentioned** section printed at the end (v4.2.0)
- Sources printed at the end (sorted by citation number)
- Token usage and cost breakdown included

**Non-streaming fallback:** Use `--stream false` for simpler output at the cost of losing citations and entity data.

## Pricing & Limits

Brave pricing is credit-based and can change. Do **not** assume a fixed free request count.

Current public guidance (verify in Brave dashboard/docs before production use):
- Monthly trial credits may be offered (e.g. `$5 in monthly credits`)
- Search and Answers consume credits differently
- Rich suggestions require a paid Autosuggest plan
- Answers may also include token-based costs
- QPS limits depend on your plan tier

Always check your live limits and usage in:
- https://api-dashboard.search.brave.com
- https://brave.com/search/api/

## Technical Details

### Architecture

The skill uses a shared `utils.js` module containing:
- `parseArgs()` — CLI argument parser
- `fetchWithRetry()` — fetch with exponential backoff retry on 429 and 5xx
- `createCache()` — in-memory TTL cache (used by `brave_suggest`)

### brave_search.js

The core search script with the following optimizations:
- **Parallel summary fetch:** When `--summary` is enabled, the summary key is extracted from the search response and fetched in parallel with the search results
- **Pagination hint:** Response includes a hint for the next page offset when `more_results_available` is true
- **Rate limit handling:** Retries on 429 (honors `Retry-After` header) and 5xx (exponential backoff)

### brave_answers.js v4.2.0

The AI answers script supports two modes:
- **Streaming (default):** Progressive output with real-time entity extraction, deduplicated citations, token usage, and cost breakdown
- **Non-streaming:** Full citation and entity extraction from batch response via `parseCitations()` and `parseEntities()`

Key changes in v4.2.0:
- **Entity extraction:** Streaming mode parses `<enum_item>` tags incrementally — entity names are streamed inline as they are parsed, and a consolidated **Entities mentioned** section is printed at the end with URL and citation count per entity
- **Citation deduplication:** Duplicate source URLs are deduplicated so each source is cited only once (sorted by citation number)
- **Non-streaming mode (v4.2.0):** Full `parseCitations()` and `parseEntities()` applied to the batch response content, so citations and entities are extracted even without streaming

### brave_suggest.js

The autosuggest script with the following optimizations:
- **In-memory cache:** 60-second TTL cache keyed by `query|count|country|rich` — deduplicates rapid successive calls
- **Key fallback chain:** `AUTOSUGGEST_API_KEY` → `BRAVE_AUTOSUGGEST_API_KEY` → `BRAVE_SEARCH_API_KEY`

### brave_answers streaming

When streaming is enabled (`stream: true`):
- SSE chunks are parsed in real-time
- Citations are collected and printed at end (sorted by citation number)
- Entity items (`<enum_item>`) are parsed incrementally — streamed inline and collected for the **Entities mentioned** section
- Usage block (`<usage>`) parsed and displayed with token counts and total cost

## Security & Packaging Notes

- This skill only calls Brave official endpoints under `https://api.search.brave.com/res/v1`.
- It requires `BRAVE_SEARCH_API_KEY` and `BRAVE_ANSWERS_API_KEY` (keep them in `.env`, not inline in commands/chats).
- Optionally accepts `AUTOSUGGEST_API_KEY` or `BRAVE_AUTOSUGGEST_API_KEY` for autosuggest.
- It does not request persistent/system privileges and does not modify system config.
- All scripts are Node.js 18+ native (no external dependencies).
