# Search Strategy

## Two-Stage Pipeline

### Stage 1: Server-Side (MCP)

Call `memos_search_memos(query="user intent")` for full-text candidate retrieval.
This returns a bounded candidate set from the Memos server.

Use this stage alone for simple keyword lookups.

### Stage 2: Client-Side Rerank (Optional)

For semantic or fuzzy queries, rerank candidates locally using
`scripts/fragments_search.py`:

```bash
# macOS / Linux
python3 scripts/fragments_search.py --query "..." --candidates '<json>'

# Windows
py scripts/fragments_search.py --query "..." --candidates '<json>'
```

The script uses TF-IDF + LSA (SVD) with cosine similarity.
Requires: Python 3.8+, numpy.

Output: ranked results with scores, titles, excerpts.

### When to Use Each

| Scenario | Approach |
|----------|----------|
| Exact keyword | Stage 1 only |
| Semantic / fuzzy intent | Stage 1 + Stage 2 |
| Browse recent memos | `memos_list_memos` (skip search) |

## Tuning

| Goal | Parameters |
|------|-----------|
| High precision | `--min-score 0.25 --top-k 5` |
| High recall | `--min-score 0.10 --top-k 10` |
| Balanced (default) | `--min-score 0.15 --top-k 8` |

## Token Discipline

1. Start with search or list (titles/excerpts only).
2. Expand to full content only for shortlisted IDs via `memos_get_memo`.
3. Avoid bulk retrieval unless explicitly requested.
