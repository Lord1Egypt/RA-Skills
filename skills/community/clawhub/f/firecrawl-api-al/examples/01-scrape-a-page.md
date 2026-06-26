# Example 01 — Scrape a Single Page to Clean Markdown

## User request

> "Pull the text of this blog post for me so I can read it without the ads and popups: https://www.firecrawl.dev/blog/introducing-fire-engine"

## Agent reasoning summary

- One known URL, plain reading goal → a single `scrape` call is the cheapest correct operation.
- Want readable prose, so request `markdown` and set `onlyMainContent: true` to strip navigation, ads, and footers.
- The post's canonical link comes from `metadata.sourceURL`; I'll cite that, not the user's typed URL.

## Firecrawl operation to use

`scrape` (synchronous). One URL in, one document out. This is the right tool because the target is a single known page — no discovery (`map`), no multi-page traversal (`crawl`), no query (`search`) is needed. Cost: scrape bills a small number of credits per page (reported back in `metadata.creditsUsed`). Synchronous means the result is returned in the same response; no polling.

## Request shape

```json
POST https://api.firecrawl.dev/v2/scrape
Authorization: Bearer $FIRECRAWL_API_KEY
Content-Type: application/json

{
  "url": "https://www.firecrawl.dev/blog/introducing-fire-engine",
  "formats": ["markdown"],
  "onlyMainContent": true
}
```

> Verification needed: confirm the exact endpoint path/version with https://docs.firecrawl.dev

## Response handling

```json
{
  "success": true,
  "data": {
    "markdown": "# Introducing Fire Engine\n\nFire Engine is ...",
    "metadata": {
      "sourceURL": "https://www.firecrawl.dev/blog/introducing-fire-engine",
      "statusCode": 200,
      "creditsUsed": 1,
      "title": "Introducing Fire Engine"
    }
  }
}
```

Parsing steps:
1. Check `success === true`. If false, branch to error handling (see Example 08).
2. Confirm `data.metadata.statusCode` is in the 2xx range. A `200`-level `success` with a non-2xx `statusCode` (e.g. 404/403) means the upstream page failed — treat the markdown as unreliable.
3. Read `data.markdown` as the clean body.
4. If `data.markdown` is empty or only whitespace, the page likely rendered client-side; retry once with `{ "waitFor": 3000 }` before giving up.
5. Record `data.metadata.creditsUsed` for cost reporting.

## Citation behavior

Cite `data.metadata.sourceURL`. This is the canonical URL Firecrawl resolved (after any redirect), which may differ from the URL the user pasted. Always cite the resolved one so the link is reproducible.

## Final answer pattern

```
Here's the cleaned article:

<article markdown from data.markdown>

---
Source: [1] {data.metadata.title} — {data.metadata.sourceURL}
(Retrieved via Firecrawl scrape, {data.metadata.creditsUsed} credit.)
```

## Common failure mode

Returning `data.markdown` even when `statusCode` is 404/403 — the agent hands the user a "soft 404" or paywall stub presented as the real article, with a confident citation. The user trusts incomplete content.

## Improved version

Gate on the status code and content length before answering:

```
1. success !== true            -> report failure, do not fabricate (Example 08)
2. statusCode not 2xx          -> tell user the page was unreachable/blocked; show statusCode
3. markdown empty/whitespace   -> retry once with waitFor: 3000; if still empty, say "no extractable content"
4. otherwise                   -> return markdown + cite metadata.sourceURL + report creditsUsed
```

This guarantees the user only ever sees verified, non-empty content tied to a real, resolved URL.
