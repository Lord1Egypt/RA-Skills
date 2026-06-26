from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests

ROADSHOW_DETAIL_API = "https://roadshow.lvb.eastmoney.com/LVB/api/Roadshow/Detail"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)


class EastMoneyError(Exception):
    pass


@dataclass
class ParsedPage:
    url: str
    channel_id: str
    html_title: Optional[str]
    metadata: Dict[str, Any]
    media_candidates: List[Dict[str, Any]]
    subtitle_candidates: List[Dict[str, Any]]
    notes: List[str]


def validate_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise EastMoneyError("URL must use http or https")
    if parsed.netloc != "roadshow.eastmoney.com":
        raise EastMoneyError("Only roadshow.eastmoney.com public URLs are supported")
    m = re.fullmatch(r"/luyan/(\d+)", parsed.path)
    if not m:
        raise EastMoneyError("Only public roadshow URLs like https://roadshow.eastmoney.com/luyan/5149204 are supported")
    return m.group(1)


def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _jsonp_to_obj(text: str) -> Dict[str, Any]:
    text = text.strip()
    m = re.match(r"^[^(]+\((.*)\);?$", text, re.S)
    if not m:
        raise EastMoneyError("Unexpected JSONP payload")
    return json.loads(m.group(1))


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT, "Referer": "https://roadshow.eastmoney.com/"})
    return s


def fetch_page(url: str, timeout: int = 20) -> ParsedPage:
    channel_id = validate_url(url)
    notes: List[str] = []
    s = _session()

    html_resp = s.get(url, timeout=timeout)
    html_resp.raise_for_status()
    html = html_resp.text
    title_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    html_title = title_match.group(1).strip() if title_match else None

    params = {
        "callback": "cbskill",
        "device_id": _md5("35dkmnjhbgtyhjko"),
        "version": "1.0.0",
        "plat": "Web",
        "product": "EastMoney",
        "network": "Wifi",
        "ctoken": "",
        "utoken": "",
        "model": "pc",
        "osversion": "1.0",
        "channel_id": channel_id,
    }
    api_resp = s.get(ROADSHOW_DETAIL_API, params=params, timeout=timeout)
    api_resp.raise_for_status()
    payload = _jsonp_to_obj(api_resp.text)
    if int(payload.get("result", 0)) != 1 or not payload.get("data"):
        raise EastMoneyError(f"Roadshow detail API failed: {payload.get('message', 'unknown error')}")

    data = payload["data"]
    media_candidates = _extract_media_candidates(data)
    subtitle_candidates = _extract_subtitle_candidates(data)
    if not subtitle_candidates:
        notes.append("No subtitle endpoint was discovered from public page/API fields.")
    if not media_candidates:
        notes.append("No playable media URL was discovered from public page/API fields.")
    return ParsedPage(
        url=url,
        channel_id=channel_id,
        html_title=html_title,
        metadata=data,
        media_candidates=media_candidates,
        subtitle_candidates=subtitle_candidates,
        notes=notes,
    )


def _extract_media_candidates(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    chapters = data.get("playback_chapter") or []
    for idx, chapter in enumerate(chapters):
        for group in chapter.get("media_group") or []:
            media = group.get("media") or {}
            url = media.get("url")
            if not url:
                continue
            out.append(
                {
                    "source": "playback_chapter",
                    "chapter_index": idx,
                    "format": media.get("format") or group.get("format"),
                    "av_type": group.get("av_type"),
                    "duration_seconds": media.get("duration"),
                    "size_bytes": media.get("size"),
                    "width": media.get("width"),
                    "height": media.get("height"),
                    "url": url.replace("http://", "https://", 1),
                }
            )
    return out


def _extract_subtitle_candidates(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []

    def walk(obj: Any, path: str = "root") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                p = f"{path}.{k}"
                if isinstance(v, str):
                    lower = v.lower()
                    if any(token in lower for token in [".vtt", ".srt", "subtitle", "caption", "transcript"]):
                        found.append({"source": p, "url": v})
                walk(v, p)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")

    walk(data)
    uniq = []
    seen = set()
    for item in found:
        key = (item["source"], item["url"])
        if key not in seen:
            uniq.append(item)
            seen.add(key)
    return uniq
