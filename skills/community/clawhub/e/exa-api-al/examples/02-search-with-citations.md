# Example 02 — Multi-Source Answer with Inline Citations

A question that benefits from several independent sources. The agent gathers multiple results, ranks them by `score`, writes inline `[1][2]` markers, and lists sources ranked by relevance.

## User request

> "What are the main health benefits and risks of intermittent fasting? Cite your sources."

## Agent reasoning summary

- Multi-faceted question (benefits *and* risks) — needs several sources, not one page.
- Use one `search` with inline `contents.text` to gather evidence, then synthesize across results.
- Rank sources by `score`, dedup by URL, and attach inline `[n]` markers to each claim.

## Exa operation to use

Use **`search`** with inline `contents` (endpoint `POST /search`).

- Why: a synthesized answer needs multiple grounded sources, each individually citable. `search` returns ranked candidates with `score`, which drives both selection and the sources ordering.
- Cost tradeoff: requesting `text` for ~6 results costs more than 3, but cross-source synthesis needs breadth. Use `highlights` to keep prompt context small while still grounding claims. (`/answer` would auto-cite, but here the user explicitly wants visible, score-ranked sources, so we control ranking ourselves.)

## Request shape

```json
POST https://api.exa.ai/search
Headers: { "x-api-key": "<EXA_API_KEY>", "Content-Type": "application/json" }
{
  "query": "health benefits and risks of intermittent fasting evidence",
  "type": "auto",
  "numResults": 6,
  "contents": {
    "text": { "maxCharacters": 1200 },
    "highlights": { "numSentences": 3, "highlightsPerUrl": 3 }
  }
}
```

## Response handling

1. **Collect** all `results`.
2. **Dedup by url**: canonicalize URLs (lowercase host, strip trailing `/`, drop `utm_*` and `ref` params, drop `#fragment`); keep the highest-`score` entry per canonical URL.
3. **Filter by score**: discard `score < 0.15`. If fewer than 3 survive, broaden the query or raise `numResults` and retry once.
4. **Rank** survivors by `score` descending — this order becomes the `[n]` numbering and the sources list.
5. **Map claims to sources**: for each claim, find which result's `text`/`highlights` supports it and tag with that `[n]`. A claim may carry multiple markers `[1][3]` when corroborated.

Example ranked set after dedup/filter:

```
[1] score 0.52  Mayo Clinic — intermittent fasting overview
[2] score 0.48  NIH/PubMed review — metabolic effects
[3] score 0.39  Harvard Health — fasting cautions
```

## Citation behavior

- Inline markers `[1]`, `[2]` appear immediately after the supported claim.
- Numbering follows score-rank (highest score = `[1]`).
- Corroborated claims may show multiple markers: `[1][2]`.
- Every `[n]` used inline MUST appear in the sources list, and vice versa (no orphan citations).

## Final answer pattern

```
Intermittent fasting (IF) shows several documented benefits and some risks.

Benefits
- Improved insulin sensitivity and lower fasting glucose in several studies [2].
- Modest weight loss comparable to continuous calorie restriction [1][2].
- Potential cardiometabolic improvements (blood pressure, lipids) [1].

Risks / cautions
- Not advised during pregnancy or for people with a history of eating disorders [3].
- Can cause hypoglycemia in people on glucose-lowering medication [3].
- Early side effects include headaches, irritability, and fatigue [1].

Sources (ranked by relevance):
[1] Mayo Clinic — Intermittent fasting overview — https://www.mayoclinic.org/...  (score 0.52)
[2] NIH/PubMed — Metabolic effects of IF (review) — https://pubmed.ncbi.nlm.nih.gov/...  (score 0.48)
[3] Harvard Health — Cautions on fasting — https://www.health.harvard.edu/...  (score 0.39)
```

## Common failure mode

- **Citation drift**: writing a fluent synthesis, then appending a generic list of URLs without verifying each inline `[n]` actually maps to text that supports that specific claim. Readers can't trace claims, and some claims end up uncited.
- Secondary: listing duplicate URLs (e.g. `http` vs `https`, `?utm_source=...`) as separate sources because dedup was skipped.

## Improved version

- Enforce a claim→source check: before finalizing, confirm every claim's `[n]` points to a result whose `text`/`highlights` contains that claim. Drop or soften claims with no support.
- Show `score` next to each source so the user sees ranking rationale.
- Flag thin evidence explicitly:

```
> Verification needed: the "cardiometabolic improvements" claim rests on a single
> source [1]. Treat as preliminary; confirm methodology, or see https://docs.exa.ai.
```
