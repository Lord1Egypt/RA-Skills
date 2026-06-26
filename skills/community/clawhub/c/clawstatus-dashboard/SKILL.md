---
name: clawstatus-dashboard
description: Install, update, run, and verify the public ClawStatus dashboard from GitHub. Use when an agent needs to deploy ClawStatus locally or on a LAN host, refresh an existing checkout, restart the user service, or verify the dashboard is reachable on port 8900.
---

# ClawStatus Dashboard

Install or refresh ClawStatus from the public GitHub repo, then verify that the dashboard is reachable.

The published dashboard includes:
- 15-day daily token actual-consumption chart
- active/passive token split
- modal model switching for Overview agents and Cron jobs
- cron frequency display (human-readable, e.g. 每天 07:00) and manual run trigger button
- disabled cron jobs are automatically hidden
- lastStatus color coding: ok = green, error = red
- next-run displayed as countdown (e.g. 5m30s)
- CN/EN language toggle with persistent preference
- OpenClaw status color coding (green/yellow/red)
- configurable refresh speed (Fastest/Fast/Medium/Slow)
- Bootstrap-free (no CDN dependency)

## Quick start

1. Run `scripts/install_or_update.sh [target-dir]` to clone or update the repo and install it in editable mode.
2. Start or restart the app:
   - foreground: `clawstatus --host 0.0.0.0 --port 8900 --no-debug`
   - systemd user service: `systemctl --user restart clawstatus.service`
3. Verify access:
   - local: `curl -I http://127.0.0.1:8900/`
   - LAN: `curl -I http://<lan-ip>:8900/`

## Workflow

### Install or update

- Use `scripts/install_or_update.sh` for normal setup.
- Default target directory is `~/ClawStatus`.
- The script clones `https://github.com/NeverChenX/ClawStatus.git` when missing, otherwise fast-forwards the existing checkout.

### Run

Choose one:

- Foreground command for quick manual runs.
- `systemctl --user restart clawstatus.service` when the host already has a user service definition.

### Verify

Always verify with HTTP response headers after install or restart.

If you need command examples, read `references/commands.md`.
