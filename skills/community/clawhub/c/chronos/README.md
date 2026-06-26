# Chronos

Chronos is a lightweight recurring-task engine backed by `periodic_tasks` + `periodic_occurrences`, with temporary compatibility for legacy `entries` rows.

## Phase-1 data model direction

- `periodic_tasks` is the canonical definition table for scheduled work.
- `periodic_occurrences` is the canonical execution/reminder table.
- `entries` remains only for inbox-style one-shot notes and legacy compatibility.
- Scheduled `once` tasks with an explicit `start_date` now use canonical task storage.
- `monthly_dates` is a supported cycle type.
- `hourly` is a supported cycle type, with `interval_hours` + `time_of_day` anchor semantics.
- `monthly_n_times` can now run on either a weekday cadence (`weekday=0..6`) or a daily cadence (`weekday=NULL`) while still enforcing a monthly completion quota.
- Special system behaviors should live in explicit task metadata (`special_handler`) instead of free-text regex whenever possible.

## Quick examples

```bash
python3 skills/chronos/scripts/todo.py add "一次性计划任务" \
  --cycle-type once \
  --start-date 2026-03-27 \
  --time 10:00

python3 skills/chronos/scripts/todo.py add "同步 subagent 记忆" \
  --cycle-type hourly \
  --interval-hours 4 \
  --time 08:00 \
  --task-kind system \
  --special-handler sync_subagent_memory

python3 skills/chronos/scripts/todo.py add "Meta-Review fallback" \
  --cycle-type daily \
  --time 02:00 \
  --task-kind system \
  --special-handler meta_review_fallback

python3 skills/chronos/scripts/migrate_legacy_entries.py --db /home/ubuntu/.openclaw/workspace/todo.db
python3 skills/chronos/scripts/migrate_legacy_entries.py --db /home/ubuntu/.openclaw/workspace/todo.db --apply
python3 skills/chronos/scripts/archive_legacy_entries.py --db /home/ubuntu/.openclaw/workspace/todo.db
python3 skills/chronos/scripts/archive_legacy_entries.py --db /home/ubuntu/.openclaw/workspace/todo.db --apply
python3 skills/chronos/scripts/normalize_historical_residues.py --db /home/ubuntu/.openclaw/workspace/todo.db
python3 skills/chronos/scripts/normalize_historical_residues.py --db /home/ubuntu/.openclaw/workspace/todo.db --apply
python3 skills/chronos/scripts/todo.py complete-overdue --dry-run
python3 skills/chronos/scripts/schema_preflight.py
```

## Hourly cadence semantics

`cycle_type=hourly` is day-scoped and canonical.

Required fields:
- `interval_hours`: integer 1-24
- `time_of_day`: anchor `HH:MM`

Expansion rule for each active day:
- start from the anchor minute
- emit all same-minute slots every `interval_hours`
- include earlier same-day slots too, so `--interval-hours 4 --time 08:00` expands to:
  - `00:00, 04:00, 08:00, 12:00, 16:00, 20:00`

This is conservative and matches the legacy `每 4 小时：同步 subagent 记忆` expectation without introducing cross-day offset state.

`sync_subagent_memory` now reads a file-backed ledger at `memory/subagent_sync_ledger.json` via `memory_manager.py pending-subagents`, so the hourly handler no longer guesses session ids from all memory. Ledger schema/status/pending semantics are centralized in `scripts/subagent_sync_ledger.py`, and OpenClaw auto-records completed subagent sessions into that ledger on the subagent completion path. `memory_manager.py record-subagent <session_id>` remains available only for manual backfill. Successful syncs are marked handled with `mark-subagent-synced`, and failures remain pending with an updated error trail.

When `complete-overdue` processes multiple overdue hourly occurrences for the same task on the same day and that task has a `special_handler`, Chronos now runs the handler once for that task/day batch, then marks every overdue occurrence completed with `completion_mode=fallback_handler_merged` and a per-occurrence `special_handler_result` trail (`merge_key`, merged index/count, source occurrence).

## Monthly quota over daily cadence

