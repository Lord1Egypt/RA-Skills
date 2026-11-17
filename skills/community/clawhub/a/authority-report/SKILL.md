---
name: authority-report
description: Use when the user wants a periodic authority and backlink report — referring-domain movement, pillar state, prospect pipeline — as a document, from link exports or TrustGrowth authority data.
---
# Authority Report

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion. Output follows `references/reporting.md`: shared skeleton, SHIP/FIX/BLOCK/UNDECIDED verdict, Measured/User-provided/Estimated labels.

## Sources

Categories: `~~link database`, `~~search console` (`references/connectors.md`).

- Tier 1 (open): the user's `~~search console` links export (User-provided) plus Open PageRank for domain-level context (Estimated, named).
- Tier 2: `~~link database` provider the user already runs; individual-link claims carry that provider's name and crawl date.
- Connected (TrustGrowth): `GET /api/v1/sites/{slug}/authority` (paginated) — pillar state, referring-domain snapshots over time, and the prospect pipeline.

## Shape

Lead with movement in referring domains (gained, lost, unchanged) between two dated snapshots of the same source. Domain counts from different providers are different measurements — never subtract one from the other. The prospect pipeline reports states (identified, contacted, linked) as of the report date; outreach results are facts, expected links are not. Link quality judgments are interpretation and say so; no invented "domain authority" number is presented as a measurement.

## When not to use

- Judging whether specific links or domains are worth pursuing → `backlink-opportunities`.
- Reviewing and acting on the authority queue interactively → `authority-review`.
- Folding one authority line into a broader status → `weekly-report` or `score-report`.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
