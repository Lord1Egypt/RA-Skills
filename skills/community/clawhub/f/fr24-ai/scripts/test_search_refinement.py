#!/usr/bin/env python3
"""搜索细化与汇总过滤的自检（维护者本地运行）。"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent


def _run(cmd: list[str]) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout or f"exit {proc.returncode}")
    return json.loads(proc.stdout)


def main() -> int:
    errors: list[str] = []

    sys.path.insert(0, str(_SCRIPTS))
    from fare_summarizer import _summarize_from_data  # noqa: E402
    from search_refinement import apply_refinement, parse_carriers_from_text  # noqa: E402

    if parse_carriers_from_text("要CA") != ["CA"]:
        errors.append("parse_carriers_from_text CA")

    base = {
        "searchLegs": [{"origin": "SZX", "destination": "BKK", "depDate": "2026-06-01"}],
        "adultNum": 1,
        "childNum": 0,
        "infantNum": 0,
        "preferences": {"cabin": "Y", "stops": 2},
    }
    p, note, err = apply_refinement(base, "国航 12点")
    if err or "CA" not in (p.get("preferences") or {}).get("preferredCarrier", []):
        errors.append(f"apply_refinement: {err} {note}")

    data = {
        "offers": [
            {
                "offerId": "1",
                "legId": "L1",
                "currency": "USD",
                "pricePerPax": [{"paxType": "ADT", "baseFare": 100, "totalTax": 10}],
                "cabin": ["Y"],
            },
            {
                "offerId": "2",
                "legId": "L2",
                "currency": "USD",
                "pricePerPax": [{"paxType": "ADT", "baseFare": 80, "totalTax": 10}],
                "cabin": ["Y"],
            },
        ],
        "legs": [
            {"legId": "L1", "segmentIds": ["S1"]},
            {"legId": "L2", "segmentIds": ["S2^S3"]},
        ],
        "segments": [
            {
                "segmentId": "S1",
                "depAirport": "SZX",
                "arrAirport": "BKK",
                "depTime": "202606011200",
                "carrier": "CA",
                "flightNo": "8919",
            },
            {
                "segmentId": "S2",
                "depAirport": "SZX",
                "arrAirport": "HKG",
                "depTime": "202606010800",
                "carrier": "MU",
                "flightNo": "501",
            },
            {
                "segmentId": "S3",
                "depAirport": "HKG",
                "arrAirport": "BKK",
                "depTime": "202606011400",
                "carrier": "MU",
                "flightNo": "701",
            },
        ],
    }
    flt = _summarize_from_data(
        data,
        filters={"preferredCarrier": ["CA"], "depTimeWindow": {"from": "11:00", "to": "13:00"}},
    )
    if not flt.get("directLowest") or flt["directLowest"].get("offerId") != "1":
        errors.append("summarizer filter direct")
    if flt.get("transferLowest"):
        errors.append("summarizer should drop MU transfer")

    _run(
        [
            sys.executable,
            str(_SCRIPTS / "nl_to_search.py"),
            "parse",
            "--text",
            "深圳到曼谷 6月1日",
        ]
    )
    refined = _run(
        [
            sys.executable,
            str(_SCRIPTS / "nl_to_search.py"),
            "refine",
            "--text",
            "CA 中午12点",
        ]
    )
    if refined.get("action") != "refine":
        errors.append(f"refine action={refined.get('action')}")
    prefs = (refined.get("agentOnly") or {}).get("payload", {}).get("preferences", {})
    if "CA" not in (prefs.get("preferredCarrier") or []):
        errors.append("refine payload missing CA")

    from booking_format import format_search_data  # noqa: E402

    mock_raw = {
        "code": "000000",
        "data": data,
        "skillMeta": {"remainingQuota": 5, "dailyLimit": 10},
    }
    payload = json.loads((_ROOT / ".cache" / "pending_search.json").read_text(encoding="utf-8"))
    internal = format_search_data(mock_raw, "skill", search_payload=payload)
    if internal.get("success") and not internal.get("directLowest"):
        errors.append("format_search_data missing direct with filters")
    if "筛选条件" not in (internal.get("message") or ""):
        errors.append("format_search_data message missing filter line")

    out = {"ok": len(errors) == 0, "errors": errors}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
