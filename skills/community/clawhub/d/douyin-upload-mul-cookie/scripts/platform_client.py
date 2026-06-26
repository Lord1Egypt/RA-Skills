#!/usr/bin/env python3
import json
import os
import urllib.error
import urllib.parse
import urllib.request


class PlatformClientError(RuntimeError):
    pass


DEFAULT_PLATFORM_BASE_URL = "http://easyclaw.bar/shuzirenapi"
USER_PORTAL_URL = "http://easyclaw.bar/shuziren/user"
KEY_SETUP_HINT = f"Please go to {USER_PORTAL_URL} to generate and configure your platform key."


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise PlatformClientError(f"Platform key is not configured. {KEY_SETUP_HINT}")
    return value


def api_base() -> str:
    base_url = os.environ.get("CHANJING_PLATFORM_BASE_URL", "").strip() or DEFAULT_PLATFORM_BASE_URL
    base_url = base_url.rstrip("/")
    if base_url.endswith("/api"):
        return base_url
    return f"{base_url}/api"


def default_headers(content_type: str | None = None) -> dict[str, str]:
    platform_token = os.environ.get("CHANJING_PLATFORM_API_TOKEN", "").strip()
    if platform_token:
        headers = {"X-API-Token": platform_token}
    else:
        api_key = os.environ.get("CHANJING_PLATFORM_API_KEY", "").strip()
        api_secret = os.environ.get("CHANJING_PLATFORM_API_SECRET", "").strip()
        if not api_key or not api_secret:
            raise PlatformClientError(f"Platform key is not configured. {KEY_SETUP_HINT}")
        headers = {
            "X-API-Key": api_key,
            "X-API-Secret": api_secret,
        }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def build_url(path: str) -> str:
    clean_path = path if path.startswith("/") else f"/{path}"
    return f"{api_base()}{clean_path}"


def parse_response(response) -> dict | list | str | None:
    raw = response.read()
    if not raw:
        return None
    text = raw.decode("utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def request_json(method: str, path: str, payload: dict | None = None):
    body = None
    headers = default_headers()
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        build_url(path),
        data=body,
        headers=headers,
        method=method.upper(),
    )
    try:
        with urllib.request.urlopen(request) as response:
            return parse_response(response)
    except urllib.error.HTTPError as exc:
        error_payload = parse_response(exc)
        if exc.code == 401:
            raise PlatformClientError(f"Platform key is invalid or expired. {KEY_SETUP_HINT}") from exc
        if isinstance(error_payload, dict) and "detail" in error_payload:
            raise PlatformClientError(str(error_payload["detail"])) from exc
        raise PlatformClientError(json.dumps(error_payload, ensure_ascii=False)) from exc
    except urllib.error.URLError as exc:
        raise PlatformClientError(f"Failed to connect to platform: {exc}") from exc
