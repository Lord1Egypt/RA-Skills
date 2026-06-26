from __future__ import annotations

import html
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .constants import AUTHOR_ROLE_PATTERNS, AUTHOR_SUFFIXES, MIN_PYTHON, PRICE_TOKEN_RE


def ensure_python_version() -> None:
    if sys.version_info < MIN_PYTHON:
        required = ".".join(str(part) for part in MIN_PYTHON)
        raise RuntimeError(f"Python {required}+ is required for this skill.")


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def redact_sensitive_text(value: Any) -> str:
    text = str(value)
    text = re.sub(
        r"(?i)(access[_-]?token|refresh[_-]?token|code[_-]?verifier|authorization[_-]?code)([\"'\s:=]+)([^\"'\s,&}]+)",
        r"\1\2[redacted]",
        text,
    )
    text = re.sub(r"(?i)(Bearer\s+)[A-Za-z0-9._~+/=-]+", r"\1[redacted]", text)
    text = re.sub(r"(?i)(openid\.oa2\.authorization_code=)[^&\s]+", r"\1[redacted]", text)
    return text


def redact_sensitive_payload(payload: Any) -> Any:
    if isinstance(payload, dict):
        redacted: dict[str, Any] = {}
        for key, value in payload.items():
            normalized_key_name = re.sub(r"[^a-z0-9]", "", str(key).casefold())
            if normalized_key_name in {"accesstoken", "refreshtoken", "codeverifier", "authorizationcode"}:
                redacted[key] = "[redacted]"
            else:
                redacted[key] = redact_sensitive_payload(value)
        return redacted
    if isinstance(payload, list):
        return [redact_sensitive_payload(item) for item in payload]
    if isinstance(payload, str):
        return redact_sensitive_text(payload)
    return payload


def strip_html(value: str) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<br\s*/?>", ". ", text, flags=re.I)
    text = re.sub(r"</p>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_parentheticals(value: str) -> str:
    return re.sub(r"\((?:[^)]*)\)", " ", value or "")


def strip_combining_marks(value: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", value) if not unicodedata.combining(ch))


def normalized_key(value: str, *, ascii_only: bool = False) -> str:
    text = html.unescape(value or "").replace("&", " and ").replace("’", "'")
    text = strip_parentheticals(text)
    text = unicodedata.normalize("NFKC", text).casefold()
    if ascii_only:
        text = strip_combining_marks(text).encode("ascii", "ignore").decode("ascii")
    normalized = "".join(ch if ch.isalnum() else " " for ch in text)
    return normalize_space(normalized)


def split_author_roles(value: str) -> str:
    cleaned = normalize_space(strip_html(value))
    lowered = cleaned.casefold()
    for pattern in AUTHOR_ROLE_PATTERNS:
        match = re.search(pattern, lowered)
        if match:
            cleaned = cleaned[: match.start()].strip(" ,;-")
            lowered = cleaned.casefold()
    return normalize_space(cleaned)


def normalize_author_key(value: str, *, ascii_only: bool = False) -> str:
    cleaned = split_author_roles(value)
    normalized = normalized_key(cleaned, ascii_only=ascii_only)
    tokens = [token for token in normalized.split() if token and token not in AUTHOR_SUFFIXES]
    filtered: list[str] = []
    for index, token in enumerate(tokens):
        if len(token) == 1 and 0 < index < len(tokens) - 1:
            continue
        filtered.append(token)
    return " ".join(filtered).strip()


def parse_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).strip())
    except Exception:
        return None


def parse_rating(value: Any) -> int:
    try:
        return int(str(value or "").strip() or 0)
    except Exception:
        return 0


def parse_int_value(value: Any) -> int | None:
    text = normalize_space(str(value or "")).replace(",", "")
    if not text:
        return None
    try:
        return int(text)
    except Exception:
        return None


def parse_localized_price(raw: str | None) -> float | None:
    if raw in (None, ""):
        return None
    text = normalize_space(str(raw)).replace("\xa0", "")
    match = PRICE_TOKEN_RE.search(text)
    if not match:
        plain = re.search(r"(\d[\d.,]*)", text)
        if not plain:
            return None
        number = plain.group(1)
    else:
        number = match.group("prefix_amount") or match.group("suffix_amount") or ""
    number = number.replace(" ", "")
    if "," in number and "." in number:
        if number.rfind(",") > number.rfind("."):
            number = number.replace(".", "").replace(",", ".")
        else:
            number = number.replace(",", "")
    elif "," in number:
        number = number.replace(".", "").replace(",", ".")
    else:
        number = number.replace(",", "")
    try:
        return float(number)
    except Exception:
        return None


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def atomic_write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def write_json_atomic(path: Path, payload: Any) -> None:
    atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def prompt(text: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default not in (None, "") else ""
    raw = input(f"{text}{suffix}: ").strip()
    if raw:
        return raw
    return default or ""


def truncate_text(text: str, limit: int) -> str:
    text = normalize_space(text)
    if len(text) <= limit:
        return text
    clipped = text[: max(0, limit - 1)].rstrip(" ,;:")
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped.rstrip(" ,;:") + "…"


def approx_token_count(text: str) -> int:
    return max(0, round(len(text) / 4))


def normalize_review_text(text: str) -> str:
    cleaned = normalize_space(strip_html(text))
    return re.sub(r"([.!?])(?:\s*[.!?]){1,}", r"\1", cleaned)
