# Recipe: Find Similar Sources

## Goal
Given a seed URL, use Exa **findSimilar** to discover related pages ranked by similarity `score`, then filter and present the strongest analogues.

## When to use
- The user has one good page and wants "more like this" (competitors, related papers, similar articles).
- Expanding a source set in a research brief beyond keyword/neural search.
- Not for answering a question (use `answer-with-sources.md`).

## Inputs
| Input | Required | Notes |
|-------|----------|-------|
| `url` | Yes | The seed page (an Exa `id`). |
| `numResults` | No | Default 10; keep lean. |
| `excludeSourceDomain` | No | Exclude the seed's own domain to avoid same-site near-duplicates. |
| `category` | No | Constrain to a type (e.g. `"company"`, `"research paper"`). |
| `includeDomains`/`excludeDomains` | No | Scope. |
| API key | Yes | Header `x-api-key`. Never hardcode. |

## Steps
1. **Validate the seed URL** is well-formed and on-topic (a bad seed yields bad neighbors).
2. **Call findSimilar** with the `url`, `numResults`, and filters (often `excludeSourceDomain:true`).
3. **Validate** `results` non-empty. If empty, relax filters or try a better/canonical seed URL.
4. **Normalize & dedupe** by URL; drop the seed itself if returned.
5. **Filter by `score`.** Keep results above a sensible similarity threshold; discard weak/off-topic tails.
6. **Evaluate** survivors (`prompts/source-evaluation.md`) for authority/recency if quality matters.
7. **(Optional) Fetch contents** for the top few (`get-and-summarize.md`) to confirm relevance.
8. **Record `costDollars`.**

## Output format
```
Seed: <url>
Similar sources (by score):
1. <title> — <url>  (score <0-1>, published <date|unknown>)
2. ...
Cost: $<costDollars>
```

## Example
```
Seed: https://example.org/company-a
Similar sources (by score):
1. Competitor B overview — https://example.org/company-b (score 0.86, published 2025-09-01)
2. Competitor C overview — https://example.org/company-c (score 0.81, published 2025-07-15)
Cost: $0.006
```

## Edge cases
- **Off-topic neighbors:** raise the score threshold or pick a more canonical/representative seed.
- **Same-site duplicates dominate:** set `excludeSourceDomain:true`.
- **Empty results:** seed may be too obscure/low-quality; switch to keyword/neural search instead.
- **Seed is paywalled/thin:** similarity may be weak; verify by fetching a couple of results' contents.
- **Errors:** `400` fix body; `401` stop; `429` back off.

## Production notes (incl. cost)
- findSimilar is a discovery call like search; the main extra cost comes from any subsequent contents fetches — fetch only the top survivors.
- Keep `numResults` modest; long tails are usually low-score noise.
- Log `costDollars`.

> Verification needed: confirm `findSimilar` parameter names (`excludeSourceDomain`, etc.) and response shape with https://docs.exa.ai
