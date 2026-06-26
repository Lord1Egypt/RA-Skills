"""APIKeyCheck 响应解析（无第三方依赖，便于单测）。"""

from __future__ import annotations

from typing import Any

# apikey 相关错误码（业务 API / SessionCreate 共用）
ERR_APIKEY_INVALID = 40001
ERR_APIKEY_DISABLED = 40005
ERR_APIKEY_REVOKED = 40008
ERR_APIKEY_EXPIRED = 40010
ERR_CLIENT_KEY_MISMATCH = 40015

API_KEY_ERROR_STATUS_BY_CODE = {
    ERR_APIKEY_INVALID: "invalid",
    ERR_CLIENT_KEY_MISMATCH: "invalid",
    ERR_APIKEY_DISABLED: "disabled",
    ERR_APIKEY_REVOKED: "disabled",
    ERR_APIKEY_EXPIRED: "expired",
}

# APIKeyCheck data.status：0=invalid 1=valid 2=disabled 3=expired
API_KEY_CHECK_STATUS_BY_CODE = {
    0: "invalid",
    1: "valid",
    2: "disabled",
    3: "expired",
}


def _as_bool_flag(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if not text:
        return None
    if text in {"1", "true", "active", "valid", "ok", "success"}:
        return True
    if text in {"0", "false", "inactive", "invalid", "expired", "error"}:
        return False
    return None


def coerce_api_key_check_status(value: Any) -> str | None:
    """将 APIKeyCheck 的 status 或兼容字段解析为 invalid/valid/disabled/expired。"""
    if value is None:
        return None
    if isinstance(value, bool):
        return "valid" if value else "invalid"
    if isinstance(value, (int, float)):
        return API_KEY_CHECK_STATUS_BY_CODE.get(int(value))
    text = str(value).strip().lower()
    if text in {"valid", "ok", "active", "1"}:
        return "valid"
    if text in {"invalid", "0"}:
        return "invalid"
    if text in {"disabled", "2"}:
        return "disabled"
    if text in {"expired", "3"}:
        return "expired"
    return None


def classify_api_key_error_code(code: Any) -> str | None:
    """把 API 错误码映射为 invalid/disabled/expired，无法识别返回 None。"""
    try:
        return API_KEY_ERROR_STATUS_BY_CODE.get(int(code))
    except (TypeError, ValueError):
        return None


def parse_api_key_check_status(payload: Any) -> str:
    """解析 APIKeyCheck 响应 data；无法识别时返回 unknown。"""
    if not isinstance(payload, dict):
        parsed = coerce_api_key_check_status(payload)
        return parsed or "unknown"

    if "status" in payload:
        parsed = coerce_api_key_check_status(payload.get("status"))
        if parsed:
            return parsed

    for key in ("valid", "isValid", "active", "isActive"):
        if key not in payload:
            continue
        parsed = _as_bool_flag(payload.get(key))
        if parsed is True:
            return "valid"
        if parsed is False:
            return "invalid"

    for key in ("data", "content", "result"):
        if key not in payload:
            continue
        nested = payload.get(key)
        if isinstance(nested, dict):
            parsed = parse_api_key_check_status(nested)
        else:
            parsed = coerce_api_key_check_status(nested)
            if not parsed:
                flag = _as_bool_flag(nested)
                if flag is True:
                    parsed = "valid"
                elif flag is False:
                    parsed = "invalid"
        if parsed and parsed != "unknown":
            return parsed
    return "unknown"
