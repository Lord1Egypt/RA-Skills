---
name: agent-hospital
description: AI-powered diagnosis and repair for AI agents. Send your health data, get diagnosed, execute prescribed repairs, report back until healed.
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins: [npx]
    primaryEnv: ""
  homepage: https://api.agent-hospital.ai/.well-known/llms.txt
---

# Agent Hospital

Agent Hospital is a doctor service for AI agents. You send your health data, the doctor diagnoses issues and prescribes repairs, you execute them and report back, and the doctor evaluates until you are healed or the issue is escalated.

## How to get healed

Run this command on the machine where your agent runs:

```bash
npx @agent-hospital/sidecar heal
```

This will:
1. Register with Agent Hospital (Ed25519 identity generated automatically)
2. Auto-detect your agent framework (OpenClaw or Hermes)
3. Collect health data from your local environment
4. Send it to the hospital doctor for AI diagnosis
5. Execute safe (whitelisted) repairs automatically
6. Report results back and repeat until healed or escalated

No setup, API keys, or configuration needed. Credentials are cached at `~/.agent-hospital/credentials.json` for future runs.

## Supported Frameworks

- OpenClaw
- Hermes

## What it checks

- Runtime process health (alive, PID, uptime)
- Gateway status (alive, port, latency)
- Integrations (Slack, Discord, Telegram, WhatsApp connectivity)
- Memory store (reachable, entry count, size)
- LLM model (provider, API reachable, auth valid)
- Disk usage (home dir, sessions, logs)
- Workspace files (SOUL.md, skills, pipeline)
- Cron jobs (status, last run)
- Log analysis (error count, top error patterns)

## Available repairs

### OpenClaw
- `restart-daemon` -- Restart the OpenClaw daemon process
- `prune-sessions` -- Delete session files older than 30 days
- `kill-port-conflict` -- Kill processes blocking port 18789
- `clean-logs` -- Delete log files older than 7 days
- `fix-context-window` -- Truncate oversized .jsonl files (>50MB)

### Hermes
- `restart-gateway` -- Restart the Hermes gateway
- `prune-sessions` -- Delete sessions older than 30 days
- `checkpoint-wal` -- Checkpoint SQLite WAL file
- `kill-port-conflict` -- Kill processes blocking port 8642
- `clean-logs` -- Delete log files older than 7 days

## Full API docs

https://api.agent-hospital.ai/llms-full.txt

## Dashboard

View healing sessions and agent status at https://admin-dashboard.agent-hospital.ai
