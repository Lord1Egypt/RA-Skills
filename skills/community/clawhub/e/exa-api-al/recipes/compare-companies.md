# Recipe: Compare Companies

## Goal
Build a side-by-side, cited comparison of two or more companies across consistent dimensions (what they do, products, funding/scale, recent news, differentiators) using Exa search/findSimilar/contents.

## When to use
- The user asks "compare A vs B," "who are X's competitors," or "A vs B vs C on [dimensions]."
- Competitive landscape or due-diligence snapshots.
- Not for a single-fact lookup (use `answer-with-sources.md`).

## Inputs
| Input | Required | Notes |
|-------|----------|-------|
| `companies` | Yes | List of names (and URLs if known). |
| `dimensions` | No | Default: overview, products, funding/scale, recent news, differentiators. |
| `freshness` | No | For "recent news," set date range + `category:"news"`. |
| API key | Yes | Header `x-api-key`. Never hardcode. |

## Steps
1. **Resolve each company** to a canonical source: search `category:"company"` for `"<name> company"` or use the provided URL. Confirm you have the right entity (disambiguate same-name firms).
2. **(Optional) Expand the set** for "competitors" requests via `find-similar-sources.md` on a seed company's URL.
3. **Define shared dimensions** so the comparison is apples-to-apples.
4. **Per company, per dimension, run scoped searches** (`search-the-web.md`): keyword/`category:"company"` for facts, `category:"news"`+dates for recent developments.
5. **Fetch contents** for the top source(s) per cell (`get-and-summarize.md`), `summary`/`highlights` mode to control cost.
6. **Extract facts strictly from retrieved text**, attributing each. Note "not found" where a dimension lacks evidence — do not guess.
7. **Evaluate sources** (`prompts/source-evaluation.md`); prefer primary/independent sources, especially for funding/scale.
8. **Assemble a comparison table** with inline `[n]` citations (`prompts/citation-generation.md`).
9. **Hallucination check** (`prompts/hallucination-check.md`); total the `costDollars` ledger.

## Output format
```
# Comparison: <A> vs <B> (vs <C>)
Date: <date>

| Dimension      | <A>            | <B>            |
|----------------|----------------|----------------|
| Overview       | ... [1]        | ... [4]        |
| Products       | ... [2]        | ... [5]        |
| Funding/scale  | ... [3]        | not found      |
| Recent news    | ... [6]        | ... [7]        |
| Differentiators| ...            | ...            |

## Notes & uncertainties
- <conflict or gap> [n]

## Sources
[1] <title> — <url> (date, score)
...

## Cost ledger
Search: $<x> | Contents: $<y> | Total: $<z>
```

## Example
```
# Comparison: Acme vs Globex
| Dimension     | Acme                         | Globex                       |
| Overview      | B2B logistics SaaS [1]       | Freight marketplace [4]      |
| Funding/scale | Series C, $X raised [3]      | not found                    |
| Recent news   | Launched EU expansion [6]    | Layoffs reported [7]         |
## Cost ledger
Search: $0.04 | Contents: $0.05 | Total: $0.09
```

## Edge cases
- **Same-name companies:** disambiguate via domain/HQ/industry before collecting facts.
- **Asymmetric data** (one company well-covered, another not): show "not found"; never backfill the gap by inference.
- **Funding/valuation figures vary by source:** cite the most recent primary source; note discrepancies.
- **Stale "recent news":** enforce date window; mark older items.
- **Errors:** `400` fix body; `401` stop; `429` back off.

## Production notes (incl. cost)
- Cost scales with companies × dimensions × contents fetches. Cap it: limit dimensions, fetch one strong source per cell, prefer `summary`/`highlights` and `keyword`/`category:"company"` over neural where possible.
- Reuse a company's resolved canonical page across dimensions instead of re-searching.
- Maintain the cost ledger; trim dimensions if a budget cap is hit.

> Verification needed: confirm `category:"company"` availability and findSimilar parameters with https://docs.exa.ai
