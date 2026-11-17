---
name: clearml-metrics-logging-pattern
description: Standardized ClearML metrics logging patterns for PDEBench experiment scripts — train loss, validation metrics, competition scores, PDE residual, and TensorBoardX integration. Includes patterns for dist/expflow compatibility.
category: mlops
tags: [clearml, metrics, logging, experiment-tracking, pdebench]
author: Li Shen
version: 0.7.2
metadata:
  hermes:
    tags: [mlops, pde, clearml, metrics, logging, experiment, competition]
    homepage: https://github.com/diamond2nv/expflow
    related_skills: [expflow-pipeline-hpo, experiment-lifecycle-governance, competition-task-intelligence]
---

# ClearML Metrics Logging Pattern

> **Part of the Exo suite** — literature (`hfpclawer`) → experiments (`expflow-pde`) → proofs
> (`omega-architect`). Three independent CLIs that meet through **files and CLI calls**, never imports.
> Entry skill: `exo-suite-linkage` (wiring, cost tiers **low → medium → high**, degradation ladder).
> Install: `uv tool install hfpclawer` · `uv tool install expflow-pde` ·
> `uv tool install "omega-architect @ git+https://github.com/diamond2nv/omega-architect@v0.2.3"`

## When to Use

- Creating or modifying PDEBench training/evaluation scripts
- Adding clearml logging to `train_task1.py`, `train_task1_phys.py`, `train_task1_ft.py`, `train_task1_unroll.py`
- Ensuring expflow (single-node + distributed) can auto-capture metrics
- Standardizing metric naming for compare-scores and gating

## Installation



```bash
pip install "expflow-pde[clearml]"
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

## Standardized Metric Naming Convention

All clearml metrics use **Group/Metric** naming, compatible with `expflow clearml compare-scores`:

```python
# Loss group — error/cost related scalars
clearml_logger.report_scalar('Loss', 'Train MSE',     float_val, iteration=epoch)
clearml_logger.report_scalar('Loss', 'Val MSE',       float_val, iteration=epoch)
clearml_logger.report_scalar('Loss', 'Val RelMSE',    float_val, iteration=epoch)
clearml_logger.report_scalar('Loss', 'Physics',       float_val, iteration=epoch)
clearml_logger.report_scalar('Loss', 'Commut',        float_val, iteration=epoch)
clearml_logger.report_scalar('Loss', 'Stability',     float_val, iteration=epoch)

# Score group — competition segment scores (100-point scale)
clearml_logger.report_scalar('Score', 'Seg Total',    float_val, iteration=epoch)
clearml_logger.report_scalar('Score', 'Seg1',         float_val, iteration=epoch)
clearml_logger.report_scalar('Score', 'Seg2',         float_val, iteration=epoch)
clearml_logger.report_scalar('Score', 'Seg3',         float_val, iteration=epoch)

# PDE group — PDE residuals (per-segment)
clearml_logger.report_scalar('PDE', 'Mean Residual',  float_val, iteration=epoch)
clearml_logger.report_scalar('PDE', 'Seg1 Residual',  float_val, iteration=epoch)
clearml_logger.report_scalar('PDE', 'Seg2 Residual',  float_val, iteration=epoch)
clearml_logger.report_scalar('PDE', 'Seg3 Residual',  float_val, iteration=epoch)

# System group — system monitoring
clearml_logger.report_scalar('System', 'GPU Alloc MB',   float_val, iteration=epoch)
clearml_logger.report_scalar('System', 'GPU Reserved MB', float_val, iteration=epoch)
clearml_logger.report_scalar('System', 'LR',              float_val, iteration=epoch)

# Kfold group — k-fold cross-validation results
clearml_logger.report_scalar('Kfold', 'Mean Seg',    float_val, iteration=0)
clearml_logger.report_scalar('Kfold', 'Std Seg',     float_val, iteration=0)
clearml_logger.report_scalar('Kfold', 'CV Seg%',     float_val, iteration=0)
```

## Code Templates

### Template A: Add clearml logging to training loop

Insert into existing `train_task1.py` / `train_task1_phys.py` / `train_task1_ft.py` / `train_task1_unroll.py`:

```python
# After Task.init(), get logger
clearml_logger = None
if clearml_task is not None:
    try:
        clearml_logger = clearml_task.get_logger()
    except Exception:
        pass

