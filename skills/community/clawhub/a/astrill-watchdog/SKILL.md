# astrill-watchdog

Monitors Astrill VPN on Ubuntu (deb GUI package) and automatically restarts it when the StealthVPN tunnel drops.

## What it does

Watches `tun0` + ping every 30 seconds. On failure, performs a full Astrill restart:
- `pkill astrill` kills the process tree (root-owned children `asproxy`/`asovpnc` die with the parent — no sudo needed)
- `setsid /autostart` relaunches Astrill with the full desktop environment (`DISPLAY`, `DBUS`, `WAYLAND_DISPLAY`) so it can initialize its GUI/Wayland stack from a systemd service context
- Astrill auto-connects to the last used server

On restart failure: logs a CRITICAL block, resumes checking next cycle. Never exits.

## Requirements

- Ubuntu Linux, Astrill deb GUI package (`/usr/local/Astrill/astrill`)
- `ping`, `ip`, `pgrep`, `pkill`, `setsid` (Ubuntu defaults)
- Active desktop session (DISPLAY/DBUS/WAYLAND) — required for Astrill relaunch

## Installation

```bash
bash setup.sh
```

No sudo. Installs the watchdog, creates a systemd user unit, and starts the service. Enabled on login automatically.

## Usage

```bash
astrill-watchdog.sh start    # start watchdog (also done by systemd on login)
astrill-watchdog.sh stop     # stop watchdog
astrill-watchdog.sh status   # health summary + last 20 log lines
astrill-watchdog.sh once     # single health check + restart if needed, then exit
```

## Files

| Path | Purpose |
|------|---------|
| `~/.config/astrill-watchdog/astrill-watchdog.sh` | Watchdog script |
| `~/.config/systemd/user/astrill-watchdog.service` | Systemd user unit |
| `~/.local/state/astrill-watchdog/watchdog.log` | Log file (rotates at 5000 lines) |
| `~/.local/state/astrill-watchdog/watchdog.pid` | PID file |

## Configuration

Edit the config block at the top of `astrill-watchdog.sh`:

```bash
CHECK_INTERVAL=30      # seconds between health checks
RECONNECT_WAIT=60      # seconds to wait after restart before health check
PING_HOST="8.8.8.8"
PING_COUNT=3
PING_TIMEOUT=3
LOG_MAX_LINES=5000
```

After editing, restart: `systemctl --user restart astrill-watchdog.service`

## Diagnostics

```bash
# Live log tail
tail -f ~/.local/state/astrill-watchdog/watchdog.log

# Systemd journal
journalctl --user -u astrill-watchdog.service -n 30

# Full status summary
astrill-watchdog.sh status
```
