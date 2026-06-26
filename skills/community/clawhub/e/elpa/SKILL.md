---
name: elpa
description: "Orchestrate real ELPA-style ensemble forecasting workflows by triggering external sub-model training jobs (for example PyTorch/Prophet/TiDE/transformers), then computing ELPA online/offline weights from validation errors. Use when you need production-oriented ensemble training instead of lightweight simulation adapters."
---

# ELPA

## Overview

This skill does not train toy adapters. It triggers real sub-model training commands from your own training codebases and then builds ELPA routing/weights from real validation errors.

Default model pool is intentionally larger than 4 and can be expanded freely.

## Workflow

1. Prepare a training config JSON (see `assets/elpa_train_template.json`).
2. Dry-run the command plan to verify all sub-model commands.
3. Execute real sub-model training when resources are available.
4. Prepare validation error inputs per model.
5. Build ELPA ensemble policy JSON from those errors.

## 1) Prepare Config

Create a config based on `assets/elpa_train_template.json`.

- Put your real training entrypoints in each model `train_cmd`.
- Keep each model tagged as `online` or `offline`.
- Add as many models as needed; ELPA is not limited to 4.

## 2) Dry-Run Plan (No Training)

```bash
python3 scripts/elpa_orchestrator.py \
  --config assets/elpa_train_template.json \
  --run-dir .runtime/elpa_run \
  --manifest-out .runtime/elpa_run/train_manifest.json
```

This prints and records the commands that would run, without training.

## 3) Execute Real Training

```bash
python3 scripts/elpa_orchestrator.py \
  --config /path/to/your_train_config.json \
  --run-dir .runtime/elpa_run \
  --manifest-out .runtime/elpa_run/train_manifest.json \
  --execute
```

Use this only in an environment that has the required ML dependencies and hardware.

## 4) Build ELPA Integration Policy

After each sub-model produces validation errors, run:

```bash
python3 scripts/elpa_integrator.py \
  --config /path/to/your_integrate_config.json \
  --output .runtime/elpa_run/elpa_policy.json
```

The output includes:

- `scores` for each model from validation errors
- `online_weights` and `offline_weights`
- `best_online_model` and `best_offline_model`
- ELPA control fields (`beta`, `dirty_interval`, `amplitude_window`, `mutant_epsilon`)

## Model Scaling

To support more models, append model blocks in your config with:

- unique `name`
- `group` as `online` or `offline`
- real `train_cmd`

No script changes are needed for adding models.

## Files

- `scripts/elpa_orchestrator.py`: real sub-model training command planner/executor
- `scripts/elpa_integrator.py`: ELPA score/weight builder from validation errors
- `assets/elpa_train_template.json`: >4-model real training template
- `assets/elpa_integrate_template.json`: ELPA integration template
- `references/config-schema.md`: config field reference and placeholders