# At end of epoch loop (after avg_loss is computed)
if clearml_logger is not None:
    clearml_logger.report_scalar('Loss', 'Train MSE', avg_loss, iteration=epoch + 1)
    clearml_logger.report_scalar('System', 'LR', scheduler.get_last_lr()[0], iteration=epoch + 1)
    if DEVICE.type == 'cuda':
        clearml_logger.report_scalar('System', 'GPU Alloc MB', round(gpu_alloc, 1), iteration=epoch + 1)

# After validation (after val_mse, val_rel, seg are computed)
if clearml_logger is not None:
    clearml_logger.report_scalar('Loss', 'Val MSE', val_mse, iteration=epoch + 1)
    clearml_logger.report_scalar('Loss', 'Val RelMSE', val_rel, iteration=epoch + 1)
    clearml_logger.report_scalar('Score', 'Seg Total', seg['total_segmented_score'], iteration=epoch + 1)
    clearml_logger.report_scalar('Score', 'Seg1', seg['seg1_score'], iteration=epoch + 1)
    clearml_logger.report_scalar('Score', 'Seg2', seg['seg2_score'], iteration=epoch + 1)
    clearml_logger.report_scalar('Score', 'Seg3', seg['seg3_score'], iteration=epoch + 1)

# For physics loss (train_task1_phys.py)
if clearml_logger is not None and phys_loss is not None:
    clearml_logger.report_scalar('Loss', 'Physics', phys_loss.item(), iteration=epoch + 1)
```

### Template B: Eval script clearml logging

```python
def run_eval_and_log(model, val_data, cl_task, tag):
    clearml_logger = cl_task.get_logger() if cl_task is not None else None
    val_mse, val_rel, seg_scores = evaluate_autoregressive(model, val_data)

    if clearml_logger is not None:
        clearml_logger.report_scalar('Score', 'Seg Total', seg_scores['total_segmented_score'], iteration=1)
        clearml_logger.report_scalar('Score', 'Seg1', seg_scores['seg1_score'], iteration=1)
        clearml_logger.report_scalar('Score', 'Seg2', seg_scores['seg2_score'], iteration=1)
        clearml_logger.report_scalar('Score', 'Seg3', seg_scores['seg3_score'], iteration=1)
        clearml_logger.report_scalar('Loss', 'Val MSE', val_mse, iteration=1)
        clearml_logger.report_scalar('Loss', 'Val RelMSE', val_rel, iteration=1)

    return val_mse, val_rel, seg_scores
```

### Template C: Double Logger (TensorBoardX + ClearML)

```python
class DoubleLogger:
    def __init__(self, tb_writer=None, cl_logger=None):
        self.tb = tb_writer
        self.cl = cl_logger

    def scalar(self, group, name, value, iteration):
        if self.tb is not None:
            self.tb.add_scalar(f'{group}/{name}', value, iteration)
        if self.cl is not None:
            self.cl.report_scalar(group, name, value, iteration=iteration)
```

## Consistency with expflow

- Group names match `compare-scores` display names
- Metric names match `STANDARD_METRICS` keys (via underscore)
- `iteration` must increment monotonically (clearml x-axis requirement)
- Single-value eval metrics use `iteration=1`


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

## Known Pitfalls

1. **`Task.get_logger()` must be called after `Task.init()`**, otherwise returns None
2. **`capture_tensorboard=True`** — TensorBoardX and clearml dual-write works, but clearml adds TensorBoard path prefix to group names
3. **Distributed metrics** are stored per-trial — parent optuna study only stores `user_objective`, not aggregated trial metrics
4. **Group + Metric name must be consistent** — always `Score/Seg Total`, never `Score/Seg_Total`
