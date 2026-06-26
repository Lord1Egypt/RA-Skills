#!/usr/bin/env python3
"""密钥配置 CLI：set / status / clear（管理 .cache/keys.json）。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import (  # noqa: E402
    CACHE_DIR,
    KEYS_FILE,
    _ENV_TO_JSON_KEYS,
    _load_dotenv,
    _load_keys_json,
    is_booking_ready,
    is_newapi_configured,
    reload_config,
)


def _mask(val: str, show: int = 4) -> str:
    if len(val) <= show:
        return "*" * len(val) if val else "(未配置)"
    return val[:show] + "*" * (len(val) - show)


def cmd_status() -> dict:
    reload_config()
    env = _load_dotenv()
    keys = _load_keys_json()
    sources: dict = {}

    for env_name, json_key in _ENV_TO_JSON_KEYS.items():
        from_env = (env_name in env) or (bool(__import__("os").environ.get(env_name, "").strip()))
        from_dotenv = env_name in env
        from_json = json_key in keys
        sources[env_name] = {
            "hasValue": bool(__import__("os").environ.get(env_name, "").strip())
            or bool(env.get(env_name, "").strip())
            or bool(keys.get(json_key, "").strip()),
            "sources": {
                "envVar": bool(__import__("os").environ.get(env_name, "").strip()),
                "dotenv": from_dotenv,
                "keysJson": from_json,
            },
        }

    configured = is_newapi_configured()
    booking = is_booking_ready()

    message = f"采购配置: {'已配置' if configured else '未配置'}，预订: {'就绪' if booking else '未就绪'}"
    return {
        "skill": "fr24-ai",
        "status": "success",
        "action": "config-status",
        "data": {
            "configured": configured,
            "bookingReady": booking,
            "sources": sources,
        },
        "message": message,
    }


def cmd_set(values: dict[str, str]) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    existing: dict = {}
    if KEYS_FILE.is_file():
        try:
            existing = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    field_map = {
        "appkey": "appkey",
        "sign-secret": "signSecret",
        "sign_secret": "signSecret",
        "aes-secret": "aesSecret",
        "aes_secret": "aesSecret",
    }
    updated = []
    for key, val in values.items():
        json_key = field_map.get(key, key)
        if val:
            existing[json_key] = val
            updated.append(json_key)

    KEYS_FILE.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    reload_config()

    configured = is_newapi_configured()
    booking = is_booking_ready()
    return {
        "skill": "fr24-ai",
        "status": "success",
        "action": "config-set",
        "data": {
            "updated": updated,
            "configured": configured,
            "bookingReady": booking,
        },
        "message": f"已更新: {', '.join(updated)}。采购: {'已配置' if configured else '未配置'}，预订: {'就绪' if booking else '未就绪'}",
    }


def cmd_clear() -> dict:
    if KEYS_FILE.is_file():
        KEYS_FILE.unlink()
    reload_config()
    return {
        "skill": "fr24-ai",
        "status": "success",
        "action": "config-clear",
        "message": "已清除 .cache/keys.json 配置。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="fr24-ai 密钥配置管理")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="查看配置状态与来源")

    p_set = sub.add_parser("set", help="设置密钥（写入 .cache/keys.json）")
    p_set.add_argument("--appkey", default="", help="采购 APPKEY")
    p_set.add_argument("--sign-secret", default="", help="SHA512 签名密钥")
    p_set.add_argument("--aes-secret", default="", help="16 字节 AES 密钥")

    sub.add_parser("clear", help="清除 .cache/keys.json")

    args = parser.parse_args()

    if args.cmd == "status":
        out = cmd_status()
    elif args.cmd == "set":
        vals = {
            k: getattr(args, k, "").strip()
            for k in ("appkey", "sign_secret", "aes_secret")
        }
        # argparse 将 - 转为 _，映射回来
        vals = {
            "appkey": args.appkey.strip(),
            "sign-secret": args.sign_secret.strip(),
            "aes-secret": args.aes_secret.strip(),
        }
        if not any(vals.values()):
            out = {
                "skill": "fr24-ai",
                "status": "failure",
                "action": "config-set",
                "message": "请至少指定一项: --appkey, --sign-secret, --aes-secret",
            }
        else:
            out = cmd_set(vals)
    else:
        out = cmd_clear()

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("status") == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
