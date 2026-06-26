"""预订流程引导文案与结构化选项（供 Agent / MCP 响应使用）。"""
from __future__ import annotations

from typing import Any

# 校验成功后，向用户收集乘客与联系人时展示的说明（含自然语言示例）
PASSENGER_INFO_USER_PROMPT = """生单需要每位乘客的证件信息及订单联系人。请按下面格式用自然语言发给我（可一位或多位）：

**成人示例（1 位）：**
> 乘客：张三，男，1990年1月15日出生，护照 E12345678，2030年12月31日到期，中国籍。
> 联系人：张三，手机 13800138000，邮箱 zhangsan@example.com

**机票英文姓名示例（与证件一致时）：**
> 乘客：张三，男，1990-01-15，护照 E12345678，2030-12-31 到期，国籍 CN（机票姓名 ZHANG/SAN）。
> 联系人：张三，手机 +86 13800138000，邮箱 zhangsan@example.com

**成人+儿童示例：**
> 成人：张三，男，1988-03-20，护照 G12345678，2031-06-30 到期，中国籍。
> 儿童：张小三，男，2018-06-01，护照 G87654321，2031-06-30 到期，中国籍，与成人张三同行。
> 联系人：张三，13800138000，zhangsan@example.com

**字段说明（缺一会无法生单）：**
- 乘客：姓名（中文或姓/名）、性别（男/女）、出生日期、证件类型（默认护照）、证件号、证件有效期、国籍
- 联系人：姓名、手机号（建议含区号 86）、邮箱"""

PASSENGER_INFO_EXAMPLES: list[str] = [
    "乘客：张三，男，1990年1月15日出生，护照 E12345678，2030年12月31日到期，中国籍。"
    "联系人：张三，手机 13800138000，邮箱 zhangsan@example.com",
    "乘客：张三，男，1990-01-15，护照 E12345678，2030-12-31 到期，国籍 CN。"
    "联系人：张三，手机 +86 13800138000，zhangsan@example.com",
    "成人：张三，男，1988-03-20，护照 G12345678，2031-06-30 到期，中国籍。"
    "儿童：张小三，男，2018-06-01，护照 G87654321，2031-06-30 到期，中国籍。"
    "联系人：张三，13800138000，zhangsan@example.com",
]

BOOKING_SELECTION_USER_PROMPT = (
    "当前有不止一条可订报价，请先告诉我您要订哪一条，再核对乘客信息：\n"
    "回复「直飞」或「中转」，或说明航班号（如 HO1832）。"
)

# 标准预订顺序（Agent 必须遵守）
BOOKING_WORKFLOW_STEPS = [
    "skill_search_client.py search → 展示报价；多条时用户选择直飞/中转",
    "skill_booking_client.py parse-passengers → 展示字段对照表",
    "用户回复「乘客信息确认无误」→ skill_booking_client.py verify --passenger-confirmed",
    "校验成功 → 展示 orderPreview → 用户回复「确认生单」",
    "skill_booking_client.py order --user-confirmed",
]

PASSENGER_CONFIRM_PHRASE = "乘客信息确认无误"
ORDER_CONFIRM_PHRASE = "确认生单"

# export ResponseCode.VERIFY_INCONSISTENT_IDENTITIES
VERIFY_INCONSISTENT_IDENTITIES_CODE = "304016"
VERIFY_INCONSISTENT_IDENTITIES_CODES = frozenset({"304016", "000304016"})

VERIFY_IDENTITY_MISMATCH_USER_MESSAGE = (
    "校验失败：当前报价与采购身份不一致。\n"
    "若您刚刚在本机配置了新的采购 APPKEY，需要先用新身份重新搜索航班，"
    "确认新的直飞/中转报价后，再核对乘客信息并重新校验。"
)

VERIFY_IDENTITY_MISMATCH_AGENT_STEPS = [
    "提示用户：新 APPKEY 生效后必须重新 search（不可沿用旧 booking_context 的 offerId）",
    "可选：nl_to_search.py parse → 用户确认 → skill_search_client.py search --selection ...",
    "用户选定报价后：parse-passengers → verify --passenger-confirmed",
]


