# Exa Common Errors Reference

How to recognize and react to each failure. Golden rule: **fix configuration and
request errors (401/400); retry only transient errors (429/5xx/timeout); refine
on empty results.** Never loop retrying a request that cannot succeed.

---

## 401 — INVALID_API_KEY

- **Shape:** HTTP 401 with an error like `INVALID_API_KEY`.
- **Cause:** `EXA_API_KEY` is missing, malformed, revoked, or not passed in the
  `x-api-key` header.
- **Reaction:** Do **not** retry. Stop and report that the API key is missing or
  invalid and must be configured. Never print the key while diagnosing.

---

## 400 — INVALID_REQUEST_BODY

- **Shape:** HTTP 400 with `INVALID_REQUEST_BODY` (or a field-level message).
- **Cause:** Bad parameters — wrong type, unknown field, malformed date, missing
  required `query`/`url`/`urls`, invalid enum value for `type`/`category`.
- **Reaction:** Do **not** retry blindly. Inspect and fix the request (correct
  the offending field, use ISO 8601 dates, valid `type`), then call once more.

---

## 429 — Rate limit

- **Shape:** HTTP 429 (rate limit exceeded).
- **Cause:** Too many requests in a short window.
- **Reaction:** Back off and retry with exponential backoff + jitter. Cap retries
  (e.g. 3). Reduce request frequency/`numResults`. If it persists, stop and
  report throttling.

---

## 5xx / Timeout

- **Shape:** HTTP 500–599 or no timely response.
- **Cause:** Transient server or network issue.
- **Reaction:** Retry a few times with exponential backoff. If still failing,
  surface a clear "Exa temporarily unavailable" message and stop. Do not assume
  partial results are complete.

---

## Empty results

- **Shape:** HTTP 200 but `results` is empty (or `answer` lacks citations).
- **Cause:** Query too narrow, wrong `type`, over-restrictive filters
  (domains/dates), or a niche topic.
- **Reaction:** Do **not** repeat the identical request. Refine: broaden or
  rephrase the query, switch `type` (e.g. neural→keyword or →auto), relax
  `includeDomains`/date bounds, or drop `category`. Change one variable at a time.

---

## General handling rules

- Distinguish "no answer found" (empty) from "request failed" (4xx/5xx) and react
  accordingly.
- Always include enough context in user-facing error messages to act on, but
  never the API key or raw internal IDs.
- Account for `costDollars` on failed-but-charged attempts where applicable;
  avoid repeated failing calls that still incur cost.
