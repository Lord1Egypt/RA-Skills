"""
Driftwatch — Main Entry Point
Runs all 3 analysis modules and aggregates into a single JSON report.

Usage:
    python3 scripts/scan.py [--workspace /path/to/workspace]
    python3 scripts/scan.py [--workspace /path/to/workspace] --save
    python3 scripts/scan.py [--workspace /path/to/workspace] --save --history

Output: JSON to stdout. Exit code always 0 — the agent interprets the JSON.
"""

import sys
import os
import json
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from references.constants import DRIFTWATCH_VERSION, OPENCLAW_VERSION_TAG


def _run_module(func, workspace_path):
    """Run a single analysis module, returning {"error": "..."} on failure."""
    try:
        return func(workspace_path)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def _count_severities_truncation(result):
    """Extract critical/warning/info counts from truncation module output."""
    counts = {"critical": 0, "warning": 0, "info": 0}
    if "error" in result:
        counts["warning"] += 1
        return counts
    for f in result.get("files", []):
        s = f.get("status")
        if s in counts:
            counts[s] += 1
    agg_status = result.get("aggregate", {}).get("aggregate_status")
    if agg_status in counts:
        counts[agg_status] += 1
    return counts


def _count_severities_findings(result):
    """Extract critical/warning/info counts from a module with a 'findings' list."""
    counts = {"critical": 0, "warning": 0, "info": 0}
    if "error" in result:
        counts["warning"] += 1
        return counts
    for f in result.get("findings", []):
        s = f.get("severity")
        if s in counts:
            counts[s] += 1
    return counts


def _count_severities_simulation(result):
    """Extract critical/warning counts from simulation module output."""
    counts = {"critical": 0, "warning": 0, "info": 0}
    if "error" in result:
        counts["warning"] += 1
        return counts
    for f in result.get("files", []):
        status = f.get("status")
        if status == "truncated_now":
            counts["critical"] += 1
        elif status == "at_risk":
            counts["warning"] += 1
    return counts


def _build_summary(truncation, compaction, hygiene, simulation):
    tc = _count_severities_truncation(truncation)
    cc = _count_severities_findings(compaction)
    hc = _count_severities_findings(hygiene)
    sc = _count_severities_simulation(simulation)

    critical = tc["critical"] + cc["critical"] + hc["critical"] + sc["critical"]
    warning  = tc["warning"]  + cc["warning"]  + hc["warning"]  + sc["warning"]
    info     = tc["info"]     + cc["info"]      + hc["info"]     + sc["info"]

    return {
        "critical": critical,
        "warning": warning,
        "info": info,
        "total_findings": critical + warning + info,
    }


