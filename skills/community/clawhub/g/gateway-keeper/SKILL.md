---
name: gateway-keeper
description: >
  OS-level watchdog that monitors OpenClaw gateway health and auto-restarts on crash.
  After restart, triggers session recovery so interrupted work resumes automatically.
  Use when setting up gateway reliability, crash recovery, auto-restart, or watchdog
  monitoring for OpenClaw deployments. Supports Windows (Task Scheduler + PowerShell)
  and Linux/macOS (systemd/cron + bash). Triggers: "gateway-keeper", "watchdog",
  "gateway health", "auto-restart gateway", "crash recovery".
---

# Gateway Keeper

OS-level watchdog for OpenClaw gateway. Runs **outside** the gateway process so it survives crashes.

## How It Works

1. **Health check** — Runs `openclaw gateway status` every 15 minutes
2. **Auto-restart** — If gateway is down, runs `openclaw gateway start`
3. **Recovery signal** — Writes `logs/gateway-recovery.json` with crash timestamp
4. **Session recovery** — HEARTBEAT.md template detects recovery file, prompts agent to check incomplete work

## Quick Setup

### Install

Run the appropriate install script for your OS:

**Windows (PowerShell as Admin):**
```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>/scripts/install.ps1"
```

**Linux/macOS:**
```bash
bash "<skill-dir>/scripts/install.sh"
```

### Uninstall

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>/scripts/uninstall.ps1"
```

**Linux/macOS:**
```bash
bash "<skill-dir>/scripts/uninstall.sh"
```

## Recovery Protocol

After gateway restart, the agent should check `logs/gateway-recovery.json`:

```json
{
  "crashed_at": "2026-02-26T00:00:00Z",
  "restarted_at": "2026-02-26T00:15:00Z",
  "restarted_by": "gateway-keeper"
}
```

Add to HEARTBEAT.md (done automatically by install script):

```markdown
## Gateway Crash Recovery
If `logs/gateway-recovery.json` exists:
1. Read crash timestamp
2. List all active sessions/sub-agents
3. Check each for incomplete work
4. Resume or retry as needed
5. Delete the recovery file when done
```

## Files

| File | Purpose |
|------|---------|
| `scripts/check-gateway.ps1` | Windows health check + restart |
| `scripts/check-gateway.sh` | Linux/macOS health check + restart |
| `scripts/install.ps1` | Windows Task Scheduler setup |
| `scripts/install.sh` | Linux/macOS cron/systemd setup |
| `scripts/uninstall.ps1` | Windows cleanup |
| `scripts/uninstall.sh` | Linux/macOS cleanup |

## Customization

Edit check interval by modifying the scheduled task/cron entry. Default: 15 minutes.

To change recovery behavior, edit the HEARTBEAT.md recovery section.
