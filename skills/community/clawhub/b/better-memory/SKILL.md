---
name: better-memory
description: One-shot smart installation and ongoing maintenance for a native OpenClaw memory stack with L1 daily logs (`memory/YYYY-MM-DD.md`), L2 sidecar summaries, and L3 weekly rollups in `MEMORY.md`. Use when installing memory capability, migrating legacy memory safely, capturing typed memory (`experience`/`value`/`standard`), running daily or weekly distillation, or generating monthly conflict/bloat review reports.
metadata: {"openclaw":{"requires":{"bins":["python3"]},"config":{"stateDirs":[".openclaw-memory-os"],"example":"state_dir = \".openclaw-memory-os\""}}}
---

# Better Memory V2

## Smart Install (Recommended)

Run once to inject memory capability additively and generate migration + schedule artifacts:

`python3 skills/better-memory/scripts/smart_install.py --workspace .`

Supported install customization:
- `--daily-time HH:MM` (default `22:00`)
- `--weekly-day MON..SUN` (default `SUN`)
- `--weekly-time HH:MM` (default `20:00`)
- `--monthly-day 1..31` (default `1`)
- `--monthly-time HH:MM` (default `10:00`)
- `--entry-threshold N` (default `8`)

## Memory Layers

- L1 (native): `memory/YYYY-MM-DD.md`
- L2 (sidecar): `.openclaw-memory-os/l2/{experience,value,standard}.md`
- L3 (native): managed block in `MEMORY.md`

Typed taxonomy:
- `experience`: `think`, `say`, `do`
- `value`: `good`, `bad`
- `standard`: `right`, `wrong`

## Commands

- Capture L1 typed memory:
  `python3 skills/better-memory/scripts/capture_memory.py --workspace . --kind <experience|value|standard> --axis <axis> --topic "<topic>" --statement "<statement>"`
- Daily review (L1 -> L2):
  `python3 skills/better-memory/scripts/run_daily_review.py --workspace .`
- Weekly rollup (L2 -> L3):
  `python3 skills/better-memory/scripts/run_weekly_rollup.py --workspace .`
- Monthly advisory review (no auto cleanup):
  `python3 skills/better-memory/scripts/run_monthly_review.py --workspace .`
- Apply approved monthly cleanup actions:
  `python3 skills/better-memory/scripts/apply_monthly_cleanup.py --workspace . --rerollup`
  - This command also writes an apply summary in `.openclaw-memory-os/reviews/apply-summary-*.md`.
- Emit cron template:
  `python3 skills/better-memory/scripts/emit_cron_template.py --workspace .`
- Legacy migration plan prepare/apply:
  - `python3 skills/better-memory/scripts/promote_legacy_memory.py --workspace . --prepare`
  - `python3 skills/better-memory/scripts/promote_legacy_memory.py --workspace . --apply`

Compatibility command:
- `python3 skills/better-memory/scripts/refine_memory.py --workspace .`
  - Runs daily review then weekly rollup in one command.

## Installation Policy

- Preserve existing `AGENTS.md`, `MEMORY.md`, and daily logs.
- Write only managed blocks in `AGENTS.md`, `MEMORY.md`, and optional `HEARTBEAT.md`.
- Keep sidecar artifacts outside native `memory/` so `memory_search` behavior stays clean.
- Generate migration review and editable migration plan; do not auto-import legacy lines unless enabled.

## Monthly Cleanup Policy

- Monthly script only produces a report and suggested actions.
- Monthly script also produces a disabled-by-default cleanup plan JSON.
- Do not auto-delete or auto-rewrite memory on monthly review.
- Resolve conflicts and bloat with user confirmation, enable selected plan actions, then apply.

## References

Read `references/memory-schema.md` for schema and lifecycle details.
