# Search Performance — Profiling, Caches, and Pagination at Depth

## Measure First, in This Order

1. **`took`** in the response — server-side search time, excluding network and client deserialisation. Compare it against client-observed latency; a large gap is a client problem.
2. **`"profile": true`** — per-shard, per-clause breakdown. Read `rewrite_time` (query expansion, the wildcard tell), `build_scorer`, `score`, `next_doc`, and the separate `collector` and `aggregations` trees.
3. **Search slow log** — the pattern across all traffic, not one query:

```json
PUT /<index>/_settings
{ "index.search.slowlog.threshold.query.warn": "2s",
  "index.search.slowlog.threshold.query.info": "500ms",
  "index.search.slowlog.threshold.fetch.warn": "500ms" }
```

Query phase and fetch phase are logged separately, and the distinction matters: a slow **query** phase is matching and scoring cost; a slow **fetch** phase is `_source` size, highlighting, or too many `top_hits`. They have nothing in common as fixes.

4. **`GET /_nodes/stats/indices/search`** — per-node query and fetch totals, and the queue. If one node's numbers dwarf the others, it is a hot shard, not a slow query.

## The Caches

| Cache | Scope | Invalidated by | Notes |
|---|---|---|---|
| Node query cache | Filter clauses, per segment, per node | Segment merge | Only caches filters used repeatedly on segments above a size threshold. `indices.queries.cache.size`, default 10% of heap |
| Shard request cache | Whole request, per shard | Refresh | Only for `size: 0` requests by default — aggregation dashboards benefit, result pages do not. `indices.requests.cache.size`, default 1% of heap |
| Field data cache | Fielddata on `text`, and global ordinals | Refresh (ordinals rebuilt) | If this is large, someone enabled `fielddata: true` (SKILL.md Core Rules 9) |
| OS page cache | Every segment file read | Memory pressure | The biggest cache by far, and the reason heap stops at half the RAM (Core Rules 5) |

Cache-defeating patterns worth hunting for:

- **Unrounded `now`** in a range filter. `"gte": "now-1h"` produces a new cache key every millisecond. `"now-1h/m"` rounds to the minute and makes the request cacheable, at a minute of staleness nobody notices.
- A per-user or per-request value inside a `filter` clause that is different every time — it belongs in `must` or should be restructured.
- Frequent refreshes: the request cache clears on every refresh, so a 1s refresh interval on a dashboard index means the cache never survives.

## Pagination at Depth

- **`from`/`size`** — each shard sorts and returns `from + size` hits to the coordinator, which merges and discards. Bounded by `index.max_result_window` (default 10,000). Correct for the first few pages, and only those.
- **`search_after`** — pass the previous page's `sort` values as the cursor. Constant cost per page regardless of depth. Requires a **unique, total** sort: append `_shard_doc` (added automatically with a PIT) or `_id` as the tiebreak, or pages will skip and repeat documents.
- **Point in time** — `POST /<index>/_pit?keep_alive=5m` returns an ID that freezes the segment view. Pass it instead of an index name so a concurrent refresh cannot shift the result set mid-pagination. **Close it** (`DELETE /_pit`) when done: an open PIT pins segments, and pinned segments cannot be merged away, so leaked PITs quietly grow disk usage.
- **`scroll`** — legacy. Holds a context per scroll, capped by `search.max_open_scroll_context` (default 500), and `search_context_missing_exception` is what a leaked or expired one looks like. Use PIT + `search_after` for everything new.
- **Exports** — PIT + `search_after` with `size: 5000` and a `_shard_doc` sort, or `_reindex` into a scratch index when the destination is Elasticsearch anyway.

Deep pagination is usually a product problem. Nobody clicks to page 500; a crawler or an export job got pointed at a paging endpoint. Rate-limit the endpoint and give the export a real API.

## Cutting Per-Request Work

- `"_source": {"includes": [...]}` or `filter_path` — the largest easy win on wide documents, because it cuts fetch, network, and client parsing at once.
- `track_total_hits: false` — skips counting matches beyond what is needed to fill the page. Default is `10000`, which already caps the cost; `false` removes it entirely, and `true` forces a full count. Set `false` for infinite-scroll UIs.
- `terminate_after: N` — stops each shard after N matching documents. Deterministic cost, incomplete results; right for typeahead, wrong for anything reporting a total.
- `"size": 0` on aggregation-only requests — skips the fetch phase.
- `?preference=<stable_string>` — routes a user's repeated queries to the same replica: warm caches and stable scores between pages.
- `_msearch` — one round trip for results plus facets plus counts, executed with shard-level parallelism.
- `async_search` (`elasticsearch >=7.7`) — submit a long analytical query, poll for partial results. Keeps a dashboard responsive instead of holding an HTTP connection for a minute.

## Structural Levers

- **Fewer shards per query.** Every shard is a unit of parallelism *and* a fixed coordination cost. A query fanning out to 200 shards to return 10 documents spends most of its time in merge overhead. Over-sharding is the most common cause of unexplained baseline latency (SKILL.md Shard and Heap Arithmetic).
- **Index-time work beats query-time work.** Precompute a field in an ingest pipeline instead of a runtime field or a script; flatten a nested structure the queries never need separated.
- **Index sorting** (`index.sort.field` at creation) lets a query with the same sort terminate early, and improves compression. Costs indexing throughput.
- **`force_merge` read-only indices** to one segment: fewer segments, less per-segment overhead, faster queries. Only on indices that will never be written again, or you create giant segments that normal merging will never reclaim.
- **Filter before scoring.** Every clause moved from `must` to `filter` removes a BM25 computation and gains a cache entry (SKILL.md Core Rules 2).
- **Routing.** A query restricted to one shard with `?routing=` avoids the fan-out entirely, when the data model supports it.

## Latency Symptom Table

| Symptom | Likely cause | Check |
|---|---|---|
| High `rewrite_time` in the profile | Wildcard, regexp, prefix, or fuzzy expanding to thousands of terms | `_validate/query?rewrite=true` |
| Slow fetch phase, fast query phase | Large `_source`, highlighting, or `top_hits` in aggregations | `_source` filtering; the `unified` highlighter with `offsets` |
| p50 fine, p99 terrible | GC pauses, or one hot shard | `_nodes/stats/jvm`, `_cat/shards` distribution |
| Slow only on the first request after a refresh | Cold caches and rebuilt global ordinals | Longer `refresh_interval`; `eager_global_ordinals` on a heavily aggregated keyword field |
| Everything slow, no query stands out | Over-sharding, or the page cache too small for the index | `_cat/shards` count; free RAM versus index size on disk |
| Slower as the day goes on | Index growing without rollover, or segment count climbing | `_cat/segments`, `_cat/indices` |
| One node much slower | Hot shard, failing disk, or an unbalanced allocation | `_cat/nodes`, `_nodes/hot_threads` |
| Aggregations slow, queries fine | Doc values not in page cache, or high-cardinality `terms` | `_nodes/stats/indices/fielddata`; lower `size`, or `composite` for pagination |
