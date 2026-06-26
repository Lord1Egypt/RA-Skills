#!/usr/bin/env python3
"""
form_audit.py — Per-form quality: contacts created, engagement of those contacts.

Catches forms feeding garbage. Joins forms → contacts that have form metadata
(or sourceid) → engagement signal from messageActivities/linkData fallback.

Usage:
  python3 form_audit.py
  python3 form_audit.py --format json
"""

from __future__ import annotations

from collections import defaultdict

from _ac_client import ACClient, cli_main


def fetch(client: ACClient) -> dict:
    forms = client.paginate("forms", "forms", max_items=500)
    contacts = client.paginate("contacts", "contacts", max_items=20000)
    activities = client.fetch_engagement_events(max_items=30000)
    return {"forms": forms, "contacts": contacts, "activities": activities}


def analyze(data: dict) -> dict:
    contacts_by_form = defaultdict(list)
    for c in data["contacts"]:
        # AC stores form id in contact.sourceid for form-sourced contacts (when populated)
        sid = str(c.get("sourceid") or "")
        if sid:
            contacts_by_form[sid].append(c)

    engaged = set()
    for a in data["activities"]:
        if a.get("event") in ("open", "click"):
            engaged.add(a.get("contact"))

    rows = []
    for f in data["forms"]:
        fid = str(f["id"])
        cs = contacts_by_form.get(fid, [])
        engaged_count = sum(1 for c in cs if str(c["id"]) in engaged)
        rows.append({
            "id": fid,
            "name": f.get("name"),
            "contacts": len(cs),
            "engaged_contacts": engaged_count,
            "engagement_rate": (engaged_count / len(cs)) if cs else 0,
        })
    rows.sort(key=lambda x: -x["contacts"])
    return {"forms": rows, "total_forms": len(data["forms"])}


def render_markdown(r: dict) -> str:
    lines = [
        "# Form Audit",
        "",
        f"Total forms: {r['total_forms']}",
        "",
        "| ID | Name | Contacts | Engaged | Engagement % |",
        "|---|---|---|---|---|",
    ]
    for f in r["forms"]:
        lines.append(
            f"| {f['id']} | {f['name']} | {f['contacts']} | "
            f"{f['engaged_contacts']} | {f['engagement_rate']*100:.1f}% |"
        )
    return "\n".join(lines)

def main():
    cli_main(
        description="Form audit",
        fetch_data=fetch,
        analyze=analyze,
        render_markdown=render_markdown,
    )
if __name__ == "__main__":
    main()
