---
name: Elasticsearch
slug: elasticsearch
version: 1.0.2
description: >-
  Designs, queries, and operates Elasticsearch: mappings, analyzers, query DSL, aggregations, bulk indexing, shard sizing, and cluster health.
  Use when writing a search query or an index mapping, when a search returns nothing or the wrong documents, when a term query on a text field
  returns zero hits without an error, when results rank badly, when aggregations fail with "fielddata is disabled", when the cluster turns yellow
  or red, when shards stay unassigned, when indexing is slow or a bulk request returns per-item errors, when disk hits the flood-stage watermark
  and indices go read-only, when circuit breakers trip, or when paging past 10,000 hits breaks. Covers ILM rollover, reindexing, snapshots,
  upgrades, kNN and hybrid vector search, autocomplete, synonyms and analyzers, nested modeling, geo queries, ES|QL, Painless, ingest pipelines,
  data streams, security, language clients, and OpenSearch compatibility. Not for standalone vector stores (vector-databases) or lightweight
  site search (meilisearch).
homepage: https://clawic.com/skills/elasticsearch
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🔍
    requires:
      anyBins:
      - curl
    os:
    - linux
    - darwin
    - win32
    displayName: Elasticsearch
    configPaths:
    - ~/Clawic/data/elasticsearch/
---

User preferences and memory live in `~/Clawic/data/elasticsearch/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/elasticsearch/` or `~/clawic/elasticsearch/`), move it to `~/Clawic/data/elasticsearch/`.

## When To Use

- Writing or reviewing a query DSL body, an index mapping, an analyzer, or an aggregation
- Search is wrong: no hits, wrong documents, wrong order, wrong buckets, or duplicates
- The cluster is unhealthy: yellow or red, unassigned shards, read-only indices, breakers tripping, heap pressure
- Indexing or search is slow, or bulk requests fail, stall, or get rejected
- Designing the index layout: shard counts, aliases, templates, data streams, ILM, multi-tenancy, reindex plans
- Operating it: snapshots and restores, security and API keys, monitoring, rolling upgrades, migration to or from OpenSearch
- Not for choosing a standalone vector database, or for lightweight site search where a cluster is more than the job needs (see Related Skills)

## Quick Reference

| Situation | Play |
|---|---|
| Zero hits, no error, and you can see the value in `_source` | A `term` query against a `text` field, or case mismatch on a `keyword` — run `_analyze` and compare tokens (→ `debugging.md`) |
| Right documents, wrong order | Get `"explain": true` on one bad document before touching a single boost (→ `relevance.md`) |
| "Fielddata is disabled on text fields by default" | Aggregate and sort on the `.keyword` sub-field, never enable fielddata (Core Rules 9) |
| Need full-text search AND exact match on one field | Multi-field: `text` with a `fields.keyword` sub-field (→ `mapping.md`) |
| Need to change a field's type, analyzer, or `index` setting | Impossible in place: new index → `_reindex` → alias swap (Core Rules 3 → `index-lifecycle.md`) |
| Array of objects matches on the wrong combination | Objects flatten and lose per-item association; `nested` restores it (→ `data-modeling.md`) |
| Cluster yellow | Unassigned replicas; expected on a single node (set `number_of_replicas: 0`), otherwise `_cluster/allocation/explain` (→ `incidents.md`) |
| Cluster red | A primary is unassigned — some data is unreadable right now, stop writes and diagnose (→ `incidents.md`) |
| Every index suddenly rejects writes as read-only | Flood-stage disk watermark (→ `incidents.md`) |
| `circuit_breaking_exception` | A request asked for more heap than it may have — narrow the aggregation, do not raise the breaker (→ `incidents.md`) |
| `version_conflict_engine_exception` | Concurrent write: `retry_on_conflict` for updates, `if_seq_no`+`if_primary_term` for read-modify-write (→ `bulk-indexing.md`) |
| Paging past 10,000 hits fails | `search_after` with a point-in-time (Core Rules 8 → `search-performance.md`) |
| Search latency regressed | `"profile": true` on the slow query, then the search slow log for the pattern (→ `search-performance.md`) |
| Indexing throughput regressed | Refresh interval, merge pressure, and `write` thread-pool rejections, in that order (→ `bulk-indexing.md`) |
| Autocomplete / search-as-you-type | `edge_ngram` in the index analyzer only, never in the search analyzer (→ `autocomplete.md`) |
| Semantic search, embeddings, "find similar" | `dense_vector` + `knn`, blended with BM25 through RRF (→ `vector-search.md`) |
| Search by distance, radius, or bounding box | `geo_point` vs `geo_shape`, and the lat/lon ordering trap (→ `geo-search.md`) |
| Logs, metrics, traces, anything with a `@timestamp` | Data stream + ILM rollover, never hand-rolled daily indices (→ `logs-and-timeseries.md`) |
| Computed or derived value needed at query time | Runtime field first (no reindex), Painless `script_score` only if scoring depends on it (→ `scripting.md`) |
| "How do I write this in ES\|QL", or an ad-hoc slice-and-group investigation | `POST /_query` with a pipe: `FROM … \| WHERE … \| STATS … BY …`; no scoring, implicit `LIMIT 1000` (→ `esql.md`) |
| Alert when a NEW document matches a saved search | Reverse search: store the query in a `percolator` field and run `percolate` (→ `queries.md`) |
| Anything else | Shrink the query to the smallest failing form on one index, then in order: `_validate/query?explain` for syntax, `_analyze` for tokens, `_explain` for scoring, `_profile` for time |

