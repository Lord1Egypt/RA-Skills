# Analyzers — The Chain That Decides What Matches

An analyzer is three stages in fixed order: **character filters** (rewrite the raw string) → **tokenizer** (split into terms, exactly one) → **token filters** (transform the term stream). Understand it once and most "why doesn't this match" questions answer themselves.

**Contents**: [The Symmetry Rule](#the-symmetry-rule) · [Built-In Analyzers Worth Knowing](#built-in-analyzers-worth-knowing) · [Stemming: What It Costs](#stemming-what-it-costs) · [Synonyms](#synonyms) · [Normalizers (Keyword Fields)](#normalizers-keyword-fields) · [Character Filters](#character-filters) · [Custom Analyzer Anatomy](#custom-analyzer-anatomy) · [Non-English and Mixed-Language Content](#non-english-and-mixed-language-content) · [Debugging the Chain](#debugging-the-chain)

## The Symmetry Rule

The index analyzer and the search analyzer must produce comparable tokens. They do not have to be identical — and the cases where they differ deliberately are the interesting ones.

| Field kind | Index analyzer | Search analyzer | Why |
|---|---|---|---|
| Normal text | `standard` or a language analyzer | same | Symmetry |
| Autocomplete | `edge_ngram`-based | `standard` | Ngramming the query too makes everything match everything |
| Synonym-expanded | `standard` | `standard` + `synonym_graph` | Change synonyms without a reindex |
| Codes and SKUs | `keyword` analyzer or a `keyword` field | same | No splitting, no lowercasing beyond a normalizer |

Verify, never assume:

```
POST /<index>/_analyze { "field": "title", "text": "Wi-Fi Router 5GHz" }
POST /<index>/_analyze { "analyzer": "my_search_analyzer", "text": "wifi router" }
```

Run both, diff the token lists. If the two sets share no term, the query cannot match no matter what the DSL says.

## Built-In Analyzers Worth Knowing

- `standard` — Unicode word boundaries + lowercase. Splits `Wi-Fi` into `[wi, fi]` and `5GHz` into `[5ghz]`. The default, and right most of the time.
- `keyword` — one token, the whole input, unchanged. For a `text` field that must behave atomically.
- `simple` — splits on anything non-letter, so `v2` becomes `[v]` and the digits are gone. A silent data-loss default for anything with version numbers.
- `whitespace` — splits on whitespace only, no lowercasing. Preserves punctuation, which is occasionally exactly right for code search.
- Language analyzers (`english`, `spanish`, `german`, …) — tokenize, lowercase, remove stopwords, stem. `running`, `runs`, `ran` all collapse to `run`.
- `standard` + `asciifolding` is the minimum viable analyzer for anything with accents: without it `café` and `cafe` are different terms.

## Stemming: What It Costs

- Stemmers are aggressive and lossy. English stemming maps `universe` and `university` to the same stem, and `international` to `intern`. Precision drops in exchange for recall.
- Order inside the filter chain matters: `lowercase` before any stemmer, always. A stemmer sees `Running` and does nothing with it.
- Protect terms with `keyword_marker` (a list of words the stemmer must skip) or fix individual cases with `stemmer_override` — cheaper and far more predictable than swapping stemmer algorithms.
- Serve both: index the stemmed field for recall and an unstemmed multi-field for precision, then boost the exact field in a `multi_match`.
- Stopword removal breaks phrases: with `english`, `"the who"` indexes as nothing at all. For an index with band names, film titles, or quotes, set `stopwords: "_none_"` and accept the size.

## Synonyms

```json
"filter": {
  "my_synonyms": { "type": "synonym_graph", "synonyms_path": "analysis/synonyms.txt", "updateable": true }
}
```

- Put synonyms in the **search** analyzer. Index-time expansion bakes the vocabulary into the segments, skews term statistics (a term with five synonyms inflates document frequency), and every edit becomes a reindex.
- `synonym_graph` is the multi-word-capable version and is only valid as a search-time filter. Plain `synonym` mishandles multi-word entries in phrase queries.
- `"updateable": true` plus `POST /<index>/_reload_search_analyzers` applies a changed synonym file without closing the index — the reason search-time wins operationally.
- Expansion (`ipod, i-pod, i pod`) is symmetric; contraction (`i-pod, i pod => ipod`) collapses to one term and is cheaper, but then the query must run through the same filter or it will not find it.
- Synonyms and stemming interact badly: put the synonym filter **before** the stemmer, so `automobile => car` happens on a whole word rather than on a stem nobody wrote a rule for.

## Normalizers (Keyword Fields)

A `keyword` field cannot use an analyzer, but it can use a `normalizer` — token filters only, no tokenizer:

```json
"normalizer": { "lc": { "type": "custom", "filter": ["lowercase", "asciifolding"] } }
```

Case-insensitive exact match on tags, emails, or country codes without switching to `text`. Without it, `term: {tag: "Sale"}` misses every document that stored `sale`.

## Character Filters

Applied before tokenization, so they can fix things the tokenizer would otherwise destroy:

- `html_strip` — removes markup from crawled content before it becomes terms.
- `mapping` — literal substitutions: `"&" => " and "`, `"." => ""` so `U.S.A` survives as `usa`.
- `pattern_replace` — regex; the usual job is stripping punctuation from phone numbers or part codes so `AB-1234` and `AB1234` collide.

## Custom Analyzer Anatomy

```json
"settings": { "analysis": {
  "char_filter": { "amp": { "type": "mapping", "mappings": ["& => and"] } },
  "filter": { "en_stem": { "type": "stemmer", "language": "light_english" } },
  "analyzer": { "content": {
      "type": "custom", "char_filter": ["amp"], "tokenizer": "standard",
      "filter": ["lowercase", "asciifolding", "en_stem"] } } } }
```

- `light_english` stems less aggressively than `english` — the usual right answer when the aggressive stemmer produced complaints.
- Analysis settings are **static**: adding or changing an analyzer requires closing the index (`POST /<index>/_close`, update, `_open`) and then reindexing for existing documents to use it. The exception is an `updateable` search-time synonym filter.
- Name analyzers by purpose (`content`, `sku`, `autocomplete_index`), never by construction (`custom_analyzer_2`) — the name shows up in every mapping that uses it.

## Non-English and Mixed-Language Content

- One field per language plus a language-detection step at ingest beats one analyzer for everything. Query all of them in a `multi_match` and let scoring pick.
- CJK: `standard` splits Chinese into single characters, which is usable but imprecise. `icu_tokenizer` (analysis-icu plugin) or a dedicated plugin does real word segmentation.
- `icu_folding` is a stronger `asciifolding` covering scripts beyond Latin; worth it as soon as content is not English-only.
- Case folding in Turkish is not the same operation as in English (dotless ı). Language-specific `lowercase` variants exist for exactly this — use them when the corpus is Turkish, Greek, or Irish.

## Debugging the Chain

```
POST /_analyze { "tokenizer": "standard", "filter": ["lowercase"], "text": "Wi-Fi", "explain": true }
GET  /<index>/_termvectors/<id>?fields=title
```

`"explain": true` shows the token stream after **each** stage, with positions and offsets — the fastest way to find which filter destroyed the term. `_termvectors` shows what is actually stored for a specific document, which settles arguments about whether a reindex ever happened.
