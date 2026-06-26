---
name: openclaw-guardian
version: 1.0.2
description: >
  Production-hardened OpenClaw gateway watchdog. Monitors the gateway process
  using graduated health checks, performs escalating repairs (restart → doctor
  fix → optional git rollback), alerts via Telegram and/or Discord, commits
  daily snapshots, and runs as a native macOS launchd or Linux systemd service.
metadata:
  openclaw:
    homepage: https://github.com/openclaw/openclaw-guardian
    requires:
      bins:
        - openclaw
        - git
        - curl
    platforms:
      - darwin
      - linux
author: Forge ⚙️ (OpenClaw sub-agent)
---

# 🛡️ OpenClaw Guardian

A battle-hardened watchdog that keeps your OpenClaw gateway running — and tells you when it can't.

## What It Does

OpenClaw Guardian runs as a background service and continuously monitors the OpenClaw gateway using two independent health signals. When the gateway goes down, it works through an escalating repair sequence before entering a cooldown and waiting for manual help. Every significant event is logged and sent to your configured alert channel(s).

### Health Check Strategy (graduated)

1. **CLI check** — `openclaw gateway status` (the authoritative signal)
2. **HTTP fallback** — `curl http://localhost:${OPENCLAW_PORT}/health` (5s timeout)
3. Both must fail before the guardian considers the gateway truly down

### Repair Strategy (escalating)

| Level | Action | Trigger |
|-------|--------|---------|
| **1 — Restart** | `openclaw gateway restart` | First failure |
| **2 — Doctor Fix** | `openclaw doctor --fix` → `openclaw gateway start` | After Level 1 fails |
| **3 — Git Rollback** | Stash → reset to last stable commit → pop stash | After `GUARDIAN_MAX_REPAIR` failures, only if `GUARDIAN_ENABLE_ROLLBACK=true` |
| **Cooldown** | Sleep `GUARDIAN_COOLDOWN` seconds | After all levels exhausted |

> **Note:** Level 3 rollback is **off by default** and requires explicit opt-in via `GUARDIAN_ENABLE_ROLLBACK=true`. Even then, it always stashes uncommitted work before resetting — your changes are never silently discarded.

### Alerting

Guardian supports both Telegram and Discord simultaneously. If neither is configured, it runs in log-only mode.

**Alert events:**
- Guardian started / stopped
- Gateway down detected
- Each repair attempt (with level)
- Repair success / failure
- Rollback triggered
- All repairs exhausted (cooldown entered)

### Daily Snapshots

Once per calendar day, guardian runs `git add -A && git commit` in your workspace. It respects `.gitignore`, so secrets you've excluded stay excluded. Commit message format: `guardian: daily snapshot YYYY-MM-DD`.

---

## Quick Start

### 1. Configure environment variables

Create `~/.openclaw/guardian.env` (or export in your shell profile):

```bash
# Required for alerts — set at least one
export GUARDIAN_TELEGRAM_BOT_TOKEN="bot123456:ABC..."
export GUARDIAN_TELEGRAM_CHAT_ID="-1001234567890"
# OR
export GUARDIAN_DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# Optional tuning
export GUARDIAN_CHECK_INTERVAL=30
export GUARDIAN_MAX_REPAIR=3
export GUARDIAN_COOLDOWN=600
export GUARDIAN_ENABLE_ROLLBACK=false  # set true to enable git rollback
export GUARDIAN_WORKSPACE="$HOME/.openclaw/workspace"
export GUARDIAN_LOG="/tmp/openclaw-guardian.log"
export OPENCLAW_PORT=3578
```

### 2. Install as a system service

```bash
# macOS or Linux — auto-detects
./scripts/install-guardian.sh

# With a custom log path
GUARDIAN_LOG=/var/log/openclaw-guardian.log ./scripts/install-guardian.sh
```

### 3. Verify it's running

```bash
# macOS
launchctl list | grep openclaw

# Linux
systemctl --user status openclaw-guardian

# Both
tail -f /tmp/openclaw-guardian.log
```

### 4. Run manually (testing / foreground)

```bash
# Source your config first
source ~/.openclaw/guardian.env

# Run guardian in the foreground (Ctrl-C to stop)
./scripts/guardian.sh
```

### 5. Uninstall

