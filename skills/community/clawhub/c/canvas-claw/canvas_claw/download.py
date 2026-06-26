from __future__ import annotations

from pathlib import Path
from urllib import request


def download_url(url: str, destination: Path) -> Path:
    with request.urlopen(url, timeout=120) as response:
        destination.write_bytes(response.read())
    return destination


def infer_extension(url: str, fallback: str) -> str:
    candidate = Path(url.split("?", 1)[0]).suffix.lower()
    if candidate:
        return candidate
    return fallback