Depth on demand, by phase:

- **Diagnose** — `debugging.md` why a document does not match or does not rank · `errors.md` error string to cause · `incidents.md` red cluster, read-only indices, breakers, heap · `monitoring.md` what to watch and alert on
- **Design** — `mapping.md` field types and mapping mechanics · `analyzers.md` the analysis chain, synonyms, language handling · `data-modeling.md` nested, parent-child, multi-tenancy, index granularity · `queries.md` the query DSL that matters, plus percolator reverse search · `esql.md` the piped query language, when to prefer it, and its row cap · `relevance.md` BM25, boosting, ranking evaluation · `aggregations.md` buckets, metrics, accuracy limits · `autocomplete.md` as-you-type, suggesters, highlighting · `vector-search.md` kNN, hybrid, RRF · `geo-search.md` points, shapes, distance, geo aggregations · `scripting.md` Painless and runtime fields
- **Load** — `bulk-indexing.md` bulk, reindex, ingest pipelines, concurrency control · `clients.md` REST conventions, language clients, retries and timeouts
- **Operate** — `search-performance.md` profiling, caches, deep pagination, PIT · `cluster.md` nodes, shards, allocation, sizing, rolling restarts · `index-lifecycle.md` templates, aliases, data streams, ILM, zero-downtime reindex · `snapshots.md` repositories, restore drills, disaster recovery · `security.md` authentication, API keys, RBAC, query injection · `upgrades.md` version paths, breaking changes, OpenSearch divergence · `logs-and-timeseries.md` observability workloads and retention

## Core Rules

