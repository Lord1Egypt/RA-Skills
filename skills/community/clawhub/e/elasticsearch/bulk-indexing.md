# Bulk Indexing, Reindex, and Ingest — The Write Path

**Contents**: [What Happens When You Index a Document](#what-happens-when-you-index-a-document) · [Bulk Format and Error Handling](#bulk-format-and-error-handling) · [Tuning the Load](#tuning-the-load) · [Refresh Semantics on Write](#refresh-semantics-on-write) · [Concurrency Control](#concurrency-control) · [Reindex](#reindex) · [Ingest Pipelines](#ingest-pipelines) · [Write-Path Symptoms](#write-path-symptoms)

## What Happens When You Index a Document

1. The coordinating node routes it: `shard = hash(_routing) % number_of_primary_shards` — which is exactly why primary count is immutable (SKILL.md Core Rules 4).
2. The primary shard writes to an in-memory buffer and appends to the **translog**.
3. `refresh` (every `refresh_interval`, default 1s) turns the buffer into a searchable segment. **This is when the document becomes visible to search**, not when the write returns.
4. `flush` fsyncs segments to disk and truncates the translog.
5. Background merges combine small segments into larger ones and physically drop deleted documents.

Most write-performance work is about steps 3 and 5: fewer refreshes, fewer segments, less merging.

## Bulk Format and Error Handling

```
{"index": {"_index": "products", "_id": "1"}}
{"title": "Wireless router", "price": 89.99}
{"update": {"_index": "products", "_id": "2", "retry_on_conflict": 3}}
{"doc": {"price": 79.99}}
```

Newline-delimited JSON, action line then payload line, and a **trailing newline on the last line** — omitting it produces a confusing parse error rather than a clear one.

- A `_bulk` call returns HTTP 200 even when every item failed. Branch on the top-level `errors` boolean, then walk `items[]` for the ones with a `status` ≥ 400 (SKILL.md Core Rules 6). Silent document loss almost always starts here.
- Retry only the failed items, never the whole batch: reindexing successes wastes work and, with auto-generated IDs, creates duplicates.
- Failures worth distinguishing: `mapper_parsing_exception` (bad data — fix the producer, retrying will never help), `version_conflict_engine_exception` (concurrency — retry the item), `es_rejected_execution_exception` (back-pressure — back off and reduce concurrency), `circuit_breaking_exception` (batch too large — halve it).
- Actions: `index` (create or replace), `create` (fail if `_id` exists — the idempotent choice), `update` (partial merge or script), `delete`.
- Auto-generated IDs skip the "does this ID already exist" lookup and are measurably faster. Use them for append-only data; use explicit IDs whenever a replay must be idempotent.

## Tuning the Load

| Lever | Setting | Note |
|---|---|---|
| Payload size | `bulk_batch_mb`, default 10 MB | Bytes, not document count — 10,000 small logs and 200 large documents are different requests |
| Concurrency | ~2 in-flight requests per write thread | The `write` pool is one thread per allocated processor; queue depth 10,000 |
| Refresh | `refresh_interval: -1` during load, restore after | SKILL.md Core Rules 7 |
| Replicas | `number_of_replicas: 0` during a rebuildable load | Restore after; recovery copies segments instead of re-indexing |
| Durability | `index.translog.durability: async` + `sync_interval: 5s` | Trades up to 5s of acknowledged writes on a node crash for real throughput. Only for replayable data |
| Merge throttling | `indices.store.throttle` is gone; use `index.merge.scheduler.max_thread_count: 1` on spinning disks | On SSD the default is right |

Find the ceiling empirically: start at the defaults, double concurrency until throughput stops rising or rejections appear, then step back one notch. The rejection is the answer, not an error to fight.

## Refresh Semantics on Write

- `?refresh=false` (default) — return immediately, visible within `refresh_interval`.
- `?refresh=wait_for` — return once the change is visible, without forcing a refresh. Blocks up to `refresh_interval`, costs nothing extra. The right choice for "write then read" in a UI.
- `?refresh=true` — force an immediate refresh. Creates a tiny segment per call; a loop doing this generates thousands of segments and hours of merging. Almost never correct outside tests.

The read-your-own-write alternative that costs nothing: `GET /<index>/_doc/<id>` is real-time (it reads the translog), so fetching by ID after a write always works even before a refresh. Only *searching* is refresh-bound.

## Concurrency Control

- Every write bumps `_seq_no` and `_primary_term`. Read-modify-write: read the document with those two, then write back with `if_seq_no` and `if_primary_term`. A mismatch throws `version_conflict_engine_exception` — the whole point.
- `retry_on_conflict: N` exists only on `_update` and bulk `update` actions. It re-reads and re-applies the script or partial document, so it is safe for commutative updates (counters) and unsafe for anything order-dependent.
- External versioning (`version_type: external`) lets an upstream system's version number win: Elasticsearch accepts the write only if the supplied version is higher. The correct pattern for CDC pipelines replaying out of order.
- `_delete_by_query` and `_update_by_query` snapshot at start; documents changed after the snapshot throw conflicts. `conflicts: "proceed"` continues and reports `version_conflicts` in the result — read that number, do not assume zero.

## Reindex

```json
POST /_reindex?wait_for_completion=false&slices=auto
{ "source": { "index": "products-v1", "size": 2000,
              "query": {"range": {"@timestamp": {"gte": "2026-01-01"}}} },
  "dest":   { "index": "products-v2", "op_type": "create" } }
```

- `wait_for_completion=false` returns a task ID immediately. Track with `GET /_tasks/<id>`, cancel with `POST /_tasks/<id>/_cancel`. Anything above a few minutes must run this way or an HTTP timeout will orphan it.
- `slices: auto` parallelises to one slice per source shard — the single biggest speedup available.
- `op_type: create` makes the reindex idempotent: existing IDs are reported as conflicts rather than overwritten, so a resumed run does not redo work.
- `requests_per_second` throttles a reindex that is starving live traffic. It can be changed on a **running** task with `POST /_reindex/<task_id>/_rethrottle`, and `-1` removes the limit.
- **Reindex does not copy settings or mappings.** Create the destination index first, from a template, with the corrected mapping and `refresh_interval: -1`, `number_of_replicas: 0`.
- Cross-cluster: `source.remote` with a host, whitelisted via `reindex.remote.whitelist`. This is also the supported path across incompatible major versions.
- Verify before the alias swap: compare `_count` on both sides with the same query, and spot-check a sample of documents field by field.

## Ingest Pipelines

Transformation at write time, on ingest-role nodes, before the document reaches a shard.

```json
PUT /_ingest/pipeline/weblogs
{ "processors": [
    {"grok":   {"field": "message", "patterns": ["%{COMBINEDAPACHELOG}"]}},
    {"date":   {"field": "timestamp", "formats": ["dd/MMM/yyyy:HH:mm:ss Z"], "target_field": "@timestamp"}},
    {"geoip":  {"field": "clientip", "target_field": "geo"}},
    {"remove": {"field": ["message", "timestamp"], "ignore_missing": true}} ],
  "on_failure": [ {"set": {"field": "ingest_error", "value": "{{ _ingest.on_failure_message }}"}} ] }
```

- Attach with `?pipeline=weblogs`, or set `index.default_pipeline` on the index so nobody can forget. `index.final_pipeline` runs after it, for enrichment nobody may override.
- **Always define `on_failure`**, at the pipeline level at minimum. Without it, one malformed line rejects the document and the data is gone; with it, the document lands with an error field you can query for later.
- Test before deploying: `POST /_ingest/pipeline/weblogs/_simulate` with sample documents, and `?verbose=true` to see the document after every processor.
- `grok` patterns backtrack: an unanchored pattern on a long line can burn CPU on every document. Anchor with `^`/`$`, prefer `dissect` for fixed-delimiter formats — it is several times faster because it does no regex at all.
- Pipelines run on ingest nodes; a heavy pipeline on a cluster with no dedicated ingest role competes with search on the same machines.

## Write-Path Symptoms

| Symptom | Cause | Fix |
|---|---|---|
| Throughput falls as the load runs | Merge pressure from too-frequent refreshes | `refresh_interval: 30s` or `-1` (Core Rules 7) |
| `es_rejected_execution_exception` on writes | `write` queue full | Reduce client concurrency and back off; adding nodes helps, retrying harder does not |
| Bulk latency spikes every few seconds | Large merges, or translog flush | Check `GET /_cat/thread_pool/write?v` and merge stats in `_nodes/stats/indices/merges` |
| Documents indexed but not searchable | Refresh has not run yet | `?refresh=wait_for`, or fetch by ID (real-time) |
| Disk grows much faster than data | Deleted-document tombstones awaiting merge | Expected; delete whole indices instead where possible |
| Every document rejected after a schema change | Mapping conflict | `mapper_parsing_exception`; mappings are append-only (Core Rules 3) |
| Reindex much slower than the original load | No slicing, or the destination kept `refresh_interval: 1s` and replicas | `slices: auto`, and prepare the destination index |
