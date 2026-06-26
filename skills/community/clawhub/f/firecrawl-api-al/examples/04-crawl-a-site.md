# Example 04 — Crawl a Documentation Site (Async, with Bounded Polling)

## User request

> "Crawl the docs under https://docs.example.com/guides and give me a summary of every guide, with links."

## Agent reasoning summary

- Whole section of a site, many unknown pages → `crawl`, which discovers and fetches linked pages under a path.
- Crawl is asynchronous: start the job, get an `id`, poll until `status: completed`, paginating the result `data`.
- Bound the work: cap with `limit`, scope with `includePaths`, and cap wall-clock polling time so I never hang.

## Firecrawl operation to use

`crawl` (asynchronous). Unlike `scrape`, crawl traverses the site, so it returns a job `id` immediately and the documents arrive later via status polling. Cost scales with pages fetched — roughly one scrape's worth of credits per crawled page — so always set `limit`. Use `includePaths` to keep the crawl inside `/guides` and avoid burning credits on the whole domain.

## Request shape

Start the job:

```json
POST https://api.firecrawl.dev/v2/crawl
Authorization: Bearer $FIRECRAWL_API_KEY

{
  "url": "https://docs.example.com/guides",
  "limit": 50,
  "includePaths": ["^/guides/.*"],
  "scrapeOptions": { "formats": ["markdown"], "onlyMainContent": true }
}
```

Response:

```json
{ "success": true, "id": "a1b2c3d4-...", "url": "https://api.firecrawl.dev/v2/crawl/a1b2c3d4-..." }
```

Poll status:

```json
GET https://api.firecrawl.dev/v2/crawl/a1b2c3d4-...
Authorization: Bearer $FIRECRAWL_API_KEY
```

> Verification needed: confirm path params, status field names, and pagination cursor with https://docs.firecrawl.dev

## Response handling

Poll response shape:

```json
{
  "status": "scraping",          // -> "completed" | "failed" | "cancelled"
  "total": 37,
  "completed": 22,
  "creditsUsed": 22,
  "next": "https://api.firecrawl.dev/v2/crawl/a1b2c3d4-...?skip=10",
  "data": [
    { "markdown": "# Getting Started ...",
      "metadata": { "sourceURL": "https://docs.example.com/guides/getting-started", "statusCode": 200 } }
  ]
}
```

Bounded polling loop:
1. Start job, capture `id`.
2. Loop: GET status every ~3–5s.
   - `status === "completed"` → collect all `data`, then break.
   - `status === "failed"` / `"cancelled"` → stop and report (see Example 08).
   - still running → keep polling, surface progress as `completed/total`.
3. **Hard bound**: stop after a max elapsed time (e.g. 120s) or a max poll count. On timeout, use whatever pages already arrived and tell the user the crawl was partial.
4. **Paginate**: if a `next` cursor/URL is present, follow it and concatenate `data` until exhausted — a single status response may not contain all documents.
5. Dedup the merged documents by `metadata.sourceURL`.

## Citation behavior

Each guide in the summary cites its own `metadata.sourceURL`. The crawl entry point URL is context, not a citation for individual page content.

## Final answer pattern

```
Crawled 37 guide pages under /guides (Firecrawl crawl, 37 credits).

- Getting Started — install and first request [1]
- Authentication — API keys and Bearer tokens [2]
- Webhooks — event delivery and retries [3]
... (one bullet per deduped page)

Sources
[1] https://docs.example.com/guides/getting-started
[2] https://docs.example.com/guides/authentication
[3] https://docs.example.com/guides/webhooks
```

If the crawl was bounded early: prepend
`Note: crawl stopped at the 120s limit after 22/37 pages; summary below is partial.`

## Common failure mode

Treating crawl like a synchronous call — reading `data` from the very first start response (which only has `id`), or polling forever with no time cap and hanging. Also: ignoring the `next` cursor and silently summarizing only the first page of results, or crawling the whole domain because `limit`/`includePaths` were omitted (credit blowout).

## Improved version

```
1. Always set limit + includePaths on start (scope + cost guard).
2. Poll on an interval with BOTH a max-time and max-iteration cap.
3. On each poll: report completed/total progress.
4. Follow `next` until no cursor remains; concatenate all data pages.
5. Dedup by sourceURL; sum creditsUsed.
6. On timeout/partial: answer with what arrived AND disclose it's partial.
7. On status failed/cancelled: report cleanly, don't fabricate a summary.
```

This keeps the crawl scoped, bounded, complete (paginated), and honest about partial results.