1. **`text` matches, `keyword` filters.** A `text` field is analyzed into tokens; a `term` query is not analyzed. `"Quick Brown"` indexed as `text` becomes `[quick, brown]`, so `term: {title: "Quick Brown"}` matches nothing and returns HTTP 200 with zero hits — no error anywhere. Default shape for anything a human types AND a machine filters on: multi-field `text` + `fields.keyword`. Search `title`, filter and aggregate `title.keyword`.
2. **Filter context for everything that is not ranking.** Test: if dropping the clause would change WHICH documents come back but not their ORDER, it belongs in `bool.filter` or `bool.must_not`. Those skip BM25 entirely and are cached per segment; `must`/`should` score every hit. Tenant IDs, status flags, date ranges, term lists, geo boxes — always filter.
3. **Mappings are append-only.** New field: yes. Change an existing field's type, analyzer, or `index` flag: never, in any version. The only path is new index → `_reindex` → alias swap, so put every index that matters behind an alias on day one, before you need it (`index-lifecycle.md`). Corollary: `dynamic: strict` on anything user-facing, because a typo'd field name is otherwise silently created with a guessed type.
4. **Size shards from data volume, not from node count.** `primary_shards = max(1, ceil(expected_primary_gb / target_shard_size_gb))` — 600 GB at the 40 GB default (`target_shard_size_gb`) gives 15 primaries. Primary count is fixed at creation. Too few shards means slow recovery and a ceiling on parallelism; too many means wasted heap, because every shard is a full Lucene index with fixed overhead and the cluster hard-refuses allocation past `cluster.max_shards_per_node` (default 1000, replicas counted). Data that keeps growing gets rollover instead of a guess (`index-lifecycle.md`).
5. **Heap is half the RAM and never past the compressed-pointer threshold.** `Xms = Xmx = min(RAM/2, 31g)`. A 128 GB node still gets 31 GB; the other half is the OS page cache that Lucene actually reads from, and starving it costs more than the heap gains. Past roughly 32 GB the JVM drops compressed object pointers, so 33 GB of heap addresses fewer objects than 31 GB. Verify, do not assume: the startup log line reports `compressed ordinary object pointers [true]`.
6. **Bulk, never per-document, and find the ceiling by measurement.** Start at `bulk_batch_mb` (default 10 MB of payload, not document count) with a few requests in flight, raise until throughput flatlines or `es_rejected_execution_exception` appears — that rejection is the signal that you found the limit, not an error to retry harder against. A `_bulk` call returns HTTP 200 while individual items fail: branch on the response's `errors` flag every single time, or you will lose documents quietly.
7. **A rebuildable bulk load sets `refresh_interval: -1` and `number_of_replicas: 0`, then restores both.** Every refresh seals a segment; refreshing once per second (the default) through a four-hour load creates roughly 14,400 tiny segments that merging then has to grind back down. Adding replicas after the load copies finished segments instead of re-indexing every document. Escape hatch: keep replicas if the source cannot be replayed, since you are running without redundancy until they are back.
8. **Deep pagination is `search_after`, not `from`/`size`.** `from + size` must stay within `index.max_result_window` (default 10,000), and every shard sorts and ships `from + size` hits to the coordinating node, so page 500 costs each shard the same work as returning 10,000 documents. User-facing paging: `search_after` on a stable sort plus a point-in-time. Full exports: PIT scans or `_reindex`, never a paging loop (`search-performance.md`).
9. **Aggregate and sort on `keyword`, never on `text`.** `terms` on a `text` field fails with "Fielddata is disabled on text fields by default". Setting `fielddata: true` to silence it loads every distinct term of that field into heap, uninvertered per segment — the most common self-inflicted circuit breaker there is. The fix is always the `.keyword` sub-field, or `index: false` + `doc_values: true` if the field is aggregation-only.

## Search Triage

Symptom-first, in order. Steps 1-3 are seconds each and eliminate the causes that look like the expensive ones.

1. **Does the document exist?** `GET /<index>/_doc/<id>`. If not, the problem is ingest, not search (`bulk-indexing.md`).
2. **Does the query parse the way you think?** `GET /<index>/_validate/query?explain=true` with the body. A misplaced brace turns a `filter` into a no-op that silently matches everything.
3. **What tokens are actually indexed?** `POST /<index>/_analyze` with `{"field": "title", "text": "Quick Brown"}`. Compare against the query terms. Mismatch here explains most zero-hit reports (Core Rules 1) and every "it works for one word but not two".
4. **Why did THIS document not match?** `GET /<index>/_explain/<id>` with the query body — it names the clause that failed, per document.
5. **Why is it ranked HERE?** Same query with `"explain": true`, read the score breakdown top-down: field boost, then BM25 term frequency, then length norm (`relevance.md`).
6. **Where does the time go?** `"profile": true` — per-shard, per-clause timings. A slow `should` clause or a rewrite-heavy wildcard shows up as `rewrite_time` (`search-performance.md`).
7. **Is it the query or the cluster?** Re-run against one shard with `?preference=_shards:0`. Same latency means query cost; wildly different means an unhealthy node or a cold shard (`cluster.md`).

## Query Types That Matter

Everything else is a variation. Choose from the left column, never from habit.

