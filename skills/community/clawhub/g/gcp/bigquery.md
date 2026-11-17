# BigQuery — Cost, Modeling, and Making Queries Cheap

BigQuery is why many teams are on GCP at all, and it is also the fastest way to spend four figures in an afternoon. The whole discipline is one sentence: **you pay for bytes scanned, not rows returned.**

**Contents:** [The Cost Model](#the-cost-model) · [Dry Run Before Every Run](#dry-run-before-every-run) · [Partitioning](#partitioning) · [Clustering](#clustering) · [Query Patterns That Cost Money](#query-patterns-that-cost-money) · [On-Demand vs Editions](#on-demand-vs-editions) · [Storage Billing](#storage-billing) · [Getting Data In](#getting-data-in) · [Modeling](#modeling) · [Governance and Guardrails](#governance-and-guardrails)

**Before estimating or optimizing a query**, read `## BigQuery` in `~/Clawic/data/gcp/memory.md` — or `datasets.md` if `## Boxes` points there. Partition columns, table sizes and the measured scan baselines are all there, and re-deriving them costs a scan.

## The Cost Model

Two independent meters, and people optimize the wrong one.

| Meter | Billed on | Typical share |
|---|---|---|
| **Compute** | On-demand: bytes scanned (~$6.25/TiB, with a monthly free allowance). Editions: slot-hours | Usually the majority, and the volatile part |
| **Storage** | GB-months, at an active rate that halves for partitions untouched for 90 days | Steady and small until data volume is large |

Facts that decide behaviour:

- Storage is **columnar**. Scanning a table reads only the columns the query names — which is why `SELECT *` on a 200-column table can cost 50× the same query naming four columns.
- **`LIMIT` does not reduce bytes scanned.** Neither does a `WHERE` on a non-partitioned, non-clustered column: the filter is applied after the data is read. This surprises everyone exactly once, usually expensively.
- Some operations are free: `SELECT` against metadata views (`INFORMATION_SCHEMA` in most cases), batch loads, exports, deletes of whole partitions, and cached query results. Cached results require a byte-identical query against unchanged tables — a query with `CURRENT_TIMESTAMP()` in it never caches.
- Queries are billed with a per-query minimum, so ten thousand tiny queries are not free either.

## Dry Run Before Every Run

A dry run returns the bytes the query will scan, costs nothing, and takes a second. Make it reflexive before any interactive query against a large table, and mandatory before anything scheduled.

- The dry-run estimate **ignores clustering**: actual bytes billed on a clustered table can be substantially lower than the estimate. It never goes the other way, so treat the estimate as a ceiling.
- Set **maximum bytes billed** on scheduled queries and on anything a human wrote today. The query fails instead of billing — which is the correct outcome for a mistake.
- Set a **custom quota** on query bytes per project per day. It is the only hard stop BigQuery offers, and it is the reason a runaway dashboard costs a hundred dollars instead of five thousand (`costs.md`).
- Record the measured dry-run size of the queries that run often in `## BigQuery` (or `datasets.md`) as a scan baseline with its date. A baseline is what turns "BigQuery got expensive" into a number in one read.

## Partitioning

The primary cost control. A query with a filter on the partition column reads only the matching partitions.

- **Partition by ingestion time, a date/timestamp column, or an integer range.** A date column that matches how people filter beats ingestion time, because ingestion time is not what analysts put in the `WHERE` clause.
- **Turn on `require_partition_filter`.** It makes an unfiltered query fail instead of scanning the whole table. On any table above a few hundred gigabytes this is not optional — it is the difference between a mistake costing nothing and costing a day's budget.
- **Pruning needs a filter the planner can resolve statically.** A literal or a simple expression prunes; a filter comparing the partition column to a subquery result, or wrapping it in a function, may not. When a dry run comes back at full table size despite a date filter, this is why — materialize the boundary into a literal or a scalar subquery the planner can evaluate.
- Partition limits are per table and generous, but daily partitions over many years plus a per-partition minimum size can make many tiny partitions inefficient. Monthly partitions suit slow-growing history.
- **Partition expiration** deletes old partitions automatically and is the cheapest retention policy that exists.

## Clustering

Sorts data within each partition by up to four columns, so filters and aggregations on those columns read fewer blocks.

- **Order matters and is prefix-based**: clustering by `(a, b, c)` helps a filter on `a`, on `a AND b`, and on `a AND b AND c` — not a filter on `b` alone. Put the most-filtered, highest-cardinality-that-people-actually-filter-on column first.
- Clustering is free, requires no maintenance, and BigQuery re-clusters in the background.
- It pairs with partitioning rather than replacing it: partition by time, cluster by the identifier people filter by.
- Because the savings do not show in a dry run, measure clustering's effect from actual bytes billed in `INFORMATION_SCHEMA.JOBS`, not from the estimate.

## Query Patterns That Cost Money

| Pattern | Why it costs | Do instead |
|---|---|---|
| `SELECT *` | Reads every column in the scanned partitions | Name the columns; `SELECT * EXCEPT(big_blob)` where the list is long |
| Filter on a non-partition column to "limit" the scan | The filter runs after the read | Filter the partition column too, even when redundant |
| `SELECT * FROM t ORDER BY x LIMIT 10` on a huge table | Full scan, then sort | Filter the partition first; use approximate functions where exactness is not required |
| Repeating an expensive subquery in several CTE branches | Each reference can re-read | Materialize once into a temp table, or a materialized view |
| Joining a huge fact table to another huge fact table | Shuffle cost, and both scanned in full | Filter both sides to their partitions before joining; denormalize the common path |
| `COUNT(DISTINCT x)` over billions of rows | Exact distinct is expensive | `APPROX_COUNT_DISTINCT` where a fraction of a percent of error is acceptable |
| A dashboard refreshing hourly against the raw table | The same scan, every hour, forever | Materialized view, or a scheduled aggregate into a small table the dashboard reads |
| Querying an external table on Cloud Storage repeatedly | No BigQuery storage optimizations; files are read whole | Load it in, or use BigLake with the appropriate metadata caching |
| `INFORMATION_SCHEMA.JOBS` scanned without a time filter | It is a table like any other | Always bound it by `creation_time` |

The single highest-leverage optimization in most accounts: find the top three queries by bytes billed in `INFORMATION_SCHEMA.JOBS_BY_PROJECT` over the last 30 days. They are almost always one dashboard or one scheduled query, and fixing that one item is most of the saving.

## On-Demand vs Editions

`bq_billing_model` decides which advice applies.

- **On-demand** — pay per byte scanned, with a large but shared slot pool. Rewards sparse, unpredictable querying. Punishes a heavy scheduled workload, and gives no capacity guarantee: a busy neighbour can slow your query without changing your bill.
- **Editions (Standard / Enterprise / Enterprise Plus)** — pay for slot-hours with autoscaling and an optional baseline. Rewards steady load. Punishes idle baseline slots. Higher editions add features (materialized-view refresh behaviours, cross-region replication, CMEK) as much as performance.
- **The break-even is arithmetic, not preference**: convert a representative month's on-demand bytes-billed into cost, then price the slot capacity that would serve the same workload at acceptable concurrency. Reservations with autoscaling and a low baseline are the usual first move, because they cap the downside without paying for idle capacity.
- Commitments (1-year, 3-year) discount slots further and should follow the same rule as any commitment: only after the workload is stable and right-sized (`costs.md`).
- Reservations are assigned to projects or folders, so a mixed estate can keep ad-hoc analysis on-demand while production pipelines run on committed slots. That split is usually the cheapest configuration and almost nobody sets it up.

## Storage Billing

- **Active vs long-term**: a table partition not modified for 90 consecutive days drops to roughly half price automatically. Reading it does not reset the clock; **writing to it does**. A nightly job that rewrites history keeps the whole table at the active rate forever.
- **Logical vs physical billing** is a per-dataset choice: logical bills uncompressed bytes, physical bills compressed bytes plus time travel and fail-safe storage. Well-compressing data (repetitive strings, sparse columns) is usually much cheaper on physical. Compare the two figures in `INFORMATION_SCHEMA.TABLE_STORAGE` before switching; the switch has a cooling-off period.
- **Time travel** (default 7 days, configurable down to 2) and fail-safe storage are billed under physical billing. Reducing the time-travel window on a large, churning table is a real saving — and a real reduction in your ability to undo a mistake.
- Deleting rows costs a write; dropping a partition costs nothing. Design retention around partitions.

## Getting Data In

| Path | Cost | Use |
|---|---|---|
| Batch load from Cloud Storage | Free | The default. Anything that can wait minutes |
| Storage Write API | Per GB, with a monthly free allowance | Streaming with exactly-once semantics; the modern streaming path |
| Legacy streaming inserts | Materially more per GB than the Write API | Migrate off it; it exists for compatibility |
| Datastream (CDC) | Per GB processed | Continuous replication from a database (`pipelines.md`) |
| Data Transfer Service | Varies by source | Scheduled loads from SaaS sources and other clouds |
| External / BigLake tables | Query-time only | Data that lives in Cloud Storage and is queried rarely |
| `LOAD DATA` / federated queries | Query-time | One-off analysis without a load step |

The rule: if it can be a batch load, make it a batch load — the ingest is free and the resulting table is fully optimized. Streaming is for data that is worthless when it is ten minutes old, and it should be justified by that, not by convenience.

## Modeling

- **Denormalize by default.** BigQuery joins are fine but scanning one wide table beats scanning two and shuffling. Nested and repeated fields (`STRUCT`, `ARRAY`) let you denormalize without exploding row counts, and `UNNEST` at query time reads only the columns touched.
- **Small dimension tables can stay separate** — a broadcast join against a small table is cheap and keeps the model comprehensible.
- **Views cost what they scan** every time they are queried; they save nothing. **Materialized views** store the result and refresh incrementally, and BigQuery will silently rewrite a query to use one — that automatic rewrite is the feature.
- **Table snapshots and clones**: a clone is a cheap writable copy billed only on divergence, which makes a full-size test environment nearly free. A snapshot is a cheap point-in-time restore point. Both are underused.
- **Dataset location is permanent.** You cannot move a dataset between regions; you copy it. Choose the location against residency requirements and against where the data will be joined, because cross-region joins are not possible without copying (`organization.md`).

## Governance and Guardrails

- Access at dataset, table, column and row level. **Column-level** access uses policy tags from Data Catalog; **row-level** uses row access policies. Both are enforced at query time, so a masked column costs nothing extra to protect.
- Authorized views and authorized datasets let a consumer query a curated view without any access to the underlying tables — the correct way to share with another team.
- **Data Access audit logs are on and free for BigQuery**, which makes "who queried this table" answerable without enabling anything. That is not true for most other services (`security.md`).
- Guardrails to put in place before handing a dataset to a team: `require_partition_filter` on the large tables, maximum bytes billed on scheduled queries, a project-level daily query quota, and partition expiration matching the retention policy.
- CMEK at dataset creation if the compliance regime requires it — a decision that cannot be retrofitted to existing tables without a rewrite.

Whenever a dataset is created, a table is partitioned or clustered, or a scan baseline is measured, write the row into `## BigQuery` in `~/Clawic/data/gcp/memory.md` (dataset, location, partition column, cluster columns, size, typical scan). A query that took real work to bring down goes to `~/Clawic/data/gcp/artifacts/query-<name>.md` with the before and after bytes and why it works, plus its `## Boxes` line (`memory-template.md`).
