# Quota System Deep Dive

## How Quota is Structured

```
openclaw.json  ←  config (ceilings, per-agent allocations)
    ↕  reconciled on every call
search-quota.json  ←  live state (daily counters, used/remaining)
```

The quota file lives at `~/.openclaw/workspace/shared/search-quota.json` by default.

## Daily Reset

On the first call after midnight, all counters reset:
- `used` → 0
- `remaining` → daily_limit
- `shared_pool` → 0
- All agent `gemini_used` / `brave_used` → 0
- All agent `completed` → false

## Deduction Priority (per search call)

```
1. agent_allocation  →  agent has gemini/brave remaining
2. shared_pool       →  other agents released unused quota
3. provider_direct   →  leftover headroom in daily limit
4. fallback provider →  try the other API
5. web_fetch         →  scrape (blocked for finance queries in Strategy A)
6. error             →  all paths exhausted
```

## Shared Pool Mechanics

When a scheduled agent finishes its work for the day, call `search_mark_agent_complete`. This releases any unspent allocation into the shared pool, which other agents can use.

Example: `stock-analysis` has 15 Gemini calls allocated, uses 8, then completes.
→ 7 calls are added to `providers.gemini.shared_pool`
→ Any other agent can now draw from those 7 calls

**Double-release protection:** Calling `search_mark_agent_complete` a second time on the same day returns an error — the agent's `completed` flag prevents the shared pool from being inflated.

## Circuit Breaker

Each provider has an in-memory circuit breaker:
- Opens after **3 consecutive failures**
- Auto-resets after **60 seconds**
- While open: that provider is skipped immediately (no network call)
- Resets on any successful call

The circuit breaker is per-process — it does not persist to disk.

## File Locking

`saveQuota()` uses `proper-lockfile` to prevent concurrent writes from multiple agents corrupting the quota file. If the lock cannot be acquired after 3 retries, the call returns an error — retry after a moment.

## Integrity Checks on Load

On every `loadQuota()`:
- Negative `used`, `remaining`, `shared_pool` counters are clamped to 0
- Old single-counter format (`used`) is migrated to per-provider (`gemini_used`, `brave_used`)
- Corrupted JSON is deleted and replaced with a fresh default file
