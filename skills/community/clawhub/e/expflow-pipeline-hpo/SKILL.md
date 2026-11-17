---
name: expflow-pipeline-hpo
description: >
  PDEBench competition workflow orchestration with expflow —
  three pipeline modes (full/fast/skip), distributed HPO, pruner integration,
  and ClearML HyperParameterOptimizer native mode.
category: mlops
tags: [pipeline, orchestration, hpo, pdebench, clearml]
author: Li Shen
version: 0.7.2
metadata:
  hermes:
    tags: [mlops, pde, hpo, clearml, optuna, pipeline, competition]
    homepage: https://github.com/diamond2nv/expflow
    related_skills: [experiment-lifecycle-governance, clearml-metrics-logging-pattern, competition-task-intelligence]
---

# expflow PDEBench Pipeline & HPO

> **Part of the Exo suite** — literature (`hfpclawer`) → experiments (`expflow-pde`) → proofs
> (`omega-architect`). Three independent CLIs that meet through **files and CLI calls**, never imports.
> Entry skill: `exo-suite-linkage` (wiring, cost tiers **low → medium → high**, degradation ladder).
> Install: `uv tool install hfpclawer` · `uv tool install expflow-pde` ·
> `uv tool install "omega-architect @ git+https://github.com/diamond2nv/omega-architect@v0.2.3"`

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


## Experiment Loop Commands (0.7.0)

| Group | Sub-commands | Purpose |
|:--|:--|:--|
| `expflow dispatch` | `status` `list` `tree` `stats` `audit-log` `archive` | local SQLite dispatch database (what was submitted, when, by whom) |
| `expflow iterate` | `run` | one-shot iteration: diagnose → suggest → submit |
| `expflow repeat` | `diagnose` `resubmit` | repair diagnosis and resubmission (Hermes `/goal` compatible) |
| `expflow hypothesis` | `open` `record` `list` `show` `rejected` `close` | hypothesis tracking, **including negative results** |

Pair them: `dispatch` gives the provenance trail, `iterate`/`repeat` close the loop, and
`hypothesis` keeps the failed directions from being retried blindly.

### Only in the development line (not in the 0.7.0 PyPI artifact yet)

- `expflow competition` — `init` `stop` `status` `merge` `mask` `bootstrap` `collect` `validate`
  (competition logging sessions, parameterized scoring).
- Modules added after 0.7.0: noise-aware champion validation + agent arbiter (`validate.py`),
  cross-session dead-end registry (`registry.py`), stagnation detection and experiment reports
  (`monitor.py`).

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
