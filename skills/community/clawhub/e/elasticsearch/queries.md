# Query DSL — The Clauses That Carry the Work

Compact reference for building and reading query bodies. Type-selection table and the term-vs-match rule live in SKILL.md; this is the depth behind them.

**Contents**: [`bool` Semantics](#bool-semantics) · [Full-Text Clauses](#full-text-clauses) · [Term-Level Clauses](#term-level-clauses) · [Fuzziness](#fuzziness) · [Result Shaping](#result-shaping) · [Reverse Search With `percolator`](#reverse-search-with-percolator) · [Reading a Query Before You Run It](#reading-a-query-before-you-run-it)

## `bool` Semantics

```json
{"bool": {
  "must":     [ {"match": {"title": "wireless router"}} ],   // scores
  "should":   [ {"match": {"brand": "netgear"}} ],           // boosts if present
  "filter":   [ {"term": {"status": "active"}},
                {"range": {"price": {"lte": 200}}} ],        // no score, cached
  "must_not": [ {"term": {"discontinued": true}} ],          // no score, cached
  "minimum_should_match": 1 }}
```

- `minimum_should_match` default depends on context: **0** when `must` or `filter` is present (should clauses only boost), **1** when the bool has only `should` clauses (they become the requirement). Every bool with `should` should state it explicitly; relying on the implicit switch is how a filter change silently widens a result set.
- It accepts counts (`2`), percentages (`"75%"`), negatives (`-1` = all but one), and combinations (`"2<75%"` = require all if ≤2 clauses, else 75%).
- `must_not` is filter context, so it never contributes score — a common surprise for people expecting a penalty rather than an exclusion. For a soft penalty use `boosting` with `negative_boost`.
- Nesting bools is normal and cheap. Deeply nested `should` groups still resolve to one Lucene BooleanQuery; readability is the only real constraint.

## Full-Text Clauses

| Clause | Behaviour | Notes |
|---|---|---|
| `match` | Analyzes the input, ORs the terms by default | `operator: "and"` or `minimum_should_match` to tighten |
| `match_phrase` | Terms in order, adjacent | `slop: N` allows N position moves; `slop: 2` covers most word-order variation |
| `match_phrase_prefix` | Phrase where the last term is a prefix | Expands to `max_expansions` terms (default 50) — the results are not the "best" 50, just the first 50 alphabetically |
| `match_bool_prefix` | Every term a `term` query, last one a prefix | Better default for search-as-you-type than phrase_prefix; order-independent |
| `multi_match` | One query, several fields | Type matters, see below |
| `combined_fields` | Treats several fields as one, with correct BM25 across them | Requires the same analyzer everywhere; the principled version of `cross_fields` |
| `query_string` | Full Lucene syntax including `AND`, `*`, `~`, field prefixes | Throws 400 on malformed input — never hand it raw user text |
| `simple_query_string` | Same idea, never throws, ignores what it cannot parse | The safe one for a user-facing "advanced search" box |
| `intervals` | Positional rules: term A within N words of B, ordered or not | The tool for legal and patent search where proximity is the requirement |

### `multi_match` types

- `best_fields` (default) — score = the single best-matching field. Right when one field is expected to contain the whole query ("wireless router" in the title).
- `most_fields` — score = sum across fields. Right for the same text analyzed several ways (stemmed + unstemmed + ngram), which is the standard recall-plus-precision pattern.
- `cross_fields` — treats the fields as one big field, so "John Smith" can match `first_name` and `last_name` separately. Requires identical analyzers per group or it silently falls back to `best_fields` per analyzer group.
- `phrase` / `phrase_prefix` — runs `match_phrase` per field with `best_fields` scoring.
- `tie_breaker` (0-1) adds a fraction of the non-best fields' scores to `best_fields`; 0.3 is the common starting value when pure best-field ranking feels too binary.

## Term-Level Clauses

- `term` — exact, unanalyzed. `case_insensitive: true` exists (`elasticsearch >=7.10`) but a `normalizer` on the field is cheaper.
- `terms` — OR of exact values. Capped by `index.max_terms_count` (65,536). Past that, or when the list lives in another index, use a **terms lookup**: `{"terms": {"user_id": {"index": "groups", "id": "g1", "path": "members"}}}` — one fetch instead of a giant request body.
- `range` — numbers, dates, IPs, and version strings. Date math is relative to the coordinating node's `now` unless you pass `time_zone`; round it (`now-1d/d`) so the request cache can hold the result, because an unrounded `now` makes every request unique.
- `exists` — matches when the field has at least one indexed, non-null value. `""` and `[]` count as present; `null`, a missing key, and a value skipped by `ignore_above` or `ignore_malformed` count as absent.
- `prefix`, `wildcard`, `regexp`, `fuzzy` — all expand to a term set before executing. Leading wildcards scan the entire term dictionary of that field. Use the `wildcard` field type, an `edge_ngram` field, or a reversed field instead.
- `ids` — fetch by `_id`, the cheapest lookup there is.
- `script` — last resort; runs per candidate document with no index support.

`search.allow_expensive_queries: false` (cluster setting, `elasticsearch >=7.7`) blocks `script`, `regexp`, leading-wildcard, `prefix` on non-optimised fields, `fuzzy`, and joining queries outright. Worth enabling on a shared cluster so one bad query cannot take the tier down.

## Fuzziness

- `fuzziness: "AUTO"` = 0 edits for terms of 1-2 characters, 1 edit for 3-5, 2 edits above 5. Short, typo-prone queries get **no** tolerance under AUTO — set `AUTO:3,6` or a literal `1` when short queries matter.
- Edits are Levenshtein on the analyzed term, so stemming happens first and can make two different words one edit apart.
- `prefix_length` (default 0) freezes the first N characters and cuts the expansion cost sharply; 1 or 2 is nearly free precision.
- `max_expansions` (default 50) caps candidate terms per field. On a large term dictionary this silently truncates, so fuzzy results can be non-deterministic across shards.
- Fuzzy is not spell-correction. For "did you mean", use the term or phrase suggester.

## Result Shaping

- `_source` filtering: `"_source": {"includes": ["id","title"]}` — cuts payload and JSON parsing; the single easiest latency win on wide documents.
- `fields` (`elasticsearch >=7.10`) returns formatted values from `doc_values` or runtime fields, respecting the mapped `date` format — preferable to `_source` when you want the indexed representation.
- `sort` on anything means the sort field needs `doc_values`; sorting on `_score` is the default and free. Sorting by a `text` field is impossible — use the `.keyword` sub-field.
- `collapse: {"field": "product_id"}` deduplicates by a `keyword` field and optionally returns `inner_hits` per group. Cheaper than a `terms` + `top_hits` aggregation, but it collapses only the returned page, so the total is still uncollapsed.
- `track_total_hits` defaults to 10,000: past that, `hits.total.value` reports `10000` with `"relation": "gte"`. Set `true` only when the exact count is a product requirement — it forces a full match count.
- `min_score` cuts the tail, but BM25 scores are not comparable across queries or indices; a threshold tuned on one query set will discard good results on another.
- `_msearch` runs several bodies in one round trip with per-request shard parallelism — the right shape for a page that needs facets from a different query than the results.

## Reverse Search With `percolator`

Normal search stores documents and runs a query. Percolation stores **queries** and runs a document against them: "which saved searches would this new listing have matched?" That is the alerting primitive — price watches, job alerts, fraud rules, content moderation.

```json
PUT /alerts/_mapping
{"properties": {"query": {"type": "percolator"},
                "title": {"type": "text"}, "price": {"type": "double"}}}

PUT /alerts/_doc/watch-1
{"query": {"bool": {"must": [{"match": {"title": "wireless router"}}],
                    "filter": [{"range": {"price": {"lte": 100}}}]}}}

GET /alerts/_search
{"query": {"percolate": {"field": "query",
                         "document": {"title": "Wireless router AC1200", "price": 89}}}}
```

- **The percolator index must carry the mapping of the documents you percolate**, not just the `percolator` field. The stored query is parsed against that mapping, so `price` must be mapped there even though no real product ever lands in this index. Mapping drift between the alerts index and the live index is the failure mode: analyzers diverge, matches silently stop.
- It does not brute-force every stored query. At index time Elasticsearch extracts the mandatory terms of each query into a hidden field and uses them to pre-select candidates, so the cost scales with how many stored queries *could* match, not with how many exist. Queries with no extractable term (pure `range`, `wildcard`, `script`) skip that filter and are verified on every percolation — keep them a minority.
- `percolate` accepts `documents` (an array) to test a batch in one call, and `_percolator_document_slot` in the hit tells you which input document matched which stored query.
- Combine with `highlight` to show the user *why* their alert fired, and with an ordinary `bool.filter` on the alerts index (`{"term": {"user_id": ...}}`) to percolate against one tenant's watches only.
- Scale ceiling: percolation is a search over the alerts index, so it shards and caches like any other. Millions of stored queries are fine; a single document percolated against them on every write is not — batch the writes, or run percolation from an ingest queue rather than inline in the write path.
- Not for: threshold alerts over aggregates ("more than 100 errors in 5 minutes"). Percolation is per-document. Aggregate conditions need Watcher or a scheduled query.

## Reading a Query Before You Run It

```
GET /<index>/_validate/query?explain=true&rewrite=true    # syntax + the rewritten Lucene form
GET /<index>/_search?explain=true                         # per-hit score breakdown
GET /<index>/_explain/<id>                                # why one document did or did not match
```

`rewrite=true` shows what a `wildcard` or `fuzzy` clause actually expanded into — the fastest way to see that one innocent-looking clause became 4,000 terms.
