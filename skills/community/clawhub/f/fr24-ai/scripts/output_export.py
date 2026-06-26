"""用户展示/下载视图：剥离调试与 Agent 内部字段。"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import SKILL_ID  # noqa: E402

# 不得出现在 userView / message（用户可见）中的片段
_USER_TEXT_BLOCKLIST = (
    "FR_NEWAPI_SKIP",
    "FR_BOOKING_TEST",
    "SKIP_AUTH",
    "SKIP_IP_WHITELIST",
    "fr24-skip",
    "flight-deve",
    "skill.local.env",
    "FR_SKILL_GRAY_HEADER",
    "FR_SKILL_EXPORT_BASE_URL",
    "nl_scenario_test",
    "booking_flow_test",
)


def sanitize_user_text(text: str) -> str:
    """去掉联调环境变量、deve 网关等维护者信息。"""
    if not text:
        return ""
    kept: list[str] = []
    for line in str(text).splitlines():
        upper = line.upper()
        if any(token in upper for token in _USER_TEXT_BLOCKLIST):
            continue
        if "联调" in line and any(x in line for x in ("可选", "deve", "测试", "SKIP", "维护者")):
            continue
        if "跳过" in line and ("白名单" in line or "签名" in line):
            continue
        if line.strip().startswith("#") and ("$env:" in line or "set FR_" in line):
            continue
        kept.append(line)
    return "\n".join(kept).strip()


# 仅写入 agentOnly，不得出现在 userView / 用户下载附件中
_SEARCH_AGENT_KEYS = frozenset(
    {
        "code",
        "traceId",
        "processingTime",
        "searchMode",
        "bookingEnabled",
        "bookingReady",
        "workflowSteps",
        "bookingConfigHint",
        "registerPortalUrl",
        "bookingChoices",
    }
)

# bookingConfigHint 仅存在于 agentOnly，且不得进入 userView / message

_VERIFY_AGENT_KEYS = frozenset(
    {
        "code",
        "traceId",
        "processingTime",
        "workflowStep",
        "verifyOfferId",
        "passengers",
        "agentContact",
        "passengerRawMappings",
        "contactRaw",
        "apiMessage",
        "nextSteps",
    }
)

_USER_OFFER_KEYS = frozenset(
    {
        "label",
        "route",
        "flights",
        "totalPrice",
        "currency",
        "platingCarrier",
        "segments",
        "refundChange",
        "baggage",
        "flightCategory",
        "flightCategoryLabel",
    }
)


def _pick_keys(obj: dict[str, Any] | None, keys: frozenset[str]) -> dict[str, Any] | None:
    if not obj:
        return None
    return {k: obj[k] for k in keys if k in obj}


def user_offer(offer: dict[str, Any] | None) -> dict[str, Any] | None:
    out = _pick_keys(offer, _USER_OFFER_KEYS)
    if out and offer.get("offerId"):
        out["quoteId"] = offer["offerId"]
    return out


def user_booking_choices(choices: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    """用户可选直飞/中转，含 quoteId 以便 Agent 准确对应。"""
    out: list[dict[str, Any]] = []
    for c in choices or []:
        if not isinstance(c, dict):
            continue
        item = {
            "key": c.get("key"),
            "label": c.get("label"),
            "route": c.get("route"),
            "flights": c.get("flights"),
            "totalPrice": c.get("totalPrice"),
            "currency": c.get("currency"),
        }
        if c.get("offerId"):
            item["quoteId"] = c["offerId"]
        out.append(item)
    return out


def _refund_baggage_lines(offer: dict[str, Any] | None) -> list[str]:
    if not offer:
        return []
    lines: list[str] = []
    rc = offer.get("refundChange") or {}
    if rc.get("refundText"):
        lines.append(f"退票：{rc['refundText']}")
    if rc.get("changeText"):
        lines.append(f"改期：{rc['changeText']}")
    for d in rc.get("details") or []:
        if d and d not in lines:
            lines.append(str(d))
    for b in offer.get("baggage") or []:
        lines.append(str(b))
    return lines


def build_search_user_message(user_view: dict[str, Any], *, demo: bool = True) -> str:
    lines: list[str] = []
    if demo:
        lines.append("（测试环境演示价，人均成人价）")
    quota = user_view.get("remainingQuota")
    if quota is not None:
        limit = user_view.get("dailyLimit")
        if limit is not None:
            lines.append(f"今日剩余搜索次数：{quota}/{limit}")
        else:
            lines.append(f"今日剩余搜索次数：{quota}")

    for key, title in (("directLowest", "直飞最低"), ("transferLowest", "中转最低")):
        offer = user_view.get(key)
        if not offer:
            continue
        lines.append(
            f"【{title}】{offer.get('route', '')} {offer.get('flights', '')} "
            f"约 {offer.get('totalPrice')} {offer.get('currency', '')}/人"
        )
        lines.extend(_refund_baggage_lines(offer))

    if user_view.get("selectionRequired"):
        lines.append("请先告知要订「直飞」或「中转」。")
    return "\n".join(lines) if lines else user_view.get("message") or ""


def search_user_view(internal: dict[str, Any]) -> dict[str, Any]:
    demo = internal.get("searchMode") != "newapi"
    user: dict[str, Any] = {
        "success": internal.get("success"),
        "directLowest": user_offer(internal.get("directLowest")),
        "transferLowest": user_offer(internal.get("transferLowest")),
        "remainingQuota": internal.get("remainingQuota"),
        "dailyLimit": internal.get("dailyLimit"),
        "selectionRequired": internal.get("selectionRequired"),
        "bookingChoices": user_booking_choices(internal.get("bookingChoices")),
    }
    if not internal.get("success"):
        user["message"] = internal.get("message") or "搜索未成功"
        if internal.get("registerPortalUrl"):
            user["registerPortalUrl"] = internal["registerPortalUrl"]
    else:
        user["message"] = build_search_user_message(user, demo=demo)
    return user


def search_agent_only(internal: dict[str, Any]) -> dict[str, Any]:
    agent = {k: internal[k] for k in _SEARCH_AGENT_KEYS if k in internal}
    agent["directLowest"] = internal.get("directLowest")
    agent["transferLowest"] = internal.get("transferLowest")
    agent["selectionRequired"] = internal.get("selectionRequired")
    return agent


def parse_user_view(intent_summary: str, payload: dict[str, Any]) -> dict[str, Any]:
    legs = payload.get("searchLegs") or []
    prefs = payload.get("preferences") or {}
    trip = "往返" if len(legs) >= 2 else "单程"
    leg_rows = [
        {
            "origin": leg.get("origin"),
            "destination": leg.get("destination"),
            "depDate": leg.get("depDate"),
        }
        for leg in legs
    ]
    cabin_map = {"Y": "经济舱", "C": "商务舱", "F": "头等舱", "P": "超级经济舱"}
    cabin = cabin_map.get(str(prefs.get("cabin", "Y")).upper(), prefs.get("cabin", "Y"))
    filters: dict[str, Any] = {}
    if prefs.get("preferredCarrier"):
        filters["preferredCarrier"] = prefs["preferredCarrier"]
    if prefs.get("depTimeLabel"):
        filters["depTimeLabel"] = prefs["depTimeLabel"]
    elif prefs.get("depTimeWindow"):
        filters["depTimeWindow"] = prefs["depTimeWindow"]
    view: dict[str, Any] = {
        "intentSummary": intent_summary,
        "tripType": trip,
        "legs": leg_rows,
        "adultNum": payload.get("adultNum", 1),
        "childNum": payload.get("childNum", 0),
        "infantNum": payload.get("infantNum", 0),
        "cabin": cabin,
        "directOnly": prefs.get("stops") == 0,
    }
    if filters:
        view["searchFilters"] = filters
    return view


def verify_user_view(internal: dict[str, Any]) -> dict[str, Any]:
    user: dict[str, Any] = {
        "success": internal.get("success"),
        "totalPrice": internal.get("totalPrice"),
        "currency": internal.get("currency"),
        "passengerDisplay": internal.get("passengerDisplay"),
        "contactDisplay": internal.get("contactDisplay"),
        "orderPreview": internal.get("orderPreview"),
        "orderConfirmPrompt": internal.get("orderConfirmPrompt"),
        "requiresOrderConfirmation": internal.get("requiresOrderConfirmation"),
        "requiresResearch": internal.get("requiresResearch"),
    }
    if internal.get("verifyOfferId"):
        user["quoteId"] = internal["verifyOfferId"]
    if internal.get("success"):
        user["message"] = internal.get("orderConfirmPrompt") or internal.get("message", "")
    else:
        user["message"] = (
            internal.get("userHint") or internal.get("message") or "校验未成功"
        )
    return user


def verify_agent_only(internal: dict[str, Any]) -> dict[str, Any]:
    return {k: internal[k] for k in _VERIFY_AGENT_KEYS if k in internal}


def passengers_user_view(internal: dict[str, Any]) -> dict[str, Any]:
    return {
        "success": internal.get("success", True),
        "passengerDisplay": internal.get("passengerDisplay"),
        "contactDisplay": internal.get("contactDisplay"),
        "displayMessage": internal.get("display_message") or internal.get("message"),
        "confirmPhrase": internal.get("confirmPhrase"),
        "passengerConfirmPrompt": internal.get("passengerConfirmPrompt"),
        "message": internal.get("message") or internal.get("display_message"),
    }


def passengers_agent_only(internal: dict[str, Any]) -> dict[str, Any]:
    return {
        k: internal[k]
        for k in (
            "passengers",
            "agentContact",
            "passengerRawMappings",
            "contactRaw",
            "nextSteps",
            "code",
            "step",
            "workflowStep",
        )
        if k in internal
    }


def order_user_view(internal: dict[str, Any]) -> dict[str, Any]:
    return {
        "success": internal.get("success"),
        "orderNo": internal.get("orderNo"),
        "orderStatus": internal.get("orderStatus"),
        "partnerOrderNo": internal.get("partnerOrderNo"),
        "totalPrice": internal.get("totalPrice"),
        "currency": internal.get("currency"),
        "payDeadline": internal.get("payDeadline"),
        "message": internal.get("message"),
    }


def order_agent_only(internal: dict[str, Any]) -> dict[str, Any]:
    return {k: internal[k] for k in ("code",) if k in internal}


def wrap_envelope(
    *,
    action: str,
    status: str,
    user_view: dict[str, Any],
    agent_only: dict[str, Any] | None = None,
    message: str | None = None,
) -> dict[str, Any]:
    """统一 Skill 响应：userView 供用户展示/下载，agentOnly 仅供 Agent 续跑。"""
    msg = sanitize_user_text(message if message is not None else user_view.get("message", ""))
    uv = dict(user_view)
    if "message" in uv:
        uv["message"] = sanitize_user_text(str(uv["message"]))
    if "displayMessage" in uv:
        uv["displayMessage"] = sanitize_user_text(str(uv["displayMessage"]))
    if "passengerInfoPrompt" in uv:
        uv["passengerInfoPrompt"] = sanitize_user_text(str(uv["passengerInfoPrompt"]))
    out: dict[str, Any] = {
        "skill": SKILL_ID,
        "status": status,
        "action": action,
        "message": msg,
        "userView": uv,
    }
    if agent_only:
        out["agentOnly"] = agent_only
    return out


def failure_envelope(action: str, message: str, *, agent_only: dict[str, Any] | None = None) -> dict[str, Any]:
    return wrap_envelope(
        action=action,
        status="failure",
        user_view={"message": message},
        agent_only=agent_only,
        message=message,
    )


def wrap_config_required(action: str, envelope: dict[str, Any]) -> dict[str, Any]:
    """将 booking_config_required 转为 userView + agentOnly。"""
    data = envelope.get("data") or {}
    user_view: dict[str, Any] = {
        "message": sanitize_user_text(data.get("message") or envelope.get("message", "")),
    }
    if data.get("registerPortalUrl"):
        user_view["registerPortalUrl"] = data["registerPortalUrl"]
    agent_only = {
        k: data[k]
        for k in ("code", "step", "bookingConfigHint", "detail")
        if k in data
    }
    return wrap_envelope(
        action=action,
        status="failure",
        user_view=user_view,
        agent_only=agent_only or None,
        message=user_view["message"],
    )
