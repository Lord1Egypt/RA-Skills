"""滴答开放平台本地 OAuth 授权与凭证落盘。"""

from __future__ import annotations

import base64
import json
import os
import secrets
import threading
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, Optional, Tuple

DIDA_AUTHORIZATION_ENDPOINT = "https://dida365.com/oauth/authorize"
DIDA_TOKEN_ENDPOINT = "https://api.dida365.com/oauth/token"
DEFAULT_REDIRECT_URI = "http://localhost:38000/callback"
DEFAULT_SCOPE = "tasks:read tasks:write"


def get_openapi_env_path() -> Path:
    """返回本地 Open API 凭证文件路径。"""

    override = os.environ.get("DIDA_COACH_OPENAPI_ENV_PATH")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".dida-coach" / "dida-openapi.env"


def generate_oauth_state() -> str:
    """生成 OAuth state。"""

    return secrets.token_urlsafe(24)


def build_authorization_url(
    client_id: str,
    *,
    redirect_uri: str = DEFAULT_REDIRECT_URI,
    scope: str = DEFAULT_SCOPE,
    state: Optional[str] = None,
) -> Tuple[str, str]:
    """生成滴答开放平台授权链接。"""

    oauth_state = state or generate_oauth_state()
    query = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": oauth_state,
        }
    )
    return f"{DIDA_AUTHORIZATION_ENDPOINT}?{query}", oauth_state


def exchange_code_for_token(
    client_id: str,
    client_secret: str,
    code: str,
    *,
    redirect_uri: str = DEFAULT_REDIRECT_URI,
) -> Dict[str, object]:
    """用授权码换取 token。"""

    payload = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
    ).encode("utf-8")
    basic_token = base64.b64encode(
        f"{client_id}:{client_secret}".encode("utf-8")
    ).decode("ascii")
    request = urllib.request.Request(
        DIDA_TOKEN_ENDPOINT,
        data=payload,
        headers={
            "Authorization": f"Basic {basic_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("token 响应不是对象")
    return data


def read_openapi_env(path: Optional[Path] = None) -> Dict[str, str]:
    """读取本地凭证文件。"""

    env_path = path or get_openapi_env_path()
    if not env_path.exists():
        return {}

    values: Dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_openapi_env(
    client_id: str,
    client_secret: str,
    token_data: Dict[str, object],
    *,
    redirect_uri: str = DEFAULT_REDIRECT_URI,
    path: Optional[Path] = None,
) -> Path:
    """把 Open API 凭证写入本地 .env。"""

    env_path = path or get_openapi_env_path()
    current = read_openapi_env(env_path)
    current.update(
        {
            "DIDA_OPENAPI_CLIENT_ID": client_id,
            "DIDA_OPENAPI_CLIENT_SECRET": client_secret,
            "DIDA_OPENAPI_REDIRECT_URI": redirect_uri,
            "DIDA_OPENAPI_ACCESS_TOKEN": str(token_data.get("access_token", "")),
            "DIDA_OPENAPI_REFRESH_TOKEN": str(token_data.get("refresh_token", "")),
            "DIDA_OPENAPI_TOKEN_TYPE": str(token_data.get("token_type", "")),
            "DIDA_OPENAPI_SCOPE": str(token_data.get("scope", DEFAULT_SCOPE)),
        }
    )
    if "expires_in" in token_data:
        current["DIDA_OPENAPI_EXPIRES_IN"] = str(token_data.get("expires_in", ""))

    lines = ["# Dida Coach Open API credentials"]
    for key in sorted(current.keys()):
        lines.append(f"{key}={current[key]}")
    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return env_path


@dataclass
class CallbackResult:
    code: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None


def wait_for_oauth_callback(
    *,
    host: str = "127.0.0.1",
    port: int = 38000,
    expected_state: Optional[str] = None,
    timeout_seconds: int = 180,
) -> CallbackResult:
    """监听本地 callback，接收授权码。"""

    result = CallbackResult()
    done = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/callback":
                self.send_response(404)
                self.end_headers()
                return

            params = urllib.parse.parse_qs(parsed.query)
            result.code = params.get("code", [None])[0]
            result.state = params.get("state", [None])[0]
            result.error = params.get("error", [None])[0]

            body = "授权完成，你可以回到终端或客户端继续。"
            if expected_state and result.state != expected_state:
                result.error = "state_mismatch"
                body = "授权失败：state 不匹配，可以关闭此页面后重试。"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            done.set()

        def log_message(self, format: str, *args: object) -> None:  # noqa: A003
            return

    server = HTTPServer((host, port), Handler)
    server.timeout = 0.5
    started = time.time()
    try:
        while time.time() - started < timeout_seconds and not done.is_set():
            server.handle_request()
    finally:
        server.server_close()

    if not done.is_set():
        result.error = "timeout"
    return result
