# Chronos historical cleanup note — 2026-03-26

## Scope
Focused only on low-risk historical leftovers in `/home/ubuntu/.openclaw/workspace/todo.db`:
- orphan `periodic_occurrences` whose parent task no longer exists
- `cycle_type='once'` tasks with `start_date IS NULL`

## Safe normalization rule
1. **Orphan occurrences**: delete them. They have no parent task, so they cannot represent valid live scheduling state.
2. **Once + NULL start_date**:
   - if exactly one occurrence exists, set `start_date` to that occurrence date
   - if no occurrence exists but `end_date` exists, set `start_date = end_date` (legacy residue where `end_date` was carrying the scheduled date)
   - otherwise leave untouched for manual review

## Current workspace findings before apply
- Orphan occurrences: 4
  - `253` → missing `task_id=43`
  - `271` → missing `task_id=19`
  - `358` → missing `task_id=175`
  - `362` → missing `task_id=178`
- `once` tasks with `NULL start_date`: 4
  - `171 华夏银行能量驿站抢购永辉` → one historical occurrence on `2026-03-20`, safe to backfill
  - `172 厦e站周五抢券` → no occurrence, `end_date=2026-03-27`, safe to normalize to `start_date=2026-03-27`
  - `173 抓厦e站数据` → no occurrence, `end_date=2026-03-26`, safe to normalize to `start_date=2026-03-26`
  - `174 工银e生活小程序周五大转盘` → no occurrence, `end_date=2026-03-27`, safe to normalize to `start_date=2026-03-27`

## Added tooling
- `scripts/normalize_historical_residues.py`
  - dry-run by default
  - supports `--apply` and `--json`
  - intentionally leaves ambiguous residues untouched
- `tests/test_normalize_historical_residues.py`

## Recommended commands
```bash
python3 skills/chronos/scripts/normalize_historical_residues.py --db /home/ubuntu/.openclaw/workspace/todo.db
python3 skills/chronos/scripts/normalize_historical_residues.py --db /home/ubuntu/.openclaw/workspace/todo.db --apply
```
