# Changelog

All notable changes to Cron Sentinel are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); this project adheres to semantic versioning.

## [1.1.0] - 2026-05-24

Security-review fixes. No behavior change to the tool itself.

### Added
- Explicit `permissions` block in the SKILL.md frontmatter (shell execution, state-file read/write under `~/.cron-sentinel/`, the `CRON_SENTINEL_STATE` env var, and no network) so the skill's real capabilities are visible to the permission model and to reviewers instead of being implicit in the code.
- "Permissions & data" section documenting exactly what the skill touches, plus a secrets warning that `wrap` stores the last ~2000 chars of a job's output in `state.json` in plaintext (with mitigations).
- "When NOT to use" guidance to keep the skill from activating on plain scheduling requests, cron-syntax questions, and one-off reminders.

### Changed
- Tightened the description and "When to use this" triggers to scope activation to reliability / silent-failure-detection intent rather than every mention of scheduling.

## [1.0.0] - 2026-05-23

Initial release.

### Added
- `wrap` command: runs a scheduled command and records each run (start, end, exit code, duration, output tail) to a state file, with configurable retries (exponential backoff) and a per-attempt timeout. Output is passed through transparently and the command's exit code is preserved.
- `check` command: watchdog that flags both crashed jobs (non-zero exit) and overdue jobs (expected to have run by now but didn't), with a tunable grace window. Exits non-zero when any job is unhealthy so it can drive an alert.
- `status` command: human-readable table of every tracked job — last run, health, and next expected time.
- `crontab` command: prints a ready-to-paste wrapped crontab line plus a watchdog line, with correct shell quoting.
- Human-duration parsing for cadence (`30m`, `12h`, `1d`, `1w`) powering silent-failure detection.
- UTC-based timestamps and atomic state writes for correctness across timezones, DST, and concurrent runs.
- Zero dependencies: pure Python standard library. No API key or external service.
