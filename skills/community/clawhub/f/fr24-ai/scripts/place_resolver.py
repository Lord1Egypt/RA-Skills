"""地名 -> IATA 三字码。"""
from __future__ import annotations

import json
import re
from pathlib import Path

PLACES_FILE = Path(__file__).resolve().parent.parent / "references" / "places.json"
IATA_RE = re.compile(r"^[A-Za-z]{3}$")


def load_places() -> dict[str, str]:
    with PLACES_FILE.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {k.strip().lower(): v.upper() for k, v in raw.items()}


def resolve_place(text: str, places: dict[str, str] | None = None) -> str | None:
    if not text or not str(text).strip():
        return None
    t = str(text).strip()
    if IATA_RE.match(t):
        return t.upper()
    table = places if places is not None else load_places()
    return table.get(t.lower()) or table.get(t)


def resolve_place_required(text: str, label: str) -> tuple[str | None, str | None]:
    code = resolve_place(text)
    if code:
        return code, None
    return None, f"无法识别{label}：{text}，请使用 IATA 三字码或常见城市名"
