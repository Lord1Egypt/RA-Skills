# async-queue — Delayed Task Queue for OpenClaw Agents

Schedule delayed or async tasks between OpenClaw agents via a file-backed queue daemon.

## Install
1. `openclaw skills install async-queue`
2. `bash "$(openclaw skill path async-queue)/scripts/install.sh"`
3. `openclaw gateway restart`

## Quick Start
Push a delayed task:
```bash
node ~/.openclaw/queue/push.js --to main --task "Check deploy status" --delay 5m
```
Check the queue:
```bash
node ~/.openclaw/queue/queue-cli.js list
```

## Queue Discipline
Always pair a push with a follow-up check-in so work is verified after it fires.
```bash
node ~/.openclaw/queue/push.js --to main --task "Run rollout checks" --delay 10m --then "Confirm rollout results"
```

## Full Docs
See `SKILL.md`.
