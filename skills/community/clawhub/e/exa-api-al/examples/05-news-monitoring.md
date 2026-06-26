# Example 05 — News Monitoring (Recency-Aware Search)

Time-sensitive question. The agent constrains results to recent news with `category:"news"` + `startPublishedDate`, dedups, and writes a recency-aware answer that cites publication dates.

## User request

> "What's the latest news on the NVIDIA antitrust investigations? Keep it to the past 30 days."

## Agent reasoning summary

- The user wants *fresh* news with an explicit time window — apply `category:"news"` + `startPublishedDate`.
- Sort/weight by recency (`publishedDate`), not just `score`, and dedup near-identical wire stories.
- Cite each fact with its publication date so the reader can judge freshness.

## Exa operation to use

Use **`search`** with `category:"news"` and a `startPublishedDate` freshness filter (endpoint `POST /search`).

- Why: `category:"news"` biases the index toward news outlets; `startPublishedDate` enforces the time window so stale evergreen pages are excluded.
- Cost tradeoff: requesting `highlights` (not full `text`) keeps cost low while still grounding each claim; fetch full `contents` only if the user wants a deep dive. `type:"fast"` lowers latency/cost for monitoring loops at some recall cost; `type:"auto"` is the safer default.

## Request shape

Compute the window relative to today (2026-05-31 → 30 days back = 2026-05-01):

```json
POST https://api.exa.ai/search
Headers: { "x-api-key": "<EXA_API_KEY>", "Content-Type": "application/json" }
{
  "query": "NVIDIA antitrust investigation",
  "type": "auto",
  "category": "news",
  "startPublishedDate": "2026-05-01T00:00:00.000Z",
  "endPublishedDate": "2026-05-31T23:59:59.000Z",
  "numResults": 12,
  "contents": {
    "highlights": { "numSentences": 2, "highlightsPerUrl": 2 }
  }
}
```

Notes:
- Always pass an ISO-8601 `startPublishedDate`; without it, the index may return undated/old pages even under `category:"news"`.
- `endPublishedDate` bounds the window precisely (useful for "past 30 days" vs. "this week").

## Response handling

1. **Filter to window**: trust `startPublishedDate`, but also drop any result with a missing or out-of-range `publishedDate` (some pages carry no reliable date).
2. **Dedup by url** AND **near-duplicate dedup**: wire stories (AP/Reuters) get reprinted across many outlets with near-identical text. Collapse by normalized title similarity + same date, keeping the original/highest-`score` outlet.
3. **Rank by recency, then score**: primary sort `publishedDate` descending so "latest" really means latest; break ties by `score`.
4. **Extract facts** from `highlights`; attach each to its dated source.
5. If 0 results: widen the window (e.g. 30 → 60 days) once and tell the user you did.

## Citation behavior

- Inline marker `[n]` after each fact, numbered newest-first.
- The sources list shows **`publishedDate` for every source** — non-negotiable for news, since freshness is the whole point.
- Distinct outlets covering the same event get separate entries only if they add new facts; otherwise collapse to one.

## Final answer pattern

```
Latest on NVIDIA antitrust investigations (window: 2026-05-01 to 2026-05-31)

- (May 28) Regulators reportedly expanded the probe to cover bundling practices [1].
- (May 20) NVIDIA filed a formal response disputing market-dominance claims [2].
- (May 6) A second jurisdiction opened a preliminary inquiry [3].

As of 2026-05-31, the most recent development is the May 28 expansion [1]. No newer
items appeared in the window.

Sources (newest first):
[1] ... — https://...  (publishedDate: 2026-05-28)
[2] ... — https://...  (publishedDate: 2026-05-20)
[3] ... — https://...  (publishedDate: 2026-05-06)
```

## Common failure mode

- **Omitting `startPublishedDate`**, so old evergreen explainers rank above genuine breaking news and the "latest" framing is wrong.
- **Wire-story duplication**: the same Reuters report appears 6 times, making thin news look like broad corroboration.
- **Undated claims**: presenting facts without `publishedDate`, so the reader can't judge recency.

## Improved version

- Always set `startPublishedDate` (and usually `endPublishedDate`) for "latest/recent" requests; state the window in the answer.
- Add explicit recency framing ("As of <today>, the most recent item is <date>") and newest-first ordering.
- Collapse near-duplicate wire reprints before counting corroboration.
- When the window is empty, widen once and disclose it:

```
> Verification needed: no qualifying news in the past 30 days. I widened the window
> to 60 days for the items above; confirm scope or check https://docs.exa.ai.
```
