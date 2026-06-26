# Reference: Common Errors

How to recognize each error and the agent's correct reaction. Inspect `success`, HTTP status, `metadata.statusCode`, and any error body before reacting. **Retry only transient errors.**

> Verification needed: confirm exact error codes, bodies, and `Retry-After` behavior at https://docs.firecrawl.dev.

---

## 401 Unauthorized

- **Shape:** HTTP 401; error indicating invalid/missing authentication.
- **Cause:** Missing or wrong `FIRECRAWL_API_KEY` (bad Bearer token).
- **Reaction:** **Do not retry.** Report that `FIRECRAWL_API_KEY` is missing/invalid and must be fixed in the environment. Never print the key.

## 400 BAD_REQUEST

- **Shape:** HTTP 400 with a `BAD_REQUEST`-style error/message.
- **Cause:** Malformed request — invalid URL, bad/unknown parameters, invalid `schema`, conflicting options.
- **Reaction:** **Do not retry unchanged.** Fix the offending field (correct the URL, drop/repair params, fix the JSON schema), then issue one corrected call.

## 402 Payment Required / out of credits

- **Shape:** HTTP 402 or an out-of-credits error.
- **Cause:** The account has no remaining credits.
- **Reaction:** **Do not retry.** Stop spending. Report that Firecrawl credits are exhausted and need topping up.

## 429 Too Many Requests

- **Shape:** HTTP 429, possibly with `Retry-After`.
- **Cause:** Rate limit exceeded.
- **Reaction:** **Retry with exponential backoff**, honoring `Retry-After` when present. Cap the number of attempts; slow down concurrency.

## 5xx Server Errors

- **Shape:** HTTP 500/502/503/504.
- **Cause:** Transient server-side problem.
- **Reaction:** **Retry with exponential backoff**, capped (e.g. up to 3 attempts). If it persists, report the failure.

## Crawl timeout / crawl still scraping

- **Shape:** Your bounded wait elapsed while `GET /v2/crawl/{id}` still returns `status: "scraping"`.
- **Cause:** The crawl is large/slow; it is **not** a failure.
- **Reaction:** Keep the `id`. Either keep polling (with backoff) or return partial `data` plus the `id` so the job can be resumed later. **Do not start a new crawl.**

## Empty content / empty markdown

- **Shape:** `success: true` but `data.markdown` is empty or near-empty (often with a 200 status).
- **Cause:** Client-side rendering, lazy loading, or a soft block/consent wall.
- **Reaction:** Retry once with `waitFor` (and/or `actions` to dismiss walls / reveal content); add `proxy` only if a block is evident. If still empty, report that content could not be extracted from the URL.

## Empty / wrong structured JSON

- **Shape:** `data.json` empty, missing fields, or mistyped.
- **Cause:** Missing page content, or an unclear `prompt`/`schema`.
- **Reaction:** Tighten the `prompt` and `schema`; add `waitFor` if content was missing. Do not loop on the identical call.

---

## Quick decision table

| Error | Retry? | Action |
|-------|--------|--------|
| 401 | No | Fix key, report. |
| 400 BAD_REQUEST | No (unchanged) | Fix request, call once. |
| 402 | No | Stop; report out of credits. |
| 429 | Yes (backoff) | Honor Retry-After; cap attempts. |
| 5xx | Yes (backoff) | Cap attempts; then report. |
| Crawl timeout | Keep polling by `id` | Don't restart; report partial + id. |
| Empty markdown | Once | Add waitFor/actions/proxy. |
| Empty json | Adjust, not loop | Improve prompt/schema; add waitFor. |
