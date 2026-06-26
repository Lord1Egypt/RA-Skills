#!/usr/bin/env python3
"""
list_growth_forecast.py — Linear projection of list size N days out.

Computes net daily growth rate (adds minus suppressions) over a trailing
window, projects forward.

Usage:
  python3 list_growth_forecast.py
  python3 list_growth_forecast.py --window-days 90 --project-days 90
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _ac_client import ACClient


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


def fetch(client: ACClient, max_items: int = 50000) -> list:
    return client.paginate("contacts", "contacts", max_items=max_items)


def analyze(contacts: list, window_days: int, project_days: int) -> dict:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=window_days)
    total = len(contacts)
    new_in_window = 0
    suppressed_in_window = 0
    for c in contacts:
        cd = _parse_iso(c.get("cdate"))
        if cd and cd >= window_start:
            new_in_window += 1
    # crude: count current unsub/bounce as proxy; a true churn calc needs status-change history
    daily_growth = (new_in_window - suppressed_in_window) / max(window_days, 1)
    projected_size = total + daily_growth * project_days
    return {
        "total_contacts": total,
        "window_days": window_days,
        "new_in_window": new_in_window,
        "daily_growth_estimate": daily_growth,
        "project_days": project_days,
        "projected_size": int(projected_size),
        "projected_change": int(projected_size - total),
    }


def render_markdown(r: dict) -> str:
    return "\n".join([
        "# List Growth Forecast",
        "",
        f"- Current contacts: {r['total_contacts']:,}",
        f"- New in last {r['window_days']} days: {r['new_in_window']:,}",
        f"- Daily growth rate: {r['daily_growth_estimate']:.1f}/day",
        f"- Projected in {r['project_days']} days: **{r['projected_size']:,}** ({r['projected_change']:+,})",
        "",
        "_Linear projection. Suppression rate is approximated; output is directional._",
    ])


def main():
    parser = argparse.ArgumentParser(description="List growth forecast")
    parser.add_argument("--window-days", type=int, default=30)
    parser.add_argument("--project-days", type=int, default=90)
    parser.add_argument("--max-items", type=int, default=50000,
                        help="Cap /contacts stream (default 50000)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    contacts = fetch(client, max_items=args.max_items)
    r = analyze(contacts, args.window_days, args.project_days)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
