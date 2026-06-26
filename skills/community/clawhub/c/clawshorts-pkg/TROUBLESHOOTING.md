# ClawShorts Troubleshooting Guide

## Common Issues

### Daemon Keeps Dying / Restarting Repeatedly

**Symptom:** The ClawShorts daemon restarts every 30-90 seconds, cycling continuously. Logs show "Shutdown requested (signal 15)" followed by immediate restart.

**Root Cause:** The LaunchAgent plist uses `ThrottleInterval` inside `KeepAlive`, which conflicts with launchd's restart behavior.

**Bad plist configuration:**
```xml
<key>KeepAlive</key>
<dict>
    <key>ThrottleInterval</key>
    <integer>60</integer>
</dict>
```

`ThrottleInterval` tells launchd "wait 60 seconds before restarting if this job dies." But combined with `KeepAlive`, this creates a restart cycle where launchd repeatedly kills and restarts the job with no useful polling happening between restarts.

**Fix:** Use `KeepAlive: true` without ThrottleInterval:
```xml
<key>KeepAlive</key>
<true/>
```

This tells launchd "keep this running indefinitely, restart immediately if it dies." No throttle logic.

**Verification:**
```bash
# Check if daemon is cycling
tail -f ~/.clawshorts/daemon.log

# Look for repeated "Shutdown requested (signal 15)" + "ClawShorts started" cycles

# Check daemon uptime (should be stable, not restarting every minute)
ps aux | grep clawshorts-daemon
ps -p <PID> -o etime  # elapsed time since start
```

**Workaround if launchctl remains unstable:** Run the daemon manually with nohup:
```bash
nohup python3 /path/to/clawshorts-daemon.py 192.168.1.100 --daily-limit 300 --debug > ~/.clawshorts/daemon.log 2>&1 &
```
The nohup approach bypasses launchd entirely and provides rock-solid stability.

---

### Time Not Accumulating / Shorts Not Detected

**Symptom:** You're watching YouTube Shorts but the counter stays at 0 or doesn't increase.

**How Detection Works:**

The daemon checks the UI every 3 seconds via ADB:
1. Dumps the UI hierarchy with `uiautomator dump /sdcard/ui.xml`
2. Finds the **focused element** (the active video player)
3. Measures its pixel width
4. Compares to screen width (1920x1080 on Fire TV):

| Focused Width | Interpretation | Counts Time? |
|--------------|----------------|--------------|
| < 1728px (< 90%) | YouTube Shorts (portrait 9:16, centered) | ✅ YES |
| >= 1728px (>= 90%) | Regular YouTube video (full screen landscape) | ❌ NO |
| Not YouTube app | Fire TV Home / other app | ❌ NO |

**Debugging Steps:**
```bash
# Manually check what's on screen
adb -s 192.168.1.100 shell "uiautomator dump /sdcard/ui.xml"
adb -s 192.168.1.100 pull /sdcard/ui.xml /tmp/ui.xml
grep -o 'focused="true"[^>]*bounds="[^"]*"' /tmp/ui.xml

# Check what app is in foreground
adb -s 192.168.1.100 shell "dumpsys activity activities | grep -E mResumedActivity"

# Verify YouTube is the active app
adb -s 192.168.1.100 shell "dumpsys activity activities | grep -i youtube"
```

**Why time might not be accumulating:**
1. You're on the Fire TV Home screen, not YouTube
2. You're watching regular YouTube videos (full screen), not Shorts
3. YouTube app is open but nothing is playing
4. You've already hit your daily limit (300s by default)

**Verify the database:**
```bash
sqlite3 ~/.clawshorts/clawshorts.db "SELECT * FROM daily_usage WHERE date = date('now', 'localtime');"
```
If this shows 300+ seconds, you've hit your limit.

---

### ADB Device Not Found / Connection Lost

**Symptom:** `adb devices` shows nothing, or Fire TV disconnects repeatedly.

**Solutions:**
```bash
# Reconnect
adb kill-server && adb start-server
adb connect 192.168.1.100:5555

# Verify connection
adb devices
```

The daemon has built-in auto-reconnect: if ADB connection drops, it automatically tries to reconnect on the next poll cycle.

---

### Daily Limit Not Resetting

The limit resets at midnight local time automatically. The daemon detects day changes and resets the counter.

If you need to reset manually:
```bash
sqlite3 ~/.clawshorts/clawshorts.db "UPDATE daily_usage SET seconds = 0 WHERE date = date('now', 'localtime');"
```

---

## Verifying Installation

After installing, verify everything works:

```bash
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh status
```

This does a **live verification** showing:
- Daemon status (🟢 active / 🔴 not running / 🟡 idle)
- Current screen info (app, focused element width, Shorts vs regular)
- Today's usage vs limit

If daemon shows 🔴, run:
```bash
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh start
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh status  # verify again
```

## Debug Mode

Enable debug logging to see every UI poll:
```bash
# Run with --debug flag
nohup python3 /path/to/clawshorts-daemon.py 192.168.1.100 --daily-limit 300 --debug > ~/.clawshorts/daemon.log 2>&1 &
```

Debug output shows:
- Screen size detection
- Focused element width on each poll
- Delta seconds added to the counter
- Whether Shorts or regular video is detected

---

## LaunchAgent Plist Reference

**Location:** `~/Library/LaunchAgents/com.fink.clawshorts.plist`

**Working configuration:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fink.clawshorts</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>/Users/username/.openclaw/workspace/skills/clawshorts/scripts/clawshorts-daemon.py</string>
        <string>192.168.1.100</string>
        <string>--daily-limit</string>
        <string>300</string>
        <string>--debug</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/username/.clawshorts.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/username/.clawshorts.log</string>
</dict>
</plist>
```

---

## File Locations

| File | Purpose |
|------|---------|
| `~/.clawshorts/clawshorts.db` | SQLite database with daily usage |
| `~/.clawshorts/daemon.log` | Debug log from the daemon |
| `~/.clawshorts.log` | LaunchAgent stdout/stderr (if using plist) |
| `~/.clawshorts/ui-<IP>.xml` | Last UI hierarchy dump |
| `~/Library/LaunchAgents/com.fink.clawshorts.plist` | macOS LaunchAgent plist |

---

## Database Schema

```sql
CREATE TABLE daily_usage (
    ip      TEXT NOT NULL,
    date    TEXT NOT NULL,
    seconds REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY (ip, date)
);
```

Query today's usage:
```bash
sqlite3 ~/.clawshorts/clawshorts.db "SELECT * FROM daily_usage WHERE date = date('now', 'localtime');"
```
