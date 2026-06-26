# Example 07 — Map to Discover URLs, Then Selectively Scrape (Cost-Efficient)

## User request

> "On https://docs.example.com, find all the pages about authentication and summarize just those — don't crawl the whole site."

## Agent reasoning summary

- I need to find relevant pages without paying to fetch every page → `map` lists a site's URLs cheaply, then I scrape only the matches.
- `map`'s `search` parameter pre-filters URLs server-side, shrinking the candidate set before any scrape credits are spent.
- Scrape only the filtered, deduped URLs — far cheaper than a full crawl for a narrow topic.

## Firecrawl operation to use

`map` (synchronous) to enumerate the site's URLs, optionally filtered by `search`; then `scrape` (synchronous) on the selected subset. `map` is the cheapest discovery primitive — it returns links without fetching/parsing each page's content, so it costs far less than a crawl. This "map then selectively scrape" pattern is the cost-efficient alternative to crawling when you only want a topical slice.

## Request shape

Discover + filter:

```json
POST https://api.firecrawl.dev/v2/map
Authorization: Bearer $FIRECRAWL_API_KEY

{
  "url": "https://docs.example.com",
  "search": "authentication",
  "limit": 100
}
```

Then scrape each selected URL (parallelizable), as in Example 01:

```json
{ "url": "https://docs.example.com/guides/authentication", "formats": ["markdown"], "onlyMainContent": true }
```

## Response handling

Map response:

```json
{
  "success": true,
  "links": [
    { "url": "https://docs.example.com/guides/authentication" },
    { "url": "https://docs.example.com/reference/auth-tokens" },
    { "url": "https://docs.example.com/guides/authentication?ref=nav" }
  ]
}
```

Steps:
1. Collect `links[].url`.
2. **Normalize + dedup**: strip tracking query params/fragments and lowercase host so `.../authentication` and `.../authentication?ref=nav` collapse to one URL.
3. **Refine the filter client-side** if `search` was loose: keep URLs whose path matches the topic (e.g. contains `auth`), drop obvious non-matches (changelog, pricing).
4. **Cap the scrape set** to a sensible N (e.g. top 5–10) to control cost; if there are more, tell the user and offer to expand.
5. Scrape only the surviving URLs. Skip non-2xx / empty results.
6. Summarize from scraped markdown; keep a `sourceURL → [n]` map. Sum credits (map is cheap; scrapes dominate).

## Citation behavior

Cite the resolved `metadata.sourceURL` of each scraped page. The `map` output is discovery only — never cite a mapped URL you didn't actually scrape, since you have no content from it.

## Final answer pattern

```
Authentication docs on docs.example.com (3 relevant pages, scraped):

- Authentication guide — Bearer token flow and header format [1].
- Auth tokens reference — token lifetimes, scopes, rotation [2].
- OAuth setup — third-party app authorization [3].

Sources
[1] https://docs.example.com/guides/authentication
[2] https://docs.example.com/reference/auth-tokens
[3] https://docs.example.com/guides/oauth-setup

(Firecrawl map (1 credit) + 3 scrapes; ~4 credits total. 2 more auth-related URLs found — say the word to include them.)
```

## Common failure mode

Skipping `map` and crawling the entire site to find a handful of auth pages (huge credit waste), or scraping every URL `map` returns including near-duplicates with tracking params (paying twice for the same page). Also: citing mapped URLs as sources without scraping them, so the "summary" of those pages is fabricated.

## Improved version

```
1. map with search="authentication" -> cheap candidate list.
2. Normalize + dedup URLs (strip query/fragment).
3. Client-side refine to the topic; cap to top N for cost.
4. Scrape ONLY the selected subset.
5. Summarize from scraped markdown; cite scraped sourceURLs only.
6. Report that extra matches exist and offer to expand, instead of
   silently truncating or silently over-spending.
```

This delivers a focused, fully-sourced summary at a fraction of a full crawl's cost, with no fabricated coverage.
