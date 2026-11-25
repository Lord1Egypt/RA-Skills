#!/usr/bin/env python3
"""Validate an email draft without creating or sending a message."""

from __future__ import annotations

import argparse
from email.utils import getaddresses
import json
import os
import re
import sys

DEFAULT_ALLOWLIST = "you@example.com"
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
INJECTION_RE = re.compile(
    r"(?:ignore (?:all |the )?(?:previous|prior) instructions|system prompt|developer message|reveal .*token)",
    re.IGNORECASE,
)


def parse_addresses(raw: str) -> list[str]:
    addresses = [address.strip().lower() for _, address in getaddresses([raw]) if address.strip()]
    if not addresses or any(not EMAIL_RE.fullmatch(address) for address in addresses):
        raise ValueError("Every recipient must be a valid explicit email address.")
    return addresses


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--to", required=True, help="Comma-separated To recipients")
    parser.add_argument("--cc", default="", help="Comma-separated Cc recipients")
    parser.add_argument("--bcc", default="", help="Comma-separated Bcc recipients")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    body = sys.stdin.read()
    allowlist_raw = os.environ.get("BLUEBIRD_EMAIL_ALLOWLIST", DEFAULT_ALLOWLIST)
    allowlist = {address.strip().lower() for address in allowlist_raw.split(",") if address.strip()}
    result: dict[str, object] = {"ok": False, "status": "rejected", "sent": False, "warnings": []}

    try:
        if not allowlist or any(not EMAIL_RE.fullmatch(address) for address in allowlist):
            raise ValueError("The deployment recipient allowlist is missing or invalid.")
        recipients = parse_addresses(",".join(value for value in (args.to, args.cc, args.bcc) if value))
        blocked = sorted(set(recipients) - allowlist)
        if blocked:
            raise ValueError(f"Recipient is not allowlisted: {', '.join(blocked)}")
        subject = args.subject.strip()
        if not subject or len(subject) > 200:
            raise ValueError("Subject must contain 1 to 200 characters.")
        if not body.strip() or len(body) > 8000:
            raise ValueError("Body must contain 1 to 8,000 characters.")
        if INJECTION_RE.search(body):
            result["warnings"] = ["Draft contains instruction-like text; verify it is quoted as untrusted content."]
        result.update({
            "ok": True,
            "status": "draft_ready_for_human_review",
            "recipients": recipients,
            "subject": subject,
            "bodyCharacters": len(body),
        })
    except ValueError as exc:
        result["error"] = str(exc)

    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(result["status"])
        if "error" in result:
            print(result["error"], file=sys.stderr)
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
