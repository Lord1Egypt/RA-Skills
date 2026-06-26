#!/usr/bin/env python3
"""
automation_audit.py — Inventory automations: status, enrollments, exit reasons.

Flags automations with 0 enrollments in N days (orphaned), high exit-without-completion
rates, and inactive automations.

Usage:
  python3 automation_audit.py
  python3 automation_audit.py --window-days 30 --format json
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from _ac_client import ACClient, cli_main


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


def fetch(client: ACClient, max_items: int = 50000) -> dict:
    automations = client.paginate("automations", "automations", max_items=2000)
    contact_automations = client.paginate("contactAutomations", "contactAutomations", max_items=max_items)
    return {"automations": automations, "contact_automations": contact_automations}


def analyze(data: dict, window_days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    by_auto = defaultdict(lambda: {"enrolled": 0, "completed": 0, "active": 0, "removed": 0, "recent": 0})
    for ca in data["contact_automations"]:
        aid = str(ca.get("automation"))
        b = by_auto[aid]
        b["enrolled"] += 1
        status = str(ca.get("status"))
        if status == "1":
            b["active"] += 1
        elif status == "2":
            b["completed"] += 1
        elif status == "3":
            b["removed"] += 1
        ts = _parse_iso(ca.get("adddate") or ca.get("created_timestamp"))
        if ts and ts >= cutoff:
            b["recent"] += 1

    rows = []
    orphaned = []
    for a in data["automations"]:
        aid = str(a["id"])
        b = by_auto.get(aid, {"enrolled": 0, "completed": 0, "active": 0, "removed": 0, "recent": 0})
        completion_rate = (b["completed"] / b["enrolled"]) if b["enrolled"] else 0
        rec = {
            "id": aid,
            "name": a.get("name"),
            "status": a.get("status"),
            "enrolled_total": b["enrolled"],
            "active": b["active"],
            "completed": b["completed"],
            "removed": b["removed"],
            "completion_rate": completion_rate,
            "recent_enrollments": b["recent"],
        }
        rows.append(rec)
        if b["recent"] == 0 and str(a.get("status")) == "1":
            orphaned.append(rec)
    rows.sort(key=lambda x: -x["enrolled_total"])
    return {"automations": rows, "orphaned_active": orphaned, "window_days": window_days}


def render_markdown(r: dict) -> str:
    lines = [
        "# Automation Audit",
        "",
        f"- Total automations: {len(r['automations'])}",
        f"- Active automations with 0 enrollments in last {r['window_days']} days: **{len(r['orphaned_active'])}**",
        "",
    ]
    if r["orphaned_active"]:
        lines.append("## Orphaned (active but not enrolling anyone)")
        for a in r["orphaned_active"]:
            lines.append(f"- {a['name']} (id={a['id']})")
        lines.append("")
    lines.append("## All automations")
    lines.append("| ID | Name | Status | Enrolled | Active | Completed | Removed | Completion % | Recent |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for a in r["automations"]:
        lines.append(
            f"| {a['id']} | {a['name']} | {a['status']} | {a['enrolled_total']} | "
            f"{a['active']} | {a['completed']} | {a['removed']} | "
            f"{a['completion_rate']*100:.1f}% | {a['recent_enrollments']} |"
        )
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--window-days", type=int, default=30)
    parser.add_argument("--max-items", type=int, default=50000)


def _fetch(client, args):
    return fetch(client, max_items=args.max_items)


def _analyze(data, args):
    return analyze(data, args.window_days)


def main():
    cli_main(
        description="Audit automations",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
