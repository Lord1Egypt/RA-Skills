# Search Strategy

Use this reference before changing adaptive search behavior.

## Design Goal

Follow the same broad pattern as mature tool-using search agents:

```text
start with a small search
inspect sources
expand only when needed
preserve all sources
stop when marginal value drops
```

The goal is not to maximize API calls. The goal is to maximize useful unique sources per call.

## Default Budgets

```text
fast:
  initial_queries: 1
  planned_query_limit: 1
  top_k: 10
  second_pass_terms: 0

normal:
  initial_queries: 3
  planned_query_limit: 12
  top_k: 20
  second_pass_terms: 0

deep:
  initial_queries: 5
  top_k: 30
  second_pass_terms: 5
```

Use `run_search_plan.py --top-k 50` only when the user wants a fixed, exhaustive run or when smoke testing the known Baidu `top_k=50` ceiling.

The preferred fixed-budget command is:

```bash
python scripts/adaptive_search.py --topic "<topic>" --mode deep --fixed --top-k 50
```

This still writes the same `run_summary.json`, `adaptive_trace.json`, `deduped_sources.json`, and `research_pack.md`.

## Stop Conditions

Adaptive search should stop after the initial stage when:

```text
required intent coverage has been attempted
and
raw_result_count >= max_raw_results
or
new_unique_sources / returned_references < min_unique_yield for low_yield_patience queries
```

Default unique-yield thresholds:

```text
fast: 0.35
normal: 0.25
deep: 0.18
```

These are intentionally conservative. If users complain about missing coverage, lower the threshold or increase patience.

`max_raw_results` is a soft cap until required intent coverage has been attempted. For normal product searches, required coverage includes overview, review, complaint, official, platform, and experience. This prevents a high `top_k` run from stopping before official/platform queries.

## Expansion Order

Use this order:

1. Seed queries: core topic, review, complaint.
2. Official and platform queries: official source, Zhihu, Tieba, Xiaohongshu, Bilibili, Weibo.
3. Coverage queries: owner/user reports, quality, price, forum/comparison.
4. Result-driven terms: only in deep mode by default.

## Reporting

Always report:

```text
queries run
raw result count
deduped source count
duplicate count
stop reason
top domains
known gaps
```
