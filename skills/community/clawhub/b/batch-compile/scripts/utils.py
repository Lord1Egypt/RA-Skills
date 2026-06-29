from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta

COMMON_MODULE_VERSION = "paperkb-v3.0"
TZ = timezone(timedelta(hours=8))


def now_str() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def today_str() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def slugify(value: str, fallback: str = "item") -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "-", text).strip("-")
    return text or fallback


def sanitize_filename(title: str, max_len: int = 90) -> str:
    name = re.sub(r'[\\/:*?"<>|\r\n\t]', " ", title or "")
    name = re.sub(r"\s+", " ", name).strip().strip(". ")
    return (name[:max_len].rstrip() if len(name) > max_len else name) or "untitled"


def normalize_for_match(text: str) -> str:
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]", "", (text or "").lower())


def json_fail(error: str, message: str) -> dict:
    return {"success": False, "error": error, "message": message}
