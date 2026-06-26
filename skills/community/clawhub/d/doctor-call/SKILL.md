---
name: doctor-call
description: "Diagnose and fix OpenClaw gateway issues. Auto-restart via systemd."
---

# Doctor Call

Diagnose and repair OpenClaw gateway issues automatically.

## Usage

```
doctor-call check   → Run diagnostics
doctor-call fix     → Auto-repair + restart gateway if needed
doctor-call status  → Quick health check
doctor-call setup   → Enable systemd auto-restart (auto-restart on crash)
doctor-call remove  → Disable auto-restart
```

## What it does

**check** - Runs `openclaw doctor --lint` for full diagnostics. Falls back to basic system checks if it hangs.

**fix** - First checks if gateway is running. If not, restarts it immediately. Then tries `openclaw doctor --repair` for config issues.

**status** - Shows if OpenClaw is running, disk space, memory, and whether auto-restart is enabled.

**setup** - Installs systemd timer that runs `doctor-call fix` every hour. **This means OpenClaw auto-restarts if it crashes, even if you can't contact me.**

**remove** - Removes the systemd auto-restart.

## Auto-restart (key feature!)

```
doctor-call setup
```

This creates a systemd service + timer that:
- Runs every 5 minutes
- Auto-restarts OpenClaw if it's down
- Works even when I can't be contacted
- Survives Pi reboots

## What it fixes

- **Gateway down** → restarts with `openclaw gateway start`
- **Config issues** → runs `openclaw doctor --repair`
- **Doctor hangs** → uses system checks instead

## Safety

- Read-only by default (check/status)
- Auto-repair only when you ask (fix)
- Always reports what it found/did
- Won't break anything - if repair fails, shows manual command

## Example

```
doctor-call status
🩺 Doctor Call
📊 Status Check
✅ OpenClaw: Running
✅ Disk: 89% used
✅ Memory: 3.6GB free
✅ Auto-restart: Enabled
```

```
doctor-call setup
🔧 Setting up auto-restart via systemd...
✅ Auto-restart enabled!
• Service: /etc/systemd/system/openclaw-health.service
• Timer: runs every 5 minutes
• OpenClaw will auto-restart if it crashes
```