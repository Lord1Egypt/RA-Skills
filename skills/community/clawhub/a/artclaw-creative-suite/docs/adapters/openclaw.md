# OpenClaw Adapter

Use this adapter in OpenClaw and OpenClaw-compatible environments that expose `sessions_spawn`.

## Execution Model

Generation and workflow commands must use spawn mode:
```bash
python3 scripts/artclaw.py generate-image \
  --prompt "Cyberpunk cityscape at night" \
  --aspect-ratio 16:9 \
  --spawn \
  --deliver-to ou_xxxxxx \
  --deliver-channel feishu
```

Flow:

1. Run the target `generate-*` or `run-workflow` command with `--spawn`.
2. Include `--deliver-to` and `--deliver-channel`.
3. Read `sessions_spawn_args` from the CLI JSON output.
4. Pass `sessions_spawn_args` to `sessions_spawn`.
5. Immediately tell the user the job has been submitted.
6. Do not wait silently in the main agent.

Do not use `--spawn` for analysis commands.

