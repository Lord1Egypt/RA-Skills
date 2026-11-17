# Changelog

All notable changes to `design-guide` are documented here. The project follows Semantic Versioning from `v0.1.0` onward.

## [Unreleased]

## [0.1.2] - 2026-08-09

### Changed

- Skill display name renamed from "F Design" to "Design Guide" for clarity.
- Configuration directory consistently uses `.design-guide/` across all references.

### Added

- Locale contract and message catalogs for `en` and `zh-CN`.
- Localized CLI help and human-readable status/error output with English fallback.
- Bilingual maintainer and release documents plus catalog parity tests.

## [0.1.1] - 2026-08-07

### Fixed

- Gitee tag synchronization no longer force-updates the mirror's `main` branch.
- Secret scanning checks README, workflow, and test files instead of skipping whole files, and works from non-Git source directories.
- `design-guide-doctor.py` rejects drift between `VERSION` and `design-guide.json`.
- Provider smoke tests refuse to run when release version sources disagree.

## [0.1.0] - 2026-08-07

### Added

- Level 0/1/2 design-depth routing with explicit user confirmation for exploratory work.
- Automatic presentation of standalone HTML and managed review servers.
- Machine-validated implementation contracts with approval evidence, flows, states, accessibility, performance, data, and visual gates.
- Project intelligence, managed preview, screenshot capture, visual diff, and strict browser QA scripts.
- Existing product/page design evaluation with evidence, scorecards, priorities, tradeoffs, acceptance criteria, and before/after comparison.
- Scope Gate rules that prevent unrequested mobile, accessibility, implementation, redesign, or publishing work and forbid inherited side goals.
- Behavior-level review fixtures for the historical mobile/WeChat context-leak regression.
- Specialized review templates for data tables, dashboards, complex forms, mobile navigation, and high-risk batch operations.
- Cross-AIDE version manifest, digest-based synchronization, and `design-guide-doctor.py` for Codex, Claude Code, Cursor, and Qwen Code.
- Three deterministic end-to-end product journey checks.
- Depth Stack visual identity and bilingual documentation.

### Changed

- CI secret scanning now uses boundary-aware token detection to avoid false positives such as ordinary `task-based` prose.
- Cross-AIDE sync excludes repository workflows, promotional artifacts, caches, private profiles, and generated review files.

### Known Limitations

- Provider-side invocation tests are not automatic because they can consume external model quota and require explicit authorization.
- Browser QA requires Playwright/Chromium; accessibility and Lighthouse gates require their declared local tools.
- Design quality still depends on the host model following the skill and on sufficient product context/evidence.
