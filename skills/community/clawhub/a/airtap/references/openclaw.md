# OpenClaw Relay

Use this optional path only when the host explicitly wants Airtap progress updates mirrored into
OpenClaw.

## Rules

- `task poll` stays local unless `--openclaw-target` is provided.
- Prefer passing the full routing tuple when it is available:
  `--openclaw-channel`, `--openclaw-account`, `--openclaw-target`,
  `--openclaw-thread-id`, and `--openclaw-reply-to`.
- Milestone-only delivery is the default: acknowledgement, one plan/start update, and the final or
  waiting-state update.
- Add `--openclaw-verbose` only when the host explicitly wants every Airtap agent update
  forwarded.
- Never invent routing values. Use only values supplied or approved by the user.

## Examples

Forward milestone updates:

```bash
python3 scripts/airtap.py task poll \
  --task-id "task_abc123" \
  --openclaw-channel discord \
  --openclaw-target "channel:1234567890" \
  --openclaw-thread-id "9876543210"
```

Forward every Airtap agent update:

```bash
python3 scripts/airtap.py task poll \
  --task-id "task_abc123" \
  --openclaw-channel discord \
  --openclaw-target "channel:1234567890" \
  --openclaw-thread-id "9876543210" \
  --openclaw-verbose
```
