# AIMA Doctor Skill Pack

This folder is a ClawHub-publishable OpenClaw skill bundle for AIMA Doctor.

## What this contains

- `SKILL.md`: the OpenClaw skill entrypoint
- `README.md`: packaging notes

The helper runtime is distributed separately from:

- `https://aimaservice.ai/doctor/runtime.zip`

## Local install

1. Copy this folder under `<workspace>/skills/` or `~/.openclaw/skills/`.
2. Extract the helper runtime into `~/.openclaw/tools/aima-doctor/`.
3. Start a new OpenClaw session or restart the gateway.

## Publish to ClawHub

```bash
clawhub publish ./aima-doctor --slug aima-doctor --name "AIMA Doctor" --version 0.2
```
