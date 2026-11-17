---
name: classic-ir
description: Local BM25 code and text search + hybrid retrieval engine (SQLite FTS5 + RRF fusion). Use when finding code, searching notes/corpora, or first-pass retrieval before dense/rerank spend. Covers recall measurement and RM3-style expansion. Feeds breakthrough-finder stages retrieve/expand.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins: [python3]
---

# Classic IR

Find code and text fast, locally. Proven stack: BM25 via FTS5,
dense-slot interface, reciprocal-rank fusion, RM3 pseudo-relevance
expansion. Index your files, search with ranked BM25, expand queries,
fuse rankings.

## Commands (`ir.py`, stdlib + sqlite3 FTS5)

```
python ir.py index DIR --db corpus.db     # index .md/.txt files
python ir.py search DB "query" [--k 100]  # BM25 ranked JSON
python ir.py expand DB "query" [--k 5]    # RM3 candidate terms from top-k
python ir.py fuse A.json B.json [--k 60]  # RRF fusion of two rankings
```

## Rules

- First-pass is BM25 always (zero-shot robust, cheap, exact-match).
- Dense/LLM rerank only over top-100 — never full-corpus.
- RM3 expansion is opt-in per query (drift risk); log expansions.

## Worked example

```bash
python ir.py index ./notes --db notes.db        # 2 files indexed
python ir.py search notes.db "BM25 saturation"  # [{"path":"a.md","rank":1}]
python ir.py expand notes.db "BM25"             # [{"term":"rank","df_topk":2}]
```

Limits: lexical only (no semantics); Python ≥3.8 + FTS5;
stdlib only, no network, no secrets.
