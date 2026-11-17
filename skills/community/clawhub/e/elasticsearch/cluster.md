# Cluster — Nodes, Shards, Allocation, and Staying Available

Sizing formulas live in SKILL.md (Shard and Heap Arithmetic); this is the topology and operations around them.

## Node Roles

| Role | Job | Sizing note |
|---|---|---|
| `master` | Cluster state: mappings, index metadata, allocation decisions | Dedicated masters on any cluster above ~6 nodes. CPU and a little RAM; no data |
| `data_content` / `data_hot` / `data_warm` / `data_cold` / `data_frozen` | Store and search shards | Where the RAM and disk go |
| `ingest` | Run ingest pipelines | Only worth separating when pipelines are heavy |
| `ml` | Machine learning jobs, ELSER inference | Licensed; keep off data nodes so a model does not evict page cache |
| `remote_cluster_client` | Cross-cluster search and replication | Required on coordinating nodes doing CCS |
| coordinating-only (all roles disabled) | Fan out queries and merge results | A load-balancer with a JVM; useful when result merging is heavy |

**Three dedicated master-eligible nodes** is the availability answer, and the number is not arbitrary: quorum is `floor(n/2) + 1`, so 3 survives one loss and 2 survives none. Two master-eligible nodes are strictly worse than one.

## Bootstrapping and Split Brain

- `cluster.initial_master_nodes` is used **once**, on the very first start of a brand-new cluster. Leaving it in the config afterwards means a node that loses its data directory can bootstrap a *second* cluster with the same name — the modern split-brain. Remove it after the first successful formation.
- `discovery.seed_hosts` is the ongoing list of master-eligible addresses; it is required and stays.
- `elasticsearch >=7.0` replaced `minimum_master_nodes` with automatic voting configurations. Never set the old one; never manually edit voting exclusions except to remove a master permanently.

## Shard Allocation

```
GET /_cat/shards?v&h=index,shard,prirep,state,node,unassigned.reason,store
GET /_cluster/allocation/explain            # the one command that answers "why"
```

`_cluster/allocation/explain` names the exact deciders that said no. Read it before changing any setting; the usual answers are disk watermark, allocation filtering, shard-per-node limits, or "no valid shard copy exists".

- `index.routing.allocation.require.<attr>` / `include` / `exclude` pins shards to nodes by attribute — how hot/warm tiers, rack awareness, and node decommissioning all work.
- `cluster.routing.allocation.awareness.attributes: zone` spreads replicas across zones. With `force.zone.values` set, the cluster refuses to over-allocate into a surviving zone during an outage, keeping capacity honest.
- `index.routing.allocation.total_shards_per_node` prevents one index from concentrating on one node — the fix for a hot node holding four of five primaries.
- Decommission a node by adding it to `cluster.routing.allocation.exclude._name` and waiting for shards to drain **before** shutting it down. Pulling it first triggers a full re-replication under load.
- Rebalancing is throttled by `cluster.routing.allocation.node_concurrent_recoveries` (default 2) and `indices.recovery.max_bytes_per_sec` (default 40 MB/s). Raising the latter speeds recovery and competes with live traffic for disk and network.

## Restarts Without an Outage

Rolling restart, per node:

1. `PUT /_cluster/settings` → `"cluster.routing.allocation.enable": "primaries"` — stops replica shuffling for a node that is coming back in minutes.
2. `POST /_flush` — commits the translog so the returning node replays less on startup. (Synced flush, `_flush/synced`, was the 7.x form of this step; it was deprecated in 7.6 and removed in `elasticsearch >=8.0`, where sequence numbers do the same job automatically. On 8.x and later, plain `_flush` is the whole step.)
3. Stop the node, do the work, start it.
4. Re-enable allocation (`"enable": null`) and wait for green before touching the next node.

Skipping step 1 means the cluster starts rebuilding every replica the moment the node disappears, then throws the work away when it returns.

## Disk Watermarks

| Watermark | Default | Effect |
|---|---|---|
| low | 85% | No new shards allocated to the node |
| high | 90% | Shards actively moved off the node |
| flood_stage | 95% | Every index with a shard on that node goes read-only |

The flood-stage block auto-releases below the high watermark on `elasticsearch >=7.4`. Alert at 80%, well before the low watermark, because relocation itself needs free space to work with.

## Cross-Cluster Search and Replication

- **CCS** queries remote clusters as `remote_name:index` in the same request. Latency is the slowest remote's latency; `skip_unavailable: true` per remote keeps one unreachable cluster from failing the whole search.
- **CCR** replicates indices to a follower cluster (licensed). Follower indices are read-only and lag by network round-trip plus indexing time. The disaster-recovery pattern that keeps a warm standby; not a backup, because a bad write replicates too.
- Both need `remote_cluster_client` on the coordinating nodes, and the remote configured under `cluster.remote`.

## Cluster State and Its Limits

- Every mapping, index setting, alias, template, and stored script lives in the cluster state, held in memory on **every** node and published on every change. Ten thousand indices with a thousand fields each is a cluster-state problem long before it is a disk problem.
- Symptoms of a bloated cluster state: slow master elections, slow index creation, master node CPU spikes on every write to metadata, `_cluster/state` responses in the tens of megabytes.
- The fixes are structural: fewer indices (rollover with larger shards), fewer fields (`dynamic: strict`, `flattened`), fewer aliases.
- `cluster.max_shards_per_node` (default 1000, replicas included) is a hard refusal, not a warning. Hitting it stops index creation cluster-wide — including tomorrow's rollover index, at whatever hour that runs.

## Capacity Planning

Work from measurements, not from ratios:

1. Index a representative day of real data into one shard of a test index.
2. Read `GET /_cat/indices?v&h=index,docs.count,pri.store.size` to get bytes per document after compression — typically 0.5-1.5× the raw JSON size depending on field count and mapping choices.
3. Total primary size = bytes/doc × expected documents. Multiply by `(1 + replicas)` for disk, then add 30% headroom (merges need free space, and the low watermark starts at 85%).
4. Shard count from the formula (SKILL.md); node count from disk, then check heap: `shards_per_node ≤ 20 × heap_gb`.
5. Benchmark queries at target concurrency on that one shard before multiplying. Query latency does not scale linearly with shard count, and finding out in production is expensive.

## Node Prerequisites Everyone Forgets

- `vm.max_map_count = 262144` — Elasticsearch refuses to start below it. The single most common container-startup failure.
- File descriptors 65,536; process limit 4,096.
- **Swap off**, or `bootstrap.memory_lock: true`. A swapped-out JVM heap turns garbage collection into a multi-second disk-bound stall, which the cluster experiences as a node failure.
- Heap: `Xms = Xmx`, both at `min(RAM/2, 31g)` (SKILL.md Core Rules 5). Never let the JVM resize the heap at runtime.
- Same JVM, same Elasticsearch version, same hardware profile across data nodes. A single slow node drags every fan-out query to its latency, because the coordinator waits for the last shard.
