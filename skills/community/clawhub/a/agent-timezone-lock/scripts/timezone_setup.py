#!/usr/bin/env python3
"""
timezone_setup.py — Configure the user's local timezone for OpenClaw timezone skill.

Usage:
  python3 timezone_setup.py              # Interactive detection + prompt
  python3 timezone_setup.py --set "America/New_York"
  python3 timezone_setup.py --detect     # Auto-detect only, no prompt
  python3 timezone_setup.py --patch-agents  # Patch AGENTS.md with standing order
"""

import argparse
import json
import os
import re
import subprocess
import sys

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "tz_config.json")
AGENTS_MD_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "AGENTS.md")
USER_MD_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "USER.md")

# Common timezone display names
TZ_DISPLAY = {
    "America/New_York": "US Eastern",
    "America/Chicago": "US Central",
    "America/Denver": "US Mountain",
    "America/Los_Angeles": "US Pacific",
    "America/Anchorage": "US Alaska",
    "Pacific/Honolulu": "US Hawaii",
    "America/Phoenix": "US Arizona (no DST)",
    "Europe/London": "UK (London)",
    "Europe/Paris": "Central European",
    "Europe/Berlin": "Central European",
    "Europe/Moscow": "Moscow",
    "Asia/Tokyo": "Japan",
    "Asia/Shanghai": "China",
    "Asia/Kolkata": "India",
    "Asia/Dubai": "Gulf (UAE)",
    "Australia/Sydney": "Australia Eastern",
    "Pacific/Auckland": "New Zealand",
    "UTC": "UTC (no conversion)",
}

# ET shorthand mapping
TZ_ALIASES = {
    "ET": "America/New_York",
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "CT": "America/Chicago",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "MT": "America/Denver",
    "MST": "America/Denver",
    "MDT": "America/Denver",
    "PT": "America/Los_Angeles",
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "GMT": "UTC",
    "UTC": "UTC",
}


def detect_from_user_md():
    """Read timezone from USER.md Timezone: field."""
    if not os.path.exists(USER_MD_PATH):
        return None
    with open(USER_MD_PATH) as f:
        content = f.read()
    # Match "Timezone: US Eastern (ET / UTC-5, UTC-4 DST)" or "Timezone: America/New_York"
    match = re.search(r"Timezone:\s*(.+)", content, re.IGNORECASE)
    if not match:
        return None
    raw = match.group(1).strip()
    # Try to find a known IANA tz or alias in the string
    # Check aliases first
    for alias, tz in TZ_ALIASES.items():
        if alias in raw.upper():
            return tz
    # Check IANA names
    for iana in TZ_DISPLAY.keys():
        if iana.lower() in raw.lower():
            return iana
    return None


