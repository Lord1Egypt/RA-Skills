"""
Shared helpers for clean-json-toolkit.

Pure standard library. No third-party imports.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterator, List, Tuple

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def load_json(path: Path) -> Tuple[Any, str]:
    """Return (parsed_data, kind). kind is 'json' or 'jsonl'.

    Sniffs the file: if it looks like one-JSON-object-per-line, returns a
    list of those objects with kind='jsonl'. Otherwise parses as a single
    JSON document.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("\ufeff"):
        text = text[1:]
    stripped = text.lstrip()
    # If it starts with `{` or `[` and has only one top-level value, JSON.
    # Otherwise try jsonl.
    if not stripped:
        return None, "json"
    # Quick heuristic: jsonl if the first non-empty line ends with `}` and
    # there are multiple non-empty lines that all parse as JSON.
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) > 1 and stripped[0] == "{":
        try:
            objs = [json.loads(l) for l in lines]
            return objs, "jsonl"
        except json.JSONDecodeError:
            pass
    return json.loads(text), "json"


def dump_json(data: Any, indent: int = 2) -> str:
    return json.dumps(data, indent=indent, ensure_ascii=False)


def dump_jsonl(rows: List[Any]) -> str:
    return "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n"


def walk(obj: Any, prefix: str = "") -> Iterator[Tuple[str, Any]]:
    """Yield (path, value) for every leaf in a nested structure."""
    if isinstance(obj, dict):
        if not obj:
            yield (prefix or "$", obj)
            return
        for k, v in obj.items():
            key = str(k)
            safe = key if _is_simple_key(key) else f'"{key}"'
            new = f"{prefix}.{safe}" if prefix else safe
            yield from walk(v, new)
    elif isinstance(obj, list):
        if not obj:
            yield (prefix or "$", obj)
            return
        for i, v in enumerate(obj):
            new = f"{prefix}[{i}]" if prefix else f"[{i}]"
            yield from walk(v, new)
    else:
        yield (prefix or "$", obj)


def _is_simple_key(k: str) -> bool:
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", k))


def type_of(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        return "array"
    if isinstance(v, dict):
        return "object"
    return type(v).__name__
