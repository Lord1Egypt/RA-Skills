# Example 08 — Error Recovery: 401 / 400 / 402 / 429 / Empty Content / Crawl Timeout

## User request

> "Scrape https://app.example.com/dashboard and summarize it." (And more generally: handle whatever goes wrong without crashing or making things up.)

## Agent reasoning summary

- Any Firecrawl call can fail; I detect the failure by HTTP status / error `code`, then react appropriately per case.
- Different failures need different reactions: fix the request, retry with backoff, keep polling, add credits, or wait for render.
- Always communicate the failure honestly — never fabricate content to paper over an error.

## Firecrawl operation to use

Applies to all operations (`scrape`, `crawl`, `map`, `search`). The recovery logic keys off the HTTP status code and the error `code`/message in the body, plus the response `status` field for async crawl jobs.

## Request shape

The original call is ordinary (e.g. a scrape from Example 01). What matters is the **error branch** that wraps every call:

```json
POST https://api.firecrawl.dev/v2/scrape
Authorization: Bearer $FIRECRAWL_API_KEY

{ "url": "https://app.example.com/dashboard", "formats": ["markdown"], "onlyMainContent": true }
```

## Response handling

Detect → react matrix:

| Symptom | How to detect | Reaction |
|---|---|---|
| Bad/missing key | HTTP `401` | Do **not** retry. Report auth failure; ask the user to set a valid `FIRECRAWL_API_KEY` (never print or hardcode the key). |
| Malformed request | HTTP `400`, `code: BAD_REQUEST` | Do **not** blind-retry. Inspect the message, fix the request (bad URL, unknown field, invalid schema), then retry once. |
| Out of credits | HTTP `402` (out-of-credits) | Stop. Report that credits are exhausted; suggest topping up or narrowing scope (lower `limit`). Don't loop. |
| Rate limited | HTTP `429` | Retry with exponential backoff, honoring `Retry-After` if present. Cap attempts (e.g. 3); then report. |
| Empty / JS-rendered page | `success:true` but `markdown` empty/whitespace | Retry once with `{ "waitFor": 3000 }` (let client-side render). If still empty, report "no extractable content." |
| Soft failure | `success:true` but `metadata.statusCode` non-2xx (403/404/5xx) | Treat content as invalid; report the upstream status. Don't summarize stub content. |
| Crawl never finishes | async `status` stays `scraping` past your time cap | Stop polling at the bound; use pages already collected and mark the result partial. |
| Crawl errored | async `status: "failed"`/`"cancelled"` | Report cleanly; offer to restart with a smaller `limit`/tighter `includePaths`. |

Backoff sketch for 429:

```
attempt = 0
while attempt < 3:
    resp = call()
    if resp.status != 429: break
    wait = resp.headers["Retry-After"] or (2 ** attempt) seconds
    sleep(wait); attempt += 1
```

> Verification needed: confirm exact error codes, the `Retry-After` header, and `waitFor` semantics with https://docs.firecrawl.dev

## Citation behavior

On failure there is nothing to cite — do not invent a `sourceURL` or summarize content you didn't successfully retrieve. On a *partial* success (e.g. timed-out crawl), cite only the pages that actually completed, and disclose the gap.

## Final answer pattern

Success: normal answer (Examples 01–07).

Failure (example, 402):

```
I couldn't complete the scrape: Firecrawl returned 402 (out of credits).
No content was retrieved, so I won't summarize anything.
Options: top up Firecrawl credits, or narrow the request (e.g. fewer pages).
```

Partial (crawl timeout):

```
The crawl didn't finish within the time limit (22/37 pages completed).
Here's a summary of the 22 pages I did retrieve [partial]:
... cite only completed pages' sourceURLs ...
Say the word to resume/extend the crawl.
```

## Common failure mode (before)

```
- Retrying a 401 or 400 in a tight loop (auth/validation errors never self-heal) -> wasted calls.
- Hammering on 429 with no backoff -> deeper throttling.
- Looping on 402 instead of stopping -> nothing improves.
- Returning empty markdown as if it were the page, or summarizing a 404 stub.
- Polling a crawl forever with no time cap -> the agent hangs.
- Fabricating a plausible summary + citation to hide the error -> user misled.
```

## Improved version (after)

```
Wrap every Firecrawl call in detect -> react -> communicate:

DETECT by status/code:
  401 -> auth: stop, ask for valid key (never expose it)
  400/BAD_REQUEST -> fix the request, retry ONCE
  402 -> out of credits: stop, suggest top-up/narrow scope
  429 -> exponential backoff (honor Retry-After), max 3, then report
  success but empty markdown -> retry once with waitFor; else "no content"
  success but non-2xx statusCode -> report upstream status, don't summarize
  crawl over time cap -> use partial data, mark partial
  crawl failed/cancelled -> report, offer smaller re-run

COMMUNICATE: state what failed and why; never fabricate content or citations.
On partial success: answer with what arrived and disclose the gap.
```

This makes the agent resilient (right reaction per error), economical (no pointless loops), and trustworthy (no hallucinated recovery).
