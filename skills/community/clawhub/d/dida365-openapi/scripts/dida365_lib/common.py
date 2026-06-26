"""Shared helpers for the Dida365 OpenAPI CLI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Type


def json_dumps(data: Any, *, sort_keys: bool = False) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=sort_keys)


def load_json_file(path: str | Path, expected_type: Optional[Type[Any]] = None) -> Any:
    file_path = Path(path).expanduser()
    try:
        content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"JSON file not found: {file_path}") from exc
    except OSError as exc:
        raise ValueError(f"Unable to read JSON file: {file_path}") from exc
    return parse_json_text(content, label=str(file_path), expected_type=expected_type)


def parse_json_text(
    text: str,
    *,
    label: str,
    expected_type: Optional[Type[Any]] = None,
) -> Any:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} contains invalid JSON: {exc}") from exc
    if expected_type is not None and not isinstance(data, expected_type):
        raise ValueError(f"{label} must be a JSON {expected_type.__name__}")
    return data


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def omit_none(mapping: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in mapping.items() if value is not None}


def compact_list(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def merge_json_object(base: dict[str, Any], updates: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    merged.update(updates)
    return merged


def redact_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    if not value:
        return value
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def redact_mapping(data: Mapping[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    secret_keys = set(keys)
    redacted: dict[str, Any] = {}
    for key, value in data.items():
        if key in secret_keys:
            redacted[key] = redact_value(value)
        else:
            redacted[key] = value
    return redacted