def _load_check_config():
    """Load alert thresholds from ~/.driftwatch/config.json or use defaults."""
    defaults = {
        "per_file_warning_percent": 70,
        "per_file_critical_percent": 90,
        "aggregate_warning_percent": 60,
        "aggregate_critical_percent": 80,
        "growth_rate_warning_chars_per_day": 200,
    }
    config_path = os.path.expanduser("~/.driftwatch/config.json")
    try:
        if os.path.isfile(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            thresholds = data.get("alert_thresholds", {})
            for key in defaults:
                if key not in thresholds:
                    thresholds[key] = defaults[key]
            return thresholds
    except (json.JSONDecodeError, OSError):
        pass
    return defaults


def _check_thresholds(report):
    """
    Evaluate scan against thresholds. Print one-line summary. Return exit code.
    0 = healthy, 1 = warning, 2 = critical.
    """
    thresholds = _load_check_config()
    truncation = report.get("truncation", {})
    files = truncation.get("files", [])
    aggregate = truncation.get("aggregate", {})
    trends = report.get("trends", {})

    criticals = []
    warnings = []

    # Per-file checks
    for f in files:
        pct = f.get("percent_of_limit", 0)
        name = f.get("file", "?")
        if pct >= thresholds["per_file_critical_percent"]:
            criticals.append(f"{name} at {pct:.0f}% of limit")
        elif pct >= thresholds["per_file_warning_percent"]:
            warnings.append(f"{name} at {pct:.0f}% of limit")

    # Aggregate check
    agg_pct = aggregate.get("percent_of_aggregate", 0)
    if agg_pct >= thresholds["aggregate_critical_percent"]:
        criticals.append(f"aggregate at {agg_pct:.0f}%")
    elif agg_pct >= thresholds["aggregate_warning_percent"]:
        warnings.append(f"aggregate at {agg_pct:.0f}%")

    # Growth rate check (from trends if available)
    trend_files = trends.get("files", [])
    for tf in trend_files:
        rate = tf.get("growth_rate_chars_per_day", 0)
        if rate >= thresholds["growth_rate_warning_chars_per_day"]:
            warnings.append(f"{tf['file']} growing {rate} chars/day")

    # Simulation check — actively truncated files are always critical
    simulation = report.get("simulation", {})
    for sf in simulation.get("files", []):
        if sf.get("status") == "truncated_now":
            criticals.append(f"{sf['file']} TRUNCATED")

    # Determine exit code and print summary
    if criticals:
        msg = f"✗ Critical — {', '.join(criticals)}"
        print(msg)
        return 2
    elif warnings:
        msg = f"⚠ Warning — {', '.join(warnings)}"
        print(msg)
        return 1
    else:
        num_files = len(files)
        msg = f"✓ All clear — {num_files} files healthy, {agg_pct:.1f}% aggregate budget used"
        print(msg)
        return 0


def _resolve_workspace(args_workspace):
    """Return workspace path from arg → env var → default."""
    if args_workspace:
        return os.path.expanduser(args_workspace)
    env = os.environ.get("OPENCLAW_WORKSPACE")
    if env:
        return os.path.expanduser(env)
    return os.path.expanduser("~/.openclaw/workspace/")


def main():
    parser = argparse.ArgumentParser(
        prog="scan.py",
        description=(
            "Driftwatch — OpenClaw workspace health scanner.\n"
            "Checks bootstrap truncation, compaction anchor health, and workspace hygiene.\n"
            "Outputs a JSON report to stdout.\n\n"
            "Workspace resolution order:\n"
            "  1. --workspace flag\n"
            "  2. OPENCLAW_WORKSPACE environment variable\n"
            "  3. ~/.openclaw/workspace/ (default)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--workspace",
        metavar="PATH",
        help="Path to your OpenClaw workspace directory (default: ~/.openclaw/workspace/)",
        default=None,
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Persist scan results to ~/.driftwatch/history/ for trend tracking",
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Include trend analysis from stored scan history",
    )
    parser.add_argument(
        "--visual",
        action="store_true",
        help="Output terminal bar chart of bootstrap file budget",
    )
    parser.add_argument(
        "--html",
        metavar="PATH",
        help="Generate self-contained HTML report at the specified path",
        default=None,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Cron-friendly mode: one-line summary, exit 0/1/2 for healthy/warning/critical",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="With --check, also output full JSON (default: --check suppresses JSON)",
    )
    args = parser.parse_args()

    workspace_path = _resolve_workspace(args.workspace)
    workspace_path = os.path.abspath(workspace_path)

    # Import modules here so import failures are caught per-module
    def load_truncation(wp):
        from scripts.truncation import analyze_truncation
        return analyze_truncation(wp)

    def load_compaction(wp):
        from scripts.compaction import analyze_compaction
        return analyze_compaction(wp)

    def load_hygiene(wp):
        from scripts.hygiene import analyze_hygiene
        return analyze_hygiene(wp)

    def load_simulation(wp):
        from scripts.simulation import analyze_simulation
        return analyze_simulation(wp)

    truncation = _run_module(load_truncation, workspace_path)
    compaction = _run_module(load_compaction, workspace_path)
    hygiene    = _run_module(load_hygiene,    workspace_path)
    simulation = _run_module(load_simulation, workspace_path)

    summary = _build_summary(truncation, compaction, hygiene, simulation)

    scan_timestamp = datetime.now(timezone.utc)

    report = {
        "driftwatch_version": DRIFTWATCH_VERSION,
        "openclaw_version_tag": OPENCLAW_VERSION_TAG,
        "workspace": workspace_path,
        "scan_timestamp": scan_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "truncation": truncation,
        "compaction": compaction,
        "hygiene": hygiene,
        "simulation": simulation,
        "web_dashboard_note": (
            "For visual truncation maps and drift tracking over time, visit bubbuilds.com"
        ),
    }

    # --save: persist scan to history (runs BEFORE --history so trends include this scan)
    if args.save:
        history_dir = os.path.expanduser("~/.driftwatch/history")
        try:
            os.makedirs(history_dir, exist_ok=True)
            filename = scan_timestamp.strftime("%Y-%m-%dT%H%M%SZ.json")
            save_path = os.path.join(history_dir, filename)
            save_data = dict(report)
            save_data["saved_to"] = save_path
            fd = os.open(save_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2)
            report["saved_to"] = save_path
        except OSError as e:
            # Save failed — add warning but don't crash
            if "findings" not in report.get("hygiene", {}):
                report.setdefault("save_warning", str(e))
            else:
                report["hygiene"]["findings"].append({
                    "severity": "warning",
                    "check": "save_failed",
                    "message": f"Could not save scan history: {e}",
                })

        # Run retention pruning after save
        try:
            from scripts.trends import prune_history
            prune_history(history_dir)
        except Exception:
            pass  # Retention failure is non-critical

    # --history: load trends from stored scan history + current live scan
    if args.history:
        history_dir = os.path.expanduser("~/.driftwatch/history")
        try:
            from scripts.trends import analyze_trends
            report["trends"] = analyze_trends(history_dir, workspace_path, report)
        except Exception as e:
            report["trends"] = {"error": f"{type(e).__name__}: {e}"}

    # --check: cron-friendly one-line output with exit codes
    if args.check:
        exit_code = _check_thresholds(report)
        if args.json:
            print(json.dumps(report, indent=2))
        sys.exit(exit_code)

    # --visual: terminal bar chart
    if args.visual:
        from scripts.visual import render_terminal
        print(render_terminal(report))
    else:
        print(json.dumps(report, indent=2))

    # --html: generate HTML report
    if args.html:
        try:
            from scripts.visual import render_html
            render_html(report, args.html)
        except Exception as e:
            print(f"Warning: HTML report generation failed: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
