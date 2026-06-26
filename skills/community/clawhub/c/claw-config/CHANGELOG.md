# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — Initial release

### Added
- Seven subcommands: `whoami`, `schema`, `docs`, `diagnose`, `plan`, `apply`, `report`.
- Strict self-identification via `$OPENCLAW_AGENT_ID` (refuses to guess; fails closed).
- Static cross-agent write guard — refuses patches that touch another agent's slice.
- Docs subcommand fetches raw markdown from `docs.openclaw.ai` (Mintlify `.md` endpoints) and the full-content `llms-full.txt` corpus for keyword search.
- Per-openclaw-version cache directory layout, with auto-pruning of stale version directories on upgrade.
- Versioned backups in a dedicated directory (avoids openclaw's own rotating-backup cleanup), automatic restore-from-backup on `apply` failure.
- Cron safety gate: `apply` refuses to run under `OPENCLAW_CRON_CONTEXT=1`; read-only subcommands run anywhere; `docs` serves cache only in cron context.
- 12 structural diagnose checks; `diagnose` exits `3` on any `fail`.
- `--max-age <hours>` and `--refresh` for caller-controlled docs cache freshness.
- Argparse `prog=` follows the invoking symlink name so aliases (e.g. `oclm`) display correctly in `--help`.
