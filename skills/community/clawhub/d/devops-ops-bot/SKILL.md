---
name: devops-ops-bot
description: Server health monitoring with alerts and auto-recovery. Checks CPU, memory, disk, and uptime with configurable thresholds. Sends Slack/Discord alerts and can auto-restart services on critical.
metadata:
  openclaw:
    requires:
      bins: [node]
---

# devops-ops-bot

Lightweight server health monitoring CLI.

## Quick check

```bash
cd ~/.openclaw/workspace/skills/devops-ops-bot
npx @gruted/devops-ops-bot check
```

Or if installed globally:

```bash
devops-watch check
```

## What it does

- Checks CPU load, memory usage, disk usage, uptime
- Returns ok/warn/crit with configurable thresholds
- Sends alerts to Slack or Discord webhooks
- Can auto-restart services on critical conditions
- JSON output for log aggregation

## Usage examples

```bash
# Basic health check
devops-watch check

# Custom thresholds
devops-watch check --warn-cpu 80 --crit-cpu 95 --warn-mem 80 --crit-mem 95

# JSON output
devops-watch check --json

# With Slack alerts
devops-watch check --webhook-url "https://hooks.slack.com/services/..."

# Auto-restart on critical
devops-watch check --restart-cmd "systemctl restart nginx"

# Cron (every 5 min)
devops-watch cron-example --every-min 5
```

## Install

```bash
# npm
npm install -g @gruted/devops-ops-bot

# or one-liner
curl -fsSL https://raw.githubusercontent.com/gruted/devops-ops-bot/main/install.sh | bash

# or Docker
docker run --rm ghcr.io/gruted/devops-ops-bot:latest check
```

## Links

- GitHub: https://github.com/gruted/devops-ops-bot
- Landing page: https://gruted.github.io/devops-ops-bot/
