---
name: mission-control
description: CLI-first system health aggregator for autonomous AI agents. Query all agent processes, resources, cron jobs, and services in one shot. Use when a user asks for system status, agent health, resource monitoring, cron checks, or wants to restart/inspect autonomous systems (daemons, AOMS, VPS workers, cron jobs).
---

# Mission Control

## Overview

Single-command health aggregator for autonomous AI infrastructure. Replaces checking 5+ separate tools by collecting agent status, resource health, cron jobs, and service state into one report.

Designed for operators running autonomous agents (OpenClaw daemons, AOMS, VPS workers) who need a fast answer to "is everything OK?"

## Core Rules

- Read-only by default. Only `restart` mutates state and requires confirmation.
- Prefer `--json` output when piping to other tools or storing results.
- Do not invent OpenClaw CLI flags. Use only documented commands.
- When the user asks "what's running?" or "system status" - run `mctl status` for the full picture.

## Commands

### Full Status (default)
```bash
bash scripts/mctl.sh status
```
Returns: agents, resources (CPU/RAM/disk/GPU), cron jobs, services, OpenClaw status.

### Agent List
```bash
bash scripts/mctl.sh agents
```
Detects running processes matching: openclaw daemon, openclaw gateway, and any process with "agent", "daemon", "worker", or "aoms" in its name. Shows PID and uptime.

### Resource Health
```bash
bash scripts/mctl.sh health
```
CPU count, load average, RAM usage, disk usage, NVIDIA GPU (if present). Color-coded thresholds:
- Green: <60% usage
- Yellow: 60-80%
- Red: >80%

### Cron Jobs
```bash
bash scripts/mctl.sh cron
```
Lists OpenClaw cron jobs via `openclaw cron list`.

### Services
```bash
bash scripts/mctl.sh services
```
Checks systemd status for `openclaw-gateway` and `openclaw-daemon`. Also shows listening ports.

### View Logs
```bash
bash scripts/mctl.sh logs [service-name]
```
Shows last 50 lines from the past hour for a systemd service. Defaults to `openclaw-daemon`.

### Restart Service
```bash
bash scripts/mctl.sh restart <service-name>
```
Restarts a systemd service. Requires sudo. **Always confirm with the user before running.**

### JSON Output
Add `--json` to any command for machine-readable output:
```bash
bash scripts/mctl.sh --json status
```

## Usage Examples

### Quick daily check
```
User: "How's the system?"
Agent: runs `mctl status` and summarizes findings
```

### Debug a slow agent
```
User: "Why is my daemon slow?"
Agent: runs `mctl health` to check resources, then `mctl logs openclaw-daemon`
```

### Pre-deployment check
```
User: "Is everything healthy before I deploy?"
Agent: runs `mctl --json status`, checks for red flags, gives go/no-go
```

### Automated monitoring via cron
```bash
# Add to openclaw cron for daily checks
openclaw cron add --name "mission-control:daily" \
  --schedule "0 8 * * *" \
  --command "bash ~/.openclaw/skills/mission-control/scripts/mctl.sh --json status > /tmp/mctl-status.json"
```

## What Gets Checked

| Check | Source | Threshold |
|-------|--------|-----------|
| Agent processes | `pgrep` | Any running = green |
| CPU load | `/proc/loadavg` | >CPUs = yellow |
| RAM | `free -m` | >80% = red |
| Disk | `df -h /` | >85% = red |
| GPU/VRAM | `nvidia-smi` | Optional |
| Cron | `openclaw cron list` | Shows schedule |
| Services | `systemctl` | active/failed |
| Ports | `ss -ltnp` | Informational |

## Installation

No external dependencies. Requires:
- Bash 4+
- Standard Linux utilities (ps, free, df, ss)
- Optional: `nvidia-smi` for GPU, `openclaw` CLI for cron/status

```bash
# Install via ClawHub
clawhub install mission-control

# Or manually
cp -r . ~/.openclaw/skills/mission-control/
chmod +x ~/.openclaw/skills/mission-control/scripts/mctl.sh
```

## Integration with OpenClaw

Works with the existing OpenClaw ecosystem:
- **openclaw cron** - Schedule periodic health checks
- **openclaw status** - Included in full status report
- **openclaw daemon** - Monitored as an agent process
- **openclaw gateway** - Service health checked

## When to Use

- Daily health checks for autonomous systems
- Before deployments or major changes
- Debugging performance issues
- Quick "is everything running?" answer
- Automated monitoring via cron
- Post-incident verification

## Differences from mission-control-dashboard

| Feature | mission-control (this) | mission-control-dashboard |
|---------|----------------------|--------------------------|
| Interface | CLI / agent skill | Web UI (browser) |
| Use case | Quick status queries | Visual monitoring |
| Dependencies | Bash only | Python 3.8+ |
| Real-time | On-demand | Polling dashboard |
| Best for | AI agent queries | Human visual monitoring |

Use both together: this skill for agent-driven checks, the dashboard for visual monitoring.

## Author
Built for autonomous infrastructure operations.

## Price
**Free** on ClawHub

## Tags
#monitoring #agents #health #cli #devops #automation #infrastructure #status

## License
MIT
