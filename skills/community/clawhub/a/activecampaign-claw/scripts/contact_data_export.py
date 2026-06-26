#!/usr/bin/env python3
"""
contact_data_export.py — Raw per-contact JSON dump across all sub-resources.

Pulls one contact's profile plus every related record (custom-field values,
tags, list memberships, automation enrollments, deals) into a single local
JSON file. The output is on your machine — never transmitted anywhere.

Use cases:
  - Deep debugging: "what does AC actually think about this contact?"
  - Pre-change baseline: capture state before a manual fix in the dashboard
  - Audit support: provide a reviewable record of one contact's data
  - Compliance request handling: when a contact asks what data you hold
    about them, this gives you a single artifact to work from before
    forwarding through whatever legally-required channel applies

The output contains the contact's personal data. Treat it as you would any
other customer-data file (store securely, share only with people who need
it, delete when no longer needed).

Confirmation: this script requires `--confirm` before running. Without it,
the script prints a notice describing what would be exported and exits.

Usage:
  python3 contact_data_export.py user@example.com --confirm
  python3 contact_data_export.py user@example.com --confirm --output report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _ac_client import ACClient, emit_files


def fetch(client: ACClient, email: str) -> dict:
    res = client.get("contacts", params={"email": email})
    contacts = res.get("contacts") or []
    if not contacts:
        raise SystemExit(
            f"No contact found with email '{email}'. "
            f"Check the spelling, or look up the contact in your AC dashboard first."
        )
    contact = contacts[0]
    cid = contact["id"]

    # Fetch every per-contact subresource in parallel. The shared client
    # rate-limit lock keeps total throughput at 5 req/sec, but the pool
    # overlaps request prep + parsing for a meaningful speedup.
    out: dict = {"contact": contact}
    filters = {"filters[contact]": cid}
    bulk = client.fetch_many([
        ("fieldValues",        "fieldValues",        filters, 10000),
        ("contactTags",        "contactTags",        filters, 10000),
        ("contactLists",       "contactLists",       filters, 10000),
        ("contactAutomations", "contactAutomations", filters, 10000),
        ("deals",              "deals",              filters, 2000),
    ])
    for label, value in bulk.items():
        if isinstance(value, dict) and "error" in value:
            if label == "deals" and value.get("status_code") == 403:
                out["deals"] = "Deals feature not enabled"
            else:
                out[label] = value
        else:
            out[label] = value

    return out


_CONFIRM_NOTICE = """\
# Contact data export — confirmation required

This script will pull every record AC has about one contact (profile,
custom-field values, tags, list memberships, automation enrollments,
deals) and write it to a local JSON file or print it to stdout.

The output contains personal data about that contact. It is a local file
on your machine — never transmitted anywhere — but it should be treated
as any other customer-data export: store securely, share only with people
who need it for a legitimate reason, delete when no longer needed.

To proceed:

  python3 scripts/contact_data_export.py <email> --confirm

To save to a file:

  python3 scripts/contact_data_export.py <email> --confirm --output report.json
"""


def main():
    parser = argparse.ArgumentParser(
        description="Raw per-contact JSON dump across all sub-resources"
    )
    parser.add_argument("email")
    parser.add_argument("--confirm", action="store_true",
                        help="Required to actually export. Without it, prints a notice.")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if not args.confirm:
        print(_CONFIRM_NOTICE)
        sys.exit(0)

    client = ACClient()
    data = fetch(client, args.email)
    out = json.dumps(data, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
        emit_files(args.output)
    else:
        print(out)


if __name__ == "__main__":
    main()
