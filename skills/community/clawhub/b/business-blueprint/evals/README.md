# Export Evals

This directory holds machine-readable export quality inputs, thresholds, and taxonomy data for `kai-business-blueprint`.

## Files

- `export-integrity-thresholds.json` — numeric thresholds for geometry-sensitive integrity checks
- `defect-taxonomy.json` — canonical defect categories used by tests and eval fixtures
- `export-scoring-schema.json` — minimal scoring/output schema for export eval runs

## Fixtures

- `fixtures/route-freeflow.json` — generic graph that should stay on `freeflow`
- `fixtures/route-architecture.json` — categorized architecture graph that should resolve to `architecture-template`
- `fixtures/route-evolution.json` — dated staged flow that should resolve to `evolution`

## Usage

- Route tests read these fixtures to keep export-family decisions stable.
- Integrity tests should reference taxonomy ids instead of inventing one-off failure labels.
- Human-readable failure maps, if needed later, should be generated from these files and test references rather than hand-maintained as the source of truth.
