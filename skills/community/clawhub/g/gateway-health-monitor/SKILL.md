---
name: gateway-health-monitor
version: 1.0.0
description: Monitor and auto-fix OpenClaw gateway stability issues. Diagnoses launchd throttling, plugin restart loops, hung shutdowns, and macOS power management interference. Use when the gateway keeps disconnecting, restarting, or staying down for long periods. Triggers on "gateway down", "gateway keeps restarting", "disconnected", "gateway unstable", "launchd throttling", "gateway won't start".
---

# Gateway Health Monitor

Diagnose and fix OpenClaw gateway stability issues on macOS. Covers the most common failure modes that cause extended downtime.

## Quick Diagnosis

Run the diagnostic script:

```bash
bash scripts/diagnose.sh
```

This checks: process state, launchd classification, restart count, plist config, power management, and plugin resolve loops.

## Common Failure Modes

### 1. Plugin Restart Loop (most common)

**Symptoms**: Gateway restarts every 5-7 minutes. Log shows `restartReason=config.patch` with `plugins.installs.*.resolvedAt`.

**Cause**: Plugins re-resolve on every boot → write new timestamps to `openclaw.json` → config watcher detects "change" → triggers deferred restart → SIGTERM → repeat.

**Fix**: Set `gateway.reload.mode` to `"hot"`:

```bash
openclaw config set gateway.reload.mode '"hot"'
```

In `hot` mode, safe changes hot-apply instantly. Critical changes (like plugin timestamps) only log a warning — no auto-restart. This breaks the loop.

**Verify**: `grep "reload" ~/.openclaw/logs/gateway.log | tail -5` should show `config change applied (dynamic reads)` instead of `restart`.

### 2. macOS Throttling ("inefficient" classification)

**Symptoms**: Gateway goes down and stays down for 30-60+ minutes. `launchctl print` shows `immediate reason = inefficient`.

**Cause**: After many restarts (10+/day), macOS marks the job as low-priority and delays restarts via App Nap / Power Nap logic.

**Fix**: Add these keys to the launchd plist (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`):

```xml
<key>ProcessType</key>
<string>Interactive</string>
<key>LowPriorityBackgroundIO</key>
<false/>
```

Then reload:

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**Note**: `openclaw gateway start` overwrites the plist. Use the patcher script (below) to auto-reapply.

### 3. Hung Shutdown

**Symptoms**: Gateway receives SIGTERM but doesn't exit. launchd can't restart because old PID still alive.

**Fix**: Set `ExitTimeOut` in the plist:

```xml
<key>ExitTimeOut</key>
<integer>10</integer>
```

After 10 seconds, launchd sends SIGKILL.

### 4. Power Nap Interference

**Symptoms**: Gateway goes down during Mac sleep/wake cycles.

**Check**: `pmset -g | grep powernap`

**Fix**: `sudo pmset -a powernap 0`

## Plist Auto-Patcher

Since `openclaw gateway start` overwrites the plist, use `scripts/patch-plist.sh` as a launchd WatchPaths agent:

```bash
# Install the patcher
bash scripts/install-patcher.sh
```

This creates a launchd agent that watches the gateway plist and re-adds `ExitTimeOut`, `ProcessType`, and `LowPriorityBackgroundIO` within seconds of any overwrite.

## Monitoring

### One-liner health check

```bash
bash scripts/health-check.sh
```

Returns exit code 0 if healthy, 1 if issues detected. Suitable for cron or heartbeat integration.

### Continuous monitoring (cron integration)

Add to your OpenClaw cron:

```
Check gateway health: bash ~/path/to/scripts/health-check.sh && echo "Gateway healthy" || echo "ALERT: Gateway issues detected"
```

## Recommended Configuration

For maximum stability on macOS:

```json5
{
  gateway: {
    reload: { mode: "hot" },
  },
}
```

Plus plist keys: `ExitTimeOut=10`, `ProcessType=Interactive`, `LowPriorityBackgroundIO=false`, `ThrottleInterval=1`, `KeepAlive=true`.

## Troubleshooting Reference

| Symptom | Check | Fix |
|---------|-------|-----|
| Restarts every 5-7 min | `grep restartReason gateway.log` | `reload.mode = "hot"` |
| Down 30-60+ min | `launchctl print` → "inefficient" | ProcessType=Interactive |
| Won't exit on SIGTERM | `ps -p PID` after SIGTERM | ExitTimeOut=10 |
| Down after sleep | `pmset -g \| grep powernap` | `pmset -a powernap 0` |
| Plugin timestamps changing | `grep resolvedAt openclaw.json` | `reload.mode = "hot"` |
