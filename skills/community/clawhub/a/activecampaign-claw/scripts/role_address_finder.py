#!/usr/bin/env python3
"""
role_address_finder.py — Surface role-based email addresses on the contact list.

Role addresses (info@, support@, noreply@, etc.) hurt deliverability and are
usually accidental subscriptions. Lists them so you can review and suppress.

Usage:
  python3 role_address_finder.py
  python3 role_address_finder.py --max-contacts 5000 --format json
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path

from _ac_client import ACClient

ROLE_LOCAL_PARTS = {
    "info", "support", "sales", "admin", "noreply", "no-reply", "contact",
    "hello", "team", "office", "help", "service", "marketing",
    "abuse", "postmaster", "webmaster", "hr", "jobs", "press", "media",
    "accounts", "accounting", "finance", "legal", "compliance", "inquiries",
    "feedback", "general", "enquiries", "sysadmin", "root",
}


def find_role_addresses(contacts: Iterable[dict]) -> list[dict]:
    out = []
    for c in contacts:
        email = (c.get("email") or "").strip().lower()
        if "@" not in email:
            continue
        local = email.split("@", 1)[0]
        if local in ROLE_LOCAL_PARTS:
            out.append({
                "id": c["id"],
                "email": email,
                "first_name": c.get("firstName"),
                "last_name": c.get("lastName"),
                "status": c.get("status"),
            })
    return out


def render_markdown(matches: list[dict], total: int) -> str:
    lines = [
        "# Role Address Audit",
        "",
        f"- Contacts scanned: **{total}**",
        f"- Role addresses found: **{len(matches)}** ({(len(matches) / total * 100) if total else 0:.1f}%)",
        "",
    ]
    if matches:
        lines.append("| ID | Email | Status |")
        lines.append("|---|---|---|")
        for m in matches[:200]:
            lines.append(f"| {m['id']} | {m['email']} | {m['status']} |")
        if len(matches) > 200:
            lines.append(f"\n…and {len(matches) - 200} more")
        lines.append("")
        lines.append("Recommendation: review and unsubscribe — role addresses rarely engage and risk spam complaints.")
    else:
        lines.append("**No role addresses detected.**")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find role-based email addresses")
    parser.add_argument("--max-contacts", type=int, default=10000)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    counter = {"scanned": 0}

    def _counted():
        for c in client.stream("contacts", "contacts", max_items=args.max_contacts):
            counter["scanned"] += 1
            yield c

    matches = find_role_addresses(_counted())
    scanned = counter["scanned"]

    if args.format == "json":
        out = json.dumps({"scanned": scanned, "matches": matches}, indent=2)
    else:
        out = render_markdown(matches, scanned)

    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
