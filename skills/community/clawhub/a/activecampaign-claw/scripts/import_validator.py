#!/usr/bin/env python3
"""
import_validator.py — Pre-import sanity check for a contact CSV.

Catches problems before they hit AC: malformed emails, role addresses,
free-mail vs. corporate split, duplicates within the file, missing required
columns. Local-only — does not call the AC API.

Usage:
  python3 import_validator.py contacts.csv
  python3 import_validator.py contacts.csv --email-column Email
  python3 import_validator.py contacts.csv --format json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
ROLE_LOCAL_PARTS = {
    "info", "support", "sales", "admin", "noreply", "no-reply", "contact",
    "hello", "team", "office", "help", "service", "marketing",
    "abuse", "postmaster", "webmaster", "hr", "jobs", "press", "media",
}
FREE_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com",
    "aol.com", "icloud.com", "me.com", "mac.com", "msn.com", "ymail.com",
    "googlemail.com", "protonmail.com", "proton.me", "gmx.com", "mail.com",
}


def _detect_email_column(headers: list[str]) -> str | None:
    candidates = [h for h in headers if h and h.lower().strip() in {"email", "email address", "e-mail"}]
    if candidates:
        return candidates[0]
    for h in headers:
        if h and "email" in h.lower():
            return h
    return None


def analyze(csv_path: Path, email_column: str | None) -> dict:
    rows = []
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        col = email_column or _detect_email_column(headers)
        if not col:
            raise SystemExit(f"ERROR: Could not detect email column in {csv_path}. Headers: {headers}")
        for row in reader:
            rows.append(row)

    total = len(rows)
    seen = Counter()
    malformed = []
    role_addresses = []
    domain_counts = Counter()
    free_count = 0
    corporate_count = 0
    blank_count = 0

    for i, row in enumerate(rows, start=2):  # +2 = 1 for header, 1 for 1-indexed
        raw = (row.get(col) or "").strip()
        if not raw:
            blank_count += 1
            continue
        normalized = raw.lower()
        seen[normalized] += 1
        if not EMAIL_RE.match(raw):
            malformed.append({"line": i, "value": raw})
            continue
        local, _, domain = normalized.partition("@")
        if local in ROLE_LOCAL_PARTS:
            role_addresses.append({"line": i, "value": raw})
        domain_counts[domain] += 1
        if domain in FREE_DOMAINS:
            free_count += 1
        else:
            corporate_count += 1

    duplicates = {email: cnt for email, cnt in seen.items() if cnt > 1}

    valid = total - blank_count - len(malformed)
    return {
        "file": str(csv_path),
        "email_column": col,
        "total_rows": total,
        "valid_rows": valid,
        "blank_emails": blank_count,
        "malformed_count": len(malformed),
        "malformed_sample": malformed[:10],
        "duplicate_count": len(duplicates),
        "duplicate_sample": dict(list(duplicates.items())[:10]),
        "role_address_count": len(role_addresses),
        "role_address_sample": role_addresses[:10],
        "free_mail_count": free_count,
        "corporate_count": corporate_count,
        "free_pct": (free_count / valid * 100) if valid else 0,
        "top_domains": domain_counts.most_common(10),
    }


def render_markdown(report: dict) -> str:
    r = report
    lines = [
        f"# Import Validation: {r['file']}",
        "",
        f"- Total rows: **{r['total_rows']}**",
        f"- Valid emails: **{r['valid_rows']}**",
        f"- Blank emails: {r['blank_emails']}",
        f"- Malformed: {r['malformed_count']}",
        f"- Duplicates within file: {r['duplicate_count']}",
        f"- Role addresses (info@, support@, etc.): {r['role_address_count']}",
        f"- Free mail vs. corporate: {r['free_mail_count']} free / {r['corporate_count']} corporate ({r['free_pct']:.1f}% free)",
        "",
    ]
    if r["malformed_sample"]:
        lines.append("## Malformed (first 10)")
        for m in r["malformed_sample"]:
            lines.append(f"- line {m['line']}: `{m['value']}`")
        lines.append("")
    if r["duplicate_sample"]:
        lines.append("## Duplicates (first 10)")
        for email, cnt in r["duplicate_sample"].items():
            lines.append(f"- `{email}` × {cnt}")
        lines.append("")
    if r["role_address_sample"]:
        lines.append("## Role addresses (first 10)")
        for ra in r["role_address_sample"]:
            lines.append(f"- line {ra['line']}: `{ra['value']}`")
        lines.append("")
    if r["top_domains"]:
        lines.append("## Top domains")
        for d, n in r["top_domains"]:
            lines.append(f"- {d}: {n}")
        lines.append("")
    if r["malformed_count"] == 0 and r["duplicate_count"] == 0 and r["role_address_count"] == 0:
        lines.append("**Verdict: clean — safe to import.**")
    else:
        lines.append("**Verdict: clean up flagged rows before importing.**")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate a contact CSV before AC import")
    parser.add_argument("csv_path", help="Path to CSV file")
    parser.add_argument("--email-column", default=None, help="Email column name (auto-detected if omitted)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    p = Path(args.csv_path)
    if not p.exists():
        raise SystemExit(f"ERROR: file not found: {p}")

    report = analyze(p, args.email_column)
    if args.format == "json":
        out = json.dumps(report, indent=2)
    else:
        out = render_markdown(report)

    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
