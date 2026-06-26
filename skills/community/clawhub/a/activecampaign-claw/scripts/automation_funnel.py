#!/usr/bin/env python3
"""
automation_funnel.py — Per-step dropoff for one automation.

Counts contacts at each block: enrolled → completed step 1 → step 2 → … →
exited (completed vs. removed). Shows where they fall out.

Usage:
  python3 automation_funnel.py <automation_id>
  python3 automation_funnel.py 5 --format json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from _ac_client import ACClient


def fetch(client: ACClient, automation_id: str) -> dict:
    automation = client.get(f"automations/{automation_id}").get("automation", {})
    blocks = client.paginate("automationBlocks", "automationBlocks", params={"filters[automation]": automation_id}, max_items=2000)
    contact_autos = client.paginate("contactAutomations", "contactAutomations", params={"filters[automation]": automation_id}, max_items=20000)
    return {"automation": automation, "blocks": blocks, "contact_automations": contact_autos}


def analyze(data: dict) -> dict:
    blocks = sorted(data["blocks"], key=lambda b: int(b.get("ordernum") or 0))
    by_status = Counter()
    last_block_count = Counter()
    for ca in data["contact_automations"]:
        status = str(ca.get("status"))
        by_status[status] += 1
        last = str(ca.get("lastblock"))
        if last:
            last_block_count[last] += 1
    enrolled = sum(by_status.values())
    completed = by_status.get("2", 0)
    active = by_status.get("1", 0)
    removed = by_status.get("3", 0)

    funnel = []
    for b in blocks:
        cur = last_block_count.get(b["id"], 0)
        funnel.append({
            "block_id": b["id"],
            "order": b.get("ordernum"),
            "type": b.get("type"),
            "title": b.get("title") or b.get("description") or b.get("type"),
            "contacts_at_block": cur,
        })
    return {
        "automation_id": data["automation"].get("id"),
        "name": data["automation"].get("name"),
        "status": data["automation"].get("status"),
        "enrolled_total": enrolled,
        "active": active,
        "completed": completed,
        "removed": removed,
        "completion_rate": (completed / enrolled) if enrolled else 0,
        "blocks": funnel,
    }


def render_markdown(r: dict) -> str:
    lines = [
        f"# Automation Funnel: {r['name']} (id={r['automation_id']})",
        "",
        f"- Status: {r['status']}",
        f"- Enrolled total: {r['enrolled_total']}",
        f"- Active: {r['active']}",
        f"- Completed: {r['completed']}",
        f"- Removed: {r['removed']}",
        f"- Completion rate: {r['completion_rate']*100:.1f}%",
        "",
        "## Per-block (last position of each contact)",
        "| Order | Type | Title | Contacts at block |",
        "|---|---|---|---|",
    ]
    for b in r["blocks"]:
        lines.append(f"| {b['order']} | {b['type']} | {b['title']} | {b['contacts_at_block']} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Automation funnel")
    parser.add_argument("automation_id")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    data = fetch(client, args.automation_id)
    r = analyze(data)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
