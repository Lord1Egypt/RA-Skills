# AICE Skill

AI Confidence Engine skill for OpenClaw.

## What it does
- Bidirectional scoring across 5 domains (TECH, OPS, JUDGMENT, COMMS, ORCH)
- Agent + User + Team confidence model
- Hub sync support (`api.hubaice.com`)

## Files
- `SKILL.md` — core behavior/spec
- `confidence.template.json` — safe starter template (no personal data)
- `resources/` — reference docs and pattern definitions
- `scripts/` — helper scripts

## Install
1. Copy this folder into your OpenClaw skills directory.
2. Rename `confidence.template.json` to `confidence.json` for a fresh install.
3. Load the skill in your OpenClaw startup flow.

## Notes
- Do **not** commit personal logs or private API keys.
- Hub scoring starts fresh server-side by design.
