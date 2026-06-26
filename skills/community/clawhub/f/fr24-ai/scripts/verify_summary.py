#!/usr/bin/env python3
"""校验 Skill 搜索摘要：直飞/中转各一条，含退改、行李、航班号。"""
from __future__ import annotations

import argparse
import json
import secrets
import sys
import urllib.error
import urllib.request
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import CLIENT_KEY_HEADER, EXPORT_BASE_URL, GRAY_HEADER, SHOPPING_PATH  # noqa: E402


def validate_summary(raw: dict) -> list[str]:
    errors: list[str] = []
    code = str(raw.get("code", ""))
    if code not in ("0", "000000"):
        errors.append(f"unexpected code: {code}")
        return errors

    summary = raw.get("summary")
    if not summary:
        errors.append("missing summary")
        return errors

    direct_count = summary.get("directCount") or 0
    transfer_count = summary.get("transferCount") or 0
    required = []
    if direct_count > 0:
        required.append(("directLowest", "直飞"))
    if transfer_count > 0:
        required.append(("transferLowest", "中转"))
    if not required:
        errors.append("no direct/transfer offers in summary counts")
        return errors

    for key, _label in required:
        offer = summary.get(key)
        if not offer:
            errors.append(f"missing {key} (count>0)")
            continue
        if not offer.get("flights"):
            errors.append(f"{key}: missing flights")
        if not offer.get("refundChange"):
            errors.append(f"{key}: missing refundChange")
        elif not offer["refundChange"].get("refundText") or not offer["refundChange"].get("changeText"):
            errors.append(f"{key}: incomplete refundChange")
        if not offer.get("baggage"):
            errors.append(f"{key}: missing baggage")
        segs = offer.get("segments") or []
        if not segs or not all(s.get("flightNo") for s in segs):
            errors.append(f"{key}: segments/flightNo incomplete")

    offers = (raw.get("data") or {}).get("offers") or []
    if len(offers) > 2:
        errors.append(f"data.offers not trimmed: {len(offers)}")
    ids = set()
    for k in ("directLowest", "transferLowest"):
        o = summary.get(k)
        if o and o.get("offerId"):
            ids.add(o["offerId"])
    offer_ids = {o.get("offerId") for o in offers}
    if ids and offer_ids and ids != offer_ids:
        errors.append(f"offer ids mismatch: summary={ids} data={offer_ids}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload-file", required=True)
    parser.add_argument("--client-key", help="optional; generates new key if omitted")
    args = parser.parse_args()

    payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    client_key = args.client_key or secrets.token_urlsafe(32)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        CLIENT_KEY_HEADER: client_key,
    }
    if GRAY_HEADER:
        headers["gray"] = GRAY_HEADER

    req = urllib.request.Request(
        EXPORT_BASE_URL + SHOPPING_PATH,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if not body.strip():
            out = {
                "code": str(e.code),
                "ok": False,
                "errors": [f"HTTP {e.code} {e.reason}，请检查 config.py 中 EXPORT_BASE_URL 与 GRAY_HEADER"],
                "message": e.reason,
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        raw = json.loads(body)

    errors = validate_summary(raw)
    out = {
        "code": raw.get("code"),
        "traceId": raw.get("traceId"),
        "summaryStats": {
            "totalOffers": (raw.get("summary") or {}).get("totalOffers"),
            "directCount": (raw.get("summary") or {}).get("directCount"),
            "transferCount": (raw.get("summary") or {}).get("transferCount"),
            "offersInData": len((raw.get("data") or {}).get("offers") or []),
        },
        "remainingQuota": (raw.get("skillMeta") or {}).get("remainingQuota"),
        "errors": errors,
        "ok": len(errors) == 0,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
