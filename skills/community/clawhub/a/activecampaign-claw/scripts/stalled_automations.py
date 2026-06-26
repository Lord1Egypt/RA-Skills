#!/usr/bin/env python3
"""
stalled_automations.py — Contacts whose automation step hasn't advanced in N days.

Likely stuck on a Wait or malformed If/Else. Lists contact + automation +
days-since-last-step.

Usage:
  python3 stalled_automations.py
  python3 stalled_automations.py --min-days 14 --format json
"""

from __future__ import annotations

from datetime import datetime, timezone

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
    contact_autos = client.paginate("contactAutomations", "contactAutomations", max_items=max_items)
    return {"automations": automations, "contact_automations": contact_autos}


def analyze(data: dict, min_days: int) -> dict:
    name_by_id = {str(a["id"]): a.get("name") for a in data["automations"]}
    now = datetime.now(timezone.utc)
    stalled = []
    for ca in data["contact_automations"]:
        if str(ca.get("status")) != "1":
            continue
        # AC exposes last update via lastdate / updated_timestamp on contactAutomation
        ts = _parse_iso(ca.get("lastdate") or ca.get("updated_timestamp"))
        if not ts:
            continue
        days = (now - ts).total_seconds() / 86400
        if days >= min_days:
            stalled.append({
                "contact": ca.get("contact"),
                "automation": name_by_id.get(str(ca.get("automation"))),
                "lastblock": ca.get("lastblock"),
                "days_since_advance": int(days),
                "last_update": ts.isoformat(),
            })
    stalled.sort(key=lambda x: -x["days_since_advance"])
    return {"min_days": min_days, "stalled_count": len(stalled), "stalled": stalled}


def render_markdown(r: dict) -> str:
    lines = [
        f"# Stalled Automation Enrollments (>{r['min_days']} days without advance)",
        "",
        f"Stalled contacts: **{r['stalled_count']}**",
        "",
    ]
    if r["stalled"]:
        lines.append("| Contact | Automation | Last block | Days stalled | Last update |")
        lines.append("|---|---|---|---|---|")
        for s in r["stalled"][:200]:
            lines.append(
                f"| {s['contact']} | {s['automation']} | {s['lastblock']} | "
                f"{s['days_since_advance']} | {s['last_update']} |"
            )
    else:
        lines.append("_No stalled enrollments._")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--min-days", type=int, default=14)
    parser.add_argument("--max-items", type=int, default=50000)


def _fetch(client, args):
    return fetch(client, max_items=args.max_items)


def _analyze(data, args):
    return analyze(data, args.min_days)


def main():
    cli_main(
        description="Stalled automation enrollments",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
