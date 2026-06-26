"""export HTTP：Skill 搜索 + NewApi 校验/生单。"""
from __future__ import annotations

import gzip
import json
import secrets
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import (  # noqa: E402
    BOOKING_PATH,
    CACHE_DIR,
    CLIENT_KEY_FILE,
    CLIENT_KEY_HEADER,
    EXPORT_BASE_URL,
    FR24_API_HEADER,
    GRAY_HEADER,
    NEWAPI_AES_SECRET,
    NEWAPI_APP_KEY,
    NEWAPI_SHOPPING_PATH,
    NEWAPI_SIGN_SECRET,
    NEWAPI_SKIP_AUTH,
    NEWAPI_SKIP_IP_WHITELIST,
    PRICING_PATH,
    SHOPPING_PATH,
    USER_BOOKING_USER_MESSAGE,
    booking_required_payload,
    is_newapi_configured,
)
from newapi_auth import build_authentication, encrypt_passengers  # noqa: E402

BJ = ZoneInfo("Asia/Shanghai")
SUCCESS_CODES = frozenset({"0", "000000"})


def ensure_client_key() -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if CLIENT_KEY_FILE.exists():
        data = json.loads(CLIENT_KEY_FILE.read_text(encoding="utf-8"))
        key = data.get("clientKey", "")
        if len(key) >= 32:
            return key
    key = secrets.token_urlsafe(32)
    CLIENT_KEY_FILE.write_text(
        json.dumps(
            {"clientKey": key, "createdAt": datetime.now(BJ).isoformat()},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return key


def _decompress_response(resp) -> bytes:
    """读取 HTTP 响应体，自动解压 gzip。"""
    data = resp.read()
    if resp.headers.get("Content-Encoding") == "gzip":
        data = gzip.decompress(data)
    return data


def _http_post(url: str, body: dict, headers: dict[str, str], timeout: int = 120) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(_decompress_response(resp).decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw_bytes = e.read()
        try:
            raw_bytes = gzip.decompress(raw_bytes)
        except Exception:
            pass
        raw = raw_bytes.decode("utf-8", errors="replace")
        if raw.strip():
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                pass
        return {"code": str(e.code), "message": raw or e.reason}
    except urllib.error.URLError as e:
        return {"code": "NETWORK_ERROR", "message": f"无法连接 {EXPORT_BASE_URL}：{e.reason}"}


def skill_shopping(payload: dict) -> dict:
    """统一走 /ai/shopping：未配置密钥为演示模式；已配置则带 appkey + authentication。"""
    key = ensure_client_key()
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        CLIENT_KEY_HEADER: key,
    }
    body: dict = dict(payload)
    if is_newapi_configured():
        err = _require_newapi_secrets()
        if err:
            return {"code": "CONFIG_REQUIRED", "message": USER_BOOKING_USER_MESSAGE, "detail": err}
        headers["appkey"] = NEWAPI_APP_KEY
        headers["Accept-Encoding"] = "gzip"
        if NEWAPI_SKIP_AUTH:
            headers["fr24-skip-auth"] = "1"
        if NEWAPI_SKIP_IP_WHITELIST:
            headers[FR24_API_HEADER] = "1"
        body = _attach_auth(body)
    if GRAY_HEADER:
        headers["gray"] = GRAY_HEADER
    return _http_post(EXPORT_BASE_URL + SHOPPING_PATH, body, headers)


def run_search(payload: dict) -> tuple[dict, str]:
    """搜索始终经 Skill 接口；searchMode 仅区分是否携带采购认证。"""
    mode = "skill-auth" if is_newapi_configured() else "skill"
    return skill_shopping(payload), mode


def _newapi_headers_base() -> dict[str, str]:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "appkey": NEWAPI_APP_KEY,
        "Accept-Encoding": "gzip",
    }
    if GRAY_HEADER:
        headers["gray"] = GRAY_HEADER
    if NEWAPI_SKIP_AUTH:
        headers["fr24-skip-auth"] = "1"
    return headers


def _newapi_headers() -> dict[str, str]:
    headers = _newapi_headers_base()
    if NEWAPI_SKIP_IP_WHITELIST:
        headers[FR24_API_HEADER] = "1"
    return headers


def _newapi_channel_headers() -> dict[str, str]:
    """校验 / 生单等 NewApi 写操作请求头。"""
    headers = _newapi_headers_base()
    headers[FR24_API_HEADER] = "1"
    return headers


def _require_newapi_secrets() -> str | None:
    if NEWAPI_SKIP_AUTH:
        return None if NEWAPI_APP_KEY else "未配置 FR_NEWAPI_APPKEY"
    if not NEWAPI_APP_KEY:
        return "未配置 FR_NEWAPI_APPKEY"
    if not NEWAPI_SIGN_SECRET:
        return "未配置 FR_NEWAPI_SIGN_SECRET"
    return None


def require_booking_config(for_order: bool = False) -> str | None:
    err = _require_newapi_secrets()
    if err:
        return err
    if for_order and not NEWAPI_AES_SECRET:
        return "未配置 FR_NEWAPI_AES_SECRET（16 字节，乘客 AES）"
    return None


def _attach_auth(body: dict[str, Any]) -> dict[str, Any]:
    payload = dict(body)
    if not NEWAPI_SKIP_AUTH:
        payload["authentication"] = build_authentication(NEWAPI_APP_KEY, NEWAPI_SIGN_SECRET)
    return payload


def pricing(
    offer_id: str,
    adult_num: int = 1,
    child_num: int = 0,
    infant_num: int = 0,
    series_trace_id: str | None = None,
    series_rs_time: int | None = None,
) -> dict:
    err = require_booking_config(for_order=False)
    if err:
        out = booking_required_payload(step="verify")
        out["detail"] = err
        return out

    body: dict[str, Any] = {
        "offerId": offer_id,
        "adultNum": adult_num,
        "childNum": child_num,
        "infantNum": infant_num,
    }
    if series_trace_id:
        body["seriesTraceId"] = series_trace_id
    if series_rs_time is not None:
        body["seriesRsTime"] = series_rs_time

    return _http_post(
        EXPORT_BASE_URL + PRICING_PATH,
        _attach_auth(body),
        _newapi_channel_headers(),
    )


def booking(
    offer_id: str,
    passengers: list[dict[str, Any]],
    agent_contact: dict[str, Any],
    partner_order_no: str | None = None,
) -> dict:
    err = require_booking_config(for_order=True)
    if err:
        out = booking_required_payload(step="order")
        out["detail"] = err
        return out

    try:
        passenger_encrypt = encrypt_passengers(passengers, NEWAPI_AES_SECRET)
    except ValueError as e:
        return {"code": "CONFIG_ERROR", "message": str(e)}

    body: dict[str, Any] = {
        "offerId": offer_id,
        "passengers": passenger_encrypt,
        "agentContact": agent_contact,
    }
    if partner_order_no:
        body["partnerOrderNo"] = partner_order_no

    return _http_post(
        EXPORT_BASE_URL + BOOKING_PATH,
        _attach_auth(body),
        _newapi_channel_headers(),
        timeout=180,
    )
