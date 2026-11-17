# Monitoring — What to Watch, What to Alert On, What to Ignore

Most Elasticsearch dashboards show fifty metrics and alert on the wrong three. This is the short list that predicts incidents, with the thresholds that give useful warning time.

## Alert On These

| Signal | Where | Alert at | Why this number |
|---|---|---|---|
| Disk used per node | `_cat/allocation` | 80% | The low watermark is 85% and relocation needs free space to work with; 80% leaves room to act |
| Cluster status red | `_cluster/health` | Immediately | A primary is unassigned: data is unavailable now |
| Cluster status yellow | `_cluster/health` | Sustained >15 min | Brief yellow during recovery is normal; persistent yellow means no redundancy |
| JVM heap after old GC | `_nodes/stats/jvm` | Floor above 75% | Healthy heap sawtooths back down; a rising floor precedes GC death spiral |
| Thread-pool rejections | `_cat/thread_pool` | Any sustained rate | Cumulative counter — alert on the derivative, not the value |
| Search latency p99 | Application side | Your SLO | Server `took` misses queueing and network |
| Indexing rate drop | `_nodes/stats/indices/indexing` | >50% below baseline | A stalled pipeline is invisible to health checks |
| Total shard count | `_cat/shards` | 80% of `cluster.max_shards_per_node × nodes` | The limit is a hard refusal that stops tomorrow's rollover |
| Unassigned shards | `_cluster/health` | >0 for >10 min | `node_left.delayed_timeout` is 1m; beyond that it is not transient |
| SLM policy failures | `_slm/stats` | Any | A silently failing snapshot is discovered during a restore |
| ILM errors | `_ilm/explain` | Any step in ERROR | A stuck policy means indices stop rolling and stop being deleted |

## Do Not Alert On These

- **Instantaneous heap percentage.** The JVM is supposed to fill the heap and collect. Only the post-collection floor carries information.
- **Segment count.** It rises and falls with merging by design.
- **Total `rejected` count.** Cumulative since node start; a large number from three months ago fires forever.
- **CPU during merges or a reindex.** Expected, and throttling it can be worse than the spike.
- **Yellow on a single-node dev cluster.** Structural, not a fault.

## The Metrics Endpoints

```
GET /_cluster/health?level=indices
GET /_cluster/stats?human                      # cluster-wide totals: shards, docs, store, JVM
GET /_nodes/stats?human                        # everything per node; large — use filter_path
GET /_nodes/stats/jvm,os,fs,thread_pool?human
GET /_nodes/stats/indices/search,indexing,merges,refresh,translog
GET /_cat/allocation?v&s=disk.percent:desc
GET /_cat/thread_pool/search,write,get?v&h=node_name,name,active,queue,rejected
GET /_ilm/explain                              # per-index lifecycle state
GET /_slm/stats                                # snapshot policy successes and failures
```

Scrape with `filter_path` rather than pulling whole `_nodes/stats` payloads on a short interval — the response is megabytes on a large cluster and the collection itself becomes load.

## Slow Logs

```json
PUT /<index>/_settings
{ "index.search.slowlog.threshold.query.warn":  "2s",
  "index.search.slowlog.threshold.query.info":  "500ms",
  "index.search.slowlog.threshold.fetch.warn":  "500ms",
  "index.indexing.slowlog.threshold.index.warn": "5s" }
```

- Thresholds are **per shard**, not per request: a query taking 300 ms on each of ten shards never appears at a 500 ms threshold even though the user waited longer.
- Query phase and fetch phase log separately and have unrelated causes.
- `index.search.slowlog.level` controls verbosity; the logged source is truncated by default, and raising that limit fills the disk on a busy cluster.
- Set `X-Opaque-Id` on client requests: it appears in the slow log and in `_tasks`, and it is the only reliable link from a slow application request to a specific query.

## Tracing a Slow Request Right Now

```
GET /_tasks?actions=*search*&detailed=true      # what is running, with the query source
GET /_tasks?actions=*reindex*&detailed=true
POST /_tasks/<task_id>/_cancel
GET /_nodes/hot_threads?threads=3&interval=1s   # what a pegged node is doing
```

`_tasks` with `detailed=true` shows the query text of in-flight searches. Combined with `hot_threads` it usually names the offender in under a minute, which is faster than reconstructing from logs.

## Capacity Trends Worth Charting

These are the ones that give weeks of warning rather than minutes:

- Primary store size per index over time, with the rollover threshold drawn on it.
- Shards per node against the `20 per GB of heap` budget (SKILL.md Shard and Heap Arithmetic).
- Documents indexed per day, so retention math stays connected to reality.
- Search rate and p99 on the same chart — latency rising while rate is flat means the data grew, not the traffic.
- Snapshot repository size, which should flatten once SLM retention is working.

## Deciding What Broke

| Observation | Points at |
|---|---|
| One node's heap, CPU, or latency far above the others | Hot shard or a sick node |
| All nodes degrade together, gradually | Data growth outrunning page cache, or shard count creep |
| Latency spikes correlated with `[gc][old]` log lines | Heap pressure |
| Search rejections but low CPU | Too many shards per query — coordination overhead, not compute |
| Write rejections with healthy CPU and disk | Client concurrency above the write pool |
| Cluster metrics clean, users complain | Client-side: connection pool, deserialisation, or a timeout retry storm |
| Latency step-change at a deploy | A query shape change; diff the slow log before and after |

## Monitoring Gates

- Does a disk alert fire at 80%, before the low watermark?
- Is the heap alert on the post-GC floor rather than instantaneous usage?
- Are rejection alerts computed as a rate?
- Do SLM and ILM failures page someone, or only appear when queried?
- Is `X-Opaque-Id` set by the application so slow queries can be traced back?
- Is there a chart that would have shown the last incident coming a week earlier? If not, that is the chart to add.
