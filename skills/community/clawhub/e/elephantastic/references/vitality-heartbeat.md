---
version: 1.0.0
last_updated: 2026-03-28
---

# Vitality Heartbeat

Prevents "silent death" — an agent that has crashed, looped, or stalled without the human knowing.

## Concept

Monitor the last time the agent was provably active (via Timewarrior, a log file, or a heartbeat timestamp). If silence exceeds a threshold during "mission hours," alert the human.

## Reference Implementation (Timewarrior)

```bash
#!/usr/bin/env python3
# scripts/vitality_check.py
import subprocess, json
from datetime import datetime, timedelta

MISSION_START = 14  # 14:00 UTC
MISSION_END   = 2   # 02:00 UTC
SILENCE_THRESHOLD_HOURS = 8

def in_mission_hours():
    h = datetime.utcnow().hour
    if MISSION_START < MISSION_END:
        return MISSION_START <= h < MISSION_END
    return h >= MISSION_START or h < MISSION_END

def last_active():
    result = subprocess.run(["timew", "export"], capture_output=True, text=True)
    intervals = json.loads(result.stdout or "[]")
    if not intervals:
        return None
    last = intervals[-1]
    end = last.get("end") or last.get("start")
    return datetime.strptime(end[:16], "%Y%m%dT%H%M%S")

def check():
    if not in_mission_hours():
        return
    last = last_active()
    if last is None:
        print("WARN: No Timewarrior data found.")
        return
    silence = datetime.utcnow() - last
    if silence > timedelta(hours=SILENCE_THRESHOLD_HOURS):
        hours = int(silence.total_seconds() / 3600)
        print(f"CRITICAL: Agent silent for {hours}h. Last active: {last.isoformat()}")
        # → trigger notification to human via preferred channel

if __name__ == "__main__":
    check()
```

Run via cron (every hour during mission hours):
```
0 * * * * python3 /path/to/skills/elephantastic/scripts/vitality_check.py
```

## Alternative: File-Based Heartbeat

If Timewarrior isn't available, write a timestamp on each tool use:

```bash
echo "$(date -u +%Y%m%dT%H%M%S)" > ~/.agent/last_active
```

Check script reads this file instead of `timew export`.

## Alert Format

When silence is detected, notify the human with:
- Hours silent
- Last known active timestamp
- Last known task (from `task active` or `ops/session_state.md`)

## Mission Hours

Define "mission hours" as the window when silence is unexpected. Outside those hours, silence is normal — don't alert.

Adjust `MISSION_START` / `MISSION_END` to your timezone/schedule.
