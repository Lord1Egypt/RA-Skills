# Example 01 — Basic Search (Single Factual Question)

A minimal end-to-end pattern: one `search` call answers a simple, factual question, and the agent cites the page it pulled the fact from.

## User request

> "Who is the current CEO of OpenAI, and when did they take the role?"

## Agent reasoning summary

- This is a single, well-scoped factual lookup — one `search` call is enough; no multi-source synthesis needed.
- Request the page `text` inline (`contents.text`) so the answer can be grounded without a second `contents` round trip.
- Keep `numResults` small (3) to control `costDollars`; pick the highest-`score` authoritative result.

## Exa operation to use

Use **`search`** (endpoint `POST /search`).

- Why: a search returns ranked candidate pages with `score`, and requesting `contents` inline gives the text needed to answer in the same call.
- Cost tradeoff: `search` alone is cheap; adding `contents.text` increases `costDollars` per result. For one fact, 3 results with text is a good balance. Avoid `/answer` here only if you specifically want to control the source ranking yourself — otherwise `/answer` is also valid (see Example 02).

## Request shape

```json
POST https://api.exa.ai/search
Headers: { "x-api-key": "<EXA_API_KEY>", "Content-Type": "application/json" }
{
  "query": "current CEO of OpenAI and when they took the role",
  "type": "auto",
  "numResults": 3,
  "contents": {
    "text": true,
    "highlights": { "numSentences": 2, "highlightsPerUrl": 2 }
  }
}
```

Notes:
- `type: "auto"` lets Exa choose neural vs. keyword. For a named-entity fact, this is reliable.
- The API key comes from the `EXA_API_KEY` environment variable. **Never hardcode it.**

## Response handling

Response shape (abridged):

```json
{
  "results": [
    {
      "id": "https://openai.com/about",
      "title": "About OpenAI",
      "url": "https://openai.com/about",
      "publishedDate": "2024-05-10",
      "author": null,
      "score": 0.41,
      "text": "Sam Altman is the chief executive officer of OpenAI...",
      "highlights": ["Sam Altman is the CEO of OpenAI."]
    }
  ],
  "costDollars": { "total": 0.005 }
}
```

Handling steps:
1. **Filter by score**: drop results below a sensible floor (e.g. `score < 0.15`) — they are weak matches.
2. **Dedup by url**: normalize `url` (strip trailing `/`, `utm_*` query params, `#fragment`) and keep the highest-`score` entry per canonical URL. Remember `id === url`.
3. **Prefer authoritative source**: among survivors, prefer the official/primary domain (here, `openai.com`) over aggregators.
4. **Extract the fact** from `text`/`highlights` of the chosen result. Do not state anything not present in the retrieved text.

## Citation behavior

- Cite the single result whose `text` supports the claim, using an inline marker `[1]`.
- The sources list maps `[1]` to the result's `title` + `url`.
- If two results support the fact, cite the most authoritative one; do not pad citations.

## Final answer pattern

```
Sam Altman is the current CEO of OpenAI [1]. He has held the role since the
company's founding in 2015, aside from a brief period in November 2023 [1].

Sources:
[1] About OpenAI — https://openai.com/about
```

## Common failure mode

- **Answering from the model's prior knowledge** instead of the retrieved `text`, then attaching a citation that does not actually contain the claim. This produces confident but unsupported answers and broken citation provenance.
- Secondary failure: citing a low-`score` aggregator blog rather than the primary source.

## Improved version

- Ground strictly: only assert what appears in the chosen result's `text`/`highlights`; if the text doesn't state the start date, say so rather than inventing it.
- Add a verification note when the primary source is ambiguous or undated:

```
Sam Altman is the current CEO of OpenAI [1].

> Verification needed: the retrieved page did not state an exact start date.
> Confirm with https://docs.exa.ai for sourcing, or re-run with category:"news"
> and a recent startPublishedDate for a dated source.

Sources:
[1] About OpenAI — https://openai.com/about (publishedDate: 2024-05-10)
```
