# Changelog

## [Unreleased]

### Fixed
- `audit`'s dominant-space walk found no roots (root detection used `_parent_key(...) is None`, which never matches a real path), so `audit` produced zero dominant-space findings. Root detection now checks whether a node's parent is absent from the scan set.
- Test portability: the five `windows-native` tests are now skipped off-Windows, and the dominant-space reporting test no longer depends on the host temporary path (Linux: 37 passed, 5 skipped).

### Added
- `examples/`: reproducible tiny demo (`make-sample-data.sh`, `demo-config.json`) and a committed `demo-audit/` bundle showing a real dominant-space finding.

## [0.1.0] - 2026-09-19
### Added
- Public cross-platform `DirStat_Skill` repository layout for Windows and Linux hosts.
- Native Windows scan engine and generic CLI commands: `scan`, `summarize-export`, and `audit`.
- Recursive review dossier outputs with `review_report.md`, `review_candidates.csv`, and `candidates.json`.
- Public skill packaging with `SKILL.md` and `AGENTS.md` for agent-driven usage.

### Changed
- Renamed the public identity from `safe-delete-advisor-skill` to `DirStat_Skill`.
- Renamed the Python package from `safe_delete_advisor` to `dirstat_skill`.
- Reframed all public docs and outputs around review-only language instead of cleanup automation.

### Fixed
- Added hard-fail CLI guardrails for invalid engine/platform/path combinations.
- Aligned OpenClaw skill symlinks to the canonical repository path.

### Safety
- The tool is read-only and never removes files automatically.
