"""
Driftwatch — Drift Tracking & Trend Analysis

Loads stored scan history from ~/.driftwatch/history/ and calculates
per-file growth rates, deltas, and days-to-limit projections.

Compares the current live scan against stored historical data.
"""

import os
import json
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from references.constants import (
    BOOTSTRAP_MAX_CHARS_PER_FILE,
    BOOTSTRAP_TOTAL_MAX_CHARS,
    BOOTSTRAP_FILE_ORDER,
)

# Default retention: 90 days
DEFAULT_RETENTION_DAYS = 90
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.driftwatch/config.json")


def _load_config():
    """Load ~/.driftwatch/config.json if it exists. Returns defaults on failure."""
    defaults = {
        "retention_days": DEFAULT_RETENTION_DAYS,
        "alert_thresholds": {
            "per_file_warning_percent": 70,
            "per_file_critical_percent": 90,
            "aggregate_warning_percent": 60,
            "aggregate_critical_percent": 80,
            "growth_rate_warning_chars_per_day": 200,
        },
    }
    try:
        if os.path.isfile(DEFAULT_CONFIG_PATH):
            with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            # Merge with defaults
            for key in defaults:
                if key not in user_config:
                    user_config[key] = defaults[key]
            return user_config, None
        return defaults, None
    except (json.JSONDecodeError, OSError) as e:
        return defaults, f"Could not parse ~/.driftwatch/config.json: {e}"


def _load_history(history_dir, workspace_path, max_scans=10):
    """Load stored scan JSONs, filtered to matching workspace, sorted oldest-first."""
    if not os.path.isdir(history_dir):
        return []

    scans = []
    for fname in os.listdir(history_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(history_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Filter to matching workspace
            if data.get("workspace") != workspace_path:
                continue
            # Parse timestamp from the data
            ts_str = data.get("scan_timestamp", "")
            try:
                ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except ValueError:
                continue  # Skip unparseable timestamps
            scans.append((ts, data))
        except (json.JSONDecodeError, OSError):
            continue  # Skip corrupt files

    # Sort by timestamp, oldest first
    scans.sort(key=lambda x: x[0])

    # Take the most recent max_scans entries
    if len(scans) > max_scans:
        scans = scans[-max_scans:]

    return scans


def _classify_trend(growth_rate):
    """Classify growth rate into trend category."""
    if growth_rate < 0:
        return "shrinking"
    elif growth_rate < 50:
        return "stable"
    elif growth_rate <= 200:
        return "growing"
    else:
        return "accelerating"


def _get_file_chars(scan_data, filename):
    """Extract char_count for a specific file from a scan's truncation data."""
    for f in scan_data.get("truncation", {}).get("files", []):
        if f.get("file") == filename:
            return f.get("char_count", 0)
    return 0


def analyze_trends(history_dir, workspace_path, current_scan, max_scans=10):
    """
    Analyze trends from stored scan history + current live scan.

    Args:
        history_dir: Path to ~/.driftwatch/history/
        workspace_path: Current workspace path (for filtering history)
        current_scan: The current live scan result dict
        max_scans: Maximum number of historical scans to analyze

    Returns:
        dict with trend analysis
    """
    config, config_warning = _load_config()
    stored_scans = _load_history(history_dir, workspace_path, max_scans)

    findings = []
    if config_warning:
        findings.append({
            "severity": "warning",
            "message": config_warning,
        })

    # No history at all
    if len(stored_scans) == 0:
        result = {
            "scans_analyzed": 0,
            "note": "No history found. Run with --save to establish a baseline.",
        }
        if findings:
            result["findings"] = findings
        return result

    # Only 1 stored scan
    if len(stored_scans) == 1:
        result = {
            "scans_analyzed": 1,
            "note": "Baseline established. Trends available after 2+ scans.",
        }
        if findings:
            result["findings"] = findings
        return result

    # 2+ stored scans — calculate trends
    oldest_ts, oldest_scan = stored_scans[0]
    newest_ts, newest_scan = stored_scans[-1]
    time_span = (newest_ts - oldest_ts).total_seconds() / 86400  # days

    if time_span < 1.0:
        # Don't extrapolate daily rates from sub-day scan intervals —
        # the math produces absurd numbers (e.g., -200K chars/day from
        # a 17-hour span). Require at least 24 hours between oldest
        # and newest scan for meaningful daily rate calculation.
        result = {
            "scans_analyzed": len(stored_scans),
            "time_span_days": round(time_span, 2),
            "note": (
                "Scans are less than 1 day apart. "
                "Daily rate trends require at least 24 hours between "
                "oldest and newest scan."
            ),
        }
        if findings:
            result["findings"] = findings
        return result

    # Per-file trends
    file_trends = []
    total_current = 0
    total_oldest = 0

    for filename in BOOTSTRAP_FILE_ORDER:
        current_chars = _get_file_chars(current_scan, filename)
        oldest_chars = _get_file_chars(oldest_scan, filename)
        delta = current_chars - oldest_chars
        growth_rate = round(delta / time_span, 1)

        # Days to limit
        if growth_rate > 0:
            remaining = BOOTSTRAP_MAX_CHARS_PER_FILE - current_chars
            if remaining <= 0:
                days_to_limit = 0
            else:
                days_to_limit = round(remaining / growth_rate)
        else:
            days_to_limit = None  # Not approaching limit

        trend = _classify_trend(growth_rate)

        file_trends.append({
            "file": filename,
            "current_chars": current_chars,
            "oldest_chars": oldest_chars,
            "delta": delta,
            "growth_rate_chars_per_day": growth_rate,
            "days_to_limit": days_to_limit,
            "trend": trend,
        })

        total_current += current_chars
        total_oldest += oldest_chars

    # Aggregate trend
    agg_delta = total_current - total_oldest
    agg_growth_rate = round(agg_delta / time_span, 1)
    if agg_growth_rate > 0:
        agg_remaining = BOOTSTRAP_TOTAL_MAX_CHARS - total_current
        if agg_remaining <= 0:
            agg_days_to_limit = 0
        else:
            agg_days_to_limit = round(agg_remaining / agg_growth_rate)
    else:
        agg_days_to_limit = None

    result = {
        "scans_analyzed": len(stored_scans),
        "time_span_days": round(time_span, 1),
        "files": file_trends,
        "aggregate": {
            "current_total": total_current,
            "growth_rate_chars_per_day": agg_growth_rate,
            "days_to_aggregate_limit": agg_days_to_limit,
            "trend": _classify_trend(agg_growth_rate),
        },
    }
    if findings:
        result["findings"] = findings
    return result


def prune_history(history_dir):
    """Delete history files older than retention_days."""
    config, _ = _load_config()
    retention_days = config.get("retention_days", DEFAULT_RETENTION_DAYS)
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

    if not os.path.isdir(history_dir):
        return

    for fname in os.listdir(history_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(history_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            ts_str = data.get("scan_timestamp", "")
            ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if ts < cutoff:
                os.remove(fpath)
        except (json.JSONDecodeError, OSError, ValueError):
            continue  # Skip corrupt files, don't delete them
