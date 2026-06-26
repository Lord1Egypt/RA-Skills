#!/usr/bin/env python3
"""
free_vs_corporate_report.py — Free-mail vs. corporate domain split on the contact list.

Strategic context for B2B segmentation. Lists with mostly free-mail (Gmail,
Yahoo, etc.) skew consumer; corporate-heavy lists skew B2B.

Usage:
  python3 free_vs_corporate_report.py
  python3 free_vs_corporate_report.py --top-domains 25 --format json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

from _ac_client import ACClient

FREE_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com",
    "aol.com", "icloud.com", "me.com", "mac.com", "msn.com", "ymail.com",
    "googlemail.com", "protonmail.com", "proton.me", "gmx.com", "mail.com",
    "yandex.com", "yandex.ru", "zoho.com", "fastmail.com", "tutanota.com",
}


def analyze(contacts: Iterable[dict]) -> dict:
    free = 0
    corporate = 0
    invalid = 0
    total = 0
    domains = Counter()

    for c in contacts:
        total += 1
        email = (c.get("email") or "").strip().lower()
        if "@" not in email:
            invalid += 1
            continue
        domain = email.split("@", 1)[1]
        domains[domain] += 1
        if domain in FREE_DOMAINS:
            free += 1
        else:
            corporate += 1

    valid = free + corporate
    return {
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "free": free,
        "corporate": corporate,
        "free_pct": (free / valid * 100) if valid else 0,
        "corporate_pct": (corporate / valid * 100) if valid else 0,
        "top_free_domains": [
            (d, c) for d, c in domains.most_common(50) if d in FREE_DOMAINS
        ][:25],
        "top_corporate_domains": [
            (d, c) for d, c in domains.most_common(100) if d not in FREE_DOMAINS
        ][:25],
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Free vs. Corporate Domain Split",
        "",
        f"- Total contacts: {r['total']}",
        f"- Valid emails: {r['valid']} (invalid/missing: {r['invalid']})",
        f"- Free mail: **{r['free']}** ({r['free_pct']:.1f}%)",
        f"- Corporate: **{r['corporate']}** ({r['corporate_pct']:.1f}%)",
        "",
    ]
    if r["top_free_domains"]:
        lines.append("## Top free-mail domains")
        for d, c in r["top_free_domains"]:
            lines.append(f"- {d}: {c}")
        lines.append("")
    if r["top_corporate_domains"]:
        lines.append("## Top corporate domains")
        for d, c in r["top_corporate_domains"]:
            lines.append(f"- {d}: {c}")
        lines.append("")
    if r["free_pct"] > 70:
        lines.append("**Lean: consumer (>70% free mail).**")
    elif r["corporate_pct"] > 70:
        lines.append("**Lean: B2B (>70% corporate).**")
    else:
        lines.append("**Lean: mixed audience.**")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Free vs. corporate domain split")
    parser.add_argument("--max-contacts", type=int, default=10000)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    contacts = client.stream("contacts", "contacts", max_items=args.max_contacts)
    r = analyze(contacts)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
