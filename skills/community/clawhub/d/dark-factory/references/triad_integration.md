# Triad Integration Architecture

This document describes how `intent-engineering`, `dark-factory`, and `feedback-loop` work together as a three-skill pipeline.

## Overview

```
┌──────────────────┐   specification.json   ┌──────────────────┐
│ intent-          │ ─────────────────────▶ │ dark-factory     │
│ engineering      │                        │                  │
│ (The "Why")      │ ◀───────────────────── │ (The "How")      │
└──────────────────┘  updated_spec.json     └────────┬─────────┘
                                                     │
                                            outcome_report.json
                                                     │
                                                     ▼
                                            ┌──────────────────┐
                                            │ feedback-loop    │
                                            │                  │
                                            │ (The "Learn")    │
                                            └──────────────────┘
```

## Data Flow

### Stage 1 → Stage 2 (intent-engineering → dark-factory)

`intent-engineering` produces a `specification.json` that dark-factory consumes as its primary input. The specification must conform to `specification_schema.json`.

**Key fields passed:**
- `specification_id` — links all three stages together
- `behavioral_scenarios` — drives both validation and test execution
- `success_criteria.test_pass_rate` — the acceptance threshold
- `dependencies` — informs integration test scope

### Stage 2 → Stage 3 (dark-factory → feedback-loop)

`dark-factory` produces an `outcome_report.json` that feedback-loop consumes for analysis. The report must conform to `outcome_report_schema.json`.

**Key fields passed:**
- `report_id` — unique identifier for this execution
- `performance_metrics` — pass rates and timing for trend analysis
- `edge_cases` — failed behavioral scenarios become regression tests
- `failures` — unit test failures become improvement suggestions
- `cryptographic_signature` — proves report integrity

### Stage 3 → Stage 1 (feedback-loop → intent-engineering)

`feedback-loop` produces an `updated_specification.json` that feeds back into intent-engineering, activating the self-improving loop.

**Key fields passed:**
- `behavioral_scenarios` — original + new auto-generated regression tests
- `version` — bumped version number (e.g. 1.0.0 → 1.0.1)
- `success_criteria` — potentially tightened based on observed performance

## Integration Points

### Running the Full Pipeline

```bash
# Stage 1: Generate specification
python /home/ubuntu/skills/intent-engineering/scripts/orchestrator.py \
  --skill my-skill --goal "Build a weekly report generator"

# Stage 2: Execute dark factory
python /home/ubuntu/skills/dark-factory/scripts/orchestrator.py specification.json

# Stage 3: Run feedback loop
python /home/ubuntu/skills/feedback-loop/scripts/feedback_loop_orchestrator.py \
  --spec specification.json --outcome specification_outcome_report.json
```

### Using the Unified Orchestrator (recommended)

```bash
python /home/ubuntu/skills/unified-orchestrator/scripts/pipeline.py \
  --mode full --skill my-skill --goal "Build a weekly report generator"
```

## Best Practices

**Specification quality** — the dark factory is only as good as its specification. Use `specification_validator.py` before every run. Invest time in writing clear, testable behavioral scenarios with concrete input/output examples.

**Iterative improvement** — do not expect perfection on the first run. The self-improving loop is designed to accumulate edge cases and regression tests over multiple cycles, progressively raising quality.

**Shared data contracts** — all three skills share the same `specification_schema.json` and `outcome_report_schema.json`. Never modify these schemas without updating all three skills simultaneously.

**Version tracking** — always increment the specification version when the feedback-loop produces an `updated_specification.json`. This creates an auditable history of how the specification evolved.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
| :--- | :--- | :--- |
| Validation fails with "Missing required field" | Specification missing required fields | Run `specification_validator.py` and fix reported errors |
| Behavioral pass rate < target | Scenarios too strict or ambiguous | Review failed scenarios, clarify expected outputs |
| Integration tests all fail | Dependencies not registered | Add dependencies to `skill_registry.json` |
| Feedback loop alignment score < 0.7 | Goal drift between cycles | Review `shared_intent.md` and realign specification goal |
