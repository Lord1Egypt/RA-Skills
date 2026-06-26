#!/usr/bin/env python3
"""Shared helpers for Artifact Deck."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

MAX_BULLETS = 6


def ensure_existing_path(raw_path: str, label: str) -> Path:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"{label} does not exist: {path}")
    return path


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_section_spec(spec: str) -> tuple[str, str]:
    if "=" not in spec:
        raise ValueError(f"Expected TITLE=PATH, got: {spec}")
    title, raw_path = spec.split("=", 1)
    title = title.strip()
    raw_path = raw_path.strip()
    if not title or not raw_path:
        raise ValueError(f"Expected TITLE=PATH, got: {spec}")
    return title, raw_path


def parse_slide_spec(spec: str) -> Dict[str, Any]:
    if "=" not in spec:
        raise ValueError(f"Expected TITLE=bullet one|bullet two, got: {spec}")
    title, raw_bullets = spec.split("=", 1)
    title = title.strip()
    bullets = [item.strip() for item in raw_bullets.split("|") if item.strip()]
    if not title or not bullets:
        raise ValueError(f"Expected TITLE=bullet one|bullet two, got: {spec}")
    return {"title": title, "bullets": bullets[:MAX_BULLETS], "source": "inline"}


def parse_image_spec(spec: str) -> Dict[str, str]:
    if "=" not in spec:
        raise ValueError(f"Expected TITLE=PATH|CAPTION, got: {spec}")
    title, raw = spec.split("=", 1)
    title = title.strip()
    path_part, _, caption = raw.partition("|")
    path_part = path_part.strip()
    caption = caption.strip()
    if not title or not path_part:
        raise ValueError(f"Expected TITLE=PATH|CAPTION, got: {spec}")
    return {"title": title, "path": path_part, "caption": caption}


def normalize_bullet(line: str) -> str:
    text = line.strip()
    text = re.sub(r"^[-*+]\s+", "", text)
    text = re.sub(r"^\d+[.)]\s+", "", text)
    return text.strip()


def bullets_from_markdown(path: Path, limit: int = MAX_BULLETS) -> List[str]:
    bullets: List[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        cleaned = normalize_bullet(stripped)
        if not cleaned:
            continue
        bullets.append(cleaned)
        if len(bullets) >= limit:
            break
    return bullets


def slide_titles(manifest: Dict[str, Any]) -> List[str]:
    titles = [str(manifest.get("title") or "").strip()]
    for slide in manifest.get("slides") or []:
        title = str(slide.get("title") or "").strip()
        if title:
            titles.append(title)
    for image in manifest.get("images") or []:
        title = str(image.get("title") or "").strip()
        if title:
            titles.append(title)
    return [title for title in titles if title]
