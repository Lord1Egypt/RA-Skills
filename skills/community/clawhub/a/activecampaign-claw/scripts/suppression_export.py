#!/usr/bin/env python3
"""
suppression_export.py — Export all suppressed contacts (unsub, bounce) with timestamps.

Use this when you need to demonstrate suppression compliance, migrate
to another ESP, or audit unsub trends. The output includes contact email
addresses — treat it as you would any customer-data export.

Confirmation: this script requires the `--confirm` flag before running.
Without it, the script prints a notice describing what will be exported
and asks the user to re-run with `--confirm`.

Usage:
  python3 suppression_export.py --confirm
  python3 suppression_export.py --confirm --format json --output suppression.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from _ac_client import ACClient, emit_files


def fetch(client: ACClient) -> dict:
    unsubs = client.paginate("contacts", "contacts", params={"status": 2}, max_items=20000)
    bounces = client.paginate("contacts", "contacts", params={"status": 3}, max_items=20000)
    bounce_logs = client.paginate("bounceLogs", "bounceLogs", max_items=20000)
    return {"unsubs": unsubs, "bounces": bounces, "bounce_logs": bounce_logs}


def analyze(data: dict) -> dict:
    bounce_reasons = Counter()
    bounces_by_contact = {}
    for b in data["bounce_logs"]:
        cid = str(b.get("contact"))
        reason = b.get("bounceCode") or b.get("error") or "unknown"
        bounce_reasons[reason] += 1
        bounces_by_contact[cid] = {
            "code": b.get("bounceCode"),
            "error": b.get("error"),
            "tstamp": b.get("tstamp"),
        }

    unsubs = [
        {
            "id": c["id"],
            "email": c.get("email"),
            "udate": c.get("udate"),
            "cdate": c.get("cdate"),
        }
        for c in data["unsubs"]
    ]
    bounces = [
        {
            "id": c["id"],
            "email": c.get("email"),
            "bounce": bounces_by_contact.get(str(c["id"])),
        }
        for c in data["bounces"]
    ]

    return {
        "unsubscribed_count": len(unsubs),
        "bounced_count": len(bounces),
        "bounce_reason_breakdown": dict(bounce_reasons.most_common(20)),
        "unsubs": unsubs,
        "bounces": bounces,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Suppression Export",
        "",
        f"- Unsubscribed: **{r['unsubscribed_count']}**",
        f"- Bounced: **{r['bounced_count']}**",
        "",
    ]
    if r["bounce_reason_breakdown"]:
        lines.append("## Bounce reason breakdown")
        for code, n in r["bounce_reason_breakdown"].items():
            lines.append(f"- {code}: {n}")
        lines.append("")
    if r["unsubs"]:
        lines.append(f"## Unsubscribed contacts (showing first 100 of {r['unsubscribed_count']})")
        lines.append("| ID | Email | Updated |")
        lines.append("|---|---|---|")
        for u in r["unsubs"][:100]:
            lines.append(f"| {u['id']} | {u['email']} | {u['udate']} |")
        lines.append("")
    if r["bounces"]:
        lines.append(f"## Bounced contacts (showing first 100 of {r['bounced_count']})")
        lines.append("| ID | Email | Code |")
        lines.append("|---|---|---|")
        for b in r["bounces"][:100]:
            code = (b["bounce"] or {}).get("code", "—")
            lines.append(f"| {b['id']} | {b['email']} | {code} |")
        lines.append("")
    if not r["unsubs"] and not r["bounces"]:
        lines.append("No suppressed contacts found.")
    return "\n".join(lines)


_CONFIRM_NOTICE = """\
# Suppression export — confirmation required

This script will export every suppressed contact in your AC account,
including:

  - Email addresses
  - Unsubscribe and bounce timestamps
  - Bounce reason codes

The output is a local file (or stdout) — it is never sent anywhere.
Treat it like any other customer-data export: store it securely, share
it only with the people who need it for the legitimate business reason
(compliance audit, ESP migration, internal review).

To proceed:

  python3 scripts/suppression_export.py --confirm

To save to a file instead of printing:

  python3 scripts/suppression_export.py --confirm --output suppression.json --format json
"""


def main():
    parser = argparse.ArgumentParser(description="Export suppressed contacts")
    parser.add_argument("--confirm", action="store_true",
                        help="Required to actually export. Without it, "
                             "prints a notice describing what would be exported.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if not args.confirm:
        print(_CONFIRM_NOTICE)
        sys.exit(0)

    client = ACClient()
    data = fetch(client)
    r = analyze(data)
    out = json.dumps(r, indent=2, default=str) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
        emit_files(args.output)
    else:
        print(out)


if __name__ == "__main__":
    main()
