"""自然语言 / SearchIntent -> Skill 搜索 JSON（ApiSearchRq 搜索字段）。"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from date_parser import parse_date
from passenger_parser import DEFAULT, parse_passengers, validate_passengers
from place_resolver import resolve_place_required
from search_refinement import (  # noqa: E402
    describe_preferences,
    parse_carriers_from_text,
    parse_dep_time_window,
)

CABIN_MAP = {
    "经济": "Y",
    "经济舱": "Y",
    "y": "Y",
    "商务": "C",
    "公务": "C",
    "商务舱": "C",
    "c": "C",
    "头等": "F",
    "头等舱": "F",
    "f": "F",
    "超经": "P",
    "超级经济": "P",
    "p": "P",
}


def build_payload_from_intent(intent: dict[str, Any]) -> tuple[dict | None, str | None, str | None]:
    """从 Agent 提供的 intent 构建请求体。返回 (payload, summary, error)。"""
    trip = (intent.get("tripType") or "OW").upper()
    legs_in = intent.get("legs") or []
    if not legs_in:
        return None, None, "缺少航段信息"

    legs = []
    for i, leg in enumerate(legs_in):
        origin, err = resolve_place_required(
            leg.get("originCode") or leg.get("originText") or leg.get("origin") or "",
            "出发地",
        )
        if err:
            return None, None, err
        dest, err = resolve_place_required(
            leg.get("destinationCode") or leg.get("destinationText") or leg.get("destination") or "",
            "目的地",
        )
        if err:
            return None, None, err
        dep, err = parse_date(leg.get("depDateText") or leg.get("depDate") or "")
        if err:
            return None, None, err
        type_o = leg.get("typeO") or "airportcode"
        type_d = leg.get("typeD") or "airportgroup"
        item = {
            "origin": origin,
            "destination": dest,
            "depDate": dep,
            "typeO": type_o,
            "typeD": type_d,
        }
        legs.append(item)

    if trip == "RT" and len(legs) < 2:
        return None, None, "往返需要出发日期与返程日期"
    if len(legs) > 2:
        return None, None, "Skill 暂不支持超过2段行程，请拆成单程或往返"

    passengers = intent.get("passengers") or {}
    if isinstance(passengers, dict) and passengers:
        pax = {
            "adultNum": int(passengers.get("adult", passengers.get("adultNum", 1))),
            "childNum": int(passengers.get("child", passengers.get("childNum", 0))),
            "infantNum": int(passengers.get("infant", passengers.get("infantNum", 0))),
        }
    else:
        pax = parse_passengers(intent.get("passengerText"))

    perr = validate_passengers(pax)
    if perr:
        return None, None, perr

    prefs = intent.get("preferences") or {}
    cabin_raw = str(prefs.get("cabin") or intent.get("cabinText") or "Y").strip()
    if len(cabin_raw) == 1:
        cabin = cabin_raw.upper()
    else:
        cabin = CABIN_MAP.get(cabin_raw.lower(), "Y")

    stops = 2
    if intent.get("directOnly") or prefs.get("directOnly"):
        stops = 0
    elif prefs.get("stops") is not None:
        stops = int(prefs["stops"])

    payload = {
        "searchLegs": legs,
        "adultNum": pax["adultNum"],
        "childNum": pax["childNum"],
        "infantNum": pax["infantNum"],
        "preferences": {
            "cabin": cabin[:1].upper() if cabin else "Y",
            "stops": stops,
            "resultCtrl": min(20, int(prefs.get("resultCtrl", 15))),
        },
    }
    if prefs.get("preferredCarrier"):
        payload["preferences"]["preferredCarrier"] = prefs["preferredCarrier"]
    if prefs.get("prohibitedCarrier"):
        payload["preferences"]["prohibitedCarrier"] = prefs["prohibitedCarrier"]
    if prefs.get("depTimeWindow"):
        payload["preferences"]["depTimeWindow"] = prefs["depTimeWindow"]
    if prefs.get("depTimeLabel"):
        payload["preferences"]["depTimeLabel"] = prefs["depTimeLabel"]

    summary = _format_summary(payload, trip, intent.get("directOnly"))
    return payload, summary, None


DATE_PART = (
    r"\d{4}-\d{2}-\d{2}|\d+月\d+[日号]|明天|后天|今天|今日|明日|"
    r"(?:本|下)周[一二三四五六日天]|下星期[一二三四五六日天]|本星期[一二三四五六日天]|"
    r"下周|本周|下星期|本星期"
)
DATE_TOKEN = rf"({DATE_PART})"


def _strip_direct_keyword(s: str) -> tuple[str, bool]:
    """去掉「直飞」避免被吃进城市名（如 上海直飞东京）。"""
    direct = "直飞" in s
    cleaned = re.sub(r"直飞", " ", s)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned, direct


def _strip_leading_passenger_text(s: str) -> str:
    """去掉句首乘客描述，避免干扰航线匹配。"""
    return re.sub(
        r"^[\s\d一二两三四五六七八九十]+[大小](?:[\s\d一二两三四五六七八九十]+[大小])?\s*",
        "",
        s,
    ).strip()


def _match_route(s: str) -> re.Match[str] | None:
    """匹配 出发地-目的地-去程日期。"""
    s = _strip_leading_passenger_text(s)
    patterns = [
        rf"从\s*(.+?)\s*去\s*(.+?)\s+{DATE_TOKEN}",
        rf"(.+?)往返\s*(.+?)\s+{DATE_TOKEN}",
        rf"(.+?)(?:到|去|飞|→|->)\s*(.+?)\s+{DATE_TOKEN}",
        rf"(.+?)(?:到|去|飞)(.+?)\s*{DATE_TOKEN}",
        rf"(.+?)\s+(.+?)\s+{DATE_TOKEN}",
    ]
    for pat in patterns:
        m = re.search(pat, s)
        if m:
            return m
    return None


def parse_simple_text(text: str) -> tuple[dict | None, str | None, str | None]:
    """从简短中文句式解析（规则），复杂句子应由 Agent 构造 intent。"""
    raw = text.strip()
    raw = re.sub(r"多少钱|价格|票价|最便宜|查一下|查询|帮我", "", raw).strip()
    s, direct_only = _strip_direct_keyword(raw)
    s = _strip_leading_passenger_text(s)
    s = re.sub(r"(?<=[\u4e00-\u9fff])(下周|本周|下星期|本星期)", r" \1", s)
    intent: dict[str, Any] = {"tripType": "OW", "legs": [{}], "passengers": {}}

    m = _match_route(s)
    if not m:
        partial = re.search(r"从\s*(.+?)\s*去\s*(.+?)(?:\s|$)", s)
        if partial:
            return (
                None,
                None,
                f"已识别 {partial.group(1).strip()}→{partial.group(2).strip()}，请补充出发日期",
            )
        return None, None, "未能理解行程，请说明「出发地到目的地 + 日期」，或由 Agent 补充 intent JSON"

    origin = m.group(1).strip()
    dest = m.group(2).strip()
    dep_date = m.group(3).strip()
    intent["legs"][0]["originText"] = origin
    intent["legs"][0]["destinationText"] = dest
    intent["legs"][0]["depDateText"] = dep_date

    if "往返" in raw:
        intent["tripType"] = "RT"
        m_ret = re.search(rf"(?:回|返程|返回)\s*({DATE_PART})", raw)
        if not m_ret:
            dates = re.findall(rf"({DATE_PART})", raw)
            if len(dates) >= 2:
                ret_date = dates[1]
            else:
                return None, None, "往返请补充返程日期（如：回7月8日）"
        else:
            ret_date = m_ret.group(1).strip()
        intent["legs"].append(
            {
                "originText": dest,
                "destinationText": origin,
                "depDateText": ret_date,
            }
        )

    intent["passengerText"] = raw
    if direct_only:
        intent["directOnly"] = True
    if "商务" in raw or "公务" in raw:
        intent["cabinText"] = "商务舱"
    elif "头等" in raw:
        intent["cabinText"] = "头等舱"
    elif "经济" in raw:
        intent["cabinText"] = "经济舱"

    carriers = parse_carriers_from_text(raw)
    if carriers:
        intent.setdefault("preferences", {})["preferredCarrier"] = carriers
    window, time_label = parse_dep_time_window(raw)
    if window:
        intent.setdefault("preferences", {})["depTimeWindow"] = window
        if time_label:
            intent["preferences"]["depTimeLabel"] = time_label

    return build_payload_from_intent(intent)


def _format_summary(payload: dict, trip: str, direct_only: bool = False) -> str:
    legs = payload["searchLegs"]
    parts = [f"{l['origin']}→{l['destination']} {l['depDate']}" for l in legs]
    p = payload
    direct_note = "，仅直飞" if direct_only or p.get("preferences", {}).get("stops") == 0 else ""
    filter_note = describe_preferences(p.get("preferences") or {})
    extra = f"，{filter_note}" if filter_note else ""
    return (
        f"{'往返' if trip == 'RT' else '单程'} "
        f"{' / '.join(parts)}，"
        f"{p['adultNum']}成人{p['childNum']}儿童{p['infantNum']}婴儿，"
        f"舱等{p['preferences']['cabin']}{direct_note}{extra}"
    )


def main():
    import argparse
    import sys

    _scripts = Path(__file__).resolve().parent
    _root = _scripts.parent
    if str(_scripts) not in sys.path:
        sys.path.insert(0, str(_scripts))
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

    from output_export import failure_envelope, parse_user_view, wrap_envelope  # noqa: E402

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["build", "parse"])
    parser.add_argument("--text", default="")
    parser.add_argument("--intent-file", default="")
    args = parser.parse_args()

    pending = _root / ".cache" / "pending_search.json"

    if args.command == "parse":
        payload, summary, err = parse_simple_text(args.text)
    else:
        intent = json.loads(open(args.intent_file, encoding="utf-8").read())
        payload, summary, err = build_payload_from_intent(intent)

    if err:
        print(json.dumps(failure_envelope("parse", err), ensure_ascii=False, indent=2))
        sys.exit(1)

    pending.parent.mkdir(parents=True, exist_ok=True)
    pending.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out = wrap_envelope(
        action="parse",
        status="success",
        user_view=parse_user_view(summary, payload),
        agent_only={"payload": payload, "payloadFile": str(pending)},
        message="解析成功，请确认下方行程；确认后将为您搜索航班。",
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
