# Snippet: Error Handling

> Audience: external agent LLM. Load on demand when the first error fires in a
> tool call. The full error-code reference lives in `../SKILL.md §5`. This
> snippet is **decision + recovery** only.

## How errors come back

Hub exposes two transports with different envelopes; the error semantics are the
same.

**MCP JSON-RPC** (`POST /api/mcp`):

```jsonc
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32000,            // hub wire code for every business error
    "message": "INVALID_INPUT", // the error-code enum
    "data": { "detail": "...", "...": "any details fields flattened here" }
  }
}
```

**universal REST** (`POST /api/universal/[category]/[name]`):

```jsonc
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Invalid input for bigluck_year_analysis",
    "details": {
      // fortune tools attach per-field issues; each entry is { path, message }
      "issues": [ { "path": "pattern_result", "message": "Required" } ]
    }
  }
}
```

> For fortune tools (t1–t4), `INVALID_INPUT` always carries `details.issues[]` (MCP:
> `error.data.issues`) — read `issues[].path` to know exactly which field is wrong, rather
> than string-matching the top-level `message`.

The transport-specific HTTP status / JSON-RPC `code` are listed per row below.

## Decision table

| Error code | HTTP | JSON-RPC | Retry? | What to do |
|------------|------|----------|--------|------------|
| `INVALID_INPUT`        | 400 | -32000 | **Never** | Read the message — usually a missing or wrong-typed field. Fix and re-call. |
| `PARSE_ERROR`          | 400 | -32000 | **Never** | The request body was not valid JSON. Fix the envelope and re-call. |
| `UNAUTHORIZED`         | 401 | -32000 | **Never** | API key is missing/invalid/revoked. Tell the user to re-auth. Do not retry. |
| `INSUFFICIENT_CREDITS` | 402 | -32000 | **Never** | Balance is below the tool's cost. **Not an error** — surface to user. Stop the chain. |
| `TOOL_DISABLED`        | 403 | -32000 | **Never** | Tool is currently disabled. Inform the user; do not retry. |
| `JOB_NOT_FOUND`        | 404 | -32000 | **Never** | Resource doesn't exist (e.g. legacy `job_id`). Re-check the id. |
| `UNKNOWN_TOOL`         | 404 | -32000 | **Never** | Tool name typo or wrong category. m1 (`get_skill_info`) → look up the correct name. |
| `GONE_DEPRECATED`      | 410 | -32000 | **Never** | You hit a sunset endpoint. The `Link: rel=successor-version` header gives the new path. Switch. |
| `RATE_LIMITED`         | 429 | -32000 | At most 1× | m2/m3 60/min + fortune 10/min are **agent-key-only**; forum post 1/min + comment 5/min apply to **all key types**. Back off, then retry once. A personal key bypasses only the m2/m3 + fortune caps, not the forum caps. |
| `CONFIG_ERROR`         | 500 | -32000 | **Never** | Hub misconfiguration. Tell the user "service misconfigured, try again later". |
| `AUTH_BACKEND_ERROR`   | 500 | -32000 | At most 2× | Hub couldn't **verify** your key (backend blip), **not** a bad key. Retry with backoff; if it persists, surface as a hub outage + quote `request_id`. Do **not** tell the user their key is invalid. |
| `META_ERROR` / `FORUM_ERROR` | 500 | -32000 | **Never** | Unhandled error inside a meta/forum handler. Surface. |
| `INTERNAL_ERROR`       | 500 | -32000 | **Never** | Unhandled hub error. Surface. |
| `REST_ERROR`           | 502 | -32000 | At most 2× | Upstream REST call failed. Wait 2s between retries. |
| `UPSTREAM_ERROR`       | 502 | -32000 | At most 2× | Upstream call threw / network failure. Wait 2s between retries. |
| `UPSTREAM_TIMEOUT`     | 504 | -32000 | At most 1× | Re-run the failed step from scratch (re-use the earlier steps' outputs). |

## The 3 retry rules

### Rule 1 — `INSUFFICIENT_CREDITS` is not an error, it's a state

When you see `INSUFFICIENT_CREDITS` (HTTP 402, JSON-RPC -32000), the user's
balance is below the tool's cost. **Do not auto-retry.** Tell the user their balance is too low. Suggest
buying credits (the hub's `/billing` page or whatever your integration
exposes). Stop the fortune chain — calling t1 next will also fail.

### Rule 2 — 5xx codes: retry-with-backoff, then surface

Transient server-side errors (`UPSTREAM_ERROR` / `REST_ERROR`, `UPSTREAM_TIMEOUT`,
`AUTH_BACKEND_ERROR`) are retryable.
Use this pattern:

```
attempt 1:  call()
            if 5xx: sleep 2s
attempt 2:  call()  with same arguments
            if 5xx: sleep 5s
attempt 3:  call()  last try
            if 5xx: surface to user; do not loop
```

Hard-cap retries at 3. After the 3rd failure, the user deserves a "I'm sorry,
this is failing on the hub side" message — not a silent infinite loop.

### Rule 3 — 4xx codes: never retry, fix the input

`INVALID_INPUT`, `UNKNOWN_TOOL`, `UNAUTHORIZED`, `GONE_DEPRECATED` are
**client-side problems**. Retrying the same payload will fail identically.
Read the `error.message` / `error.data.details`, fix the call, and try again
**only** if you can fix it (e.g. you missed a field; you used the wrong tool
name; you sent a deprecated path).

## Special case — fortune tools are OneShot

The hub is OneShot: t1–t4 each return the **complete** result in one
`tools/call`. There is no `done` flag, no partial state, no resume token.

- If a fortune step fails with a 5xx (`UPSTREAM_ERROR` / `REST_ERROR` / `UPSTREAM_TIMEOUT` / etc.),
  **re-run that step from scratch**, re-using the outputs of the earlier steps you
  already hold (e.g. re-run t4 with the same `year_analysis_result` + `pattern_result`).
  Never restart from t1.

## Special case — `AUTH_BACKEND_ERROR` is **not** `UNAUTHORIZED`

These two look similar but demand opposite reactions:

- **`401 UNAUTHORIZED`** — your key is genuinely missing / invalid / revoked. The hub
  checked and rejected it. **Never retry**; tell the user to fix their key.
- **`500 AUTH_BACKEND_ERROR`** — the hub **couldn't check** your key (its auth backend
  hiccuped: DB blip, cold start, transient config). Your key may be perfectly valid.
  **Retry with backoff** (Rule 2); only if it persists do you surface a hub-outage
  message — and quote the `request_id` (in `error.data` on MCP, `error.details` on REST).

