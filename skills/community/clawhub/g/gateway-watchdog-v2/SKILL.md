---
name: gateway-watchdog
description: Production-grade bash watchdog for the OpenClaw gateway. Runs via launchd every 5 minutes. Handles boot grace periods, progressive retry with backoff, port-level fallback checks, stale PID detection, and restart cooldowns — preventing restart loops while keeping the gateway reliably alive.
---

# gateway-watchdog

Keeps the OpenClaw gateway alive without killing it during startup. Five defensive layers prevent false restarts and restart loops.

## How It Works

1. **HTTP check** — pings `http://127.0.0.1:18789`; exits immediately if the gateway responds
2. **Boot grace** — if the process is <180s old, waits without acting (avoids killing a booting gateway)
3. **Port check** — if the port is bound but HTTP is slow, waits up to 15s for recovery
4. **Progressive retry** — 3 retries at 15s / 30s / 45s intervals
5. **Cooldown** — enforces a 10-minute gap between restarts to prevent loops

Logs go to `~/.openclaw/logs/watchdog.log`.

## Setup (macOS launchd)

Create `~/Library/LaunchAgents/com.openclaw.gateway-watchdog.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway-watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/skills/gateway-watchdog/scripts/gateway-watchdog.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then load it:

```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.gateway-watchdog.plist
```

## Usage (manual)

```bash
bash scripts/gateway-watchdog.sh
```

## Requirements

- macOS (uses `launchctl`, `lsof`, `date -j`)
- `curl` in PATH
- OpenClaw gateway running under `launchd` as `ai.openclaw.gateway`
