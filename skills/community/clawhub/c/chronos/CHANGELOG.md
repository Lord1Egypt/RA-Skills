# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- End-to-end reminder chain coverage for occurrence creation, reminder persistence, immediate reminder fallback, missing-config behavior, and cleanup.
- `scripts/check_git_hygiene.sh` to fail fast when tracked `__pycache__` or `*.pyc` artifacts leak into the repo.
- `core/openclaw_cron.py` helper to centralize OpenClaw cron add/remove command construction.
- `scripts/schema_preflight.py` to verify the actual runtime DB, required tables, key constraints, duplicate occurrence groups, and invalid statuses before any schema migration.
- `scripts/migrate_legacy_entries.py` for conservative Phase-2 migration of deterministic legacy recurring/system rows from `entries` into canonical task metadata.
- `scripts/archive_legacy_entries.py` for the final conservative legacy cleanup step that marks migrated linked `entries` rows readonly+archived without deleting them.
- `tests/test_migrate_legacy_entries.py` covering deterministic link/create decisions, Meta-Review migration, and explicit manual-review quarantine for unsupported every-N-hours rows.
- `tests/test_archive_legacy_entries.py` covering readonly archive application, audit metadata, and idempotent rereads.

### Changed
- Reminder cron creation/removal now goes through a shared helper instead of duplicating argv construction.
- README verification steps now include config diagnostics, schema preflight, full test discovery, legacy cron dry-run cleanup, legacy archive dry-run/apply, and git hygiene checks.
- Phase-2 docs now document the conservative migration policy, including `legacy_entry_id` / `source` traceability and the deliberate refusal to auto-migrate unsupported cadences such as `每 4 小时 ...`.
- Legacy archive handling now treats `entries.status='archived'` as the preferred first-class archive state when the schema allows it, while still honoring `chronos_archived_*` metadata as a backward-compatible fallback for constrained old schemas.
- `todo.py` now treats archived migrated legacy rows as readonly compatibility records: live list/snapshot flows ignore them, `show` exposes the archive trail, and direct `complete` / `skip` fail closed.
- Extracted shared `core/legacy_archive.py` so archive/readonly semantics, SQL projection helpers, and operator-facing messages are defined once and reused by both `archive_legacy_entries.py` and `todo.py`.

### Fixed
- Removed previously tracked Python cache artifacts from git history going forward.
- Eliminated changelog duplication and aligned the current hardening notes with real behavior.
- `complete-overdue` now merges same-day overdue hourly special-handler batches per task so one handler run can complete multiple overdue occurrences while preserving per-occurrence merge trace metadata.

## [1.0.0] - 2026-03-16

### Added
- Initial stable release.
