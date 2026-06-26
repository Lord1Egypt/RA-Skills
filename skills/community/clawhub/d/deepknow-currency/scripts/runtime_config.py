from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_BASE_URL = "https://rate.feedai.cn"
SUPPORTED_PUBLIC_BASE_URLS = (
    "https://rate.feedai.cn",
)
SUPPORTED_QUOTE_CURRENCIES = ("USD", "EUR", "JPY", "GBP")


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def config_path() -> Path:
    return skill_root() / "config.yaml"


def strip_yaml_inline_comment(value: str) -> str:
    result: list[str] = []
    in_single_quote = False
    in_double_quote = False
    escape_next = False

    for char in value:
        if char == "#" and not in_single_quote and not in_double_quote:
            break

        result.append(char)

        if escape_next:
            escape_next = False
            continue
        if char == "\\" and in_double_quote:
            escape_next = True
            continue
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            continue
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote

    return "".join(result)


def normalize_base_url(value: str) -> str:
    normalized = value.strip().rstrip("/")
    if not normalized:
        raise ValueError("base_url is empty")

    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"invalid base_url: {value}")
    if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
        raise ValueError(f"base_url must not include path/query/fragment: {value}")

    return normalized


def read_base_url_from_config() -> str | None:
    path = config_path()
    if not path.exists():
        return None

    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        if key.strip() != "base_url":
            continue
        cleaned_value = strip_yaml_inline_comment(value).strip().strip("\"'")
        return normalize_base_url(cleaned_value)
    return None


def resolve_base_url() -> str:
    env_value = os.getenv("INKRATE_SKILL_BASE_URL", "").strip()
    config_value = read_base_url_from_config()
    return normalize_base_url(env_value or config_value or DEFAULT_BASE_URL)