```bash
./scripts/uninstall-guardian.sh
```

---

## Environment Variable Reference

| Variable | Default | Description |
|---|---|---|
| `GUARDIAN_CHECK_INTERVAL` | `30` | Seconds between health checks |
| `GUARDIAN_MAX_REPAIR` | `3` | Max Level 1+2 attempts before Level 3 |
| `GUARDIAN_COOLDOWN` | `600` | Cooldown sleep (seconds) after all repairs fail |
| `GUARDIAN_ENABLE_ROLLBACK` | `false` | Enable Level 3 git rollback (**off by default**) |
| `GUARDIAN_LOG` | `/tmp/openclaw-guardian.log` | Log file path (rotates at 1 MB) |
| `GUARDIAN_WORKSPACE` | `$HOME/.openclaw/workspace` | Path to the OpenClaw workspace git repo |
| `GUARDIAN_TELEGRAM_BOT_TOKEN` | _(unset)_ | Telegram Bot API token |
| `GUARDIAN_TELEGRAM_CHAT_ID` | _(unset)_ | Telegram chat or channel ID |
| `GUARDIAN_DISCORD_WEBHOOK_URL` | _(unset)_ | Discord incoming webhook URL |
| `OPENCLAW_PORT` | _(auto-detected)_ | Gateway HTTP port — auto-parsed from `openclaw gateway status` if not set |

---

## File Layout

```
skills/openclaw-guardian/
├── SKILL.md                    ← this file
└── scripts/
    ├── guardian.sh             ← main watchdog (run continuously)
    ├── install-guardian.sh     ← sets up launchd / systemd service
    └── uninstall-guardian.sh   ← clean removal
```

**Runtime files** (created automatically, not committed):

| File | Purpose |
|------|---------|
| `/tmp/openclaw-guardian.lock` | Single-instance lockfile containing PID |
| `/tmp/openclaw-guardian-last-snapshot` | Date of last successful daily snapshot |
| `/tmp/openclaw-guardian.log` | Current log (rotated to `.log.1` at 1 MB) |

---

## How It Improves on myclaw-guardian

| Issue in myclaw-guardian | Fix in openclaw-guardian |
|---|---|
| `git reset --hard` without stashing — could silently destroy uncommitted work | Always `git stash` before any reset; `git stash pop` to restore regardless of outcome |
| Process detection via `pgrep` — fragile, can match wrong process | Uses `openclaw gateway status` (the actual CLI) as primary, with HTTP fallback |
| No lockfile — multiple instances could run simultaneously | `/tmp/openclaw-guardian.lock` with PID written; stale lock detection on startup |
| Only Discord alerts | Supports Telegram **and** Discord simultaneously; log-only if neither configured |
| Level 3 rollback always enabled — risky default | Level 3 off by default (`GUARDIAN_ENABLE_ROLLBACK=false`), explicit opt-in required |
| No graduated health checking | Two independent checks: CLI → HTTP; both must fail before declaring gateway down |
| No cooldown after exhausting repairs | Configurable cooldown (`GUARDIAN_COOLDOWN`) before resuming monitoring |

---

## Logging

Logs are timestamped and structured:

```
[2026-03-05 11:30:00] [INFO] OpenClaw Guardian started (PID 12345)
[2026-03-05 11:30:30] [INFO] Gateway healthy
[2026-03-05 11:31:00] [WARN] CLI status check failed — trying HTTP health endpoint
[2026-03-05 11:31:05] [WARN] Gateway health check FAILED
[2026-03-05 11:31:05] [INFO] ALERT: 🔴 Gateway is DOWN — beginning repair sequence
[2026-03-05 11:31:05] [INFO] Repair Level 1: restarting gateway
[2026-03-05 11:31:35] [INFO] Level 1 repair succeeded
```

Log rotates automatically when it exceeds 1 MB (one backup: `.log.1`).

---

## Security Notes

- **No secrets in git** — daily snapshots use `git add -A` which respects `.gitignore`. Ensure your `.gitignore` excludes `.env`, `*.key`, etc.
- **Level 3 rollback is destructive by nature** — only enable it if you understand git reset semantics and have tested your `.gitignore` coverage.
- **Alert tokens in env only** — never put `GUARDIAN_TELEGRAM_BOT_TOKEN` or webhook URLs in files that get committed.
