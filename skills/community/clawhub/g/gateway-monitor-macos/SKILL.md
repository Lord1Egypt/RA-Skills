---
name: gateway-monitor-macos
description: Install and operate a local OpenClaw Gateway Monitor stack on macOS with LaunchAgent + watchdog. Use when setting up, repairing, or validating gateway-monitor services, including one-command install/uninstall/status and automatic launchctl registration.
---

# Gateway Monitor (macOS)

Run this skill when you need a reproducible install of gateway monitor + watchdog on macOS.

## Install

Run:

```bash
bash scripts/install.sh
```

What it does:
- Copy monitor files to `~/.openclaw/tools/gateway-monitor`
- Install/update LaunchAgents:
  - `ai.openclaw.gateway-monitor`
  - `ai.openclaw.gateway-watchdog`
- Reload both jobs with `launchctl`
- Verify monitor API health (`/api/summary`)

## Status

Run:

```bash
bash scripts/status.sh
```

## Uninstall

Run:

```bash
bash scripts/uninstall.sh
```

## Notes

- This skill targets macOS `launchd` only.
- Installer is idempotent: safe to run repeatedly.
- Backups of existing plists are written to `~/.openclaw/config-backups` before overwrite.
