# Relevance — Making the Right Documents Come First

Ranking work has one rule above all others: **measure before and after, on a judgement set, never on the one query someone complained about**. Tuning by anecdote moves the complaint, not the quality.

## How BM25 Scores

`score(q, d) = Σ over query terms of  IDF(t) · (tf · (k1+1)) / (tf + k1 · (1 - b + b · dl/avgdl))`

- **IDF** — rare terms are worth more. A term in 5 of 1M documents dominates a term in 900k.
- **tf saturation** — `k1` (default 1.2) caps the payoff of repetition. The 10th occurrence of a term adds almost nothing; this is the main thing BM25 fixed over TF-IDF.
- **Length normalisation** — `b` (default 0.75) penalises long fields. A match in a 4-word title outranks the same match in a 4,000-word body, which is usually what you want and occasionally exactly what you do not.
- Tuning `k1`/`b` on the similarity is a late-stage move. `b: 0` (no length normalisation) is the one adjustment with a clear use case: fields where length carries no signal, like a comma-joined tag list.

Read a real score instead of theorising:

```
GET /<index>/_search { "explain": true, "query": {...} }
```

The breakdown names each contribution: `boost`, `idf`, `tf`, `dl`. Do this on one document that ranks too high and one that ranks too low before changing anything.

## Boosting, in Increasing Order of Blast Radius

1. **Field boost** — `"fields": ["title^3", "body"]`. Multiplies that field's contribution. Start here.
2. **Clause boost** — `{"match": {"brand": {"query": "acme", "boost": 2}}}` inside a `should`. Additive on top of the base score.
3. **`boosting` query** — `positive` / `negative` with `negative_boost: 0.2` demotes without excluding. The right tool for "show refurbished items, just lower".
4. **`constant_score`** — wraps a filter and gives every match a fixed score. Useful for combining a hard signal with BM25 in a `should` list.
5. **`dis_max` + `tie_breaker`** — take the best-matching clause, plus a fraction of the rest. What `best_fields` uses underneath.
6. **`function_score`** — arbitrary multiplication by field values, decay curves, or scripts. Powerful and easy to misuse; see below.
7. **`script_score`** — full Painless control of the final score. Last resort, and it disables some optimisations.

Boost values are relative and not linear in perceived quality. `^3` versus `^10` on a title rarely changes the top 3 but reshuffles positions 5-20. Change one boost at a time and re-measure.

## Signals That Are Not Text

- **`rank_feature` / `rank_features` field types** — store popularity, pagerank, or a click score, then use the `rank_feature` query. It is designed for this and runs far faster than `function_score`, because the field is indexed for exactly this access pattern. `saturation`, `log`, and `sigmoid` functions shape the curve.
- **`distance_feature`** — boost by proximity in time or space, natively. "Recent news first" and "near me first" without a script: `{"distance_feature": {"field": "@timestamp", "pivot": "7d", "origin": "now"}}`. The `pivot` is where the boost halves.
- **`function_score` decay functions** (`gauss`, `exp`, `linear`) — same idea with more control over `origin`, `scale`, `offset`, `decay`. `gauss` for "near the ideal", `exp` for "sharply prefer the newest".
- **Never multiply raw popularity into the score.** A product with 100,000 views beats every relevant result. Compress it first: `log1p(views)`, or a `saturation` rank feature with a pivot at the median.

## Score Consistency Traps

- **Scores are not comparable across queries or indices.** A 12.4 in one query and a 12.4 in another mean nothing to each other. Any absolute `min_score` threshold is a bug waiting for a corpus change.
- **IDF is computed per shard.** On a small or unevenly distributed index, the same document can score differently depending on which shard it lives on, and results reshuffle between identical requests. Fixes, in order: fewer shards (often one is correct for entity data); `?preference=<session_id>` so a user hits the same replica each time; `?search_type=dfs_query_then_fetch` to compute global term statistics first, at a round-trip cost.
- **Deleted documents still count toward term statistics** until their segments merge, so scores drift after a large delete or update batch until merging catches up.
- **Nested and parent-child scoring needs `score_mode`.** Default `avg` for `nested`, `none` for `has_child` — a child match contributing zero score is usually the unnoticed cause of "the join works but ranking is random".

## Rescoring: Cheap First, Expensive Second

```json
"rescore": { "window_size": 100,
  "query": { "rescore_query": {"match_phrase": {"body": {"query": "wireless router", "slop": 2}}},
             "query_weight": 0.7, "rescore_query_weight": 1.3 } }
```

Run a cheap recall query over everything, then re-rank only the top `window_size` per shard with the expensive signal (phrase proximity, a script, a model score). This is how proximity boosting stays affordable at scale.

- `window_size` is per shard, so with 5 shards you rescore up to 500 documents to return 10.
- Rescoring cannot pull a document into the window that the base query ranked below it. If the right answer is not in the first pass, no amount of rescoring finds it — fix recall first.

## Measuring: `_rank_eval`

```json
POST /<index>/_rank_eval
{ "requests": [ { "id": "router_query",
      "request": {"query": {"multi_match": {"query": "wireless router", "fields": ["title^3","body"]}}},
      "ratings": [ {"_index":"products","_id":"1","rating":3},
                   {"_index":"products","_id":"7","rating":0} ] } ],
  "metric": { "dcg": { "k": 10, "normalize": true } } }
```

- Metrics available: `precision_at_k`, `recall_at_k`, `mean_reciprocal_rank`, `dcg` (with `normalize: true` for nDCG), `expected_reciprocal_rank`. nDCG is the default choice when ratings are graded rather than binary.
- A judgement set of 30-50 real queries with the top 10 rated each is enough to catch regressions. Perfect coverage is not the goal; a stable baseline is.
- Source the queries from actual traffic, weighted by frequency. Tuning the head of the distribution is where the measurable wins are; the tail is where the interesting failures are.
- Run it in CI on every relevance change. Without it, "improving relevance" is indistinguishable from moving the problem.

## Common Ranking Complaints and Their Causes

| Complaint | Usual cause |
|---|---|
| Exact title match ranks below a long body match | No field boost, or `most_fields` summing many weak body hits |
| Short documents always win | `b: 0.75` length normalisation; lower `b` on that field or boost by a length-independent signal |
| Popular items never surface | No popularity signal, or one multiplied in raw and then clipped by a `min_score` |
| Same query, different order on refresh | Per-shard IDF, or a `should` clause tied on score; add a deterministic tiebreak sort on `_id` |
| A synonym match outranks the literal term | Index-time synonyms distorted document frequency — move them to search time |
| Recent content buried | No `distance_feature` on `@timestamp`, or a decay `scale` far wider than the content's actual lifespan |
| Stemming merged two different words | `english` is aggressive; try `light_english` or a `stemmer_override` |
