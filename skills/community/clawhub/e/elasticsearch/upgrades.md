# Upgrades — Version Paths, Breaking Changes, and OpenSearch

**Contents**: [The Upgrade Path Rule](#the-upgrade-path-rule) · [Rolling Upgrade Procedure](#rolling-upgrade-procedure) · [Breaking Changes That Bite](#breaking-changes-that-bite) · [Reindex From Remote](#reindex-from-remote) · [Elasticsearch vs OpenSearch](#elasticsearch-vs-opensearch) · [Version-Gated Features Referenced Elsewhere](#version-gated-features-referenced-elsewhere) · [Upgrade Gates](#upgrade-gates)

## The Upgrade Path Rule

- **Within a major**: upgrade directly between any two minors via a rolling restart. 8.3 → 8.15 is one operation.
- **Across a major**: go through the **last minor of the previous major** first. 7.4 → 8.x means 7.4 → 7.17 → 8.x. Skipping a major is not supported and the node refuses to start.
- **Index compatibility spans one major.** An 8.x node reads indices created by 7.x and 8.x, and refuses indices created by 6.x or earlier. Check before upgrading, not after:

```
GET /_migration/deprecations                                  # what will break
GET /_cat/indices?v&h=index,creation.date.string
GET /<index>/_settings?filter_path=**.version.created_string
```

- Indices too old to carry forward: reindex them on the current major (cheapest and best — it also fixes the mapping), or mount them read-only as archive indices on `elasticsearch >=8.3`, or snapshot and accept that restoring needs an old cluster.
- Two majors behind means two hops, each with its own testing round. Plan it as two projects.

## Rolling Upgrade Procedure

1. **Snapshot first**, and verify it. This is the rollback plan; a downgrade is not possible once a node writes with the newer version.
2. `GET /_migration/deprecations` on the current version and resolve everything flagged critical.
3. Upgrade a **non-production copy** restored from that snapshot, and run the real query suite against it. Deprecation warnings do not catch behaviour changes in scoring or aggregation defaults.
4. Disable shard allocation (`"cluster.routing.allocation.enable": "primaries"`) and flush before each node.
5. Upgrade **master-eligible nodes last**. A newer master cannot manage older nodes; older masters manage newer nodes fine.
6. Re-enable allocation, wait for green, then the next node. Never two at once.
7. Upgrade clients afterwards, as a separate change with its own rollback.

Rolling back a partially-upgraded cluster means restoring the snapshot. There is no downgrade path. That single fact should shape how much testing precedes step 4.

## Breaking Changes That Bite

| Change | Version | Impact |
|---|---|---|
| Mapping types removed | 7.0 | `_doc` only; `include_type_name` gone in 8.0. Old client code sending a type fails |
| `interval` split into `calendar_interval` / `fixed_interval` | 7.0 | Every `date_histogram` in dashboards and code |
| Default shards 5 → 1 | 7.0 | Indices created without an explicit count are suddenly single-shard |
| `hits.total` becomes an object | 7.0 | `hits.total.value` plus a `relation`, and capped at 10,000 by default |
| Security on by default, TLS required | 8.0 | Every client needs credentials and a CA. The largest practical hurdle in 7 → 8 |
| Transport client removed | 8.0 | Java applications must move to the REST client |
| `geo_polygon` query deprecated | 7.12 | Replace with a `geo_shape` query |
| `_source` disabled indices | ongoing | Cannot be reindexed, so they cannot cross a major boundary |
| System indices restricted | 7.10+ | Direct writes to `.kibana` and friends now fail |

Behaviour changes that no deprecation warning catches: scoring adjustments that reorder results, analyzer or tokenizer updates that change indexed terms, and default settings changes. This is why step 3 runs the query suite rather than a smoke test — the failure mode is worse rankings, not errors.

## Reindex From Remote

The escape hatch when the version gap is too wide for an in-place upgrade, and the safest option for anything critical.

```json
POST /_reindex?wait_for_completion=false&slices=auto
{ "source": { "remote": { "host": "http://old-cluster:9200",
                          "username": "u", "password": "p",
                          "socket_timeout": "60s" },
              "index": "products", "size": 1000 },
  "dest": { "index": "products", "op_type": "create" } }
```

- Requires `reindex.remote.whitelist` on the **destination** cluster, listing the source host and port.
- The destination pulls, so the new cluster controls the pace. Throttle with `requests_per_second` if the old cluster is still serving traffic.
- Create the destination index first with the mapping you want. This is the moment to fix every mapping mistake accumulated over the old cluster's life; it costs nothing extra here.
- Works across major versions that could never be upgraded in place, and lets both clusters run side by side while traffic is cut over gradually — which is a rollback plan a rolling upgrade does not have.

## Elasticsearch vs OpenSearch

- OpenSearch forked from Elasticsearch 7.10 when Elastic moved from Apache 2.0 to SSPL/Elastic License in 7.11. Elastic later re-added AGPLv3 as a licensing option (from 8.16), which changes the licensing argument but not the code divergence.
- Everything at the 7.10 baseline behaves the same: query DSL, mappings, analyzers, aggregations, bulk, ILM (as ISM in OpenSearch), snapshots.
- Post-fork, they diverge and the gap widens: ES-only features include the newer vector search stack (`int8_hnsw`, `bbq_hnsw`, RRF retrievers, `semantic_text`, ELSER), ES|QL, runtime-field evolution, and TSDS. OpenSearch has its own equivalents with different APIs and different maturity — its kNN plugin, its own hybrid query, and ISM in place of ILM.
- Clients are forked too, and the Elasticsearch 8.x client refuses to talk to an OpenSearch cluster via a product-check header. Use the `opensearch-*` client family rather than pinning a 7.x Elasticsearch client indefinitely.
- Managed offerings named "OpenSearch" (including AWS's) are the fork; the `deployment` variable records which one, so guidance comes out in the right dialect.
- Migration in either direction: snapshot restore works within the shared 7.10 lineage; beyond that, reindex from remote is the reliable path, because it moves documents rather than segments.

## Version-Gated Features Referenced Elsewhere

Quick index of the floors used across these guides, so a plan can be checked against `major_version` at a glance:

| Feature | Floor |
|---|---|
| Automatic release of the flood-stage read-only block | 7.4 |
| Point in time (PIT) | 7.10 |
| Runtime fields | 7.11 |
| `match_only_text` | 7.14 |
| Composable index templates | 7.8 |
| Data streams | 7.9 |
| `wildcard` field type | 7.9 |
| Searchable snapshots | 7.10 |
| `search.allow_expensive_queries` | 7.7 |
| kNN on `dense_vector`, security on by default | 8.0 |
| `subobjects: false` | 8.3 |
| `geohex_grid` | 8.1 |
| TSDS (time-series data streams) | 8.7 |
| RRF hybrid ranking | 8.8 (retriever syntax 8.14) |
| `dense_vector` dims up to 4096 | 8.11 |
| `semantic_text` | 8.15 |
| Binary quantization (`bbq_hnsw`) | 8.16 |

## Upgrade Gates

- Is there a verified snapshot taken immediately before, and a restore that has actually been timed?
- Has `_migration/deprecations` been run and every critical item resolved?
- Have the real queries run against a restored copy on the target version, with results compared rather than just checked for errors?
- Is the path legal (last minor of the previous major before crossing)?
- Are there indices created more than one major ago, and is there a plan for each?
- Are masters scheduled last, and is allocation disabled per node?
- Is the client upgrade a separate change with its own rollback?
