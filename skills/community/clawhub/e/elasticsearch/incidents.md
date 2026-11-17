# Incidents — Red Clusters, Read-Only Indices, Breakers, and Heap

Ordered by how often each one wakes people up. Every chain starts with a check, not a change.

**Contents**: [First Sixty Seconds](#first-sixty-seconds) · [Every Index Went Read-Only](#every-index-went-read-only) · [Cluster Red](#cluster-red) · [Cluster Yellow](#cluster-yellow) · [Circuit Breakers](#circuit-breakers) · [Heap Pressure and GC](#heap-pressure-and-gc) · [Thread-Pool Rejections](#thread-pool-rejections) · [Node Will Not Start](#node-will-not-start) · [Data Loss Triage](#data-loss-triage) · [Post-Incident](#post-incident)

## First Sixty Seconds

```
GET /_cluster/health?level=indices
GET /_cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,disk.used_percent,master
GET /_cat/indices?v&health=red
GET /_cat/shards?v&h=index,shard,prirep,state,unassigned.reason | grep -v STARTED
```

Three questions in order: **is data missing** (red), **is the cluster accepting writes** (read-only blocks), **is a node about to die** (heap, disk, GC). Everything else waits.

## Every Index Went Read-Only

Symptom: writes fail with `cluster_block_exception ... blocked by: [FORBIDDEN/12/index read-only / allow delete (api)]`.

1. Confirm the cause: `GET /_cat/allocation?v` — one node above 95% (flood stage) blocks **every index with a shard on it**, not just the full node's own indices.
2. Free disk. In order of speed: delete old time-based indices (instant reclaim), clear a snapshot repository staging directory, add disk. `_delete_by_query` reclaims nothing until merges run — the wrong tool in an emergency.
3. On `elasticsearch >=7.4` the block clears automatically below the high watermark. If it does not, or on 7.3 and earlier, release it explicitly:

```json
PUT /_all/_settings
{ "index.blocks.read_only_allow_delete": null }
```

4. Root cause afterwards: no ILM delete phase, an index with no rollover, a snapshot that never completes, or an oversized translog. Alert at 80% so this never repeats.

## Cluster Red

A primary shard is unassigned: some data cannot be read or written right now.

1. `GET /_cluster/allocation/explain` (no body returns the first unassigned shard). Read `unassigned_info.reason` and every decider that returned `no`.
2. `NODE_LEFT` and the node is coming back → wait. `index.unassigned.node_left.delayed_timeout` (default 1m) exists so a restart does not trigger a full re-replication; raise it to 5-10m during planned maintenance.
3. `ALLOCATION_FAILED` → the shard failed to open repeatedly. `POST /_cluster/reroute?retry_failed=true` after fixing the underlying cause; the retry counter is what is blocking, not the original error.
4. Watermark or filtering decider said no → free disk, or fix `index.routing.allocation.*` rules that no surviving node satisfies.
5. **No valid shard copy exists** (the disk really is gone) → the only options are restore from snapshot, or `POST /_cluster/reroute` with `allocate_stale_primary` / `allocate_empty_primary`. The first accepts possibly-stale data; the second **destroys that shard's data permanently**. Never run either without confirming the snapshot situation first.

## Cluster Yellow

Replicas are unassigned; all data is readable, redundancy is not there.

- One node with `number_of_replicas: 1` — permanent yellow by definition. Set `default_replicas: 0` in dev, or add a node.
- After a node loss, yellow is the expected intermediate state while replicas rebuild. Watch `_cat/recovery?active_only=true` for progress rather than re-checking health.
- Yellow that never resolves with spare nodes available: allocation filtering, awareness rules forcing a zone that no longer exists, or `total_shards_per_node` set too low.

## Circuit Breakers

`circuit_breaking_exception` means a request was **rejected to save the node**. It is the system working.

| Breaker | Default limit | Usual trigger |
|---|---|---|
| parent (real memory) | 95% of heap | Aggregate pressure; the one that usually fires |
| request | 60% of heap | One aggregation building too many buckets or a huge `cardinality` precision |
| fielddata | 40% of heap | Someone set `fielddata: true` on a `text` field (SKILL.md Core Rules 9) |
| in-flight requests | 100% of heap | Bulk payloads too large, too many concurrent |
| script compilation | rate-based | Scripts interpolating values into source |

The response names the breaker and the byte amounts. Fix the request, not the limit: raising a breaker converts a rejected query into an OOM-killed node, which takes its shards with it.

## Heap Pressure and GC

Signals: heap above 75% sustained after old-gen GC, `[gc][old]` lines with pauses above a second, node timing out of the cluster and rejoining.

1. `GET /_nodes/stats/jvm?human` — look at `mem.heap_used_percent` and old-gen collection **counts and times**, not instantaneous usage. Sawtooth to 75% is healthy; a floor that keeps rising is not.
2. `GET /_nodes/stats/breaker` — which breaker holds the memory.
3. `GET /_cat/fielddata?v&s=size:desc` — if this is non-trivial, that is the leak (Core Rules 9).
4. Segment and shard overhead: `GET /_cat/shards?v` count per node against the `20 shards per GB of heap` budget (SKILL.md). Too many shards is a slow, permanent heap tax that no query tuning fixes.
5. `GET /_nodes/hot_threads?threads=3` — what the CPU is actually doing during the stall.
6. Only after the above: more heap, up to the `min(RAM/2, 31g)` ceiling, or more nodes.

A node that leaves the cluster during a long GC and rejoins is not a network problem, even though the logs say so.

## Thread-Pool Rejections

`es_rejected_execution_exception` means a queue filled.

```
GET /_cat/thread_pool/search,write,get?v&h=node_name,name,active,queue,rejected
```

- `rejected` is cumulative since node start. Take two samples a minute apart; a big number that is not moving is history.
- `write` rejections → the client is pushing harder than the cluster absorbs. Back off. Raising `queue_size` buys latency and memory, not throughput.
- `search` rejections → too much concurrency or too many shards per query. Reduce fan-out before adding nodes.
- Rejections on one node only → hot shard or a sick node, not a capacity problem.

## Node Will Not Start

| Log line | Cause |
|---|---|
| `max virtual memory areas vm.max_map_count [65530] is too low` | `sysctl -w vm.max_map_count=262144`; the top container failure |
| `failed to obtain node locks` | Another process already owns the data directory, or a stale lock after an unclean kill |
| `the default discovery settings are unsuitable for production` | Bootstrap checks: set `discovery.seed_hosts` and `cluster.initial_master_nodes` |
| `master not discovered yet` | Seed hosts wrong, network partition, or no quorum among master-eligible nodes |
| `unsupported/incompatible index version` | An index created too many majors ago; reindex from the previous major or restore it read-only |
| `bootstrap checks failed: memory locking requested but not available` | `bootstrap.memory_lock: true` without the matching `LimitMEMLOCK` / ulimit |

## Data Loss Triage

When a shard copy is genuinely gone:

1. Stop writes to the affected indices — a partially-written index is harder to reconcile than a stopped one.
2. Inventory what exists: `GET /_snapshot/<repo>/_all?verbose=false` and `GET /_cat/shards` for the surviving copies.
3. If the source data is replayable (a log pipeline, a database of record), reindexing from source beats every restore option and produces a complete index.
4. If not, restore the index from the most recent snapshot into a **new** index name, verify counts, then swap the alias.
5. `allocate_empty_primary` is the last option and it is destructive. Write down what it will discard, get that acknowledged, then run it.

## Post-Incident

- Was there an alert before the user report? Disk at 80%, heap floor rising, and rejection rate are the three that give real warning.
- Did the index have rollover and a delete phase? Most disk incidents are a missing ILM policy.
- Was there a current, **restore-tested** snapshot? An untested snapshot is a hypothesis.
- Did anyone raise a limit to make an error go away? Record it — that setting is the next incident.
