# Performance — Query Budgets, Caching, Profiling

Order of attack, because it is almost always this order: **count the queries** → **fix the worst query** → **cache what is still expensive** → **move work out of the request**. Caching before counting hides an N+1 behind a warm cache and lets it explode the day the cache is cold.

## Measure First

| Question | Tool |
|---|---|
| How many queries does this path run? | `assertNumQueries(n)` in a test, `CaptureQueriesContext` in code |
| Which queries, and how long each? | `django.db.backends` logger at DEBUG |
| What is the database's plan for this one? | `qs.explain(analyze=True)` |
| Where does the time go inside the view? | `time.perf_counter()` around the suspicious blocks, or a sampling profiler |
| Which endpoints matter at all? | Request-duration metrics in production; optimizing an endpoint nobody calls is free entertainment |

- `connection.queries` only fills when `DEBUG = True`, so it is a development tool. `CaptureQueriesContext` works regardless and is what belongs in tests.
- Time in the shell is not time in the request: serialization, template rendering, middleware and connection setup are all absent there.
- Record the number before and after. "It feels faster" has approved plenty of changes that made things slower.

## The Query Budget

- A page's query count must be constant in the number of rows it displays. Budget = 1 query for the page + 1 per `prefetch_related` + 0 for `select_related` + 1 for the count if you paginate (SKILL.md Core Rules 1 owns this formula).
- Pin it with `assertNumQueries` on the endpoints that matter. It is the only test that fails when someone adds `{{ order.customer.name }}` to a template.
- Constant but large is a separate problem: 40 constant queries per page usually means several serializers each doing their own lookup — hoist them into the queryset with annotations.
- Pagination count: `Paginator` runs `COUNT(*)` per page. Options in order of effort: cache the count, use `show_full_result_count = False` in the admin, or switch to cursor/keyset pagination which needs no count at all.

## Database-Side Wins

- Index what you filter, join, and sort on. The ORM creates indexes for foreign keys and unique constraints, never for your composite `WHERE`.
- `only()`/`defer()` matter when a table has large text or JSON columns you do not display — otherwise the win is small and the deferred-field trap is real.
- `values()`/`values_list()` skip model instantiation. For a large read-only export, that is a meaningful saving; for 50 rows it is noise.
- Aggregate in the database, not in Python. A `Count`/`Sum` annotation replaces a loop that fetches every row to add numbers.
- `bulk_create`/`bulk_update` with a batch size replace per-row writes; size the batch from the backend's parameter ceiling.
- Deep `OFFSET` pagination reads and discards every skipped row: page 500 at 50 per page reads 25 000 rows to return 50. Keyset pagination (`filter(created_at__lt=cursor)`) is flat.
- When the plan itself is the problem — a sequential scan, a bad join order, a misestimate — that is a database question, not a Django one (see Related Skills in SKILL.md).

## Caching Layers

| Layer | Granularity | Invalidation |
|---|---|---|
| Per-site (`UpdateCacheMiddleware` + `FetchFromCacheMiddleware`) | Whole anonymous responses | Time only. Never for authenticated pages |
| Per-view (`@cache_page(600)`) | One view's response | Time; vary with `@vary_on_headers("Cookie")` or it serves one user's page to another |
| Template fragment (`{% cache 600 name key %}`) | A block of HTML | Time, plus every variable in the key |
| Low-level (`cache.get_or_set(key, fn, 600)`) | Any Python value | Yours to design — the only layer where correctness is achievable |
| Queryset result | A computed list | Yours; store ids, not model instances, when the objects are large |

- **The key must contain everything the content depends on.** A fragment cached on `order.id` but rendered differently for staff serves staff HTML to customers. This is the most common cache bug in Django applications.
- `LocMemCache` is per-process: with N workers there are N independent caches and N × the misses, and a `cache.delete()` in one worker leaves the other copies stale. Its `MAX_ENTRIES` default of 300 with `CULL_FREQUENCY` 3 also evicts a third of the cache at random once full. Use Redis or Memcached for anything shared.
- The default `TIMEOUT` is 300 seconds; `None` means never expire, `0` means never cache. Passing `None` where you meant "default" caches forever.
- `cache.get_or_set` still lets N concurrent misses all compute the value (a thundering herd). For expensive values, add a short lock key or accept a stale value while one worker refreshes.
- Invalidate on write, in `transaction.on_commit` — invalidating inside the transaction leaves the cache repopulated from a read that the rollback then contradicts (SKILL.md Core Rules 5).
- Cache versioning (`KEY_PREFIX`, `VERSION`) invalidates everything at once at deploy time, which is often cheaper than reasoning about individual keys.

## Sessions, Connections, Startup

- Database-backed sessions add a read (and often a write) per authenticated request; a cached or `cached_db` engine removes the read.
- `CONN_MAX_AGE = 0` (the default) reconnects on every request: a TCP handshake plus authentication before your first query. Raise it, and then count total connections.
- A slow first request after deploy is import time: module-level work in `apps.py`, heavy imports, or a warm-up query. Move it into `ready()` deliberately, or accept it and add a warm-up request to the deploy.
- Context processors and middleware run on every request; a query in either is a query on every page of the site.

## Move Work Out Of The Request

- Anything the user does not need in the response — email, PDF generation, third-party calls, denormalization — belongs in a task queue.
- Pre-compute expensive aggregates into a summary table refreshed on a schedule. A dashboard that aggregates a million rows per view will never be fast enough to cache well.
- Stream large exports (`StreamingHttpResponse` with `.iterator()`) instead of building them in memory, or hand the job to a task that writes to storage and emails a link — the second keeps the worker free.
- If a request must call several external services, that is the case where async views genuinely win.

## Diminishing Returns

- Beyond the query count and one or two hot queries, most Django "optimization" is noise against network latency and template rendering. Verify against a profile before rewriting readable code.
- Denormalization buys reads and costs consistency. Do it when a measured aggregate is the bottleneck, keep exactly one writer for the derived column, and prefer a database-maintained `GeneratedField` (Django >=5.0) where the expression allows it.
- Scaling workers hides latency; it does not reduce it, and it multiplies database connections. Fix the query before adding the instance.
