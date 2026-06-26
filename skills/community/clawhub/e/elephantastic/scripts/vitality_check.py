#!/usr/bin/env python3
"""
Agent GTD - Vitality Check
Monitor agent silence during mission hours and alert if threshold exceeded.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
import os

# Configuration (override via env vars)
MISSION_START_UTC = int(os.environ.get("AGENT_GTD_MISSION_START", "14"))  # 14:00 UTC
MISSION_END_UTC = int(os.environ.get("AGENT_GTD_MISSION_END", "2"))       # 02:00 UTC
MAX_SILENCE_HOURS = int(os.environ.get("AGENT_GTD_MAX_SILENCE", "8"))     # 8 hours

def get_timew_export():
    """Get timewarrior export data."""
    try:
        result = subprocess.run(
            ["timew", "export"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        return []

def parse_timew_date(date_str):
    """Parse timewarrior date format: YYYYMMDDTHHMMSSZ"""
    try:
        return datetime.strptime(date_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None

def is_mission_hours():
    """Check if current time is within mission hours."""
    now = datetime.now(timezone.utc)
    hour = now.hour
    if MISSION_START_UTC < MISSION_END_UTC:
        return MISSION_START_UTC <= hour < MISSION_END_UTC
    else:
        # Wrap around midnight (e.g., 14:00 to 02:00)
        return hour >= MISSION_START_UTC or hour < MISSION_END_UTC

def get_last_task():
    """Try to get last active task from Taskwarrior."""
    try:
        result = subprocess.run(
            ["task", "active", "export"],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        if data:
            return data[0].get("description", "Unknown")
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        pass
    return None

def check_vitality():
    """Check if agent has been silent too long."""
    data = get_timew_export()
    
    if not data:
        # Try file-based fallback
        heartbeat_file = os.path.expanduser("~/.agent/last_active")
        if os.path.exists(heartbeat_file):
            with open(heartbeat_file) as f:
                last_str = f.read().strip()
            try:
                last_active = datetime.strptime(last_str, "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
            except ValueError:
                print("WARNING: Could not parse heartbeat file.")
                return False
        else:
            print("WARNING: No Timewarrior history or heartbeat file found.")
            return False
    else:
        last_entry = data[-1]
        
        if "end" not in last_entry:
            # Currently active
            print("OK: Active task running.")
            return True
        
        last_active = parse_timew_date(last_entry["end"])
        if not last_active:
            print("ERROR: Could not parse last entry date.")
            return False
    
    now = datetime.now(timezone.utc)
    silence_duration = now - last_active
    hours_silent = silence_duration.total_seconds() / 3600
    
    print(f"INFO: Last activity ended {hours_silent:.1f} hours ago.")
    
    if hours_silent > MAX_SILENCE_HOURS:
        if is_mission_hours():
            last_task = get_last_task()
            msg = f"CRITICAL: Agent silent for {hours_silent:.1f} hours during mission time!"
            if last_task:
                msg += f" Last task: {last_task}"
            print(msg)
            return False
        else:
            print(f"NOTICE: Agent silent for {hours_silent:.1f} hours (off-hours).")
            return True
    
    return True

if __name__ == "__main__":
    if not check_vitality():
        sys.exit(1)
    sys.exit(0)
