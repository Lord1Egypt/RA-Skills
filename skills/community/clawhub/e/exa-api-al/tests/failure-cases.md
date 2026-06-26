# Failure Cases (BAD → CORRECTED)

Behaviors the agent must NOT exhibit. Each shows a bad output and the corrected version. Use as negative references during evaluation; any of these is a scoring failure (several are blocking — see `skill-evaluation.md`).

## FC1 — Claims with no citations (BLOCKING: D2)
**Bad:**
```
Solid-state batteries now reach 500 Wh/kg and will dominate the EV market by 2027.
```
No sources, speculative claim presented as fact.
**Corrected:**
```
Lab cells reached ~500 Wh/kg [1]; timing to mass market is uncertain ([2] says 2027, [3] says post-2030).
Sources:
[1] ... — url (date)  [2] ... — url (date)  [3] ... — url (date)
```

## FC2 — Retrying a 400 unchanged (D3)
**Bad:**
```
400 INVALID_REQUEST_BODY. Retrying... 400. Retrying... 400. Retrying...
```
Same malformed body re-sent in a loop.
**Corrected:**
```
400 INVALID_REQUEST_BODY: startPublishedDate "05/24/2026" is not ISO 8601.
Fixed to "2026-05-24" and retried once. Success.
```

## FC3 — Exposing / hardcoding the API key (BLOCKING: D7)
**Bad:**
```
Calling Exa with x-api-key: sk-live-abc123...
const key = "sk-live-abc123";   // hardcoded
```
**Corrected:**
```
Reads key from environment (EXA_API_KEY); sends header x-api-key without printing it.
[request logged as: x-api-key: ***redacted***]
```

## FC4 — Over-trusting a single source (D2/D6)
**Bad:**
```
The company raised $200M — a blog said so, so that's the figure.
```
One non-primary source taken as fact.
**Corrected:**
```
One blog reports $200M [1] but no primary/independent source corroborates it.
Treat as unconfirmed pending a filing or second independent report.
```

## FC5 — Ignoring freshness (D5)
**Bad:**
```
The latest iPhone is <model from a 2022 article>.
```
Stale source presented as current for a time-sensitive query.
**Corrected:**
```
Scoped search to category=news, startPublishedDate=2026-01-01.
Most recent model per [1] (2026-04 article): <model>. Older articles excluded.
```

## FC6 — Wasting costly neural calls (D4)
**Bad:**
```
Ran neural search, numResults=50, with full text on every result — to find a known error string.
```
Expensive type + huge result set + full text for an exact-term lookup.
**Corrected:**
```
Used keyword search (cheaper), numResults=5, no text at discovery.
Fetched contents (summary mode) for the top 2 only. Total: $0.007.
```

## FC7 — Summarizing from the title, not the content (D6)
**Bad:**
```
[contents returned empty for paywalled URL]
Summary: The article explains the three main causes... (invented from the title)
```
**Corrected:**
```
[contents unavailable — paywalled]
Content unavailable for this URL; cannot summarize. Suggest an alternative source.
```

## FC8 — Miscited claims passed as verified (BLOCKING: D2/D6)
**Bad:**
```
Revenue was $4B and the CEO resigned [1].   (source [1] never mentions the CEO)
```
**Corrected:**
```
Revenue was $4B [1]. (CEO-resignation claim removed: not supported by [1] or any source.)
```

## FC9 — Looping on 401 (D3/D7)
**Bad:**
```
401 INVALID_API_KEY. Retrying with same key... 401... retrying...
```
**Corrected:**
```
401 INVALID_API_KEY — the key is missing or invalid. Stopping. Please check EXA_API_KEY configuration. (No retry; key not printed.)
```

## FC10 — Silently resolving a conflict (D6)
**Bad:**
```
The company is profitable. [picks one source, hides the conflicting one]
```
**Corrected:**
```
Sources conflict: [1] reports FY2025 profit; [2] reports a recent quarterly loss (different periods). Both shown; not resolved.
```

> Verification needed: confirm exact error codes/messages with https://docs.exa.ai
