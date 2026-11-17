# Snapshots — Backup, Restore, and Disaster Recovery

A snapshot you have never restored is a hypothesis. Everything below assumes the restore drill is the deliverable, not the snapshot schedule.

## How Snapshots Actually Work

- Snapshots are **incremental at the Lucene segment level**: the second snapshot copies only segments created since the first. A daily snapshot of a 2 TB index that receives 20 GB/day transfers roughly 20 GB, plus whatever merging rewrote.
- They are **not** point-in-time consistent across indices in the transactional sense. Each shard is snapshotted at a consistent moment for that shard; documents written mid-snapshot may or may not be included.
- Snapshots are cheap on the cluster but not free: they compete for disk I/O and network. `max_snapshot_bytes_per_sec` on the repository throttles them.
- Deleting a snapshot only removes segments no other snapshot references, so repository size does not fall proportionally when you delete one.
- File-level copies of the data directory are **not** a backup. Segments referenced by an in-flight merge produce an index that fails to open. The snapshot API is the only supported path.

## Registering a Repository

```json
PUT /_snapshot/backups
{ "type": "s3",
  "settings": { "bucket": "es-backups", "base_path": "prod", "compress": true,
                "max_snapshot_bytes_per_sec": "100mb", "max_restore_bytes_per_sec": "200mb" } }
```

- Types: `s3`, `gcs`, `azure`, `hdfs`, and `fs` (a shared filesystem). For `fs`, the path must be in `path.repo` in `elasticsearch.yml` on **every** master and data node, and it must be genuinely shared storage — a local directory per node produces a repository that only ever holds a third of your shards.
- Verify after registering: `POST /_snapshot/backups/_verify` confirms every node can write to it. `POST /_snapshot/backups/_analyze` runs a deeper correctness and performance check on the storage's consistency guarantees.
- Credentials go in the keystore (`elasticsearch-keystore add s3.client.default.access_key`), never in `elasticsearch.yml`.
- **Never point two clusters at the same repository path for writing.** Both will believe they own the metadata, and the repository ends up corrupt. Use `readonly: true` on the second cluster's registration.

## Taking Snapshots

```json
PUT /_slm/policy/daily
{ "schedule": "0 30 2 * * ?", "name": "<prod-{now/d}>", "repository": "backups",
  "config": { "indices": ["*"], "include_global_state": true },
  "retention": { "expire_after": "30d", "min_count": 7, "max_count": 60 } }
```

- SLM automates the schedule **and the expiry**. Without retention, the repository grows until the bill or the bucket limit stops it.
- `include_global_state: true` captures index templates, ILM policies, ingest pipelines, stored scripts, and cluster settings — everything you would otherwise rebuild by hand at the worst moment. It does not include security roles and users unless the `.security` index is in scope.
- Snapshots are per-index; run one policy for the whole cluster rather than per-team policies whose overlapping schedules fight for I/O.
- `GET /_snapshot/backups/_current` shows an in-flight snapshot; `DELETE` on it aborts cleanly.

## Restoring

```json
POST /_snapshot/backups/prod-2026.07.25/_restore
{ "indices": "products-v2",
  "rename_pattern": "(.+)", "rename_replacement": "restored-$1",
  "index_settings": { "index.number_of_replicas": 0 },
  "include_aliases": false }
```

- **Restore into a new name and verify before swapping the alias**. Restoring over a live index requires closing it first, which is an outage you chose.
- `include_aliases: false` prevents the restore from stealing a live alias the moment it completes — the single most damaging default to get wrong.
- Restoring is a full data transfer, unlike snapshotting. Restore throughput, not snapshot throughput, is what determines your recovery time. Measure it.
- Track progress with `GET /_cat/recovery?active_only=true&v`, not by polling cluster health.
- A restored index keeps its original shard count and mapping. Changing either still requires a reindex.

## Searchable Snapshots

`elasticsearch >=7.10`, licensed. Mounts a snapshot as a searchable index without a full restore.

- `fully_mounted` (cold tier) keeps a full local copy: normal search speed, and it removes the need for replicas because the snapshot is the redundancy.
- `partially_mounted` (frozen tier) caches blocks on local disk on demand: a tiny fraction of the storage, first-query latency in seconds rather than milliseconds. The right home for compliance data queried twice a year.
- The repository becomes part of the serving path, not just the recovery path. Its availability and durability now affect queries, which changes how you treat the bucket's lifecycle rules.

## Disaster Recovery Tiers

| Approach | Recovery time | Data loss window | Cost |
|---|---|---|---|
| Snapshot + restore | Hours (transfer-bound) | Up to the snapshot interval | Storage only |
| Snapshot to a second region | Hours + cross-region transfer | Snapshot interval | Storage + egress |
| CCR follower cluster (licensed) | Minutes (promote the follower) | Seconds | A second cluster |
| Rebuild from source of record | Hours to days | None | Pipeline capacity |

The fourth is the one people forget, and it is often the best: if Elasticsearch is a derived index over a database or a log pipeline, reindexing from source gives a complete, correct index and needs no snapshot at all. It also fixes any mapping mistake in the same pass. Cluster-level DR effort should be proportional to how *un*-replayable the source is.

CCR replicates mistakes as faithfully as data — a bad `_delete_by_query` reaches the follower in seconds. It covers infrastructure failure, not human error. Snapshots cover both.

## The Restore Drill

Quarterly, on a schedule, into a scratch cluster or a renamed index:

1. Pick the most recent snapshot without looking at whether it succeeded — that check is part of the drill.
2. Restore one representative index. Time it end to end and write the number down; that measured figure is your real RTO, and it is usually several times the estimate.
3. Verify `_count`, run three real queries, and compare results against production.
4. Confirm `include_global_state` actually restored templates, ILM policies, and pipelines — this is the part that is quietly missing when a real incident arrives.
5. Record the date and the measured time. A drill whose result nobody wrote down did not happen.

## Snapshot Gates

- Is the repository verified from every node, and registered read-only on any secondary cluster?
- Does SLM have a retention policy, and is the repository size trending flat rather than upward?
- Is `include_global_state: true` set, and has a restore proved that templates and ILM policies come back?
- Has a restore been timed in the last quarter, with the number written down?
- Do restores go to a new index name with `include_aliases: false`?
- Is there a written answer to "could we just reindex from source instead", with the reason?
