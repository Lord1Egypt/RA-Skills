#!/usr/bin/env python3
"""
schema_diff.py — Compare two account snapshots and report taxonomy changes.

Snapshots are produced by account_archive.py / snapshot.py. Diffs lists, tags,
custom fields, automations (by name + status). Local-only.

Usage:
  python3 schema_diff.py before.json after.json
  python3 schema_diff.py before.json after.json --format json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _index(items: list, key: str = "id", name_key: str = "name") -> dict:
    return {str(item.get(key)): item for item in items if item.get(key) is not None}


def _diff_collection(a: list, b: list, name_key: str = "name") -> dict:
    a_idx = _index(a)
    b_idx = _index(b)
    a_ids = set(a_idx)
    b_ids = set(b_idx)
    added_ids = b_ids - a_ids
    removed_ids = a_ids - b_ids
    common_ids = a_ids & b_ids
    renamed = []
    for cid in common_ids:
        an = (a_idx[cid].get(name_key) or "").strip()
        bn = (b_idx[cid].get(name_key) or "").strip()
        if an != bn:
            renamed.append({"id": cid, "from": an, "to": bn})
    return {
        "added": [b_idx[i] for i in sorted(added_ids)],
        "removed": [a_idx[i] for i in sorted(removed_ids)],
        "renamed": renamed,
    }


def diff(before: dict, after: dict) -> dict:
    bt = before.get("taxonomy", before)
    at = after.get("taxonomy", after)

    out = {}
    out["lists"] = _diff_collection(bt.get("lists", []), at.get("lists", []), "name")
    out["tags"] = _diff_collection(bt.get("tags", []), at.get("tags", []), "name")

    bcf = (bt.get("custom_fields") or {}).get("contacts", [])
    acf = (at.get("custom_fields") or {}).get("contacts", [])
    out["contact_fields"] = _diff_collection(bcf, acf, "title")

    bdf = (bt.get("custom_fields") or {}).get("deals", [])
    adf = (at.get("custom_fields") or {}).get("deals", [])
    out["deal_fields"] = _diff_collection(bdf, adf, "fieldLabel")

    out["pipelines"] = _diff_collection(bt.get("pipelines", []), at.get("pipelines", []), "name")
    out["automations"] = _diff_collection(bt.get("automations", []), at.get("automations", []), "name")

    # status changes for automations
    a_auto = _index(bt.get("automations", []))
    b_auto = _index(at.get("automations", []))
    status_changes = []
    for aid in set(a_auto) & set(b_auto):
        if a_auto[aid].get("status") != b_auto[aid].get("status"):
            status_changes.append({
                "id": aid,
                "name": b_auto[aid].get("name"),
                "from": a_auto[aid].get("status"),
                "to": b_auto[aid].get("status"),
            })
    out["automations"]["status_changed"] = status_changes
    return out


def render_markdown(d: dict) -> str:
    lines = ["# Schema diff", ""]
    for section, label in [
        ("lists", "Lists"),
        ("tags", "Tags"),
        ("contact_fields", "Contact fields"),
        ("deal_fields", "Deal fields"),
        ("pipelines", "Pipelines"),
        ("automations", "Automations"),
    ]:
        sec = d[section]
        added = sec["added"]
        removed = sec["removed"]
        renamed = sec["renamed"]
        status = sec.get("status_changed", [])
        if not (added or removed or renamed or status):
            continue
        lines.append(f"## {label}")
        if added:
            lines.append(f"**Added ({len(added)}):**")
            for x in added:
                name = x.get("name") or x.get("title") or x.get("fieldLabel") or x.get("id")
                lines.append(f"- {name} (id={x.get('id')})")
        if removed:
            lines.append(f"**Removed ({len(removed)}):**")
            for x in removed:
                name = x.get("name") or x.get("title") or x.get("fieldLabel") or x.get("id")
                lines.append(f"- {name} (id={x.get('id')})")
        if renamed:
            lines.append(f"**Renamed ({len(renamed)}):**")
            for r in renamed:
                lines.append(f"- id={r['id']}: `{r['from']}` → `{r['to']}`")
        if status:
            lines.append(f"**Status changed ({len(status)}):**")
            for s in status:
                lines.append(f"- {s['name']}: {s['from']} → {s['to']}")
        lines.append("")
    if len(lines) == 2:
        lines.append("No structural changes.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Diff two AC account snapshots")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    before = json.loads(Path(args.before).read_text())
    after = json.loads(Path(args.after).read_text())
    d = diff(before, after)
    out = json.dumps(d, indent=2) if args.format == "json" else render_markdown(d)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
