#!/usr/bin/env python3
"""
contact_completeness_report.py — % of contacts with each field populated.

Measures built-in fields (firstName, lastName, phone) and custom fields
across the contact base. Catches forms asking for too little.

Usage:
  python3 contact_completeness_report.py
  python3 contact_completeness_report.py --max-contacts 5000 --format json
"""

from __future__ import annotations

from collections import Counter, defaultdict

from _ac_client import ACClient, cli_main


def fetch(client: ACClient, max_contacts: int) -> dict:
    contacts = client.paginate("contacts", "contacts", max_items=max_contacts)
    fields = client.paginate("fields", "fields", max_items=2000)
    field_values = client.paginate("fieldValues", "fieldValues", max_items=max_contacts * 5)
    return {"contacts": contacts, "fields": fields, "field_values": field_values}


def analyze(data: dict) -> dict:
    contacts = data["contacts"]
    fields = data["fields"]
    fvs = data["field_values"]

    total = len(contacts)
    builtin_present = Counter()
    for c in contacts:
        if (c.get("firstName") or "").strip():
            builtin_present["firstName"] += 1
        if (c.get("lastName") or "").strip():
            builtin_present["lastName"] += 1
        if (c.get("phone") or "").strip():
            builtin_present["phone"] += 1

    # field values: count contacts with non-empty value per field
    field_contact_set = defaultdict(set)
    for fv in fvs:
        v = (fv.get("value") or "").strip()
        if v and fv.get("contact") and fv.get("field"):
            field_contact_set[str(fv["field"])].add(str(fv["contact"]))

    custom_completeness = []
    for f in fields:
        fid = str(f["id"])
        n = len(field_contact_set.get(fid, set()))
        custom_completeness.append({
            "id": fid,
            "title": f.get("title", ""),
            "type": f.get("type", ""),
            "populated": n,
            "pct": (n / total * 100) if total else 0,
        })

    custom_completeness.sort(key=lambda x: -x["populated"])

    return {
        "total_contacts": total,
        "builtin": {
            "firstName": {
                "populated": builtin_present["firstName"],
                "pct": (builtin_present["firstName"] / total * 100) if total else 0,
            },
            "lastName": {
                "populated": builtin_present["lastName"],
                "pct": (builtin_present["lastName"] / total * 100) if total else 0,
            },
            "phone": {
                "populated": builtin_present["phone"],
                "pct": (builtin_present["phone"] / total * 100) if total else 0,
            },
        },
        "custom_fields": custom_completeness,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Contact Completeness Report",
        "",
        f"Total contacts: **{r['total_contacts']}**",
        "",
        "## Built-in fields",
        f"- firstName: {r['builtin']['firstName']['populated']} ({r['builtin']['firstName']['pct']:.1f}%)",
        f"- lastName: {r['builtin']['lastName']['populated']} ({r['builtin']['lastName']['pct']:.1f}%)",
        f"- phone: {r['builtin']['phone']['populated']} ({r['builtin']['phone']['pct']:.1f}%)",
        "",
        "## Custom fields",
        "| Field | Type | Populated | % |",
        "|---|---|---|---|",
    ]
    for cf in r["custom_fields"]:
        lines.append(f"| {cf['title']} | {cf['type']} | {cf['populated']} | {cf['pct']:.1f}% |")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--max-contacts", type=int, default=5000)


def _fetch(client, args):
    return fetch(client, args.max_contacts)


def main():
    cli_main(
        description="Contact field completeness",
        fetch_data=_fetch,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