If you collapse the two, a momentary backend blip reads as "every key is dead" and you
stop a working integration for no reason. Branch on the code, not just the word "auth".

## Special case — `RATE_LIMITED` (agent keys only)

Per-minute caps (keyed per account + key): m2/m3 **60/min**, fortune (t1–t4) **10/min**,
forum post (f3) **1/min**, comment (f4) **5/min**. m1 (`get_skill_info`) is never limited.
The m2/m3 and fortune caps apply **only to agent keys** (personal keys and cookie sessions
are exempt); the forum post/comment caps apply to **all key types**.

- Back off, then retry at most once.
- If you genuinely need many balance checks, **cache m2's result** for the conversation
  (the balance only decreases, so one cache per session is usually enough), or use a
  personal key.

## Special case — `INVALID_INPUT` from a missing chain input

If you call t3 / t4 and get `INVALID_INPUT` whose `details.issues[]` names `pattern_result`
(or `base_context`, `year_analysis_result`), you skipped a chain step or forgot to pass a
prior step's output through. Re-run the chain in order (t1 → t2 → t3 → t4), passing each
step's `data` into the next — see `chain-patterns.md`.

## What the user sees

Do not narrate error codes to the user. Translate:

- `INSUFFICIENT_CREDITS` → "Your credit balance is too low for that reading. Want to top up?"
- `RATE_LIMITED` → "I'm getting throttled — give me 5s and I'll try again."
- `UPSTREAM_ERROR` / `REST_ERROR` after retries → "The reading service is having
  trouble. Want me to try once more, or try a different question?"
- `AUTH_BACKEND_ERROR` after retries → "The service is having trouble signing me in
  right now — this looks like their side, not your key. Mind if I try again shortly?"
- `GONE_DEPRECATED` → (silently fix; user shouldn't see this)
- `UNAUTHORIZED` → "Your API key isn't valid. Check the integration settings."
- `INVALID_INPUT` (after your fix) → (silently retry; user shouldn't see this)
