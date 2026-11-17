# Mapping — Field Types and the Decisions You Cannot Undo

A mapping is a contract you sign once. Adding a field is free; changing one is a reindex (SKILL.md Core Rules 3). Everything below is about getting it right the first time and about the field types most teams never learn exist.

**Contents**: [Choosing the Type](#choosing-the-type) · [Multi-Fields](#multi-fields) · [Dynamic Mapping and Field Explosion](#dynamic-mapping-and-field-explosion) · [Dynamic Templates](#dynamic-templates) · [Runtime Fields](#runtime-fields) · [`_source` and Stored Fields](#_source-and-stored-fields) · [Settings You Set at Creation](#settings-you-set-at-creation) · [Verifying a Mapping](#verifying-a-mapping)

## Choosing the Type

| Data | Type | Why not the obvious alternative |
|---|---|---|
| Prose a human searches | `text` | Cannot be sorted or aggregated at all |
| IDs, SKUs, enums, tags, emails | `keyword` | `text` destroys them: `USER-42` becomes `[user, 42]` |
| Both of the above on one field | multi-field `text` + `fields.keyword` | The default for titles, names, product descriptions |
| Log message you grep but never phrase-search | `match_only_text` (`elasticsearch >=7.14`) | Drops positions and norms — noticeably smaller index, constant score |
| A value you only filter on, never search | `keyword` with `index: true, doc_values: true` | Fine as is; drop `norms` — they are already off for keyword |
| A value you only aggregate on | `index: false, doc_values: true` | Skips the inverted index entirely |
| Numbers you range-query | `long` / `double` / `scaled_float` | `scaled_float` with `scaling_factor: 100` stores money as an integer and stays exact |
| Numbers you only look up exactly (IDs, ports, status codes) | `keyword` | Numeric types optimise for ranges; term lookups on `keyword` are faster |
| IP addresses | `ip` | Supports CIDR range queries; a `keyword` cannot |
| Timestamps | `date` with an explicit `format` | Dynamic mapping guesses one format and rejects the next shape it sees |
| One value repeated across a whole index | `constant_keyword` (`elasticsearch >=7.7`) | Stored once in metadata; also lets the coordinator skip whole indices |
| High-cardinality strings you grep with wildcards | `wildcard` (`elasticsearch >=7.9`) | Built for leading wildcards; a `keyword` scans every term |
| Arbitrary, unpredictable key sets | `flattened` (`elasticsearch >=7.3`) | Whole object becomes one field — no mapping explosion, but no analysis and no numeric ranges |
| Objects whose fields must stay associated | `nested` | Each sub-object becomes a hidden Lucene document; a 20-item array indexes as 21 documents |
| Embeddings | `dense_vector` | `index: true` builds the HNSW graph for `knn`; `index: false` leaves only brute-force `script_score` |
| Coordinates and areas | `geo_point` / `geo_shape` | A point costs about two numeric fields; a shape is far heavier to index and query |

## Multi-Fields

```json
{ "title": { "type": "text", "analyzer": "english",
    "fields": { "raw": { "type": "keyword", "ignore_above": 256 },
                "ac":  { "type": "text", "analyzer": "autocomplete_index",
                         "search_analyzer": "standard" } } } }
```

- One source value, several indexed representations. Search `title`, sort and aggregate `title.raw`, autocomplete on `title.ac`.
- `ignore_above: 256` is what dynamic mapping applies by default: values longer than that are stored in `_source` but **not indexed**, so they silently vanish from term queries and aggregations. Raise it deliberately for long identifiers.
- The hard ceiling underneath it is Lucene's: a single keyword term above 32,766 bytes fails the whole document with `max_bytes_length_exceeded`. Hash or truncate long values before indexing.
- Adding a new sub-field to an existing multi-field is legal, but only new documents get it — existing documents need `_update_by_query` to re-index in place.

## Dynamic Mapping and Field Explosion

- `dynamic` has four values: `true` (add the field), `runtime` (add it as a runtime field, `elasticsearch >=7.11`), `false` (store in `_source`, do not index — invisible to search, no error), `strict` (reject the document with `strict_dynamic_mapping_exception`).
- `false` is the trap: the document indexes fine, the field is in `_source`, and every query on it returns nothing. Prefer `strict` anywhere a producer might typo a field name.
- `index.mapping.total_fields.limit` defaults to 1000, counting every leaf and every multi-field sub-field. Hitting it stops indexing for the whole index. Raising it is a stay of execution: 10,000 mapped fields is heap in the cluster state on every node.
- The usual cause is user-controlled JSON keys (`attributes.<anything>`). Fix with `flattened`, not with a bigger limit.
- `subobjects: false` (`elasticsearch >=8.3`) lets `a.b.c` stay a flat field name instead of implying nested objects — the clean answer for ECS-style dotted keys.

## Dynamic Templates

Set the rule once instead of mapping 400 fields:

```json
"dynamic_templates": [
  { "ids_as_keyword":   { "match": "*_id",   "mapping": { "type": "keyword" } } },
  { "strings_default":  { "match_mapping_type": "string",
      "mapping": { "type": "keyword", "ignore_above": 256 } } }
]
```

- Templates are evaluated in array order, first match wins — put the specific patterns above the catch-all.
- The default dynamic behaviour for strings is `text` + `keyword` sub-field, which doubles the index for fields nobody full-text searches. Overriding it to plain `keyword` is the single biggest index-size win in log-shaped data.
- Templates apply to fields added later; they never retro-map existing fields.

## Runtime Fields

`elasticsearch >=7.11`. A field computed from `_source` or `doc_values` at query time.

- The escape hatch when the mapping is wrong and a reindex is not scheduled yet: define it on the index or per search, query it immediately, no data movement.
- Cost is paid per document scanned, per query — fine for a filter that runs after other filters have narrowed the set, terrible as the primary selective clause on a large index.
- Promotion path: prove the field with a runtime definition, then bake it into the mapping at the next reindex. Same name, same output, queries do not change.
- `"dynamic": "runtime"` makes newly-seen fields queryable without adding them to the mapping — the middle ground between `strict` and field explosion.

## `_source` and Stored Fields

- `_source` is the original JSON. Disabling it makes `_reindex`, `_update`, `_update_by_query`, highlighting, and the Explain API impossible. Almost never worth it; use `_source.excludes` for the one giant field instead.
- Excluding a field from `_source` means it is still searchable but cannot be returned or reindexed — a one-way door for that field.
- `"_source": ["title", "price"]` on the request (source filtering) cuts network and JSON-parsing cost without changing storage. That is what you usually want when someone proposes disabling `_source`.
- `store: true` on a field is only useful when `_source` is disabled or the field is huge and rarely fetched.

## Settings You Set at Creation

| Setting | Default | Change it when |
|---|---|---|
| `number_of_shards` | 1 | Always compute it (SKILL.md Shard and Heap Arithmetic) |
| `number_of_replicas` | 1 | `default_replicas` variable; 0 on single-node dev |
| `refresh_interval` | 1s | 30s for logs (fewer segments), `-1` during a bulk load |
| `index.codec` | LZ4 | `best_compression` on cold or archival data: smaller on disk, slower to read |
| `index.mapping.total_fields.limit` | 1000 | Only with a written reason; fix the producer first |
| `index.sort.field` | none | Index sorting speeds up early-terminating queries on that sort, at index-time cost |
| `dynamic` | true | `strict` for anything user-facing |

`refresh_interval` and `number_of_replicas` are dynamic (change any time). Shard count, `index.sort`, and `codec` are creation-only — another reason every index is born from a template.

## Verifying a Mapping

```
GET /<index>/_mapping                       # what is actually mapped
GET /<index>/_field_caps?fields=*           # types across an alias or wildcard — spots divergence
GET /<index>/_mapping/field/price           # one field, fast
POST /<index>/_analyze {"field":"title","text":"..."}   # what a value becomes
```

`_field_caps` is the one to run before querying an alias that spans many indices: the same field mapped as `long` in one index and `keyword` in another makes sorts and aggregations fail across the alias, and nothing warns you at write time.
