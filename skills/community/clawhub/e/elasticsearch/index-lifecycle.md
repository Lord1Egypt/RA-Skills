# Index Lifecycle — Templates, Aliases, Rollover, ILM, and the Alias Swap

Mappings are append-only (SKILL.md Core Rules 3), so the ability to move to a new index without downtime is the operational foundation everything else stands on. Build it before you need it.

## Component and Index Templates

```json
PUT /_component_template/base-settings
{ "template": { "settings": { "number_of_shards": 3, "number_of_replicas": 1,
                              "refresh_interval": "30s" } } }

PUT /_index_template/logs
{ "index_patterns": ["logs-*"], "priority": 200,
  "composed_of": ["base-settings", "ecs-mappings"],
  "template": { "settings": { "index.lifecycle.name": "logs-policy" } },
  "data_stream": {} }
```

- Component templates are reusable blocks; index templates compose them and add their own. Highest `priority` wins when patterns overlap, and only **one** index template applies per index — templates do not merge across priorities.
- Templates apply at index **creation**. Changing one never touches existing indices; the change lands on the next rollover.
- Verify before relying on it: `POST /_index_template/_simulate_index/logs-2026.07.26` shows the exact settings and mappings a new index would receive.
- `elasticsearch >=7.8` uses composable templates; the legacy `_template` API still exists and is applied only when no composable template matches. Mixing the two is a reliable source of "my settings did not apply".

## Aliases

- Every index that will ever be reindexed sits behind an alias, from day one. Applications only ever name the alias.
- Atomic swap — both operations in one request, so there is no moment with zero or two targets:

```json
POST /_aliases
{ "actions": [ {"remove": {"index": "products-v1", "alias": "products"}},
               {"add":    {"index": "products-v2", "alias": "products"}} ] }
```

- **Filtered aliases** carry a query: `{"add": {"index": "orders", "alias": "orders-acme", "filter": {"term": {"tenant": "acme"}}}}`. Tenant isolation the application cannot forget.
- An alias spanning several indices is read-only for writes unless exactly one member has `"is_write_index": true`. Without it, an indexing request to the alias fails.
- `?routing` can be baked into an alias so every query through it goes to one shard.

## Rollover and Data Streams

Rollover creates a new backing index when a condition is met, so no index grows without bound.

```json
PUT /_ilm/policy/logs-policy
{ "policy": { "phases": {
  "hot":    { "actions": { "rollover": { "max_primary_shard_size": "40gb",
                                         "max_age": "7d" } } },
  "warm":   { "min_age": "7d",  "actions": { "shrink": {"number_of_shards": 1},
                                             "forcemerge": {"max_num_segments": 1} } },
  "cold":   { "min_age": "30d", "actions": { "searchable_snapshot": {"snapshot_repository": "backups"} } },
  "delete": { "min_age": "90d", "actions": { "delete": {} } } } } }
```

- Roll on `max_primary_shard_size` (set from `target_shard_size_gb`, default 40), not on `max_docs` or a date alone. Size is what actually determines shard health; a daily index is 400 MB on a quiet week and 400 GB after a launch.
- `max_age` alongside size gives predictable retention boundaries on low-volume indices, and gives the delete phase something to work from.
- **`min_age` counts from index creation**, or from rollover for a rolled index — not from the phase before. A `warm` at 7d and a `cold` at 30d both measure from the same origin.
- ILM checks policies every `indices.lifecycle.poll_interval` (default 10m), so actions are not instant. `GET /<index>/_ilm/explain` says which phase, which step, and why it is stuck. `POST /<index>/_ilm/retry` after fixing the cause.
- Data streams (`elasticsearch >=7.9`) are the managed form: an append-only abstraction over hidden backing indices, requiring a `@timestamp` field. Writes go to the stream, reads span all backing indices, rollover is automatic. Updates and deletes by `_id` are not allowed — use `_update_by_query`.
- Deleting an index reclaims disk immediately; `_delete_by_query` writes tombstones and reclaims nothing until merges run. This is the whole reason time-based data is split into indices.

## Zero-Downtime Reindex

The procedure, in order. Skipping step 6 is how a reindex silently loses a day of writes.

1. **Create the destination** from a template with the corrected mapping, `refresh_interval: -1`, `number_of_replicas: 0`.
2. **Dual-write** if the source keeps receiving writes: the application writes to both the alias's current index and the new one, or an ingest pipeline fans out. If writes can pause, pausing is simpler and safer.
3. **Reindex** with `wait_for_completion=false` and `slices: auto`; throttle with `requests_per_second` if live traffic suffers.
4. **Catch up**: re-run the reindex filtered to `@timestamp` (or a sequence column) since the first run started, with `op_type: create` so nothing is rewritten.
5. **Restore settings** on the destination: `refresh_interval` back to its normal value, replicas back to `default_replicas`, then `POST /<dest>/_refresh`.
6. **Verify before swapping**: `_count` on both sides with the same query, `_count` per day for the last week, and a field-by-field diff on a random sample. A count match with a mapping mistake is still a broken index — check that the new field types actually query correctly.
7. **Swap the alias atomically** (single `_aliases` request).
8. **Keep the old index** for at least one full business cycle. Rolling back is one more atomic swap, and only if you did not delete it.

## Shrink, Split, and Clone

- `_shrink` reduces primary shards to a divisor of the original (5 → 1, 6 → 3 or 2). Requires the index read-only and every shard copy on **one** node. The standard warm-phase action after writes stop.
- `_split` multiplies primaries by a factor, requiring `index.number_of_routing_shards` set at creation. Setting it up front is the cheap insurance that makes a later growth mistake fixable without a full reindex.
- `_clone` copies an index with identical shard count — for a snapshot of state before a risky `_update_by_query`.
- All three are metadata-and-hardlink operations where possible, so they are far faster than a reindex. None of them can change a mapping.

## Force Merge

- `POST /<index>/_forcemerge?max_num_segments=1` on a **read-only** index: fewer segments means less per-segment overhead, better compression, and physically removed deleted documents.
- On an index still receiving writes it produces multi-GB segments that the normal merge policy will never select again, so deleted documents in them are never reclaimed. Only ever after writes stop.
- It is I/O-heavy and cannot be cancelled cleanly. Run it in the warm phase via ILM, or during a maintenance window.

## Lifecycle Gates

- Does every index either have a rollover policy or a bounded, known maximum size?
- Is every index that applications write to behind an alias?
- Does the ILM policy have a `delete` phase, or a written decision that it must not?
- Does rollover trigger on `max_primary_shard_size` derived from `target_shard_size_gb`?
- Is `index.number_of_routing_shards` set at creation so `_split` stays available?
- Was `GET /<index>/_ilm/explain` checked after the policy was attached, rather than assumed?
