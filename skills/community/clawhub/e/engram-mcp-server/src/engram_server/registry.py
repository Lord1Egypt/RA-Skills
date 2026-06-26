from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


REGISTRY_URL = (
    "https://raw.githubusercontent.com/DazhuangJammy/Engram/main/registry.json"
)

_LIST_ALL_QUERIES = {
    "",
    "*",
    "all",
    "any",
    "list",
    "everything",
    "engram",
    "engrams",
    "expert",
    "experts",
    "全部",
    "所有",
    "列表",
}


def fetch_registry() -> list[dict]:
    try:
        with urlopen(REGISTRY_URL, timeout=30) as response:  # nosec: B310
            payload = response.read().decode("utf-8")
    except (OSError, URLError, TimeoutError):
        return []

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def load_registry_file(path: Path | str) -> list[dict]:
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return []
    try:
        payload = file_path.read_text(encoding="utf-8")
    except OSError:
        return []

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def merge_registry_entries(*entry_sets: list[dict]) -> list[dict]:
    """Merge registry entries, allowing later sets to override earlier ones by name."""
    merged: list[dict] = []
    index_by_name: dict[str, int] = {}

    for entries in entry_sets:
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name", "")).strip()
            if not name:
                continue
            normalized = dict(entry)
            normalized["name"] = name
            key = name.lower()
            if key in index_by_name:
                merged[index_by_name[key]] = normalized
            else:
                index_by_name[key] = len(merged)
                merged.append(normalized)
    return merged


def search_registry(query: str, entries: list[dict]) -> list[dict]:
    q = query.strip().lower()
    if q in _LIST_ALL_QUERIES:
        return entries

    tokens = [token for token in re.split(r"\s+", q) if token]
    if not tokens:
        return entries

    scored: list[tuple[int, dict]] = []
    for entry in entries:
        name = str(entry.get("name", "")).strip()
        description = str(entry.get("description", "")).strip()
        tags = entry.get("tags", [])
        if not isinstance(tags, list):
            tags = [str(tags)]
        tags_text = " ".join(str(tag).strip() for tag in tags if str(tag).strip())

        name_l = name.lower()
        desc_l = description.lower()
        tags_l = [str(tag).strip().lower() for tag in tags if str(tag).strip()]
        haystack = f"{name_l} {desc_l} {' '.join(tags_l)}"

        if not all(token in haystack for token in tokens):
            continue

        score = 0
        for token in tokens:
            if token == name_l:
                score += 12
            elif name_l.startswith(token):
                score += 8
            elif token in name_l:
                score += 6

            if token in tags_l:
                score += 5
            elif any(token in tag for tag in tags_l):
                score += 4

            if token in desc_l:
                score += 2

        score += min(len(tags_text), 60) // 20
        scored.append((score, entry))

    scored.sort(key=lambda item: (-item[0], str(item[1].get("name", "")).lower()))
    return [entry for _, entry in scored]


def resolve_name(name: str, entries: list[dict]) -> str | None:
    for entry in entries:
        if entry.get("name") == name:
            source = entry.get("source")
            if isinstance(source, str) and source.strip():
                return source
            return None

    lowered = name.strip().lower()
    for entry in entries:
        entry_name = entry.get("name")
        if isinstance(entry_name, str) and entry_name.lower() == lowered:
            source = entry.get("source")
            if isinstance(source, str) and source.strip():
                return source
            return None
    return None
