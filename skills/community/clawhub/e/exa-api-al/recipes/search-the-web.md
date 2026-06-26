# Recipe: Search the Web

## Goal
Run a single Exa web search and turn the raw `results` array into a ranked, deduplicated list of candidate sources (URL, title, date, score) that downstream recipes can act on.

## When to use
- The user asks "find pages / articles / sources about X."
- You need discovery (a set of URLs) rather than a finished answer. If the user wants a written answer with citations, use `answer-with-sources.md` or `build-research-brief.md` instead.
- As the first step inside larger recipes (research brief, monitor topic, compare companies).

## Inputs
| Input | Required | Notes |
|-------|----------|-------|
| `query` | Yes | A natural-language sentence (neural) or exact phrase/keywords (keyword). See `prompts/query-planning.md`. |
| `type` | No | `"auto"` (default), `"neural"`, `"keyword"`, `"fast"`. |
| `category` | No | e.g. `"news"`, `"research paper"`, `"company"`, `"pdf"`, `"github"`, `"tweet"`. |
| `numResults` | No | Default 10; keep small (5–10) to control cost. |
| `startPublishedDate` / `endPublishedDate` | No | ISO 8601 (e.g. `2025-01-01`). Combine with `category:"news"` for freshness. |
| `includeDomains` / `excludeDomains` | No | Scope to or away from specific sites. |
| API key | Yes | Sent as header `x-api-key`. Never hardcode; read from env. |

## Steps
1. **Plan the query.** Decide neural (conceptual sentence) vs keyword/fast (exact terms, names, error strings). Default to `type:"auto"` if unsure.
2. **Scope it.** Add `category`, date range, and domain filters only when they sharpen the result. Freshness-sensitive topics → `category:"news"` + `startPublishedDate`.
3. **Set `numResults` deliberately.** Start at 5–10. Do not request `text` here unless you need it now — fetch contents in a later step to keep cost down.
4. **Call search.** POST to the Exa search endpoint with header `x-api-key`. Body holds `query`, `type`, `category`, `numResults`, and any filters.
5. **Validate the response.** Confirm `results` is a non-empty array. If empty, broaden (drop a filter, switch `neural`→`auto`/`keyword`) and retry once.
6. **Normalize each result** to `{title, url, publishedDate, author, score}`. Remember `id === url`.
7. **Deduplicate** by normalized URL (strip trailing slash, `utm_*`, fragments) and by near-identical title.
8. **Sort** by `score` descending; surface the top N. Keep the full set available for later recipes.
9. **Record `costDollars`** from the response for the run's cost ledger.

## Output format
```
Query: "<query>"  (type=<type>, category=<category|none>, dates=<range|none>)
Results (sorted by score):
1. <title> — <url>
   score=<0-1>  published=<date|unknown>  author=<author|unknown>
2. ...
Cost: $<costDollars>
```

## Example
Request (conceptual):
```json
{
  "query": "recent breakthroughs in solid-state battery energy density",
  "type": "auto",
  "category": "research paper",
  "numResults": 5
}
```
Normalized output:
```
Query: "recent breakthroughs in solid-state battery energy density" (type=auto, category=research paper)
Results (sorted by score):
1. Sulfide electrolyte advances raise cell energy density — https://example.org/paper-a
   score=0.91  published=2025-03-12  author=A. Researcher
2. ...
Cost: $0.005
```

## Edge cases
- **Empty `results`.** Broaden once (remove date/category, or switch type). If still empty, report "no results" — do not invent URLs.
- **`400 INVALID_REQUEST_BODY`.** A field is malformed (bad date format, unknown `type`/`category`). Fix the body; do NOT blindly retry the same payload.
- **`401 INVALID_API_KEY`.** Key missing/invalid. Stop and surface a config error; never retry in a loop.
- **`429`.** Rate limited. Back off (exponential) and retry; reduce `numResults`/frequency.
- **Duplicate near-identical URLs** (http/https, www, tracking params): collapse before ranking.
- **Missing `publishedDate`/`author`:** render as `unknown`; never fabricate.
- **Paywalled/JS-heavy URLs:** fine to list here; flag when you later fetch contents.

## Production notes (incl. cost)
- `costDollars` appears on every response. `keyword` and `fast` are cheaper than `neural`; `auto` lets Exa pick. Prefer `keyword`/`fast` for known-string lookups, reserve `neural` for conceptual discovery.
- Requesting `text`/`highlights`/`summary` in the same call adds cost — omit at the discovery stage; fetch only the winners later (`get-and-summarize.md`).
- Keep `numResults` lean; more results = more downstream content cost, not just search cost.
- Log every `costDollars` to a per-task ledger so cost controls in `tests/skill-evaluation.md` can be checked.
- Cache identical queries within a session to avoid duplicate billing.

> Verification needed: confirm exact endpoint paths, current category enum values, and field names with https://docs.exa.ai
