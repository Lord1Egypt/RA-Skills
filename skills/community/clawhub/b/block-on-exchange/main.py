#!/usr/bin/env python3
"""CalIn — Sync any ICS calendar to Exchange as blocked time slots."""

import sys
from datetime import datetime, timezone
from pathlib import Path

import config


def cmd_setup():
    """Run interactive setup for ICS source and Microsoft target."""
    import ics_source
    import ms_auth

    ics_source.setup()
    ms_auth.setup()
    print("Setup complete! Run 'python main.py sync' to sync now.")


def cmd_sync():
    """Run one sync cycle."""
    import sync
    sync.run_sync()


def cmd_status():
    """Show sync status."""
    last_sync_file = config.DATA_DIR / "last_sync"
    if last_sync_file.exists():
        ts = last_sync_file.read_text().strip()
        print(f"Last sync: {ts}")
    else:
        print("No sync has been run yet.")

    if config.EVENT_MAP_FILE.exists():
        import json
        mapping = json.loads(config.EVENT_MAP_FILE.read_text())
        print(f"Currently tracking: {len(mapping)} synced events")
    else:
        print("No events synced yet.")


def cmd_clear():
    """Delete all synced Exchange events and clear the mapping."""
    import json
    import ms_auth
    import sync

    event_map = sync.load_event_map()
    if not event_map:
        print("No synced events to clear.")
        return

    print(f"Deleting {len(event_map)} synced events from Exchange...")
    for source_id, data in event_map.items():
        sync.delete_exchange_event(data["exchange_id"])
    sync.save_event_map({})
    print("Done. All synced events removed.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command>")
        print()
        print("Commands:")
        print("  setup   — Set up ICS source and Microsoft authentication")
        print("  sync    — Run one sync cycle")
        print("  status  — Show last sync time and event count")
        print("  clear   — Remove all synced events from Exchange")
        sys.exit(1)

    command = sys.argv[1]
    commands = {
        "setup": cmd_setup,
        "sync": cmd_sync,
        "status": cmd_status,
        "clear": cmd_clear,
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        sys.exit(1)

    commands[command]()


if __name__ == "__main__":
    main()
