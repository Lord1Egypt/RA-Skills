# Debugging — Why This Document Does Not Match, or Does Not Rank

Symptom-first chains. Each step is a check that costs seconds; the ordering exists so the cheap eliminations happen before the expensive theorising. The seven-step triage summary is in SKILL.md (Search Triage); this is the depth per symptom.

## Zero Hits

1. **Does the document exist?** `GET /<index>/_doc/<id>`. A missing document is an ingest problem, and no amount of query work will find it.
2. **Is it visible yet?** A document is searchable only after a refresh (default 1s). `GET /_doc/<id>` reads the translog and is real-time; `_search` is not. `?refresh=wait_for` on the write settles this permanently.
3. **Are you querying the right index?** `GET /_cat/aliases?v` — an alias pointing at last week's index after a failed swap is a silent, total outage of new data.
4. **What is actually indexed for that field?** `POST /<index>/_analyze {"field": "title", "text": "<the exact source value>"}`. Compare its output to the terms your query uses.
5. **Is the field indexed at all?** `GET /<index>/_mapping/field/<field>`. Watch for `index: false`, `dynamic: false` on the parent (the value is in `_source` and nowhere else), or `ignore_above` shorter than the value.
6. **Is it a `term` on a `text` field?** The single most common cause (SKILL.md Core Rules 1). Switch to `match`, or to `term` on `.keyword`.
7. **Does the query parse as intended?** `GET /<index>/_validate/query?explain=true` with the body. A misplaced brace turns a filter into a no-op.
8. **Ask the document directly:** `GET /<index>/_explain/<id>` with the query body. It states, per clause, why the document did or did not match.

## Some Documents Match, Others Should But Do Not

- Compare two documents' term vectors: `GET /<index>/_termvectors/<id>?fields=title`. Different tokens for what looks like the same text means an analyzer change happened between the two writes — everything indexed before the change still holds the old tokens.
- Check for divergent mappings behind an alias: `GET /<pattern>/_field_caps?fields=<field>`. One index mapping the field as `keyword` and another as `text` gives half-working queries with no error.
- Values skipped by `ignore_above` (default 256 in dynamic mappings) or by `ignore_malformed` are in `_source` and absent from the index. `_termvectors` shows the absence; `_source` hides it.
- Multi-word queries failing while single words work: `operator` is `or` by default, so this is usually the reverse — check `minimum_should_match`, then check whether a stopword filter removed a term entirely.

## Wrong Documents Match

- Run with `"explain": true` on one wrong hit and read which clause contributed. A clause you thought was restrictive is usually scoring rather than filtering (SKILL.md Core Rules 2).
- A `bool` with only `should` clauses requires **one** match, not all. Adding a `filter` silently changes the requirement to zero.
- Array-of-objects matching the wrong combination is the flattening bug — it needs `nested`.
- Fuzzy or stemming collisions: `_analyze` both the query and the unexpected document's field. `universe` and `university` share a stem under the `english` analyzer.
- Leading-wildcard or `query_string` input from a user can match far more than intended: `_validate/query?rewrite=true` shows the expansion.

## Wrong Order

1. `"explain": true`, then read the breakdown for the document that ranks too high **and** the one that ranks too low. Fixing one without the other moves the problem.
2. Field boost missing, or `most_fields` accumulating many weak matches into a higher total than one strong match.
3. Length normalisation: a match in a short field outscores the same match in a long one by design (`b = 0.75`).
4. Same query returning different orders across requests → per-shard IDF or a score tie. Add a deterministic tiebreak sort, or pin with `?preference=`.
5. Nested or parent-child matches contributing zero score because `score_mode` was left at its default.
6. Popularity or recency signals absent, or multiplied in raw and swamping relevance.

## Data Looks Stale

- `GET /<index>/_settings/index.refresh_interval` — a load left it at `-1` and nobody restored it (SKILL.md Core Rules 7). Everything indexed since is invisible to search and perfectly retrievable by ID, which is exactly what makes this confusing.
- Alias not swapped after a reindex: `GET /_cat/aliases?v`.
- An open point-in-time or scroll pins an old segment view; the request is reading a frozen snapshot on purpose.
- Reading a replica that is behind, or a CCR follower index, which is read-only and lags by design.

## Cross-Checking Tools

```
GET  /<index>/_doc/<id>                                  # real-time, bypasses refresh
GET  /<index>/_termvectors/<id>?fields=<f>               # what is stored for THIS document
POST /<index>/_analyze  {"field":"<f>","text":"..."}     # what a value WOULD become now
GET  /<index>/_explain/<id>   + query body               # match/no-match with reasons
GET  /<index>/_validate/query?explain=true&rewrite=true  # syntax and expansion
GET  /<index>/_search?explain=true                       # per-hit score breakdown
GET  /<index>/_search  {"profile": true, ...}            # where the time goes
GET  /<pattern>/_field_caps?fields=*                     # mapping divergence across an alias
GET  /_cat/aliases?v                                     # which index is really being queried
```

`_analyze` reflects the **current** analyzer; `_termvectors` reflects what was stored **at index time**. When they disagree, an analyzer changed and the index was never rebuilt — that gap is the answer to a large share of "it worked last month".

## Reproducing Small

When the chains run out, shrink until the behaviour changes:

1. Copy 5-10 relevant documents into a scratch single-shard index with the same mapping. One shard removes IDF skew and distribution effects.
2. Strip the query to one clause. Add clauses back one at a time; the one that breaks it names the subsystem and the guide to open.
3. Still wrong on one shard with one clause? It is mapping or analysis, not query or cluster: compare `_analyze` output against the mapped field type and its analyzer.
4. Correct on one shard but wrong on the real index? It is distribution: shard-level statistics, divergent mappings across the alias, or an unhealthy node.
