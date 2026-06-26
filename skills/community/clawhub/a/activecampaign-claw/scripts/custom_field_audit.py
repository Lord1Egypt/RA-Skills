#!/usr/bin/env python3
"""
custom_field_audit.py — Audit custom fields for hygiene and dependencies.

Per field: % of contacts with a value, value cardinality, whether any segment
or automation references it. Surfaces zombie fields safe to delete.

Usage:
  python3 custom_field_audit.py
  python3 custom_field_audit.py --format json
"""

from __future__ import annotations

import json
from collections import defaultdict

from _ac_client import ACClient, cli_main


def fetch(client: ACClient, max_field_values: int) -> dict:
    fields = client.paginate("fields", "fields", max_items=2000)
    field_values = client.paginate("fieldValues", "fieldValues", max_items=max_field_values)
    automations = client.paginate("automations", "automations", max_items=2000)
    segments = client.paginate("segments", "segments", max_items=2000)
    contacts = client.paginate("contacts", "contacts", max_items=10000)
    return {
        "fields": fields,
        "field_values": field_values,
        "automations": automations,
        "segments": segments,
        "contact_count": len(contacts),
    }


def analyze(data: dict) -> dict:
    fields = data["fields"]
    fvs = data["field_values"]
    total = data["contact_count"]

    by_field = defaultdict(list)
    for fv in fvs:
        fid = str(fv.get("field"))
        v = (fv.get("value") or "").strip()
        if v:
            by_field[fid].append(v)

    auto_blob = json.dumps(data["automations"])
    seg_blob = json.dumps(data["segments"])

    out = []
    for f in fields:
        fid = str(f["id"])
        title = f.get("title", "")
        values = by_field.get(fid, [])
        n_values = len(values)
        unique = len(set(values))
        # check if title or perstag is referenced anywhere
        perstag = f.get("perstag") or ""
        referenced = (title and title in auto_blob) or (title and title in seg_blob) \
            or (perstag and perstag in auto_blob) or (perstag and perstag in seg_blob)
        out.append({
            "id": fid,
            "title": title,
            "type": f.get("type"),
            "perstag": perstag,
            "populated": n_values,
            "pct": (n_values / total * 100) if total else 0,
            "unique_values": unique,
            "used_in_automation_or_segment": bool(referenced),
        })

    out.sort(key=lambda x: x["pct"])
    zombies = [x for x in out if x["populated"] == 0 and not x["used_in_automation_or_segment"]]
    low_use = [x for x in out if 0 < x["pct"] < 5 and not x["used_in_automation_or_segment"]]

    return {
        "total_contacts": total,
        "fields": out,
        "zombies": zombies,
        "low_use_unreferenced": low_use,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Custom Field Audit",
        "",
        f"- Total contacts: {r['total_contacts']}",
        f"- Total custom fields: {len(r['fields'])}",
        f"- Zombie fields (0 values, unreferenced): **{len(r['zombies'])}**",
        f"- Low-use fields (<5% populated, unreferenced): **{len(r['low_use_unreferenced'])}**",
        "",
        "## All fields",
        "| Field | Type | Populated | % | Unique | Referenced? |",
        "|---|---|---|---|---|---|",
    ]
    for f in r["fields"]:
        lines.append(
            f"| {f['title']} | {f['type']} | {f['populated']} | {f['pct']:.1f}% | "
            f"{f['unique_values']} | {'yes' if f['used_in_automation_or_segment'] else 'no'} |"
        )
    if r["zombies"]:
        lines.append("")
        lines.append("## Zombie fields (safe to delete)")
        for z in r["zombies"]:
            lines.append(f"- {z['title']} (id={z['id']}, type={z['type']})")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--max-field-values", type=int, default=20000)


def _fetch(client, args):
    return fetch(client, args.max_field_values)


def main():
    cli_main(
        description="Audit custom fields",
        fetch_data=_fetch,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
