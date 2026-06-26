# Afternoon Research Prompt Template

*Version 2.0.0 | Uses CORE + TOPICS layered structure*

---

## Step 1: Load Prompt Stack

1. Load `PROMPTS/CORE/system-prompt.md` — generic base
2. Load `PROMPTS/CORE/signal-rules.md` — signal definition
3. Load `PROMPTS/CORE/digest-format.md` — output format
4. Load `PROMPTS/TOPICS/<topic>.md` — domain-specific layer

TOPICS inherits from CORE. Do not contradict.

---

## Step 2: Freshness Gate

For each topic in CONFIG/topics.yaml:

1. Read `topics/<topic>/META.json`
2. If `lastAfternoonUpdate` is today's date → skip
3. If `retryCount >= 2` AND `retryDate` is today → skip (exhausted)
4. Otherwise → proceed to scan

---

## Step 3: Search

Run the agent's web search tool per topic:
- Query: `search_query` from `CONFIG/topics.yaml` + `latest` suffix
- Max results: 8
- Time range: last 24h (or tool equivalent)

---

## Step 4: Write News File

Write to: `topics/<topic>/news/<topic>-YYYY-MM-DD.md`

```
Headline: <exact headline text>
Source: <outlet name>
URL: <url or N/A>
Note: <1-2 sentence context or take>
CapturedAt: <ISO8601>

---
```

---

## Step 5: Update META.json

After successful write:
- `lastHeartbeatUpdate` → current ISO8601
- `lastAfternoonUpdate` → YYYY-MM-DD
- `retryCount` → 0
- `lastError` → null

On failure: call meta_record_failure, retry once if allowed, else skip.

---

## Step 6: Produce Digest

1. Read news files (no re-search)
2. Apply CORE rules + TOPICS domain layer
3. Focus on what changed **since this morning** — new signals, confirmations, contradictions
4. Mark freshness: `[fresh]` / `[stale]` / `[retry N/2]` / `[exhausted]`

Deliver via message tool (Telegram or WhatsApp).

---

*Version 2.0.0 | 2026-04-20*