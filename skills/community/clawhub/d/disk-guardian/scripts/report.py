#!/usr/bin/env python3
"""
report.py — Generate a human-readable markdown health report with risk rankings.

Usage:
    # Full pipeline:
    python3 scan_drives.py | python3 parse_smart.py | python3 report.py

    # From parsed JSON file:
    python3 report.py --input parsed.json

    # Include trend alerts from history:
    python3 report.py --input parsed.json --trends trends.json

    # Save to file:
    python3 report.py --input parsed.json --output report.md

    # Options:
    python3 report.py --data-dir /custom/path --input parsed.json
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "workspace" / "disk-guardian"

# Risk score weights (higher = worse)
RISK_SCORE = {
    "Critical": 100,
    "Warning": 30,
    "Good": 0,
    "Unknown": 10,
}

ATTRIBUTE_EXPLANATIONS = {
    "Reallocated_Sector_Ct": (
        "The drive has found and remapped bad sectors to spare areas. "
        "Any non-zero value means the drive has physical damage. Replace soon."
    ),
    "Current_Pending_Sector": (
        "Sectors that couldn't be read and are waiting to be remapped. "
        "These represent potential data loss. Back up immediately."
    ),
    "Offline_Uncorrectable": (
        "Sectors that failed during an offline scan and couldn't be corrected. "
        "Indicates physical read errors. Imminent failure risk."
    ),
    "Reported_Uncorrect": (
        "Uncorrectable errors reported during read/write/verify operations. "
        "Non-zero values mean data was lost or corrupted. Immediate backup required."
    ),
    "End-to-End_Error": (
        "Data mismatch detected between cache and disk buffer. "
        "Suggests hardware failure in the data path. Investigate immediately."
    ),
    "Command_Timeout": (
        "Commands that timed out waiting for the drive to respond. "
        "Can indicate a failing drive or SATA connection issue."
    ),
    "UDMA_CRC_Error_Count": (
        "Errors during data transfer over the SATA cable. "
        "Could be a bad cable or connector rather than the drive itself."
    ),
    "Spin_Retry_Count": (
        "Number of times the drive needed multiple attempts to spin up. "
        "Indicates a mechanical issue with the spindle motor."
    ),
    "Temperature": (
        "Drive temperature. Above 50°C is a warning; above 60°C risks damage. "
        "Ensure adequate airflow and cooling."
    ),
    "SSD_Life_Left": (
        "Estimated percentage of write endurance remaining. "
        "Below 20% means the SSD is approaching end of life."
    ),
    "Available Spare": (
        "NVMe: percentage of spare blocks available for reallocation. "
        "When this reaches the threshold, the drive will stop accepting writes."
    ),
    "Percentage Used": (
        "NVMe: estimated percentage of rated write endurance used. "
        "Above 80% means the drive is heavily worn."
    ),
    "Media and Data Integrity Errors": (
        "NVMe: errors detected and corrected by the media itself. "
        "Any non-zero value indicates media failures — replace the drive."
    ),
    "Critical Warning": (
        "NVMe: hardware-level critical warning flags. "
        "Any non-zero value indicates a serious drive problem."
    ),
}

STATUS_EMOJI = {
    "Critical": "🔴",
    "Warning": "🟡",
    "Good": "🟢",
    "Unknown": "⚪",
}

RECOMMENDATIONS = {
    "Critical": [
        "**Back up all data immediately** — do not wait.",
        "Replace the drive as soon as possible.",
        "Do not store new critical data on this drive.",
        "Run a full disk backup before any further diagnostics.",
    ],
    "Warning": [
        "Schedule a backup if not already current.",
        "Monitor this drive closely with weekly scans.",
        "Consider replacing proactively if the drive is over 3 years old.",
    ],
    "Good": [
        "No action required.",
        "Continue regular monthly SMART scans.",
    ],
    "Unknown": [
        "Check SMART support and permissions (may need sudo).",
        "Ensure smartctl is installed and up to date.",
    ],
}


def compute_risk_score(drive: dict, trend_alerts: list) -> int:
    """Compute a numeric risk score for ranking."""
    base = RISK_SCORE.get(drive.get("health_status", "Unknown"), 10)

    # Add points for each flag
    for flag in drive.get("flags", []):
        level = flag.get("level", "")
        base += RISK_SCORE.get(level, 0) // 10

    # Add trend alert points
    device = drive.get("device", "")
    for alert in trend_alerts:
        if alert.get("device") == device:
            base += RISK_SCORE.get(alert.get("level", "Warning"), 30) // 5

    # Penalize high power-on-hours (proxy for age/wear)
    poh = drive.get("power_on_hours", 0) or 0
    if poh > 50000:
        base += 20
    elif poh > 30000:
        base += 10
    elif poh > 20000:
        base += 5

    return base


def format_hours(hours):
    """Format power-on hours into human-readable string."""
    if hours is None:
        return "N/A"
    years = hours // 8760
    days = (hours % 8760) // 24
    if years > 0:
        return f"{hours:,}h (~{years}y {days}d)"
    return f"{hours:,}h"


def generate_report(drives: list, trend_alerts: list, data_dir: Path) -> str:
    """Generate markdown health report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []

    # Header
    lines.append(f"# 🖴 Disk Health Report")
    lines.append(f"*Generated: {now}*")
    lines.append("")

    if not drives:
        lines.append("No drives found or no data to report.")
        return "\n".join(lines)

    # Summary counts
    statuses = [d.get("health_status", "Unknown") for d in drives]
    critical_count = statuses.count("Critical")
    warning_count = statuses.count("Warning")
    good_count = statuses.count("Good")
    unknown_count = statuses.count("Unknown")

    lines.append("## Summary")
    if critical_count > 0:
        lines.append(f"> ⚠️ **{critical_count} drive(s) in CRITICAL condition — back up immediately!**")
        lines.append("")
    lines.append(f"- 🔴 Critical: {critical_count}")
    lines.append(f"- 🟡 Warning: {warning_count}")
    lines.append(f"- 🟢 Good: {good_count}")
    lines.append(f"- ⚪ Unknown: {unknown_count}")
    lines.append(f"- **Total drives scanned: {len(drives)}**")
    lines.append("")

    # Drive Inventory Table
    lines.append("## Drive Inventory")
    lines.append("")
    lines.append("| Device | Model | Type | Capacity | Power-On Hours | Temp | Status |")
    lines.append("|--------|-------|------|----------|----------------|------|--------|")

    for drive in drives:
        device = drive.get("device", "?")
        model = drive.get("model", "Unknown")
        if len(model) > 30:
            model = model[:28] + "…"
        drive_type = drive.get("drive_type", "?")
        capacity = drive.get("capacity", "N/A")
        # Shorten capacity
        if capacity and len(capacity) > 20:
            import re
            m = re.search(r'[\d,.]+ \w+', capacity)
            capacity = m.group(0) if m else capacity[:20]
        poh = format_hours(drive.get("power_on_hours"))
        temp = f"{drive.get('temperature_c')}°C" if drive.get("temperature_c") else "N/A"
        status = drive.get("health_status", "Unknown")
        emoji = STATUS_EMOJI.get(status, "⚪")
        lines.append(f"| `{device}` | {model} | {drive_type} | {capacity} | {poh} | {temp} | {emoji} {status} |")

    lines.append("")

    # Drives Ranked by Risk
    lines.append("## Drives Ranked by Risk")
    lines.append("")
    scored = [(compute_risk_score(d, trend_alerts), d) for d in drives]
    scored.sort(key=lambda x: x[0], reverse=True)

    for rank, (score, drive) in enumerate(scored, 1):
        device = drive.get("device", "?")
        status = drive.get("health_status", "Unknown")
        emoji = STATUS_EMOJI.get(status, "⚪")
        model = drive.get("model", "Unknown")
        lines.append(f"### #{rank} — `{device}` {emoji} {status}")
        lines.append(f"*{model} · Risk score: {score}*")
        lines.append("")

        flags = drive.get("flags", [])
        if flags:
            lines.append("**Issues detected:**")
            for flag in flags:
                level = flag.get("level", "Info")
                msg = flag.get("message", "")
                attr = flag.get("attribute", "")
                flag_emoji = "🔴" if level == "Critical" else "🟡"
                lines.append(f"- {flag_emoji} {msg}")
                # Add explanation if available
                explanation = ATTRIBUTE_EXPLANATIONS.get(attr)
                if explanation:
                    lines.append(f"  - *{explanation}*")
            lines.append("")

        # Drive-specific trend alerts
        device_trends = [a for a in trend_alerts if a.get("device") == device]
        if device_trends:
            lines.append("**Trend alerts:**")
            for alert in device_trends:
                level = alert.get("level", "Warning")
                alert_emoji = "🔴" if level == "Critical" else "🟡"
                lines.append(f"- {alert_emoji} {alert.get('message', '')}")
            lines.append("")

        # Recommendations
        recs = RECOMMENDATIONS.get(status, RECOMMENDATIONS["Unknown"])
        lines.append("**Recommendations:**")
        for rec in recs:
            lines.append(f"- {rec}")
        lines.append("")

    # Trend Summary (if any)
    if trend_alerts:
        lines.append("## Trend Alerts")
        lines.append("")
        lines.append("Concerning patterns detected across historical scans:")
        lines.append("")
        for alert in trend_alerts:
            level = alert.get("level", "Warning")
            alert_emoji = "🔴" if level == "Critical" else "🟡"
            lines.append(f"- {alert_emoji} {alert.get('message', '')}")
        lines.append("")

    # SMART not installed notice
    errors = [d for d in drives if d.get("error")]
    if errors:
        lines.append("## Scan Errors")
        lines.append("")
        for drive in errors:
            device = drive.get("device", "?")
            error = drive.get("error", "Unknown error")
            hint = drive.get("hint", "")
            lines.append(f"- `{device}`: {error}")
            if hint:
                lines.append(f"  - {hint}")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("*Report generated by disk-guardian. Run with `--sudo` if drives show errors.*")
    lines.append(f"*Data directory: `{data_dir}`*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate disk health report")
    parser.add_argument("--input", help="Path to parse_smart.py JSON output")
    parser.add_argument("--trends", help="Path to history.py --trends JSON output")
    parser.add_argument("--output", help="Save report to this file path")
    parser.add_argument(
        "--data-dir",
        default=str(DEFAULT_DATA_DIR),
        help=f"Data directory for context (default: {DEFAULT_DATA_DIR})"
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    # Load parsed drives
    if args.input:
        drives = json.loads(Path(args.input).read_text())
    else:
        stdin_data = sys.stdin.read().strip()
        if not stdin_data:
            print("Error: No input provided. Pipe parse_smart.py output or use --input.")
            sys.exit(1)
        drives = json.loads(stdin_data)

    # Load trends if provided
    trend_alerts = []
    if args.trends:
        trend_alerts = json.loads(Path(args.trends).read_text())
    else:
        # Try to load from history automatically
        history_trends_path = data_dir / "history.json"
        if history_trends_path.exists():
            try:
                import subprocess as _sp, sys as _sys
                history_script = Path(__file__).parent / "history.py"
                if history_script.exists():
                    result = _sp.run(
                        [_sys.executable, str(history_script), "--trends",
                         "--data-dir", str(data_dir)],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        trend_alerts = json.loads(result.stdout)
            except Exception:
                pass

    report = generate_report(drives, trend_alerts, data_dir)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)
        print(f"Report saved to: {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
