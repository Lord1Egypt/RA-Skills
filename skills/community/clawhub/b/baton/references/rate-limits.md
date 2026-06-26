# Baton rate-limit and load-spreading policy

Baton's rate-limit management is a best-effort local coordination mechanism for multiple main agents sharing providers/models.

## Files

```text
.openclaw/baton/rate-limits.json
.openclaw/baton/runtime/rate-state.json
.openclaw/baton/runtime/rate-state.lock
```

## Policy schema

```json
{
  "version": 1,
  "defaults": {
    "maxConcurrentPerProvider": 4,
    "maxConcurrentPerModel": 2,
    "cooldownMsAfter429": 120000,
    "cooldownMsAfterTimeout": 60000,
    "spreadParallelWorkers": true
  },
  "providers": {
    "openai": { "maxConcurrent": 3, "cooldownMsAfter429": 180000 },
    "anthropic": { "maxConcurrent": 2 }
  },
  "models": {
    "openai/gpt-5-mini": { "maxConcurrent": 2 }
  }
}
```

## Routing under load

1. Avoid providers/models with active cooldown.
2. Prefer zero-active providers for new parallel fan-out.
3. Respect provider and model max concurrency.
4. Use same-tier fallback before tier escalation.
5. Defer low-priority work rather than causing a thundering herd.
6. Record failures and set cooldowns on 429/rate-limit/timeouts.

## Multi-agent fairness

Each main agent should include `agentId` in leases. Baton should use short leases and expire stale ones. This avoids one stuck agent blocking the shared model pool indefinitely.

## Human-facing behaviour

If rate limits constrain execution, say that Baton is reducing parallelism or using an alternative allowed model. Do not expose secret provider keys, raw auth profiles, or internal session IDs.
