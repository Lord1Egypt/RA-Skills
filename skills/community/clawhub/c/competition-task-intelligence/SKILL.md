---
name: competition-task-intelligence
title: Competition Task Intelligence — PDE Equation Registry, Task Analysis, and Strategic Advising
description: >
  Build and maintain a structured PDE equation registry, analyze competition tasks
  (difficulty, bottlenecks, score projections), generate strategic recommendations
  for research focus, and expose this intelligence via CLI and MCP tools.
category: mlops
author: Li Shen
version: 1.0.0
tags: [mlops, competition, strategy, equations, analysis, planning, pde, task-intelligence]
metadata:
  hermes:
    tags: [mlops, pde, competition, strategy, equations, analysis, ai4s]
    homepage: https://github.com/diamond2nv/expflow
    related_skills:
      - expflow-pipeline-hpo
      - experiment-lifecycle-governance
      - clearml-metrics-logging-pattern
      - agent4pde-competition-scoring
      - pde-experiment-hyperparameters
created: 2026-05-19
updated: 2026-05-19
---

# Competition Task Intelligence

## Overview

System for structured PDE equation management and competition task analysis. Provides:

1. **PDE Equation Registry** — structured metadata (LaTeX, dimensions, params, datasets) for 11+ PDEs
2. **Task Analysis** — per-task difficulty assessment, bottleneck identification, proven strategy catalog
3. **Score Projection** — optimistic/expected/conservative score estimates with confidence levels
4. **Strategic Advising** — which task to focus on, suggested schedule, rationale
5. **CLI + MCP** — `expflow analyze` command group and MCP tools

## Installation

```bash
pip install expflow-pde
```

## Architecture

```
expflow_pde/equations.py     ──── PDE equation static registry (11+ equations)
expflow_pde/analyze.py       ──── Analysis engine (task intelligence, strategy)
expflow_pde/cli_analyze.py   ──── CLI: analyze task/equations/status/advise
expflow_pde/mcp_server.py    ──── MCP: exp_compare_scores, exp_list_workers
```

## 1. PDE Equation Registry

Each equation entry in `EQUATIONS` dict includes: full name, LaTeX, dimensions, parameters, competition task mapping, metrics, solver, data samples, and competition info.

### API

```python
from expflow_pde.equations import (
    get_equations(),                    # All 11+ equations
    get_equation(name),                 # Single equation
    list_equations_for_task(task_id),   # task1/task2/task3
    get_equation_metrics(name, task),   # Relevant STANDARD_METRICS
    list_equation_names(),              # Sorted names
    list_competition_equations(),       # Only competition equations
)
```

## 2. Task-Level Intelligence

### CLI

```bash
# Strategic advising (primary entry point)
expflow analyze advise

# Per-task analysis
expflow analyze task task1
expflow analyze task task3

# Equation reference
expflow analyze equations --task competition

# Competition overview
expflow analyze status
```

### Example Output

```
expflow analyze status

Task     Score              Difficulty     Status         Priority
  ────────────────────────────────────────────────────────────────────
  task1    142/150            🟡 medium       🔴 In Progress  high
  task2    -/150              🔴 hard         ⚪ Not Started  low
  task3    -/350              🔥 very_hard    ⚪ Not Started  medium

  总分: 142/650  (508 pts remaining)
```

### Score Estimation

```python
from expflow_pde.analyze import estimate_score_potential, get_strategic_recommendation

estimates = estimate_score_potential("task1")
# Returns: {"optimistic": 148, "expected": 145, "conservative": 140, "confidence": "high"}

rec = get_strategic_recommendation()
# Returns: {"primary_focus": "task1", "remaining_headroom": {...}, "suggested_schedule": {...}}
```

### Difficulty Classification

| Label | Icon | Example | Meaning |
|-------|:----:|---------|---------|
| easy | 🟢 | Baseline tasks | High confidence, proven methods exist |
| medium | 🟡 | Task 1 | Known bottlenecks, clear path forward |
| hard | 🔴 | Task 2 | Multiple unknown challenges |
| very_hard | 🔥 | Task 3 (KS) | Chaotic dynamics, exponential error growth |

## Integration with Other Systems

### With experiment-lifecycle-governance
`compare-scores` gating builds on equation metrics from this system. When adding a new equation, its metrics must exist in `STANDARD_METRICS` for gating to work.

### With analyze-experiment-autoregressive-degradation
Chain: `analyze advise → decide task → run experiment → analyze degradation → feed back to _TASK_META`.

## Pitfalls

1. **`_TASK_META` becomes stale** — hardcoded scores must be updated after each submission
2. **Competition deadline hardcoded** — `get_strategic_recommendation()` has `remaining_days` from `2026-05-27`
3. **Scoring formula duplication** — Task 3 formulae are in both `equations.py` and `analyze.py`; keep synced
4. **No clearml import in analyze** — `analyze.py` uses only pure Python/stdlib for fast CLI startup
