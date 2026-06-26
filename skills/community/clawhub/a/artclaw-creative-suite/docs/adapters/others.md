# Generic Adapter

Use this adapter when the current platform has no dedicated adapter.

First, determine which execution model applies:

## Claw-compatible Platform

If the platform exposes a sub-agent spawn tool (e.g. `sessions_spawn`, `delegate_task`, or equivalent), follow `docs/adapters/openclaw.md` instead of this file.

## Plain CLI Platform

If no spawn tool is available, use this execution model.

### Execution Model

For generation and workflow commands:

1. Do not use `--spawn`.
2. Use `--no-wait` so the CLI submits the job and returns immediately.
3. If the user explicitly asks to wait, you may omit `--no-wait`.
4. Return `job_id` to the user along with the `job-status` command to check progress.

Submit command form:

```bash
python3 scripts/artclaw.py generate-image \
  --prompt "A cute kitten rolling on the floor" \
  --aspect-ratio 1:1 \
  --no-wait
```

Status command:

```bash
python3 scripts/artclaw.py job-status --job-id "job_xxxxxxxx"
```

Analysis commands are synchronous and may run normally.
