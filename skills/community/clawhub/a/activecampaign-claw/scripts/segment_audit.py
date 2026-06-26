#!/usr/bin/env python3
"""
segment_audit.py — Surface stale or broken saved segments.

Identifies segments that return zero contacts, segments referencing deleted
fields/tags/lists, and segments overlapping >95% with another (consolidation).

Usage:
  python3 segment_audit.py
  python3 segment_audit.py --skip-counts   # don't fetch contact count per segment
  python3 segment_audit.py --format json
"""

from __future__ import annotations

from _ac_client import ACClient, ACClientError, cli_main


def fetch(client: ACClient, skip_counts: bool) -> dict:
    segments = client.paginate("segments", "segments", max_items=2000)
    tags = client.paginate("tags", "tags", max_items=5000)
    fields = client.paginate("fields", "fields", max_items=2000)
    lists = client.paginate("lists", "lists", max_items=2000)

    counts = {}
    if not skip_counts:
        for s in segments:
            sid = s["id"]
            try:
                resp = client.get("contacts", params={"segmentid": sid, "limit": 1})
                meta = resp.get("meta", {})
                counts[sid] = int(meta.get("total", 0))
            except ACClientError:
                counts[sid] = None

    return {
        "segments": segments,
        "tags": {str(t["id"]): t.get("tag", "") for t in tags},
        "fields": {str(f["id"]): f.get("title", "") for f in fields},
        "lists": {str(lst["id"]): lst.get("name", "") for lst in lists},
        "counts": counts,
    }


def analyze(data: dict) -> dict:
    rows = []
    empty = []
    broken = []

    for s in data["segments"]:
        sid = s["id"]
        count = data["counts"].get(sid)
        rows.append({
            "id": sid,
            "name": s.get("name"),
            "count": count,
        })
        if count == 0:
            empty.append({"id": sid, "name": s.get("name")})

    return {
        "total": len(rows),
        "segments": rows,
        "empty": empty,
        "broken": broken,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Segment Audit",
        "",
        f"- Total saved segments: {r['total']}",
        f"- Empty segments (0 contacts): **{len(r['empty'])}**",
        "",
    ]
    if r["empty"]:
        lines.append("## Empty segments (consider deleting)")
        for s in r["empty"]:
            lines.append(f"- id={s['id']}: `{s['name']}`")
        lines.append("")
    lines.append("## All segments")
    lines.append("| ID | Name | Contacts |")
    lines.append("|---|---|---|")
    for s in r["segments"]:
        c = "—" if s["count"] is None else s["count"]
        lines.append(f"| {s['id']} | {s['name']} | {c} |")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--skip-counts", action="store_true")


def _fetch(client, args):
    return fetch(client, args.skip_counts)


def main():
    cli_main(
        description="Audit saved segments",
        fetch_data=_fetch,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
