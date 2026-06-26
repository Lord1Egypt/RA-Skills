# Troubleshooting

## SSH Connection Fails

### Symptom

- `ssh exited with code 255`
- `Permission denied (publickey)`
- `Connection timed out`

### Checks

- Confirm `host`, `port`, `username`, and `ssh_key_path`.
- Test SSH manually with the same host and key.
- Ensure the key has correct permissions such as `chmod 600 ~/.ssh/id_rsa`.
- If host key prompts block automation, keep `strict_host_key_checking` as `accept-new` or pre-populate `known_hosts`.
- If the server is password-based, export `AUTOCLAW_TRAIN_SSH_PASSWORD` before running the scripts.

## Environment Activation Fails

### Symptom

- `conda: command not found`
- Training command starts but imports fail immediately.

### Fixes

- Set `conda_sh_path` to the correct AutoDL Miniconda path.
- Set `env_name` to the actual Conda environment.
- If the project uses a venv, set `venv_path` to the venv directory.
- If you already have a custom activation one-liner, set `env_activate` directly.

## Training Starts Then Exits Immediately

### Symptom

- `remote_train.py` returns a PID, but `check_status.py` reports `stopped` or `failed` soon after.

### Fixes

- Run `summarize_log.py --action detect-failure` to inspect recent errors.
- Confirm `train_command` is valid from inside the remote project directory.
- Check whether the launcher script writes logs somewhere other than `log_path` or `log_candidates`.
- If using distributed launchers, refine `process_match` so status checks can find the correct process.

## No Logs Found

### Symptom

- Log selection returns no file.

### Fixes

- Set `log_path` explicitly if your project writes to a custom location.
- Add additional entries to `log_candidates`.
- Check whether the training script writes only to stdout; if so, keep `remote_train.py` background mode so stdout is redirected to the configured log file.

## GPU Utilization Is Very Low

### Possible Reasons

- Data loading is too slow.
- Batch size is too small.
- The process is stuck in CPU preprocessing or dataset I/O.
- The training job already stopped but memory is still partially reserved.

### Suggested Actions

- Check `monitor_resources.py` for CPU load and memory pressure.
- Inspect log timestamps with `check_status.py`.
- Increase DataLoader workers, pin memory, or batch size if the framework allows it.

## CUDA Out Of Memory

### Typical Fixes

- Reduce batch size.
- Enable gradient accumulation.
- Use mixed precision.
- Shorten sequence length or image resolution.
- Resume from the latest checkpoint after adjusting memory-sensitive settings.

## Disk Nearly Full

### Typical Fixes

- Move checkpoints to a larger mount.
- Reduce checkpoint retention.
- Clean old experiment outputs manually after verification.
- Do not automate destructive cleanup inside this skill.

## NaN Or Divergence

### Typical Fixes

- Lower learning rate.
- Check mixed precision stability.
- Clip gradients.
- Validate data normalization and labels.
- Resume from an earlier stable checkpoint rather than the most recent broken state.
