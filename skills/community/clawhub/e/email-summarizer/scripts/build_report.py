#!/usr/bin/env python3
"""
build_report.py — Analyse email JSON and generate HTML + Excel contact report.

Reads the JSON produced by fetch_imap.py or parse_file.py, builds a contact
profile, and writes <output>.html + <output>.xlsx.

This script does NOT send anything. Use send_report.py for delivery.

Usage:
  # From a file
  python3 build_report.py --input emails.json --output report

  # Piped from fetch_imap.py
  python3 fetch_imap.py --days 30 | python3 build_report.py --output report

  # Specify owner explicitly (e.g. when analysing someone else's PST)
  python3 build_report.py --input emails.json --output report --owner alice@example.com

Output:
  report.html   — self-contained HTML report (open in any browser or email client)
  report.xlsx   — Excel spreadsheet with the same data
"""

import argparse, json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _analyze import infer_owner, build_contacts
from _render  import build_report_html, build_excel


def main():
    parser = argparse.ArgumentParser(
        description="Build HTML + Excel contact profile report from email JSON.")
    parser.add_argument("--input",  default=None,
                        help="Path to emails JSON file. Reads from stdin if omitted.")
    parser.add_argument("--output", default="contact_report",
                        help="Output path prefix (default: contact_report). "
                             "Writes <prefix>.html and <prefix>.xlsx")
    parser.add_argument("--owner",  default="",
                        help="Mailbox owner address. Auto-inferred from data if omitted.")
    args = parser.parse_args()

    # ── Load ──────────────────────────────────────────────────────────────────
    if args.input:
        print(f"[build] Loading {args.input}", file=sys.stderr)
        with open(args.input, "r", encoding="utf-8") as f:
            raw = json.load(f)
    else:
        print("[build] Reading from stdin…", file=sys.stderr)
        raw = json.load(sys.stdin)

    if isinstance(raw, dict) and "emails" in raw:
        emails     = raw["emails"]
        date_range = f'{raw.get("since", "all")} – {raw.get("until", "now")}'
        data_owner = raw.get("owner", "")
    else:
        emails     = raw
        date_range = "all"
        data_owner = ""

    print(f"[build] {len(emails)} emails loaded", file=sys.stderr)

    # ── Owner ─────────────────────────────────────────────────────────────────
    owner = args.owner.strip().lower()
    if not owner:
        owner = data_owner.lower() if data_owner else infer_owner(emails)
        if owner:
            print(f"[build] Owner: {owner}", file=sys.stderr)
        else:
            print("[build] Warning: could not determine owner. "
                  "Use --owner to specify explicitly.", file=sys.stderr)

    report_label = owner or args.input or "stdin"

    # ── Analyse ───────────────────────────────────────────────────────────────
    contacts = build_contacts(emails, owner)
    now_str  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[build] {len(contacts)} contacts found", file=sys.stderr)

    # ── Write HTML ────────────────────────────────────────────────────────────
    html_path = args.output.rstrip("/") + ".html"
    html      = build_report_html(contacts, report_label, date_range, now_str, len(emails))
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[build] HTML  → {html_path}", file=sys.stderr)

    # ── Write Excel ───────────────────────────────────────────────────────────
    xlsx_tmp  = build_excel(contacts, report_label, date_range, now_str)
    xlsx_path = args.output.rstrip("/") + ".xlsx"
    os.replace(xlsx_tmp, xlsx_path)
    print(f"[build] Excel → {xlsx_path}", file=sys.stderr)

    print(f"[build] Done — {len(contacts)} contacts, {len(emails)} emails, label: {report_label}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
