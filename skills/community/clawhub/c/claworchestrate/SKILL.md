---
name: claworchestrate
description: Orchestrate AI agents across multiple machines. Dispatch tasks, monitor progress, and coordinate teams from a central gateway. Works over Tailscale, SSH, or any network.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
---

# ClawOrchestrate

**Cross-machine AI agent orchestration for OpenClaw.**

Dispatch tasks from one machine to agents running on another. Monitor progress. Coordinate teams.

## What It Does

- Send tasks to agents on remote machines via HTTP
- Trigger local `openclaw agent` commands on remote hosts
- Simple REST API — works with curl, any HTTP client
- Tailscale-compatible (secure by default)

## Quick Start

### 1. Install the dispatcher on remote machines (PC2, PC3, etc.)

```bash
# Copy dispatcher to remote machine
scp scripts/dispatcher.py user@remote-host:~/.openclaw/dispatcher.py

# Start the dispatcher
ssh user@remote-host "nohup python3 ~/.openclaw/dispatcher.py &"
```

### 2. Send tasks from your gateway machine (PC1)

```bash
# Dispatch to an agent
curl -X POST http://remote-ip:9876/dispatch \
  -H 'Content-Type: application/json' \
  -d '{"agent":"byondedu-ceo","message":"Read TASKS.md and start building."}'

# Check health
curl http://remote-ip:9876/health
```

### 3. Automate with scripts

```bash
# Dispatch to all teams
bash scripts/dispatch-all.sh "Daily standup — report progress."
```

## Architecture

```
┌─────────────┐     HTTP POST      ┌─────────────┐
│   PC1       │ ─────────────────► │   PC2       │
│  (Gateway)  │                    │  (Remote)   │
│             │                    │             │
│  Che (CEO)  │    :9876/dispatch  │  ByondEdu   │
│  sends task │                    │  AgentSocial│
└─────────────┘                    └─────────────┘
                                          │
                                   dispatcher.py
                                          │
                                   openclaw agent
                                   --agent byondedu-ceo
                                   --message "..."
```

## Setup as Systemd Service (Persistent)

On each remote machine:

```bash
cat > ~/.config/systemd/user/agent-dispatcher.service << 'EOF'
[Unit]
Description=ClawOrchestrate Agent Dispatcher
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/%u/.openclaw/dispatcher.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable agent-dispatcher
systemctl --user start agent-dispatcher
```

## API Reference

| Endpoint | Method | Body | Response |
|---|---|---|---|
| `/dispatch` | POST | `{"agent":"id","message":"text"}` | `{"status":"dispatched","agent":"id"}` |
| `/health` | GET | — | `{"status":"ok"}` |

## Security

- Runs on Tailscale network only (not exposed to internet)
- No authentication (Tailscale provides network-level auth)
- Add API key auth for public deployments (see docs/SECURITY.md)

## Files

- `scripts/dispatcher.py` — The HTTP server (run on remote machines)
- `scripts/dispatch-all.sh` — Broadcast script (run on gateway)
- `scripts/setup-service.sh` — Systemd service installer
- `docs/ARCHITECTURE.md` — Full architecture details
- `docs/SECURITY.md` — Security hardening guide

## License

MIT — Free for personal and commercial use.
Premium features (dashboard, scheduler, analytics) available at claworchestrate.com.