| Need | Query | Trap |
|---|---|---|
| Exact value, filtering | `term` / `terms` | Analyzed field returns nothing (Core Rules 1); `terms` caps at `index.max_terms_count` (65,536) — beyond that use a terms lookup |
| Human-typed words | `match` | `operator: "or"` is the default: one matching word is a hit. Set `minimum_should_match: "75%"` for a real AND-ish feel |
| An exact phrase | `match_phrase` | `slop: 0` by default — "quick brown fox" will not match "quick fox" until you allow slop |
| Words across several fields | `multi_match` | `best_fields` (default) scores the single best field; `cross_fields` treats them as one field but demands the same analyzer everywhere |
| Numbers, dates, versions | `range` in filter context | Date math (`now-7d/d`) is evaluated per shard, and unrounded `now` defeats the request cache |
| Field present / absent | `exists` / `must_not: exists` | Empty string and empty array count as present; `null` and a missing key do not |
| Typo tolerance | `match` with `fuzziness: "AUTO"` | AUTO means 0 edits for terms of 1-2 chars, 1 edit for 3-5, 2 edits above 5 — short queries get no tolerance at all |
| Prefix / partial | `match_bool_prefix`, or an `edge_ngram` field | `wildcard`/`regexp` with a leading `*` scans every term in the field; use the `wildcard` field type or `autocomplete.md` |
| Combining any of the above | `bool` | `should` alongside `must`/`filter` requires zero matches by default; alone it requires one. State `minimum_should_match` explicitly |

## Shard and Heap Arithmetic

The canonical numbers; every guide references these rather than restating them.

| Quantity | Formula or range | Note |
|---|---|---|
| Primary shards | `max(1, ceil(primary_gb / target_shard_size_gb))` | `target_shard_size_gb` default 40; useful range 10-50 |
| Shard size, search workloads | 10-30 GB | Smaller shards, faster queries, more overhead |
| Shard size, log workloads | 30-50 GB | Throughput and retention beat query latency |
| Heap per node | `min(RAM/2, 31g)` | Core Rules 5 |
| Shards per node, soft budget | ≤ 20 shards per GB of heap | 31 GB heap → aim under 620 shards; the hard stop is `cluster.max_shards_per_node` (1000) |
| Total cluster shards | `indices × (primaries × (1 + replicas))` | Replicas count against every limit above |
| Disk headroom | Keep usage under the 85% low watermark | Full watermark ladder in `incidents.md` |

Worked example: 2 TB of primary log data, 40 GB target, one replica. Primaries = ceil(2000/40) = 50. Total shards = 50 × 2 = 100. At 31 GB heap per node that is well inside budget on three nodes — but as one index it would also be unrecoverable and unshrinkable, which is exactly why time-series data rolls over instead (`index-lifecycle.md`).

## Error Strings

Match on the exception type; the message text drifts between versions. Full catalog with fixes in `errors.md`.

| Exception | Means | First move |
|---|---|---|
| `illegal_argument_exception: Fielddata is disabled` | Aggregating or sorting on `text` | Use `.keyword` (Core Rules 9) |
| `cluster_block_exception ... read-only-allow-delete` | Flood-stage watermark tripped | Free disk; the block auto-clears below the high watermark on `elasticsearch >=7.4` (→ `incidents.md`) |
| `circuit_breaking_exception` | Request would exceed a heap breaker | Narrow the aggregation or the batch; raising the breaker converts a rejected query into a dead node |
| `version_conflict_engine_exception` | Concurrent write to the same `_id` | `retry_on_conflict` on updates; `if_seq_no`+`if_primary_term` for read-modify-write |
| `es_rejected_execution_exception` | Thread-pool queue full | Back off and reduce concurrency — retrying immediately makes it worse (`bulk-indexing.md`) |
| `mapper_parsing_exception` | Value does not fit the mapped type | Fix the producer or add an ingest coercion; the mapping cannot be changed (Core Rules 3) |
| `illegal_argument_exception: Limit of total fields [1000] has been exceeded` | Mapping explosion from dynamic fields | `dynamic: strict` or `flattened` (→ `mapping.md`); raising the limit postpones the outage |
| `search_phase_execution_exception` | A shard-level failure aggregated up | Read `failed_shards[].reason` — the real error is nested inside |
| `index_not_found_exception` on a wildcard | The pattern matched nothing | `ignore_unavailable` / `allow_no_indices`, or the alias never got swapped |
| `too_many_buckets_exception` | Aggregation exceeded `search.max_buckets` | Use `composite` for pagination instead of a huge `size` (→ `aggregations.md`) |

## Cluster Health In One Screen

```
GET /_cluster/health?level=indices          # green/yellow/red and where
GET /_cat/indices?v&s=store.size:desc       # size, doc count, health per index
GET /_cat/shards?v&h=index,shard,prirep,state,unassigned.reason
GET /_cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,disk.used_percent
GET /_cat/thread_pool/search,write?v&h=node_name,name,active,queue,rejected
GET /_cluster/allocation/explain            # why THIS shard is unassigned
GET /_nodes/hot_threads                     # what a pegged node is actually doing
```

