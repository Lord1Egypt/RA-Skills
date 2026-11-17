---
name: competition-task-intelligence
title: Competition Task Intelligence — PDE Equation Registry, Task Analysis, and Strategic Advising
description: >
  Build and maintain a structured PDE equation registry, analyze competition tasks
  (difficulty, bottlenecks, score projections), generate strategic recommendations
  for research focus, and expose this intelligence via CLI and MCP tools.
category: mlops
author: Li Shen
version: 0.7.2
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

> **Part of the Exo suite** — literature (`hfpclawer`) → experiments (`expflow-pde`) → proofs
> (`omega-architect`). Three independent CLIs that meet through **files and CLI calls**, never imports.
> Entry skill: `exo-suite-linkage` (wiring, cost tiers **low → medium → high**, degradation ladder).
> Install: `uv tool install hfpclawer` · `uv tool install expflow-pde` ·
> `uv tool install "omega-architect @ git+https://github.com/diamond2nv/omega-architect@v0.2.3"`

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

**Version floor**: install `expflow-pde>=0.7.0` (public/PyPI line). The development line is ahead
(0.7.3): anything marked "development line" below is not in the PyPI 0.7.0 artifact.

```bash
uv tool install expflow-pde                  # 1) isolated CLI, `expflow` on PATH (recommended)
# pin the version — `uvx`/`uv tool run` reuse an installed tool env (may run an older
# release), and an unpinned launch is a supply-chain (rug-pull) risk
uvx --from "expflow-pde==0.7.0" expflow --help        # 2) run it without installing anything
uv pip install expflow-pde                   # 3) inside an existing project / venv
pip install expflow-pde                      # 4) no uv — pip and pipx both work
pipx install expflow-pde                     #    (pipx needs a recent version; 1.0.0 cannot parse specs)
# extras ride along with any form, e.g.: uv tool install "expflow-pde[clearml]"
```
*All five forms above were run and verified (uv tool install / uvx --from / uv pip / pip / pipx).*

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


## Hermes Agent Environment

- **MCP server** — `expflow mcp` starts a FastMCP server (18+ tools) for agent integration:

  ```yaml
  # ~/.hermes/config.yaml
  mcp:
    servers:
      expflow:
        command: "expflow"
        args: ["mcp"]
  ```

- **Config** — `expflow init` writes the toolkit config; real credentials (ClearML API, Langfuse
  keys, dataset paths) belong in `.env` / a local `config.yaml`, never in tracked files.
- **Environment overrides** — `EXPFLOW_HOME`, `EXPFLOW_PIN_HASH`, `EXPFLOW_COMPETITION_DEADLINE`,
  `EXPFLOW_SEMANTIC_URL`.
- **Cost profile (not zero-cost)** — the orchestration layer itself makes no LLM call, but runs cost
  real money and hardware: ClearML workers/queue time, GPU hours for the submitted experiments, and
  storage for artifacts. Quote costs from recorded runs, never an estimate.

## Pitfalls

1. **`_TASK_META` becomes stale** — hardcoded scores must be updated after each submission
2. **Competition deadline hardcoded** — `get_strategic_recommendation()` has `remaining_days` from `2026-05-27`
3. **Scoring formula duplication** — Task 3 formulae are in both `equations.py` and `analyze.py`; keep synced
4. **No clearml import in analyze** — `analyze.py` uses only pure Python/stdlib for fast CLI startup
