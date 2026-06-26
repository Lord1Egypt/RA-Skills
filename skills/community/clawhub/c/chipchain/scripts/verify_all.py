#!/usr/bin/env python3
"""
Run all chipchain verification scripts.

Usage:
    python scripts/verify_all.py              # Run all verifiers
    python scripts/verify_all.py --only tickers        # Selective run

Exit code: 0 = all pass, 1 = any failures
Output: verification_summary.md + individual reports
"""

import argparse
import importlib
import sys
import time
from datetime import datetime
from pathlib import Path

# Ensure scripts/ is on the import path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _verify_common import find_skill_dir, write_report  # noqa: E402

VERIFIERS = {
    "tickers": {
        "module": "verify_tickers",
        "description": "Stock tickers (yfinance + pykrx)",
    },
    "cas": {
        "module": "verify_cas",
        "description": "CAS numbers (PubChem)",
    },
}


def run_verifier(name: str, info: dict) -> dict:
    """Run a single verifier module and capture its result."""
    result = {
        "name": name,
        "description": info["description"],
        "success": False,
        "error": None,
        "duration_s": 0,
    }

    print(f"\n{'='*60}")
    print(f"  RUNNING: {name} -- {info['description']}")
    print(f"{'='*60}\n")

    start = time.time()
    try:
        mod = importlib.import_module(info["module"])
        success = mod.main()
        result["success"] = bool(success) if success is not None else True
    except SystemExit as e:
        result["success"] = e.code == 0
    except Exception as e:
        result["error"] = str(e)[:200]
        print(f"\n  ERROR in {name}: {e}")

    result["duration_s"] = round(time.time() - start, 1)
    return result


def main():
    parser = argparse.ArgumentParser(description="Run chipchain verifiers")
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Comma-separated list of verifiers to run (e.g., tickers,cas)",
    )
    args = parser.parse_args()

    # Determine which verifiers to run
    if args.only:
        selected = [v.strip() for v in args.only.split(",")]
        unknown = [v for v in selected if v not in VERIFIERS]
        if unknown:
            print(f"Unknown verifiers: {', '.join(unknown)}")
            print(f"Available: {', '.join(VERIFIERS.keys())}")
            raise SystemExit(1)
        to_run = {k: VERIFIERS[k] for k in selected}
    else:
        to_run = VERIFIERS

    print(f"chipchain verification suite")
    print(f"Running {len(to_run)} verifier(s): {', '.join(to_run.keys())}")

    # Run each verifier
    results = []
    for name, info in to_run.items():
        result = run_verifier(name, info)
        results.append(result)

    # Summary
    pass_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - pass_count
    total_time = sum(r["duration_s"] for r in results)

    print(f"\n{'='*60}")
    print(f"  VERIFICATION SUMMARY")
    print(f"{'='*60}")
    for r in results:
        status = "PASS" if r["success"] else "FAIL"
        error_msg = f" ({r['error'][:50]})" if r["error"] else ""
        print(f"  [{status}] {r['name']:10s} -- {r['description']}{error_msg}  ({r['duration_s']}s)")
    print(f"\n  Total: {pass_count} passed, {fail_count} failed ({total_time:.1f}s)")
    print(f"{'='*60}")

    # Write summary report
    skill_dir = find_skill_dir()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    sections = []

    # Overview
    overview = f"**Total verifiers:** {len(results)}\n"
    overview += f"**Passed:** {pass_count}\n"
    overview += f"**Failed:** {fail_count}\n"
    overview += f"**Total time:** {total_time:.1f}s\n\n"
    overview += "| Verifier | Status | Duration | Notes |\n"
    overview += "|---|---|---|---|\n"
    for r in results:
        status = "PASS" if r["success"] else "FAIL"
        notes = r["error"][:50] if r["error"] else ""
        overview += f"| {r['name']} | {status} | {r['duration_s']}s | {notes} |\n"
    sections.append({"heading": "Overview", "content": overview})

    # Individual report links
    links = "| Verifier | Report | JSON |\n|---|---|---|\n"
    report_names = {
        "tickers": ("ticker_verification_report.md", "ticker_verification.json"),
        "cas": ("cas_verification_report.md", "cas_verification.json"),
    }
    for name in to_run:
        md_name, json_name = report_names.get(name, ("N/A", "N/A"))
        links += f"| {name} | [{md_name}]({md_name}) | [{json_name}]({json_name}) |\n"
    sections.append({"heading": "Individual Reports", "content": links})

    summary_path = skill_dir / "verification_summary.md"
    write_report(summary_path, "Verification Summary", sections)
    print(f"\nSummary report: {summary_path}")

    raise SystemExit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
