# Example 04 — Multi-Step Research Workflow

A broader question requiring decomposition: break into sub-questions, run targeted searches, fetch full `contents` of the best sources, then synthesize a single cited brief.

## User request

> "Give me a research brief on the state of solid-state batteries for EVs in 2024:
> who the leading players are, the main technical hurdles, and expected timelines."

## Agent reasoning summary

- Compound question — decompose into 3 sub-questions (players, hurdles, timelines).
- Run one focused `search` per sub-question to gather diverse candidates, then dedup across all of them.
- Fetch full `contents` only for the top few deduped sources to ground a synthesized brief; cite throughout.

## Exa operation to use

Use **`search`** (one per sub-question) → then **`contents`** on the selected top sources (endpoints `POST /search`, `POST /contents`).

- Why: parallel narrow searches give better recall per sub-topic than one broad query. Deferring full text to a second `contents` call means you only pay for full text on the URLs you actually keep.
- Cost tradeoff: searches with `highlights` (no full `text`) are cheap for triage; full `text` via `contents` is the expensive step, so restrict it to ~4-6 winners. This is cheaper and more controllable than requesting full `text` on every search result.

## Request shape

Step 1 — three triage searches (highlights only, cheap):

```json
POST /search
{ "query": "leading companies developing solid-state EV batteries 2024",
  "type": "auto", "numResults": 8, "category": "company",
  "contents": { "highlights": { "numSentences": 2, "highlightsPerUrl": 2 } } }
```
```json
POST /search
{ "query": "technical challenges manufacturing solid-state batteries dendrites scale 2024",
  "type": "neural", "numResults": 8,
  "contents": { "highlights": { "numSentences": 2 } } }
```
```json
POST /search
{ "query": "solid-state battery commercialization timeline EV 2025 2026 2027",
  "type": "auto", "numResults": 8, "category": "news", "startPublishedDate": "2024-01-01",
  "contents": { "highlights": { "numSentences": 2 } } }
```

Step 2 — fetch full text for the deduped top sources:

```json
POST /contents
{ "urls": ["<top url 1>", "<top url 2>", "<top url 3>", "<top url 4>", "<top url 5>"],
  "text": { "maxCharacters": 5000 },
  "summary": { "query": "players, technical hurdles, and timelines for solid-state EV batteries" } }
```

## Response handling

1. **Pool** results from all three searches.
2. **Dedup by url** across the pooled set (canonicalize host/path, strip tracking params). The same authoritative page often appears in multiple sub-searches — keep the highest `score`.
3. **Filter by score** (`>= 0.15`) and prefer primary/specialist sources (OEMs, battery makers, trade press) over generic listicles.
4. **Select top 4-6** by score *with topic coverage in mind* — ensure each sub-question has at least one strong source before fetching full text.
5. **Fetch contents** for the selected URLs; build the brief only from returned `text`/`summary`.
6. Track `costDollars` across all calls; report the total if the user cares about budget.

## Citation behavior

- Assign `[n]` to each source that survives to the contents step, numbered by score-rank.
- Each section (Players / Hurdles / Timelines) cites the sources backing its claims.
- A source may support multiple sections and be reused across them with the same `[n]`.

## Final answer pattern

```
Research brief: Solid-state batteries for EVs (2024)

Leading players
- Toyota and Idemitsu announced a joint solid-state production plan [1].
- QuantumScape and Solid Power are the most-cited pure-play developers [1][2].

Main technical hurdles
- Dendrite formation at the lithium-metal anode limits cycle life [2].
- Scaling defect-free solid electrolyte sheets remains the key manufacturing barrier [2][3].

Expected timelines
- Limited/sample production targeted around 2026-2027; mass-market EV use later [3].

Bottom line
- Real engineering progress in 2024, but mass-market timelines remain uncertain and
  vendor-stated [3].

Sources (ranked by relevance):
[1] ... — https://...  (score 0.50)
[2] ... — https://...  (score 0.44)
[3] ... — https://...  (score 0.38, news, 2024-06-01)

Approx. Exa cost for this brief: $0.04 (3 searches + 1 contents call).
```

## Common failure mode

- **Fetching full `text` for every search result** (24 pages) — large cost and bloated context, most of it discarded.
- **Topic gaps**: ranking purely by `score` can leave one sub-question (e.g. timelines) with no strong source, so that section ends up thin or uncited.

## Improved version

- Two-phase retrieval: cheap `highlights` triage, then full `contents` only on winners.
- Coverage-aware selection: guarantee at least one strong source per sub-question before spending on `contents`.
- Surface uncertainty for vendor-stated timelines:

```
> Verification needed: timelines are company-stated targets, historically optimistic.
> Treat 2026-2027 as aspirational; cross-check against independent analysis or
> https://docs.exa.ai.
```
