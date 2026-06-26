"""~/.eqxiu/config.json 与登录、鉴权状态。"""

from __future__ import annotations

import getpass
import json
import sys
from typing import Any

import requests

from .constants import CONFIG_DIR, CONFIG_PATH, CONFIG_TOKEN_KEY, PASSPORT_PROFILE_URL


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.is_file():
        return {}
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(data: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        CONFIG_PATH.chmod(0o600)
    except OSError:
        pass


def token_from_config(cfg: dict[str, Any]) -> str:
    v = cfg.get(CONFIG_TOKEN_KEY) or cfg.get("x_openclaw_token")
    return (v if isinstance(v, str) else str(v or "")).strip()


def check_auth_status(access_token: str, timeout: float) -> dict[str, Any]:
    headers = {CONFIG_TOKEN_KEY: access_token}
    r = requests.get(PASSPORT_PROFILE_URL, headers=headers, timeout=timeout)
    if r.status_code != 200 or not r.json().get("success"):
        return {"success": False, "code": 1002, "msg": "认证失败"}
    return {"success": True, "code": 200, "msg": "认证成功", "data": r.json().get("obj")}


def login_interactive() -> int:
    cfg = load_config()
    print("交互式登录：令牌输入时不会回显。", file=sys.stderr)
    token = getpass.getpass("X-Openclaw-Token: ").strip()
    if not token:
        print("未输入令牌，已取消。", file=sys.stderr)
        return 1
    cfg[CONFIG_TOKEN_KEY] = token
    save_config(cfg)
    print(f"已保存至 {CONFIG_PATH}（{CONFIG_TOKEN_KEY}）。", file=sys.stderr)
    return 0
