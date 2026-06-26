# Example 03 — Get Content from User-Supplied URLs

The user already has the URLs. The agent must NOT search — it should fetch the clean text of each URL with `contents` and summarize, citing each URL.

## User request

> "Summarize these two articles for me and tell me where they disagree:
> https://example.com/ai-regulation-eu and https://example.com/ai-regulation-us"

## Agent reasoning summary

- The user provided exact URLs — there is nothing to discover, so **do not call `search`**.
- Use `contents` to retrieve clean, readable `text` for the given URLs directly.
- Summarize each source separately, then compare; cite each URL by its position.

## Exa operation to use

Use **`contents`** (endpoint `POST /contents`).

- Why: `contents` returns clean extracted `text` (and optional `summary`/`highlights`) for known URLs without spending a search. Searching here would be wasteful and could return the wrong pages.
- Cost tradeoff: `contents` bills per URL for retrieval; requesting both `text` and a model-generated `summary` costs more than `text` alone. For a two-article compare, request `text` (full enough to compare) plus an optional `summary` only if you want Exa to pre-condense.

## Request shape

```json
POST https://api.exa.ai/contents
Headers: { "x-api-key": "<EXA_API_KEY>", "Content-Type": "application/json" }
{
  "urls": [
    "https://example.com/ai-regulation-eu",
    "https://example.com/ai-regulation-us"
  ],
  "text": { "maxCharacters": 4000 },
  "summary": { "query": "key claims and policy stance on AI regulation" }
}
```

Notes:
- `urls` (also accepted as `ids`, since `id === url`) is the list to fetch.
- `summary.query` focuses Exa's summary on what you care about (the comparison axis).

## Response handling

Response shape (abridged):

```json
{
  "results": [
    { "id": "https://example.com/ai-regulation-eu", "url": "https://example.com/ai-regulation-eu",
      "title": "The EU AI Act", "publishedDate": "2024-03-13",
      "text": "...", "summary": "The EU adopts a risk-tiered approach..." },
    { "id": "https://example.com/ai-regulation-us", "url": "https://example.com/ai-regulation-us",
      "title": "US AI Executive Order", "publishedDate": "2023-10-30",
      "text": "...", "summary": "The US relies on executive action and..." }
  ],
  "costDollars": { "total": 0.012 }
}
```

Handling steps:
1. **Map each result back to the requested URL** (match on `url`). Preserve the user's order for citation numbering.
2. **Check for retrieval gaps**: if a requested URL is missing from `results`, or its `text` is empty (paywall, JS-only page, 404), flag it — do not fabricate a summary.
3. **Summarize per source** from `text`/`summary` only.
4. **Diff**: identify points where the two `text` bodies make opposing claims.
5. No score/dedup logic needed — the user fixed the source set.

## Citation behavior

- Each provided URL gets a stable marker by input order: first URL = `[1]`, second = `[2]`.
- Every summarized point and every "they disagree on X" point cites the URL(s) it came from.
- Disagreement points carry both markers, e.g. `[1] vs [2]`.

## Final answer pattern

```
Article 1 — "The EU AI Act" [1]
- Adopts a risk-tiered framework with binding obligations for high-risk systems [1].
- Centralized enforcement via national authorities [1].

Article 2 — "US AI Executive Order" [2]
- Relies on executive action and agency guidance rather than a single statute [2].
- Emphasizes voluntary commitments from large AI developers [2].

Where they disagree
- Bindingness: EU imposes legally binding rules [1]; the US approach is largely
  voluntary/guidance-based [2].
- Structure: comprehensive single act [1] vs. distributed agency action [2].

Sources:
[1] The EU AI Act — https://example.com/ai-regulation-eu (2024-03-13)
[2] US AI Executive Order — https://example.com/ai-regulation-us (2023-10-30)
```

## Common failure mode

- **Reflexively calling `search`** on the article topic instead of `contents` on the given URLs — burning cost and risking summarizing different pages than the ones the user pasted.
- **Silently inventing a summary** for a URL whose `text` came back empty (paywalled/blocked), producing a fabricated comparison.

## Improved version

- Always use `contents` when URLs are supplied; reserve `search`/`findSimilar` for discovery.
- Handle missing/empty `text` explicitly:

```
Article 2 could not be retrieved — Exa returned empty text (likely paywalled or
JavaScript-rendered).

> Verification needed: re-try contents for https://example.com/ai-regulation-us,
> provide an archived/PDF link, or confirm options at https://docs.exa.ai.
I summarized Article 1 only; the comparison is incomplete until Article 2 loads.
```

- Optionally request `livecrawl: "always"` (or `"fallback"`) in `contents` to force a fresh fetch when the cached copy is stale or empty, accepting higher latency and cost.
