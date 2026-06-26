# Recipe: Build a Research Brief

## Goal
Produce a structured, multi-source, fully cited research brief on a topic by orchestrating search → contents → synthesis, with explicit source evaluation and a cost ledger.

## When to use
- The user wants depth: "research X," "give me a brief/report on X," "what's the state of X."
- Multiple sub-questions or perspectives are needed.
- Not for a single fact (use `answer-with-sources.md`) or pure URL discovery (use `search-the-web.md`).

## Inputs
| Input | Required | Notes |
|-------|----------|-------|
| `topic` | Yes | The subject/question. |
| `sub_questions` | No | Explicit angles; otherwise derive 3–6. |
| `freshness` | No | If recent-only, set date range + `category:"news"`. |
| `domain_scope` | No | include/exclude domains. |
| API key | Yes | Header `x-api-key`. Never hardcode. |

## Steps
1. **Decompose** the topic into 3–6 sub-questions (`prompts/query-planning.md`). Cover definitions, current state, evidence, counterpoints, and recency.
2. **Plan queries per sub-question.** Choose neural vs keyword; add `category`/dates/domains as needed.
3. **Search each sub-question** (`search-the-web.md`), `numResults` 5–8 each. Keep cost lean — no `text` yet.
4. **Pool & dedupe** all results across sub-questions by normalized URL; rank by `score`.
5. **Evaluate sources** (`prompts/source-evaluation.md`): score, domain authority, recency, independence. Drop low-quality/duplicative ones. Aim for corroboration (≥2 independent sources per key claim).
6. **Fetch contents** only for the selected top sources (`get-and-summarize.md`), using `highlights`/`summary` to control cost; full `text` only where needed.
7. **Synthesize** per sub-question strictly from retrieved content (`prompts/synthesis.md`), keeping per-claim attribution. Note conflicts and gaps.
8. **Generate citations** — inline `[n]` + sources list (`prompts/citation-generation.md`).
9. **Hallucination check** (`prompts/hallucination-check.md`): every claim must be supported; flag/remove unsupported ones.
10. **Assemble the brief** and total the `costDollars` ledger.

## Output format
```
# Research Brief: <topic>
Date: <date>  | Sources evaluated: <n>  | Sources cited: <m>

## Summary
<5–8 sentence executive summary with [n] citations>

## <Sub-question 1>
<findings with [n] citations>

## <Sub-question 2>
...

## Conflicts & uncertainties
- <conflict/gap> [n]

## Sources
[1] <title> — <url> (published <date>, score <0-1>)
...

## Cost ledger
Search: $<x> | Contents: $<y> | Total: $<z>
```

## Example
```
# Research Brief: State of solid-state batteries (2025)
Date: 2026-05-31 | Sources evaluated: 18 | Sources cited: 7
## Summary
Solid-state cells reached X Wh/kg in lab settings [1][2], but manufacturing scale remains the bottleneck [3]...
## Manufacturing readiness
...[3][4]
## Conflicts & uncertainties
- Source [2] claims 2027 mass production; [5] says post-2030. [2][5]
## Sources
[1] ... — https://example.org/a (2025-03-12, score 0.91)
## Cost ledger
Search: $0.03 | Contents: $0.06 | Total: $0.09
```

## Edge cases
- **Thin coverage:** if few quality sources, say so explicitly; do not pad with weak/duplicative ones.
- **All sources agree but all from one outlet:** flag lack of independence; seek corroboration.
- **Conflicting data:** present both with attribution under "Conflicts."
- **Freshness:** for fast-moving topics, prioritize news-dated sources; mark anything older than the relevant window.
- **Errors:** `400` fix body; `401` stop; `429` back off. Never fabricate to fill a gap.

## Production notes (incl. cost)
- This recipe is the most expensive: many searches + multiple contents calls. Control cost by (a) lean `numResults`, (b) selecting only top sources for contents, (c) preferring `summary`/`highlights` over full `text`, (d) using `keyword`/`fast` where exact terms suffice.
- Maintain the cost ledger throughout; abort/trim if a budget cap is hit.
- Reuse cached search results across sub-questions to avoid re-billing overlapping queries.

> Verification needed: confirm endpoints, category values, and contents options with https://docs.exa.ai
