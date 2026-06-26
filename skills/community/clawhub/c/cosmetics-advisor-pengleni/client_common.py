#!/usr/bin/env python3
"""Shared helpers for ClawHub skill CLI clients."""

import json
import os
import socket
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


def load_env_file(path: str = ".env") -> None:
    """Load key-value pairs from an env file into process environment.

    功能:
        读取 .env 文件并写入 os.environ；仅在变量尚未存在时写入。

    输入:
        path: env 文件路径，默认 .env。

    输出:
        无返回值；副作用为更新当前进程环境变量。
    """
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def require_env(name: str) -> str:
    """Get required environment variable or terminate program.

    功能:
        读取指定环境变量，若为空则打印错误并退出。

    输入:
        name: 环境变量名。

    输出:
        环境变量字符串值（去除首尾空白）。
    """
    value = os.getenv(name, "").strip()
    if not value:
        print(f"[ERROR] Missing required env: {name}")
        sys.exit(1)
    return value


def get_request_timeout_seconds(default: float = 30.0) -> float:
    """Resolve request timeout from environment with fallback.

    功能:
        从 REQUEST_TIMEOUT_SECONDS 读取超时时间，并做健壮性校验。

    输入:
        default: 默认超时时间（秒）。

    输出:
        可用的超时时间（float）。
    """
    raw = os.getenv("REQUEST_TIMEOUT_SECONDS", "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except ValueError:
        return default


def post_json(url: str, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
    """Send HTTP POST JSON request and normalize error responses.

    功能:
        发送 JSON POST 请求，可附带 Bearer Token，并将网络/HTTP 异常统一包装。

    输入:
        url: 目标接口 URL。
        payload: JSON 请求体字典。
        token: 可选 Bearer Token。

    输出:
        响应字典；若失败返回包含 error 字段的标准结构。
    """
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=get_request_timeout_seconds()) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": {"status": e.code, "body": body}}
    except urllib.error.URLError as e:
        return {"error": {"status": "NETWORK", "body": str(e)}}
    except (TimeoutError, socket.timeout) as e:
        return {"error": {"status": "TIMEOUT", "body": str(e)}}
    except Exception as e:
        return {"error": {"status": "UNKNOWN", "body": str(e)}}


def has_error(data: Dict[str, Any]) -> bool:
    """Check whether a response dict contains standardized error info.

    功能:
        判断响应是否包含 error 对象。

    输入:
        data: 待检查的响应字典。

    输出:
        True 表示包含 error；否则 False。
    """
    return isinstance(data, dict) and isinstance(data.get("error"), dict)


def print_json(data: Dict[str, Any]) -> None:
    """Pretty-print JSON dictionary to stdout.

    功能:
        以 UTF-8 和缩进格式打印字典内容，便于调试查看。

    输入:
        data: 待打印的字典。

    输出:
        无返回值；将格式化 JSON 输出到标准输出。
    """
    print(json.dumps(data, ensure_ascii=False, indent=2))


def load_session(path: str = ".session.json") -> Dict[str, Any]:
    """Load session data from a local JSON file.

    功能:
        读取本地会话文件，支持文件不存在或 JSON 损坏时安全降级。

    输入:
        path: 会话文件路径，默认 .session.json。

    输出:
        会话字典；读取失败时返回空字典。
    """
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_session(data: Dict[str, Any], path: str = ".session.json") -> None:
    """Persist session data to local JSON file.

    功能:
        将 user_id/session_id 等会话信息写入本地文件。

    输入:
        data: 要保存的会话字典。
        path: 目标文件路径，默认 .session.json。

    输出:
        无返回值；副作用为写入/覆盖目标 JSON 文件。
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
