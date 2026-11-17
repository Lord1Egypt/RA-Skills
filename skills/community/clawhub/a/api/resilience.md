# Resilience Traps

Rate-limit budgeting, 429 handling, and header semantics live in `rate-limits.md`; this file covers retries, timeouts, circuit breakers, outages, and pooling.

## Retry Logic

- Retry policy by status class: 429/502/503/504 → backoff and retry; 500 → retry only idempotent requests; any other 4xx → never retry, fix the request
- Backoff formula (canonical: SKILL.md Core Rule 2): `sleep = random(0, min(cap, base × 2^attempt))`, base 1s, cap 30-60s, max `retry_max` retries (default 4) — full jitter, per the AWS backoff-and-jitter analysis; equal deterministic backoff re-synchronizes clients into a thundering herd
- `Retry-After` overrides the formula; it arrives as either delta-seconds (`Retry-After: 30`) or an HTTP-date — parse both
- Retry on POST without an idempotency key = duplicates. Stripe accepts an `Idempotency-Key` header and stores keys for 24h — reuse the same key on every retry of the same logical operation, a fresh key per retry defeats the mechanism
- Retry budget: cap total time (retries included) below your caller's timeout, or your caller retries you and multiplies traffic

## Timeouts

- Set both, always: connect timeout 3-5s (TCP/DNS should be fast or never), read timeout 10-30s for sync APIs — raise read only for endpoints documented as slow (LLM generation, report exports)
- No timeout = a hung request holds its thread/socket forever; the default in many HTTP libraries is no timeout
- Read timeout includes server processing time, not just network — a timeout tuned to network latency alone fires on every slow-but-healthy response
- Client-side timeout doesn't cancel server-side work: the operation may still complete — treat a timed-out POST like a 500 (unknown outcome, retry only with idempotency key)

## Circuit Breaker

- Reference defaults (Hystrix): open when error rate >50% over a 10s rolling window with ≥20 requests; retry one probe after 5s (half-open). The volume floor matters: without it, 1 failure in 1 request = "100% error rate" and the circuit flaps
- Half-open without a request limit = flood on the recovering server
- Circuit per host, not per endpoint = one bad endpoint takes down all calls to the service
- No circuit-state metrics/logging = outages are undebuggable ("why is everything failing instantly with no requests sent?")

## Provider Outages

- 5xx spike or timeout wave → check the provider's status page before debugging your code; a regional incident shows in your logs only as undifferentiated failures
- Degrade deliberately: feature-flag each integration so its outage disables one feature, not the app — the flag also gives you a kill switch when YOUR retry traffic is making their incident worse
- During the outage: queue writes and replay them with idempotency keys (Retry Logic above); serve reads from cache with staleness stated (→ `caching.md`) — never fabricate a fresh-looking answer
- After recovery, drain the queue with backoff at reduced concurrency: every other client is draining too, and the synchronized flood re-kills the recovering service (same jitter law as SKILL.md Core Rule 2)

## Error Handling

- Generic catch that silences all errors = invisible bugs; branch on status class first
- Retry that logs every attempt at error level = log flood during an outage; log once per operation with attempt count
- Error inside the fallback handler = crash instead of graceful degradation; fallbacks must be simpler than the primary path
- Async error without a handler = unhandled rejection, process may die

## Connection Pooling

- Pool exhausted = requests queue or fail without any network error — check pool metrics before blaming the API
- Stale connection in pool = first request after idle fails, second succeeds; the "works on retry" smell — enable idle eviction or keep-alive probes
- Pool size too large = you become the DoS; size to (peak concurrent requests) + small headroom, not "big number"
