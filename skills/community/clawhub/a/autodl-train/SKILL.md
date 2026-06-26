---
name: operating-autodl-training
description: Operates remote model training jobs on AutoDL Linux servers over SSH. Use when starting a training run, checking whether training is still alive, reviewing GPU/CPU/memory/disk usage, reading recent logs, diagnosing abnormal interruptions, or summarizing the latest training outcome with next-step recommendations.
---

# Operating AutoDL Training

Use this skill for remote training operations on an AutoDL Linux server. It is designed for high-frequency workflows around "start training, watch progress, inspect resources, read logs, diagnose failures, and decide what to do next" while keeping execution constrained to one configured project directory.

## What This Skill Does

- Starts a configured training command in the target project directory over SSH.
- Activates the remote Python environment with Conda or virtualenv fallbacks.
- Checks whether training is still running by combining process, GPU, and log freshness signals.
- Summarizes GPU, CPU, memory, and disk pressure instead of dumping raw command output.
- Reads recent logs and extracts likely metrics such as `epoch`, `step`, `loss`, `lr`, `grad_norm`, `val_loss`, `accuracy`, `mAP`, and `F1`.
- Detects common training failures such as CUDA OOM, NCCL errors, NaN, disk full, timeout, and segmentation faults.
- Produces a human-readable training summary and recommends whether to continue, tune, or resume from a checkpoint.

## Required Inputs

Collect or confirm these values before running any script:

- `host`: AutoDL server hostname or IP.
- `port`: SSH port, usually `22`.
- `username`: Remote Linux username.
- `project_path`: Absolute project directory on the remote server, for example `/root/autodl-tmp/your-project`.
- One environment option: `env_name`, `env_activate`, or `venv_path`.
- `train_command`: The training launch command, such as `python train.py`, `python -m torch.distributed.run ...`, or `bash scripts/train.sh`.
- Optional password mode: provide `AUTOCLAW_TRAIN_SSH_PASSWORD` as an environment variable or local `.env` file when SSH key login is not available.

Prefer a config file at `config.example.json` copied to a real file such as `config.json`, or environment variables based on `.env.example`.

## Safety Rules

- Only operate inside the configured `project_path`.
- Do not invent missing SSH credentials or secrets.
- Do not write plaintext passwords into files.
- Prefer SSH keys or environment variables.
- Refuse obviously destructive launch commands such as `rm -rf`, `reboot`, `shutdown`, `mkfs`, or fork bombs.
- Do not kill unrelated processes or run global destructive recovery commands.

## Workflow

### 1. Confirm Configuration

Read `config.example.json` and `references/usage.md` to understand the expected fields. Ask the user for any missing values instead of guessing.

### 2. Start Or Resume Training

Run `scripts/remote_train.py` to start a background job or build a resume command:

```bash
python scripts/remote_train.py --config config.json
python scripts/remote_train.py --config config.json --resume-from outputs/checkpoints/last.ckpt
```

Use this when the user asks to launch training, re-launch after interruption, or resume from a checkpoint.

### 3. Check Live Status

Run `scripts/check_status.py` when the user asks whether training is still running:

```bash
python scripts/check_status.py --config config.json
```

This script combines process matching, `nvidia-smi`, and recent log updates to classify the run as `running`, `stopped`, `failed`, or `unknown`.

### 4. Inspect Resource Pressure

Run `scripts/monitor_resources.py` to summarize GPU/CPU/memory/disk usage:

```bash
python scripts/monitor_resources.py --config config.json
```

Use the human-readable bottleneck assessment in the output instead of pasting raw command output unless the user asks for raw data.

### 5. Read Logs And Summaries

Run `scripts/summarize_log.py` in one of these modes:

```bash
python scripts/summarize_log.py --config config.json --action read --tail 200
python scripts/summarize_log.py --config config.json --action detect-failure --tail 400
python scripts/summarize_log.py --config config.json --action summarize --tail 400
```

Use `read` for recent excerpts and metrics, `detect-failure` for exception diagnosis, and `summarize` for a concise human-facing assessment with next steps.

## Script Map

- `scripts/remote_train.py`: start training, optional resume templating, structured launch result.
- `scripts/check_status.py`: process/GPU/log-based training status.
- `scripts/monitor_resources.py`: GPU/CPU/memory/disk summary and bottleneck hints.
- `scripts/summarize_log.py`: read logs, detect failures, summarize convergence and next actions.
- `scripts/common.py`: shared config loading, SSH execution, safe path checks, remote helpers.
- `scripts/log_utils.py`: reusable log parsing, failure detection, trend analysis, recommendation logic.

## References

- Read `references/usage.md` for setup steps, example configs, and example commands.
- Read `references/troubleshooting.md` when SSH, environment activation, logs, or training recovery fail.

## Agent Guidance

- Start with the least invasive action that answers the user’s request.
- When the user asks a yes/no status question, prefer `scripts/check_status.py` before reading a long log.
- When the user asks why training stopped, run `scripts/check_status.py` and then `scripts/summarize_log.py --action detect-failure`.
- When the user asks whether to continue training, run `scripts/summarize_log.py --action summarize` and include the recommendations from the script in the final response.
- When a checkpoint path is provided, prefer `scripts/remote_train.py --resume-from ...` so the resume command is explicit and auditable.
