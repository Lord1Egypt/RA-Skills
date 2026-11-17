---
name: authority-review
description: Use when the user asks "how authoritative is my site", about domain authority/DR, brand mentions, or why competitors outrank them on equal content. Reviews entity clarity, independent references, author credibility, and reputation signals from observable and imported evidence. Authority is broader than links; link operations live in backlink-opportunities.
---
# Authority Review

Authority is what independent parties say and how consistently you exist as an entity — links are one signal inside it, not the whole of it. This skill assesses the broader standing; it refuses to compress that into a number it did not measure.

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract (`evidence_type: authority`). Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Assess (open/import)

1. **Entity clarity.** One unambiguous answer to "who is this": consistent name/description/identifiers across the site, its schema markup, and the third-party surfaces the user names. Ambiguity here suppresses everything downstream.
2. **Independent references.** Citations, mentions, reviews, directories, press — imported or user-named, each with source and date. Distinguish independent references from self-placed ones.
3. **Author and editorial credibility.** Real authors with verifiable existence, credentials where claimed, editorial standards where implied. Overlaps `eeat-review`'s checklist — pull its output rather than re-deriving.
4. **First-party proof.** Product evidence, original data, named customers — the assets that give anyone a reason to cite this site.
5. **Comparative standing — cohort required.** Comparative claims ("weaker than competitors") require a named peer cohort with the same evidence collected for each peer. No cohort → report absolute observations only and say the comparison was not performed.

## Vendor metrics and scores

- DA/DR/AS and similar are **provider opinions, not Google metrics** — Google says third-party scores should locate problems, not become the optimization target. Report them only from imported/provider evidence, always with provider name and date, never merged into one number.
- **No composite authority score in open mode.** If evidence coverage is too thin for a defensible assessment, say `insufficient evidence` and list what is missing — do not emit a hedged score instead.

## Connected mode

TrustGrowth's `authority_score` (in `/score`) is TrustGrowth's own measured pillar — name it as such, never as a DA/DR equivalent. A detailed authority/backlink read surface is documented in the live OpenAPI when available; check at execution time and do not invent fields it does not have. `/eeat`'s authoritativeness pillar carries the signal-level detail available today.

## Sources by tier

Categories: `~~link database` and `~~AI monitor` (`references/connectors.md`). Tier 1 is observable pages plus a GSC Links export; Tier 2 adds Open PageRank as a labelled proxy; Tier 3 is TrustGrowth `authority` and `eeat`, or a paid index the user already has. Never invent a domain score.

## When not to use

- Backlink profile analysis, link gaps, reclamation, outreach planning → `backlink-opportunities`.
- On-site trust signals as a checklist → `eeat-review` (this skill consumes it).
- Whether AI engines cite you → `ai-visibility`.
- Anything that ends in a repository edit → `fix-my-site`.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
