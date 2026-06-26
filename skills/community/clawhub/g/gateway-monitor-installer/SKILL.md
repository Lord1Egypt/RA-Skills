---
name: gateway-monitor-installer
description: Install, update, run, and remove OpenClaw Gateway Monitor + Gateway Watchdog on macOS via LaunchAgent. Use when user asks to deploy one-click monitoring, recover broken gateway daemon automatically, check launchctl health, or uninstall monitor/watchdog services.
---

# Gateway Monitor Installer

Use bundled scripts for deterministic operations.

## Runbook

1. Install or update:

```bash
bash scripts/install.sh
```

2. Verify status:

```bash
bash scripts/status.sh
```

3. Uninstall cleanly:

```bash
bash scripts/uninstall.sh
```

## What `install.sh` does

- Copy monitor and watchdog binaries to `~/.openclaw/tools/gateway-monitor/bin/`
- Render LaunchAgent templates into `~/Library/LaunchAgents/`
- Backup existing plist files to `~/.openclaw/config-backups/`
- Bootstrap + enable + kickstart both agents
- Run post-install status check

## Services

- `ai.openclaw.gateway-monitor` → monitor UI server (`http://127.0.0.1:18990`)
- `ai.openclaw.gateway-watchdog` → periodic gateway self-healing check

## Notes

- Re-running `install.sh` is safe (idempotent)
- `watchdog` script expects OpenClaw CLI at `/opt/homebrew/bin/openclaw`
- If node path differs, edit `assets/bin/gateway-watchdog.sh` before install
