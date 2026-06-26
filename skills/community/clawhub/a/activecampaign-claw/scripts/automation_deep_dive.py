#!/usr/bin/env python3
"""
automation_deep_dive.py — Structure + funnel + active enrollments for one automation.

Pulls the automation, its blocks (steps), and the contactAutomations
records concurrently. Computes per-step drop-off the same way
`automation_funnel.py` does, but in a single combined report alongside
the structural view.

Usage:
  python3 automation_deep_dive.py <automation_id>
  python3 automation_deep_dive.py 7 --format json
"""

from __future__ import annotations

from collections import Counter

from _ac_client import ACClient, cli_main, sanitize


def _add_args(parser):
    parser.add_argument("automation_id", help="Automation id")
    parser.add_argument("--max-enrollments", type=int, default=500,
                        help="Cap on /contactAutomations sample for funnel "
                             "shape (default 500). Raise for higher precision "
                             "on big enrollments.")


def fetch_data(client: ACClient, args) -> dict:
    aid = args.automation_id
    # Metadata is a single-record endpoint, not paginated — fetch it directly.
    # Then fan out the two collection endpoints in parallel.
    meta_res = client.get(f"automations/{aid}")
    meta = meta_res.get("automation") or {}

    bulk = client.fetch_many([
        ("automationBlocks", "automationBlocks",
         {"filters[automation]": aid}, 1000),
        ("contactAutomations", "contactAutomations",
         {"filters[automation]": aid}, args.max_enrollments),
    ])
    return {
        "meta": meta,
        "blocks": bulk.get("automationBlocks") if isinstance(bulk.get("automationBlocks"), list) else [],
        "enrollments": bulk.get("contactAutomations") if isinstance(bulk.get("contactAutomations"), list) else [],
    }


def analyze(data: dict) -> dict:
    meta = data.get("meta") or {}
    blocks = data.get("blocks") or []
    enrollments = data.get("enrollments") or []

    by_status = Counter(str(e.get("status")) for e in enrollments)
    by_current_block = Counter(str(e.get("lastblock")) for e in enrollments
                               if str(e.get("status")) == "1")

    step_rows = []
    for b in sorted(blocks, key=lambda x: int(x.get("ordernum") or 0)):
        bid = str(b.get("id"))
        step_rows.append({
            "id": bid,
            "ordernum": b.get("ordernum"),
            "type": b.get("type"),
            "title": sanitize(b.get("text") or b.get("title") or ""),
            "active_at_step": by_current_block.get(bid, 0),
        })

    return {
        "id": meta.get("id"),
        "name": sanitize(meta.get("name", "")),
        "status": meta.get("status"),
        "entered": meta.get("entered"),
        "exited": meta.get("exited"),
        "by_status": dict(by_status),
        "steps": step_rows,
        "total_blocks": len(blocks),
        "total_enrollments_sampled": len(enrollments),
    }


def render_markdown(r: dict) -> str:
    status_map = {"0": "draft", "1": "active", "2": "paused"}
    lines = [
        f"# Automation deep-dive: `{r['name']}` (id={r['id']})".rstrip(),
        "",
        f"- Status: {status_map.get(str(r['status']), r['status'])}",
        f"- Lifetime: entered **{r['entered']}**, exited **{r['exited']}**",
        f"- Total blocks (steps): {r['total_blocks']}",
        f"- Enrollments sampled: {r['total_enrollments_sampled']}",
        "",
        "## Enrollment status breakdown",
    ]
    enroll_map = {"-1": "removed", "1": "active", "2": "completed", "3": "ended"}
    for status, count in sorted(r["by_status"].items(), key=lambda x: -x[1]):
        lines.append(f"- {enroll_map.get(status, status)}: {count}")
    lines.append("")
    if r["steps"]:
        lines.append("## Steps")
        lines.append("| Order | Type | Title | Active here |")
        lines.append("|---:|---|---|---:|")
        for s in r["steps"]:
            lines.append(
                f"| {s['ordernum']} | {s['type'] or '—'} | "
                f"{s['title'] or '—'} | {s['active_at_step']} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Automation structure + funnel + enrollments in one report",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
