#!/usr/bin/env python3
"""
now.py — Report current time in the user's configured local timezone.
Used by OpenClaw timezone skill to prevent UTC/local confusion.
"""

import json
import os
import sys
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "tz_config.json")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return None


def get_time_with_config(config):
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+
    except ImportError:
        try:
            from backports.zoneinfo import ZoneInfo
        except ImportError:
            # Fallback: use pytz if available
            try:
                import pytz
                tz = pytz.timezone(config["timezone"])
                now = datetime.now(tz)
                return now, config["timezone"], config.get("display_name", config["timezone"])
            except ImportError:
                return None, None, None

    tz_name = config["timezone"]
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    return now, tz_name, config.get("display_name", tz_name)


def main():
    config = load_config()

    if not config:
        # No config — report UTC with a warning
        now_utc = datetime.utcnow()
        print(f"⚠️  Timezone not configured. Current UTC time: {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("Run timezone_setup.py to configure your local timezone.")
        sys.exit(1)

    now, tz_name, display_name = get_time_with_config(config)

    if now is None:
        # Fallback: system local time
        now = datetime.now()
        offset_hours = config.get("utc_offset_hours", 0)
        print(f"⚠️  Could not load timezone library. System local time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Configured timezone: {config.get('timezone', 'unknown')} (UTC{offset_hours:+.0f}h)")
        sys.exit(0)

    # Format output
    time_str = now.strftime("%I:%M %p").lstrip("0")  # "2:30 PM" not "02:30 PM"
    date_str = now.strftime("%A, %B %-d, %Y")
    tz_abbr = now.strftime("%Z")  # e.g. "EDT", "EST", "PST"
    offset_str = now.strftime("%z")  # e.g. "+0500"

    # Format offset nicely: "+0500" -> "UTC+5"
    if offset_str:
        sign = offset_str[0]
        hours = int(offset_str[1:3])
        mins = int(offset_str[3:5])
        if mins:
            offset_display = f"UTC{sign}{hours}:{mins:02d}"
        else:
            offset_display = f"UTC{sign}{hours}" if hours else "UTC"
    else:
        offset_display = ""

    print(f"🕐 {time_str} {tz_abbr}  ({date_str})")
    print(f"   Timezone: {display_name} [{tz_name}] {offset_display}")


if __name__ == "__main__":
    main()
