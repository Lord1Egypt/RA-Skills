# ES|QL — Piped Query Language for Analytics and Investigation

ES|QL is a second query surface, not a syntax skin over the DSL: a separate compute engine reached at `POST /_query`. Technical preview on `elasticsearch >=8.11`, GA on `elasticsearch >=8.14`. It returns **columns and rows**, never `_source` documents and never a relevance ranking.

## Choose ES|QL Or The Query DSL

| Job | Surface | Why |
|---|---|---|
| Ad-hoc investigation, "slice this by X and show me the top Y" | ES\|QL | One pipe expresses filter → derive → group → sort; the DSL needs a nested aggregation tree |
| Anything the user ranks by relevance | Query DSL | ES\|QL rows come back unscored; BM25 ranking, boosting, and `_rank_eval` live in the DSL |
| Parse an unstructured field at query time | ES\|QL | `GROK` / `DISSECT` inline, no ingest pipeline and no reindex |
| Join a lookup table onto results | ES\|QL | `ENRICH` (and `LOOKUP JOIN` on 9.x); the DSL has no join |
| Feed an application's search results page | Query DSL | Highlighting, suggesters, `collapse`, `inner_hits`, pagination beyond a row cap |
| kNN / hybrid semantic retrieval | Query DSL | Vector retrieval and RRF belong to the DSL surface |
| Data touching `nested` fields | Query DSL | ES\|QL cannot read `nested` sub-documents at all |
| Anything else | Query DSL | It is the surface every client, tool, and version supports |

## Shape Of A Query

```
POST /_query
{"query": """
FROM logs-app-*
| WHERE @timestamp >= NOW() - 24 hours AND http.status >= 500
| EVAL route = CASE(url LIKE "/api/*", "api", "web")
| STATS errors = COUNT(*), p95 = PERCENTILE(duration_ms, 95) BY route, bucket = BUCKET(@timestamp, 1 hour)
| SORT errors DESC
| LIMIT 50
""",
 "params": [],
 "filter": {"range": {"@timestamp": {"gte": "now-24h"}}}}
```

- One **source command** first (`FROM`, `ROW`, `SHOW INFO`), then processing commands separated by `|`. Order is execution order.
- Core processing commands: `WHERE` · `EVAL` (new column) · `STATS ... BY` (aggregate) · `SORT` · `LIMIT` · `KEEP` / `DROP` / `RENAME` (column projection) · `DISSECT` / `GROK` (parse a string column) · `ENRICH` · `MV_EXPAND` (one row per multivalue).
- `params` is the injection-safe way to interpolate user input — `WHERE user == ?` — exactly as with prepared statements. String-concatenating into the query text is the ES|QL form of the `query_string` injection bug.
- The top-level `filter` key takes an ordinary DSL query and is applied before the pipeline. Use it for the time range: it is the cheapest possible pushdown.
- `format` (`txt`, `csv`, `tsv`, `json`, `arrow`) and `columnar: true` change the response shape. `txt` is for humans; never parse it.

## The Row Cap Everyone Hits

- **No `LIMIT` means an implicit `LIMIT 1000`.** Results silently stop at a thousand rows; nothing in the response says "truncated" as loudly as it should.
- The hard ceiling is `esql.query.result_truncation_max_size` (default 10,000). A `LIMIT` above it is capped, not honoured.
- Consequence: ES|QL is a **result-set** language, not an export tool. Aggregate down to rows you will actually read, or export with a PIT scan or `_reindex` from the DSL side.
- There is no `search_after` for ES|QL. Paginating means re-running with a narrower `WHERE`, which is why time-bucketed investigation works and offset paging does not.

## Pushdown: Where The Time Goes

