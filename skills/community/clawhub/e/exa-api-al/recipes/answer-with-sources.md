# Recipe: Answer with Sources

## Goal
Produce a direct, cited answer to a factual question using Exa **answer**, returning `{answer, citations}`, and present it with inline `[n]` markers and a sources list.

## When to use
- The user asks a concrete, answerable question ("Who/what/when/how much…").
- You want a fast grounded answer without manually running search → contents → synthesis.
- Not for open-ended research reports (use `build-research-brief.md`) or pure discovery (use `search-the-web.md`).

## Inputs
| Input | Required | Notes |
|-------|----------|-------|
| `query` | Yes | The question, phrased clearly and specifically. |
| `text` | No | Request citation `text` snippets to verify support. |
| API key | Yes | Header `x-api-key`. Never hardcode. |

## Steps
1. **Sharpen the question.** Make it specific and answerable (add entity, timeframe, units). Vague questions yield weak citations.
2. **Call answer** with the `query` and header `x-api-key`. Request citation `text` when you need to verify claims.
3. **Validate.** Confirm `answer` is non-empty AND `citations` is non-empty. An answer with no citations is unsupported — treat with caution.
4. **Map claims to citations.** Run `prompts/hallucination-check.md`: every factual claim in `answer` must trace to a citation; flag any that don't.
5. **Render inline `[n]` citations** keyed to the `citations` list (`prompts/citation-generation.md`).
6. **Check freshness** for time-sensitive questions: inspect citation dates. If stale, fall back to search with `category:"news"` + `startPublishedDate`.
7. **Record `costDollars`.**

## Output format
```
<answer text with inline [1][2] markers>

Sources:
[1] <title> — <url>
[2] <title> — <url>

Cost: $<costDollars>
```

## Example
Query: "What is the current world record for the men's marathon?"
```
The men's marathon world record is <time>, set by <runner> at the <event, year>. [1][2]

Sources:
[1] <title> — https://example.org/record
[2] <title> — https://example.org/event

Cost: $0.01
```

## Edge cases
- **`answer` present but `citations` empty:** do not present as authoritative; fall back to `search` + `get-and-summarize` + `synthesis`, or state the limitation.
- **Time-sensitive query with stale citations:** redo via news-scoped search.
- **Ambiguous query:** ask one clarifying question or answer the most likely reading and state the assumption.
- **Claim unsupported by any citation:** drop it or label it explicitly as unverified — never present it as cited.
- **`400`:** fix body, no blind retry. **`401`:** stop, config error. **`429`:** back off + retry.

## Production notes (incl. cost)
- `answer` bundles retrieval + generation, so it can cost more than a bare `keyword` search but saves multiple round-trips. Use it for single questions; for multi-faceted reports, orchestrate search/contents yourself to control cost.
- Requesting citation `text` adds payload/cost but is worth it for verification on high-stakes answers.
- Always log `costDollars`.

> Verification needed: confirm `answer` request/response field names and citation `text` option with https://docs.exa.ai
