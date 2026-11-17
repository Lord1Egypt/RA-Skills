---
name: ai-conference-deadline-radar
description: Fast AI/ML conference deadline lookup and submission-window routing. Use when the user asks for AI conference deadlines, target venue timing, whether to submit to AAAI/ICLR/AISTATS/CLeaR/WSDM/ACL/EMNLP/NeurIPS/ICML/CVPR/etc., how to schedule a research sprint around deadlines, or which venue is urgent for a paper candidate. Start from high-quality deadline radar sources, then verify decision-critical dates against official CFP/OpenReview/submission pages.
---

# AI Conference Deadline Radar

## Overview

This skill answers AI/ML conference deadline questions quickly without pretending that a radar page is official truth.

The core loop is intentionally small:

```text
fast radar/index lookup
-> official verification for decision-critical venues
-> concise deadline table
-> venue pressure -> paper/sprint action
```

Use it for deadline questions, venue-window planning, and research sprint routing. Do not use it for general literature review unless the deadline affects submission planning.

## Portable Assumptions

This skill must work after installation by a generic agent, not only inside WeHub/Hermes.

- It requires no API key, account, database, cron, private workspace, or WeHub local state.
- The helper script uses only Python standard-library modules.
- The helper script can run from the skill directory or by absolute installed path; do not assume the agent's current working directory is the skill folder.
- If the helper script cannot run, open the radar URLs manually and follow the same source hierarchy.
- If browsing/network access is unavailable, say which parts cannot be verified and label them `unverified` or `historical_estimate`; do not invent dates.

## Source Hierarchy

Use `references/source-policy.md` when the answer affects a submission decision, a source conflicts, or a venue status is uncertain.

Short version:

1. **Radar/index first** for speed and discovery:
   - `https://mlciv.com/ai-deadlines/?sub=ML,CV,CG,NLP,RO,SP,DM,AP,KR,HCI,EDU`
   - `https://ccfddl.com/conference/deadlines_zh.xml` for structured CCFDDL RSS records
   - `https://aideadlines.org/`
   - `https://aideadlin.es/`
2. **Official source for final decisions**:
   - official conference CFP / dates page
   - OpenReview venue page or submission invitation
   - official submission site
   - official rolling-review calendar, for example ACL Rolling Review dates
3. **Never treat historical dates as confirmed current-year dates.**

## Fast Lookup Workflow

### 1. Normalize the question

Identify:

- target venues, if named;
- year;
- paper area or candidate, if provided;
- whether the user needs a quick radar answer or a submission decision.

If the user says "this paper", "today", "next two months", or asks where to submit, treat it as a planning decision and verify official sources.

### 2. Run the fast radar pass

If terminal access is available, run the helper from the skill directory:

```bash
python scripts/fetch_deadline_sources.py --query "AAAI ICLR AISTATS CLeaR WSDM" --timeout 3
```

If the current working directory is elsewhere, call the installed helper by absolute path:

```bash
python /path/to/ai-conference-deadline-radar/scripts/fetch_deadline_sources.py --query "AAAI ICLR AISTATS CLeaR WSDM" --timeout 3
```

The helper uses short timeouts, concurrent fetches, and a temp cache. It returns snippets plus `candidate_links` from radar pages to speed up official-source verification. Treat those links as leads, not final authority. Four-digit years help rank snippets and candidate links, but year-specific queries stay venue-anchored when venues are named.

The helper includes a small built-in normalizer for core venue aliases and deadline stages. It recognizes common aliases for venues such as AAAI/ICLR/AISTATS/CLeaR/WSDM/ACL/ARR/EACL/EMNLP/NeurIPS/ICML/CVPR, and canonicalizes stages such as abstract, full, supplement/code, rebuttal, notification, and camera-ready.

For CCFDDL, the helper reads the structured RSS feed and may return `structured_records` with venue, year, stage, deadline, timezone, rank/category hints, source URL, and `source_kind: "radar_hint"`. Use those records for fast table assembly and lead selection; still verify official pages before labeling a date `official_confirmed`.

Preserve helper status labels exactly. A helper record with `source_kind: "radar_hint"` stays `radar_hint` in the answer even when `source_url` points to an official-looking site. Upgrade to `official_confirmed` only after you personally inspect an official CFP/OpenReview/submission page in the current turn and can cite that inspected page as the source.

When consuming `--json`, require `helper_version: "0.1.0"` and `schema_version: "1"` before relying on field names.

By default, the helper returns in fast mode after enough higher-priority radar sources succeed. Use `--wait-all` only when diagnosing source health or when the first sources are stale, missing, or contradictory.

If terminal access is unavailable, open `mlciv/ai-deadlines` first, then use one alternate radar source only if the first source is stale, missing, or ambiguous.

### 3. Verify decision-critical venues

Only verify official pages for venues that affect the user's decision; keep the target set small, usually 3-8 venues. Record:

- official URL;
- abstract deadline;
- full paper deadline;
- supplement/code deadline;
- timezone, usually AoE / UTC-12;
- notification / rebuttal if relevant;
- status: `official_confirmed`, `historical_estimate`, `radar_hint`, or `unverified`.

### 4. Convert dates into action

Do not stop at a date list. For each candidate or venue, say:

- urgency class;
- why the venue fits or does not fit;
- missing evidence before submission;
- kill signal;
- next 7 days action.

Urgency classes:

- `P0-now`: abstract/full deadline within 30 days or already in final-prep window.
- `P1-sprint`: 30-60 days; can decide a sprint.
- `P2-mainline`: 60-120 days; useful for method/experiment maturation.
- `P3-watch`: no official CFP, too far away, or not decision-critical.

## Answer Format

Use the user's language by default; use Chinese for Gong/WeHub-facing work when the surrounding context is Chinese. Keep venue names, URLs, and status tags in English.

```markdown
**结论**：...

| Venue | Status | Abstract | Full | Supp/Code | TZ | Source | Urgency |
|---|---|---:|---:|---:|---|---|---|

**怎么排**：
1. ...
2. ...

**待核验**：
- ...
```

If asked "which conference should this paper target", use:

```markdown
**推荐窗口**：...
**不推荐窗口**：...
**缺的证据**：...
**kill signal**：...
**next 7 days**：...
```

## Hard Rules

- Do not cite `mlciv`, `aideadlines`, `aideadlin.es`, or `ccfddl` as final authority for a submission decision.
- Do not upgrade helper `source_kind: "radar_hint"` to `official_confirmed` just because the helper found an official-looking `source_url`.
- Do not merge abstract and full paper deadlines.
- Do not omit timezone.
- Do not convert historical dates into official current-year deadlines.
- Do not make an unbounded conference catalog when the user only needs 3-8 target venues.
- Do not recommend a venue only by topic label; account for evidence standard and submission package readiness.
- Do not depend on private local paths, Discord context, or WeHub state in a public-marketplace answer.
