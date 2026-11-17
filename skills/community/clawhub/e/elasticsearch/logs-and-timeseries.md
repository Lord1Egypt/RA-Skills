# Logs and Time-Series — Observability Workloads

Log and metric data breaks the assumptions of entity search: writes dominate reads, documents are never updated, cardinality is unpredictable, and volume is bounded only by retention. The design consequences are large enough that this is effectively a different product.

## The Shape

- **Append-only.** No updates, no deletes by ID. That removes version conflicts, tombstones, and most merge pressure.
- **Delete by index, never by query.** Dropping an index reclaims disk instantly; `_delete_by_query` over 500M documents writes 500M tombstones and reclaims nothing until merges run.
- **Recent data is hot, old data is cold.** Almost every query has a time filter, so tiering by age matches the access pattern exactly.
- **Schema is semi-known.** Some fields are fixed (`@timestamp`, `host`, `service`), some arrive from applications nobody controls — which is where mapping explosion comes from.

## Data Streams

`elasticsearch >=7.9`. The managed form: a name you write to, hidden backing indices underneath, automatic rollover, ILM attached.

```json
PUT /_index_template/logs-app
{ "index_patterns": ["logs-app-*"], "data_stream": {}, "priority": 200,
  "composed_of": ["logs-mappings", "logs-settings"] }
POST /logs-app-prod/_doc      { "@timestamp": "2026-07-26T10:00:00Z", "message": "..." }
```

- Requires a `@timestamp` field mapped as `date` or `date_nanos`.
- Writes go to the stream; reads span every backing index. Rollover is automatic through ILM.
- Updates and deletes by `_id` are rejected. `_update_by_query` and `_delete_by_query` work, for the GDPR case.
- Backing indices are named `.ds-<stream>-<date>-<gen>` and are hidden. Address the stream, never the backing index, except when debugging allocation.
- The alternative — hand-rolled `logs-2026.07.26` daily indices — produces 400 MB indices on quiet days and 400 GB on busy ones, which is the shard-sizing problem in its purest form. Roll on size.

## Mapping for Volume

The default dynamic mapping is wrong for logs in a specific, expensive way: it maps every string as `text` **plus** a `keyword` sub-field, roughly doubling the index for fields nobody full-text searches.

```json
"dynamic_templates": [
  { "message_field": { "path_match": "message", "mapping": { "type": "match_only_text" } } },
  { "strings_as_keyword": { "match_mapping_type": "string",
      "mapping": { "type": "keyword", "ignore_above": 1024 } } } ]
```

- `match_only_text` (`elasticsearch >=7.14`) drops positions and norms: noticeably smaller than `text`, constant scoring, phrase queries still work by consulting `_source` (slower). For log messages you grep rather than rank, this is the right type.
- Everything else as `keyword`: filterable, aggregatable, sortable, and half the size of the `text`+`keyword` pair.
- `index: false, doc_values: true` for fields you only ever chart and never filter on.
- `index.codec: best_compression` on the warm phase and below: smaller on disk, slower to decompress, and old data is queried rarely by definition.
- `subobjects: false` (`elasticsearch >=8.3`) keeps ECS-style dotted names flat instead of building deep object trees.
- Guard the field count: application-supplied structured logging fields are the classic route to the 1,000-field limit. `flattened` for the free-form bag, `dynamic: strict` for the parts you own.

## ECS and Field Naming

- Elastic Common Schema fixes names (`host.name`, `service.name`, `event.dataset`, `log.level`, `@timestamp`) so dashboards and detection rules work across sources.
- The value is not the schema itself; it is that every source agrees. A house schema applied consistently beats ECS applied to half the pipelines.
- Normalise at ingest, at the edge: an ingest pipeline or the collector renames fields once, rather than every query handling three spellings of the same thing.
- Keep the raw line. `event.original` costs storage and settles every "the parser ate it" argument in seconds.

## Time-Series Data Streams and Downsampling

- **TSDS** (`elasticsearch >=8.7`) is a data stream in time-series mode: documents are sorted by dimension and timestamp, which compresses metrics dramatically compared to a general index. Requires declaring `time_series_dimension` and `time_series_metric` on fields, and the index becomes append-only within a time bound.
- **Downsampling** replaces raw documents with statistical aggregates at a coarser interval (raw → 5m → 1h) as data ages. A year of 10-second metrics at full resolution is a storage bill nobody wanted; nobody queries it at that resolution either.
- Attach downsampling as an ILM action in the warm or cold phase, so it is automatic rather than a project.
- Metrics with unbounded label cardinality (a `user_id` dimension, a request ID) defeat both. Cardinality control is the whole discipline of metrics storage.

## Tiering

| Tier | Hardware | Typical age | Configuration |
|---|---|---|---|
| hot | NVMe, high CPU | 0-7d | Receives writes, `refresh_interval: 30s`, replicas per `default_replicas` |
| warm | Cheaper disk | 7-30d | Read-only, shrunk to one shard, force-merged, `best_compression` |
| cold | Cheap disk or object storage | 30-90d | Fully-mounted searchable snapshot; replicas unnecessary (licensed) |
| frozen | Object storage + local cache | 90d+ | Partially-mounted snapshot; seconds-to-first-byte (licensed) |
| delete | — | Per retention policy | The phase most policies forget to include |

Without a license for searchable snapshots, the open-tier version is: hot and warm on data nodes, then snapshot and delete, restoring on demand for the rare old query. Slower to access, and the retention math is identical.

## Query Patterns

- Always filter on `@timestamp` first, rounded (`now-24h/h`) so the request cache can hold the result. An unrounded `now` makes every dashboard refresh a cache miss.
- Index-level date filtering: with data streams, a time filter lets the coordinator skip whole backing indices via `constant_keyword` and index metadata — one of the largest wins available, and free.
- Dashboards are aggregation-only: `"size": 0` and `?request_cache=true`.
- `date_histogram` needs `time_zone`, `min_doc_count: 0`, and `extended_bounds`, or the chart silently omits quiet periods.
- Long analytical queries over months of data: `async_search`, so the dashboard is not holding a connection open.
- `refresh_interval: 30s` on the hot tier: log search almost never needs one-second freshness, and it cuts segment creation thirtyfold.

## Retention and Cost

Sizing formula: `daily_gb × retention_days × (1 + replicas) × 1.3` for the headroom the watermarks demand.

Levers in order of effect:

1. **Drop fields at ingest.** The cheapest byte is the one never indexed. Most log pipelines carry fields nobody has ever queried.
2. **Shorter hot retention, longer cold.** Query patterns collapse after a few days; storage class should follow.
3. **`keyword` instead of `text`+`keyword`** on everything not full-text searched.
4. **Downsample metrics** rather than keeping raw resolution.
5. **`best_compression`** below the hot tier.
6. **Sampling** for high-volume, low-value events (debug logs, health-check access lines) — a 1-in-100 sample keeps the distribution and drops 99% of the cost.

Deleting an index is the only operation that returns disk immediately. Every retention design should end in a `delete` phase, and the absence of one is the root cause of most disk incidents.
