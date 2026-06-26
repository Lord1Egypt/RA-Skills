# Example 08 — Error Recovery (401 / 400 / 429 / Empty Results)

Real calls fail. This example shows how the agent detects each failure class (by status/error tag), reacts appropriately (fix vs. retry vs. refine), and communicates clearly — with before/after contrasts.

## User request

> "Search Exa for recent papers on retrieval-augmented generation and summarize the top three."

## Agent reasoning summary

- Any Exa call can fail — branch on the error class rather than treating all failures the same.
- 401 = fix auth (don't retry blindly); 400 = fix the request body; 429 = back off and retry; empty results = refine the query, not an error.
- Always tell the user what happened and what was done, and never fabricate results to cover a failure.

## Exa operation to use

Use **`search`** (endpoint `POST /search`), wrapped in error handling that inspects HTTP status and the error tag/code in the body.

- Why: search is the natural call here; the lesson is the surrounding detect/react/communicate loop.
- Cost tradeoff: failed calls may still incur minimal cost or none; avoid retry storms on 401/400 (they will never succeed unchanged) — those waste calls. Only 429 and transient 5xx warrant retry.

## Request shape

```json
POST https://api.exa.ai/search
Headers: { "x-api-key": "<EXA_API_KEY>", "Content-Type": "application/json" }
{
  "query": "retrieval-augmented generation",
  "type": "auto",
  "category": "research paper",
  "startPublishedDate": "2025-06-01T00:00:00.000Z",
  "numResults": 10,
  "contents": { "highlights": { "numSentences": 2 } }
}
```

## Response handling — detect, react, communicate

Inspect HTTP status and the body's error tag/code. Branch:

### 401 — `INVALID_API_KEY`
- **Detect**: HTTP 401; body tag `INVALID_API_KEY`.
- **React**: do NOT retry the same key. Verify `EXA_API_KEY` is set and exported; the key is missing, expired, or malformed. Re-running unchanged will fail again.
- **Communicate**: ask the user/operator to set a valid key. Never print or hardcode the key.

```
Exa returned 401 INVALID_API_KEY. The EXA_API_KEY environment variable is missing or
invalid. Please set a valid key (do not paste it in chat); I'll retry once it's configured.
```

### 400 — `INVALID_REQUEST_BODY`
- **Detect**: HTTP 400; body tag `INVALID_REQUEST_BODY` (often names the offending field).
- **React**: fix the request, don't retry as-is. Common causes: bad date format (must be ISO-8601), unknown `type`/`category` value, malformed `contents`, `numResults` out of range.
- **Communicate**: state what was corrected, then retry.

```
Before: "startPublishedDate": "2025/06/01"   ← invalid format → 400
After:  "startPublishedDate": "2025-06-01T00:00:00.000Z"   ← ISO-8601, accepted
```

### 429 — rate limited
- **Detect**: HTTP 429.
- **React**: retry with exponential backoff + jitter (e.g. 1s, 2s, 4s), honoring `Retry-After` if present; cap retries (e.g. 3). This is the only class where blind retry is correct.
- **Communicate**: only mention to the user if it causes noticeable delay or exhausts retries.

```
Hit 429 (rate limited). Backing off and retrying (attempt 2/3 after 2s)...
```

### Empty results (`results: []`, HTTP 200)
- **Detect**: successful call, but `results` is empty (or all below the score floor).
- **React**: this is NOT an error — refine the query. Loosen `type` to `"auto"`, relax/remove `startPublishedDate`, drop or change `category`, broaden wording, or raise `numResults`. Retry once or twice with one change at a time.
- **Communicate**: tell the user you broadened and how.

```
No results for the strict filters. Removed category:"research paper" and widened the
date window to 2025-01-01; found 8 results.
```

## Citation behavior

- On success after recovery, cite normally (inline `[n]` + sources list, ranked by score) — see Example 02.
- On unrecoverable failure, cite nothing and produce no fabricated sources. Absence of an answer is reported honestly.

## Final answer pattern

Success after recovery:
```
(Note: initial query returned no results; I broadened the filters.)

Top 3 recent RAG papers:
1. ... [1]
2. ... [2]
3. ... [3]

Sources:
[1] ... — https://...  (score 0.55)
[2] ... — https://...  (score 0.49)
[3] ... — https://...  (score 0.41)
```

Unrecoverable failure:
```
I couldn't complete the search: Exa returned 401 INVALID_API_KEY after one attempt.
No results to show. Set a valid EXA_API_KEY and I'll retry.

> Verification needed: if the key is valid but still rejected, confirm endpoint/headers
> at https://docs.exa.ai.
```

## Common failure mode

- **Treating every failure identically** — e.g. retrying a 401 or 400 in a loop (never succeeds, wastes calls) or giving up on a 429 (just needed backoff).
- **Fabricating results** to hide an empty/failed response, destroying trust and grounding.
- **Leaking the API key** in logs or error messages while debugging a 401.

## Improved version (before / after)

**Before** — one undifferentiated catch:
```
try { search(...) } catch (e) { return "Sorry, something went wrong." }
```
Opaque, no recovery, may have been a trivially fixable 400 or a transient 429.

**After** — classified detect → react → communicate:
```
result = call_exa_search(body)
switch (result.status):
  200 & results.length:  proceed → filter by score, dedup by url, answer with citations
  200 & empty:           refine query (one change), retry ≤2; tell user what changed
  400 INVALID_REQUEST_BODY: fix offending field (e.g. ISO dates), retry once
  401 INVALID_API_KEY:   stop; ask for valid EXA_API_KEY; never retry blindly, never log key
  429:                   exponential backoff + jitter, honor Retry-After, retry ≤3
  5xx / network:         backoff retry ≤2; if still failing, report honestly
default: report the status honestly; produce no fabricated sources
```
Always: never hardcode/print the key; never invent results; on success, cite normally.
