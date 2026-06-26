#!/usr/bin/env python3
"""Dida365 OAuth helpers."""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any


TOKEN_FILE = Path(__file__).with_name(".dida-token.json")

DEFAULT_CALLBACK_PORT = 18365
OAUTH_BASE = "https://dida365.com/oauth"


def load_env_file() -> None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


def save_token(token_data: dict[str, Any]) -> None:
    payload = dict(token_data)
    payload["obtained_at"] = int(time.time())
    TOKEN_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_token_data() -> dict[str, Any]:
    return json.loads(TOKEN_FILE.read_text(encoding="utf-8"))


def get_access_token() -> str:
    """获取当前的 access token。"""
    # 优先从环境变量获取（手动设置模式）
    manual_token = os.environ.get("DIDA_ACCESS_TOKEN")
    if manual_token:
        return manual_token

    # 其次从本地缓存文件获取
    if TOKEN_FILE.exists():
        try:
            token_data = load_token_data()
            access_token = token_data.get("access_token")
            if access_token:
                return access_token
        except Exception:
            pass

    # 如果都没有，提示用户进行授权
    raise RuntimeError("未找到 access token。请先运行: python3 index.py auth")


def _require_oauth_client() -> tuple[str, str]:
    """确保 client_id 和 client_secret 已配置。"""
    load_env_file()
    client_id = os.environ.get("DIDA_CLIENT_ID")
    client_secret = os.environ.get("DIDA_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("缺少 DIDA_CLIENT_ID 或 DIDA_CLIENT_SECRET。请在 .env 文件中配置。")
    return client_id, client_secret


def _request_token(payload: dict[str, str], client_id: str, client_secret: str) -> dict[str, Any]:
    """发送 Token 相关请求（使用 Basic Auth）。"""
    basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    body = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{OAUTH_BASE}/token",
        data=body,
        headers={
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            error_text = exc.read().decode("utf-8", errors="replace")
        except Exception:
            error_text = str(exc)
        raise RuntimeError(f"Token 请求失败: HTTP {exc.code} - {error_text}") from exc


def exchange_token(code: str, client_id: str, client_secret: str, redirect_uri: str) -> dict[str, Any]:
    """使用授权码换取 Token。"""
    return _request_token(
        {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        client_id,
        client_secret,
    )


def refresh_access_token() -> str:
    """自动刷新 access token。"""
    if os.environ.get("DIDA_ACCESS_TOKEN"):
        raise RuntimeError("使用 DIDA_ACCESS_TOKEN 环境变量时无法自动刷新。")

    if not TOKEN_FILE.exists():
        raise RuntimeError("未找到 token 文件，无法刷新。")

    token_data = load_token_data()
    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("当前存储的 Token 不包含 refresh_token，请重新运行授权流程。")

    client_id, client_secret = _require_oauth_client()
    refreshed = _request_token(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": "tasks:write tasks:read",
        },
        client_id,
        client_secret,
    )

    # 保持原有的 refresh_token (如果响应中没给新的)
    if "refresh_token" not in refreshed:
        refreshed["refresh_token"] = refresh_token

    save_token(refreshed)
    return refreshed["access_token"]


class CallbackHandler(BaseHTTPRequestHandler):
    """处理 OAuth 回调的 HTTP Handler。"""
    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        error = params.get("error", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        msg = "<h1>授权成功</h1><p>请返回终端继续。</p>"
        if error:
            self.server.auth_result = {"error": error}
            msg = f"<h1>授权失败</h1><p>错误原因: {error}</p>"
        elif code:
            self.server.auth_result = {"code": code}
        else:
            self.server.auth_result = {"error": "missing_code"}
            msg = "<h1>错误</h1><p>未收到授权码。</p>"
        
        self.wfile.write(msg.encode("utf-8"))

    def log_message(self, format: str, *args: Any) -> None:
        pass


def _wait_for_callback(port: int) -> str:
    """启动本地服务器等待回调。"""
    server = HTTPServer(("127.0.0.1", port), CallbackHandler)
    server.auth_result = {}
    try:
        server.handle_request()
        auth_result = server.auth_result
    finally:
        server.server_close()

    if "error" in auth_result:
        raise RuntimeError(f"授权回调错误: {auth_result['error']}")
    return auth_result["code"]


def run_oauth_flow(authorization_code: str | None = None) -> None:
    """运行完整的 OAuth 授权流程。"""
    client_id, client_secret = _require_oauth_client()
    port = int(os.environ.get("DIDA_CALLBACK_PORT", str(DEFAULT_CALLBACK_PORT)))
    redirect_uri = f"http://localhost:{port}/callback"
    
    if authorization_code:
        code = authorization_code
    else:
        auth_url = (
            f"{OAUTH_BASE}/authorize?"
            + urllib.parse.urlencode({
                "client_id": client_id,
                "scope": "tasks:write tasks:read",
                "redirect_uri": redirect_uri,
                "response_type": "code",
            })
        )
        print(f"\n请在浏览器中打开以下链接完成授权:\n\n{auth_url}\n")
        print("等待回调中...")
        code = _wait_for_callback(port)

    print("正在换取 access token...")
    token_data = exchange_token(code, client_id, client_secret, redirect_uri)
    save_token(token_data)
    print("\n授权成功！Token 已保存。")
