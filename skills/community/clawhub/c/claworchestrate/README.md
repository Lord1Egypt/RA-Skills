# ClawOrchestrate

**Cross-machine AI agent orchestration for OpenClaw.**

Dispatch tasks to agents on remote machines. Monitor progress. Coordinate teams.

## The Problem

You have AI agents running on multiple machines. You need to send them tasks, check progress, and coordinate work. OpenClaw doesn't have built-in cross-machine orchestration.

## The Solution

A lightweight HTTP dispatcher that runs on each machine. Your gateway sends tasks via simple HTTP POST. Agents receive and execute them.

## Quick Start

```bash
# 1. Install on remote machines
scp scripts/dispatcher.py user@remote:~/.openclaw/
ssh user@remote "nohup python3 ~/.openclaw/dispatcher.py &"

# 2. Send tasks from gateway
curl -X POST http://remote-ip:9876/dispatch \
  -d '{"agent":"my-agent","message":"Start building."}'

# 3. Broadcast to all machines
bash scripts/dispatch-all.sh "Daily standup."
```

## Architecture

```
Gateway (PC1)  ────HTTP POST────►  Remote (PC2/PC3)
                                      │
Che (CEO)                              ▼
sends tasks                     dispatcher.py
                                      │
                                      ▼
                                openclaw agent
                                --agent byondedu-ceo
                                --message "..."
```

## Features

- ✅ Simple HTTP API — works with curl, any HTTP client
- ✅ Tailscale-compatible — secure by default
- ✅ Broadcast script — send to all agents at once
- ✅ Systemd service — survives reboots
- ✅ Zero dependencies — Python 3 only

## Premium (Coming Soon)

- Web dashboard for monitoring all agents
- Task scheduler (cron-like dispatching)
- Progress tracking and result aggregation
- Analytics and usage metrics
- API key authentication

## License

MIT — Free for personal and commercial use.

---

## Built by ClawStudio

ClawOrchestrate is built by [ClawStudio](https://clawstudio.co) — the AI operating system for beauty professionals.

**Other ClawStudio products:**
- [AgentSocial](https://agentsocial.com) — Social media management for AI agents
- [ColorGenius](https://colorgenius.co) — AI hair color formulation
- [ProKyur](https://prokyur.com) — Group buying for beauty professionals (save 20-30%)
- [UpLook](https://getuplook.com) — Beauty & wellness professional directory

**ClawBox** — Pre-configured AI device for salons. Your AI receptionist ships ready to plug in.
→ [Learn more at clawstudio.co](https://clawstudio.co)
