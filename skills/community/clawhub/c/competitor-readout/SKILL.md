---
name: competitor-readout
description: Use when the user wants a periodic competitor digest — what tracked competitors changed, where the gaps are — as a document, from observation history or public diffs.
---
# Competitor Readout

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion. Output follows `references/reporting.md`: shared skeleton, SHIP/FIX/BLOCK/UNDECIDED verdict, Measured/User-provided/Estimated labels.

## Sources

Categories: `~~SEO tool`, `~~web crawler` (`references/connectors.md`).

- Tier 1 (open): fetch competitor pages now, diff against the Wayback Machine or a prior local crawl; on-page facts only (titles, structure, schema, published content). No prior state means observations, not changes.
- Connected (TrustGrowth): `GET /api/v1/sites/{slug}/competitors` (`?view=` for the observation-history view) and `GET /api/v1/sites/{slug}/keywords?type=content_gap` for keywords competitors hold that the site does not.

## Shape

One section per competitor that actually changed; competitors with no observed change get one line, not a section. Distinguish "changed" (two dated observations differ) from "new to us" (first observation). Traffic or ranking claims about a competitor from third-party tools are Estimated with the estimator named — never present them as the competitor's real numbers. Comparisons naming a competitor in outward-facing copy need owner review before they leave the report.

## When not to use

- Setting up or adjusting which competitors are tracked, or asking "how do I compare right now" interactively → `competitor-watch`.
- Acting on a gap keyword → `keyword-scout`, then `content-strategy`.
- Public claims built on this readout → `score-report` for the claim-safe path.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
