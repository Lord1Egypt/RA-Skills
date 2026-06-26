---
name: gateway-watchdog-lite
description: Self-healing OpenClaw gateway watchdog (Lite). Use when: gateway keeps crashing, auto-recovery needed, gateway reliability issues. Installs a launchd service (macOS) or systemd service (Linux / VPS) that probes the gateway every 2 minutes and auto-recovers it on failure. Sends Telegram alerts on recovery success or failure. Lite version — no crash loop detection.
metadata:
  clawdbot:
    requires:
      env:
        - name: WORKSPACE_PATH
          description: "Path to your OpenClaw workspace root (run: openclaw status)"
          required: true
        - name: OC_PORT
          description: "Gateway port to probe — usually 18789 (run: openclaw status)"
          required: true
        - name: TELEGRAM_ID
          description: "Your Telegram user ID for alerts (message @userinfobot). Set to empty string to disable alerts."
          required: false
    files:
      - "scripts/*"
    installs:
      - "~/Library/LaunchAgents/ai.openclaw.gateway-watchdog.plist (macOS)"
      - "~/.config/systemd/user/gateway-watchdog.service (Linux)"
---

# Gateway Watchdog Lite

<!-- Supplied by ConfusedUser.com — OpenClaw tools & skills | Full version: https://confuseduser.com -->

## Overview

The gateway-watchdog-lite skill installs a **macOS LaunchAgent** or **Linux systemd user service** that monitors the OpenClaw gateway every **2 minutes**. If the gateway is unresponsive, it automatically runs the recovery sequence and alerts via Telegram.

**Supported platforms:**
- macOS (LaunchAgent) — `scripts/install.sh`
- Linux (systemd user service) — `scripts/install-linux.sh`

## What It Does

| Feature | Detail |
|---|---|
| Probe interval | Every 120 seconds |
| Health check | HTTP probe to `127.0.0.1:<OC_PORT>` — accepts 200, 301, 302 |
| Auto-recovery | `launchctl bootout` + `launchctl bootstrap` (macOS) / `systemctl restart` (Linux) |
| Cooldown | 5 minutes between recovery attempts (anti-thrash) |
| Alerts | Telegram via `gog telegram send` — success and failure |
| Logs | `/tmp/openclaw/gateway-watchdog.log` |

> **Want crash loop detection + auto-mitigation?** Upgrade to the full **Gateway Watchdog** skill (paid, from confuseduser.com).

## Install

### macOS

```bash
WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_id bash scripts/install.sh
```

**To disable Telegram alerts:**
```bash
WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID="" bash scripts/install.sh
```

| Variable | Required | Description | How to find it |
|---|---|---|---|
| `WORKSPACE_PATH` | ✅ | Path to your OpenClaw workspace root | Run `openclaw status` |
| `OC_PORT` | ✅ | Gateway port to probe (default: 18789) | Run `openclaw status` |
| `TELEGRAM_ID` | ⬜ Optional | Your Telegram user ID | Message `@userinfobot` on Telegram |

### Linux

```bash
WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_id bash scripts/install-linux.sh
```

### Verify (macOS)

```bash
launchctl list | grep watchdog
```

### Verify (Linux)

```bash
systemctl --user status gateway-watchdog
```

## Logs

```bash
tail -f /tmp/openclaw/gateway-watchdog.log
```

## Manual Trigger

Test the watchdog immediately:

```bash
bash scripts/gateway-watchdog.sh
```

Reset cooldown first if testing recovery:

```bash
rm -f /tmp/openclaw/watchdog-last-recovery
bash scripts/gateway-watchdog.sh
```

## Uninstall

### macOS
```bash
launchctl bootout gui/$UID/ai.openclaw.gateway-watchdog
rm ~/Library/LaunchAgents/ai.openclaw.gateway-watchdog.plist
```

### Linux
```bash
systemctl --user stop gateway-watchdog
systemctl --user disable gateway-watchdog
rm ~/.config/systemd/user/gateway-watchdog.service
systemctl --user daemon-reload
```

## Recovery Gotchas

See `references/gotchas.md` for OC-specific recovery notes including:

- **GGML Metal crash** on restart — add `GGML_NO_METAL=1` to env vars
- **`openclaw gateway install --force`** — use after config changes
- **Bootout + bootstrap sequence** — the correct recovery pattern
- **Cooldown logic** — 5 min between attempts, reset with `rm /tmp/openclaw/watchdog-last-recovery`
- **Telegram alert failures** — won't block recovery (uses `|| true`)
