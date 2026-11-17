# Rate Limits — Budgets, 429s, Spending Less

## Read the Headers Before the Wall

- `X-RateLimit-Remaining` low → slow down preemptively; reacting only to the 429 means you already exceeded the limit and may already be penalized.
- `X-RateLimit-Reset` semantics differ per API: epoch seconds (GitHub) vs seconds-until-reset — sleeping "until epoch 1750000000" as a delta is a multi-year sleep; check which one before computing.
- Header names are non-standard: `X-RateLimit-*`, `RateLimit-*` (IETF draft), or nothing at all — some APIs document limits only in prose. The service section states what the provider sends.

## What Kind of Limit Is It

The symptom pattern identifies the mechanism:

| Symptom | Mechanism | Consequence |
|---|---|---|
| Fails at consistent clock boundaries (top of minute/hour) | Fixed window | Bursting right after reset is safe; bursting across the boundary double-spends |
| Smooth rate fine, short bursts fail | Token bucket / leaky bucket | Spread requests; burst capacity is the bucket size, not the per-hour number |
| 429 only when running requests in parallel, low total rate | Concurrency cap, not a rate limit | Limit in-flight requests (semaphore); backoff alone won't fix it |
| One endpoint limited, others fine | Per-endpoint buckets (GitHub search vs core) | A 429 on one endpoint says nothing about the others |
| Limits hit with traffic you didn't send | Per-key or per-IP bucket shared with other clients | Separate keys per client, or move off a shared egress IP |

GraphQL APIs meter by computed query cost, not request count (→ `graphql.md` Rate Limits Are Cost-Based).

## When You Get a 429

- Honor `Retry-After` when present (parse rules and retry formula: `resilience.md` Retry Logic; canonical backoff: SKILL.md Core Rule 2).
- Stop the whole worker pool, not just the failing request — other in-flight requests spend the same bucket and extend the penalty on providers that punish continued violations.
- A burst of 429s is normal operation; a sustained plateau means demand exceeds quota — reduce demand (below) or buy a higher tier. Alert on the plateau, not the burst.

## Spending Less of the Limit

- Request the documented max page size — 10× fewer requests for the same data (→ `pagination.md`).
- Batch endpoints where offered: one call for N items (→ `async-jobs.md` Batch Endpoints).
- Conditional requests: a 304 is cheap or free — GitHub does not count conditional requests that return 304 against the rate limit (→ `caching.md`).
- Webhooks instead of polling for change detection (→ `webhooks.md`); if you must poll, decay the interval (→ `async-jobs.md` Polling Discipline).
- Throttle client-side below the documented limit, leaving headroom for retries and for other processes sharing the key — a client tuned to exactly the limit 429s on its own retry traffic.

## Multiple Instances, One Key

- N workers each spending the full budget = N× overrun. Divide the limit by instance count, or centralize the counter (shared token bucket in Redis or equivalent).
- Serverless scale-out is the worst case: unbounded concurrency turns one traffic spike into an instant 429 storm — put a queue with a concurrency cap between the trigger and the API call.
- Per-user OAuth tokens usually get per-user buckets — fan work out across user tokens instead of funneling everything through one app credential where the provider's terms allow it.
