#!/usr/bin/env python3
"""Atomic OpenClaw runner implemented with Python standard library HTTP."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

try:
    from scripts.openclaw_safety import detect_local_image, summarize_http_request, summarize_json_text
except ImportError:
    from openclaw_safety import detect_local_image, summarize_http_request, summarize_json_text


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
COMMANDS_FILE = PROJECT_ROOT / "api" / "commands.json"

DEFAULT_AK_URL = "https://www.designkit.com/openClaw"
DEFAULT_API_BASE = "https://openclaw-designkit-api.meitu.com"
DEFAULT_CLIENT_ID = "2288866678"
DEFAULT_ASYNC_QUERY_ENDPOINT = "/openclaw/mtlab/query"


def normalize_api_base_for_openclaw(base: str, endpoint: str, query_endpoint: str) -> str:
    normalized = (base or "").rstrip("/")
    if endpoint.startswith("/openclaw/") or query_endpoint.startswith("/openclaw/"):
        normalized = normalized.removesuffix("/v1")
    return normalized


def append_query_param(url: str, key: str, value: str) -> str:
    joiner = "&" if "?" in url else "?"
    return f"{url}{joiner}{key}={value}"


def normalize_webapi_base_for_maat(base: str, api_base: str) -> str:
    raw = (base or api_base or DEFAULT_API_BASE).rstrip("/")
    if raw.endswith("/v1/"):
        raw = raw[:-4]
    elif raw.endswith("/v1"):
        raw = raw[:-3]
    return raw.rstrip("/")


def extract_msg_id(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    for path in (("data", "msg_id"), ("data", "task_id"), ("data", "id"), ("msg_id",), ("task_id",), ("id",)):
        current: Any = payload
        for key in path:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                current = None
                break
        if isinstance(current, str) and current:
            return current
    return ""


def extract_media_urls(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    data = payload.get("data")
    if not isinstance(data, dict):
        return []
    urls: list[str] = []
    for item in data.get("media_info_list") or []:
        if isinstance(item, dict):
            url = item.get("media_data")
            if isinstance(url, str) and url:
                urls.append(url)
    return urls


def json_error(error_type: str, message: str, user_hint: str, *, extra: Optional[Dict[str, Any]] = None, exit_code: int = 1) -> None:
    out: Dict[str, Any] = {
        "ok": False,
        "error_type": error_type,
        "message": message,
        "user_hint": user_hint,
    }
    if extra:
        out.update(extra)
    print(json.dumps(out, ensure_ascii=False))
    raise SystemExit(exit_code)


def debug_log(message: str) -> None:
    if os.environ.get("OPENCLAW_DEBUG", "0") == "1":
        print(f"[DEBUG] {message}", file=sys.stderr)


def request_log(message: str) -> None:
    if os.environ.get("OPENCLAW_REQUEST_LOG", "0") != "0":
        print(f"[REQUEST] {message}", file=sys.stderr)


def request_log_response_json(label: str, text: str, http_code: Optional[int] = None) -> None:
    if os.environ.get("OPENCLAW_REQUEST_LOG", "0") == "0":
        return
    try:
        max_len = int(os.environ.get("OPENCLAW_REQUEST_LOG_BODY_MAX", "20000"))
    except ValueError:
        max_len = 20000
    summary = summarize_json_text(
        text,
        ak=os.environ.get("DESIGNKIT_OPENCLAW_AK", "").strip(),
        http_code=http_code,
        max_len=max_len,
    )
    print(f"[REQUEST] {label} (summary):", file=sys.stderr)
    print(json.dumps(summary, ensure_ascii=False, indent=2), file=sys.stderr)


def request_log_http_summary(
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Optional[bytes] = None,
    *,
    multipart_hint: Optional[str] = None,
    timeout: int = 120,
) -> None:
    if os.environ.get("OPENCLAW_REQUEST_LOG", "0") == "0":
        return
    summary = summarize_http_request(
        method,
        url,
        headers,
        data=data,
        multipart_hint=multipart_hint,
        timeout=timeout,
    )
    print("[REQUEST] request (summary):", file=sys.stderr)
    print(json.dumps(summary, ensure_ascii=False, indent=2), file=sys.stderr)


def load_commands() -> Dict[str, Any]:
    with COMMANDS_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_command(commands: Dict[str, Any], action: str) -> Dict[str, Any]:
    command = commands.get(action)
    if not isinstance(command, dict):
        json_error("PARAM_ERROR", f"Unknown action: {action}", "Please use an action defined in api/commands.json")
    return command


def http_request(method: str, url: str, headers: Dict[str, str], body: Optional[bytes] = None, *, timeout: int = 120) -> Tuple[int, Any, str]:
    request_log_http_summary(method, url, headers, body, timeout=timeout)
    req = urllib.request.Request(url, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.getcode() or 200
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        code = exc.code
        raw = exc.read().decode("utf-8", errors="replace")
    request_log_response_json("response_body", raw, code)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"_raw": raw}
    return code, parsed, raw


def http_json_post(url: str, ak: str, body: bytes) -> Tuple[int, Any, str]:
    headers = {
        "Content-Type": "application/json",
        "X-Openclaw-AK": ak,
    }
    return http_request("POST", url, headers, body, timeout=120)


def http_json_get(url: str, ak: str) -> Tuple[int, Any, str]:
    headers = {"X-Openclaw-AK": ak}
    return http_request("GET", url, headers, None, timeout=120)


def build_body(template: Any, image_url: str) -> bytes:
    body_str = json.dumps(template, ensure_ascii=False).replace("{{image}}", image_url)
    return body_str.encode("utf-8")


def emit_http_error(action: str, http_code: int, raw_body: str) -> None:
    hint = "Please try again later."
    error_type = "UNKNOWN_ERROR"
    if http_code in (401, 403):
        error_type = "AUTH_ERROR"
        hint = f"Authentication failed. Please visit {os.environ.get('DESIGNKIT_OPENCLAW_AK_URL', DEFAULT_AK_URL)} to check your credits and API key."
    elif http_code == 429:
        error_type = "QPS_LIMIT"
        hint = "Rate limit reached. Please try again later."
    elif http_code >= 500:
        error_type = "TEMPORARY_UNAVAILABLE"
        hint = "Service is temporarily unavailable. Please try again later."
    elif http_code == 402:
        error_type = "ORDER_REQUIRED"
        hint = "Insufficient credits. Please visit https://www.designkit.com/ to get credits."

    try:
        body = json.loads(raw_body)
        message = str(body.get("message") or f"HTTP {http_code}")
    except json.JSONDecodeError:
        message = f"HTTP {http_code}"

    json_error(
        error_type,
        message,
        hint,
        extra={"command": action, "http_code": http_code},
    )


def emit_api_error_from_body(action: str, parsed: Any, raw_body: str) -> None:
    payload = parsed if isinstance(parsed, dict) else {"_raw": raw_body}
    message = str(payload.get("message") or "Processing failed") if isinstance(payload, dict) else "Processing failed"
    error_code = payload.get("code", -1) if isinstance(payload, dict) else -1
    print(
        json.dumps(
            {
                "ok": False,
                "command": action,
                "error_type": "API_ERROR",
                "error_code": error_code,
                "message": message,
                "user_hint": message,
                "result": payload,
            },
            ensure_ascii=False,
        )
    )
    raise SystemExit(0)


def upload_local_image(file_path: str, ak: str) -> str:
    suffix, mime = detect_local_image(file_path)
    fname = os.path.basename(file_path)
    api_base = os.environ.get("OPENCLAW_API_BASE", DEFAULT_API_BASE)
    webapi_base = normalize_webapi_base_for_maat(os.environ.get("DESIGNKIT_WEBAPI_BASE", ""), api_base)

    getsign_url = f"{webapi_base}/maat/getsign?type=openclaw"
    getsign_headers = {
        "Accept": "application/json, text/plain, */*",
        "X-Openclaw-AK": ak,
        "Origin": "https://www.designkit.cn",
        "Referer": "https://www.designkit.cn/editor/",
    }
    code, getsign_resp, _ = http_request("GET", getsign_url, getsign_headers, None, timeout=30)
    if code < 200 or code >= 300 or not isinstance(getsign_resp, dict):
        json_error("UPLOAD_ERROR", "Failed to get upload signature", "Please check your network or API key and try again")

    upload_url = str((getsign_resp.get("data") or {}).get("upload_url") or "").strip()
    if getsign_resp.get("code") != 0 or not upload_url:
        request_log(f"maat getsign rejected: code={getsign_resp.get('code')}, message={getsign_resp.get('message')}")
        json_error("UPLOAD_ERROR", "Failed to get upload signature", "Please check your network or API key and try again")

    policy_headers = {
        "Origin": "https://www.designkit.cn",
        "Referer": "https://www.designkit.cn/editor/",
    }
    policy_code, policy_resp, _ = http_request("GET", upload_url, policy_headers, None, timeout=30)
    if policy_code < 200 or policy_code >= 300 or not isinstance(policy_resp, list) or not policy_resp:
        json_error("UPLOAD_ERROR", "Failed to get upload policy", "Please check your network and try again")

    try:
        provider = policy_resp[0]["order"][0]
        provider_payload = policy_resp[0][provider]
        up_token = provider_payload["token"]
        up_key = provider_payload["key"]
        up_url = provider_payload["url"]
        up_data = provider_payload["data"]
    except (KeyError, IndexError, TypeError):
        json_error("UPLOAD_ERROR", "Failed to get upload policy", "Please check your network and try again")

    boundary = uuid.uuid4().hex.encode()
    with open(file_path, "rb") as handle:
        file_bytes = handle.read()

    def part(name: str, value: str) -> bytes:
        return (
            b"--"
            + boundary
            + b'\r\nContent-Disposition: form-data; name="'
            + name.encode()
            + b'"\r\n\r\n'
            + value.encode()
            + b"\r\n"
        )

    post_body = (
        part("token", up_token)
        + part("key", up_key)
        + part("fname", fname)
        + b"--"
        + boundary
        + b'\r\nContent-Disposition: form-data; name="file"; filename="'
        + fname.encode()
        + b'"\r\nContent-Type: '
        + mime.encode()
        + b"\r\n\r\n"
        + file_bytes
        + b"\r\n--"
        + boundary
        + b"--\r\n"
    )

    upload_target = f"{up_url}/"
    upload_headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary.decode()}",
        "Origin": "https://www.designkit.cn",
        "Referer": "https://www.designkit.cn/editor/",
    }
    request_log_http_summary(
        "POST",
        upload_target,
        upload_headers,
        None,
        multipart_hint="file=@<local-file>;type=" + mime,
        timeout=120,
    )
    req = urllib.request.Request(upload_target, data=post_body, headers=upload_headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            upload_code = resp.getcode() or 200
            raw_upload = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        upload_code = exc.code
        raw_upload = exc.read().decode("utf-8", errors="replace")
    request_log_response_json("upload_response_body", raw_upload, upload_code)
    try:
        upload_resp = json.loads(raw_upload)
    except json.JSONDecodeError:
        upload_resp = {}

    cdn_url = ""
    if isinstance(upload_resp, dict):
        cdn_url = str(upload_resp.get("data") or "")
    if not cdn_url:
        cdn_url = str(up_data or "")
    if not cdn_url:
        json_error("UPLOAD_ERROR", "Upload failed: no image URL returned", "Please try another image or check your network")
    debug_log(f"Upload completed, CDN URL: {cdn_url}")
    return cdn_url


def resolve_image_input(image_input: str, ak: str) -> str:
    if image_input.startswith("http://") or image_input.startswith("https://"):
        return image_input
    return upload_local_image(image_input, ak)


def run_action(action: str, input_json: str) -> None:
    ak = os.environ.get("DESIGNKIT_OPENCLAW_AK", "").strip()
    if not ak:
        json_error("CREDENTIALS_MISSING", "Environment variable DESIGNKIT_OPENCLAW_AK is not set", f"Please visit {os.environ.get('DESIGNKIT_OPENCLAW_AK_URL', DEFAULT_AK_URL)} to get credits")

    try:
        payload = json.loads(input_json)
    except json.JSONDecodeError:
        json_error("PARAM_ERROR", "Missing required parameter: image", "Please provide an image")
    if not isinstance(payload, dict):
        json_error("PARAM_ERROR", "Missing required parameter: image", "Please provide an image")

    commands = load_commands()
    command = read_command(commands, action)
    status = str(command.get("status") or "")
    if status == "reserved":
        json_error("NOT_IMPLEMENTED", f"{command.get('name', action)} ({action}) is under development", "This capability is not live yet. Please use https://www.designkit.com/ directly")

    image_input = str(payload.get("image") or "").strip()
    if not image_input:
        ask = command.get("ask_if_missing", {}) if isinstance(command.get("ask_if_missing"), dict) else {}
        json_error("PARAM_ERROR", "Missing required parameter: image", str(ask.get("image") or "Please provide an image"))

    endpoint = str(command.get("endpoint") or "")
    response_mode = str(command.get("response_mode") or "")
    query_endpoint = str(command.get("query_endpoint") or DEFAULT_ASYNC_QUERY_ENDPOINT)
    api_base = normalize_api_base_for_openclaw(
        os.environ.get("OPENCLAW_API_BASE", DEFAULT_API_BASE),
        endpoint,
        query_endpoint,
    )

    image_url = resolve_image_input(image_input, ak)
    body = build_body(command.get("body_template", {}), image_url)

    request_url = f"{api_base}{endpoint}"
    if endpoint.startswith("/openclaw/"):
        request_url = append_query_param(request_url, "client_id", os.environ.get("DESIGNKIT_OPENCLAW_CLIENT_ID", DEFAULT_CLIENT_ID))

    debug_log(f"Action: {action}, Endpoint: {endpoint}")
    code, parsed, raw = http_json_post(request_url, ak, body)
    if code < 200 or code >= 300:
        emit_http_error(action, code, raw)

    resp_code = str(parsed.get("code", "")) if isinstance(parsed, dict) else ""
    if resp_code != "0":
        emit_api_error_from_body(action, parsed, raw)

    if response_mode == "async":
        msg_id = extract_msg_id(parsed)
        if not msg_id:
            json_error("API_ERROR", "Async task submission succeeded but msg_id is missing", "Please try again later or contact support")

        max_wait = float(os.environ.get("OPENCLAW_ASYNC_MAX_WAIT_SEC", "180"))
        interval = float(os.environ.get("OPENCLAW_ASYNC_INTERVAL_SEC", "2"))
        max_polls = max(1, int(math.ceil(max_wait / max(interval, 1))))
        query_url_base = f"{api_base}{query_endpoint}"
        if query_endpoint.startswith("/openclaw/"):
            query_url_base = append_query_param(query_url_base, "client_id", os.environ.get("DESIGNKIT_OPENCLAW_CLIENT_ID", DEFAULT_CLIENT_ID))

        for poll_index in range(1, max_polls + 1):
            query_url = append_query_param(query_url_base, "msg_id", msg_id)
            request_log(f"poll {poll_index}/{max_polls}: {query_url}")
            query_code, query_parsed, query_raw = http_json_get(query_url, ak)
            if query_code < 200 or query_code >= 300:
                emit_http_error(action, query_code, query_raw)

            query_resp_code = str(query_parsed.get("code", "")) if isinstance(query_parsed, dict) else ""
            query_msg = str(query_parsed.get("message", "")) if isinstance(query_parsed, dict) else ""
            if query_resp_code == "0":
                media_urls = extract_media_urls(query_parsed)
                if media_urls:
                    print(
                        json.dumps(
                            {
                                "ok": True,
                                "command": action,
                                "msg_id": msg_id,
                                "media_urls": media_urls,
                                "result": query_parsed,
                            },
                            ensure_ascii=False,
                        )
                    )
                    raise SystemExit(0)
            elif query_resp_code == "29901" or query_msg.upper() == "NOT_RESULT":
                pass
            else:
                emit_api_error_from_body(action, query_parsed, query_raw)

            if poll_index < max_polls:
                time.sleep(interval)

        print(
            json.dumps(
                {
                    "ok": False,
                    "command": action,
                    "error_type": "TEMPORARY_UNAVAILABLE",
                    "message": "Async polling timed out",
                    "user_hint": f"No result was returned within {max_wait}s. Please try again later.",
                    "msg_id": msg_id,
                },
                ensure_ascii=False,
            )
        )
        raise SystemExit(0)

    media_urls = extract_media_urls(parsed)
    out: Dict[str, Any] = {
        "ok": True,
        "command": action,
        "media_urls": media_urls,
        "result": parsed,
    }
    msg_id = extract_msg_id(parsed)
    if msg_id:
        out["msg_id"] = msg_id
    print(json.dumps(out, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Designkit OpenClaw atomic runner")
    parser.add_argument("action")
    parser.add_argument("--input-json", required=True)
    args = parser.parse_args()
    run_action(args.action, args.input_json)


if __name__ == "__main__":
    main()
