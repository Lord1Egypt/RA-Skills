# Recipe: Monitor a Topic

## Goal
Track new developments on a topic over time by running recurring, freshness-scoped Exa searches and reporting only genuinely new items since the last run.

## When to use
- The user wants ongoing updates: "keep me posted on X," "what's new in X this week."
- Periodic digests (daily/weekly) on a company, technology, regulation, or event.
- Not for one-time research (use `build-research-brief.md`).

## Inputs
| Input | Required | Notes |
|-------|----------|-------|
| `topic` | Yes | What to monitor. |
| `since` | Yes | Lower bound for `startPublishedDate` (e.g. last run timestamp). |
| `seen_urls` | No | Set of URLs already reported, to dedupe across runs. |
| `cadence` | No | daily/weekly — informs the date window. |
| `includeDomains` | No | Trusted outlets. |
| API key | Yes | Header `x-api-key`. Never hardcode. |

## Steps
1. **Scope for freshness.** Set `category:"news"` and `startPublishedDate = since` (and `endPublishedDate = now` if needed).
2. **Choose type.** `keyword`/`fast` for named entities (cheap, precise); `auto`/`neural` for conceptual themes.
3. **Search** (`search-the-web.md`) with small `numResults` (5–10).
4. **Filter to new.** Drop any result whose normalized URL is in `seen_urls`. Drop items older than `since` (defensive — some sources misreport dates).
5. **Evaluate** new items (`prompts/source-evaluation.md`); demote low-score/low-authority noise.
6. **Summarize** each new item briefly via contents (`get-and-summarize.md`), `highlights`/`summary` mode to keep cost low.
7. **Emit digest** sorted by recency then score. Update `seen_urls`.
8. **Record `costDollars`** and the new `since` for the next run.

## Output format
```
# <topic> — update since <since>
New items: <n>
1. <title> — <url>  (published <date>, score <0-1>)
   <1–2 sentence summary from contents>
2. ...
No new items found. (if empty)

Cost: $<costDollars>  | Next 'since': <now>
```

## Example
```
# EU AI Act enforcement — update since 2026-05-24
New items: 2
1. Regulator issues first guidance — https://example.org/n1 (2026-05-28, score 0.88)
   The agency clarified timelines for high-risk system audits...
2. ...
Cost: $0.02 | Next 'since': 2026-05-31
```

## Edge cases
- **No new items:** say so plainly; do not resurface old items or invent updates.
- **Date drift:** some pages report wrong/missing `publishedDate`; apply the `since` filter and treat `unknown` dates cautiously.
- **Duplicate coverage** of one event across outlets: cluster them; report the event once with multiple sources.
- **Errors:** `400` fix body; `401` stop; `429` back off (especially relevant for scheduled runs).

## Production notes (incl. cost)
- Recurring runs accumulate cost — keep `numResults` small, prefer `keyword`/`fast`, and fetch contents only for genuinely new, high-score items.
- Persist `seen_urls` and `since` between runs to avoid re-fetching/re-billing the same items.
- For schedules, stagger requests and honor `429` backoff to stay within rate limits.
- Log `costDollars` per run for trend visibility.

> Verification needed: confirm `startPublishedDate`/`category:"news"` behavior and date semantics with https://docs.exa.ai
