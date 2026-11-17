#!/usr/bin/env python3
"""compliance_check.py - lint US B2B outreach drafts before a human sends them.

Checks each draft for the elements CAN-SPAM requires of commercial email, plus
the practical hygiene rules that keep a sending domain alive:

  - a real From address (and a business domain, not a freemail address)
  - a non-deceptive Subject line (no fake Re:/FW:/Fwd:)
  - a physical US postal address in the body
  - a working opt-out line (unsubscribe / opt out / remove me)
  - no prohibited claims (guaranteed results, risk-free, miracle)
  - a single clear call to action
  - a body short enough to read (soft check)

Usage:
    python3 compliance_check.py --drafts outreach/ --out compliance.json
    python3 compliance_check.py --drafts outreach/ --strict

A draft file is plain text with optional header lines:

    From: Jane at Acme <jane@acme.com>
    Subject: Quick question about your RevOps stack
    <blank line>
    body...

Stdlib only. No network calls. This lints drafts, it does not send them.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

FREEMAIL = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "icloud.com", "live.com", "msn.com", "proton.me", "protonmail.com",
}

DECEPTIVE_SUBJECT = re.compile(r"^\s*(re|fw|fwd|aw|tr)\s*[:\-]", re.IGNORECASE)
UNSUB_LINE = re.compile(
    r"(unsubscribe|opt[\s\-]?out|remove me|stop receiving|no more emails?|email preferences)",
    re.IGNORECASE,
)
POSTAL_ADDRESS = re.compile(
    r"\b\d{1,6}\s+[A-Za-z0-9.'\- ]{3,40}\b(?:street|st\.?|avenue|ave\.?|road|rd\.?|boulevard|blvd\.?|"
    r"drive|dr\.?|lane|ln\.?|court|ct\.?|way|suite|ste\.?|floor|plaza|parkway|pkwy\.?)\b",
    re.IGNORECASE,
)
CITY_STATE_ZIP = re.compile(r"\b[A-Z][A-Za-z .'-]{2,30},\s*(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\s+\d{5}(?:-\d{4})?\b")
PROHIBITED_CLAIMS = [
    (r"\bguarantee(d|s)?\b", "guaranteed claims need substantiation"),
    (r"\brisk[\- ]free\b", "risk-free claims are high risk for claims and trust"),
    (r"\bmiracle\b", "miracle claims are unsubstantiated"),
    (r"\b100%\s+(guaranteed|accurate|success)\b", "absolute accuracy claims"),
    (r"\bno\s+risk\b", "no-risk claims are high risk for claims and trust"),
    (r"\bact now\b", "false urgency is a spam signal"),
    (r"\blimited time\b", "false urgency is a spam signal"),
    (r"\bfree money\b", "misleading offer language"),
]
CTA_MARKERS = re.compile(
    r"(reply\b|let me know|worth\s+(a\s+)?\d+\s*[- ]?(minute|min|call)|book a call|"
    r"set up a call|curious if|open to|happy to send|can i send|question for you|"
    r"send (you|the) \w+|free 15)",
    re.IGNORECASE,
)


def parse_draft(path: str) -> dict:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    headers = {}
    body = raw
    lines = raw.splitlines()
    idx = 0
    while idx < len(lines) and lines[idx].strip():
        line = lines[idx].strip()
        idx += 1
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip().lower()
            if key in ("from", "to", "subject", "reply-to", "sent-from", "company", "physical-address", "address"):
                headers[key] = value.strip()
        if not headers and idx > 5:
            break
    if idx < len(lines):
        body = "\n".join(lines[idx:])
    return {"path": path, "headers": headers, "body": body.strip(), "raw": raw}


def check_draft(draft: dict) -> dict:
    headers = draft["headers"]
    body = draft["body"]
    errors, warnings = [], []

    subject = headers.get("subject", "")
    sender = headers.get("from", "")

    if not subject:
        errors.append({"rule": "subject", "message": "No Subject line found."})
    elif DECEPTIVE_SUBJECT.match(subject):
        errors.append({"rule": "subject", "message": f"Deceptive subject line: '{subject}'. Remove fake Re:/Fwd:/FW:."})
    elif len(subject) > 70:
        warnings.append({"rule": "subject", "message": f"Subject is {len(subject)} chars - US inboxes truncate near 60."})

    if not sender:
        errors.append({"rule": "from", "message": "No From address found."})
    else:
        match = re.search(r"[\w.+-]+@([\w.-]+\.[A-Za-z]{2,})", sender)
        if not match:
            errors.append({"rule": "from", "message": f"From value '{sender}' has no email address."})
        else:
            domain = match.group(1).lower()
            if domain in FREEMAIL:
                warnings.append(
                    {"rule": "from", "message": f"From domain '{domain}' is a freemail provider - deliverability and trust suffer."}
                )

    if not UNSUB_LINE.search(body):
        errors.append(
            {
                "rule": "unsubscribe",
                "message": "No opt-out line found. CAN-SPAM requires a clear and conspicuous unsubscribe mechanism.",
            }
        )

    if not POSTAL_ADDRESS.search(body) and not CITY_STATE_ZIP.search(body) and not headers.get("physical-address"):
        errors.append(
            {
                "rule": "postal_address",
                "message": "No physical postal address found. CAN-SPAM requires a valid physical address in commercial email.",
            }
        )

    for pattern, message in PROHIBITED_CLAIMS:
        found = re.search(pattern, body, re.IGNORECASE)
        if found:
            errors.append({"rule": "claims", "message": f"{message} (matched '{found.group(0)}')."})

    cta_hits = len(CTA_MARKERS.findall(body))
    if cta_hits == 0:
        warnings.append({"rule": "cta", "message": "No clear call to action found - one low-friction ask per message."})
    elif cta_hits > 3:
        warnings.append({"rule": "cta", "message": f"{cta_hits} calls to action in one message - keep it to one."})

    words = len(body.split())
    if words > 220:
        warnings.append({"rule": "length", "message": f"{words} words - US cold emails convert best under 150."})
    if words < 25:
        warnings.append({"rule": "length", "message": f"{words} words - too short to establish relevance."})

    if re.search(r"\b(hi|hey) (there|team|folks)\b", body, re.IGNORECASE):
        warnings.append({"rule": "tone", "message": "Generic greeting - personalize the first line."})

    return {
        "file": os.path.basename(draft["path"]),
        "path": draft["path"],
        "subject": subject,
        "from": sender,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "ready_for_human_review": not errors,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint US outreach drafts for CAN-SPAM and deliverability basics.")
    ap.add_argument("--drafts", required=True, help="File or directory of draft files")
    ap.add_argument("--out", help="Write JSON report here")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = ap.parse_args()

    if os.path.isdir(args.drafts):
        files = []
        for name in sorted(os.listdir(args.drafts)):
            if name.lower().endswith((".txt", ".md", ".eml")):
                files.append(os.path.join(args.drafts, name))
    elif os.path.isfile(args.drafts):
        files = [args.drafts]
    else:
        print(f"error: not found: {args.drafts}", file=sys.stderr)
        return 2

    if not files:
        print("error: no draft files found.", file=sys.stderr)
        return 2

    results = [check_draft(parse_draft(path)) for path in files]
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = len(results) - passed
    warnings = sum(len(r["warnings"]) for r in results)

    report = {
        "checked": len(results),
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "standard": "CAN-SPAM (15 U.S.C. 7704) baseline + deliverability hygiene",
        "note": "Lint only. A human still reviews and sends every message.",
        "results": results,
    }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        print(f"written: {args.out}")

    print(f"drafts checked : {len(results)}")
    print(f"passed         : {passed}")
    print(f"failed         : {failed}")
    print(f"warnings       : {warnings}\n")
    for r in results:
        print(f"[{r['status']}] {r['file']}")
        for e in r["errors"]:
            print(f"    ERROR  {e['rule']}: {e['message']}")
        for w in r["warnings"]:
            print(f"    WARN   {w['rule']}: {w['message']}")

    if failed:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
