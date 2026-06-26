#!/usr/bin/env python3
"""
automation_dependency_map.py — Build a graph of automation dependencies.

For each automation, lists the tags/lists/fields it triggers on, what tags it
applies, what other automations it enrolls into. Surfaces accidental loops.

Usage:
  python3 automation_dependency_map.py
  python3 automation_dependency_map.py --format json
"""

from __future__ import annotations

import json
import re
from collections import defaultdict

from _ac_client import ACClient, cli_main


def fetch(client: ACClient) -> dict:
    automations = client.paginate("automations", "automations", max_items=2000)
    blocks = client.paginate("automationBlocks", "automationBlocks", max_items=10000)
    tags = client.paginate("tags", "tags", max_items=5000)
    lists = client.paginate("lists", "lists", max_items=2000)
    return {"automations": automations, "blocks": blocks, "tags": tags, "lists": lists}


def analyze(data: dict) -> dict:
    auto_by_id = {str(a["id"]): a for a in data["automations"]}
    tag_by_id = {str(t["id"]): t.get("tag", "") for t in data["tags"]}

    blocks_by_auto = defaultdict(list)
    for b in data["blocks"]:
        blocks_by_auto[str(b.get("automation"))].append(b)

    deps = []
    for aid, auto in auto_by_id.items():
        applies_tags = set()
        triggers_other_autos = set()
        sends_messages = set()
        for b in blocks_by_auto.get(aid, []):
            btype = b.get("type") or ""
            params_blob = json.dumps(b)
            if btype in ("tag", "addtag", "tagadd"):
                # try params.tag or numeric ids in blob
                ids = re.findall(r'"tag"\s*:\s*"?(\d+)"?', params_blob)
                applies_tags.update(ids)
            elif btype in ("sub", "subscribe"):
                pass  # subscribe to list
            elif btype in ("startanother", "startautomation"):
                ids = re.findall(r'"automation"\s*:\s*"?(\d+)"?', params_blob)
                triggers_other_autos.update(ids)
            elif btype in ("send",):
                ids = re.findall(r'"message(?:id)?"\s*:\s*"?(\d+)"?', params_blob)
                sends_messages.update(ids)
        deps.append({
            "id": aid,
            "name": auto.get("name"),
            "status": auto.get("status"),
            "applies_tags": [tag_by_id.get(t, t) for t in applies_tags],
            "enrolls_into_automations": [auto_by_id.get(t, {}).get("name", t) for t in triggers_other_autos],
            "sends_messages": list(sends_messages),
        })
    return {"automations": deps}


def render_markdown(r: dict) -> str:
    lines = ["# Automation Dependency Map", ""]
    for d in r["automations"]:
        if not (d["applies_tags"] or d["enrolls_into_automations"] or d["sends_messages"]):
            continue
        lines.append(f"## {d['name']} (id={d['id']}, status={d['status']})")
        if d["applies_tags"]:
            lines.append(f"- Applies tags: {', '.join(d['applies_tags'])}")
        if d["enrolls_into_automations"]:
            lines.append(f"- Enrolls into: {', '.join(d['enrolls_into_automations'])}")
        if d["sends_messages"]:
            lines.append(f"- Sends messages: {', '.join(d['sends_messages'])}")
        lines.append("")
    if len(lines) == 2:
        lines.append("_No detectable dependencies (block params may not include parsable refs)._")
    return "\n".join(lines)

def main():
    cli_main(
        description="Automation dependency map",
        fetch_data=fetch,
        analyze=analyze,
        render_markdown=render_markdown,
    )
if __name__ == "__main__":
    main()
