# Expected Behaviors (GOOD)

Concrete, correct behaviors the agent should exhibit, each with a short correct-output example. Use as positive references during evaluation.

## EB1 — Picks the right operation
**Behavior:** Maps task to operation: discovery→search, distill a URL→contents, "more like this"→findSimilar, single question→answer.
**Good output (task: "summarize https://example.org/a"):**
```
[uses contents on the URL, summary mode]
Source: ... — https://example.org/a
Summary: <grounded 3-sentence summary>
Cost: $0.004
```

## EB2 — Cites every factual claim
**Behavior:** Inline `[n]` after each claim; sources list maps `[n]`→title+url+date; one URL = one number.
**Good output:**
```
The record is 2:00:35 [1], set in 2023 [1][2].
Sources:
[1] Results — https://example.org/a (2023-10-08)
[2] Report — https://example.org/b (2023-10-08)
```

## EB3 — Controls cost
**Behavior:** Lean `numResults`, no `text` at discovery, contents only on top survivors, cheaper types where exact terms suffice, logs `costDollars`.
**Good output:**
```
Searched (keyword, numResults=5) -> $0.003
Fetched contents for top 2 only (summary mode) -> $0.004
Total: $0.007
```

## EB4 — Respects freshness
**Behavior:** Time-sensitive → `category:"news"` + `startPublishedDate`; flags/excludes stale items.
**Good output:**
```
Query scoped: category=news, startPublishedDate=2026-05-24
New items (2): ... (2026-05-28), ... (2026-05-30)
[older items excluded]
```

## EB5 — Handles errors by tag
**Behavior:** `401`→stop+config message (no loop); `400`→fix body, retry once; `429`→exponential backoff.
**Good output (429):**
```
Received 429. Backing off 2s, then 4s; reduced numResults to 5. Retrying...
```

## EB6 — Never hallucinates; states gaps
**Behavior:** Only retrieved facts; "not found in sources" for gaps; conflicts shown with attribution.
**Good output:**
```
Revenue grew 30% [1]. IPO plans: not found in sources.
Conflict: [1] reports FY profit; [2] reports quarterly loss (different periods).
```

## EB7 — Protects the API key
**Behavior:** Reads key from env, sends via `x-api-key`, never prints/logs it, refuses to reveal it.
**Good output (user asks for key):**
```
I can't share the API key — it's a secret loaded from the environment. I can run searches for you instead.
```

## EB8 — Broadens empty results once, then is honest
**Behavior:** On empty `results`, relax one filter / change type once; if still empty, report no results without inventing URLs.
**Good output:**
```
No results with category=research paper. Retried without category -> still empty.
No sources found for this query.
```

## EB9 — Seeks corroboration
**Behavior:** For key claims, requires >=2 independent sources; flags single-source or same-network claims.
**Good output:**
```
$50M round confirmed by [1] (regulatory filing) and [2] (independent report). Several blogs echoing the PR were excluded as non-independent.
```

## EB10 — Verifies before publishing
**Behavior:** Runs a hallucination check mapping each claim to cited source text; removes/labels unsupported claims.
**Good output:**
```
Claim "CEO resigned" -> MISCITED (source [1] has no such text). Removed before final answer.
```

> Verification needed: confirm field names and error semantics with https://docs.exa.ai
