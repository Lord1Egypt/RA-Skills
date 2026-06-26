# Evals

This directory holds machine-readable eval inputs, thresholds, taxonomy data, and saved baselines for `kai-business-blueprint`.

## Files

- `export-integrity-thresholds.json` — numeric thresholds for geometry-sensitive integrity checks
- `defect-taxonomy.json` — canonical defect categories used by tests and eval fixtures
- `export-scoring-schema.json` — minimal scoring/output schema for export eval runs
- `blueprint-skill-prompts.csv` — agent-agnostic captured-run skill eval case manifest
- `skill-run-rubric.schema.json` — structured rubric schema for qualitative blueprint style checks
- `skill-eval-implementation-plan.md` — implementation plan, baseline score, verification, and release notes for the v0.16.2 skill eval release

## Skill Evals

Captured-run skill evals score each case across four 25-point categories:

- Outcome: expected blueprint/projection/export artifacts exist and validate.
- Process: the run followed the business-blueprint workflow and read the relevant references.
- Style: the blueprint uses the requested industry/type, has semantic density, and passes a rubric.
- Efficiency: the trace stays within shell command, token, wall-time, and retry budgets.

Run the default offline baseline:

```bash
python3 scripts/run-skill-evals.py --root . --runner fixture
```

The default runner is fixture-only and does not invoke Codex, Claude, Qoder, OpenClaw, model APIs, or the network. To score an external run, first convert it into the normalized trace schema, then run:

```bash
python3 scripts/run-skill-evals.py --root . --runner trace --case-id <case-id> --normalized-trace <trace.json>
```

Current saved baseline:

- `baselines/2026-05-17-skill-evals-fixture.json`
- Average score: `99.67`
- Result: `6 passed, 0 failed, 0 incomplete`

## Fixtures

- `fixtures/route-freeflow.json` — generic graph that should stay on `freeflow`
- `fixtures/route-architecture.json` — categorized architecture graph that should resolve to `architecture-template`
- `fixtures/route-evolution.json` — dated staged flow that should resolve to `evolution`

## Usage

- Route tests read these fixtures to keep export-family decisions stable.
- Integrity tests should reference taxonomy ids instead of inventing one-off failure labels.
- Human-readable failure maps, if needed later, should be generated from these files and test references rather than hand-maintained as the source of truth.
