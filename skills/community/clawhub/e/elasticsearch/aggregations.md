# Aggregations — Buckets, Metrics, and Where the Numbers Lie

Aggregations are fast because they are approximate in specific, documented ways. Knowing exactly which numbers are exact and which are estimates is the whole craft.

**Contents**: [The Three Families](#the-three-families) · [`terms`: the accuracy you did not know you were trading](#terms-the-accuracy-you-did-not-know-you-were-trading) · [`composite`: paginating buckets](#composite-paginating-buckets) · [`cardinality`: an estimate, always](#cardinality-an-estimate-always) · [`date_histogram`: intervals and time zones](#date_histogram-intervals-and-time-zones) · [`nested` and `reverse_nested`](#nested-and-reverse_nested) · [Metrics Worth Knowing](#metrics-worth-knowing) · [Pipeline Aggregations](#pipeline-aggregations) · [Performance and Limits](#performance-and-limits) · [Aggregation Gates](#aggregation-gates)

## The Three Families

- **Bucket** — group documents: `terms`, `date_histogram`, `histogram`, `range`, `filters`, `composite`, `nested`, `significant_terms`.
- **Metric** — compute over a bucket: `avg`, `sum`, `min`, `max`, `stats`, `cardinality`, `percentiles`, `top_hits`.
- **Pipeline** — compute over other aggregations' output: `derivative`, `moving_fn`, `cumulative_sum`, `bucket_selector`, `bucket_sort`, `sum_bucket`.

Always set `"size": 0` on an aggregation-only search. Returning 10 hits you throw away costs a fetch phase on every shard.

## `terms`: the accuracy you did not know you were trading

Each shard returns its own top `shard_size` buckets and the coordinator merges them. A term that ranks 11th on every shard but would be 3rd overall can be missed entirely.

- `size` default 10. `shard_size` default `size * 1.5 + 10`.
- `doc_count_error_upper_bound` in the response is the maximum a returned count could be undercounting. `sum_other_doc_count` is everything that fell outside the returned buckets. **Read both** — a non-zero error on a number going into a report is a correctness problem, not a rounding detail.
- To get exact counts: raise `shard_size` well above `size` (cost is memory on the coordinator), or reduce to a single shard, or use `composite`.
- Ordering by a **sub-aggregation** metric (`"order": {"avg_price": "desc"}`) makes the error unbounded and unreported: each shard picks its local top by that metric before the merge sees anything. Treat it as a hint, never as a ranking.
- `min_doc_count: 0` forces every term in the field to be returned, including ones matching no documents — an easy way to blow past `search.max_buckets` (default 65,536).

## `composite`: paginating buckets

The only bucket aggregation with a cursor.

```json
"aggs": { "by_day_and_host": { "composite": {
  "size": 1000,
  "sources": [ {"day": {"date_histogram": {"field":"@timestamp","calendar_interval":"day"}}},
               {"host": {"terms": {"field":"host.keyword"}}} ] } } }
```

- Response carries `after_key`; feed it back as `"after"` to get the next page. Counts are exact.
- Cannot be ordered by a sub-aggregation metric, and cannot be nested inside another bucket aggregation. That is the price of exactness.
- The right tool for exporting every bucket; the wrong tool for "top 10 by revenue".

## `cardinality`: an estimate, always

- HyperLogLog++. `precision_threshold` default 3,000, maximum 40,000: below the threshold counts are near-exact, above it error grows slowly (typically low single-digit percent).
- Memory cost is roughly `precision_threshold × 8` bytes **per bucket**. `precision_threshold: 40000` inside a 1,000-bucket terms agg is ~320 MB of heap for one request — a reliable way to trip the request circuit breaker.
- There is no exact distinct-count aggregation. If exact is required, `composite` over the field and count the pages, or maintain the count outside Elasticsearch.

## `date_histogram`: intervals and time zones

- `calendar_interval` (`1d`, `1M`, `1q`, `1y`) respects calendars: months of different lengths, DST-shortened days. `fixed_interval` (`24h`, `90m`) is a constant duration. They were split in `elasticsearch >=7.0` precisely because one `interval` parameter could not mean both.
- `calendar_interval` accepts only a value of 1 (`1d`, not `2d`); anything larger must be `fixed_interval`.
- `time_zone` shifts bucket boundaries so "daily" means the user's day. With `calendar_interval` this also handles DST, producing 23- and 25-hour days — correct, and a surprise for anyone dividing by 24.
- `min_doc_count: 0` plus `extended_bounds` fills empty buckets so a chart has no gaps. Without both, missing days simply do not appear and the line chart lies by omission.
- `offset: "+6h"` moves boundaries for business days that do not start at midnight.

## `nested` and `reverse_nested`

Aggregating inside a `nested` field requires entering and often leaving again:

```json
"aggs": { "items": { "nested": {"path": "line_items"},
  "aggs": { "by_sku": { "terms": {"field": "line_items.sku"},
    "aggs": { "back_to_order": { "reverse_nested": {},
      "aggs": { "orders": {"cardinality": {"field": "order_id"}} } } } } } } }
```

Without `reverse_nested`, `doc_count` counts hidden nested documents (line items), not parent documents (orders). This is the most-misread number in Elasticsearch reporting — a "1,200 orders" figure that is actually 1,200 line items.

## Metrics Worth Knowing

- `percentiles` uses TDigest: accurate at the extremes (p1, p99), less so in the middle, and error depends on `compression` (default 100). `percentile_ranks` answers the inverse question.
- `top_hits` inside a bucket returns example documents per group — the "best product per category" pattern. Expensive: it runs a mini fetch per bucket. `collapse` on the search is cheaper when you only need one level.
- `stats` and `extended_stats` return several metrics for one pass — cheaper than four separate aggregations over the same field.
- `filters` (plural) computes several named buckets from arbitrary queries in one pass, replacing N separate searches: `{"filters": {"filters": {"errors": {...}, "warnings": {...}}}}`.
- `significant_terms` finds terms unusually frequent in the result set versus the index background — genuine anomaly detection, not just counting. `significant_text` does the same on analyzed text, sampled.
- `missing` buckets documents where the field has no value, so a `terms` agg plus a `missing` agg accounts for 100% of the set.

## Pipeline Aggregations

- `derivative` on a `date_histogram` turns a running counter into a rate.
- `moving_fn` with `MovingFunctions.unweightedAvg(values)` smooths a noisy series; `window` is in buckets, not time.
- `bucket_selector` filters buckets by a metric after the fact (`params.total > 1000`) — the HAVING clause Elasticsearch otherwise lacks.
- `bucket_sort` sorts and paginates buckets already computed. It does **not** reduce work: every bucket is still built first, so it is presentation, not optimisation.
- `cumulative_sum` for running totals; `serial_diff` for period-over-period comparison.

## Performance and Limits

| Lever | Effect |
|---|---|
| `"size": 0` | Skips the fetch phase entirely |
| Move filters into `bool.filter` | Aggregations run on the filtered set; a cached filter shrinks the work at the source |
| `search.max_buckets` (default 65,536) | Total buckets per request; exceeding it throws `too_many_buckets_exception` |
| `execution_hint: "map"` on `terms` | Builds buckets from a hash map instead of global ordinals — faster on few unique values, worse on many |
| `?request_cache=true` | Aggregation-only requests (`size: 0`) are cached per shard until the next refresh; unrounded `now` in a filter defeats it |
| Sample first: `sampler` / `diversified_sampler` | Caps documents per shard before an expensive sub-aggregation |

Aggregations run on `doc_values`, not the inverted index, so they read columnar data straight from the OS page cache. That is why heap pressure and page-cache starvation hurt aggregations far more than they hurt term queries (SKILL.md Core Rules 5).

## Aggregation Gates

- Any `terms` output going into a report: is `doc_count_error_upper_bound` zero, and `sum_other_doc_count` accounted for?
- Any `cardinality` presented as a count: is it labelled as an estimate, and is `precision_threshold × buckets` within heap budget?
- Any `date_histogram` on a chart: `time_zone` set, `min_doc_count: 0` with `extended_bounds` so gaps show as zeros?
- Any aggregation inside `nested`: is the `doc_count` you are quoting parents or children?
- Any `terms` ordered by a sub-metric: is it labelled a hint rather than a ranking?
