# Daily Backup System

Automated daily backup of your entire OpenClaw setup with rotation and restore guide.

Use when: you want automatic backups of your OpenClaw configuration, agent workspaces, API keys, scripts, and data — with a one-command restore process.

## What it does

Runs daily via cron and creates a compressed backup of:
- `openclaw.json` — all agent configs, bindings, channels, crons
- All agent workspaces (SOUL.md, TOOLS.md, memory/, scripts/)
- Environment files (.env with API keys)
- Custom scripts and data pipelines
- Reverse proxy config (Caddy/Nginx)

## Features

- **Compressed tar.gz** — typically 200-500MB for a full 12-agent setup
- **7-day rotation** — keeps last 7 backups, auto-deletes older ones
- **Restore guide** — auto-generated RESTORE_GUIDE.md with step-by-step instructions
- **Excludes noise** — skips node_modules, __pycache__, session transcripts (too large, regenerated)
- **Zero downtime** — runs in background, doesn't interrupt the gateway

## Setup

1. Copy `daily_backup.sh` to your scripts directory
2. Edit the workspace paths to match your setup
3. Add cron: `0 3 * * * /bin/bash /path/to/daily_backup.sh >> /tmp/backup.log 2>&1`

## Restore (disaster recovery)

```bash
# On a fresh VPS
curl -fsSL https://openclaw.ai/install.sh | bash
cd / && tar xzf openclaw-full-backup-YYYY-MM-DD.tar.gz
openclaw gateway start
```

Full system restored in under 10 minutes.

## Tags
backup, disaster-recovery, devops, security, automation, cron, restore
