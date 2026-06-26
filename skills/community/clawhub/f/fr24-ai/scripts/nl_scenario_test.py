#!/usr/bin/env python3
"""自然语言场景批量测试：解析 -> 搜索 -> 摘要校验。"""
from __future__ import annotations

import json
import secrets
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_ROOT = _SCRIPTS.parent
for p in (_ROOT, _SCRIPTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from config import CLIENT_KEY_HEADER, EXPORT_BASE_URL, GRAY_HEADER, SHOPPING_PATH  # noqa: E402
from query_parser import build_payload_from_intent, parse_simple_text  # noqa: E402

CACHE = _ROOT / ".cache" / "nl_test"


@dataclass
class Scenario:
    id: str
    text: str
    intent: dict | None = None
    expect_parse: str = "success"  # success | fail
    expect_search: str = "skip"  # success | fail | skip
    note: str = ""


SCENARIOS: list[Scenario] = [
    Scenario("S01", "北京飞曼谷 7月1日", expect_search="success", note="基础单程"),
    Scenario("S02", "重庆到伦敦 6月20日 2大1小 商务舱", expect_search="success", note="乘客+舱等"),
    Scenario("S03", "上海直飞东京 明天", expect_search="success", note="直飞偏好"),
    Scenario("S04", "北京往返曼谷 7月1日 回7月8日", expect_search="success", note="往返"),
    Scenario("S05", "PEK到BKK 2026-08-01", note="IATA+标准日期"),
    Scenario("S06", "成都去新加坡 8月15日 1大1小", note="去字+儿童"),
    Scenario("S07", "首都机场飞曼谷 7月10日", note="机场别名"),
    Scenario("S08", "我想从拉萨去迪拜", expect_parse="fail", note="缺日期应提示补充"),
    Scenario("S09", "北京飞曼谷", expect_parse="fail", note="缺日期"),
    Scenario("S10", "广州→悉尼 2026-12-01 经济舱", note="箭头符号"),
    Scenario(
        "S11",
        "",
        intent={
            "tripType": "OW",
            "legs": [{"originText": "重庆", "destinationText": "伦敦", "depDateText": "2026-06-20"}],
            "passengers": {"adult": 1},
            "cabinText": "商务舱",
            "directOnly": False,
        },
        note="Agent intent 商务 CKG-LON",
    ),
    Scenario(
        "S12",
        "",
        intent={
            "tripType": "RT",
            "legs": [
                {"originText": "北京", "destinationText": "曼谷", "depDateText": "2026-07-01"},
                {"originText": "曼谷", "destinationText": "北京", "depDateText": "2026-07-08"},
            ],
            "passengers": {"adult": 2, "child": 0},
            "cabinText": "经济舱",
        },
        note="Agent intent 往返",
    ),
    Scenario("S13", "北京飞曼谷 7月1日 3婴儿", expect_parse="fail", note="婴儿超成人应校验失败"),
]


def run_parse(sc: Scenario) -> dict:
    if sc.intent:
        payload, summary, err = build_payload_from_intent(sc.intent)
    else:
        payload, summary, err = parse_simple_text(sc.text)
    ok = err is None
    return {
        "ok": ok,
        "error": err,
        "summary": summary,
        "payload": payload,
    }


def run_search(payload: dict, client_key: str) -> dict:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        CLIENT_KEY_HEADER: client_key,
    }
    if GRAY_HEADER:
        headers["gray"] = GRAY_HEADER
    req = urllib.request.Request(
        EXPORT_BASE_URL + SHOPPING_PATH,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            raw = json.loads(body)
        except json.JSONDecodeError:
            return {"code": str(e.code), "ok": False, "errors": [body[:200]], "message": body[:200]}
    code = str(raw.get("code", ""))
    summary = raw.get("summary") or {}
    errors = []
    if code in ("0", "000000"):
        if not summary.get("directLowest") and not summary.get("transferLowest"):
            errors.append("summary empty")
        offers = (raw.get("data") or {}).get("offers") or []
        if len(offers) > 2:
            errors.append(f"offers not trimmed: {len(offers)}")
        for key in ("directLowest", "transferLowest"):
            o = summary.get(key)
            if not o:
                continue
            if not o.get("flights"):
                errors.append(f"{key} missing flights")
            if not o.get("refundChange"):
                errors.append(f"{key} missing refundChange")
    return {
        "code": code,
        "ok": code in ("0", "000000") and not errors,
        "errors": errors,
        "direct": bool(summary.get("directLowest")),
        "transfer": bool(summary.get("transferLowest")),
        "remainingQuota": (raw.get("skillMeta") or {}).get("remainingQuota"),
        "message": raw.get("message"),
    }


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    report: list[dict] = []
    search_key = secrets.token_urlsafe(32)

    for sc in SCENARIOS:
        row: dict = {"id": sc.id, "note": sc.note, "text": sc.text or "(intent)"}
        pr = run_parse(sc)
        row["parse"] = pr
        parse_ok = pr["ok"]
        expect_ok = sc.expect_parse == "success"
        row["parseMatch"] = parse_ok == expect_ok

        if parse_ok and sc.expect_search != "skip":
            sr = run_search(pr["payload"], search_key)
            row["search"] = sr
            if sc.expect_search == "success":
                row["searchMatch"] = sr["ok"]
            elif sc.expect_search == "fail":
                row["searchMatch"] = not sr["ok"]
            else:
                row["searchMatch"] = True
            if sr.get("code") in ("307901", "404"):
                row["searchNote"] = f"infra/code={sr.get('code')}, rotated client key"
                search_key = secrets.token_urlsafe(32)
        else:
            row["search"] = None
            row["searchMatch"] = sc.expect_search == "skip" or not expect_ok

        report.append(row)

    out_path = CACHE / "report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    failed = [r for r in report if not r.get("parseMatch") or not r.get("searchMatch")]
    print(json.dumps({"total": len(report), "failed": len(failed), "report": str(out_path)}, ensure_ascii=False))
    for r in failed:
        print(f"\n--- {r['id']} {r['note']} ---")
        print("text:", r["text"])
        if not r.get("parseMatch"):
            print("parse expected", "success" if "fail" not in r["note"] else "?", "got", r["parse"].get("error") or "ok")
        if r.get("search") and not r.get("searchMatch"):
            print("search:", r["search"])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