- `WHERE` on an indexed field, placed **before** any `EVAL` that touches it, is pushed down to Lucene and skips documents at the segment level. The same `WHERE` after an `EVAL` on that field forces a scan.
- Rule: filter on raw fields first, derive second. `FROM x | WHERE status == 500 | EVAL bucket = ...` beats `FROM x | EVAL bucket = ... | WHERE status == 500` by orders of magnitude on a large index.
- `KEEP` early. Every column carried through the pipeline is fetched and materialised, and `_source`-only fields (no doc values) are the expensive ones.
- `STATS ... BY` needs doc values on the grouping field: group on `.keyword`, never on the analyzed `text` field, the same rule as `terms` aggregations.
- Long analytics run async: `POST /_query/async` with `wait_for_completion_timeout` and `keep_alive`, then poll `GET /_query/async/<id>`. Same discipline as any long task — a client timeout does not stop the compute.

## Multivalue Fields Are First-Class And Will Surprise You

- Elasticsearch fields are implicitly arrays, and ES|QL surfaces that: a field with three values returns as a three-element multivalue in one cell.
- **Most scalar functions and comparisons return `null` on a multivalued input** rather than erroring or picking one. A `WHERE tags == "sale"` that returns nothing on documents that clearly have the tag is this, every time.
- Fixes, in order of preference: `MV_MIN` / `MV_MAX` / `MV_COUNT` / `MV_DEDUPE` to collapse to a scalar, `MV_EXPAND` to fan out into one row per value (multiplies row count, counts against `LIMIT`), or `MV_EXPAND tags | WHERE tags == "sale"`, which is the membership test that works on every version.
- Multivalues are returned unordered in the general case — do not read positional meaning into them.

## Accuracy And Type Rules

- `COUNT_DISTINCT` is HyperLogLog++: approximate, with the same precision/memory trade as the `cardinality` aggregation. `MEDIAN` and `PERCENTILE` are TDigest: approximate, and less accurate the further into the tail you go.
- `VALUES` collects every distinct value into a multivalue cell — unbounded, and a reliable way to blow the request circuit breaker on a high-cardinality field. `TOP(field, n, "desc")` is the bounded form.
- Types are strict. `"5" + 1` does not coerce; cast with `::integer` or `TO_INTEGER()`. A mixed-type field across indices behind a wildcard (`long` in one, `keyword` in another) makes the column unusable — the same divergent-mapping problem `_field_caps` diagnoses on the DSL side.
- `null` propagates through arithmetic; use `COALESCE()` before it reaches a `STATS`.

## Operational Notes

- Availability tracks the version closely: cross-cluster ES|QL, full-text functions (`MATCH`, `QSTR`), spatial functions, and `LOOKUP JOIN` each landed in different releases. Before writing a query against an unknown cluster, `GET /` for the version, and treat anything past the basic pipeline as version-gated.
- ES|QL is the query language behind Kibana Discover's ES|QL mode and several alerting rule types, so a query written here is portable to a saved dashboard — which is the usual reason to prefer it for investigation work.
- Security applies normally: field- and document-level security, index privileges, and `search.allow_expensive_queries` all still gate what the pipeline can read. ES|QL is not a way around a role.
- OpenSearch does not have ES|QL. On an OpenSearch deployment the closest surfaces are its own PPL and SQL plugins, with different syntax and different function coverage — see the migration notes in the upgrades guide.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Omitting `LIMIT` and trusting the row count | Implicit `LIMIT 1000` truncates silently | State `LIMIT` explicitly, always |
| Using ES\|QL for a search results page | No scoring, no highlighting, no deep paging | Query DSL for user-facing retrieval |
| `EVAL` before the `WHERE` that filters the same field | Kills filter pushdown; scans the index | Filter on raw fields first |
| `STATS ... BY` on a `text` field | No doc values | Group on the `.keyword` sub-field |
| Interpolating user input into the query string | Injection, identical in kind to `query_string` | `params` with `?` placeholders |
| Expecting `nested` objects to be queryable | ES\|QL cannot see nested sub-documents | Query DSL with a `nested` query, or flatten the model |