def is_verify_identity_mismatch(code: str, message: str | None = None) -> bool:
    raw = str(code or "").strip()
    if raw in VERIFY_INCONSISTENT_IDENTITIES_CODES:
        return True
    if raw.isdigit() and int(raw) == 304016:
        return True
    msg = message or ""
    return "304016" in raw or (
        "身份不一致" in msg and ("校验" in msg or "Verification failed" in msg)
    )


def verify_identity_mismatch_payload() -> dict[str, Any]:
    return {
        "code": VERIFY_INCONSISTENT_IDENTITIES_CODE,
        "success": False,
        "step": "verify",
        "workflowStep": 3,
        "requiresResearch": True,
        "researchRequired": True,
        "message": VERIFY_IDENTITY_MISMATCH_USER_MESSAGE,
        "userHint": VERIFY_IDENTITY_MISMATCH_USER_MESSAGE,
        "nextSteps": VERIFY_IDENTITY_MISMATCH_AGENT_STEPS,
    }

PASSENGER_CONFIRM_USER_PROMPT = (
    "请核对上方乘客字段对照（姓名拼音、性别、证件等）。\n"
    f"若无误请回复「{PASSENGER_CONFIRM_PHRASE}」，将为您调用校验接口锁价。"
)

ORDER_CONFIRM_USER_PROMPT = (
    "请核对行程、退改规则与乘客/联系人信息。\n"
    f"若无误请回复「{ORDER_CONFIRM_PHRASE}」，将提交生单（创建真实订单）。"
)


def build_booking_choice(offer: dict[str, Any] | None, key: str, label: str) -> dict[str, Any] | None:
    if not offer or not offer.get("offerId"):
        return None
    return {
        "key": key,
        "label": label,
        "offerId": str(offer["offerId"]) if offer.get("offerId") is not None else None,
        "route": offer.get("route"),
        "flights": offer.get("flights"),
        "totalPrice": offer.get("totalPrice"),
        "currency": offer.get("currency"),
        "flightCategory": offer.get("flightCategory"),
    }


