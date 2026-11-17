# Autocomplete, Suggesters, and Highlighting

Four different problems get called "autocomplete". Pick by what the user is typing into, not by which feature sounds closest.

| Problem | Answer |
|---|---|
| Suggest a **query** to run ("wire" → "wireless router") | `completion` suggester over a curated query list |
| Match **documents** as the user types, prefix-wise | `edge_ngram` index analyzer, or `search_as_you_type` field |
| Correct a **typo** after zero or few results ("routr" → "router") | `term` / `phrase` suggester |
| Match anywhere inside a token ("less" → "wireless") | `ngram` analyzer, or the `wildcard` field type |

## `edge_ngram`: the workhorse

```json
"analysis": {
  "tokenizer": { "edge": { "type": "edge_ngram", "min_gram": 2, "max_gram": 15,
                           "token_chars": ["letter","digit"] } },
  "analyzer": { "ac_index": { "tokenizer": "edge", "filter": ["lowercase"] } } }
```

```json
"title": { "type": "text", "analyzer": "ac_index", "search_analyzer": "standard" }
```

- **`search_analyzer: standard` is not optional.** Ngramming the query too means "ca" is compared against the ngrams of "ca", and every document containing a word starting with "c" or "ca" matches — recall collapses into noise. This is the single most common autocomplete bug.
- `min_gram: 2` avoids indexing single-letter tokens that match a third of the corpus. `max_gram: 15` bounds index growth; queries longer than `max_gram` will not match unless you add a `truncate` token filter to the search analyzer.
- Index size roughly multiplies by `(max_gram − min_gram + 1)` for the ngrammed field. Put it on a multi-field, never on the only copy of the text.
- `token_chars` controls where the tokenizer splits; omitting it splits nowhere and produces ngrams that cross word boundaries.

## `search_as_you_type`

`elasticsearch >=7.2`. One field type that builds the shingled sub-fields for you:

```json
"title": { "type": "search_as_you_type", "max_shingle_size": 3 }
```

Creates `title._2gram`, `title._3gram`, and `title._index_prefix`. Query with `multi_match` type `bool_prefix` across all four. Less control than a hand-built `edge_ngram` field, much less setup, and it handles multi-word prefixes correctly — the right default unless you have a specific reason.

## `completion` suggester

An FST held **in memory**, prefix-only, extremely fast.

- Sub-millisecond even on millions of entries, because it never touches the inverted index.
- Prefix only: no infix, no fuzzy beyond a `fuzzy` block with an edit distance, no filtering except through `contexts` (category or geo).
- Not real-time: suggestions become visible after a refresh, and the whole FST is rebuilt per segment.
- Feed it a **curated list** — popular queries, product names, canonical entities — not raw document text. A completion field over full descriptions is a memory bill for suggestions nobody wants.
- Deduplicate with `skip_duplicates: true`, and weight entries with `weight` to force popular items up.

## `term` and `phrase` suggesters ("did you mean")

- `term` suggester corrects each token independently against the index's term dictionary. It has no idea whether the corrected combination exists, so "chees burgar" can become a phrase with zero hits.
- `phrase` suggester scores whole candidate phrases with an ngram language model — the one to use for a "Did you mean X?" line. It needs a shingled field to score against:

```json
"trigram": { "type": "text", "analyzer": "trigram_shingles" }
```

- `collate` runs each candidate as a real query and drops the ones returning nothing — the setting that turns suggestions into guaranteed-useful ones. Worth the extra queries.
- `suggest_mode`: `missing` (default, only for terms not in the index), `popular` (only suggest more frequent terms), `always`. `popular` is the usual production choice.
- Trigger on low result counts, not on zero: a query returning 2 poor results often needs correction more than one returning none.

## Infix and Substring Matching

- Full `ngram` (not `edge_ngram`) indexes every substring: `min_gram: 3, max_gram: 4` on a product-code field is workable; the same on descriptions is an index-size disaster.
- `index.max_ngram_diff` defaults to 1, so `min_gram: 3, max_gram: 4` is allowed but `3`-to-`6` needs the setting raised deliberately — the guard exists because the growth is multiplicative.
- The `wildcard` field type (`elasticsearch >=7.9`) is purpose-built for `*term*` on high-cardinality strings and usually beats ngrams for log-style grep on identifiers.
- Reverse-field trick for suffix search: index a `reverse`-filtered copy and query with a prefix on the reversed input. Cheaper than ngrams when only suffixes matter.

## Ranking Suggestions

Prefix matching returns many equally-valid candidates, so text score barely discriminates. Rank by a real-world signal:

- A `rank_feature` field holding search volume or click count, queried alongside the prefix match.
- `completion` suggester `weight`, set from the same data.
- Boost exact-prefix over ngram matches by querying both the `.ac` and `.keyword` sub-fields in one `multi_match` with a higher boost on the exact one.

## Highlighting

- Three highlighters: `unified` (default, works everywhere, uses the BM25 breakdown to pick the best fragments), `plain` (re-analyzes on the fly, accurate but slow on large fields), `fvh` (fast vector highlighter, needs `term_vector: with_positions_offsets` set at mapping time and roughly doubles that field's index size).
- Highlighting reads `_source` by default, so it fails on fields excluded from `_source`. `index_options: offsets` on the field lets `unified` highlight from postings instead, which is faster on big documents.
- `number_of_fragments: 0` returns the whole field highlighted rather than snippets — right for titles, wrong for article bodies.
- `highlight_query` lets you highlight terms from a different query than the one that matched: the standard trick for showing synonym or stemmed hits as the user's original word.
- On an `edge_ngram` field, highlighting marks the ngram, not the word — highlight the plain `text` multi-field instead and let the ngram field only do matching.

## Latency Budget

Autocomplete fires on every keystroke; treat 50 ms server-side as the ceiling.

- Debounce client-side (120-200 ms) before anything else — it removes more load than any server-side tuning.
- `"size": 5-10`, `_source` filtered to the two fields the dropdown renders, `track_total_hits: false` (the count is never shown).
- One `_msearch` for suggestions plus categories instead of two round trips.
- The prefix field on a small dedicated index (queries, product names) rather than the main document index: less data, better cache residency, and a rebuild that costs nothing.
