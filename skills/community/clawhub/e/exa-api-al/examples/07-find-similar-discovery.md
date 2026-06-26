# Example 07 — Find Similar (Discovery from a Seed URL)

The user has one good page and wants more like it. Use `findSimilar` to discover semantically related sources (competitors, related papers), rank by `score`, and expand the user's list.

## User request

> "Here's a company I like: https://www.anthropic.com — find me other companies doing
> similar AI safety / frontier-model work."

## Agent reasoning summary

- The user gave a *seed URL* and wants neighbors — this is similarity discovery, not keyword search.
- Use `findSimilar` from the seed; it returns semantically related pages ranked by `score`.
- Dedup (exclude the seed and its own domain), rank by `score`, and present an expandable shortlist.

## Exa operation to use

Use **`findSimilar`** (endpoint `POST /findSimilar`).

- Why: `findSimilar` takes a URL and returns pages semantically similar to it — ideal for "more like this" (competitors, related research, similar products). A keyword `search` would require you to guess the right terms; `findSimilar` infers the concept from the seed page itself.
- Cost tradeoff: like `search`, requesting `contents.text`/`highlights` per result adds cost. For a discovery shortlist, request lightweight `highlights` (or nothing) first; fetch full `contents` only for the candidates the user wants to dig into.

## Request shape

```json
POST https://api.exa.ai/findSimilar
Headers: { "x-api-key": "<EXA_API_KEY>", "Content-Type": "application/json" }
{
  "url": "https://www.anthropic.com",
  "numResults": 15,
  "excludeSourceDomain": true,
  "category": "company",
  "contents": {
    "highlights": { "numSentences": 2, "highlightsPerUrl": 1 }
  }
}
```

Notes:
- `excludeSourceDomain: true` keeps the seed's own pages (and subpages) out of the results.
- `category:"company"` biases toward company homepages (use `"research paper"` for the academic variant of this task).

## Response handling

Response shape (abridged):

```json
{
  "results": [
    { "id": "https://openai.com", "url": "https://openai.com", "title": "OpenAI",
      "score": 0.61, "highlights": ["..."] },
    { "id": "https://deepmind.google", "url": "https://deepmind.google", "title": "Google DeepMind",
      "score": 0.57, "highlights": ["..."] }
  ],
  "costDollars": { "total": 0.01 }
}
```

Handling steps:
1. **Exclude the seed**: drop any result whose canonical URL/domain equals the seed (belt-and-suspenders even with `excludeSourceDomain`).
2. **Dedup by url**: canonicalize and collapse duplicates; also collapse multiple pages from the same company to one entry (keep highest `score`).
3. **Filter by score**: discard weak neighbors (`score < 0.2`); similarity scores cluster, so a relative cutoff (e.g. keep top decile gap) can work better than a fixed floor.
4. **Rank by score** descending — this is the discovery ranking the user sees.
5. **Optional enrichment**: for the top N the user is interested in, run `contents` to add a one-line description each.

## Citation behavior

- For discovery, the "citation" is the discovered URL itself — each list item *is* its source.
- Number items `[1..n]` by `score` and show the `score` so the user sees similarity strength.
- If you add descriptions from `contents`, those descriptions are grounded in (and cite) that item's own page.

## Final answer pattern

```
Companies similar to Anthropic (https://www.anthropic.com), ranked by similarity:

[1] OpenAI — https://openai.com  (similarity 0.61)
    Frontier model lab; develops GPT-series models and safety research.
[2] Google DeepMind — https://deepmind.google  (similarity 0.57)
    Research lab behind Gemini and foundational AI safety work.
[3] Mistral AI — https://mistral.ai  (similarity 0.49)
    Open-weight frontier model developer.

These are the strongest semantic neighbors of the seed page. Want me to expand the
list (raise numResults) or pull a deeper profile (contents) on any of them?
```

## Common failure mode

- **Using keyword `search` instead of `findSimilar`**, missing companies that don't share obvious keywords with your guessed query but are conceptually close.
- **Leaving the seed/its subpages in the results** (forgot `excludeSourceDomain`), so the top "discovery" is the company itself.
- **Listing the same company multiple times** (homepage + careers page + blog) because per-domain dedup was skipped.

## Improved version

- Default to `findSimilar` for "more like this"; set `excludeSourceDomain: true` and dedup per domain.
- Show `score` and offer to expand (`numResults`) or enrich (`contents`) — discovery is iterative.
- Flag when neighbors look off-topic (low cluster scores):

```
> Verification needed: results below similarity 0.3 drift off-topic (e.g. consultancies,
> not frontier labs). I trimmed them; broaden the seed or confirm at https://docs.exa.ai.
```
