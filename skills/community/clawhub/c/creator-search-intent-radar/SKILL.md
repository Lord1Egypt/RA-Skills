---
name: creator-search-intent-radar
description: Convert TikTok/YouTube/Instagram search and trend signals into a prioritized weekly content backlog with script angles and hook directions. Use when the user asks what to post next, wants trend-based topic discovery, needs search-intent analysis, or wants a platform-by-platform content idea pipeline.
---

# Creator Search Intent Radar

## Skill Card

- **Category:** Market Intelligence
- **Core problem:** What should we post next with real demand signals?
- **Best for:** Weekly planning and topic prioritization
- **Expected input:** TikTok/YouTube/Instagram trend snippets, search hints, comments/DM FAQs
- **Expected output:** Ranked topic backlog + platform fit + hook directions + CTA
- **Creatop handoff:** Send top 3 topics into Creatop script workflow

## Overview

Turn noisy trend inputs into **ranked, publishable decisions**.

Priority order:
1) demand signal quality
2) audience fit
3) monetization fit
4) execution speed

## Workflow

### 1) Collect demand signals

Gather 10–30 candidate signals from:
- TikTok search/trend surfaces
- YouTube search/autosuggest
- Instagram/Reels momentum
- comments/DM FAQs/community threads

Record provenance for each signal:
- `source_type` (official/community/internal)
- `source_link` (if available)
- `captured_at`
- `confidence` (high/medium/low)

If live endpoints are unavailable, run **fallback mode** using recent internal patterns and clearly label output as `mode: fallback`.

### 2) Normalize and dedupe backlog

For each topic, standardize:
- `topic`
- `platform_fit` (TikTok / YouTube / Instagram)
- `intent_type` (learn / compare / buy / troubleshoot / inspiration)
- `freshness` (hot / warm / evergreen)
- `audience_fit` (1–5)
- `monetization_fit` (1–5)
- `difficulty` (1–5)

Merge near-duplicate topics before scoring.

### 3) Score and rank

Use:

`priority_score = (audience_fit * 0.35) + (freshness_score * 0.25) + (monetization_fit * 0.25) + (execution_speed * 0.15)`

Mapping:
- `freshness_score`: hot=5, warm=3, evergreen=2
- `execution_speed = 6 - difficulty`

### 4) Generate decision output

Return:
1. Top 10 ranked topics
2. Per topic: 1 content angle + 3 hook directions + CTA
3. 7-day lightweight schedule

Include `data_confidence` for each topic (high/medium/low).

## Output format

- Topic:
- Why now:
- Platform:
- Intent:
- Angle:
- Hook directions (3):
- CTA:
- Confidence:

## Quality and safety rules

- Do not present synthetic/internal signals as live external trends.
- Avoid generic topics without clear buyer intent.
- Keep recommendations executable by small creator teams.
## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