`rejected` in the thread-pool output is cumulative since node start, not a rate — compare two samples a minute apart before concluding anything (`monitoring.md`).

Every request in this skill is written in Dev Tools / raw REST. When `client` is set to anything else, emit the same call in that language's client instead — `clients.md` carries the per-client retry, timeout, and bulk-helper branch.

## Output Gates

Before emitting a mapping, a query, or an index change:

- Every string field: is it `text`, `keyword`, or a multi-field — and does each use site match that choice (Core Rules 1, 9)?
- Every non-ranking clause in `bool.filter` rather than `bool.must` (Core Rules 2)?
- New index: born from a template, behind an alias, `dynamic` set explicitly, `default_replicas` applied, and the shard count derived from the formula and a stated volume rather than copied from a neighbour (Core Rules 4)?
- Paging: within `max_result_window`, or `search_after` + PIT if not (Core Rules 8)?
- Bulk or reindex: batched, the `errors` flag inspected per response, and resumable from a recorded key (Core Rules 6)?
- Relevance change: measured against a judgement set with `_rank_eval`, not eyeballed on one query (`relevance.md`)?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/elasticsearch/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| deployment | self-managed \| elastic-cloud \| serverless \| aws-opensearch \| opensearch-self-managed | self-managed | Which node, shard, and JVM settings are reachable at all; serverless and managed offerings hide most of `cluster.md`, and the OpenSearch values switch API names and drop ES-only features (→ `upgrades.md`) |
| major_version | 7 \| 8 \| 9 | 8 | Which version-gated advice applies when the live version is unknown, and what the upgrade path looks like |
| license_tier | basic \| gold \| platinum \| enterprise | basic | Suppresses recommendations behind a paid tier (ML and ELSER, document/field-level security, searchable snapshots, cross-cluster replication, Watcher alerting, audit logging) |
| client | dev-tools \| curl \| python \| javascript \| java \| go | dev-tools | The dialect every emitted request is written in (default: raw REST as shown throughout), and which row of the per-client retry, timeout, and bulk-helper branch in `clients.md` applies |
| target_shard_size_gb | number (10-50) | 40 | The divisor in the shard-count formula (Core Rules 4) and the `max_primary_shard_size` rollover condition |
| bulk_batch_mb | number (1-20) | 10 | Starting payload size per `_bulk` request (Core Rules 6) and the batch size in reindex and ingest recipes |
| default_replicas | number (0-2) | 1 | `number_of_replicas` in emitted index templates; 0 is correct for a single-node dev cluster, which otherwise sits yellow forever |
| destructive_confirm | bool | true | `DELETE` on an index or alias, `_delete_by_query`, index close, force merge, and cluster-settings writes are emitted for review instead of executed |

Preference areas — customizable dimensions; a stated preference is recorded in `config.yaml` and applied from then on:

