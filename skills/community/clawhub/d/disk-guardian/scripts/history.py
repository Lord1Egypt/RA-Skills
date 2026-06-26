#!/usr/bin/env python3
"""
history.py — Maintain a health history log and detect concerning trends.

Usage:
    # Record a new scan (from parse_smart.py output):
    python3 scan_drives.py | python3 parse_smart.py | python3 history.py --record

    # From a file:
    python3 history.py --record --input parsed.json

    # View trend analysis:
    python3 history.py --trends [--device /dev/disk0]

    # List history:
    python3 history.py --list [--device /dev/disk0] [--limit 10]

    # Options:
    python3 history.py --data-dir /custom/path ...

History file: {data_dir}/history.json
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, timezone


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "workspace" / "disk-guardian"
HISTORY_FILE = "history.json"

# Trend detection thresholds
REALLOCATED_INCREASE_WARN = 1       # any increase is bad
TEMP_RISING_THRESHOLD_C = 5         # 5°C rise over last N scans is a warning
TEMP_RISING_SCANS = 3               # look at last N scans for temp trend
SPARE_DECLINING_THRESHOLD = 10      # 10% drop in available spare
SPARE_DECLINING_SCANS = 5


def load_history(data_dir: Path) -> dict:
    """Load history JSON from disk. Returns {'drives': {device: [entries...]}}."""
    history_path = data_dir / HISTORY_FILE
    if not history_path.exists():
        return {"drives": {}, "version": 1}
    try:
        return json.loads(history_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        # Corrupt history file — back it up and start fresh
        backup = history_path.with_suffix(".json.bak")
        try:
            history_path.rename(backup)
        except OSError:
            pass
        return {"drives": {}, "version": 1, "note": f"History reset (was corrupt: {e})"}


def save_history(data_dir: Path, history: dict):
    """Save history to disk."""
    data_dir.mkdir(parents=True, exist_ok=True)
    history_path = data_dir / HISTORY_FILE
    # Atomic write via temp file
    tmp_path = history_path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(history, indent=2, default=str))
    tmp_path.rename(history_path)


def record_scan(parsed_drives: list, data_dir: Path) -> dict:
    """
    Add a new scan snapshot to history.
    Returns a summary of what was recorded and any new trend alerts.
    """
    history = load_history(data_dir)
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    recorded = []

    for drive in parsed_drives:
        device = drive.get("device", "unknown")
        if "error" in drive:
            # Still record error entries so we track intermittent failures
            entry = {
                "timestamp": timestamp,
                "error": drive["error"],
                "health_status": "Unknown",
            }
        else:
            # Slim entry: keep key metrics, not full attribute dump
            entry = {
                "timestamp": timestamp,
                "model": drive.get("model"),
                "serial": drive.get("serial"),
                "drive_type": drive.get("drive_type"),
                "health_status": drive.get("health_status", "Unknown"),
                "temperature_c": drive.get("temperature_c"),
                "power_on_hours": drive.get("power_on_hours"),
                "flags": drive.get("flags", []),
                # Key numeric attributes for trend analysis
                "key_metrics": _extract_key_metrics(drive),
            }

        if device not in history["drives"]:
            history["drives"][device] = []

        history["drives"][device].append(entry)
        recorded.append(device)

    save_history(data_dir, history)

    # Run trend analysis on newly recorded data
    trends = analyze_trends(history)

    return {
        "recorded_at": timestamp,
        "devices_recorded": recorded,
        "trend_alerts": trends,
    }


def _extract_key_metrics(drive: dict) -> dict:
    """Extract a flat dict of key numeric metrics for trend tracking."""
    metrics = {}
    attrs = drive.get("attributes", {})
    drive_type = drive.get("drive_type", "Unknown")

    if drive_type == "NVMe":
        # NVMe attributes are already parsed strings
        for field in ("Available Spare", "Percentage Used", "Media and Data Integrity Errors",
                      "Unsafe Shutdowns", "Power On Hours"):
            val = attrs.get(field)
            if val is not None:
                import re
                m = re.search(r'([\d,]+)', str(val))
                if m:
                    metrics[field] = int(m.group(1).replace(",", ""))
    else:
        # SATA/SSD: extract raw_int for key attrs
        for attr_name in ("Reallocated_Sector_Ct", "Current_Pending_Sector",
                          "Offline_Uncorrectable", "Reported_Uncorrect",
                          "Power_On_Hours", "SSD_Life_Left"):
            if attr_name in attrs:
                raw = attrs[attr_name].get("raw_int")
                if raw is not None:
                    metrics[attr_name] = raw

    # Temperature always
    if drive.get("temperature_c") is not None:
        metrics["temperature_c"] = drive["temperature_c"]

    return metrics


def analyze_trends(history: dict) -> list:
    """
    Analyze history for concerning trends across all drives.
    Returns list of trend alert dicts.
    """
    alerts = []

    for device, entries in history["drives"].items():
        # Need at least 2 entries for trends
        valid = [e for e in entries if "key_metrics" in e]
        if len(valid) < 2:
            continue

        # Sort by timestamp
        valid_sorted = sorted(valid, key=lambda e: e["timestamp"])
        latest = valid_sorted[-1]
        metrics_latest = latest.get("key_metrics", {})

        # --- Reallocated sectors increasing ---
        for attr in ("Reallocated_Sector_Ct", "Reallocated_Event_Count"):
            vals = [(e["timestamp"], e["key_metrics"].get(attr))
                    for e in valid_sorted if attr in e.get("key_metrics", {})]
            if len(vals) >= 2:
                first_ts, first_val = vals[0]
                last_ts, last_val = vals[-1]
                if first_val is not None and last_val is not None and last_val > first_val:
                    diff = last_val - first_val
                    alerts.append({
                        "device": device,
                        "level": "Critical",
                        "trend": "reallocated_sectors_increasing",
                        "attribute": attr,
                        "change": diff,
                        "from_value": first_val,
                        "to_value": last_val,
                        "message": (
                            f"{device}: {attr.replace('_', ' ')} increased by {diff} "
                            f"(from {first_val} → {last_val}). Drive is remapping bad sectors."
                        )
                    })

        # --- Pending sectors increasing ---
        vals = [(e["timestamp"], e["key_metrics"].get("Current_Pending_Sector"))
                for e in valid_sorted if "Current_Pending_Sector" in e.get("key_metrics", {})]
        if len(vals) >= 2:
            first_ts, first_val = vals[0]
            last_ts, last_val = vals[-1]
            if first_val is not None and last_val is not None and last_val > first_val:
                alerts.append({
                    "device": device,
                    "level": "Critical",
                    "trend": "pending_sectors_increasing",
                    "attribute": "Current_Pending_Sector",
                    "change": last_val - first_val,
                    "from_value": first_val,
                    "to_value": last_val,
                    "message": (
                        f"{device}: Pending sector count rising ({first_val} → {last_val}). "
                        "Sectors flagged for reallocation but not yet remapped."
                    )
                })

        # --- Temperature rising trend ---
        temp_vals = [e["key_metrics"]["temperature_c"]
                     for e in valid_sorted[-TEMP_RISING_SCANS:]
                     if "temperature_c" in e.get("key_metrics", {})]
        if len(temp_vals) >= 2:
            # Check if consistently rising
            rising = all(temp_vals[i] < temp_vals[i+1] for i in range(len(temp_vals)-1))
            total_rise = temp_vals[-1] - temp_vals[0]
            if rising and total_rise >= TEMP_RISING_THRESHOLD_C:
                alerts.append({
                    "device": device,
                    "level": "Warning",
                    "trend": "temperature_rising",
                    "attribute": "temperature_c",
                    "change_c": total_rise,
                    "current_c": temp_vals[-1],
                    "message": (
                        f"{device}: Temperature rising trend over last {len(temp_vals)} scans "
                        f"(+{total_rise}°C, now {temp_vals[-1]}°C). Check cooling."
                    )
                })

        # --- NVMe available spare declining ---
        spare_vals = [(e["timestamp"], e["key_metrics"].get("Available Spare"))
                      for e in valid_sorted if "Available Spare" in e.get("key_metrics", {})]
        if len(spare_vals) >= 2:
            _, first_spare = spare_vals[0]
            _, last_spare = spare_vals[-1]
            if first_spare is not None and last_spare is not None:
                drop = first_spare - last_spare
                if drop >= SPARE_DECLINING_THRESHOLD:
                    alerts.append({
                        "device": device,
                        "level": "Warning",
                        "trend": "nvme_spare_declining",
                        "attribute": "Available Spare",
                        "change": drop,
                        "from_value": first_spare,
                        "to_value": last_spare,
                        "message": (
                            f"{device}: NVMe available spare declining "
                            f"({first_spare}% → {last_spare}%). "
                            "Drive wearing out."
                        )
                    })

        # --- SSD life declining ---
        life_vals = [(e["timestamp"], e["key_metrics"].get("SSD_Life_Left"))
                     for e in valid_sorted if "SSD_Life_Left" in e.get("key_metrics", {})]
        if len(life_vals) >= 2:
            _, first_life = life_vals[0]
            _, last_life = life_vals[-1]
            if first_life is not None and last_life is not None:
                drop = first_life - last_life
                if drop >= 5:  # 5% drop in SSD life
                    alerts.append({
                        "device": device,
                        "level": "Warning" if last_life > 20 else "Critical",
                        "trend": "ssd_life_declining",
                        "attribute": "SSD_Life_Left",
                        "change": drop,
                        "current_pct": last_life,
                        "message": (
                            f"{device}: SSD life declining ({first_life}% → {last_life}%). "
                            f"{'Replace soon.' if last_life <= 20 else 'Monitor closely.'}"
                        )
                    })

    return alerts


def cmd_record(args):
    data_dir = Path(args.data_dir)
    if args.input:
        parsed = json.loads(Path(args.input).read_text())
    else:
        stdin_data = sys.stdin.read().strip()
        if not stdin_data:
            print(json.dumps({"error": "No input provided"}, indent=2))
            sys.exit(1)
        parsed = json.loads(stdin_data)

    result = record_scan(parsed, data_dir)
    print(json.dumps(result, indent=2))


def cmd_trends(args):
    data_dir = Path(args.data_dir)
    history = load_history(data_dir)
    trends = analyze_trends(history)

    if args.device:
        trends = [t for t in trends if t.get("device") == args.device]

    print(json.dumps(trends, indent=2))


def cmd_list(args):
    data_dir = Path(args.data_dir)
    history = load_history(data_dir)

    if args.device:
        devices = {args.device: history["drives"].get(args.device, [])}
    else:
        devices = history["drives"]

    output = {}
    for device, entries in devices.items():
        limited = entries[-args.limit:] if args.limit else entries
        output[device] = limited

    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Disk SMART history manager")
    parser.add_argument(
        "--data-dir",
        default=str(DEFAULT_DATA_DIR),
        help=f"Data directory (default: {DEFAULT_DATA_DIR})"
    )
    parser.add_argument("--device", help="Filter to a specific device")

    subparsers = parser.add_subparsers(dest="command")

    # --record
    rec = subparsers.add_parser("--record", help="Record a new scan")
    rec.add_argument("--input", help="Path to parse_smart.py JSON output file")

    # --trends
    subparsers.add_parser("--trends", help="Show trend analysis")

    # --list
    lst = subparsers.add_parser("--list", help="List history entries")
    lst.add_argument("--limit", type=int, default=10, help="Max entries per device")

    # Support flat flags for ease of use (legacy-style)
    args, remaining = parser.parse_known_args()

    # Detect flat-flag style: python3 history.py --record
    all_args = sys.argv[1:]
    if "--record" in all_args:
        input_file = None
        if "--input" in all_args:
            idx = all_args.index("--input")
            if idx + 1 < len(all_args):
                input_file = all_args[idx + 1]
        args.command = "--record"
        args.input = input_file
        cmd_record(args)
    elif "--trends" in all_args:
        cmd_trends(args)
    elif "--list" in all_args:
        args.limit = 10
        if "--limit" in all_args:
            idx = all_args.index("--limit")
            if idx + 1 < len(all_args):
                try:
                    args.limit = int(all_args[idx + 1])
                except ValueError:
                    pass
        cmd_list(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
