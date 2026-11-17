# Performance

Fires: always

Leading word: **grandma's phone**. The oldest supported device, on a slow 3G network, with low battery, belonging to a power user with 10,000 items.

Artifact: a hot-path list (user action → work done → where it runs → cost at 10,000 items).

- **main-thread**: Disk, network, decoding, image processing or heavy computation on the UI thread; synchronous I/O in request handlers; `runBlocking`, `.sync` on the main queue, `readFileSync` on a request path.
- **startup** (when the app is a client, or a server with cold starts): Work done before the first useful frame or first byte: eager SDK init, migrations, network calls, large decodes. What can be deferred or done lazily?
- **render** (when there is a user interface): Lists without virtualization, re-render storms from broad state, images decoded at full size, layout recomputed per frame.
- **quadratic**: Nested loops, `contains` inside a loop, repeated sorts or searches over user-sized collections. Multiply out at 400 and at 10,000 items.
- **query** (when there is a database): N+1 queries, filters and foreign keys with no index, `select *` with no limit or pagination, counts computed by fetching rows, over-fetching columns the screen never shows.
- **network** (when the code calls a network): Chatty sequential calls that could be one, no HTTP caching, uncompressed or oversized payloads and images, no offline cache for data the user reopens.
- **memory**: Retain cycles, large allocations kept alive, unbounded in-memory caches. Background work that drains battery (timers, location, polling). Leaked tasks and listeners belong to the state lens.

Measure when you can (a profiler, a timed test, `EXPLAIN ANALYZE`) and mark those findings `CONFIRMED`.

Done: every hot path is in the list with its cost at 10,000 items.
