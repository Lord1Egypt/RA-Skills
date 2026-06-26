#!/usr/bin/env python3
"""Parse a founder's natural-language SAFE request into APOA-flat constraints.

Reads the message on stdin, writes JSON to stdout matching the schema in
SKILL.md Step 1. Null values mean the user should clarify before authorizing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def _money_to_dollars(text: str) -> int:
    raw = text.strip().replace("$", "").replace(",", "")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([kmb])?", raw, re.IGNORECASE)
    if not m:
        raise ValueError(f"Could not parse money value: {text!r}")
    n = float(m.group(1))
    suffix = (m.group(2) or "").lower()
    if suffix == "k":
        n *= 1_000
    elif suffix == "m":
        n *= 1_000_000
    elif suffix == "b":
        n *= 1_000_000_000
    return int(n)


def _normalize_constraints(parsed: dict[str, Any]) -> dict[str, Any]:
    # Normalize parser output before the authorization review card.
    if not parsed.get("role"):
        parsed["role"] = "founder"
    parsed["role"] = str(parsed["role"]).lower()
    if parsed["role"] not in ("founder", "investor"):
        parsed["role"] = "founder"

    if not parsed.get("mode"):
        parsed["mode"] = "demo"
    parsed["mode"] = str(parsed["mode"]).lower()
    if parsed["mode"] not in ("demo", "two_party"):
        parsed["mode"] = "demo"

    code = parsed.get("session_code")
    if code:
        code = str(code).strip().upper()
        parsed["session_code"] = code if code else None
    else:
        parsed["session_code"] = None
    if parsed["session_code"]:
        parsed["mode"] = "two_party"
    if parsed.get("discount_max") is None and parsed.get("discount_min") is not None:
        parsed["discount_max"] = parsed["discount_min"]

    for field in (
        "company_name", "founder_name", "founder_title",
        "investor_name", "investor_firm", "investment_amount",
        "investment_amount_min", "investment_amount_max",
    ):
        parsed.setdefault(field, None)
    if parsed.get("investment_amount") is None and parsed.get("investment_amount_min") is not None:
        parsed["investment_amount"] = parsed["investment_amount_min"]
    return parsed


def _extract_constraints_deterministic(message: str) -> dict[str, Any]:
    """Parse the constrained demo copy without any external LLM dependency."""
    text = " ".join(message.strip().split())
    lower = text.lower()
    code_m = re.search(r"\bINV-[A-Z0-9]{5,}\b", text, re.IGNORECASE)
    role = "investor" if code_m or re.search(r"\b(joining|join)\b", lower) else "founder"
    mode = "two_party" if code_m or "live negotiation" in lower or "real negotiation" in lower else "demo"

    founder_bot = None
    bot_m = re.search(r"\bvia\s+(@[A-Za-z0-9_]+)", text)
    if bot_m:
        founder_bot = bot_m.group(1)

    valuation_min = None
    valuation_max = None
    range_m = re.search(
        r"\bcap\b[^$]*(\$?\d+(?:\.\d+)?\s*[kmb]?)\s*(?:-|–|to|through)\s*(\$?\d+(?:\.\d+)?\s*[kmb]?)",
        text,
        re.IGNORECASE,
    )
    up_to_m = re.search(r"\bcap\s+up\s+to\s+(\$?\d+(?:\.\d+)?\s*[kmb]?)", text, re.IGNORECASE)
    single_m = re.search(r"\bcap\b[^$]*(\$?\d+(?:\.\d+)?\s*[kmb]?)", text, re.IGNORECASE)
    if range_m:
        valuation_min = _money_to_dollars(range_m.group(1))
        valuation_max = _money_to_dollars(range_m.group(2))
    elif up_to_m:
        valuation_min = 0
        valuation_max = _money_to_dollars(up_to_m.group(1))
    elif single_m:
        cap = _money_to_dollars(single_m.group(1))
        valuation_min = cap
        valuation_max = cap

    discount_min = None
    discount_max = None
    disc_range_m = re.search(
        r"(?:discount[^0-9]*)?(\d+(?:\.\d+)?)\s*%\s*(?:-|–|to|through)\s*(\d+(?:\.\d+)?)\s*%\s*(?:discount)?",
        text,
        re.IGNORECASE,
    )
    disc_floor_m = re.search(
        r"(?:at\s+least|minimum|floor|no\s+less\s+than)[^0-9]*(\d+(?:\.\d+)?)\s*%\s*(?:discount)?|(\d+(?:\.\d+)?)\s*%\s+discount\s+(?:minimum|floor)",
        text,
        re.IGNORECASE,
    )
    disc_ceiling_m = re.search(
        r"(?:up\s+to|maximum|no\s+more\s+than)[^0-9]*(\d+(?:\.\d+)?)\s*%\s*(?:discount)?",
        text,
        re.IGNORECASE,
    )
    disc_single_m = re.search(r"(\d+(?:\.\d+)?)\s*%\s+discount", text, re.IGNORECASE)
    if not disc_single_m:
        disc_single_m = re.search(r"discount[^0-9]*(\d+(?:\.\d+)?)\s*%", text, re.IGNORECASE)
    if disc_range_m:
        discount_min = float(disc_range_m.group(1)) / 100
        discount_max = float(disc_range_m.group(2)) / 100
    elif disc_floor_m:
        discount_min = float(disc_floor_m.group(1) or disc_floor_m.group(2)) / 100
        discount_max = 1.0
    elif disc_ceiling_m:
        discount_min = 0.0
        discount_max = float(disc_ceiling_m.group(1)) / 100
    elif disc_single_m:
        discount_min = float(disc_single_m.group(1)) / 100
        discount_max = discount_min

    pro_rata = "required" if re.search(r"pro[- ]?rata[^.,;]*(required|must|included)|pro[- ]?rata required", lower) else "preferred"
    mfn = "required" if re.search(r"\bmfn\b[^.,;]*(required|must)", lower) else "indifferent"

    amount = None
    amount_min = None
    amount_max = None
    check_range_m = re.search(
        r"\b(?:check(?:\s+size)?|investment|invest)\b[^$]*(\$?\d+(?:\.\d+)?\s*[kmb]?)\s*(?:-|–|to|through)\s*(\$?\d+(?:\.\d+)?\s*[kmb]?)",
        text,
        re.IGNORECASE,
    )
    check_single_m = re.search(
        r"\b(?:check(?:\s+size)?|investment|invest)\b[^$]*(\$?\d+(?:\.\d+)?\s*[kmb]?)|(\$?\d+(?:\.\d+)?\s*[kmb]?)\s+check\b",
        text,
        re.IGNORECASE,
    )
    if check_range_m:
        amount_min = float(_money_to_dollars(check_range_m.group(1)))
        amount_max = float(_money_to_dollars(check_range_m.group(2)))
        amount = amount_min
    elif check_single_m:
        amount = float(_money_to_dollars(check_single_m.group(1) or check_single_m.group(2)))

    investor_name = investor_firm = None
    if role == "founder":
        im = re.search(r"\bwith\s+(.+?)\s+at\s+(.+?)(?=\.|,|\s+cap\b|$)", text, re.IGNORECASE)
        paren_im = re.search(r"\bwith\s+(.+?)\s*\((.+?)\)", text, re.IGNORECASE)
        if im:
            investor_name = im.group(1).strip()
            investor_firm = im.group(2).strip()
        elif paren_im:
            investor_name = paren_im.group(1).strip()
            investor_firm = paren_im.group(2).strip()
    else:
        im = re.search(r"\bI\s*(?:am|'m)\s+(.+?)\s+(?:at|from)\s+(.+?)(?=,\s*cap\b|\.|$)", text, re.IGNORECASE)
        if im:
            investor_name = im.group(1).strip(" ,")
            investor_firm = im.group(2).strip(" ,")

    return _normalize_constraints({
        "role": role,
        "mode": mode,
        "session_code": code_m.group(0).upper() if code_m else None,
        "founder_bot_handle": founder_bot,
        "valuation_cap_min": valuation_min,
        "valuation_cap_max": valuation_max,
        "discount_min": discount_min,
        "discount_max": discount_max,
        "pro_rata": pro_rata,
        "mfn": mfn,
        "company_name": None,
        "founder_name": None,
        "founder_title": None,
        "investor_name": investor_name,
        "investor_firm": investor_firm,
        "investment_amount": amount,
        "investment_amount_min": amount_min,
        "investment_amount_max": amount_max,
    })


def extract_constraints(message: str) -> dict[str, Any]:
    return _extract_constraints_deterministic(message)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Parse NL SAFE terms into APOA constraints")
    parser.add_argument("--message", default="", help="The negotiation request text")
    parser.add_argument("--message-file", default="", help="Path to a file containing the request text")
    parser.add_argument("--output-file", default="", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    if args.message:
        message = args.message
    elif args.message_file:
        message = Path(args.message_file).read_text().strip()
    else:
        message = sys.stdin.read().strip()

    if not message:
        sys.stderr.write("No message provided. Use --message, --message-file, or pipe to stdin.\n")
        return 2

    try:
        constraints = extract_constraints(message)
    except (ValueError, RuntimeError) as e:
        sys.stderr.write(f"{e}\n")
        return 1

    output = json.dumps(constraints, indent=2) + "\n"
    if args.output_file:
        Path(args.output_file).write_text(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
