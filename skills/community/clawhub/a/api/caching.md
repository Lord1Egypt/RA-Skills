# Caching — Conditional Requests and Client-Side Caches

## Conditional GETs

- Store the response's `ETag`, send it back as `If-None-Match`; 304 Not Modified = your copy is current, no body transferred. `Last-Modified`/`If-Modified-Since` is the timestamp fallback when there is no ETag.
- 304s are cheap on both sides: GitHub does not count conditional requests returning 304 against the rate limit — the correct way to poll a resource for changes (→ `rate-limits.md` Spending Less).
- A 304 has no body: code that unconditionally parses the response crashes on the cache hit it asked for — branch on 304 before parsing.
- ETags are per-URL and per-variant: store them keyed by the full URL including query params, and by anything you vary (`Accept`, language) — one global "the etag" corrupts the cache on the second endpoint.
- Weak ETags (`W/"..."`) validate freshness but not byte-identity — don't use them for `If-Range` resume (→ `files.md` Downloads).

## Client-Side Caching Discipline

- The cache key must include the credential's identity when responses are per-account — a shared cache without it serves tenant A's data to tenant B. This is the one caching bug that is also an incident.
- Respect `Cache-Control` when the API sends it; absent, choose TTL by volatility and say so: reference data (currencies, country lists) hours, object data minutes, anything the user just wrote — see next bullet.
- Invalidate on your own writes: after a successful POST/PATCH/DELETE, evict or update the cached GET for that resource — read-your-writes is not guaranteed by the API (→ `debug.md` Intermittent Failures) and definitely not by your stale cache.
- Balances, inventory, live prices: don't cache, or cache for seconds and surface staleness ("as of 10:32") — a wrong-but-confident number is worse than a slow one.
- Negative caching: cache a 429/503 for the `Retry-After` horizon so concurrent callers don't pile onto a limited endpoint; never cache 4xx as if the resource state were known.

## What Never Goes in the Cache

- Presigned URLs — they expire; cache the API call that mints them, not the URL (→ `files.md`).
- OAuth tokens — they have their own refresh lifecycle, not a TTL cache (→ `auth.md` OAuth).
- Error pages from the edge (HTML 5xx) — caching one poisons the cache with a non-API response (→ `debug.md` Intermittent Failures).