def build_booking_choices(
    direct: dict[str, Any] | None,
    transfer: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    choices: list[dict[str, Any]] = []
    d = build_booking_choice(direct, "direct", "直飞最低")
    t = build_booking_choice(transfer, "transfer", "中转最低")
    if d:
        choices.append(d)
    if t:
        choices.append(t)
    return choices


def selection_required(choices: list[dict[str, Any]]) -> bool:
    return len(choices) > 1


def passenger_required_payload(*, verify_offer_id: str | None = None) -> dict[str, Any]:
    """未提供 passengers 时返回，引导用户用自然语言补充。"""
    out: dict[str, Any] = {
        "code": "PASSENGER_INFO_REQUIRED",
        "success": False,
        "step": "order",
        "message": "生单前请提供乘客与联系人信息（见下方示例）。",
        "passengerInfoPrompt": PASSENGER_INFO_USER_PROMPT,
        "passengerInfoExamples": PASSENGER_INFO_EXAMPLES,
        "nextSteps": BOOKING_WORKFLOW_STEPS,
    }
    if verify_offer_id:
        out["verifyOfferId"] = verify_offer_id
    return out


def selection_required_payload(choices: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "code": "BOOKING_SELECTION_REQUIRED",
        "success": False,
        "step": "verify",
        "message": BOOKING_SELECTION_USER_PROMPT,
        "bookingChoices": choices,
        "selectionRequired": True,
        "nextSteps": [
            "用户明确选择 direct 或 transfer",
            "parse-passengers → 用户确认乘客 → verify --passenger-confirmed → order --user-confirmed",
        ],
    }


def passenger_confirmation_required_payload(
    *,
    passenger_display: list[dict[str, Any]],
    contact_display: dict[str, Any],
    display_message: str,
) -> dict[str, Any]:
    return {
        "code": "PASSENGER_CONFIRMATION_REQUIRED",
        "success": False,
        "step": "passenger_preview",
        "workflowStep": 2,
        "message": display_message,
        "passengerDisplay": passenger_display,
        "contactDisplay": contact_display,
        "confirmPhrase": PASSENGER_CONFIRM_PHRASE,
        "passengerConfirmPrompt": PASSENGER_CONFIRM_USER_PROMPT,
        "nextSteps": [
            f"等待用户回复「{PASSENGER_CONFIRM_PHRASE}」",
            "再执行 skill_booking_client.py verify --passenger-confirmed --passengers-file ...",
        ],
    }


def passenger_not_confirmed_payload() -> dict[str, Any]:
    return {
        "code": "PASSENGER_NOT_CONFIRMED",
        "success": False,
        "step": "verify",
        "message": f"请先完成乘客核对：执行 parse-passengers 并由用户回复「{PASSENGER_CONFIRM_PHRASE}」。",
        "passengerConfirmPrompt": PASSENGER_CONFIRM_USER_PROMPT,
        "workflowStep": 2,
    }


def order_confirmation_required_payload(
    *,
    verify_offer_id: str,
    itinerary: dict[str, Any],
    passenger_display: list[dict[str, Any]],
    contact_display: dict[str, Any],
    passengers: list[dict[str, Any]],
    agent_contact: dict[str, str],
    total_price: Any,
    currency: str,
) -> dict[str, Any]:
    return {
        "code": "ORDER_CONFIRMATION_REQUIRED",
        "success": False,
        "step": "order_preview",
        "workflowStep": 4,
        "verifyOfferId": verify_offer_id,
        "itinerary": itinerary,
        "passengerDisplay": passenger_display,
        "contactDisplay": contact_display,
        "passengers": passengers,
        "agentContact": agent_contact,
        "totalPrice": total_price,
        "currency": currency,
        "confirmPhrase": ORDER_CONFIRM_PHRASE,
        "orderConfirmPrompt": ORDER_CONFIRM_USER_PROMPT,
        "message": ORDER_CONFIRM_USER_PROMPT,
        "nextSteps": [
            f"等待用户回复「{ORDER_CONFIRM_PHRASE}」",
            "再执行 skill_booking_client.py order --user-confirmed ...",
        ],
    }


def order_not_confirmed_payload(*, verify_offer_id: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {
        "code": "ORDER_NOT_CONFIRMED",
        "success": False,
        "step": "order",
        "message": f"请先向用户展示校验结果与行程退改，待用户回复「{ORDER_CONFIRM_PHRASE}」后再生单。",
        "orderConfirmPrompt": ORDER_CONFIRM_USER_PROMPT,
        "workflowStep": 4,
    }
    if verify_offer_id:
        out["verifyOfferId"] = verify_offer_id
    return out


def build_itinerary_preview(
    *,
    selected_offer: dict[str, Any] | None,
    verify_offer: dict[str, Any] | None,
    total_price: Any,
    currency: str,
) -> dict[str, Any]:
    """合并搜索摘要与校验报价，供用户最终确认。"""
    base = selected_offer or {}
    verify = verify_offer or {}
    return {
        "route": base.get("route") or verify.get("route"),
        "flights": base.get("flights"),
        "segments": base.get("segments") or [],
        "refundChange": base.get("refundChange") or _rules_brief(verify.get("rules")),
        "baggage": base.get("baggage"),
        "totalPrice": total_price,
        "currency": currency,
        "platingCarrier": base.get("platingCarrier") or verify.get("platingCarrier"),
        "flightCategoryLabel": base.get("label") or base.get("flightCategoryLabel"),
    }


def _rules_brief(rules: dict | None) -> dict[str, str]:
    if not rules:
        return {"refundText": "见订单详情", "changeText": "见订单详情"}
    refunds = rules.get("refund") or []
    changes = rules.get("change") or []
    return {
        "refundText": str(refunds[0].get("refundPolicy", "见详情")) if refunds else "见详情",
        "changeText": str(changes[0].get("changePolicy", "见详情")) if changes else "见详情",
    }
