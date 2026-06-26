# fitbit-connector

`fitbit-connector` is a **separate project repo** in Joao's OpenClaw ecosystem.

It provides Fitbit data access, sync, integrity checks, and local health-data tooling for OpenClaw.

It is **not** the canonical repo for Joao's whole OpenClaw system workspace.

## What this repo is for

This project exists to provide reliable Fitbit/health data tooling that OpenClaw can use safely.

Current responsibilities include:
- Fitbit OAuth and token handling
- Fitbit sync/cache operations
- integrity and parity checks
- backup/validation/rollback-aware pipeline runs
- unified local health database tooling
- training ↔ health correlation tooling

This repo does **not** perform coaching decisions. It exposes clean data tools so OpenClaw can reason at a higher level.

> ⚠️ **First-run requirement:** complete Fitbit OAuth once before sync/fetch commands can return real data.

## Relationship to the ecosystem

In the current target architecture:
- `joaodriessen/openclaw` = Joao's private OpenClaw system workspace repo
- `joaodriessen/openclaw-mission-control` = dashboard/control-plane product
- `joaodriessen/fitbit-connector` = this repo
- `joaodriessen/icloud-caldav-openclaw-skill` = iCloud Calendar skill

## What this repo does not own

This repo does not own:
- Joao's full OpenClaw workspace
- unrelated workspace automation/orchestrators
- generic OpenClaw runtime state
- non-Fitbit skills

## Structure

- `SKILL.md` — runtime behavior/instructions for the assistant
- `scripts/` — executable tool scripts
- `references/` — env/schema docs
- `_meta.json` — local skill metadata (slug/version)

## Core command

```bash
python3 scripts/fitbit_tools.py schema
```

Use this to inspect available commands and supported metric fields.

## Docs-first capability contract (recommended)

Prefer deterministic contract output over probe loops:

```bash
python3 scripts/fitbit_tools.py auth-status
python3 scripts/fitbit_tools.py capability-matrix
```

This gives a static scope/domain matrix from `references/capability_contract.json` and current token scopes.

Broad probing remains available for diagnostics only:

```bash
python3 scripts/fitbit_tools.py discover-capabilities --days 7 --sleep-ms 500 --stop-on-429
```

## Max-scope configuration + reauth

Set `FITBIT_SCOPES` to the full supported scope set:

`activity cardio_fitness electrocardiogram heartrate irregular_rhythm_notifications location nutrition oxygen_saturation profile respiratory_rate settings sleep social temperature weight`

If scopes change, reauthorize once:

```bash
python3 scripts/fitbit_auth.py auth-url
# Open URL, approve scopes, copy code+state from redirect URL
python3 scripts/fitbit_auth.py exchange --code "<CODE>" --state "<STATE>"
python3 scripts/fitbit_tools.py auth-status
```

## Fail-safe pipeline (backup + validation + rollback)

A hardened pipeline now runs sync + import with automatic snapshots and validation:

```bash
python3 scripts/fitbit_pipeline.py --days-backfill 3
```

What it guarantees per run:
- acquires a lock (prevents overlapping writes)
- snapshots Fitbit DB + unified DB + tokens before ingest
- syncs Fitbit range into cache and imports into unified DB
- validates freshness, row parity, and degraded-quality rows
- auto-rolls back to snapshots on validation failure
- prunes older pipeline snapshots after successful runs (keeps all snapshots from the most recent day; for older days keeps only the latest snapshot)
- writes an auditable run report in `runs/fitbit_pipeline_<timestamp>.json`

Backups are stored under `backups/pipeline/<timestamp>/`.
Use `--no-prune-backups` to disable retention temporarily or `--keep-recent-backup-days N` to widen the keep window.

## Unified local health database (SQLite)

A local SQLite layer is available for rate-limit-safe storage and cross-source unification.

- DB path (default): `assets/health_unified.sqlite3`
- Script: `scripts/health_db.py`
- Commands:
  - `init`
  - `import-fitbit-cache --start YYYY-MM-DD --end YYYY-MM-DD`
  - `import-apple-export --xml /path/to/export.xml [--limit N]`
  - `aggregate-apple-daily [--start YYYY-MM-DD --end YYYY-MM-DD]`
  - `stats`

Example:

```bash
python3 scripts/health_db.py init
python3 scripts/health_db.py import-fitbit-cache --start 2026-03-10 --end 2026-03-15
python3 scripts/health_db.py import-apple-export --xml assets/apple_health_export/unzipped/apple_health_export/export.xml
python3 scripts/health_db.py aggregate-apple-daily
python3 scripts/fitbit_tools.py unified-status
python3 scripts/fitbit_tools.py unified-fetch-latest --days 14 --source best
python3 scripts/health_db.py stats
```

## Training ↔ health correlation (v1)

Local-first correlation is available via `scripts/training_correlation.py` and wrapped in `fitbit_tools.py`.

Typical flow:

```bash
python3 scripts/fitbit_tools.py training-sync-calendar --json /path/to/google_calendar_events.json
python3 scripts/fitbit_tools.py training-health-status
python3 scripts/fitbit_tools.py training-health-window --days 28
python3 scripts/fitbit_tools.py training-health-correlation --days 90
```

This builds:
- `training_sessions`
- `training_daily_summary`
- joined view `v_training_health_daily` in `assets/health_unified.sqlite3`

See `../docs/training-health-correlation-v1.md` for details.

## Suggested OpenClaw cron

A production-safe schedule is now installed:
- Job: `fitbit:pipeline-failsafe`
- Cron: `10 6,12,18,23 * * *` (Europe/Amsterdam)
- Model: `CODEX`
- Command: `python3 /Users/joao/.openclaw/workspace/fitbit-connector/scripts/fitbit_pipeline.py --days-backfill 3`

To inspect:
```bash
openclaw cron list --json
```

## Publish (ClawHub)

From workspace root:

```bash
clawhub publish fitbit-connector --slug fitbit-connector --version 1.0.0 --name "Fitbit Connector"
```

> Requires prior `clawhub login`.
