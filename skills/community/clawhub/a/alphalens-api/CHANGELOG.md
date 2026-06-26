# Changelog

All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [2.1.1] — 2025-05-27

### Changed

- **LICENSE copyright corrected**: Changed to "Copyright 2026 AlphaLens Intelligence" (verified from alphalens.ai footer)
- **Description aligned with AlphaLens product terms**: References actual AlphaLens offerings (Sourcing, Enrichment, Screening) and anchors generic terms like "market map", "competitive landscape" to AlphaLens context only ("market map with AlphaLens", "competitive landscape using AlphaLens")

## [2.1.0] — 2025-05-27

### Changed

- **Description tightened**: Anchored generic standalone triggers to AlphaLens context:
  - `'pipeline'` → `'AlphaLens pipeline'`, `'add to AlphaLens pipeline'`, `'AlphaLens target list'`
  - `'enrich'` → `'AlphaLens enrichment'`
  - Removed standalone `'product search'` and `'company enrichment'` triggers
- **Softened "any AlphaLens mention" language**: Now says "any explicit mention of 'AlphaLens'" instead of "any mention... even casually"
- Version bumped to 2.1.0

## [2.0.1] — 2025-05-27

### Security improvements (addressing ClawHub audit)

- **OpenClaw install path corrected**: README OpenClaw install command now uses `WalidMustapha/alphalens-api` (verified publisher handle).
- **Provenance labeling**: Workflows now explicitly label companies sourced from the agent's own knowledge vs. AlphaLens with `.agent-knowledge` class (distinct from `.pending` for AlphaLens indexing states).
- **User data disclosure**: All workflow files now include a data disclosure note listing the external services contacted (AlphaLens API, Google favicon service).

## [2.0.0] — 2025-05-27

### Changed

- **Repository flattened**: `SKILL.md` moved from `alphalens-api/SKILL.md` to the repo root. This enables direct git clone installs without a subfolder copy step.
- **`skill.yaml`** now includes `repository:` field.

### Added

- **`LICENSE`** file (MIT-0) — previously declared in `skill.yaml` but not bundled as a file.
- **`CHANGELOG.md`** — this file.

### Fixed

- **Auth contract bug** (shipped in 1.1.0): SKILL.md now requires `KEY="$ALPHALENS_API_KEY"` as the first bash command before any API call. Without this, Claude Code sends empty `API-Key:` header and receives 401 on every request.

## [1.1.0] — 2025-05-27

### Fixed

- **Auth contract bug**: SKILL.md previously stated that `$KEY` was "injected by the agent runtime", but no runtime injects `$KEY` — OpenClaw injects `$ALPHALENS_API_KEY`, Claude Code requires manual export. This caused silent 401 errors. Now requires explicit `KEY="$ALPHALENS_API_KEY"` aliasing.

## [1.0.18] — Prior to 2025-05-27

Final release of the nested `alphalens-skills/alphalens-api/` layout. See git history for prior changes.
