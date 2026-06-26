# Usage Guide

## 1. Prepare Configuration

Copy `config.example.json` to `config.json` and update at least these fields:

- `host`
- `port`
- `username`
- `project_path`
- `env_name` or `env_activate` or `venv_path`
- `train_command`
- `log_path` or `log_candidates`

If the server currently only accepts password login, do not write the password into `config.json`. Export `AUTOCLAW_TRAIN_SSH_PASSWORD` in your shell or place it in an uncommitted local `.env` file and pass `--env-file .env`.

### Example Config

```json
{
  "host": "region-1.autodl.example",
  "port": 22,
  "username": "root",
  "ssh_key_path": "~/.ssh/id_ed25519",
  "project_path": "/root/autodl-tmp/your-project",
  "allowed_project_roots": ["/root/autodl-tmp"],
  "env_name": "llm-train",
  "conda_sh_path": "/root/miniconda3/etc/profile.d/conda.sh",
  "train_command": "python -m torch.distributed.run --nproc_per_node=2 train.py --config configs/sft.yaml",
  "process_match": "torch.distributed.run --nproc_per_node=2 train.py",
  "log_path": "logs/sft.log"
}
```

## 2. Start Training

```bash
python scripts/remote_train.py --config config.json
```

### Start With Overrides

```bash
python scripts/remote_train.py \
  --config config.json \
  --host 1.2.3.4 \
  --project-path /root/autodl-tmp/another-project \
  --train-command "bash scripts/train.sh"
```

### Resume From Checkpoint

```bash
python scripts/remote_train.py \
  --config config.json \
  --resume-from outputs/checkpoints/epoch-04.pt
```

If your framework uses a different resume flag, set `resume_argument_template` in config, for example:

```json
{
  "resume_argument_template": "--ckpt {checkpoint}"
}
```

## 3. Check Training Status

```bash
python scripts/check_status.py --config config.json
python scripts/check_status.py --config config.json --json
```

Typical fields:

- `status`: `running`, `stopped`, `failed`, or `unknown`
- `pid`
- `start_time`
- `latest_log_time`
- `latest_log_excerpt`
- `failure_hints`

## 4. Monitor Resources

```bash
python scripts/monitor_resources.py --config config.json
python scripts/monitor_resources.py --config config.json --json
```

The script reports:

- Per-GPU utilization and memory occupancy
- Load average relative to CPU core count
- Memory usage ratio
- Disk usage ratio for the project filesystem
- A short bottleneck assessment

## 5. Read Logs Or Summaries

### Read Recent Logs

```bash
python scripts/summarize_log.py --config config.json --action read --tail 200
```

### Detect Failures

```bash
python scripts/summarize_log.py --config config.json --action detect-failure --tail 400
```

### Summarize Training

```bash
python scripts/summarize_log.py --config config.json --action summarize --tail 400
```

The summarizer tries to extract metrics such as `epoch`, `step`, `loss`, `lr`, `grad_norm`, `val_loss`, `accuracy`, `mAP`, and `F1` from plain text logs. If the log format is custom, it falls back to heuristic summaries.

## 6. Environment Variable Mode

You can also copy `.env.example` to `.env`, export the variables, and omit `--config` if all required values are available in the environment.

### Password Login Mode

```bash
export AUTOCLAW_TRAIN_SSH_PASSWORD='your-server-password'
python scripts/check_status.py --config config.json
```

The scripts use `SSH_ASKPASS` under the hood so the password does not need to be written into `config.json`.

## 7. Recommended Operator Flow

1. Use `remote_train.py` to start training.
2. Use `check_status.py` after a short delay to confirm the launcher PID and log freshness.
3. Use `monitor_resources.py` if GPU utilization is lower than expected or if the run feels stalled.
4. Use `summarize_log.py --action summarize` when the user asks whether training is converging or should continue.
5. Use `summarize_log.py --action detect-failure` immediately after an interruption.
