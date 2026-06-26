---
name: experiment-lifecycle-governance
title: Experiment Lifecycle Governance — PIN, Metrics Registry, Compare-Scores, Audit
description: Add governance to experiment workflows — PIN-protected destructive ops, standardized metrics registry with thresholds, compare-scores ranking with gating, and competition rules audit. Builds on clearml-agent-dispatch and fysom-fsm-integration.
category: mlops
author: Li Shen
version: 1.0.0
tags: [governance, pin, metrics, compare, audit, guard, competition, safety]
metadata:
  hermes:
    tags: [mlops, pde, governance, clearml, experiment, audit, safety]
    homepage: https://github.com/diamond2nv/expflow
    related_skills: [expflow-pipeline-hpo, clearml-metrics-logging-pattern, competition-task-intelligence]
---

# Experiment Lifecycle Governance

## Overview

Governance layer for experiment workflows: protect destructive operations, standardize metrics, rank experiments with gating, and audit against competition rules.

Three sub-systems:
1. **PIN Protection** — 4-digit PIN guard for cancel/stop/delete operations
2. **Metrics Registry** — Standardized metric definitions with thresholds
3. **Compare-Scores** — Multi-model ranking with gating

## Installation

```bash
pip install expflow-pde
```

## 1. PIN Protection Pattern

### Architecture

```
~/.expflow/pin.hash          # SHA-256 hash of 4-digit PIN (never plaintext)
~/.expflow/experiments.jsonl # Experiment registry (each line = JSON record)
```

### Module Design

```python
# pin.py — 4 components:
# 1. init_pin(pin: str) -> hash          # Validate + hash + write
# 2. verify_pin(pin: str) -> bool         # Hash comparison
# 3. pin_is_set() -> bool                 # Check if PIN configured
# 4. guard(action_description) -> bool    # Interactive prompt

# sha256 hash — never store raw PIN
def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()

# Validate exactly 4 digits
def _validate_pin(pin: str) -> None:
    if not pin.isdigit() or len(pin) != 4:
        raise ValueError("PIN must be exactly 4 digits (0-9)")
```

### CLI Commands

```bash
expflow pin init 1234          # Set PIN (SHA-256 stored)
expflow pin check              # Interactive verify
expflow pin clear [--force]    # Remove PIN
expflow pin status             # Show if active

# Guarded commands (require PIN unless --force):
expflow run cancel <id>            # Interactive PIN prompt
expflow run cancel <id> --force    # Skip PIN
```

## 2. Standardized Metrics Registry

### Structure

```python
STANDARD_METRICS = {
    "seg_total": {
        "type": "scalar", "group": "Score",
        "higher_is_better": True,
        "description": "Total segment score (primary competition metric)",
    },
    "pde_mean": {
        "type": "scalar", "group": "PDE",
        "higher_is_better": False,
        "threshold": 18.09,  # Competition gate
    },
    "train_time_min": {
        "type": "scalar", "group": "Time",
        "higher_is_better": False,
        "threshold": 60,  # Competition limit
    },
    # ... 13 total metrics across Score/Loss/PDE/Time/Model/Training groups
}
```

### report_standard()

```python
def report_standard(task: Any | None = None, **kwargs: float) -> dict[str, float]:
    reported = {}
    for name, value in kwargs.items():
        info = STANDARD_METRICS.get(name)
        if info is None:
            raise ValueError(f"Unknown metric '{name}'...")
        reported[name] = float(value)
        if task is not None:
            task.report_scalar(title=info["group"], series=name, value=float(value), iteration=0)
    return reported
```

## 3. Compare-Scores: Multi-Model Ranking

### CLI

```bash
expflow clearml compare-scores \
    --project PDEBench --tags task1 \
    --sort-by pde_mean --ascending \
    --gate pde_mean:lt:18.09 --gate train_time_min:lt:60
```

### Gate Format

Gates use `metric:op:value` triplets:
- `pde_mean:lt:18.09` — PDE mean < 18.09
- `train_time_min:le:60` — Training time ≤ 60 min
- `seg_total:ge:50` — Score ≥ 50

Operators: `lt`, `le`, `gt`, `ge`.

## 4. Competition Rules Audit

### CLI

```bash
expflow audit validate exp-001 --competition-rules --task-id abc123
```

### Python API

```python
from expflow_pde.audit import validate_competition_rules

result = validate_competition_rules(
    task_metrics={"seg_total": 57.09, "pde_mean": 15.0, "train_time_min": 45.5},
    task_params={"Args/--sub_step": "5"},
)
print(f"All pass: {result['all_pass']}")
```

### Validation Checks

| Check | Condition | Details |
|-------|-----------|---------|
| `seg_total` | Primary competition score (no gating) | Reported, not gated |
| `pde_mean` | Must be < 18.09 | Threshold from STANDARD_METRICS |
| `train_time_min` | Must be < 60 | Threshold from STANDARD_METRICS |
| `sub_step` parameter | Must exist and be > 0 | Searches case-insensitive |

## Testing Patterns

### PIN Tests (36 tests)
- Hash consistency: same input → same hash
- Validation rejects: wrong length, non-numeric, empty
- Init → file exists with correct hash
- Guard mock: correct → True, quit → False

### Metrics Tests
- Registry structure: each metric has type, group, higher_is_better
- report_standard: returns dict of reported metrics

### Compare Tests
- _apply_gate: all 4 operators (lt/le/gt/ge) with passing and failing cases

## Pitfalls

### 1. YAML/Env vs File Storage for PIN
PIN hash must NOT go into `config.yaml` (risk of git commit). Use `~/.expflow/pin.hash`.
Precedence: `pin.hash` file > `.env EXPFLOW_PIN_HASH` > `config.yaml pin.hash`.

### 2. `get_last_scalar_metrics()` clearml API
Returns nested dict: `{"Score": {"seg_total": {"last": 57.09, ...}}, ...}`. Flatten to `{"seg_total": 57.09}` for compare_scores.

### 3. `--force` Flag for Script Calls
Always provide `--force` / `-f` on PIN-guarded commands for CI/automation.

### 4. Interactive `getpass` vs Non-Interactive
`getpass.getpass()` works in terminals but fails in piped commands, CI, or subagent calls. Always provide `--pin` or `--force` as alternative paths.
