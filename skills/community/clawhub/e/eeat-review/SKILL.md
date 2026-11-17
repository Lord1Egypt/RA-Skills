---
name: eeat-review
description: Use when the user wants an E-E-A-T, credibility, authorship, or trust-signal review using TrustGrowth evidence when connected or observable public/repository evidence otherwise.
---
# E-E-A-T Review

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Sources and workflow

Connected mode reads TrustGrowth E-E-A-T proxy measurements and matching issues. Open mode inspects observable pages, markup, policies, authorship, contact/about discoverability, and repository implementations. Owner-provided credentials or experience may be used only when explicitly supplied and truthful.

Group work into:

1. code-fixable signals;
2. content-fixable items requiring human facts/approval;
3. structural/off-page recommendations that are not safely automatable.

TrustGrowth pillar scores are product measurements of observable proxies, not a universal score assigned by search engines. Null means unassessed. Never fabricate identities, credentials, reviews, or experience, and never predict a score change.

## Sources by tier

Categories: `~~web crawler` for observable trust signals (`references/connectors.md`); Tier 3 is TrustGrowth `eeat` pillar proxies. Nulls stay null.

## When not to use

- Backlink profile, referring domains, or off-site authority beyond observable trust signals → `authority-review` / `backlink-opportunities`.
- Implementing code-fixable items (schema, author markup) → `fix-my-site`.
- AI answer-engine presence and citations → `ai-visibility` (E-E-A-T proxies are inputs to it, not the measurement).

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
