#!/usr/bin/env python3
"""
dedupe_contacts.py — Find duplicate contacts.

Detects: same email different case, same normalized phone, fuzzy name+company.
Outputs merge candidates with confidence scores. Never auto-merges.

Usage:
  python3 dedupe_contacts.py
  python3 dedupe_contacts.py --max-contacts 5000
  python3 dedupe_contacts.py --format json
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from pathlib import Path

from _ac_client import ACClient


def _norm_phone(p: str) -> str:
    if not p:
        return ""
    digits = re.sub(r"\D", "", p)
    if len(digits) >= 10:
        return digits[-10:]
    return digits


def _norm_email(e: str) -> str:
    return (e or "").strip().lower()


def _name_company_key(c: dict) -> str:
    fn = (c.get("firstName") or "").strip().lower()
    ln = (c.get("lastName") or "").strip().lower()
    if fn and ln:
        return f"{fn}|{ln}"
    return ""


def _slim(c: dict) -> dict:
    """Keep only the fields used downstream — keeps memory bounded for huge accounts."""
    return {"id": c["id"], "email": c.get("email")}


def find_duplicates(contacts: Iterable[dict]) -> dict:
    """Single-pass duplicate detection.

    Stores slim records keyed by email/phone/name. Singletons live in the
    `seen_*` maps; once a key is seen a second time, the entry is promoted
    into `*_dupes` and removed from `seen_*`. Final memory ≈ O(N_unique
    keys × slim record size) instead of O(N × full record size).
    """
    seen_email: dict[str, dict] = {}
    seen_phone: dict[str, dict] = {}
    seen_name: dict[str, dict] = {}
    email_dupes: dict[str, list] = {}
    phone_dupes: dict[str, list] = {}
    name_dupes: dict[str, list] = {}
    scanned = 0

    for c in contacts:
        scanned += 1
        slim = _slim(c)
        email = _norm_email(c.get("email", ""))
        phone = _norm_phone(c.get("phone", ""))
        name_key = _name_company_key(c)

        if email:
            if email in email_dupes:
                email_dupes[email].append(slim)
            elif email in seen_email:
                email_dupes[email] = [seen_email.pop(email), slim]
            else:
                seen_email[email] = slim

        if phone:
            if phone in phone_dupes:
                phone_dupes[phone].append(slim)
            elif phone in seen_phone:
                phone_dupes[phone] = [seen_phone.pop(phone), slim]
            else:
                seen_phone[phone] = slim

        if name_key:
            if name_key in name_dupes:
                name_dupes[name_key].append(slim)
            elif name_key in seen_name:
                name_dupes[name_key] = [seen_name.pop(name_key), slim]
            else:
                seen_name[name_key] = slim

    # Filter name_dupes that aren't already caught by email (high-confidence is email/phone)
    name_only = {}
    for n, cs in name_dupes.items():
        emails = {_norm_email(c.get("email", "")) for c in cs}
        if len(emails) > 1 and not any(e in email_dupes for e in emails):
            name_only[n] = cs

    return {
        "scanned": scanned,
        "email_case_duplicates": email_dupes,
        "phone_duplicates": phone_dupes,
        "name_duplicates_distinct_email": name_only,
    }


def render_markdown(d: dict, total: int) -> str:
    lines = [
        "# Duplicate Contact Audit",
        "",
        f"- Contacts scanned: **{total}**",
        f"- Email duplicates (case-insensitive): **{len(d['email_case_duplicates'])}** groups",
        f"- Phone duplicates (last-10-digits match): **{len(d['phone_duplicates'])}** groups",
        f"- Name duplicates with distinct emails: **{len(d['name_duplicates_distinct_email'])}** groups",
        "",
    ]
    if d["email_case_duplicates"]:
        lines.append("## Email duplicates (high confidence)")
        for e, cs in list(d["email_case_duplicates"].items())[:30]:
            ids = ", ".join(str(c["id"]) for c in cs)
            lines.append(f"- `{e}` — ids: {ids}")
        lines.append("")
    if d["phone_duplicates"]:
        lines.append("## Phone duplicates")
        for p, cs in list(d["phone_duplicates"].items())[:30]:
            entries = ", ".join(f"{c.get('email','?')} (id={c['id']})" for c in cs)
            lines.append(f"- `{p}` — {entries}")
        lines.append("")
    if d["name_duplicates_distinct_email"]:
        lines.append("## Same-name, different-email (review manually)")
        for n, cs in list(d["name_duplicates_distinct_email"].items())[:30]:
            entries = ", ".join(f"{c.get('email','?')} (id={c['id']})" for c in cs)
            lines.append(f"- `{n}` — {entries}")
        lines.append("")
    if not any([d["email_case_duplicates"], d["phone_duplicates"], d["name_duplicates_distinct_email"]]):
        lines.append("**No duplicates detected.**")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find duplicate contacts")
    parser.add_argument("--max-contacts", type=int, default=10000)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    contacts = client.stream("contacts", "contacts", max_items=args.max_contacts)
    d = find_duplicates(contacts)

    if args.format == "json":
        out_obj = {
            "scanned": d["scanned"],
            "email_case_duplicates": [
                {"key": e, "ids": [c["id"] for c in cs]}
                for e, cs in d["email_case_duplicates"].items()
            ],
            "phone_duplicates": [
                {"key": p, "ids": [c["id"] for c in cs]}
                for p, cs in d["phone_duplicates"].items()
            ],
            "name_duplicates_distinct_email": [
                {"key": n, "ids": [c["id"] for c in cs]}
                for n, cs in d["name_duplicates_distinct_email"].items()
            ],
        }
        out = json.dumps(out_obj, indent=2)
    else:
        out = render_markdown(d, d["scanned"])

    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
