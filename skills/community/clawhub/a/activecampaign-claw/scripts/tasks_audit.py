#!/usr/bin/env python3
"""
tasks_audit.py — Sales-rep task hygiene + workload audit.

Pulls /dealTasks (reltype=Deal and reltype=Subscriber covers both deal
and contact tasks — there is no separate /contactTasks endpoint in v3).
Reports overdue tasks, per-user completion rate, unassigned tasks,
and task age statistics.

Plan gating: /dealTasks requires CRM/Sales (Plus+). On Lite, the endpoint
returns 403 — the script exits cleanly with a "feature not enabled" message.

Usage:
  python3 tasks_audit.py
  python3 tasks_audit.py --window-days 90
  python3 tasks_audit.py --format json --output tasks_audit.json
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone

from _ac_client import (
    ACClient,
    ACClientError,
    cli_main,
    render_feature_unavailable,
)
from _ac_client import parse_date as _parse_date


def fetch_data(client: ACClient) -> dict:
    """Fetch tasks (both Deal and Subscriber reltype) and users."""
    try:
        deal_tasks = client.paginate(
            "dealTasks", "dealTasks",
            params={"filters[reltype]": "Deal"},
            max_items=20000,
        )
        contact_tasks = client.paginate(
            "dealTasks", "dealTasks",
            params={"filters[reltype]": "Subscriber"},
            max_items=20000,
        )
    except ACClientError as e:
        if e.status_code == 403:
            return {"unavailable": True, "reason": "tasks_feature_not_enabled"}
        raise
    users = client.paginate("users", "users", max_items=500)
    return {
        "tasks": deal_tasks + contact_tasks,
        "users": users,
        "unavailable": False,
    }


def analyze(data: dict, now: datetime | None = None) -> dict:
    if data.get("unavailable"):
        return {"unavailable": True, "reason": data.get("reason")}

    now = now or datetime.now(timezone.utc)
    tasks = data["tasks"]
    users = data["users"]

    user_by_id = {str(u["id"]): u for u in users}

    open_tasks = [t for t in tasks if str(t.get("status", "0")) == "0"]
    completed_tasks = [t for t in tasks if str(t.get("status", "0")) == "1"]

    overdue = []
    for t in open_tasks:
        due = _parse_date(t.get("duedate"))
        if due and due < now:
            overdue.append({
                "id": t["id"],
                "title": t.get("title", ""),
                "duedate": t.get("duedate"),
                "days_overdue": (now - due).days,
                "assignee_userid": t.get("assignee_userid") or t.get("userid"),
                "reltype": t.get("reltype"),
                "relid": t.get("relid"),
            })

    per_user = defaultdict(lambda: {
        "open": 0, "completed": 0, "overdue": 0,
        "name": "", "email": "",
    })
    for t in tasks:
        uid = str(t.get("assignee_userid") or t.get("userid") or "")
        if not uid:
            uid = "unassigned"
        bucket = per_user[uid]
        if uid in user_by_id:
            u = user_by_id[uid]
            bucket["name"] = f"{u.get('firstName', '')} {u.get('lastName', '')}".strip() or u.get("username", "")
            bucket["email"] = u.get("email", "")
        elif uid == "unassigned":
            bucket["name"] = "(unassigned)"
        if str(t.get("status", "0")) == "1":
            bucket["completed"] += 1
        else:
            bucket["open"] += 1
            due = _parse_date(t.get("duedate"))
            if due and due < now:
                bucket["overdue"] += 1

    user_rows = []
    for uid, bucket in per_user.items():
        total = bucket["open"] + bucket["completed"]
        completion_rate = bucket["completed"] / total if total else 0.0
        user_rows.append({
            "userid": uid,
            "name": bucket["name"] or f"user-{uid}",
            "email": bucket["email"],
            "open": bucket["open"],
            "completed": bucket["completed"],
            "overdue": bucket["overdue"],
            "completion_rate": completion_rate,
        })
    user_rows.sort(key=lambda r: -r["overdue"])

    completion_age_days = []
    for t in completed_tasks:
        created = _parse_date(t.get("cdate"))
        completed = _parse_date(t.get("udate"))
        if created and completed and completed >= created:
            completion_age_days.append((completed - created).days)
    completion_age_days.sort()

    median_age = (
        completion_age_days[len(completion_age_days) // 2]
        if completion_age_days else None
    )

    reltype_counts = Counter(str(t.get("reltype", "")) for t in tasks)

    return {
        "total_tasks": len(tasks),
        "open": len(open_tasks),
        "completed": len(completed_tasks),
        "overdue": len(overdue),
        "unassigned_open": sum(1 for t in open_tasks if not (t.get("assignee_userid") or t.get("userid"))),
        "by_reltype": dict(reltype_counts),
        "median_completion_age_days": median_age,
        "overdue_tasks": sorted(overdue, key=lambda t: -t["days_overdue"])[:50],
        "users": user_rows,
        "unavailable": False,
    }


def render_markdown(r: dict) -> str:
    if r.get("unavailable"):
        return render_feature_unavailable(
            "Tasks (CRM)", "Plus",
            "Tasks audit needs the /dealTasks endpoint.",
        )

    lines = [
        "# Tasks Audit",
        "",
        f"- Total tasks: **{r['total_tasks']}** (open: {r['open']}, completed: {r['completed']})",
        f"- Overdue (open + past due date): **{r['overdue']}**",
        f"- Unassigned open tasks: **{r['unassigned_open']}**",
        f"- Reltype breakdown: {r['by_reltype']}",
    ]
    if r.get("median_completion_age_days") is not None:
        lines.append(
            f"- Median time to complete: **{r['median_completion_age_days']} days**"
        )
    lines.append("")

    if r["users"]:
        lines.append("## Per-user workload")
        lines.append("")
        lines.append("| User | Open | Completed | Overdue | Completion rate |")
        lines.append("|---|---:|---:|---:|---:|")
        for u in r["users"][:20]:
            lines.append(
                f"| {u['name']} | {u['open']} | {u['completed']} | "
                f"{u['overdue']} | {u['completion_rate']*100:.0f}% |"
            )
        lines.append("")

    if r["overdue_tasks"]:
        lines.append("## Most overdue tasks")
        lines.append("")
        for t in r["overdue_tasks"][:25]:
            lines.append(
                f"- {t['days_overdue']}d overdue · {t['reltype']} {t['relid']} "
                f"· `{t['title']}` (assignee userid={t['assignee_userid']})"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    cli_main(
        description="Audit task workload + overdue items",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        feature_unavailable=(
            "Tasks (CRM)", "Plus",
            "Tasks audit needs the /dealTasks endpoint.",
        ),
    )


if __name__ == "__main__":
    main()
