# Painless and Runtime Fields — Computation Without a Reindex

Painless is the sandboxed scripting language behind runtime fields, script queries, script scores, update scripts, and ingest processors. It is the escape hatch, and every use of it costs per-document CPU that no index can amortise.

## Decision Order

1. **Can a mapping change solve it?** Usually yes, at the cost of a reindex. Cheapest at query time, most expensive to deploy.
2. **Can an ingest pipeline compute it at write time?** Once per document instead of once per document per query.
3. **Can a runtime field solve it?** No reindex, cost paid at query time, and it can be promoted to a real field later.
4. **Does the score depend on it?** `script_score`, over the smallest candidate set you can arrange (a `rescore` window over the top N, never the full result set).
5. **Script query as a filter?** Only after every indexed clause has already narrowed the set — it cannot use the index at all.

## Runtime Fields

```json
"runtime": {
  "response_bucket": {
    "type": "keyword",
    "script": "def s = doc['status'].size() == 0 ? -1 : doc['status'].value; emit(s >= 500 ? '5xx' : s >= 400 ? '4xx' : 'ok');" } }
```

- Defined in the index mapping (`elasticsearch >=7.11`) or inline in a search request under `"runtime_mappings"`. The inline form is per-query and changes nothing persistent — ideal for exploring data you do not control.
- `emit()` is mandatory; emitting nothing means the field is absent for that document, which is how you express "not applicable".
- Runtime fields can be queried, aggregated, and sorted like real fields. The cost is one script execution per document **considered**, so put every selective indexed filter before them in the `bool`.
- Promotion path: prove the definition as a runtime field, then bake the same logic into an ingest pipeline and reindex. Field name and output stay identical, so nothing downstream changes.
- `"dynamic": "runtime"` on the index maps newly-seen fields as runtime fields instead of indexed ones — queryable without contributing to the 1,000-field limit.

## Accessing Values

| Access | Source | Cost | Caveat |
|---|---|---|---|
| `doc['field'].value` | `doc_values`, columnar | Fast | Only for indexed fields with doc_values; throws if the field is missing unless you check `.size()` |
| `doc['field'].size()` | `doc_values` | Fast | **Always check before `.value`** — a missing field throws and fails the whole shard |
| `params._source.field` | `_source` JSON | Slow: parses the document per script call | The only way to read a field that has no doc_values (`text`, or `index: false` without doc_values) |
| `params['x']` | Request parameters | Free | The correct place for anything variable (see below) |

`doc['text_field']` does not work: `text` has no doc_values. Reach for the `.keyword` sub-field, or accept the `_source` cost.

## The Compilation Cache

Scripts are compiled to bytecode and cached **by exact source string**. This is the trap that ends in `circuit_breaking_exception: [script] Too many dynamic script compilations`.

```
// Wrong: a new source string per request, cache miss every time
"script": { "source": "doc['price'].value * 1.21" }

// Right: one cached compilation, parameter varies freely
"script": { "source": "doc['price'].value * params.rate", "params": { "rate": 1.21 } }
```

- `script.max_compilations_rate` defaults to 150 per 5 minutes per context. Hitting it means the code is interpolating values into source, essentially always.
- Store recurring scripts in the cluster state and call them by ID: `PUT /_scripts/<id>`, then `"script": {"id": "<id>", "params": {...}}`. One definition, one compilation, and a change deploys without touching application code.

## Script Score

```json
{ "script_score": { "query": {"match": {"title": "router"}},
    "script": { "source": "_score * Math.log(2 + doc['views'].value)" } } }
```

- Must return a non-negative number; a negative score throws at query time.
- `_score` is the wrapped query's score. Multiplying by an unbounded field value lets popularity swamp relevance — compress with `Math.log1p()` or a `saturation` rank feature instead.
- `script_score` replaces most of what `function_score` did, more predictably. Reach for `function_score` only when you need its multi-function combination modes.
- For a vector similarity on a non-indexed `dense_vector`, `cosineSimilarity(params.qv, 'embedding') + 1.0` is the brute-force path — correct, exhaustive, and only viable on small candidate sets.

## Update Scripts

```json
POST /<index>/_update/<id>
{ "script": { "source": "ctx._source.views += params.n", "params": {"n": 1} },
  "upsert": { "views": 1 } }
```

- `ctx._source` is mutable here; `ctx.op = 'noop'` skips the write entirely when nothing changed, which avoids a version bump and the resulting replication traffic.
- Every update is a delete plus a reindex of the whole document underneath. High-frequency counter updates on large documents are the classic merge-pressure generator — batch them, or keep counters outside the index.
- `retry_on_conflict: 3` handles concurrent updates to the same `_id`.
- `_update_by_query` with a script rewrites matching documents in place — the standard way to backfill a field after a mapping addition. It takes a snapshot at start and throws version conflicts on documents changed since; `conflicts: "proceed"` skips them and reports the count.

## Ingest Pipeline Scripts

`{"script": {"source": "ctx.full_name = ctx.first + ' ' + ctx.last"}}` inside a pipeline runs once per document at write time. Note the difference from update scripts: in ingest context the document is `ctx` directly, not `ctx._source`.

Prefer a purpose-built processor where one exists (`grok`, `date`, `split`, `convert`, `geoip`, `set`, `rename`) — they are faster and their failures are legible. A pipeline of ten small processors debugs far better than one script that does everything.

## Painless Gotchas

- `def` is dynamic typing; explicit types (`long`, `String`, `List`) compile to faster code and catch mistakes at compile time.
- No `null` coalescing on `doc[...]`: `doc['f'].size() == 0` is the null check, and skipping it is the most common cause of a script that works in dev and fails a shard in production.
- Dates from `doc_values` are `ZonedDateTime`; `.value.getYear()`, `.toInstant().toEpochMilli()`. Arithmetic on the raw millis is faster when you only need a difference.
- Loops are bounded by a statement limit that kills runaway scripts. Iterating a large array per document is a design signal, not something to work around.
- No `Math.random()`, no I/O, no reflection, no imports beyond the allowlist. This is deliberate: the sandbox is the reason scripting is enabled at all.
- Test in isolation before embedding: `POST /_scripts/painless/_execute` with a `context` and a `document` runs a script against a synthetic document and returns the result or the compile error.
