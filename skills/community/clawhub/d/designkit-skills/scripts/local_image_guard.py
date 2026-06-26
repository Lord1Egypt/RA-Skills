#!/usr/bin/env python3
"""Validate that local uploads are supported image files."""

from __future__ import annotations

import urllib.parse
from pathlib import Path
from typing import Tuple


SUPPORTED_IMAGE_MESSAGE = "仅支持上传 JPG/JPEG/PNG/WEBP/GIF 图片文件"
FORMAT_RULES = {
    "jpeg": {
        "extensions": {".jpg", ".jpeg"},
        "mime": "image/jpeg",
    },
    "png": {
        "extensions": {".png"},
        "mime": "image/png",
    },
    "webp": {
        "extensions": {".webp"},
        "mime": "image/webp",
    },
    "gif": {
        "extensions": {".gif"},
        "mime": "image/gif",
    },
}


def normalize_local_image_path(file_path: str) -> str:
    raw = str(file_path or "").strip()
    if not raw:
        return raw

    # Strip common wrappers copied from chat/markdown.
    for _ in range(2):
        if len(raw) >= 2 and ((raw[0] == raw[-1] and raw[0] in ("'", '"', "`"))):
            raw = raw[1:-1].strip()

    # Accept file URLs from chat tools or browsers.
    if raw.lower().startswith("file://"):
        parsed = urllib.parse.urlparse(raw)
        path = urllib.parse.unquote(parsed.path or "")
        if parsed.netloc and parsed.netloc != "localhost":
            path = f"//{parsed.netloc}{path}"
        raw = path or raw

    return str(Path(raw).expanduser())


def _detect_image_kind(header: bytes) -> str | None:
    if header.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "webp"
    return None


def describe_local_image(file_path: str) -> Tuple[str, str]:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"文件不存在: {path}")

    ext = path.suffix.lower()
    if ext not in {suffix for rule in FORMAT_RULES.values() for suffix in rule["extensions"]}:
        raise ValueError(SUPPORTED_IMAGE_MESSAGE)

    with path.open("rb") as handle:
        header = handle.read(16)
    image_kind = _detect_image_kind(header)
    if image_kind is None:
        raise ValueError(SUPPORTED_IMAGE_MESSAGE)

    rule = FORMAT_RULES[image_kind]
    if ext not in rule["extensions"]:
        raise ValueError("文件扩展名与图片内容不匹配，请确认上传的是正确的图片文件")

    return image_kind, str(rule["mime"])
