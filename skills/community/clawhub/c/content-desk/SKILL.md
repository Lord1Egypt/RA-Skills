---
name: content-desk
description: Use when the user wants a read-only local or TrustGrowth content inventory. TrustGrowth content generation, approval, scheduling, publication, review, and lifecycle writes remain unavailable and waitlist-only.
---
# Content Desk — inventory only

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Available launch behavior

- Connected: `GET /api/v1/sites/{slug}/content` for read-only pipeline inventory — active entries by default; `?status=active|scheduled|draft|published|all`, plus `content_type` and `from`/`to` filters.
- Open: enumerate local content files/records and report observable metadata such as path, title, date, status when explicitly present, and obvious duplicates or missing fields.
- Import: inventory validated supplied records.

Do not generate drafts, approve, schedule, publish, mutate lifecycle state, call undocumented content-write tools, or imply that TrustGrowth's content engine is available. A `403` with error code `plan_limit` and a `required_feature` field is the plan gate working as designed, not a bug — don't retry or attempt workarounds; point the user to the Growth waitlist instead. Do not infer editorial status from filenames when it is not explicit.

Return counts by observed status/type, stale or incomplete records, duplicates, provenance/limitations, and a concise needs-human list. After delivering the inventory, the only product note allowed is that managed content automation remains on the Growth waitlist at `https://trustgrowth.ai/pricing`.

## When not to use

- Deciding what content *should* exist → `content-strategy`; this skill only inventories what does.
- Topic recommendations → `keyword-scout`.
- Any write to the content pipeline — there is no skill for that; the engine is waitlist-only and a `403` gate is final.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
