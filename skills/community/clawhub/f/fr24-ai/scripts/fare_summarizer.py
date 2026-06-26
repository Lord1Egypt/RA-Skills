"""压缩 ApiSearchRs：直飞/中转各保留一条最低价，展示退改、行李、航班号。"""
from __future__ import annotations

import re
from typing import Any

PAX_ADT = "ADT"
BAGGAGE_EMPTY = "e"
BAGGAGE_NONE_LABEL = "无免费行李额"
BAGGAGE_UNKNOWN_LABEL = "无行李额信息"

POLICY_LABELS = {
    "withNoPenalty": "免费",
    "withCondition": "有条件",
    "notAllowed": "不允许",
    "taxRefundOnly": "仅退税",
    "airlinePolicyApplied": "以航司政策为准",
}


def _policy_label(code: str | None) -> str:
    if not code:
        return "未知"
    return POLICY_LABELS.get(code, code)


def _offer_total(offer: dict[str, Any]) -> float | None:
    prices = offer.get("pricePerPax") or []
    total = 0.0
    found = False
    for p in prices:
        if not isinstance(p, dict) or p.get("paxType") != PAX_ADT:
            continue
        base = p.get("baseFare")
        if base is None:
            continue
        tax = p.get("totalTax") or 0
        total += float(base) + float(tax or 0)
        found = True
    return round(total, 2) if found else None


def _first_adult_part(value: str | None) -> str:
    if not value or value == BAGGAGE_EMPTY:
        return ""
    if "-" in value:
        return value.split("-", 1)[0]
    return value


def _format_flight_no(carrier: str | None, flight_no: str | None) -> str:
    if not flight_no:
        return carrier or ""
    if carrier and not flight_no.upper().startswith(carrier.upper()):
        return f"{carrier}{flight_no}"
    return flight_no


