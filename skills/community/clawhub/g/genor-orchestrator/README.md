# Genor's Orchestration Skill

> Skill companion for the [genor-orchestrator-plugin](https://github.com/GenorTG/genor-orchestrator-plugin) — instructions, workflows, and dashboard web UI for OpenClaw project orchestration.

[![ClawHub](https://clawhub.com/badge/genor-orchestrator)](https://clawhub.com/packages/genor-orchestrator)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](LICENSE)

This skill works **alongside** the genor-orchestrator plugin. The plugin provides tools + hooks (the runtime), and this skill provides:

- **Coding workflow** — execution phases, fallback chains, debugging protocol
- **Project management** — session tracking, ADRs, backlog, recovery docs
- **Model routing** — routing decision tables, filtering chain, per-project allowlists
- **Dashboard Web UI** — PM2-managed Python server for model CRUD and routing config
- **Scripts** — onboarding, project scaffolding, price checking, auto-population

## Components

```
genor-orchestrator-skill/
├── SKILL.md           — Main skill instructions
├── README.md          — This file
├── ROUTING.md         — Current routing table
├── dashboard/         — Web UI (Python server)
│   └── server.py      — PM2-managed HTTP server
├── scripts/           — CLI tools
│   ├── onboard.sh     — First-time setup
│   ├── init-project.sh — Scaffold new projects
│   ├── check-models.sh — Check eligible models
│   ├── auto-populate-models.py — Auto-populate from config
│   ├── check-prices.sh — Price monitoring
│   └── ...
└── references/        — Docs
    ├── ONBOARDING.md
    ├── EXECUTION.md
    └── ...
```

## Quick Start

1. Install the plugin: `openclaw plugins install genor-orchestrator`
2. Ensure the skill is installed: `clawhub install genor-orchestrator`
3. Start the dashboard: `pm2 start dashboard/server.py --name orchestration-dashboard --interpreter python3 -- 8766`
4. Set project context: `orchestrator_set_context(project="my-project", task="fix-bug")`

## Dashboard

Start the web UI for model management and routing:

```bash
pm2 start dashboard/server.py --name orchestration-dashboard --interpreter python3 -- 8766
```

Open http://localhost:8766

## Scripts

| Script | Purpose |
|--------|---------|
| `bash scripts/onboard.sh` | First-time setup |
| `bash scripts/init-project.sh <path> <name>` | Scaffold project |
| `bash scripts/check-models.sh [project]` | Check eligible models |
| `python3 scripts/auto-populate-models.py` | Populate models from config |
| `bash scripts/check-prices.sh` | Check model prices |
| `bash scripts/test-model.sh <id>` | Test model connectivity |

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