- **Tooling** — Kibana Dev Tools vs a client library vs raw HTTP, ingest path (Beats, Logstash, Fleet, OpenTelemetry, application code), migration tooling
- **Thresholds** — slow-log warn levels, ILM rollover age and size, retention per tier, heap and disk alert points, how many hits a query may return by default
- **Conventions** — index and alias naming, field naming (ECS vs house schema), date-format policy, whether `_source` filtering is applied by default
- **Platform** — node roles and topology, storage class, region and zone awareness, container limits, whether dedicated master nodes exist
- **Risk posture** — whether reindex and ILM changes run directly or come back as reviewed requests, willingness to drop replicas during loads, appetite for `force_merge` on live indices
- **Output format** — request bodies only vs request plus a plan walkthrough, how much of an `explain` output to narrate, whether rollback steps ship with every change
- **Work order** — runtime field first vs reindex first when a mapping is wrong, whether relevance changes require an offline `_rank_eval` run before shipping
- **Integrations** — monitoring stack (Kibana Stack Monitoring, Prometheus exporter, provider console), snapshot repository (S3, GCS, Azure, shared filesystem), authentication backend (native, SAML, OIDC, LDAP)
- **Restrictions** — features the license or platform forbids, compliance regimes that mandate field-level security or encryption, indices that must never be closed or reindexed online
- **Cadence** — restore-drill frequency, ILM and mapping review cycle, snapshot schedule, index-usage audits

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `term` query on a `text` field | The query value is not analyzed; the indexed tokens are. Zero hits, HTTP 200, no error | `match`, or `term` on the `.keyword` sub-field (Core Rules 1) |
| `fielddata: true` to fix an aggregation error | Un-inverts the whole field into heap on every segment | `.keyword` sub-field (Core Rules 9) |
| Raising `index.max_result_window` to allow deep paging | Moves the failure from a clean error to an OOM under load | `search_after` + PIT (Core Rules 8) |
| Raising a circuit breaker limit to stop `circuit_breaking_exception` | The breaker is what stands between a heavy query and a dead node | Narrow the request; if it is legitimate, add heap or nodes |
| `edge_ngram` analyzer used at search time as well as index time | The query gets ngrammed too, so "ca" matches on "c" and everything matches everything | `search_analyzer: standard` on that field (`autocomplete.md`) |
| Index-time synonyms | Every synonym change means a full reindex, and the expansion is baked into scoring | Search-time `synonym_graph` (`analyzers.md`) |
| One index per tenant, at thousands of tenants | Each index costs heap and shard slots; the cluster hits `max_shards_per_node` long before disk fills | Shared index + filter, with custom routing for large tenants (`data-modeling.md`) |
| `force_merge` on an index still being written | Produces multi-GB segments that normal merging will never touch again | Force merge only after the index stops receiving writes (`index-lifecycle.md`) |
| Interpolating user input into `query_string` | Users can inject wildcards, regexes, and `*:*`; malformed syntax throws a 400 | `simple_query_string` or a `match` with `minimum_should_match` (`security.md`) |
| `scroll` for user-facing pagination | Holds a search context and a segment snapshot per scroll, capped by `search.max_open_scroll_context` | `search_after` + PIT for paging, PIT scans for exports |
| Deleting documents and expecting the disk back | Deletes are tombstones until the segments merge | Delete whole indices on a time boundary (`logs-and-timeseries.md`) |
| `dynamic: true` on user-controlled JSON | One caller with unique keys creates a field per key until the 1000-field limit stops all indexing | `dynamic: strict` or `flattened` (`mapping.md`) |
| Trusting a single-node yellow cluster as "almost healthy" | Yellow with `number_of_replicas: 1` on one node means the replica can never allocate — a real cluster in that state has no redundancy | Set `default_replicas: 0` in dev, or add a node |

## Where Experts Disagree

- **Nested vs denormalized documents.** Nested keeps per-item correctness but stores each sub-object as a hidden Lucene document, so a 20-item array is 21 documents to index, delete, and merge. Boundary: query the combination of two sub-fields together → `nested`; only ever filter on one at a time → flatten it (`data-modeling.md`).
- **Search-time synonyms vs reindexing.** Search-time expansion is editable without a reindex but costs query CPU and skews scoring for multi-word entries; index-time is fast and frozen. Boundary: a vocabulary that still changes monthly stays at search time; a settled thesaurus in a latency-critical path earns index time.
- **Sizing by shard-size rule vs by benchmark.** The 10-50 GB range is a starting posture, not a law: it comes from recovery and merge behaviour, not from your query shape. Anyone running a stable workload should benchmark one shard at real volume with real queries and size from the measured knee.
- **Elasticsearch as the primary store.** One camp keeps a system of record elsewhere and treats the index as rebuildable; the other writes straight to Elasticsearch. The testable boundary is whether you can afford to reindex from source after an unrecoverable mapping mistake or a corrupted shard — if you cannot, it was never a search index.
- **kNN alone vs hybrid retrieval.** Pure vector search wins on paraphrase and loses on exact identifiers, part numbers, and rare terms that no embedding preserved. Default to hybrid with RRF and only drop BM25 if an offline evaluation says it contributes nothing (`vector-search.md`).

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/elasticsearch (install if the user confirms):

- `search-engine` — engine-agnostic search design and relevance evaluation; jump there when the target is not Elasticsearch
- `meilisearch` — lighter site and product search when a cluster is more machinery than the job needs
- `vector-databases` — dedicated vector stores when embeddings are the whole workload rather than one field
- `rag` — retrieval design for LLM pipelines built on top of an index like this one
- `observability` — logs, metrics, and traces strategy above the storage layer

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/elasticsearch.
