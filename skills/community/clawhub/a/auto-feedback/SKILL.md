---
name: feedback-loop
version: 2.0.0
description: A self-improving feedback loop skill that works fully standalone OR integrates with intent-engineering and dark-factory when available. Observes any system or execution, analyzes performance, generates improvement suggestions, auto-creates regression tests, tracks goal alignment, and produces a signed improvement report.
---

# Feedback Loop (v2)

## Overview

The **`feedback-loop`** skill is a dual-mode, self-improving intelligence layer. It runs completely on its own with no external dependencies, and automatically unlocks richer analysis when `intent-engineering` or `dark-factory` are present.

**Use this skill when:**
- You want to analyze the performance of any process, script, or agent execution.
- You need prioritized improvement suggestions without running a full pipeline.
- You want to auto-generate regression tests from observed failures or edge cases.
- You need to track whether a system's behavior is drifting from its stated goals.
- You want a self-contained improvement report you can act on immediately.
- You are running the full `intent-engineering → dark-factory → feedback-loop` triad.

---

## Dual-Mode Operation

The skill detects what inputs are available and automatically selects the richest mode:

| Mode | Inputs Available | What You Get |
| :--- | :--- | :--- |
| **Standalone** | Any JSON log, plain text, or prior observation | Full analysis, suggestions, regression tests, alignment check, signed report |
| **Dark Factory Enhanced** | `outcome_report.json` from dark-factory | All standalone features + behavioral test pass rates, generated code review, security evidence |
| **Full Triad** | `outcome_report.json` + `specification.json` from intent-engineering | All enhanced features + goal alignment against original spec, updated specification for next cycle |

There is no configuration switch — the skill detects what is available and adapts automatically. **You never need to change anything to switch modes.**

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     FEEDBACK LOOP (v2)                           │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  INPUT LAYER (auto-detects mode)                            │ │
│  │                                                             │ │
│  │  Standalone:  any JSON log / plain text / prior obs        │ │
│  │  Enhanced:    + outcome_report.json (dark-factory)         │ │
│  │  Full Triad:  + specification.json (intent-engineering)    │ │
│  └───────────────────────┬─────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  OBSERVER  (observer.py)                                    │ │
│  │  Normalizes all inputs → observation.json                  │ │
│  └───────────────────────┬─────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ANALYZER  (analyzer.py)                                    │ │
│  │  Scores performance · detects regressions                  │ │
│  │  Generates suggestions · checks alignment                  │ │
│  │  Auto-creates regression tests                             │ │
│  └───────────────────────┬─────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ORCHESTRATOR  (orchestrator.py)                            │ │
│  │  Assembles signed improvement_report.json                  │ │
│  │  Produces updated_observation.json for next cycle          │ │
│  │  Optionally produces updated_specification.json            │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Standalone — any JSON log
```bash
python scripts/orchestrator.py --input my_execution_log.json --goal "Process tickets in under 2 minutes"
```

### Standalone — plain text description
```bash
python scripts/orchestrator.py --text "Script ran but missed 3 null input cases and took 4 minutes" --goal "Handle all inputs"
```

### Standalone — continuing a prior cycle
```bash
python scripts/orchestrator.py --observation observation.json
```

### Dark Factory Enhanced
```bash
python scripts/orchestrator.py --outcome outcome_report.json --goal "Achieve 98% test pass rate"
```

### Full Triad (after intent-engineering + dark-factory)
```bash
python scripts/orchestrator.py --outcome outcome_report.json --spec specification.json
```

### Run stages independently
```bash
python scripts/observer.py --input log.json --goal "..." --output observation.json
python scripts/analyzer.py --observation observation.json --output analysis.json
python scripts/orchestrator.py --analysis analysis.json --output-dir ./reports/
```

---

## Outputs

Every run produces files in the current directory (or `--output-dir`):

| File | Always Present | Description |
| :--- | :--- | :--- |
| `observation.json` | Yes | Normalized observation with extracted metrics |
| `analysis.json` | Yes | Performance score, suggestions, alignment score, regression tests |
| `improvement_report.json` | Yes | Final signed report with all findings and next steps |
| `updated_observation.json` | Yes | Updated observation for the next cycle |
| `updated_specification.json` | Full Triad only | Updated spec with new regression tests for intent-engineering |

---

## The Six-Step Internal Workflow

### Step 1 — Normalize Input
`observer.py` accepts any input format and normalizes it into a standard `observation.json`. In standalone mode it extracts metrics from JSON or text. In enhanced/triad mode it also ingests the structured fields from `outcome_report.json` and `specification.json`.

### Step 2 — Score Performance
`analyzer.py` computes a `performance_score` (0.0–1.0) from extracted metrics. It compares against the previous cycle's score (if available) to detect regressions and trends.

### Step 3 — Generate Improvement Suggestions
The analyzer produces concrete, actionable suggestions ranked `critical → high → medium → low`. Each suggestion includes a description, rationale, effort estimate, and expected impact. In triad mode, suggestions are also cross-referenced against the original specification's success criteria.

### Step 4 — Auto-Generate Regression Tests
Every failure and edge case is automatically converted into a regression test with a concrete `input` and `expected_output`. These are appended to `updated_observation.json` and (in triad mode) to `updated_specification.json`.

### Step 5 — Check Goal Alignment
The analyzer checks the observation against `references/alignment_values.json` (your organization's principles) and, in triad mode, against the original specification's stated goal. It produces an `alignment_score` (0.0–1.0) and flags any drift.

### Step 6 — Generate Signed Report
`orchestrator.py` assembles all outputs into a single `improvement_report.json` with a SHA-256 integrity digest, making every report independently verifiable.

---

## Self-Improving Loop

The skill is designed to be run repeatedly. Each run produces an `updated_observation.json` that serves as the input for the next run. Over time, the regression test suite grows, the alignment score stabilizes, and the improvement suggestions become more targeted.

```
Cycle 1:  any input → observation → analysis → improvement_report_1.json + updated_observation.json
Cycle 2:  updated_observation.json → analysis → improvement_report_2.json + updated_observation.json
Cycle N:  ...
```

In full triad mode, the `updated_specification.json` feeds back into `intent-engineering` to close the loop across all three skills.

---

## Configuration

All configuration lives inside the skill — no external files required.

**`references/alignment_values.json`** — Edit to define your organization's goals and values. The analyzer checks every observation against these values to produce the alignment score.

**`references/scoring_weights.json`** — Edit to change how the performance score is calculated (e.g. weight pass rate more heavily than speed).

**`references/suggestion_rules.json`** — Edit to add custom rules for generating improvement suggestions.

---

## Resources

```
feedback-loop/
├── SKILL.md                              ← this file
├── scripts/
│   ├── observer.py                       ← normalizes any input → observation.json
│   ├── analyzer.py                       ← scores, detects regressions, generates suggestions
│   └── orchestrator.py                   ← runs all stages, produces signed report
├── references/
│   ├── alignment_values.json             ← org goals and values (edit this)
│   ├── scoring_weights.json              ← performance score weights
│   ├── suggestion_rules.json             ← rules for improvement suggestions
│   └── operations_guide.md              ← detailed ops and troubleshooting guide
└── templates/
    ├── improvement_report_template.md    ← human-readable report template
    └── observation_template.json         ← blank observation template
```
