# Exa Response Fields Reference

How to interpret and use every field Exa returns. Use these to evaluate, cite,
and cost-control. Never surface `EXA_API_KEY`, and keep diagnostic fields
(`requestId`, `costDollars`) internal unless the user asks.

---

## Top-level fields

| Field                | Where        | Meaning | How the agent uses it |
|----------------------|--------------|---------|-----------------------|
| `answer`             | answer       | The synthesized short answer text. | Present to the user, paired with its `citations`. Re-verify if time-sensitive. |
| `results`            | search, findSimilar | Array of matched pages. | Iterate, rank by `score`/recency, select what to read/cite. |
| `citations`          | answer       | Sources backing the answer: `{id,title,url,text?}`. | Render as the numbered Sources list; never drop them. |
| `requestId`          | all          | Opaque request identifier. | Internal only; use for debugging/support, not user output. |
| `resolvedSearchType` | search       | The type Exa actually used (e.g. `neural`/`keyword`). | Learn how `auto` resolved; inform refinement and cost. |
| `searchTime`         | search       | Server-side time for the search. | Performance diagnostics only. |
| `costDollars`        | all          | Usage cost of the call. | Track per call and per session; drive cost-control decisions (§15 of SKILL.md). |

---

## Per-result fields (`results[]`, also citations[])

| Field           | Meaning | How the agent uses it |
|-----------------|---------|-----------------------|
| `id`            | Canonical identifier — **equals the `url`**. | Use as the citation link; pass as `urls[]` to `contents`. |
| `title`         | Page title. | Display in citations and selection. |
| `url`           | Page URL (same as `id`). | Canonical link; never invent or shorten it. |
| `publishedDate` | Publish date (when known). | Judge recency for time-sensitive claims; report "as-of" dates. |
| `author`        | Author (when known). | Helps weigh source credibility. |
| `score`         | Relevance 0–1. | Rank/select results. It measures match to query, NOT truth. |
| `text`          | Full cleaned page text (if requested). | Read deeply only when needed; large/cost-heavy. |
| `highlights`    | Most-relevant snippets (if requested). | Targeted reading and precise quotes/citations. |
| `summary`       | Short summary (if requested). | Cheapest triage and grounding signal. |

---

## Using fields well

- **Select before fetching:** rank `results` by `score` and `publishedDate`, pick
  a few, then request `contents` only for those.
- **Cite with `url`/`id`:** every sourced claim links to the canonical `url`.
- **Recency:** always check `publishedDate` for volatile facts; prefer recent
  sources and state the as-of date.
- **`text` vs `highlights` vs `summary`:** escalate only as needed —
  `summary` → `highlights` → `text` — to control cost.
- **`costDollars`:** if it climbs, narrow scope, lower `numResults`, or stop.
- **`resolvedSearchType`:** if `auto` resolved to an unexpected type and results
  are weak, override `type` explicitly and re-run.
