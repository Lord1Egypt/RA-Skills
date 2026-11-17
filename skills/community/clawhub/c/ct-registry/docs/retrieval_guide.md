# ct-registry — Retrieval Time & Data-Volume Guide

A search typically takes **10 seconds ~ 3 minutes**; large result sets (broad keywords,
deep pagination) can run up to **5 minutes**.

If a search exceeds 5 minutes without finishing, the system **returns the partial results
already retrieved** (instead of erroring) and marks the output with `is_timeout: true`.

You may trade off wait-time vs. completeness: wait for full results, or accept a partial
set for a quick preview.

## How many records fit in ~5 minutes?

Depends on query breadth; empirical ranges:

| Keyword type | Typical hit count | Fully retrievable in 5 min? | Empirical throughput |
|---|---|---|---|
| Narrow (e.g. `osimertinib`) | 20-200 | ✅ easily | WHO ~100-150 pages/min, CDE ~200-300 pages/min |
| Medium (e.g. `diabetes`) | 5,000-50,000 | ❌ partial only | 5 min ≈ 1,000-1,500 records |
| Broad (e.g. `cancer`) | 100,000+ | ❌ tiny fraction | first page ~30s, ~2-3s/page (WHO) |

- **If results are incomplete**: ① accept the partial set (sufficient for trend analysis); ② narrow the query (add intervention / sponsor / country filters); ③ split into multiple searches (by dimension).
