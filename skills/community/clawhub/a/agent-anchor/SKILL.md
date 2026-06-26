# Agent Anchor

Crash-proof dashboard for OpenClaw. Your AI agent's memory that survives everything.

## Description

Agent Anchor keeps your OpenClaw agent running smoothly — even through crashes, restarts, and interruptions. It continuously snapshots state so your agent resumes exactly where it left off.

## Features

- **Crash Recovery** — Automatically saves state every 3 minutes. Never lose context on restart.
- **Task Tracker** — Organize tasks into In Progress, Staged, and Completed
- **Terminal View** — See live system status, connection health, agent activity
- **Cron Job Monitoring** — Monitor scheduled jobs, click to see details, fix errors with one click
- **Activity Calendar** — Look back at your agent's history by date
- **Click-to-Expand** — Inspect any task or cron job for full details

## Installation

```bash
cd ~/workspace
git clone <agent-anchor-repo>
cd agent-anchor
python3 -m http.server 3456
```

Then open http://localhost:3456

## Requirements

- OpenClaw installation
- Python 3 for local server
- Web browser for dashboard

## Configuration

Edit `state-anchor.json` to customize:
- Task categories (inProgress, staged, completed)
- Revenue streams
- Contacts (hot, warm, cold)
- Cron jobs to monitor

## Price

$19 one-time (Stripe) or $19 USDC (Base network)

## Support

DM @theia_metariot on X/Twitter

---

Built by MetaRiot — Culture for the decentralized age.