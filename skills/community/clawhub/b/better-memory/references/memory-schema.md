# Better Memory V2 Schema (Native-Fusion)

## Objective

Keep OpenClaw memory native while adding structured distillation:
- L1 raw logs in `memory/YYYY-MM-DD.md`
- L2 structured summaries in `.openclaw-memory-os/l2/*.md`
- L3 weekly abstractions in managed block of `MEMORY.md`

## Typing Model

- `experience`
  - `think`, `say`, `do`
- `value`
  - `good`, `bad`
- `standard`
  - `right`, `wrong`

Legacy `preference` is migrated to `value`.

## L1 Line Format

`- [YYYY-MM-DD|M-YYYYMMDD-###|kind|axis|status|confidence|topic] statement`

Rules:
- `status`: `active`, `candidate`, `stale`, `conflicted`, `superseded`
- `confidence`: `low`, `medium`, `high`
- `topic`: short stable cluster key

## Config Schema

Stored in `.openclaw-memory-os/config.json`:
- `stale_days`
- `max_l3_per_kind`
- `min_evidence_for_l3`
- `migration_days`
- `daily_entries_soft_limit`
- `daily_review_time` (`HH:MM`)
- `weekly_rollup_day` (`MON..SUN`)
- `weekly_rollup_time` (`HH:MM`)
- `monthly_review_day` (`1..31`)
- `monthly_review_time` (`HH:MM`)
- `l1_entry_threshold` (integer)

Runtime cursor state in `.openclaw-memory-os/state.json`:
- `last_daily_review_at`
- `last_weekly_rollup_at`
- `last_monthly_review_at`
- `last_processed_l1_entry_id`

## Distillation Lifecycle

1. Daily (`run_daily_review.py`)
- Parse L1 incrementally using cursor.
- Deduplicate by normalized `(kind, topic, statement)`.
- Build/update L2 markdown + `l2/summary.json`.
- Optional stale marking when requested.

2. Weekly (`run_weekly_rollup.py`)
- Read `l2/summary.json`.
- Emit stable high-signal sections into `MEMORY.md` managed block:
  - `L3 Experience`
  - `L3 Values`
  - `L3 Standards`
- Include contradiction and stale summaries.

3. Monthly (`run_monthly_review.py`)
- Generate advisory report only:
  - conflict groups
  - bloat topics
  - redundant statements
  - stale/superseded candidates
- Also generate `monthly-YYYY-MM-plan.json` with disabled actions.
- No automatic cleanup edits until actions are explicitly enabled and applied with:
  `apply_monthly_cleanup.py --workspace . [--rerollup]`.
- Cleanup apply writes execution summary:
  - `apply-summary-YYYYMMDD-HHMMSS.md`
  - includes overview, per-action impact, and sampled entry-level changes.

## Contradiction Heuristic

- `value`: same topic contains both `good` and `bad`
- `standard`: same topic contains both `right` and `wrong`

## Migration Policy

- Smart install creates migration review and editable migration plan.
- Plan application imports only user-enabled items as `candidate`.
- Historical native memory is preserved; no destructive rewrite.

## Scheduling

`emit_cron_template.py` writes `.openclaw-memory-os/cron-template.txt` with:
- catch-up daily check (`--threshold-only`)
- daily L1 -> L2 run
- weekly L2 -> L3 rollup
- monthly advisory review
