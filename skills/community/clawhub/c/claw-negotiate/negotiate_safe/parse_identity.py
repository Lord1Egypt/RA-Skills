#!/usr/bin/env python3
"""Parse a user's short self-introduction into structured identity fields.

Used by the `run_safe.py setup` subcommand to populate the installed user's
identity (FOUNDER_NAME, FOUNDER_TITLE, COMPANY_NAME, INVESTOR_NAME,
INVESTOR_FIRM, ROLE) once, so they don't have to repeat it in every
negotiation request.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any


def _normalize_identity(parsed: dict[str, Any]) -> dict[str, Any]:
    if not parsed.get("role"):
        parsed["role"] = "founder"
    parsed["role"] = str(parsed["role"]).lower()
    if parsed["role"] not in ("founder", "investor"):
        parsed["role"] = "founder"

    for field in ("name", "title", "company", "firm"):
        parsed.setdefault(field, None)

    return parsed


def _extract_identity_deterministic(message: str) -> dict[str, Any]:
    """Parse the common profile setup copy without an external LLM."""
    text = " ".join(message.strip().split())
    lower = text.lower()

    is_investor = bool(re.search(
        r"\b(partner|investor|managing director|principal|associate)\b|\b(?:at|from)\s+[^,.]*(fund|capital|ventures|vc)\b",
        lower,
    ))

    name = title = company = firm = None

    founder_m = re.search(
        r"(?:i\s*(?:am|'m)\s+)?(?P<name>.+?),\s*(?P<title>ceo|cto|cfo|cofounder|co-founder|founder|president)\s+(?:of|at)\s+(?P<company>.+)$",
        text,
        re.IGNORECASE,
    )
    investor_m = re.search(
        r"(?:i\s*(?:am|'m)\s+)?(?P<name>.+?),\s*(?P<title>partner|managing director|principal|associate|investor)\s+(?:at|from)\s+(?P<firm>.+)$",
        text,
        re.IGNORECASE,
    )
    simple_investor_m = re.search(
        r"(?:i\s*(?:am|'m)\s+)?(?P<name>.+?)\s+(?:at|from)\s+(?P<firm>.+)$",
        text,
        re.IGNORECASE,
    )

    if investor_m:
        is_investor = True
        name = investor_m.group("name").strip(" ,")
        title = investor_m.group("title").strip()
        firm = investor_m.group("firm").strip(" .")
    elif founder_m:
        is_investor = False
        name = founder_m.group("name").strip(" ,")
        title = founder_m.group("title").strip()
        company = founder_m.group("company").strip(" .")
    elif simple_investor_m and is_investor:
        name = simple_investor_m.group("name").strip(" ,")
        firm = simple_investor_m.group("firm").strip(" .")

    return _normalize_identity({
        "role": "investor" if is_investor else "founder",
        "name": name,
        "title": title,
        "company": company,
        "firm": firm,
    })


def extract_identity(message: str) -> dict[str, Any]:
    return _extract_identity_deterministic(message)


def main() -> int:
    message = sys.stdin.read().strip()
    if not message:
        sys.stderr.write("Provide identity text on stdin.\n")
        return 2
    try:
        identity = extract_identity(message)
    except (ValueError, RuntimeError) as e:
        sys.stderr.write(f"Parse error: {e}\n")
        return 1
    sys.stdout.write(json.dumps(identity, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
