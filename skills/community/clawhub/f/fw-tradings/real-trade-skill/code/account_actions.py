"""
OpenAPI 账号错误码分派：重置 / 续期 / 联系客服。
"""

from __future__ import annotations

import sys
from pathlib import Path

_SETUP_CODE = Path(__file__).resolve().parent.parent.parent / "fosun-env-setup" / "code"
if str(_SETUP_CODE) not in sys.path:
    sys.path.insert(0, str(_SETUP_CODE))

from credential_scenarios import (
    ACTION_CONTACT_SUPPORT,
    ACTION_RENEW,
    ACTION_RESET,
    CONTACT_SUPPORT_USER_MESSAGE,
    RESET_USER_MESSAGE,
    RENEW_USER_MESSAGE,
)
from api_key_check import (
    ERR_APIKEY_DISABLED,
    ERR_APIKEY_EXPIRED,
    ERR_APIKEY_INVALID,
    ERR_APIKEY_REVOKED,
    ERR_CLIENT_KEY_MISMATCH,
    classify_api_key_error_code,
)
from ensure_fosun_env import issue_apikey_error_payload

ACTION_BY_STATUS = {
    "invalid": ACTION_RESET,
    "expired": ACTION_RENEW,
    "disabled": ACTION_CONTACT_SUPPORT,
}

_CODE_LABELS = {
    ERR_APIKEY_INVALID: "apikey 无效（不存在）",
    ERR_APIKEY_DISABLED: "apikey 已禁用",
    ERR_APIKEY_REVOKED: "apikey 已撤销",
    ERR_APIKEY_EXPIRED: "apikey 已过期",
    ERR_CLIENT_KEY_MISMATCH: "客户端密钥对不匹配",
}

_CONTACT_SUPPORT_HINT = (
    "apikey 已被禁用或撤销，skill 端无法自助恢复。"
    "用大白话告知用户联系星财富客服，不要生成二维码或尝试 TicketCreate。"
)
_CONTACT_SUPPORT_NEXT = "告知用户联系星财富客服，不要生成二维码。"


def is_apikey_error(code) -> bool:
    return classify_api_key_error_code(code) is not None


def handle_apikey_error(code, *, api_message: str = "") -> tuple[dict, int]:
    """分派 apikey 错误码，返回 (结构化 payload, exit_code)。"""
    code_int = int(code)
    status = classify_api_key_error_code(code_int)
    action = ACTION_BY_STATUS.get(status)
    if not action:
        raise ValueError(f"非 apikey 错误码: {code}")

    label = _CODE_LABELS.get(code_int, f"错误码 {code_int}")

    if action == ACTION_CONTACT_SUPPORT:
        payload = {
            "ok": False,
            "error_code": "OPENAPI_ACCOUNT_CONTACT_SUPPORT",
            "code": code_int,
            "message": api_message or label,
            "account_action": action,
            "user_message": CONTACT_SUPPORT_USER_MESSAGE,
            "hint": _CONTACT_SUPPORT_HINT,
            "next_action": _CONTACT_SUPPORT_NEXT,
        }
        return payload, 4

    payload = issue_apikey_error_payload(
        scenario=action,
        code=code_int,
        message=api_message or label,
        label=label,
    )
    if action == ACTION_RENEW:
        payload["user_message"] = RENEW_USER_MESSAGE
    else:
        payload["user_message"] = RESET_USER_MESSAGE
    return payload, 4
