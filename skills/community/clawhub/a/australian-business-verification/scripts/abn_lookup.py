#!/usr/bin/env python3
"""
abn_lookup.py — query the Australian Business Register (ABR) JSON API.

The ABR JSON API is a free, official Australian Government service that returns
publicly available ABN registration data. It requires a free authentication GUID,
obtained by registering at https://abr.business.gov.au/Tools/WebServices and set as
the ABR_GUID environment variable. There is no usage cost.

Endpoints used (all GET, JSONP):
  https://abr.business.gov.au/json/AbnDetails.aspx?abn=...&guid=...&callback=callback
  https://abr.business.gov.au/json/AcnDetails.aspx?acn=...&guid=...&callback=callback
  https://abr.business.gov.au/json/MatchingNames.aspx?name=...&guid=...&maxResults=...&callback=callback

Usage:
  python3 abn_lookup.py --validate "51 824 753 556"     # local checksum only, no API call
  python3 abn_lookup.py --abn 51824753556               # full ABN lookup
  python3 abn_lookup.py --acn 102417032                 # full ACN lookup
  python3 abn_lookup.py --name "Acme Consulting" --max-results 10

Output is JSON on stdout. A successful ABN/ACN lookup includes a top-level
"summary" object (verdict, gstRegistered, canChargeGst) in addition to the raw
ABR fields (entityName, abnStatus, gst, businessName, etc.).

This script is read-only: it cannot register, update, or cancel an ABN. It does
not persist, cache, or log any data — each invocation makes a single request (or
none, for --validate) and prints the result.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://abr.business.gov.au/json/"
REQUEST_TIMEOUT_SECONDS = 15


def clean_number(value: str) -> str:
    """Strip everything except digits (handles '51 824 753 556' style input)."""
    return re.sub(r"\D", "", value or "")


def validate_abn(digits: str) -> bool:
    """ATO modulus-89 checksum for an 11-digit ABN."""
    if len(digits) != 11 or not digits.isdigit():
        return False
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    nums = [int(d) for d in digits]
    nums[0] -= 1
    total = sum(n * w for n, w in zip(nums, weights))
    return total % 89 == 0


def validate_acn(digits: str) -> bool:
    """ASIC modulus-10 checksum for a 9-digit ACN."""
    if len(digits) != 9 or not digits.isdigit():
        return False
    weights = [8, 7, 6, 5, 4, 3, 2, 1, 0]
    nums = [int(d) for d in digits]
    total = sum(n * w for n, w in zip(nums, weights))
    remainder = total % 10
    complement = (10 - remainder) % 10
    return complement == nums[8]


def strip_jsonp(text: str) -> dict:
    """The ABR JSON API wraps responses as callback({...}); unwrap to plain JSON."""
    text = text.strip()
    start = text.find("(")
    end = text.rfind(")")
    if start == -1 or end == -1:
        # Already plain JSON (shouldn't normally happen, but handle gracefully)
        return json.loads(text)
    inner = text[start + 1 : end]
    return json.loads(inner)


def call_abr(path: str, params: dict) -> dict:
    guid = os.environ.get("ABR_GUID")
    if not guid:
        return {
            "error": (
                "ABR_GUID environment variable is not set. Register for a free "
                "GUID at https://abr.business.gov.au/Tools/WebServices and set "
                "it as ABR_GUID before retrying."
            )
        }

    query = dict(params)
    query["guid"] = guid
    query["callback"] = "callback"
    url = BASE_URL + path + "?" + urllib.parse.urlencode(query)

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "abn-business-verification-skill/1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return {"error": f"ABR API returned HTTP {e.code}"}
    except urllib.error.URLError as e:
        return {"error": f"Could not reach the ABR API: {e.reason}"}
    except TimeoutError:
        return {"error": "Timed out contacting the ABR API"}

    try:
        return strip_jsonp(body)
    except json.JSONDecodeError:
        return {"error": "Could not parse the ABR API response", "raw_response": body[:500]}


def normalize_abn_response(raw: dict) -> dict:
    """Add a clean 'summary' block on top of the raw AbnDetails/AcnDetails fields."""
    if "error" in raw:
        return raw

    message = raw.get("Message") or ""
    abn_status = raw.get("AbnStatus") or ""
    gst_date = raw.get("Gst") or None

    if message:
        verdict = "not_found" if "no records found" in message.lower() else "error"
    elif abn_status.lower() == "active":
        verdict = "active"
    elif abn_status.lower() == "cancelled":
        verdict = "cancelled"
    else:
        verdict = "unknown"

    gst_registered = bool(gst_date)
    can_charge_gst = verdict == "active" and gst_registered

    result = {
        "summary": {
            "verdict": verdict,
            "gstRegistered": gst_registered,
            "canChargeGst": can_charge_gst,
        },
        "message": message,
        "abn": raw.get("Abn"),
        "acn": raw.get("Acn"),
        "entityName": raw.get("EntityName"),
        "entityTypeCode": raw.get("EntityTypeCode"),
        "entityTypeName": raw.get("EntityTypeName"),
        "abnStatus": abn_status,
        "gst": gst_date,
        "addressState": raw.get("AddressState"),
        "addressPostcode": raw.get("AddressPostcode"),
        "addressDate": raw.get("AddressDate"),
        "businessName": raw.get("BusinessName") or [],
    }
    return result


def normalize_name_response(raw: dict) -> dict:
    if "error" in raw:
        return raw

    message = raw.get("Message") or ""
    names = raw.get("Names") or []
    # Sort by relevance score, highest first
    try:
        names = sorted(names, key=lambda n: n.get("Score", 0), reverse=True)
    except (TypeError, AttributeError):
        pass

    if names:
        verdict = "ok"
    elif message:
        verdict = "not_found" if "no" in message.lower() else "error"
    else:
        verdict = "not_found"

    return {
        "summary": {
            "verdict": verdict,
            "resultCount": len(names),
        },
        "message": message,
        "names": [
            {
                "abn": n.get("Abn"),
                "abnStatus": n.get("AbnStatus"),
                "name": n.get("Name"),
                "nameType": n.get("NameType"),
                "isCurrent": n.get("IsCurrent"),
                "state": n.get("State"),
                "postcode": n.get("Postcode"),
                "score": n.get("Score"),
            }
            for n in names
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query the Australian Business Register (ABR) JSON API for ABN/ACN/name verification."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--abn", help="11-digit Australian Business Number to look up")
    group.add_argument("--acn", help="9-digit Australian Company Number (ASIC) to look up")
    group.add_argument("--name", help="Business or entity name to search for")
    group.add_argument(
        "--validate",
        metavar="NUMBER",
        help="Validate an ABN (11 digits) or ACN (9 digits) checksum locally — no API call",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Maximum results for a name search (default 10, ABR caps at 200)",
    )
    args = parser.parse_args()

    if args.validate:
        digits = clean_number(args.validate)
        if len(digits) == 11:
            output = {"input": args.validate, "normalized": digits, "type": "ABN", "valid_checksum": validate_abn(digits)}
        elif len(digits) == 9:
            output = {"input": args.validate, "normalized": digits, "type": "ACN", "valid_checksum": validate_acn(digits)}
        else:
            output = {
                "input": args.validate,
                "normalized": digits,
                "type": "unknown",
                "valid_checksum": False,
                "note": "Expected 11 digits for an ABN or 9 digits for an ACN.",
            }
        print(json.dumps(output, indent=2))
        return

    if args.abn:
        digits = clean_number(args.abn)
        if not validate_abn(digits):
            print(json.dumps({"error": "Invalid ABN checksum", "input": args.abn, "normalized": digits}, indent=2))
            return
        raw = call_abr("AbnDetails.aspx", {"abn": digits})
        print(json.dumps(normalize_abn_response(raw), indent=2))
        return

    if args.acn:
        digits = clean_number(args.acn)
        if not validate_acn(digits):
            print(json.dumps({"error": "Invalid ACN checksum", "input": args.acn, "normalized": digits}, indent=2))
            return
        raw = call_abr("AcnDetails.aspx", {"acn": digits})
        print(json.dumps(normalize_abn_response(raw), indent=2))
        return

    # Name search
    max_results = max(1, min(args.max_results, 200))
    raw = call_abr("MatchingNames.aspx", {"name": args.name, "maxResults": str(max_results)})
    print(json.dumps(normalize_name_response(raw), indent=2))


if __name__ == "__main__":
    main()
