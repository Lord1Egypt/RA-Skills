---
name: flowclaw
version: 1.1.3
description: YAML-driven workflow orchestrator for AI agent teams with human-in-the-loop approval gates. Includes optional Notion, n8n, and Discord integrations.
platforms:
  - macOS
  - Linux
metadata:
  openclaw:
    requires:
      env:
        - WORKFLOW_EXECUTOR_API_KEY
      optionalEnv:
        - NOTION_API_KEY
        - DISCORD_BOT_TOKEN
        - N8N_API_KEY
        - OPENCLAW_GATEWAY_URL
---

# FlowClaw

YAML-driven workflow orchestrator for OpenClaw agent teams. Connects Notion → n8n → agents, with approval gates so nothing runs without your go-ahead.

## What It Does

FlowClaw is a workflow execution engine that:
1. Receives task triggers from n8n (via Notion polling)
2. Loads the appropriate YAML workflow definition
3. Executes each step by dispatching to specialized AI agents
4. Pauses at approval gates and waits for human sign-off
5. Reports progress via Discord notifications

## Requirements

- Python 3.8+
- OpenClaw with configured agents
- n8n (optional — only needed for n8n-triggered workflows)
- Notion workspace with task database (optional — only needed for Notion sync)

## Setup

1. Copy `config/example.env` to `.env` and fill in your API keys
2. Install: `pip3 install -r src/requirements.txt`
3. Start: `python3 src/workflow-executor.py`
4. Import `src/n8n-workflow.json` into your n8n instance
5. Update n8n credential/ID placeholders with your values — see [INTEGRATION-STEPS.md](docs/INTEGRATION-STEPS.md)

## Configuration

All configuration is via environment variables. See `config/example.env` for the full list.

Key variables:
- `WORKFLOW_EXECUTOR_API_KEY` — API key for authenticating requests
- `NOTION_API_KEY` — Notion integration token (starts with `secret_...`)
- `DISCORD_BOT_TOKEN` — Discord bot token for notifications (optional)
- `PORT` — Server port (default: 8765)
- `MAX_WORKERS` — Gunicorn worker count (default: 4, recommended: 2× CPU cores)
