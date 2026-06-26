"""搜索/校验/生单结果格式化（Skill JSON 信封）。"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import (  # noqa: E402
    REGISTER_PORTAL_URL,
    SEARCH_ONLY_HINT,
    USER_BOOKING_AGENT_HINT,
    USER_BOOKING_USER_MESSAGE,
    USER_SKILL_QUOTA_EXCEEDED_MESSAGE,
    booking_required_payload,
    is_booking_ready,
    is_newapi_configured,
)
from booking_guidance import (  # noqa: E402
    BOOKING_SELECTION_USER_PROMPT,
    BOOKING_WORKFLOW_STEPS,
    ORDER_CONFIRM_USER_PROMPT,
    PASSENGER_INFO_EXAMPLES,
    PASSENGER_INFO_USER_PROMPT,
    build_booking_choices,
    build_itinerary_preview,
    is_verify_identity_mismatch,
    selection_required,
    verify_identity_mismatch_payload,
)
from fare_summarizer import summarize_response, _summarize_from_data  # noqa: E402
from search_refinement import describe_preferences, extract_search_filters  # noqa: E402
from output_export import (  # noqa: E402
    order_agent_only,
    order_user_view,
    search_agent_only,
    search_user_view,
    verify_agent_only,
    verify_user_view,
    wrap_envelope,
)
from passenger_display import build_contact_display, build_passenger_display  # noqa: E402

SUCCESS_CODES = frozenset({"0", "000000"})


def _is_success(code: str) -> bool:
    return str(code) in SUCCESS_CODES


def _offer_block(label: str, offer: dict | None) -> dict[str, Any] | None:
    if not offer:
        return None
    return {
        "label": label,
        "offerId": str(offer["offerId"]) if offer.get("offerId") is not None else None,
        "route": offer.get("route"),
        "flights": offer.get("flights"),
        "totalPrice": offer.get("totalPrice"),
        "currency": offer.get("currency"),
        "platingCarrier": offer.get("platingCarrier"),
        "segments": offer.get("segments"),
        "refundChange": offer.get("refundChange"),
        "baggage": offer.get("baggage"),
    }


def _normalize_newapi_raw(raw: dict, *, filters: dict[str, Any] | None = None) -> dict:
    if raw.get("summary") and not filters:
        return raw
    data = raw.get("data")
    if isinstance(data, dict):
        return {**raw, "summary": _summarize_from_data(data, filters=filters)}
    return raw


def format_search_data(
    raw: dict,
    search_mode: str,
    *,
    search_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    skill_like = search_mode in ("skill", "skill-auth", "newapi")
    prefs = (search_payload or {}).get("preferences") or {}
    filters = extract_search_filters(prefs)
    filter_note = describe_preferences(prefs)
    if search_mode == "newapi":
        raw = _normalize_newapi_raw(raw, filters=filters or None)

    code = str(raw.get("code", ""))
    if code in ("CONFIG_REQUIRED", "CONFIG_ERROR"):
        return {
            **booking_required_payload(step="search"),
            "searchMode": search_mode,
        }

    success = _is_success(code)
    summary = (
        summarize_response(raw, filters=filters or None)
        if skill_like
        else (raw.get("summary") or {})
    )
    if search_mode == "newapi" and not summary.get("directLowest"):
        summary = {
            **_summarize_from_data(raw.get("data") or {}, filters=filters or None),
            **summary,
        }

    direct = _offer_block("直飞最低", summary.get("directLowest"))
    transfer = _offer_block("中转最低", summary.get("transferLowest"))
    booking_enabled = is_newapi_configured()
    booking_ready = is_booking_ready()
    choices = build_booking_choices(direct, transfer) if success and booking_enabled else []

    lines: list[str] = []
    if success:
        mode_label = "NewApi 采购搜索" if search_mode == "newapi" else "Skill 演示搜索"
        lines.append(f"（{mode_label}）")
        if filter_note:
            lines.append(f"筛选条件：{filter_note}")
        if filter_note and not direct and not transfer:
            matched = summary.get("matchedOfferCount", 0)
            lines.append(
                f"未找到符合上述条件的报价（共检索 {summary.get('totalOffers', 0)} 条）。"
                f"请放宽航司或起飞时段后说「重新搜索」或补充条件。"
            )
        if direct:
            lines.append(
                f"【直飞最低】{direct['route']} {direct['flights']} "
                f"约 {direct['totalPrice']} {direct['currency']}/人"
            )
        if transfer:
            lines.append(
                f"【中转最低】{transfer['route']} {transfer['flights']} "
                f"约 {transfer['totalPrice']} {transfer['currency']}/人"
            )
        if selection_required(choices):
            lines.append(BOOKING_SELECTION_USER_PROMPT)
        if booking_enabled and booking_ready:
            lines.append("如需预订，请提供乘客与联系人信息；核对后将为您校验报价并生单。")
        elif not booking_enabled:
            lines.append(SEARCH_ONLY_HINT)
            lines.append(USER_BOOKING_USER_MESSAGE)
    else:
        if code == "307901":
            lines.append(USER_SKILL_QUOTA_EXCEEDED_MESSAGE)
        else:
            lines.append(raw.get("message") or f"搜索失败：{code}")

    return {
        "success": success,
        "code": code,
        "traceId": raw.get("traceId"),
        "processingTime": raw.get("processingTime"),
        "searchMode": search_mode,
        "bookingEnabled": booking_enabled,
        "bookingReady": booking_ready,
        "directLowest": direct,
        "transferLowest": transfer,
        "bookingChoices": choices,
        "selectionRequired": selection_required(choices),
        "remainingQuota": summary.get("remainingQuota"),
        "dailyLimit": summary.get("dailyLimit"),
        "registerPortalUrl": REGISTER_PORTAL_URL if not booking_enabled else None,
        "bookingConfigHint": USER_BOOKING_AGENT_HINT if not booking_enabled else None,
        "workflowSteps": BOOKING_WORKFLOW_STEPS if booking_ready else None,
        "filterNote": filter_note or None,
        "message": "\n".join(lines),
    }


def wrap_search(
    raw: dict,
    search_mode: str,
    *,
    search_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    internal = format_search_data(raw, search_mode, search_payload=search_payload)
    user_view = search_user_view(internal)
    return wrap_envelope(
        action="search",
        status="success" if internal.get("success") else "failure",
        user_view=user_view,
        agent_only=search_agent_only(internal),
        message=user_view.get("message", ""),
    )


def format_verify_data(
    raw: dict,
    *,
    passengers: list[dict[str, Any]] | None = None,
    agent_contact: dict[str, str] | None = None,
    passenger_raw_mappings: list[dict[str, Any]] | None = None,
    contact_raw: dict[str, Any] | None = None,
    selected_offer: dict[str, Any] | None = None,
) -> dict[str, Any]:
    code = str(raw.get("code", ""))
    if code in ("CONFIG_REQUIRED", "CONFIG_ERROR"):
        out = booking_required_payload(step="verify")
        out["message"] = raw.get("message") or USER_BOOKING_USER_MESSAGE
        if raw.get("detail"):
            out["detail"] = raw.get("detail")
        return out

    if is_verify_identity_mismatch(code, raw.get("message")):
        out = verify_identity_mismatch_payload()
        out["traceId"] = raw.get("traceId")
        out["processingTime"] = raw.get("processingTime")
        out["apiMessage"] = raw.get("message")
        return out

    success = _is_success(code)
    data = raw.get("data") or {}
    offers = data.get("offer") or []
    offer = offers[0] if offers else {}
    verify_offer_id = str(offer["offerId"]) if offer.get("offerId") is not None else None

    lines: list[str] = []
    if success:
        lines.append(f"校验成功：总价约 {offer.get('totalPrice')} {offer.get('currency', '')}。")
        lines.append(ORDER_CONFIRM_USER_PROMPT)
    else:
        lines.append(f"校验失败：{raw.get('message') or code}")

    out: dict[str, Any] = {
        "success": success,
        "code": code,
        "traceId": raw.get("traceId"),
        "processingTime": raw.get("processingTime"),
        "verifyOfferId": verify_offer_id,
        "totalPrice": offer.get("totalPrice"),
        "currency": offer.get("currency"),
        "workflowStep": 4 if success else 3,
        "orderConfirmPrompt": ORDER_CONFIRM_USER_PROMPT if success else None,
        "message": "\n".join(lines),
    }
    if success and passengers and agent_contact:
        p_disp = build_passenger_display(passengers, raw_mappings=passenger_raw_mappings)
        c_disp = build_contact_display(agent_contact, raw=contact_raw)
        out["passengers"] = passengers
        out["agentContact"] = agent_contact
        out["passengerDisplay"] = p_disp
        out["contactDisplay"] = c_disp
        out["requiresOrderConfirmation"] = True
        out["orderPreview"] = {
            "itinerary": build_itinerary_preview(
                selected_offer=selected_offer,
                verify_offer=offer,
                total_price=offer.get("totalPrice"),
                currency=offer.get("currency", ""),
            ),
            "passengerDisplay": p_disp,
            "contactDisplay": c_disp,
            "verifyOfferId": verify_offer_id,
            "totalPrice": offer.get("totalPrice"),
            "currency": offer.get("currency"),
        }
    return out


def wrap_verify(data: dict[str, Any]) -> dict[str, Any]:
    user_view = verify_user_view(data)
    return wrap_envelope(
        action="verify",
        status="success" if data.get("success") else "failure",
        user_view=user_view,
        agent_only=verify_agent_only(data),
        message=user_view.get("message", ""),
    )


def format_order_data(raw: dict) -> dict[str, Any]:
    code = str(raw.get("code", ""))
    if code in ("CONFIG_REQUIRED", "CONFIG_ERROR"):
        out = booking_required_payload(step="order")
        out["message"] = raw.get("message") or USER_BOOKING_USER_MESSAGE
        return out

    success = _is_success(code)
    body = raw.get("data") or {}
    lines: list[str] = []
    if success:
        lines.append(
            f"生单成功：订单号 {body.get('orderNo')}，状态 {body.get('orderStatus')}，"
            f"总价 {body.get('totalPrice')} {body.get('currency', '')}。"
        )
    else:
        lines.append(f"生单失败：{raw.get('message') or code}")

    return {
        "success": success,
        "code": code,
        "orderNo": body.get("orderNo"),
        "orderStatus": body.get("orderStatus"),
        "partnerOrderNo": body.get("partnerOrderNo"),
        "totalPrice": body.get("totalPrice"),
        "currency": body.get("currency"),
        "payDeadline": body.get("payDeadline"),
        "message": "\n".join(lines),
    }


def wrap_order(data: dict[str, Any]) -> dict[str, Any]:
    user_view = order_user_view(data)
    return wrap_envelope(
        action="order",
        status="success" if data.get("success") else "failure",
        user_view=user_view,
        agent_only=order_agent_only(data),
        message=user_view.get("message", ""),
    )
