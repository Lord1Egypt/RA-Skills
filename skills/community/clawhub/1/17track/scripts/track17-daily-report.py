#!/usr/bin/env python3
"""Daily 17TRACK report - sync, auto-remove delivered, and print formatted status.

Uses the same path resolution and env vars as track17.py:
- TRACK17_TOKEN (required): 17TRACK API token
- TRACK17_DATA_DIR (optional): override data directory
- TRACK17_WORKSPACE_DIR (optional): override workspace directory

Output goes to stdout only — no external services are contacted beyond 17TRACK API.
"""

import os
import sys
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

# Resolve paths relative to this script, same as track17.py
SCRIPT_DIR = Path(__file__).resolve().parent
TRACK17_SCRIPT = SCRIPT_DIR / "track17.py"


def _resolve_data_dir() -> Path:
    """Same logic as track17.py resolve_data_dir()."""
    override = os.environ.get("TRACK17_DATA_DIR")
    if override:
        return Path(os.path.expandvars(os.path.expanduser(override))).resolve()

    workspace = os.environ.get("TRACK17_WORKSPACE_DIR") or os.environ.get("CLAWDBOT_WORKSPACE_DIR")
    if workspace:
        return Path(os.path.expandvars(os.path.expanduser(workspace))).resolve() / "packages" / "track17"

    # Walk up from script to find skills/ parent
    here = Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == "skills":
            return parent.parent / "packages" / "track17"

    return Path.cwd() / "packages" / "track17"


def sync_packages():
    """Sync packages via track17.py using TRACK17_TOKEN from env."""
    if not os.environ.get("TRACK17_TOKEN"):
        print("❌ TRACK17_TOKEN not set")
        return False

    result = subprocess.run(
        [sys.executable, str(TRACK17_SCRIPT), "sync"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def get_packages():
    """Get active packages from SQLite database."""
    db_path = _resolve_data_dir() / "track17.sqlite3"
    if not db_path.exists():
        return []

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, label, number, carrier, last_status,
                   last_event_desc, last_location, last_event_time_utc, last_update_at
            FROM packages
            WHERE archived = 0
            ORDER BY id
        """)
        packages = [
            {
                "id": row[0], "label": row[1], "number": row[2],
                "carrier": row[3], "status": row[4], "last_event": row[5],
                "location": row[6], "last_event_time": row[7], "last_updated": row[8],
            }
            for row in cursor.fetchall()
        ]
        conn.close()
        return packages
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        return []


def remove_package(pkg_id):
    """Remove a package via track17.py."""
    result = subprocess.run(
        [sys.executable, str(TRACK17_SCRIPT), "remove", str(pkg_id)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def auto_remove_delivered(packages):
    """Remove delivered packages and return list of removed."""
    removed = []
    for pkg in packages:
        if pkg["status"] == "Delivered":
            if remove_package(pkg["id"]):
                removed.append(pkg)
    return removed


def format_status(status):
    STATUS_MAP = {
        "InTransit": "🚚 In Transito",
        "Delivered": "✅ Consegnato",
        "NotFound": "❌ Non Trovato",
        "Exception": "⚠️ Problema",
        "Expired": "⏱️ Scaduto",
        "InfoReceived": "📋 Info Ricevute",
        "PickedUp": "📦 Ritirato",
        "AvailableForPickup": "📮 Pronto per Ritiro",
    }
    return STATUS_MAP.get(status, status or "❓ Sconosciuto")


def format_date(iso_date):
    if not iso_date:
        return None
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return iso_date.split("T")[0]


def main():
    """Generate daily report with auto-cleanup. Output to stdout."""
    if not sync_packages():
        print("⚠️ *SYNC ERROR*")
        print("")
        print("17TRACK API temporarily unavailable.")
        return

    all_packages = get_packages()
    removed_packages = auto_remove_delivered(all_packages)
    active_packages = [p for p in all_packages if p["status"] != "Delivered"]

    if removed_packages:
        print("*🗑️ DELIVERED PACKAGES REMOVED*")
        print("")
        for pkg in removed_packages:
            print(f"✅ #{pkg['id']} {pkg['label']} - {pkg['number']}")
        print("")
        print("---")
        print("")

    if not active_packages:
        print("*📦 17TRACK STATUS*")
        print("")
        print("No packages in tracking.")
        return

    now = datetime.now().strftime("%d %b %Y, %H:%M")
    print("*📦 17TRACK STATUS*")
    print("")
    print(f"_Updated: {now}_")
    print("")

    for pkg in active_packages:
        print(f"*#{pkg['id']} {pkg['label']}*")
        print(f"• Code: {pkg['number']}")
        print(f"• Status: {format_status(pkg['status'])}")
        if pkg.get("last_event"):
            print(f"• Event: {pkg['last_event']}")
        if pkg.get("location"):
            print(f"• Location: {pkg['location']}")
        if pkg.get("last_event_time"):
            date_str = format_date(pkg["last_event_time"])
            if date_str:
                print(f"• Date: {date_str}")
        print("")

    print("---")
    print("")
    print('💡 _For details: "Package details [code]"_')


if __name__ == "__main__":
    main()
