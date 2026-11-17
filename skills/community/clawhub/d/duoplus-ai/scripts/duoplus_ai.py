#!/usr/bin/env python3
"""DuoPlus cloud-phone lifecycle and HTTP Gateway client.

Only an API key supplied by the user is required. Pass it with --api-key for
the current invocation or provide DUOPLUS_API_KEY. Optional environment
variables provide deployment overrides without changing the skill:

  DUOPLUS_API_BASE
  DUOPLUS_GATEWAY_TOKEN
  DUOPLUS_GATEWAY_URL_TEMPLATE
  DUOPLUS_REGION
  DUOPLUS_CLOUD_IP
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# Default to DuoPlus' official global production OpenAPI. Mainland production
# deployments can override this with DUOPLUS_API_BASE or --api-base.
DEFAULT_API_BASE = "https://openapi.duoplus.net"
DEFAULT_GATEWAY_TEMPLATE = "https://agent-gateway.duoplus.net/agent-command"
PHONE_STATUS = {
    0: "proxy_not_configured",
    1: "running",
    2: "stopped",
    3: "expired",
    4: "expired_pending_renewal",
    10: "starting",
    11: "configuring",
    12: "configuration_failed",
}
RETRYABLE_HTTP = {408, 425, 429, 500, 502, 503, 504}


class DuoPlusError(RuntimeError):
    """An expected API, routing, validation, or automation failure."""

    def __init__(
        self,
        message: str,
        request: Optional[Dict[str, Any]] = None,
        response: Optional[Dict[str, Any]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.request = request
        self.response = response
        self.details = details

    def as_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"ok": False, "error": str(self)}
        if self.request is not None:
            result["request"] = self.request
        if self.response is not None:
            result["response"] = self.response
        if self.details is not None:
            result["details"] = self.details
        return result


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def _json_bytes(value: Dict[str, Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _redact(value: Any, key: str = "") -> Any:
    normalized = key.lower().replace("-", "_")
    if normalized in {
        "authorization",
        "duoplus_api_key",
        "api_key",
        "apikey",
        "password",
        "passwd",
        "secret",
        "token",
        "access_token",
        "refresh_token",
    }:
        if value in (None, ""):
            return value
        text = str(value)
        if normalized == "authorization" and text.lower().startswith("bearer "):
            text = text[7:]
        return f"<redacted:{len(text)}>"
    if isinstance(value, dict):
        return {str(item_key): _redact(item_value, str(item_key)) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def _request_context(
    url: str, headers: Dict[str, str], payload: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "method": "POST",
        "url": url,
        "headers": _redact(headers),
        "body": _redact(payload),
    }


def _decode_json(raw: bytes, source: str) -> Dict[str, Any]:
    try:
        decoded = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        snippet = raw[:240].decode("utf-8", errors="replace")
        raise DuoPlusError(f"{source} returned invalid JSON: {snippet}") from exc
    if not isinstance(decoded, dict):
        raise DuoPlusError(f"{source} returned a non-object JSON response")
    return _repair_mojibake(decoded)


def _repair_mojibake(value: Any) -> Any:
    """Repair legacy API messages containing GBK bytes serialized as Latin-1 text."""
    if isinstance(value, dict):
        return {key: _repair_mojibake(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_repair_mojibake(item) for item in value]
    if not isinstance(value, str) or not any(0x80 <= ord(char) <= 0xFF for char in value):
        return value
    try:
        candidate = value.encode("latin-1").decode("gb18030")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value
    original_cjk = sum("\u3400" <= char <= "\u9fff" for char in value)
    candidate_cjk = sum("\u3400" <= char <= "\u9fff" for char in candidate)
    return candidate if candidate_cjk > original_cjk else value


def _emit(value: Any) -> None:
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def _parse_json_object(value: str, label: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise DuoPlusError(f"{label} must be valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise DuoPlusError(f"{label} must be a JSON object")
    return parsed


def _status_number(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise DuoPlusError(f"invalid cloud-phone status: {value!r}") from exc


def _status_view(item: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(item)
    status = _status_number(item.get("status"))
    result["status"] = status
    result["status_name"] = PHONE_STATUS.get(status, "unknown")
    return result


def _ai_control_supported(item: Dict[str, Any]) -> bool:
    try:
        return int(item.get("http_status")) == 1
    except (TypeError, ValueError):
        return False


def _phone_view(item: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(item)
    if "status" in result:
        result = _status_view(result)
    supported = _ai_control_supported(result)
    result["ai_control_supported"] = supported
    if supported:
        result["ai_control_status"] = "supported"
        result["ai_control_message"] = "AI HTTP control is supported"
    elif result.get("http_status") in (0, "0"):
        result["ai_control_status"] = "unsupported"
        result["ai_control_message"] = "This cloud phone does not support AI HTTP control"
    else:
        result["ai_control_status"] = "unknown"
        result["ai_control_message"] = "AI HTTP control support has not been confirmed for this cloud phone"
    return result


def _ai_support_summary(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "http_status": item.get("http_status"),
        "ai_control_supported": item.get("ai_control_supported"),
        "ai_control_status": item.get("ai_control_status"),
        "ai_control_message": item.get("ai_control_message"),
    }


def _decorate_phone_response(response: Dict[str, Any]) -> Dict[str, Any]:
    data = response.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("list"), list):
        raise DuoPlusError("DuoPlus response is missing data.list")
    phones = [_phone_view(item) for item in data["list"] if isinstance(item, dict)]
    # Python's sort is stable, so the server order is preserved within each group.
    phones.sort(key=lambda item: 0 if item["ai_control_supported"] else 1)
    data["list"] = phones
    data["ai_control_supported_count"] = sum(
        1 for item in phones if item["ai_control_supported"]
    )
    data["ai_control_unsupported_count"] = sum(
        1 for item in phones if not item["ai_control_supported"]
    )
    return response


def _extract_list(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = response.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("list"), list):
        raise DuoPlusError("DuoPlus response is missing data.list")
    return [item for item in data["list"] if isinstance(item, dict)]


def _normalize_region(value: Any) -> Optional[str]:
    if value is None:
        return None
    raw = str(value).strip().lower()
    if not raw:
        return None
    compact = re.sub(r"[^a-z0-9]+", "", raw)
    direct = re.search(
        r"(?:^|[^a-z])(hk|sg|us|jp|kr|tw|gb|uk|de|fr|nl|ca|au|my|th|vn|id|ph|br|mx|ae|sa|in)(\d+)?(?:$|[^a-z0-9])",
        raw,
    )
    if direct:
        code = "gb" if direct.group(1) == "uk" else direct.group(1)
        return code + (direct.group(2) or "")
    compact_direct = re.fullmatch(
        r"(hk|sg|us|jp|kr|tw|gb|uk|de|fr|nl|ca|au|my|th|vn|id|ph|br|mx|ae|sa|in)(\d+)?",
        compact,
    )
    if compact_direct:
        code = "gb" if compact_direct.group(1) == "uk" else compact_direct.group(1)
        return code + (compact_direct.group(2) or "")

    aliases = (
        (("hongkong", "hong kong", "\u9999\u6e2f"), "hk"),
        (("singapore", "\u65b0\u52a0\u5761"), "sg"),
        (("unitedstates", "united states", "\u7f8e\u56fd"), "us"),
        (("japan", "\u65e5\u672c"), "jp"),
        (("southkorea", "south korea", "\u97e9\u56fd"), "kr"),
        (("taiwan", "\u53f0\u6e7e"), "tw"),
        (("unitedkingdom", "united kingdom", "\u82f1\u56fd"), "gb"),
        (("germany", "\u5fb7\u56fd"), "de"),
        (("france", "\u6cd5\u56fd"), "fr"),
        (("netherlands", "\u8377\u5170"), "nl"),
        (("canada", "\u52a0\u62ff\u5927"), "ca"),
        (("australia", "\u6fb3\u5927\u5229\u4e9a"), "au"),
        (("malaysia", "\u9a6c\u6765\u897f\u4e9a"), "my"),
        (("thailand", "\u6cf0\u56fd"), "th"),
        (("vietnam", "\u8d8a\u5357"), "vn"),
        (("indonesia", "\u5370\u5ea6\u5c3c\u897f\u4e9a"), "id"),
        (("philippines", "\u83f2\u5f8b\u5bbe"), "ph"),
        (("india", "\u5370\u5ea6"), "in"),
    )
    chinese_numbers = {
        "\u4e00": "1", "\u4e8c": "2", "\u4e09": "3", "\u56db": "4", "\u4e94": "5"
    }
    suffix_match = re.search(r"(\d+)", raw)
    suffix = suffix_match.group(1) if suffix_match else ""
    if not suffix:
        for chinese, number in chinese_numbers.items():
            if chinese in raw:
                suffix = number
                break
    for names, code in aliases:
        if any(name in raw or name.replace(" ", "") in compact for name in names):
            return code + suffix
    return None


class DuoPlusClient:
    def __init__(
        self,
        api_key: str,
        api_base: str,
        lang: str,
        timeout: float,
        region: Optional[str],
        cloud_ip: Optional[str],
        gateway_template: str,
        gateway_token: Optional[str],
    ) -> None:
        if not api_key:
            raise DuoPlusError(
                "API key is required. Ask the user to provide it directly, then pass it "
                "with --api-key for the current invocation."
            )
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.lang = lang
        self.timeout = timeout
        self.region_override = region
        self.cloud_ip_override = cloud_ip
        self.gateway_template = gateway_template
        self.gateway_token = gateway_token or api_key
        self._last_control_request = 0.0

    def _pace_control_api(self) -> None:
        # Official limit is 1 QPS per endpoint. A small margin avoids boundary bursts.
        wait = 1.05 - (time.monotonic() - self._last_control_request)
        if wait > 0:
            time.sleep(wait)
        self._last_control_request = time.monotonic()

    def _post(
        self,
        url: str,
        headers: Dict[str, str],
        payload: Dict[str, Any],
        timeout: Optional[float] = None,
        retries: int = 2,
        control_api: bool = False,
    ) -> Tuple[int, Dict[str, Any]]:
        raw_payload = _json_bytes(payload)
        request_context = _request_context(url, headers, payload)
        for attempt in range(retries + 1):
            if control_api:
                self._pace_control_api()
            request = Request(url, data=raw_payload, headers=headers, method="POST")
            try:
                with urlopen(request, timeout=timeout or self.timeout) as response:
                    status = int(response.status)
                    body = response.read()
                try:
                    decoded = _decode_json(body, url)
                except DuoPlusError as exc:
                    raise DuoPlusError(
                        str(exc),
                        request=request_context,
                        response={
                            "http_status": status,
                            "body": body[:1000].decode("utf-8", errors="replace"),
                        },
                    ) from exc
                return status, decoded
            except HTTPError as exc:
                body = exc.read()
                parsed: Dict[str, Any]
                try:
                    parsed = _decode_json(body, url)
                except DuoPlusError:
                    parsed = {"message": body[:240].decode("utf-8", errors="replace")}
                if exc.code in RETRYABLE_HTTP and attempt < retries:
                    time.sleep(max(1.05, 2**attempt))
                    continue
                message = parsed.get("message") or parsed.get("error") or "HTTP error"
                raise DuoPlusError(
                    f"HTTP {exc.code} from {url}: {message}",
                    request=request_context,
                    response={"http_status": int(exc.code), "body": _redact(parsed)},
                ) from exc
            except (URLError, TimeoutError, OSError) as exc:
                if attempt < retries:
                    time.sleep(max(1.05, 2**attempt))
                    continue
                raise DuoPlusError(
                    f"request failed for {url}: {exc}",
                    request=request_context,
                    response={"transport_error": str(exc)},
                ) from exc
        raise AssertionError("unreachable")

    def control(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = self.api_base + path
        headers = {
            "Content-Type": "application/json",
            "Lang": self.lang,
            "DuoPlus-API-Key": self.api_key,
        }
        http_status, response = self._post(
            url,
            headers,
            payload,
            control_api=True,
        )
        try:
            code = int(response.get("code"))
        except (TypeError, ValueError) as exc:
            raise DuoPlusError("DuoPlus response is missing a numeric code") from exc
        if code != 200:
            raise DuoPlusError(
                f"DuoPlus API error {code}: {response.get('message', 'unknown error')}",
                request=_request_context(url, headers, payload),
                response={"http_status": http_status, "body": _redact(response)},
            )
        return response

    def phones(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        return self.control("/api/v1/cloudPhone/list", filters)

    def all_phones(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        request = dict(filters)
        request["page"] = 1
        request["pagesize"] = min(100, max(1, int(request.get("pagesize", 100))))
        response = self.phones(request)
        data = response.get("data")
        if not isinstance(data, dict) or not isinstance(data.get("list"), list):
            raise DuoPlusError("DuoPlus response is missing data.list")
        merged = list(data["list"])
        try:
            total_pages = max(1, int(data.get("total_page", 1)))
        except (TypeError, ValueError):
            total_pages = 1
        for page in range(2, total_pages + 1):
            request["page"] = page
            page_response = self.phones(request)
            merged.extend(_extract_list(page_response))
        data["list"] = merged
        data["page"] = 1
        data["pagesize"] = len(merged)
        data["source_total_page"] = total_pages
        data["fetched_all"] = True
        return response

    def phone(self, image_id: str) -> Dict[str, Any]:
        response = self.phones({"image_id": [image_id], "page": 1, "pagesize": 100})
        for item in _extract_list(response):
            if str(item.get("id")) == image_id:
                return item
        raise DuoPlusError(f"cloud phone not found: {image_id}")

    def ai_support(self, image_ids: Iterable[str]) -> Dict[str, Any]:
        requested = [str(image_id) for image_id in image_ids]
        response = self.phones(
            {"image_id": requested, "page": 1, "pagesize": min(100, len(requested) or 1)}
        )
        by_id = {
            str(item.get("id")): _phone_view(item) for item in _extract_list(response)
        }
        supported: List[Dict[str, Any]] = []
        unsupported: List[Dict[str, Any]] = []
        missing: List[str] = []
        for image_id in requested:
            phone = by_id.get(image_id)
            if phone is None:
                missing.append(image_id)
            elif phone["ai_control_supported"]:
                supported.append(_ai_support_summary(phone))
            else:
                unsupported.append(_ai_support_summary(phone))
        return {
            "all_supported": not unsupported and not missing,
            "supported": supported,
            "unsupported": unsupported,
            "missing": missing,
        }

    def require_ai_support(
        self, image_ids: Iterable[str], allow_unsupported: bool = False
    ) -> Dict[str, Any]:
        support = self.ai_support(image_ids)
        if support["missing"]:
            raise DuoPlusError(
                "one or more cloud phones were not found",
                details={"missing": support["missing"]},
            )
        if support["unsupported"] and not allow_unsupported:
            unsupported = [
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "http_status": item.get("http_status"),
                    "message": item.get("ai_control_message"),
                }
                for item in support["unsupported"]
            ]
            raise DuoPlusError(
                "This cloud phone does not support AI cloud-phone automation",
                details={
                    "unsupported_phones": unsupported,
                    "hint": (
                        "Select a phone with http_status=1. For power-on only, "
                        "explicitly confirm and use --allow-no-ai."
                    ),
                },
            )
        return support

    def statuses(self, image_ids: Iterable[str]) -> Dict[str, Any]:
        response = self.control(
            "/api/v1/cloudPhone/status", {"image_ids": list(image_ids)}
        )
        data = response.get("data")
        if isinstance(data, dict) and isinstance(data.get("list"), list):
            data["list"] = [
                _status_view(item) if isinstance(item, dict) else item
                for item in data["list"]
            ]
        return response

    def status(self, image_id: str) -> Dict[str, Any]:
        items = _extract_list(self.statuses([image_id]))
        for item in items:
            if str(item.get("id")) == image_id:
                return item
        raise DuoPlusError(f"status missing for cloud phone: {image_id}")

    def info(self, image_id: str) -> Dict[str, Any]:
        return self.control("/api/v1/cloudPhone/info", {"image_id": image_id})

    def platform_shell(self, image_id: str, command: str) -> Dict[str, Any]:
        normalized = command.strip()
        if not normalized:
            raise DuoPlusError("platform shell command must not be empty")
        if normalized.lower().startswith("adb shell "):
            raise DuoPlusError(
                "platform shell command must not include the 'adb shell' prefix"
            )
        response = self.control(
            "/api/v1/cloudPhone/command",
            {"image_id": image_id, "command": normalized},
        )
        data = response.get("data")
        if not isinstance(data, dict):
            raise DuoPlusError(
                "platform shell response is missing data",
                response={"body": _redact(response)},
            )
        if data.get("success") is not True:
            message = data.get("message") or "platform shell command failed"
            raise DuoPlusError(
                str(message),
                response={"body": _redact(response)},
            )
        result = dict(response)
        result["execution_route"] = "platform_openapi_fallback"
        return result

    def lifecycle(self, operation: str, image_ids: List[str]) -> Dict[str, Any]:
        paths = {
            "power-on": ("/api/v1/cloudPhone/powerOn", 100),
            "power-off": ("/api/v1/cloudPhone/powerOff", 20),
            "restart": ("/api/v1/cloudPhone/restart", 20),
        }
        path, maximum = paths[operation]
        if not image_ids:
            raise DuoPlusError("at least one cloud-phone ID is required")
        if len(image_ids) > maximum:
            raise DuoPlusError(f"{operation} supports at most {maximum} cloud phones per call")
        return self.control(path, {"image_ids": image_ids})

    def wait_for_status(
        self,
        image_ids: List[str],
        target: int,
        timeout: float,
        poll: float,
    ) -> Dict[str, Any]:
        deadline = time.monotonic() + timeout
        latest: Dict[str, Dict[str, Any]] = {}
        while True:
            response = self.statuses(image_ids)
            latest = {
                str(item.get("id")): item for item in _extract_list(response)
            }
            if all(
                image_id in latest
                and _status_number(latest[image_id].get("status")) == target
                for image_id in image_ids
            ):
                return {
                    "ready": True,
                    "target_status": target,
                    "target_status_name": PHONE_STATUS.get(target, "unknown"),
                    "phones": [latest[image_id] for image_id in image_ids],
                }
            terminal_errors = {
                image_id: latest[image_id]
                for image_id in image_ids
                if image_id in latest
                and _status_number(latest[image_id].get("status")) in {3, 4, 12}
            }
            if terminal_errors:
                raise DuoPlusError(
                    "cloud phone entered a non-recoverable state: "
                    + json.dumps(terminal_errors, ensure_ascii=False)
                )
            if time.monotonic() >= deadline:
                raise DuoPlusError(
                    "timed out waiting for cloud-phone status "
                    f"{target}: {json.dumps(latest, ensure_ascii=False)}"
                )
            time.sleep(max(1.1, poll))

    def wait_until_status_leaves(
        self,
        image_id: str,
        waiting: Iterable[int],
        timeout: float,
        poll: float,
    ) -> Dict[str, Any]:
        waiting_set = set(waiting)
        deadline = time.monotonic() + timeout
        while True:
            current = _status_view(self.status(image_id))
            status = _status_number(current["status"])
            if status not in waiting_set:
                return current
            if time.monotonic() >= deadline:
                raise DuoPlusError(
                    f"timed out waiting for {image_id} to leave states {sorted(waiting_set)}"
                )
            time.sleep(max(1.1, poll))

    def wait_for_restart(
        self, image_ids: List[str], timeout: float, poll: float
    ) -> Dict[str, Any]:
        deadline = time.monotonic() + timeout
        transitioned = {image_id: False for image_id in image_ids}
        latest: Dict[str, Dict[str, Any]] = {}
        # Avoid accepting the still-running pre-restart state immediately.
        time.sleep(max(1.1, poll))
        while True:
            response = self.statuses(image_ids)
            latest = {
                str(item.get("id")): item for item in _extract_list(response)
            }
            for image_id in image_ids:
                if image_id in latest and _status_number(latest[image_id].get("status")) != 1:
                    transitioned[image_id] = True
            if all(
                transitioned[image_id]
                and image_id in latest
                and _status_number(latest[image_id].get("status")) == 1
                for image_id in image_ids
            ):
                return {
                    "ready": True,
                    "restart_transition_observed": True,
                    "phones": [latest[image_id] for image_id in image_ids],
                }
            terminal_errors = {
                image_id: latest[image_id]
                for image_id in image_ids
                if image_id in latest
                and _status_number(latest[image_id].get("status")) in {3, 4, 12}
            }
            if terminal_errors:
                raise DuoPlusError(
                    "cloud phone entered a non-recoverable state during restart: "
                    + json.dumps(terminal_errors, ensure_ascii=False)
                )
            if time.monotonic() >= deadline:
                raise DuoPlusError(
                    "timed out waiting for restart transition: "
                    + json.dumps(latest, ensure_ascii=False)
                )
            time.sleep(max(1.1, poll))

    def route(self, image_id: str) -> Dict[str, Any]:
        phone = self.phone(image_id)
        phone_view = _phone_view(phone)
        if not phone_view["ai_control_supported"]:
            raise DuoPlusError(
                "This cloud phone does not support AI cloud-phone automation",
                details={
                    "image_id": image_id,
                    "http_status": phone.get("http_status"),
                    "message": phone_view["ai_control_message"],
                },
            )
        cloud_ip = self.cloud_ip_override
        if not cloud_ip:
            for key in ("cloud_ip", "cloudIp", "ip", "inner_ip", "private_ip"):
                if phone.get(key):
                    cloud_ip = str(phone[key]).strip()
                    break
        region = _normalize_region(self.region_override)
        if not region:
            for key in (
                "gateway_region",
                "region_code",
                "region",
                "area_code",
                "area",
            ):
                region = _normalize_region(phone.get(key))
                if region:
                    break
        if not cloud_ip:
            raise DuoPlusError(
                "cloud-phone list did not return an IP; set DUOPLUS_CLOUD_IP as a deployment override"
            )
        if not region:
            raise DuoPlusError(
                "cloud-phone list did not return a recognizable region; "
                "set DUOPLUS_REGION as a deployment override"
            )
        try:
            url = self.gateway_template.format(
                region=region, cloud_ip=cloud_ip, image_id=image_id
            )
        except KeyError as exc:
            raise DuoPlusError(f"invalid gateway URL template placeholder: {exc}") from exc
        return {
            "image_id": image_id,
            "region": region,
            "cloud_ip": cloud_ip,
            "url": url,
            "http_status": phone.get("http_status"),
            "ai_control_supported": True,
        }

    def gateway(
        self,
        image_id: str,
        payload: Dict[str, Any],
        timeout: Optional[float] = None,
        retries: int = 1,
    ) -> Dict[str, Any]:
        route = self.route(image_id)
        _, response = self._post(
            route["url"],
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.gateway_token}",
                "Region": route["region"],
                "CloudIP": route["cloud_ip"],
            },
            payload,
            timeout=timeout,
            retries=retries,
        )
        return response

    def wait_gateway_ready(
        self, image_id: str, timeout: float, poll: float
    ) -> Dict[str, Any]:
        deadline = time.monotonic() + timeout
        last_error = "not attempted"
        while time.monotonic() < deadline:
            try:
                response = self.gateway(
                    image_id, {"operation": "ready"}, timeout=min(self.timeout, 15), retries=0
                )
                if response.get("executor") == "ready" or response.get("ready") is True:
                    return response
                last_error = json.dumps(response, ensure_ascii=False)
            except DuoPlusError as exc:
                last_error = str(exc)
                if "HTTP 401" in last_error:
                    raise
            time.sleep(max(1.0, poll))
        raise DuoPlusError(f"HTTP Gateway did not become ready: {last_error}")

    def ensure_ready(
        self,
        image_id: str,
        power_on: bool,
        phone_timeout: float,
        gateway_timeout: float,
        poll: float,
    ) -> Dict[str, Any]:
        ai_support = self.require_ai_support([image_id])
        initial = _status_view(self.status(image_id))
        initial_status = _status_number(initial["status"])
        powered_on_by_client = False
        if initial_status == 0:
            raise DuoPlusError("cloud phone has no proxy; initialize a proxy before power-on")
        if initial_status in {3, 4, 12}:
            raise DuoPlusError(
                f"cloud phone cannot be started from state {PHONE_STATUS.get(initial_status)}"
            )
        current_status = initial_status
        if current_status == 11:
            configured = self.wait_until_status_leaves(
                image_id, waiting={11}, timeout=phone_timeout, poll=poll
            )
            current_status = _status_number(configured["status"])
        if current_status == 2:
            if not power_on:
                raise DuoPlusError("cloud phone is stopped; rerun without --no-power-on")
            power_response = self.lifecycle("power-on", [image_id])
            accepted = power_response.get("data", {}).get("success", [])
            if isinstance(accepted, list) and image_id not in [str(item) for item in accepted]:
                raise DuoPlusError(
                    "power-on was not accepted: "
                    + json.dumps(power_response.get("data"), ensure_ascii=False)
                )
            powered_on_by_client = True
            current_status = 10
        if current_status != 1:
            phone_state = self.wait_for_status(
                [image_id], target=1, timeout=phone_timeout, poll=poll
            )
        else:
            phone_state = {
                "ready": True,
                "phones": [initial],
                "target_status": 1,
                "target_status_name": "running",
            }
        gateway_state = self.wait_gateway_ready(image_id, gateway_timeout, poll)
        return {
            "ready": True,
            "image_id": image_id,
            "initial_status": initial_status,
            "initial_status_name": PHONE_STATUS.get(initial_status, "unknown"),
            "powered_on_by_client": powered_on_by_client,
            "phone": phone_state,
            "gateway": gateway_state,
            "route": self.route(image_id),
            "ai_control": ai_support,
        }


def _command_ids(prefix: str) -> Tuple[str, str]:
    suffix = f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"
    return f"{prefix}-{suffix}", f"{prefix}-task-{suffix}"


def _save_screenshot(value: str, output: str) -> str:
    encoded = value
    if value.startswith("data:"):
        _, encoded = value.split(",", 1)
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise DuoPlusError("Gateway screenshot is not valid base64") from exc
    path = Path(output).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return str(path)


def _summarize_gateway_result(
    response: Dict[str, Any], screenshot_out: Optional[str]
) -> Dict[str, Any]:
    result = dict(response)
    raw_result = result.get("result_json")
    if not isinstance(raw_result, str):
        return result
    try:
        inner = json.loads(raw_result)
    except json.JSONDecodeError:
        return result
    if not isinstance(inner, dict):
        return result
    screenshot = inner.pop("screenshot", "")
    result["result_json"] = inner
    if screenshot:
        result["screenshot_chars"] = len(str(screenshot))
        if screenshot_out:
            result["screenshot_path"] = _save_screenshot(str(screenshot), screenshot_out)
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage and automate DuoPlus cloud phones with one API key"
    )
    parser.add_argument(
        "--api-key",
        help="API key supplied directly by the user for this invocation",
    )
    parser.add_argument("--api-base", default=_env("DUOPLUS_API_BASE", DEFAULT_API_BASE))
    parser.add_argument("--lang", default=_env("DUOPLUS_LANG", "zh"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--region", default=_env("DUOPLUS_REGION"))
    parser.add_argument("--cloud-ip", default=_env("DUOPLUS_CLOUD_IP"))
    parser.add_argument(
        "--gateway-url-template",
        default=_env("DUOPLUS_GATEWAY_URL_TEMPLATE", DEFAULT_GATEWAY_TEMPLATE),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="list cloud phones")
    list_parser.add_argument("--page", type=int, default=1)
    list_parser.add_argument("--pagesize", type=int, default=100)
    list_parser.add_argument(
        "--all", action="store_true", help="fetch every page before AI-support sorting"
    )
    list_parser.add_argument("--image-id", action="append")
    list_parser.add_argument("--name")
    list_parser.add_argument("--link-status", type=int, action="append")
    list_parser.add_argument("--group-id")
    list_parser.add_argument("--proxy-id")

    for name in ("status", "power-on", "power-off", "restart"):
        lifecycle = sub.add_parser(name)
        lifecycle.add_argument("image_ids", nargs="+")
        if name != "status":
            lifecycle.add_argument("--wait", action="store_true")
            lifecycle.add_argument("--wait-timeout", type=float, default=300.0)
            lifecycle.add_argument("--poll", type=float, default=3.0)
        if name == "power-on":
            lifecycle.add_argument(
                "--allow-no-ai",
                action="store_true",
                help="power on after explicit confirmation even when AI HTTP control is unsupported",
            )

    info = sub.add_parser("info")
    info.add_argument("image_id")

    route = sub.add_parser("route", help="resolve external Gateway route")
    route.add_argument("image_id")

    ensure = sub.add_parser("ensure-ready", help="start phone and wait for Gateway")
    ensure.add_argument("image_id")
    ensure.add_argument("--no-power-on", action="store_true")
    ensure.add_argument("--phone-timeout", type=float, default=300.0)
    ensure.add_argument("--gateway-timeout", type=float, default=120.0)
    ensure.add_argument("--poll", type=float, default=3.0)

    proxy_list = sub.add_parser("proxy-list")
    proxy_list.add_argument("--page", type=int, default=1)
    proxy_list.add_argument("--pagesize", type=int, default=100)
    proxy_list.add_argument("--status", type=int, action="append")

    init_proxy = sub.add_parser("init-proxy")
    init_proxy.add_argument("image_id")
    init_proxy.add_argument("--proxy-id")
    init_proxy.add_argument("--host")
    init_proxy.add_argument("--port", type=int)
    init_proxy.add_argument("--user")
    init_proxy.add_argument("--password")
    init_proxy.add_argument("--protocol", choices=("socks5", "http", "https"), default="socks5")
    init_proxy.add_argument("--ip-scan-channel", choices=("ip2location", "ipapi"), default="ip2location")
    init_proxy.add_argument("--name")
    init_proxy.add_argument("--dpi-name")
    init_proxy.add_argument("--network-mode", type=int, choices=(1, 2))
    init_proxy.add_argument("--brand")
    init_proxy.add_argument("--model")

    for name in ("health", "ready"):
        gateway = sub.add_parser(name)
        gateway.add_argument("image_id")

    ui = sub.add_parser("ui-state")
    ui.add_argument("image_id")
    ui.add_argument("--ui-lang", default="zh")
    ui.add_argument("--screenshot-out")
    ui.add_argument("--no-screenshot", action="store_true", help="Read elements without capturing a screenshot")
    ui.add_argument("--max-age-ms", type=int, choices=range(0, 2001), metavar="0..2000", default=300)

    action = sub.add_parser("action")
    action.add_argument("image_id")
    action.add_argument("action_name")
    action.add_argument("--params", default="{}")
    action.add_argument("--screenshot-out")
    action.add_argument("--deadline-seconds", type=float)

    platform_shell = sub.add_parser(
        "platform-shell",
        help="fallback shell execution through the official control API",
    )
    platform_shell.add_argument("image_id")
    platform_shell.add_argument("--command", dest="shell_command", required=True)

    query = sub.add_parser("query")
    query.add_argument("image_id")
    query.add_argument("command_id")
    query.add_argument("--screenshot-out")

    stop = sub.add_parser("stop")
    stop.add_argument("image_id")
    stop.add_argument("task_id")
    stop.add_argument("--reason", default="AI operator requested stop")
    return parser


def _client(args: argparse.Namespace) -> DuoPlusClient:
    return DuoPlusClient(
        api_key=args.api_key or _env("DUOPLUS_API_KEY", "") or "",
        api_base=args.api_base,
        lang=args.lang,
        timeout=args.timeout,
        region=args.region,
        cloud_ip=args.cloud_ip,
        gateway_template=args.gateway_url_template,
        gateway_token=_env("DUOPLUS_GATEWAY_TOKEN"),
    )


def _wait_target(operation: str) -> int:
    return 2 if operation == "power-off" else 1


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    client = _client(args)

    if args.command == "list":
        filters: Dict[str, Any] = {"page": args.page, "pagesize": args.pagesize}
        for source, target in (
            ("image_id", "image_id"),
            ("name", "name"),
            ("link_status", "link_status"),
            ("group_id", "group_id"),
            ("proxy_id", "proxy_id"),
        ):
            value = getattr(args, source)
            if value is not None:
                filters[target] = value
        response = client.all_phones(filters) if args.all else client.phones(filters)
        _emit(_decorate_phone_response(response))
        return 0

    if args.command == "status":
        _emit(client.statuses(args.image_ids))
        return 0

    if args.command in {"power-on", "power-off", "restart"}:
        ai_control = None
        if args.command == "power-on":
            ai_control = client.require_ai_support(
                args.image_ids, allow_unsupported=args.allow_no_ai
            )
        response = client.lifecycle(args.command, args.image_ids)
        result: Dict[str, Any] = {"request": response}
        if ai_control is not None:
            result["ai_control"] = ai_control
        if args.wait:
            data = response.get("data") if isinstance(response.get("data"), dict) else {}
            accepted_raw = data.get("success") if isinstance(data, dict) else None
            accepted = (
                [str(item) for item in accepted_raw]
                if isinstance(accepted_raw, list)
                else list(args.image_ids)
            )
            if not accepted:
                raise DuoPlusError(
                    f"{args.command} was not accepted for any requested cloud phone"
                )
            if args.command == "restart":
                result["wait"] = client.wait_for_restart(
                    accepted, timeout=args.wait_timeout, poll=args.poll
                )
            else:
                result["wait"] = client.wait_for_status(
                    accepted,
                    target=_wait_target(args.command),
                    timeout=args.wait_timeout,
                    poll=args.poll,
                )
        _emit(result)
        return 0

    if args.command == "info":
        _emit(client.info(args.image_id))
        return 0

    if args.command == "route":
        _emit(client.route(args.image_id))
        return 0

    if args.command == "ensure-ready":
        _emit(
            client.ensure_ready(
                args.image_id,
                power_on=not args.no_power_on,
                phone_timeout=args.phone_timeout,
                gateway_timeout=args.gateway_timeout,
                poll=args.poll,
            )
        )
        return 0

    if args.command == "proxy-list":
        payload: Dict[str, Any] = {"page": args.page, "pagesize": args.pagesize}
        if args.status is not None:
            payload["status"] = args.status
        _emit(client.control("/api/v1/proxy/list", payload))
        return 0

    if args.command == "init-proxy":
        if args.proxy_id:
            if args.host or args.port:
                raise DuoPlusError("use either --proxy-id or --host/--port, not both")
            proxy: Dict[str, Any] = {"id": args.proxy_id}
        else:
            if not args.host or args.port is None:
                raise DuoPlusError("--host and --port are required when --proxy-id is absent")
            proxy = {
                "host": args.host,
                "port": args.port,
                "protocol": args.protocol,
            }
            if args.user:
                proxy["user"] = args.user
            password = args.password or _env("DUOPLUS_PROXY_PASSWORD")
            if password:
                proxy["password"] = password
        image: Dict[str, Any] = {
            "image_id": args.image_id,
            "ip_scan_channel": args.ip_scan_channel,
            "proxy": proxy,
        }
        for name in ("name", "dpi_name", "network_mode", "brand", "model"):
            value = getattr(args, name)
            if value is not None:
                image[name] = value
        _emit(client.control("/api/v1/cloudPhone/initProxy", {"images": [image]}))
        return 0

    if args.command in {"health", "ready"}:
        _emit(client.gateway(args.image_id, {"operation": args.command}, timeout=20))
        return 0

    if args.command == "ui-state":
        command_id, task_id = _command_ids("ui-state")
        response = client.gateway(
            args.image_id,
            {
                "operation": "submit",
                "command_id": command_id,
                "task_id": task_id,
                "action": "get_ui_state",
                "payload": {
                    "task_type": "ai",
                    "task_id": task_id,
                    "action": "get_ui_state",
                    "lang": args.ui_lang,
                    "need_screenshot": not args.no_screenshot,
                    "max_age_ms": args.max_age_ms,
                },
            },
            timeout=310,
            retries=0,
        )
        _emit(_summarize_gateway_result(response, args.screenshot_out))
        return 0

    if args.command == "action":
        params = _parse_json_object(args.params, "--params")
        command_id, task_id = _command_ids(args.action_name.lower())
        body: Dict[str, Any] = {
            "operation": "submit",
            "command_id": command_id,
            "task_id": task_id,
            "action": "execute",
            "payload": {
                "task_type": "ai",
                "task_id": task_id,
                "action": "execute",
                "action_name": args.action_name.upper(),
                "params": params,
            },
        }
        if args.deadline_seconds is not None:
            body["deadline_at"] = int((time.time() + args.deadline_seconds) * 1000)
        response = client.gateway(args.image_id, body, timeout=310, retries=0)
        _emit(_summarize_gateway_result(response, args.screenshot_out))
        return 0

    if args.command == "platform-shell":
        _emit(client.platform_shell(args.image_id, args.shell_command))
        return 0

    if args.command == "query":
        response = client.gateway(
            args.image_id,
            {"operation": "query", "command_id": args.command_id},
            timeout=30,
        )
        _emit(_summarize_gateway_result(response, args.screenshot_out))
        return 0

    if args.command == "stop":
        command_id, _ = _command_ids("stop")
        _emit(
            client.gateway(
                args.image_id,
                {
                    "operation": "stop",
                    "command_id": command_id,
                    "task_id": args.task_id,
                    "reason": args.reason,
                },
                timeout=310,
                retries=0,
            )
        )
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DuoPlusError as exc:
        _emit(exc.as_dict())
        raise SystemExit(2)
