#!/usr/bin/env python3
"""
monthly_performance.py — Aggregate campaign performance per month.

Usage:
  python3 monthly_performance.py
  python3 monthly_performance.py --months 12 --format json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _ac_client import ACClient
from _ac_client import safe_int as _safe_int


def _parse_iso(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def fetch(client: ACClient, months: int) -> list:
    cutoff = datetime.now(timezone.utc) - timedelta(days=months * 31)
    campaigns = client.paginate("campaigns", "campaigns", max_items=5000)
    return [c for c in campaigns if _parse_iso(c.get("sdate") or c.get("ldate")) and (_parse_iso(c.get("sdate") or c.get("ldate")) >= cutoff)]


def analyze(campaigns: list) -> dict:
    by_month = defaultdict(lambda: {"sends": 0, "recipients": 0, "opens": 0, "uopens": 0, "clicks": 0, "uclicks": 0, "unsubs": 0, "bounces": 0})
    for c in campaigns:
        d = _parse_iso(c.get("sdate") or c.get("ldate"))
        if not d:
            continue
        key = d.strftime("%Y-%m")
        m = by_month[key]
        m["sends"] += 1
        m["recipients"] += _safe_int(c.get("send_amt"))
        m["opens"] += _safe_int(c.get("opens"))
        m["uopens"] += _safe_int(c.get("uniqueopens"))
        m["clicks"] += _safe_int(c.get("linkclicks"))
        m["uclicks"] += _safe_int(c.get("uniquelinkclicks"))
        m["unsubs"] += _safe_int(c.get("unsubscribes"))
        m["bounces"] += _safe_int(c.get("bounces"))

    rows = []
    for month, m in sorted(by_month.items()):
        recipients = m["recipients"]
        rows.append({
            "month": month,
            "sends": m["sends"],
            "recipients": recipients,
            "open_rate": (m["uopens"] / recipients) if recipients else 0,
            "click_rate": (m["uclicks"] / recipients) if recipients else 0,
            "unsub_rate": (m["unsubs"] / recipients) if recipients else 0,
            "bounce_rate": (m["bounces"] / recipients) if recipients else 0,
            **m,
        })
    return {"months": rows, "campaigns_in_window": len(campaigns)}


def render_markdown(r: dict) -> str:
    lines = [
        "# Monthly Campaign Performance",
        "",
        f"Campaigns in window: {r['campaigns_in_window']}",
        "",
        "| Month | Sends | Recipients | Open % | Click % | Unsub % | Bounce % |",
        "|---|---|---|---|---|---|---|",
    ]
    for m in r["months"]:
        lines.append(
            f"| {m['month']} | {m['sends']} | {m['recipients']:,} | "
            f"{m['open_rate']*100:.1f}% | {m['click_rate']*100:.2f}% | "
            f"{m['unsub_rate']*100:.2f}% | {m['bounce_rate']*100:.2f}% |"
        )
    if not r["months"]:
        lines.append("_No campaigns in the requested window._")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Monthly campaign performance")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    campaigns = fetch(client, args.months)
    r = analyze(campaigns)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
