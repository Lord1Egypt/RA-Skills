# agentMemo Evaluation Report

**Date:** 2026-03-16 05:10 UTC
**Server:** v2.2.0 | **Tasks:** 30 | **Categories:** 5

## 1. Performance Summary (Baseline vs agentMemo)

| Metric | Baseline | agentMemo | Delta |
|--------|----------|------------|-------|
| Accuracy | 0.0% | 100.0% | **+100.0%** |
| Latency P50 | 0.00ms | 25.06ms | +25.06ms |
| Latency P95 | 0.00ms | 335.81ms | +335.81ms |
| Avg Tokens | 17.6 | 69.8 | +296.0% |
| Memory Hit@1 | N/A | 100.0% | — |
| Memory Hit@5 | N/A | 86.7% | — |
| Avg Top Score | N/A | 0.0316 | — |

## 2. By Category

| Category | Baseline | Vault | Hit@1 | Search P50 |
|----------|----------|-------|-------|------------|
| context_retention | 0.0% | 100.0% | 100.0% | 144.8ms |
| decision_consistency | 0.0% | 100.0% | 100.0% | 24.8ms |
| error_correction | 0.0% | 100.0% | 100.0% | 25.4ms |
| preference_recall | 0.0% | 100.0% | 100.0% | 10.6ms |
| project_state | 0.0% | 100.0% | 100.0% | 27.6ms |

## 3. Cost Metrics

- **Write latency (P50/P95):** 18.5ms / 75.9ms
- **Search latency (P50/P95):** 1.1ms / 286.9ms
- **Storage per memory:** ~0 bytes
- **HNSW index vectors:** 86
- **Embedding cache hit rate:** 0.0%
- **Token overhead:** +296.0% (memory retrieval augments context)
