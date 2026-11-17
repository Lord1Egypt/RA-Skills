# Source policy for AI conference deadlines

The skill's quality depends on a simple distinction:

```text
radar/index = fast discovery
official source = decision authority
```

## Fast radar/index sources

Use these first to discover likely venues, deadlines, and links:

1. `mlciv/ai-deadlines`
   - URL: `https://mlciv.com/ai-deadlines/?sub=ML,CV,CG,NLP,RO,SP,DM,AP,KR,HCI,EDU`
   - Role: primary fast radar for AI/ML/CV/NLP/robotics/security/data-mining/HCI/education.
   - Caveat: not final authority; entries may lag official CFP changes.

2. `ccfddl-rss`
   - URL: `https://ccfddl.com/conference/deadlines_zh.xml`
   - Role: structured RSS fast path for CCF-oriented deadline discovery, abstract/full stage hints, CCF rank/category hints, and official-site leads.
   - Caveat: CCF rank and community curation do not confirm submission dates; keep every parsed record as `radar_hint` until an official CFP/OpenReview/submission page is checked.

3. `aideadlin.es`
   - URL: `https://aideadlin.es/`
   - Role: alternate AI deadline index.
   - Caveat: often includes old entries; verify year and official link.

4. `aideadlines.org`
   - URL: `https://aideadlines.org/`
   - Role: broad AI conference deadline index.
   - Caveat: may be slow or have TLS/client issues from some Python runtimes; use browser/web fetch if script fetch fails.

## Official source hierarchy

Use these before making or changing a submission plan:

1. Official conference CFP / submission instructions / important dates page.
2. OpenReview venue page or submission invitation, when that venue uses OpenReview.
3. Official submission system page, if public.
4. Official rolling-review calendar, such as ACL Rolling Review dates for ACL-family venues.
5. Official mailing-list/X announcement only when the CFP page is not live yet.

## Status labels

- `official_confirmed`: official current-year page or OpenReview/submission page confirms the date.
- `historical_estimate`: inferred from a previous cycle; useful for planning, never cite as confirmed.
- `radar_hint`: found on a radar/index page only.
- `unverified`: seen in search or conversation, but no reliable source checked.

Preserve the helper's `source_kind` label unless you inspect a stronger source in the current turn. A `ccfddl-rss` record may contain an official-looking `source_url`, but it is still only a `radar_hint` until that page is opened and checked.

## Speed rules

1. Fetch radar/index sources concurrently with short timeouts.
2. Prefer the fast source order: `mlciv-ai-deadlines`, `ccfddl-rss`, `aideadlin.es`, then `aideadlines.org`.
3. Prefer structured `ccfddl-rss` records when present; they are faster and more stable than scraping CCFDDL pages, but they are still radar/index evidence.
4. Return after enough high-priority radar sources succeed; use `--wait-all` only for source-health diagnostics or contradictions.
5. Cache radar fetches for a few minutes in temp storage.
6. Use helper `candidate_links` as verification leads when present; still inspect the official page before labeling a deadline confirmed. If the query includes years, use them to rank snippets and links, but do not accept output that only matches the year and not the requested venue.
7. Let the helper's small built-in normalizer handle common venue aliases and stage labels, but do not treat it as a complete venue ontology.
8. Only verify official pages for venues that affect the user's decision.
9. Keep the target set small: normally 3-8 venues.
10. If a source fails, report the failure and continue with other sources; do not block the whole answer.

## Portable-agent rules

- Do not require WeHub, Hermes, Discord, a private project path, or an API key.
- If the bundled helper is unavailable, manually open the radar URLs and keep the same source hierarchy.
- If the agent cannot browse, answer only with known process guidance and mark date claims `unverified`; ask for official links or browsing permission before making submission decisions.
- If a radar page says "predicted", "estimated", "historical", or "verify on official site", preserve that uncertainty in the answer.
- Do not expand into a general conference catalog; speed comes from deciding which few venues matter.

## Quality rules

- Always separate abstract, full paper, supplement/code, rebuttal, notification, and camera-ready when available.
- Always preserve timezone; most AI conferences use AoE / UTC-12.
- Convert deadlines into next action only after source status is clear.
- Do not recommend a venue purely by topic fit; consider evidence standard, current paper maturity, and submission package readiness.