For tasks like `福建农行秒杀京东卡`, the intended semantic is not plain `daily`; it is:
- remind on a daily cadence while the month quota is still unused
- once any occurrence is completed, consume the monthly quota
- auto-complete the rest of that month's pending/reminded occurrences so no more reminders fire
- resume naturally after the monthly counter resets on the next month boundary

This is represented as:
- `cycle_type=monthly_n_times`
- `n_per_month=1`
- `weekday=NULL` to mean daily cadence instead of weekly cadence

## Legacy migration policy

Phase 2+ adds `scripts/migrate_legacy_entries.py` for conservative migration out of `entries`.

What it will do automatically:
- link obvious legacy rows to an already-existing canonical task by deterministic normalized name
- create an explicit `task_kind=system` + `special_handler=meta_review_fallback` task for legacy Meta-Review rows
- create an explicit `task_kind=system` + `cycle_type=hourly` + `special_handler=sync_subagent_memory` task for legacy `每 N 小时 ... memory_manager.py sync` rows
- create canonical tasks for simple bracketed recurring rows only when the schedule is deterministic

What it will not do automatically:
- ambiguous free-text rows
- unsupported every-N-hours rows without known handler semantics

Traceability is preserved through `periodic_tasks.legacy_entry_id` and `source` (`legacy_entries_linked` / `legacy_entries_migrated`).

## Final legacy archive step

After migration has linked canonical tasks, run `scripts/archive_legacy_entries.py`.

What it does:
- finds `entries` rows already linked from `periodic_tasks.legacy_entry_id`
- adds conservative archive metadata columns on `entries` if missing:
  - `chronos_readonly`
  - `chronos_archived_at`
  - `chronos_archive_reason`
  - `chronos_archived_from_status`
  - `chronos_linked_task_id`
- prefers `status='archived'` as the first-class archive marker when the live `entries` schema allows it
- still treats archive metadata as the compatibility fallback if an older constrained `entries.status` enum cannot store `archived`
- repairs partially archived rows by completing missing readonly/archive metadata
- keeps the original row in place for audit / traceability
- keeps active Chronos surfaces clean because linked rows are already excluded from live list/snapshot/overdue queries

Operational boundary:
- canonical live scheduling state remains `periodic_tasks` + `periodic_occurrences`
- legacy `entries` archive state is now interpreted by shared helper semantics: `status='archived'` first, then `chronos_archived_at` / `chronos_archive_reason` / `chronos_archived_from_status`
- Chronos does not attempt a broad live-table migration of arbitrary `entries.status` constraints; if a deployment still forbids `archived`, the archive script preserves the prior status and relies on `chronos_archived_*` metadata instead

Operational effect:
- migrated legacy rows stop looking like live legacy tasks
- `todo.py show ID<n>` still exposes the archive trail
- `todo.py complete ID<n>` / `skip ID<n>` now fail closed on readonly archived legacy rows and point operators back to the linked canonical periodic task

Recommended sequence:
1. `python3 skills/chronos/scripts/migrate_legacy_entries.py --db /path/to/todo.db`
2. `python3 skills/chronos/scripts/migrate_legacy_entries.py --db /path/to/todo.db --apply`
3. `python3 skills/chronos/scripts/archive_legacy_entries.py --db /path/to/todo.db`
4. `python3 skills/chronos/scripts/archive_legacy_entries.py --db /path/to/todo.db --apply`
5. `python3 skills/chronos/scripts/normalize_historical_residues.py --db /path/to/todo.db`
6. `python3 skills/chronos/scripts/normalize_historical_residues.py --db /path/to/todo.db --apply`

## Historical residue cleanup

`normalize_historical_residues.py` is intentionally narrow. It only touches residues that are already outside normal live semantics:

- orphan `periodic_occurrences` whose `task_id` no longer exists
- `cycle_type='once'` tasks where `start_date IS NULL` but a single canonical date can be inferred safely

Normalization rules:
- orphan occurrences are deleted
- once task with exactly one occurrence date → `start_date = that occurrence date`
- once task with no occurrence but existing `end_date` → `start_date = end_date`
- anything else stays untouched for manual review

This keeps cleanup deterministic and avoids changing active recurring behavior.
