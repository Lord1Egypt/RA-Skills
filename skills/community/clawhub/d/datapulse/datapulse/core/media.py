"""XHS media helpers — Referer injection and guarded download."""

from __future__ import annotations

from urllib.parse import urlparse

import requests

_REFERER_REQUIRED_DOMAINS = frozenset({
    "xhscdn.com",
    "ci.xiaohongshu.com",
    "sns-img-qc.xhscdn.com",
    "sns-video-qc.xhscdn.com",
    "sns-img-bd.xhscdn.com",
    "sns-video-bd.xhscdn.com",
})

_DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

_MAX_BYTES_DEFAULT = 10 * 1024 * 1024  # 10 MB


def needs_referer(url: str) -> bool:
    """Check if a media URL requires a Referer header to load."""
    hostname = (urlparse(url).hostname or "").lower()
    return any(hostname == d or hostname.endswith(f".{d}") for d in _REFERER_REQUIRED_DOMAINS)


def build_referer(url: str) -> str:
    """Build a minimal Referer from the URL (scheme://netloc/)."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/"


def build_media_headers(url: str) -> dict[str, str]:
    """Build request headers for a media URL, adding Referer if needed."""
    headers: dict[str, str] = {"User-Agent": _DEFAULT_UA}
    if needs_referer(url):
        headers["Referer"] = build_referer(url)
    return headers


def download_media(
    url: str,
    *,
    timeout: int = 30,
    max_bytes: int = _MAX_BYTES_DEFAULT,
) -> bytes | None:
    """Download media with appropriate headers. Returns None on failure."""
    headers = build_media_headers(url)
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, stream=True)
        resp.raise_for_status()
        chunks: list[bytes] = []
        total = 0
        for chunk in resp.iter_content(chunk_size=8192):
            total += len(chunk)
            if total > max_bytes:
                return None
            chunks.append(chunk)
        return b"".join(chunks)
    except (requests.RequestException, OSError):
        return None
