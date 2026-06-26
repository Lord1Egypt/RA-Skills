# Changelog

All notable changes to Download Guard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.4.0] - 2026-05-26

### Added
- Path availability check: drive missing or path not writable -> BLOCK (exit code 2), never silently fall back to C:
- Config protection: read-back verify after writing config.md, backup old values before changing DOWNLOAD_ROOT
- Extended trigger words: `cargo install`, `go install`, `uv pip install`, `pnpm add -g`, `bun install -g`
- Extended cache scanning: pnpm, bun, cargo, go, uv, nvm, HuggingFace, Ollama, pip --user
- `check path` and `reset config` natural language commands
- Known limitations documented: nvm, Docker, build artifacts

### Changed
- `check-space.ps1`: rewritten with 3-tier path validation (drive exists -> writable -> auto-create)
- Exit code 2 now means "path unavailable" (distinct from exit code 1 "space too low")

### Fixed
- `scan-tool-cache.ps1`: version label updated from v3 to v5

## [5.3.0] - 2026-05-26

### Added
- Download size awareness: warn if >50% of free space, block if exceeds free space
- Duplicate download detection: check if file already exists before downloading
- venv recognition: `pip install` inside active virtual environment does not trigger
- Smart default disk recommendation: first-time setup recommends largest non-C: drive
- Download verification: check file exists at expected path after download
- Precise description with English trigger words and common scenarios
- `reference.md` for detailed information (keeps SKILL.md under 500 lines)

### Changed
- SKILL.md slimmed from 459 lines to 275 lines (details moved to reference.md)

## [5.2.0] - 2026-05-26

### Added
- Download transparency rules: every download must tell user the location and status
- Log auto-cleanup: entries older than `LOG_RETENTION_DAYS` auto-archive, archives exceeding `LOG_ARCHIVE_MAX_MB` auto-delete
- Path ask strategy: rules for when to ask vs when to inform (first setup = ask, daily = inform, env change = must inform)

### Changed
- `log-download.ps1`: added auto-archive logic with configurable retention
- `config.md`: added `LOG_RETENTION_DAYS` and `LOG_ARCHIVE_MAX_MB` parameters

### Fixed
- `migrate-cache.ps1`: removed residual reference to deleted `setup-wizard.ps1`

## [5.1.0] - 2026-05-26

### Removed
- `config.local.md` — two-tier config was too complex, merged into single `config.md`
- `scripts/setup-wizard.ps1` — replaced by Agent-guided first-time setup via conversation

### Changed
- All scripts unified to read only `config.md` (no more localConfig priority)
- First-time setup is now a pure Agent conversation, no external scripts

## [5.0.0] - 2026-05-26

### Added
- Public-ready restructuring: removed hardcoded paths, added setup wizard
- Two-tier config (later removed in v5.1)
- Setup wizard script (later removed in v5.1)

## [4.0.0] - 2026-05-26

### Added
- Three path types: A (cache/safe), B (install dir/needs PATH), C (file storage/safe)
- PATH linkage check when changing npm prefix or conda envs
- Warning for spaces in tool paths (npm prefix, conda envs)

## [3.0.0] - 2026-05-26

### Added
- Precise trigger words with MUST/DO NOT rules
- Status card output format
- Execution protocol with numbered steps
- Natural language command table

## [2.0.0] - 2026-05-26

### Added
- `scan-tool-cache.ps1`: scan npm/pip/yarn/conda cache locations
- `migrate-cache.ps1`: one-click cache migration to non-C: drive

### Fixed
- PowerShell 5.1 compatibility (encoding, boolean filtering)

## [1.0.0] - 2026-05-26

### Added
- Basic three-layer protection: directory locking, space check, download logging
- `check-space.ps1`: disk space verification
- `log-download.ps1`: download history tracking
