# Performance — Finding The Real Ceiling

Order of investigation, because fixing them out of order wastes days: blocked loop → database → serialization → framework overhead. FastAPI's own dispatch is rarely the bottleneck; it is the fourth thing to look at, not the first.

## Measure Before Touching Anything

- Load-test with a tool that reports percentiles (`hey`, `wrk`, `k6`, `locust`) against a build that mirrors production: same worker count, same pool size, real database, no `--reload`.
- Run the two-route test first: if a trivial `/health` degrades along with the endpoint under test, the loop is blocked and nothing else matters yet (`async.md`).
- Middleware timing per route gives you the split: total time minus handler time is framework and middleware; handler time minus query time is your code.
- Profile a single slow request in process (`pyinstrument` as middleware, or `py-spy record` against the running worker) — a sampling profiler on a live worker is the fastest route to the offending frame.
- Count queries per request in development. A list endpoint whose query count grows with page size is N+1 and no amount of tuning elsewhere will fix it (`database.md`).

## Where The Time Usually Is

| Symptom | Likely cause |
|---|---|
| All routes slow together, including health | Blocked event loop or full threadpool (`async.md`) |
| One route slow, latency flat with load | Slow query or slow upstream |
| One route slow, latency grows with load | Pool exhaustion or lock contention (`database.md`) |
| Fast locally, slow in production | Network round trips per request, cold caches, or a proxy with no keep-alive |
| CPU pinned at 100% with modest traffic | JSON serialization of large payloads, or CPU work on the loop |
| Memory grows until OOM | Unbounded concurrency, an unbounded in-process cache, or a response built fully in memory (`streaming.md`) |

## Serialization

- Response validation runs the whole payload through the response model a second time (SKILL.md rule 4). On a 5,000-item list that is the dominant cost; on a single object it is noise.
- Levers, in order of preference: return fewer items (paginate), return fewer fields (a leaner response model), then skip validation on that one route (`response_model=None` and return an explicit response).
- `ORJSONResponse` replaces the stdlib encoder with orjson, which its benchmarks put several times faster than `json` — visible on large payloads, invisible on small ones. Set it app-wide with `default_response_class=ORJSONResponse` once you have measured a serialization-bound route.
- Never build a giant list in memory to return it: stream it (`streaming.md`) or paginate it.
- `GZipMiddleware(minimum_size=500)` trades CPU for bandwidth; on a mobile-facing JSON API it usually wins, on an internal service on the same network it usually loses.

## Pagination

- Offset pagination degrades linearly: `OFFSET 100000` makes the database walk 100,000 rows before returning any. Fine for the first pages, unusable for deep ones.
- Keyset (cursor) pagination is constant time: `WHERE (created_at, id) < (:last_created, :last_id) ORDER BY created_at DESC, id DESC LIMIT :n`, with an index on exactly that tuple. Cost: no random access to page N.
- Always cap `limit` server-side (`Annotated[int, Query(le=100)]`); an uncapped limit is a denial-of-service parameter.
- Total counts are expensive on large tables — return `has_more` from fetching `limit + 1` rows instead of `COUNT(*)`.

## Caching Layers

| Layer | Mechanism | Notes |
|---|---|---|
| Client/CDN | `Cache-Control`, `ETag` + `If-None-Match` → 304 | Cheapest possible response; needs a stable representation |
| Shared cache | Redis, keyed by resource and version | Works across workers, unlike anything in-process (SKILL.md rule 6) |
| Per-process | `@lru_cache` on pure, argument-hashable functions | Hit rate divided by the worker count; only for static data |
| Per-request | A dependency computed once and reused | Free deduplication of repeated lookups (`dependencies.md`) |

Invalidation belongs with the write path: the code that updates the row deletes the key. A TTL alone means every reader can see stale data for the whole TTL, which is a product decision, not a technical default.

## Connection Reuse

- One `httpx.AsyncClient` per process, created in lifespan. A new client per request means a fresh TCP and TLS handshake each time — often more expensive than the call itself.
- Size the client's connection pool (`httpx.Limits(max_connections=100, max_keepalive_connections=20)`) so one slow upstream cannot consume all sockets.
- Database connections likewise: the pool exists to avoid per-request connection setup, which on Postgres over TLS is measured in milliseconds, not microseconds.

## Framework-Level Wins Worth Having

- `uvicorn[standard]` (uvloop + httptools) is a free constant-factor gain on the loop and the HTTP parser.
- Dependency graphs cost a little per node per request; a dependency doing I/O on every route (a feature-flag fetch, an audit write) is a tax on the whole API.
- Pydantic v2 validation is fast enough that request parsing is rarely visible in a profile; if it is, the model is unusually large or `extra="allow"` is keeping everything.
- Compression, TLS termination, and static files belong in front of the app; serving assets through `StaticFiles` in production spends worker time on bytes a proxy serves better.

## Capacity Arithmetic

Throughput ceiling per worker ≈ concurrency ÷ average latency. A route averaging 50 ms with an effective concurrency of 20 in-flight requests sustains ~400 requests/second per worker; the same route at 500 ms sustains ~40. That is why cutting a 500 ms query to 50 ms buys more than ten extra workers, and why blocking calls (which drop effective concurrency to 1 on the loop, or to 40 in the threadpool) dominate everything else.
