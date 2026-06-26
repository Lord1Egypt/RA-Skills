# Example 05 — Search the Web, Then Scrape the Top Results (Recency-Aware)

## User request

> "What are the most recent changes to the EU AI Act's rules for general-purpose AI models? Give me sourced, up-to-date info."

## Agent reasoning summary

- Open-ended, current-events question with no URLs → start with `search` to discover relevant, recent pages.
- "Most recent" means recency matters: prefer fresh results and check publication dates before trusting them.
- Then get the actual text: either pass `scrapeOptions` to `search` (one call) or scrape the top results individually; cite each.

## Firecrawl operation to use

`search` (synchronous) to find candidate URLs, then `scrape` for full content. Two efficient patterns:

- **Combined**: `search` with `scrapeOptions` set — Firecrawl scrapes each result inline, so one logical operation returns content. Convenient; costs search + per-result scrape credits.
- **Two-stage**: plain `search` (cheap), pick the best N by relevance/recency, then `scrape` only those. More control, often fewer credits.

Both report `creditsUsed`. Use the combined form when you'll likely read most results; use two-stage when you need to filter first.

## Request shape

Combined search + scrape:

```json
POST https://api.firecrawl.dev/v2/search
Authorization: Bearer $FIRECRAWL_API_KEY

{
  "query": "EU AI Act general-purpose AI model obligations update 2026",
  "limit": 5,
  "scrapeOptions": { "formats": ["markdown"], "onlyMainContent": true }
}
```

Plain search (two-stage), then scrape chosen URLs as in Example 01/02:

```json
{ "query": "EU AI Act general-purpose AI model obligations update 2026", "limit": 8 }
```

## Response handling

Search response:

```json
{
  "success": true,
  "creditsUsed": 6,
  "data": {
    "web": [
      { "url": "https://news.example/eu-ai-act-gpai-2026",
        "title": "EU finalizes GPAI code of practice",
        "description": "...", "position": 1 }
    ]
  }
}
```

Steps:
1. Read `data.web[]`. Each item has `url`, `title`, `description`, `position`.
2. **Recency filter**: the question is time-sensitive. Prefer results whose scraped content or metadata shows a recent date; demote or drop undated/stale pages. Don't rely on `position` alone for "most recent."
3. **Dedup by `url`** (and by resolved `sourceURL` after scraping) — search engines surface mirrors and syndications.
4. If two-stage: scrape the top 3–5 deduped URLs. If combined: read the `markdown` already attached to each result.
5. Synthesize only from scraped content; keep a `url → [n]` citation map.
6. Sum `creditsUsed` (search + any scrapes).

## Citation behavior

Cite the resolved `metadata.sourceURL` of each scraped page (not the search snippet). Where recency is asserted, include the publication date you found in the content so the user can judge freshness.

## Final answer pattern

```
Recent EU AI Act changes for general-purpose AI (GPAI):

- The GPAI Code of Practice was finalized, detailing transparency and copyright duties [1].
- Systemic-risk model thresholds were clarified, with added evaluation requirements [2].

(Dates noted inline where available; verify against the primary regulation for legal use.)

Sources
[1] EU finalizes GPAI code of practice (pub. 2026-03) — https://news.example/eu-ai-act-gpai-2026
[2] Systemic-risk thresholds clarified (pub. 2026-04) — https://reg.example/ai-act/gpai

(Firecrawl search + 2 scrapes, 8 credits total.)
```

## Common failure mode

Answering straight from `title`/`description` snippets without scraping (shallow, sometimes wrong), trusting `position` as "newest," or presenting three syndicated copies of one article as three independent sources. For a "most recent" question, returning an article from two years ago because it ranked #1.

## Improved version

```
1. search to discover -> get data.web[] (url/title/description/position).
2. Filter for recency BEFORE committing scrape credits (check/seek dates).
3. Dedup by url, then re-dedup by resolved sourceURL after scraping.
4. Scrape the top deduped, recent URLs (or use scrapeOptions inline).
5. Synthesize ONLY from scraped markdown; cite sourceURL + show dates.
6. State the retrieval date and recommend verifying primary sources for high-stakes topics.
```

This makes the answer genuinely current, source-grounded, and free of duplicate "sources."
