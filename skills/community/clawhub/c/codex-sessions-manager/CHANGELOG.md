# Changelog

## 0.3.2

### Fixed

- Corrected README wording for `/side` and `/fork`: the tool detects child relationships and can operate on explicit session IDs, but it does not recursively delete child threads automatically.
- Corrected storage names in README from `logs.sqlite` and `global_state.json` to `logs_N.sqlite` and `.codex-global-state.json`.
- Updated npm package contents so linked public docs, Skill entrypoint, and Skill template are included in package builds.
- Synchronized `package-lock.json` with the published package name.
- Updated public Skill instructions to prefer the installed `codex-sessions` CLI, with repository commands kept as the development path.
- Removed stale ClawHub package contents from the clean Skill publish surface.

### Notes

- This version is a post-release cleanup for the npm, GitHub, and ClawHub publish surfaces.
- Memory-related cleanup remains intentionally unchanged.

## 0.3.1

### Added

- Added read-only root diagnostics through CLI `doctor` and MCP `inspect_root`.
- Added project grouping, date filters, and status filters.
- Added recoverable trash deletion, restore, and purge flows.
- Added cleanup preview and explicit confirmation for JSONL index rewrites.
- Added warnings for unknown global-state references.
- Added public Skill packaging through `SKILL.md` and `agents/openai.yaml`.
- Added a public Skill template under `examples/`.

### Changed

- Updated compatibility with current Codex SQLite storage, including `state_N.sqlite` and `logs_N.sqlite`.
- Synchronized README, README.zh-CN, MCP behavior, and Skill guidance.
- Hardened delete and restore coverage across JSONL indexes, raw session files, SQLite rows, global state, and shell snapshots.

### Safety

- Destructive writes require `--yes` in the CLI or `confirm=true` in MCP.
- Restore performs conflict checks before writing and has no force overwrite mode.
- Unknown global-state references are reported as warnings only.
- The project continues to avoid UI, TUI, automatic cleanup, and automatic purge behavior.