def detect_from_system():
    """Try timedatectl or /etc/localtime to get system timezone."""
    # Try timedatectl
    try:
        result = subprocess.run(
            ["timedatectl", "show", "--property=Timezone", "--value"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try /etc/localtime symlink
    try:
        link = os.readlink("/etc/localtime")
        # Usually something like /usr/share/zoneinfo/America/New_York
        match = re.search(r"zoneinfo/(.+)$", link)
        if match:
            return match.group(1)
    except (OSError, AttributeError):
        pass

    # Try /etc/timezone
    try:
        if os.path.exists("/etc/timezone"):
            with open("/etc/timezone") as f:
                tz = f.read().strip()
            if tz:
                return tz
    except OSError:
        pass

    return None


def get_utc_offset(tz_name):
    """Return UTC offset hours for a timezone (approximate, uses current DST status)."""
    try:
        from zoneinfo import ZoneInfo
    except ImportError:
        try:
            from backports.zoneinfo import ZoneInfo
        except ImportError:
            try:
                import pytz
                from datetime import datetime
                tz = pytz.timezone(tz_name)
                now = datetime.now(tz)
                return now.utcoffset().total_seconds() / 3600
            except Exception:
                return 0

    from datetime import datetime
    try:
        tz = ZoneInfo(tz_name)
        now = datetime.now(tz)
        offset = now.utcoffset()
        if offset:
            return offset.total_seconds() / 3600
    except Exception:
        pass
    return 0


def save_config(tz_name, display_name=None):
    offset = get_utc_offset(tz_name)
    config = {
        "timezone": tz_name,
        "display_name": display_name or TZ_DISPLAY.get(tz_name, tz_name),
        "utc_offset_hours": offset,
        "configured_by": "timezone_setup.py",
        "note": "Edit timezone field to change. Run now.py to verify."
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Timezone saved: {config['display_name']} [{tz_name}] (UTC{offset:+.1f}h)")
    return config


def patch_agents_md(tz_name, display_name):
    """Append timezone standing order to AGENTS.md if not already there."""
    if not os.path.exists(AGENTS_MD_PATH):
        print(f"⚠️  AGENTS.md not found at {AGENTS_MD_PATH} — skipping patch")
        return

    with open(AGENTS_MD_PATH) as f:
        content = f.read()

    marker = "## Timezone Standing Order"
    if marker in content:
        # Already patched — update it
        # Replace block up to next ## header
        new_block = f"""{marker}
- User timezone: **{display_name}** [{tz_name}]
- NEVER report UTC time as local time
- All time output must be in user's local timezone  
- When in doubt: run `python3 skills/timezone/scripts/now.py` before reporting any time
- API/cron/system timestamps are UTC — always convert before displaying
"""
        # Replace existing block
        updated = re.sub(
            r"## Timezone Standing Order.*?(?=\n## |\Z)",
            new_block,
            content,
            flags=re.DOTALL
        )
        with open(AGENTS_MD_PATH, "w") as f:
            f.write(updated)
        print(f"✅ AGENTS.md timezone standing order updated.")
    else:
        # Append before end
        standing_order = f"""
---

{marker}
- User timezone: **{display_name}** [{tz_name}]
- NEVER report UTC time as local time
- All time output must be in user's local timezone  
- When in doubt: run `python3 skills/timezone/scripts/now.py` before reporting any time
- API/cron/system timestamps are UTC — always convert before displaying
"""
        with open(AGENTS_MD_PATH, "a") as f:
            f.write(standing_order)
        print(f"✅ AGENTS.md patched with timezone standing order.")


def resolve_tz(raw):
    """Resolve raw input to IANA timezone name."""
    raw = raw.strip()
    # Check aliases
    upper = raw.upper()
    if upper in TZ_ALIASES:
        return TZ_ALIASES[upper]
    # Check IANA directly (basic validation)
    if "/" in raw or raw == "UTC":
        return raw
    # Check display names
    for iana, display in TZ_DISPLAY.items():
        if raw.lower() in display.lower():
            return iana
    return raw  # Return as-is and let zoneinfo validate


def main():
    parser = argparse.ArgumentParser(description="Configure OpenClaw timezone setting")
    parser.add_argument("--set", metavar="TIMEZONE", help="Set timezone directly (IANA name or alias like ET)")
    parser.add_argument("--detect", action="store_true", help="Auto-detect timezone without prompting")
    parser.add_argument("--patch-agents", action="store_true", help="Patch AGENTS.md with standing order")
    args = parser.parse_args()

    # Handle --set
    if args.set:
        tz = resolve_tz(args.set)
        config = save_config(tz)
        if args.patch_agents or True:  # always patch
            patch_agents_md(tz, config["display_name"])
        return

    # Auto-detect
    print("🔍 Detecting timezone...")

    tz_detected = None
    source = None

    # 1. Check USER.md
    tz_from_user = detect_from_user_md()
    if tz_from_user:
        print(f"   Found in USER.md: {tz_from_user}")
        tz_detected = tz_from_user
        source = "USER.md"

    # 2. Check system
    if not tz_detected:
        tz_from_system = detect_from_system()
        if tz_from_system:
            print(f"   Found via system: {tz_from_system}")
            tz_detected = tz_from_system
            source = "system"

    if args.detect:
        if tz_detected:
            config = save_config(tz_detected)
            patch_agents_md(tz_detected, config["display_name"])
        else:
            print("❌ Could not auto-detect timezone. Run without --detect to set manually.")
            sys.exit(1)
        return

    # Interactive mode
    if tz_detected:
        display = TZ_DISPLAY.get(tz_detected, tz_detected)
        print(f"\n✨ Detected: {display} [{tz_detected}] (from {source})")
        answer = input("Use this timezone? [Y/n]: ").strip().lower()
        if answer in ("", "y", "yes"):
            config = save_config(tz_detected)
            patch_agents_md(tz_detected, config["display_name"])
            return

    # Manual entry
    print("\nCommon timezones:")
    for iana, display in list(TZ_DISPLAY.items())[:8]:
        print(f"  {display:25s}  [{iana}]")
    print("  (or enter any IANA name, e.g. Europe/Paris)")
    print("  (or short aliases: ET, PT, CT, MT, GMT, UTC)")
    raw = input("\nEnter your timezone: ").strip()
    if not raw:
        print("❌ No timezone entered. Exiting.")
        sys.exit(1)
    tz = resolve_tz(raw)
    config = save_config(tz)
    patch_agents_md(tz, config["display_name"])


if __name__ == "__main__":
    main()
