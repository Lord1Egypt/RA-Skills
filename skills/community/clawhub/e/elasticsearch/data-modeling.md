# Data Modeling — Relations, Tenancy, and How Many Indices

Elasticsearch has no joins at query time worth the name. Every relational instinct has to be resolved at index design time, and the four available answers have very different costs.

## The Four Ways to Model a Relation

| Approach | Cost | Use when |
|---|---|---|
| Denormalize (copy parent fields into the child document) | Storage, and an update fan-out when the parent changes | Parent changes rarely, children are queried alone. The default |
| `nested` | Each sub-object is a hidden Lucene document: index, delete, and merge cost multiply | You query two sub-fields of the same item together |
| `join` field (parent-child) | Query-time join within a shard; roughly 5-10× slower than nested on reads | Children update far more often than parents, and re-denormalizing would rewrite huge documents |
| Application-side join (two queries) | A network round trip, and no combined scoring | The "many" side is unbounded, or the join is rare enough not to shape the index |

Decision order: denormalize → nested → join field → app-side. Each step down is a real cost; take it only when the step above provably cannot answer the query.

## Objects vs Nested (the correctness bug)

```json
{ "user": [ { "first": "Alice", "last": "Smith" },
            { "first": "Bob",   "last": "Jones" } ] }
```

With the default `object` type this flattens to `user.first: [alice, bob]`, `user.last: [smith, jones]`. A query for `first=Alice AND last=Jones` **matches**, because the association is gone. It returns HTTP 200 with a wrong answer, which is worse than an error.

- `"type": "nested"` indexes each object as its own hidden document, restoring the boundary. Queries must be wrapped: `{"nested": {"path": "user", "query": {...}}}`.
- Sub-hits come back only if you ask: `"inner_hits": {}` inside the nested query tells you *which* item matched, which is what the UI usually needs.
- Aggregating inside a nested path needs a `nested` agg, and getting back out to parent fields needs `reverse_nested`.
- Updating one nested item rewrites the entire parent document and all its hidden children. High-churn sub-objects are the case for a `join` field instead.
- Limits: `index.mapping.nested_fields.limit` 50 distinct nested fields per index, `index.mapping.nested_objects.limit` 10,000 nested documents per parent document. A document that exceeds the second is rejected outright.

## The `join` Field

```json
"relation": { "type": "join", "relations": { "product": "review" } }
```

- Parent and child must live on the same shard: children are indexed with `?routing=<parent_id>`, and forgetting the routing parameter silently breaks the relation.
- Queries: `has_child`, `has_parent`, `parent_id`. Scoring across the join needs `score_mode` set explicitly (`none` by default on `has_child`).
- One join field per index, and hierarchies deeper than two levels multiply the cost fast.
- The honest trade: parent-child buys cheap child updates and pays on every read. If reads outnumber writes — the normal case for search — denormalize instead.

## Multi-Tenancy

| Tenants | Layout | Why |
|---|---|---|
| A handful, very different schemas | One index per tenant | Isolation, independent mappings and ILM |
| Hundreds to millions, same schema | One shared index + mandatory `tenant_id` filter | Index-per-tenant hits `cluster.max_shards_per_node` (1000) long before disk fills |
| Shared index, a few very large tenants | Shared index + custom routing per tenant | Confines a tenant's queries to one shard |
| Mixed sizes | Shared index for the long tail, dedicated indices for the whales, one alias over both | Keeps the shard budget sane without penalising big tenants |

- Custom routing (`?routing=<tenant_id>`) turns a fan-out over N shards into a single-shard query — a large latency win. The price is skew: one huge tenant lands entirely on one shard and unbalances the cluster. Mitigate with `index.routing_partition_size`, which spreads a routing value across a subset of shards.
- The tenant filter must be enforced somewhere that application code cannot forget: a filtered alias, or document-level security if the license allows it. A `tenant_id` clause that lives only in application code is a data-leak waiting for a refactor.

## One Index or Many

- **Time-based data** (logs, metrics, events, orders you only query by recent window): many indices, created by rollover, deleted whole. Deleting an index reclaims disk instantly; `_delete_by_query` only writes tombstones.
- **Entity data** (products, users, documents): one index, reindexed when the mapping changes. Splitting entities across indices by category just moves the filter from a clause to an index pattern and costs you cross-index scoring consistency.
- **Different retention or different hardware tier** is a legitimate reason to split; "these documents feel different" is not.
- Divergent mappings across an alias break sorts and aggregations at query time. Check with `GET /<pattern>/_field_caps?fields=*` before pointing an alias at a set of indices.

## Document Granularity

The unit you index should be the unit you want back in `hits`.

- Searching a book but wanting the chapter? Index chapters, with book metadata denormalized onto each.
- Searching orders but showing line items? Index line items, or index orders with `nested` line items and use `inner_hits`.
- Documents above a few hundred KB slow down `_source` fetching, highlighting, and every update. Split them, or exclude the giant field from `_source`.

## Immutable-Document Patterns

- Append-only event data makes updates disappear as a problem: no version conflicts, no merge churn from tombstones, and ILM can age whole indices.
- When state changes must be represented, index the state transition as a new document and resolve to current state with a `collapse` on the entity ID sorted by timestamp — cheaper than updating in place at high write rates.
- The counterweight: "current state" queries get more expensive and aggregations need care to avoid double-counting. Choose per workload, not per taste.

## Modeling Gates

- Does any query filter on two sub-fields of the same array item? If yes and the field is an `object`, the results are already wrong.
- Is every tenant-scoped query filtered somewhere the application cannot bypass?
- Does the document granularity match what the UI displays?
- Is the parent-update fan-out bounded? A denormalized field on 10M children means a 10M-document `_update_by_query` every time it changes.
- Will this index grow forever? If yes, it needs rollover now, not after it is 2 TB.
