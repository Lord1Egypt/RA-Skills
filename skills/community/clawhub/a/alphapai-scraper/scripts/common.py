#!/usr/bin/env python3
"""
AlphaPai skill shared helpers.
"""

from __future__ import annotations

import json
import os
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_DIR / "config"


DEFAULT_SETTINGS: dict[str, Any] = {
    "site": {
        "base_url": "https://alphapai-web.rabyte.cn",
        "login_url": "https://alphapai-web.rabyte.cn/login",
        "target_url": "https://alphapai-web.rabyte.cn/reading/home/comment",
        "token_storage_key": "USER_AUTH_TOKEN",
        "login_path_keyword": "/login",
    },
    "auth": {
        "methods": ["storage_state", "token", "cookies", "credentials", "profile"],
        "token_file": "config/token.local.json",
        "legacy_token_file": "config/token.json",
        "cookies_file": "config/cookies.local.json",
        "credentials_file": "config/credentials.local.json",
        "username": "",
        "password": "",
        "selectors": {
            "username": [
                "input[type='text']",
                "input[type='email']",
                "input[placeholder*='手机']",
                "input[placeholder*='账号']",
                "input[placeholder*='用户名']",
            ],
            "password": [
                "input[type='password']",
                "input[placeholder*='密码']",
            ],
            "submit": [
                "button[type='submit']",
                "button:has-text('登录')",
                "button:has-text('Log in')",
                "text=登录",
            ],
        },
    },
    "browser": {
        "headless": True,
        "timeout_ms": 30000,
        "launch_strategy": ["ephemeral", "profile"],
        "profile_user_data_dir": "~/Library/Application Support/Google/Chrome",
        "profile_name": "Default",
        "save_storage_state": True,
        "storage_state_file": "~/.openclaw/data/alphapai-scraper/runtime/storage-state.json",
    },
    "scrape": {
        "default_lookback_hours": 1,
        "max_items": 60,
        "max_scroll_rounds": 20,
        "list_wait_ms": 1500,
        "detail_wait_ms": 1500,
        "allow_card_fallback": True,
        "stop_when_older_than_window": True,
        "require_time_label": True,
    },
    "output": {
        "base_dir": "~/.openclaw/data/alphapai-scraper",
        "raw_format": "md",
        "report_format": "md",
        "report_suffix": "_summary",
    },
    "archive": {
        "normalized_subdir": "normalized",
        "index_subdir": "index",
        "database_name": "alphapai.sqlite",
        "scope": "alphapai",
        "visibility": "shared",
        "vector_subdir": "vector",
        "vector_collection": "alphapai_comments",
        "vector_chunk_size": 420,
        "vector_chunk_overlap": 80,
        "vector_batch_size": 8,
        "vector_top_k": 24,
        "vector_score_threshold": 0.3,
    },
    "feishu": {
        "enabled": False,
        "webhook_url": "",
        "title_prefix": "Alpha派摘要",
    },
    "ai": {
        "model": "pixcode/pa/claude-sonnet-4-6",
        "max_input_chars": 20000,
        "target_length_chars": 1000,
        "custom_requirements": "",
    },
}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def read_json_file(path: Path) -> dict[str, Any] | list[Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_path(path_str: str | None) -> Path | None:
    if not path_str:
        return None
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = (SKILL_DIR / path).resolve()
    return path


def load_settings(settings_path: str | None = None) -> dict[str, Any]:
    settings = deepcopy(DEFAULT_SETTINGS)

    candidates: list[Path] = []
    if settings_path:
        path = resolve_path(settings_path)
        if path:
            candidates.append(path)
    env_path = os.environ.get("ALPHAPAI_SETTINGS_FILE")
    if env_path:
        path = resolve_path(env_path)
        if path:
            candidates.append(path)
    candidates.extend(
        [
            CONFIG_DIR / "settings.local.json",
            CONFIG_DIR / "settings.json",
        ]
    )

    for candidate in candidates:
        if candidate and candidate.exists():
            data = read_json_file(candidate)
            if isinstance(data, dict):
                settings = deep_merge(settings, data)
            break

    output_dir = os.environ.get("ALPHAPAI_OUTPUT_DIR")
    if output_dir:
        settings["output"]["base_dir"] = output_dir

    webhook = os.environ.get("ALPHAPAI_FEISHU_WEBHOOK_URL")
    if webhook:
        settings["feishu"]["enabled"] = True
        settings["feishu"]["webhook_url"] = webhook

    return settings


def ensure_runtime_dirs(settings: dict[str, Any]) -> dict[str, Path]:
    base_dir = resolve_path(settings["output"]["base_dir"])
    assert base_dir is not None

    raw_dir = base_dir / "raw"
    report_dir = base_dir / "reports"
    normalized_dir = base_dir / str(settings["archive"]["normalized_subdir"])
    index_dir = base_dir / str(settings["archive"]["index_subdir"])
    vector_dir = index_dir / str(settings["archive"]["vector_subdir"])
    runtime_dir = base_dir / "runtime"
    for path in (base_dir, raw_dir, report_dir, normalized_dir, index_dir, vector_dir, runtime_dir):
        path.mkdir(parents=True, exist_ok=True)

    return {
        "base_dir": base_dir,
        "raw_dir": raw_dir,
        "report_dir": report_dir,
        "normalized_dir": normalized_dir,
        "index_dir": index_dir,
        "vector_dir": vector_dir,
        "runtime_dir": runtime_dir,
    }


def load_auth_bundle(settings: dict[str, Any]) -> dict[str, Any]:
    auth_settings = settings["auth"]

    token = ""
    token_path = resolve_path(auth_settings.get("token_file"))
    legacy_token_path = resolve_path(auth_settings.get("legacy_token_file"))
    for path in (token_path, legacy_token_path):
        if not path or not path.exists():
            continue
        data = read_json_file(path)
        if isinstance(data, dict):
            token = str(data.get("USER_AUTH_TOKEN") or data.get("token") or "").strip()
            if token:
                break

    cookies: list[dict[str, Any]] = []
    cookies_path = resolve_path(auth_settings.get("cookies_file"))
    if cookies_path and cookies_path.exists():
        data = read_json_file(cookies_path)
        if isinstance(data, dict) and isinstance(data.get("cookies"), list):
            cookies = normalize_cookies(data["cookies"])
        elif isinstance(data, list):
            cookies = normalize_cookies(data)

    credentials: dict[str, str] = {
        "username": str(auth_settings.get("username") or "").strip(),
        "password": str(auth_settings.get("password") or "").strip(),
    }
    credentials_path = resolve_path(auth_settings.get("credentials_file"))
    if credentials_path and credentials_path.exists():
        data = read_json_file(credentials_path)
        if isinstance(data, dict):
            credentials["username"] = str(
                data.get("username") or credentials["username"]
            ).strip()
            credentials["password"] = str(
                data.get("password") or credentials["password"]
            ).strip()

    return {
        "token": token,
        "cookies": cookies,
        "credentials": credentials,
        "storage_state_file": str(
            resolve_path(settings["browser"].get("storage_state_file") or "") or ""
        ),
    }


def normalize_cookies(raw_cookies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    allowed_keys = {
        "name",
        "value",
        "domain",
        "path",
        "expires",
        "httpOnly",
        "secure",
        "sameSite",
        "url",
    }
    for cookie in raw_cookies:
        if not isinstance(cookie, dict):
            continue
        normalized_cookie = {k: v for k, v in cookie.items() if k in allowed_keys}
        if normalized_cookie.get("name") and normalized_cookie.get("value"):
            normalized.append(normalized_cookie)
    return normalized


def parse_time_label_to_minutes(time_label: str) -> int | None:
    if not time_label:
        return None

    label = time_label.strip()
    if not label:
        return None
    if label == "刚刚":
        return 0
    if label in {"昨天", "前天"}:
        return 24 * 60

    minute_match = re.match(r"^(\d+)分钟前$", label)
    if minute_match:
        return int(minute_match.group(1))

    hour_match = re.match(r"^(\d+)小时前$", label)
    if hour_match:
        return int(hour_match.group(1)) * 60

    day_match = re.match(r"^(\d+)天前$", label)
    if day_match:
        return int(day_match.group(1)) * 24 * 60

    return None


def is_within_window(time_label: str, lookback_hours: float) -> bool:
    minutes = parse_time_label_to_minutes(time_label)
    if minutes is None:
        return False
    return minutes <= int(lookback_hours * 60)


def should_stop_on_time_label(time_label: str, lookback_hours: float) -> bool:
    minutes = parse_time_label_to_minutes(time_label)
    if minutes is None:
        return False
    return minutes > int(lookback_hours * 60)


def build_run_stamp(now: datetime | None = None) -> str:
    current = now or datetime.now()
    return current.strftime("%Y%m%d_%H%M%S")


def choose_output_extension(settings: dict[str, Any], key: str) -> str:
    value = str(settings["output"].get(key) or "md").lower().strip(".")
    if value not in {"txt", "md"}:
        return "md"
    return value
