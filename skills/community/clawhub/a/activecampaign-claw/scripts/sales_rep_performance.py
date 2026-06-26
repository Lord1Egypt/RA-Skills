#!/usr/bin/env python3
"""
sales_rep_performance.py — Per-rep deal, task, and note performance roll-up.

Cross-references /users, /deals, /dealTasks (reltype=Deal), and /notes
into a single per-rep scoreboard:

  - deals owned (open / won / lost)
  - win rate
  - avg deal value (closed-won)
  - open task count + overdue task count
  - notes count + median note length
  - composite "activity score" (notes + completed-task velocity)

Plan gating: /deals and /dealTasks both require CRM/Sales (Plus+). On Lite,
the script reports "feature not enabled" instead of crashing.

Usage:
  python3 sales_rep_performance.py
  python3 sales_rep_performance.py --format json --output sales_perf.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import ACClient, ACClientError, emit_files
from _ac_client import parse_date as _parse_date


def fetch_data(client: ACClient) -> dict:
    users = client.paginate("users", "users", max_items=500)
    notes = client.paginate("notes", "notes", max_items=20000)

    try:
        deals = client.paginate("deals", "deals", max_items=10000)
        deal_tasks = client.paginate(
            "dealTasks", "dealTasks",
            params={"filters[reltype]": "Deal"},
            max_items=20000,
        )
    except ACClientError as e:
        if e.status_code == 403:
            return {
                "users": users, "notes": notes,
                "deals_unavailable": True,
            }
        raise

    return {
        "users": users,
        "notes": notes,
        "deals": deals,
        "deal_tasks": deal_tasks,
        "deals_unavailable": False,
    }


def analyze(data: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    users = data["users"]
    notes = data["notes"]
    deals_unavailable = data.get("deals_unavailable", False)

    rep_stats = {
        str(u["id"]): {
            "userid": str(u["id"]),
            "name": (
                f"{u.get('firstName', '')} {u.get('lastName', '')}".strip()
                or u.get("username", f"user-{u['id']}")
            ),
            "email": u.get("email", ""),
            "deals_open": 0, "deals_won": 0, "deals_lost": 0,
            "deal_value_won_cents": 0,
            "tasks_open": 0, "tasks_overdue": 0, "tasks_completed": 0,
            "notes_count": 0, "notes_total_length": 0,
        }
        for u in users
    }

    if not deals_unavailable:
        # AC deal status: 0=open, 1=won, 2=lost, 3=hot
        for d in data.get("deals", []):
            uid = str(d.get("owner") or "")
            if uid not in rep_stats:
                continue
            status = str(d.get("status", "0"))
            if status == "1":
                rep_stats[uid]["deals_won"] += 1
                try:
                    rep_stats[uid]["deal_value_won_cents"] += int(d.get("value", 0))
                except (ValueError, TypeError):
                    pass
            elif status == "2":
                rep_stats[uid]["deals_lost"] += 1
            else:
                rep_stats[uid]["deals_open"] += 1

        for t in data.get("deal_tasks", []):
            uid = str(t.get("assignee_userid") or t.get("userid") or "")
            if uid not in rep_stats:
                continue
            if str(t.get("status", "0")) == "1":
                rep_stats[uid]["tasks_completed"] += 1
            else:
                rep_stats[uid]["tasks_open"] += 1
                due = _parse_date(t.get("duedate"))
                if due and due < now:
                    rep_stats[uid]["tasks_overdue"] += 1

    for n in notes:
        uid = str(n.get("userid") or "")
        if uid not in rep_stats:
            continue
        rep_stats[uid]["notes_count"] += 1
        rep_stats[uid]["notes_total_length"] += len(n.get("note") or "")

    rows = []
    for s in rep_stats.values():
        deals_total = s["deals_open"] + s["deals_won"] + s["deals_lost"]
        closed = s["deals_won"] + s["deals_lost"]
        win_rate = s["deals_won"] / closed if closed else None
        avg_won_value = (
            s["deal_value_won_cents"] / s["deals_won"]
            if s["deals_won"] else 0
        )
        avg_note_len = (
            s["notes_total_length"] / s["notes_count"]
            if s["notes_count"] else 0
        )
        # activity = log-scale combination of notes + tasks completed; signal of engagement
        activity_score = s["notes_count"] + s["tasks_completed"] * 2
        rows.append({
            **s,
            "deals_total": deals_total,
            "win_rate": win_rate,
            "avg_won_value_cents": int(avg_won_value),
            "avg_note_length": int(avg_note_len),
            "activity_score": activity_score,
        })

    rows.sort(key=lambda r: -r["activity_score"])

    return {
        "deals_unavailable": deals_unavailable,
        "reps": rows,
        "total_users": len(users),
    }


def _fmt_pct(p: float | None) -> str:
    return f"{p*100:.0f}%" if p is not None else "—"


def _fmt_dollars(cents: int) -> str:
    return f"${cents / 100:,.0f}" if cents else "—"


def render_markdown(r: dict) -> str:
    note = (
        "\n*(Deals + tasks unavailable on this AC plan — showing notes only.)*\n"
        if r["deals_unavailable"] else ""
    )
    lines = [
        "# Sales Rep Performance",
        "",
        f"- Sales reps: **{r['total_users']}**" + note,
        "",
        "## Per-rep scoreboard (sorted by activity score)",
        "",
    ]
    if r["deals_unavailable"]:
        lines += [
            "| Rep | Notes | Avg note length |",
            "|---|---:|---:|",
        ]
        for rep in r["reps"][:50]:
            lines.append(
                f"| {rep['name']} | {rep['notes_count']} | {rep['avg_note_length']} chars |"
            )
    else:
        lines += [
            "| Rep | Open | Won | Lost | Win rate | Avg won | Tasks open / overdue | Notes | Activity |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for rep in r["reps"][:50]:
            lines.append(
                f"| {rep['name']} | {rep['deals_open']} | {rep['deals_won']} | "
                f"{rep['deals_lost']} | {_fmt_pct(rep['win_rate'])} | "
                f"{_fmt_dollars(rep['avg_won_value_cents'])} | "
                f"{rep['tasks_open']} / {rep['tasks_overdue']} | "
                f"{rep['notes_count']} | {rep['activity_score']} |"
            )
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Per-rep performance scoreboard")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    data = fetch_data(client)
    report = analyze(data)
    out = json.dumps(report, indent=2) if args.format == "json" else render_markdown(report)

    if args.output:
        path = Path(args.output)
        path.write_text(out)
        print(f"Wrote {path}")
        emit_files(path)
    else:
        print(out)


if __name__ == "__main__":
    main()
