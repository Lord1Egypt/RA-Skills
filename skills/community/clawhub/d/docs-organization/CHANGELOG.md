# Changelog

All notable changes to the `docs-organization` skill will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [1.1.0] - 2026-04-08

### Added
- Step 0: Root-level noise audit — clean non-doc clutter before restructuring
- Multi-Repo / Monorepo Workspace template with umbrella vs repo-specific doc rules
- Migration checklist: snapshot before/after counts (steps 1, 14)
- Migration checklist: check implicit references before moving files (steps 6, 8)
- Anti-pattern: flat `archive/` dumping ground

### Changed
- Trimmed `description` frontmatter for conciseness (~500 → ~350 chars)
- Migration checklist expanded from 9 to 14 steps with more actionable detail
- Recommend `rg` (ripgrep) over `grep -r` for reference checks

## [1.0.0] - 2026-04-06

### Added
- Initial release
- Project size assessment (small / medium / large)
- Directory templates for each project size
- Core principles: single source of truth, CLAUDE.md as instruction manual, organize by audience + freshness, no cross-doc mirroring
- Document metadata convention (status / audience / last_reviewed)
- Anti-patterns table
- Migration checklist (9 steps)
- CLAUDE.md doc index example
