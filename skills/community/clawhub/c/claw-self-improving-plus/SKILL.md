---
name: claw-self-improving-plus
description: Turn raw mistakes, corrections, discoveries, and repeated decisions into structured learnings and promotion candidates. Use when the user wants a conservative self-improvement workflow that captures lessons, scores reuse value, deduplicates similar learnings, drafts anchored candidate patches for SOUL.md, AGENTS.md, TOOLS.md, or MEMORY.md, reviews them through an approval step, and keeps human control before any long-term file edits.
---

# Claw Self Improving Plus

Build a conservative learning pipeline. Optimize for signal, not clutter.

## Core stance

Do not auto-rewrite long-term memory or behavior files by default.

Use this flow:
1. Capture raw learning candidates.
2. Normalize them into a structured schema.
3. Score each item for promotion value.
4. Detect duplicates or merge candidates.
5. Consolidate repeated learnings into stronger records.
6. Build a prioritized learning backlog.
7. Draft anchored candidate patches.
8. Review patches with human approval.
9. Apply only approved patches.

## Learning types

Use these types:
- `mistake`: the agent did something wrong
- `correction`: the user corrected a wrong assumption or behavior
- `discovery`: a useful fact about environment, tools, preferences, or workflow
- `decision`: a durable preference, policy, or chosen design
- `regression`: a known failure mode that should not recur

## Minimal record schema

Store each learning candidate as JSON with these fields:
- `id`: stable slug or timestamped id
- `timestamp`
- `source`
- `type`
- `summary`
- `details`
- `evidence`
- `confidence`
- `reuse_value`
- `impact_scope`
- `promotion_target_candidates`
- `status`
- `related_ids`

Default enums:
- `confidence`: `low|medium|high`
- `reuse_value`: `low|medium|high`
- `impact_scope`: `single-task|project|workspace|cross-session`
- `status`: `captured|scored|merged|promoted|rejected`

## Routing rules

Promote by destination, not vibes:
- `SOUL.md`: durable style, personality, voice rules
- `AGENTS.md`: operating rules, workflows, safety/process lessons
- `TOOLS.md`: environment-specific commands, paths, model/tool preferences
- `MEMORY.md`: important long-term facts about user, projects, decisions, history
- daily/raw store only: low-confidence or highly local observations

If a learning does not clearly deserve promotion, keep it in the raw log.

## Scoring heuristic

Score each record on five dimensions:
1. `reuse_value`: will this help again?
2. `confidence`: how well supported is it?
3. `impact_scope`: how broadly does it matter?
4. `promotion_worthiness`: should it become a lasting rule or memory?
5. `promotion_target_candidates`: where should it go if promoted?

Use this practical rubric:
- High promotion priority: repeated mistake, explicit user preference, environment fact that breaks tasks, regression with real cost
- Medium priority: useful workflow pattern seen more than once
- Low priority: one-off trivia, speculative interpretation, emotional noise, temporary state

## Anchored patch generation

Prefer anchored insertion or exact replacement over blind append.

Each patch may contain:
- `target_file`
- `anchor`
- `insert_mode`
- `old_text`
- `new_text`
- `suggested_entry`
- `approved`
- `review_status`

Use exact replacement when the old text is known.
Use anchored insertion when the destination section is known.
Use append only as fallback.

## Learning store layout

Use a stable `.learnings/` structure. See `references/learning-store-layout.md`.

Recommended files:
- `.learnings/inbox.jsonl`
- `.learnings/scored.jsonl`
- `.learnings/merge.json`
- `.learnings/patches.json`
- `.learnings/apply-report.json`
- `.learnings/archive/`

## Default workflow

### 1. Capture

Append raw learnings into `.learnings/inbox.jsonl`.

Use `scripts/capture_learning.py` to create normalized records.

### 2. Score

Run `scripts/score_learnings.py` on the inbox or a batch export.

### 3. Review duplicates

Run `scripts/merge_candidates.py` to group likely duplicates.

### 4. Draft patches

Run `scripts/draft_patches.py` to produce anchored reviewable patch candidates.

### 5. Review

Use `scripts/review_patches.py` to list, approve, reject, or skip candidates.

Examples:

```bash
python scripts/review_patches.py .learnings/patches.json list
python scripts/review_patches.py .learnings/patches.json act --index 1 --action approve
python scripts/review_patches.py .learnings/patches.json act --index 2 --action reject --note "too vague"
```

### 6. Apply only after approval

Run `scripts/apply_approved_patches.py`.

This script only applies entries explicitly approved.
It validates allowed targets, supports `--dry-run`, skips duplicate entries already present, and prefers exact replacement, then anchored insertion, then append fallback.

## Output style

When reporting results, use this structure:
- `new_candidates`: count
- `high_priority`: count
- `merge_groups`: count
- `patch_candidates`: short bullet list
- `needs_human_review`: yes

## Resources

### References
- Scoring rubric: see `references/scoring-rubric.md`
- Patch target guide: see `references/promotion-targets.md`
- Learning store layout: see `references/learning-store-layout.md`

### Scripts
- `scripts/capture_learning.py`
- `scripts/score_learnings.py`
- `scripts/merge_candidates.py`
- `scripts/draft_patches.py`
- `scripts/detect_patch_conflicts.py`
- `scripts/consolidate_learnings.py`
- `scripts/build_backlog.py`
- `scripts/age_backlog.py`
- `scripts/review_backlog.py`
- `scripts/check_existing_promotions.py`
- `scripts/review_patches.py`
- `scripts/render_review.py`
- `scripts/apply_approved_patches.py`
- `scripts/archive_batch.py`
- `scripts/run_pipeline.py`
