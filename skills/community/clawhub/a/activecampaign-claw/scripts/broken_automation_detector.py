#!/usr/bin/env python3
"""
broken_automation_detector.py — Find automations referencing deleted assets.

Walks each automation's blocks and flags references to tag/field/list/message
ids that no longer exist.

Usage:
  python3 broken_automation_detector.py
  python3 broken_automation_detector.py --format json
"""

from __future__ import annotations

import json
import re
from collections import defaultdict

from _ac_client import ACClient, cli_main

REF_PATTERNS = {
    "tag": re.compile(r'"tag"\s*:\s*"?(\d+)"?'),
    "field": re.compile(r'"field"\s*:\s*"?(\d+)"?'),
    "list": re.compile(r'"list"\s*:\s*"?(\d+)"?'),
    "message": re.compile(r'"message(?:id)?"\s*:\s*"?(\d+)"?'),
    "automation": re.compile(r'"automation"\s*:\s*"?(\d+)"?'),
}


def fetch(client: ACClient) -> dict:
    automations = client.paginate("automations", "automations", max_items=2000)
    blocks = client.paginate("automationBlocks", "automationBlocks", max_items=10000)
    tags = client.paginate("tags", "tags", max_items=5000)
    fields = client.paginate("fields", "fields", max_items=2000)
    lists = client.paginate("lists", "lists", max_items=2000)
    messages = client.paginate("messages", "messages", max_items=5000)
    return {
        "automations": automations,
        "blocks": blocks,
        "valid": {
            "tag": {str(t["id"]) for t in tags},
            "field": {str(f["id"]) for f in fields},
            "list": {str(lst["id"]) for lst in lists},
            "message": {str(m["id"]) for m in messages},
            "automation": {str(a["id"]) for a in automations},
        },
    }


def analyze(data: dict) -> dict:
    blocks_by_auto = defaultdict(list)
    for b in data["blocks"]:
        blocks_by_auto[str(b.get("automation"))].append(b)

    auto_by_id = {str(a["id"]): a for a in data["automations"]}
    broken_by_auto = []

    for aid, blocks in blocks_by_auto.items():
        broken_refs = defaultdict(set)
        for b in blocks:
            blob = json.dumps(b)
            for kind, pattern in REF_PATTERNS.items():
                for found in pattern.findall(blob):
                    if found not in data["valid"][kind]:
                        broken_refs[kind].add(found)
        if any(broken_refs.values()):
            broken_by_auto.append({
                "id": aid,
                "name": auto_by_id.get(aid, {}).get("name", "(deleted automation)"),
                "broken": {k: sorted(v) for k, v in broken_refs.items()},
            })

    return {"broken": broken_by_auto, "automations_scanned": len(blocks_by_auto)}


def render_markdown(r: dict) -> str:
    lines = [
        "# Broken Automation Detector",
        "",
        f"Automations scanned: {r['automations_scanned']}",
        f"Automations with broken refs: **{len(r['broken'])}**",
        "",
    ]
    for b in r["broken"]:
        lines.append(f"## {b['name']} (id={b['id']})")
        for kind, ids in b["broken"].items():
            lines.append(f"- Missing {kind} ids: {', '.join(ids)}")
        lines.append("")
    if not r["broken"]:
        lines.append("_All automations reference valid assets._")
    return "\n".join(lines)

def main():
    cli_main(
        description="Detect broken automation refs",
        fetch_data=fetch,
        analyze=analyze,
        render_markdown=render_markdown,
    )
if __name__ == "__main__":
    main()