def _build_leg_map(legs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {leg["legId"]: leg for leg in legs if isinstance(leg, dict) and leg.get("legId")}


def _build_segment_map(segments: list[dict[str, Any]] | set) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for seg in segments or []:
        if isinstance(seg, dict) and seg.get("segmentId"):
            out[seg["segmentId"]] = seg
    return out


def _outbound_segment_ids(offer: dict[str, Any], leg_map: dict[str, dict[str, Any]]) -> list[str]:
    leg_id = offer.get("legId")
    leg = leg_map.get(leg_id or "")
    if not leg:
        return []
    raw_ids = leg.get("segmentIds") or []
    if not raw_ids:
        return []
    raw = raw_ids[0]
    if "^" in raw:
        return [x for x in raw.split("^") if x]
    return [raw]


def _format_rule_line(action: str, policy: str | None, fee: Any, text: str | None) -> str:
    if text:
        return text
    label = _policy_label(policy)
    if fee is not None and float(fee) > 0:
        return f"{action}：{label}，费用 {fee}"
    return f"{action}：{label}"


def _build_refund_change(rules: dict[str, Any] | None) -> dict[str, Any]:
    if not rules:
        return {"refundText": "无退改信息", "changeText": "无退改信息", "details": []}
    refunds = rules.get("refund") or []
    changes = rules.get("change") or []
    adt_refund = next((r for r in refunds if r.get("paxType") == PAX_ADT), refunds[0] if refunds else None)
    adt_change = next((c for c in changes if c.get("paxType") == PAX_ADT), changes[0] if changes else None)
    details: list[str] = []
    for r in refunds:
        if r.get("paxType") == PAX_ADT:
            line = _format_rule_line("退票", r.get("refundPolicy"), r.get("refundFee"), r.get("refundText"))
            if line and line not in details:
                details.append(line)
    for c in changes:
        if c.get("paxType") == PAX_ADT:
            line = _format_rule_line("改期", c.get("changePolicy"), c.get("changeFee"), c.get("changeText"))
            if line and line not in details:
                details.append(line)
    return {
        "refundText": _format_rule_line(
            "退票",
            (adt_refund or {}).get("refundPolicy"),
            (adt_refund or {}).get("refundFee"),
            (adt_refund or {}).get("refundText"),
        )
        if adt_refund
        else "无退票规则",
        "changeText": _format_rule_line(
            "改期",
            (adt_change or {}).get("changePolicy"),
            (adt_change or {}).get("changeFee"),
            (adt_change or {}).get("changeText"),
        )
        if adt_change
        else "无改期规则",
        "details": details,
    }


def _format_bag_part(pc: str | None, weight: str | None, label: str) -> str:
    adult_pc = _first_adult_part(pc)
    adult_w = _first_adult_part(weight)
    parts: list[str] = []
    if adult_pc and adult_pc != BAGGAGE_EMPTY:
        parts.append(f"{label}{adult_pc}PC")
    if adult_w and adult_w != BAGGAGE_EMPTY:
        if parts:
            parts.append(" ")
        parts.append(f"{adult_w}KG")
    return "".join(parts)


def _build_baggage_lines(
    offer: dict[str, Any],
    segment_ids: list[str],
    seg_map: dict[str, dict[str, Any]],
) -> list[str]:
    extra = offer.get("extraInfo") or {}
    bags = extra.get("freeBaggageAllowance") or []
    bag_by_seg = {b["segmentId"]: b for b in bags if isinstance(b, dict) and b.get("segmentId")}
    lines: list[str] = []
    for idx, seg_id in enumerate(segment_ids, start=1):
        seg = seg_map.get(seg_id) or {}
        route = f"{seg.get('depAirport', '')}→{seg.get('arrAirport', '')}" or seg_id
        line = f"第{idx}段 {route}"
        bag = bag_by_seg.get(seg_id)
        if not bag:
            lines.append(f"{line} | {BAGGAGE_UNKNOWN_LABEL}")
            continue
        cabin = _format_bag_part(bag.get("cabinBagPc"), bag.get("cabinBagWeight"), "手提")
        checked = _format_bag_part(bag.get("checkedBagPc"), bag.get("checkedBagWeight"), "托运")
        if cabin:
            line += f" | {cabin}"
        if checked:
            line += f" | {checked}"
        if not cabin and not checked:
            line += f" | {BAGGAGE_NONE_LABEL}"
        lines.append(line)
    return lines


def _build_offer_summary(
    offer: dict[str, Any],
    segment_ids: list[str],
    seg_map: dict[str, dict[str, Any]],
    category: str,
    category_label: str,
    price: float,
) -> dict[str, Any]:
    segments_out: list[dict[str, Any]] = []
    flight_parts: list[str] = []
    cabins = offer.get("cabin") or []
    for i, seg_id in enumerate(segment_ids, start=1):
        seg = seg_map.get(seg_id) or {}
        fn = _format_flight_no(seg.get("carrier"), seg.get("flightNo"))
        cabin = cabins[i - 1] if len(cabins) >= i else (cabins[0] if cabins else None)
        segments_out.append(
            {
                "index": i,
                "depAirport": seg.get("depAirport"),
                "arrAirport": seg.get("arrAirport"),
                "depTime": seg.get("depTime"),
                "arrTime": seg.get("arrTime"),
                "carrier": seg.get("carrier"),
                "flightNo": fn,
                "cabin": cabin,
            }
        )
        flight_parts.append(fn)
    route = ""
    if segments_out:
        route = f"{segments_out[0]['depAirport']} → {segments_out[-1]['arrAirport']}"
    return {
        "offerId": str(offer["offerId"]) if offer.get("offerId") is not None else None,
        "flightCategory": category,
        "flightCategoryLabel": category_label,
        "totalPrice": price,
        "currency": offer.get("currency") or "CNY",
        "platingCarrier": offer.get("platingCarrier"),
        "route": route,
        "flights": "+".join(flight_parts),
        "segments": segments_out,
        "refundChange": _build_refund_change(offer.get("rules")),
        "baggage": _build_baggage_lines(offer, segment_ids, seg_map),
    }


def _clock_minutes(dep_time: str | None) -> int | None:
    """从 depTime 提取当日分钟数（支持 yyyyMMddHHmm / yyyy-MM-dd HH:mm 等）。"""
    if not dep_time:
        return None
    digits = re.sub(r"\D", "", str(dep_time))
    if len(digits) >= 12:
        hh, mm = int(digits[-4:-2]), int(digits[-2:])
    elif len(digits) >= 4:
        hh, mm = int(digits[:2]), int(digits[2:4])
    else:
        return None
    if hh > 23 or mm > 59:
        return None
    return hh * 60 + mm


def _window_bounds(window: dict[str, Any]) -> tuple[int | None, int | None]:
    def _to_min(s: str | None) -> int | None:
        if not s or ":" not in s:
            return None
        h, m = s.split(":", 1)
        try:
            return int(h) * 60 + int(m)
        except ValueError:
            return None

    return _to_min(window.get("from")), _to_min(window.get("to"))


def _offer_matches_filters(
    offer: dict[str, Any],
    seg_ids: list[str],
    seg_map: dict[str, dict[str, Any]],
    filters: dict[str, Any] | None,
) -> bool:
    if not filters:
        return True
    carriers = filters.get("preferredCarrier") or []
    if carriers:
        want = {str(c).upper() for c in carriers}
        seg_carriers = {
            str((seg_map.get(sid) or {}).get("carrier") or "").upper()
            for sid in seg_ids
        }
        plating = str(offer.get("platingCarrier") or "").upper()
        if not (want & seg_carriers) and plating not in want:
            return False
    window = filters.get("depTimeWindow")
    if window:
        start_min, end_min = _window_bounds(window)
        if start_min is not None and end_min is not None:
            first_seg = seg_map.get(seg_ids[0]) or {}
            dep_min = _clock_minutes(first_seg.get("depTime"))
            if dep_min is None:
                return False
            if start_min <= end_min:
                if not (start_min <= dep_min <= end_min):
                    return False
            else:
                if not (dep_min >= start_min or dep_min <= end_min):
                    return False
    return True


def _summarize_from_data(
    data: dict[str, Any],
    *,
    filters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    offers = data.get("offers") or []
    leg_map = _build_leg_map(data.get("legs") or [])
    seg_map = _build_segment_map(data.get("segments") or [])

    direct_best: dict[str, Any] | None = None
    transfer_best: dict[str, Any] | None = None
    direct_price: float | None = None
    transfer_price: float | None = None
    direct_count = 0
    transfer_count = 0
    matched_count = 0

    for offer in offers:
        if not isinstance(offer, dict):
            continue
        seg_ids = _outbound_segment_ids(offer, leg_map)
        if not seg_ids:
            continue
        if not _offer_matches_filters(offer, seg_ids, seg_map, filters):
            continue
        matched_count += 1
        is_direct = len(seg_ids) == 1
        if is_direct:
            direct_count += 1
        else:
            transfer_count += 1
        price = _offer_total(offer)
        if price is None:
            continue
        summary = _build_offer_summary(
            offer,
            seg_ids,
            seg_map,
            "direct" if is_direct else "transfer",
            "直飞" if is_direct else "中转",
            price,
        )
        if is_direct:
            if direct_price is None or price < direct_price:
                direct_price = price
                direct_best = summary
        else:
            if transfer_price is None or price < transfer_price:
                transfer_price = price
                transfer_best = summary

    out = {
        "totalOffers": len(offers),
        "directCount": direct_count,
        "transferCount": transfer_count,
        "directLowest": direct_best,
        "transferLowest": transfer_best,
    }
    if filters:
        out["filterApplied"] = True
        out["matchedOfferCount"] = matched_count
    return out


def summarize_response(
    body: dict[str, Any],
    *,
    filters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """从 Skill 搜索响应生成展示用摘要。"""
    meta = body.get("skillMeta") or {}
    server_summary = body.get("summary")
    if server_summary and not filters:
        core = dict(server_summary)
    else:
        core = _summarize_from_data(body.get("data") or {}, filters=filters)

    return {
        **core,
        "remainingQuota": meta.get("remainingQuota"),
        "dailyLimit": meta.get("dailyLimit"),
        "code": body.get("code"),
        "message": body.get("message"),
        "traceId": body.get("traceId"),
    }
