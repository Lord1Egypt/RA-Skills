"""Common utilities for environment loading, auth, HTTP, and JSON output."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

DXB_BASE = "https://goods.dianxiaobao.net"
ALPHA_BASE = "https://api.alphashop.cn"
ALPHA_PRE_BASE = "https://api.alphashop.cn"
SESSIONS_BASE = "/tmp"

DEFAULT_MARKETPLACE_ID = "ATVPDKIKX0DER"
DEFAULT_LANGUAGE_TAG = "en_US"


def load_env() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)
        if key == "ACCESS_KEY":
            os.environ.setdefault("ALPHASHOP_ACCESS_KEY", value)
        if key == "SECRET_KEY":
            os.environ.setdefault("ALPHASHOP_SECRET_KEY", value)


load_env()


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def jwt_token() -> str:
    import jwt

    access_key = env("ALPHASHOP_ACCESS_KEY") or env("ACCESS_KEY")
    secret_key = env("ALPHASHOP_SECRET_KEY") or env("SECRET_KEY")
    if not access_key or not secret_key:
        raise RuntimeError("Missing ALPHASHOP_ACCESS_KEY / ALPHASHOP_SECRET_KEY")
    now = int(time.time())
    token = jwt.encode(
        {"iss": access_key, "exp": now + 1800, "nbf": now - 5},
        secret_key,
        algorithm="HS256",
        headers={"alg": "HS256"},
    )
    return token if isinstance(token, str) else token.decode("utf-8")


def alpha_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {jwt_token()}", "Content-Type": "application/json"}


def post(url: str, payload: dict[str, Any], headers: dict[str, str] | None = None, timeout: int = 20) -> dict[str, Any]:
    import requests

    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


SENSITIVE_KEYS = {
    "authorization",
    "encryptedcode",
    "encrypted_code",
    "usercode",
    "x-csk-ak",
    "x-csk-sign",
}


def redact_sensitive(data: Any) -> Any:
    if isinstance(data, dict):
        redacted: dict[str, Any] = {}
        for key, value in data.items():
            normalized = str(key).replace("-", "_").lower()
            if normalized in SENSITIVE_KEYS or any(token in normalized for token in ("secret", "token", "password")):
                redacted[key] = "<REDACTED>"
            else:
                redacted[key] = redact_sensitive(value)
        return redacted
    if isinstance(data, list):
        return [redact_sensitive(item) for item in data]
    if isinstance(data, str):
        text = re.sub(r"DXB[A-Za-z0-9_+=/-]{12,}", "<DXB_ENCRYPTED_CODE>", data)
        text = re.sub(r"Bearer\s+[A-Za-z0-9._~+/=-]{12,}", "Bearer <REDACTED>", text)
        return text
    return data


def redacted_dump(data: Any) -> str:
    return dump(redact_sensitive(data))


def first_present(*values: Any, default: Any = "") -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return default


def get_session_dir(argv: list[str] | None = None) -> str:
    import sys

    args = argv if argv is not None else sys.argv
    if len(args) < 2:
        print("[ERROR] 请传入 session 目录路径作为第一个参数", file=sys.stderr)
        sys.exit(1)
    session_dir = args[1]
    if not os.path.isdir(session_dir):
        print(f"[ERROR] session 目录不存在: {session_dir}", file=sys.stderr)
        sys.exit(1)
    return session_dir


def read_session(session_dir: str, filename: str, required_keys: list[str] | None = None) -> dict[str, Any]:
    path = Path(session_dir) / filename
    if not path.exists():
        raise FileNotFoundError(f"[GUARD] 缺少前置文件 {path}，请先执行对应步骤")
    data = json.loads(path.read_text(encoding="utf-8"))
    if required_keys:
        missing = [key for key in required_keys if data.get(key) in (None, "", [], {})]
        if missing:
            raise ValueError(f"[GUARD] {path} 缺少必填字段: {missing}")
    return data


def write_session(session_dir: str, filename: str, data: Any) -> str:
    path = Path(session_dir) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp_path.write_text(dump(data), encoding="utf-8")
    os.chmod(tmp_path, 0o600)
    os.replace(tmp_path, path)
    os.chmod(path, 0o600)
    print(f"[OK] 写入 {path}", file=sys.stderr)
    return str(path)
