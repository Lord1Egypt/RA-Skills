---
name: expflow-pipeline-hpo
description: >
  PDEBench competition workflow orchestration with expflow —
  three pipeline modes (full/fast/skip), distributed HPO, pruner integration,
  and ClearML HyperParameterOptimizer native mode.
category: mlops
author: Li Shen
version: 1.0.0
metadata:
  hermes:
    tags: [mlops, pde, hpo, clearml, optuna, pipeline, competition]
    homepage: https://github.com/diamond2nv/expflow
    related_skills: [experiment-lifecycle-governance, clearml-metrics-logging-pattern, competition-task-intelligence]
---

# expflow PDEBench Pipeline & HPO

Orchestrate experiment workflows for the AI4S PDE competition using expflow.
Three modes for three competition phases.

## Triggers

- User says "run HPO", "submit pipeline", "distributed experiment"
- User says "competition sprint" or "fast iterate"
- User asks about automating the train→eval→submit loop
- User mentions needing to find best hyperparams

## Installation

```bash
pip install "expflow-pde[pipeline]"
```

## Available Pipeline Modes

Three pipeline modes, each mapped to a CLI command:

### Mode A — Full (HPO → Train → Eval)

For the **exploration phase** of a competition task. Optuna finds best params
via distributed clearml-agent trials, trains with best, then evaluates.

```bash
expflow pipeline submit-full train_task1.py \
    --queue default \
    --trials 50 --parallel 4 \
    --eval-script eval_task1.py \
    --metric seg_total --direction maximize
```

Flags used:
- `--trials N`: total HPO trials
- `--parallel M`: max concurrent trials (use GPU node count)
- `--metric`: objective metric name prefixed `METRIC:` in script stdout
- `--pruner hyperband|median|percentile`: early-stop poor trials
- `--study-name`: Optuna study name (auto if omitted; persists to SQLite)
- `--skip hpo --skip eval`: run train only within full skeleton

### Mode B — Fast (Train → Eval)

For the **competition sprint** phase. You already know best params. Skip HPO,
run directly with fixed args.

```bash
expflow pipeline submit train_task1.py \
    --queue default \
    --train-param lr=0.001 --train-param epochs=80 \
    --eval-script eval_task1.py \
    --eval-param sub_step=5
```

Flags:
- `--skip eval`: train-only (just submit checkpoint)
- `--train-param key=val`: injected as `--key=val` to training script
- `--eval-param key=val`: injected as `--key=val` to eval script

### Mode C — Flexible Skip

Override step inclusion on either mode:

```bash
expflow pipeline submit-full train_task1.py \
    --skip hpo --skip eval          # = train only
expflow pipeline submit-full train_task1.py \
    --skip train --skip eval         # = HPO only
```

## HPO: Three Execution Modes

HPO (`expflow optuna run`) has three backends:

| Mode | Flag | Description | Best for |
|------|------|-------------|----------|
| Local | (default) | subprocess serial on CPU | ≤20 trials, quick test |
| Distributed | `--distributed` | ask/tell + clearml Task clone| Multi-GPU, custom control|
| Optimizer | `--optimizer -O` | Clearml `HyperParameterOptimizer` | Production, 50-200+ trials |

### Key flags across all HPO modes:
- `--pruner hyperband|median|percentile|none`: ASHA pruner saves ~40% GPU time
- `--metric <name>`: reads `METRIC:<name>=<value>` from script stdout
- `--direction maximize|minimize`
- `--timeout <min>`: safety cutoff

## Script Requirements

The training/eval script must:
1. Accept hyperparams as `--key=value` CLI arguments
2. Output `METRIC:<name>=<value>` to stdout for objective capture (local mode)
3. Report clearml scalars for distributed/optimizer mode:
   ```python
   Task.current_task().report_scalar("Score", "seg_total", value, iteration=epoch)
   ```

## Pitfalls

- **Pruner needs `trial.report()` calls during training.** If the script only reports at the end, the pruner has nothing to prune on. Call `trial.report(val_loss, epoch)` at least every 10 epochs.
- **HyperParameterOptimizer needs the metric name in `Title/Series` format.** If your metric is `seg_total`, it becomes `title=seg_total, series=seg_total`. If your clearml report_scalar is `report_scalar("Score", "seg_total", v)`, pass `--metric Score/seg_total`.
- **Clearml-agent must be running on GPU nodes** before submitting. Verify with `expflow clearml workers` or check Web UI.
- **`_collect_one_trial` polls every 5s** — waits up to 60min per trial. If trials are expected to run longer, increase `timeout_minutes`.

## Architecture Reference

Key files in `expflow_pde/`:
- `hpo.py` — 3-mode HPO runner (local/distributed/optimizer)
- `pipeline.py` — ExperimentPipeline class (fast/full modes)
- `cli_pipeline.py` — `pipeline submit` + `pipeline submit-full`
- `cli_optuna.py` — `optuna run` with all three backends

## Related

- `experiment-lifecycle-governance` — PIN, metrics registry, compare-scores, competition rules audit
- `pde-experiment-hyperparameters` — PDEBench-specific hyperparameter reference
- `multi-agent-distributed-experiment-workflow` — Hermes → OpenCode → clearml
