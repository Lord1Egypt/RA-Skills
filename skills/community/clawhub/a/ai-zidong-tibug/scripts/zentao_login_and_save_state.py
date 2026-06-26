#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZenTao API login and save token state.

Usage:
  python3 scripts/zentao_login_and_save_state.py

Environment variables:
  Required:
    HTTP_USER, HTTP_PASS, ZENTAO_USER, ZENTAO_PASS
  Optional:
    ZENTAO_URL=https://pm.jsyyds.com/
    STORAGE_STATE_PATH=./playwright/.auth/zentao-storageState.json
    VERIFY_SSL=true
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import requests
from requests.auth import HTTPBasicAuth


def env_bool(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def ensure_required_env(names: list[str]) -> Dict[str, str]:
    values: Dict[str, str] = {}
    missing: list[str] = []
    for name in names:
        val = os.getenv(name, "").strip()
        if not val:
            missing.append(name)
        else:
            values[name] = val

    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return values


def login_and_get_token(
    base_url: str,
    http_user: str,
    http_pass: str,
    zentao_user: str,
    zentao_pass: str,
    verify_ssl: bool,
) -> str:
    endpoint = f"{base_url}/api.php/v1/tokens"
    payload = {"account": zentao_user, "password": zentao_pass}

    response = requests.post(
        endpoint,
        auth=HTTPBasicAuth(http_user, http_pass),
        json=payload,
        timeout=30,
        verify=verify_ssl,
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Token login failed: HTTP {response.status_code} | {response.text[:300]}"
        )

    try:
        data = response.json()
    except Exception as exc:
        raise RuntimeError(f"Invalid token response: {response.text[:300]}") from exc

    token = data.get("token")
    if not token:
        raise RuntimeError(f"Token missing in response: {data}")
    return token


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def run() -> None:
    required = ensure_required_env([
        "HTTP_USER",
        "HTTP_PASS",
        "ZENTAO_USER",
        "ZENTAO_PASS",
    ])

    config = {
        "url": normalize_base_url(os.getenv("ZENTAO_URL", "https://pm.jsyyds.com/")),
        "http_user": required["HTTP_USER"],
        "http_pass": required["HTTP_PASS"],
        "username": required["ZENTAO_USER"],
        "password": required["ZENTAO_PASS"],
        "storage_state_path": os.getenv(
            "STORAGE_STATE_PATH", "./playwright/.auth/zentao-storageState.json"
        ),
        "verify_ssl": env_bool("VERIFY_SSL", "true"),
    }

    token = login_and_get_token(
        base_url=config["url"],
        http_user=config["http_user"],
        http_pass=config["http_pass"],
        zentao_user=config["username"],
        zentao_pass=config["password"],
        verify_ssl=config["verify_ssl"],
    )

    state = {
        "formatVersion": 2,
        "provider": "zentao-v1-token",
        "zentaoUrl": config["url"],
        "token": token,
        "account": config["username"],
        "savedAt": datetime.now(timezone.utc).isoformat(),
    }

    save_path = Path(config["storage_state_path"]).expanduser().resolve()
    save_state(save_path, state)

    masked = f"{token[:4]}...{token[-4:]}" if len(token) > 8 else "****"
    print(f"✅ 登录成功，token 已保存到: {save_path}")
    print(f"   Token: {masked}")


if __name__ == "__main__":
    run()
