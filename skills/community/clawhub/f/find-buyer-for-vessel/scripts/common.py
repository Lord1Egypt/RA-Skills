from __future__ import annotations

import json
import os
import re
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


USER_AGENT = "ShippingClaw-SellerBuyerMatcher/1.0"
CACHE_TTL_SECONDS = 12 * 60 * 60


def cache_dir() -> Path:
    configured = os.getenv("SELLER_BUYER_CACHE_DIR")
    if configured:
        path = Path(configured)
    elif os.name == "nt" and os.getenv("LOCALAPPDATA"):
        path = Path(os.environ["LOCALAPPDATA"]) / "ShippingClaw" / "find-buyer-for-vessel"
    else:
        path = Path(tempfile.gettempdir()) / "shippingclaw-find-buyer-for-vessel"
    path.mkdir(parents=True, exist_ok=True)
    return path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def read_json_cache(path: Path, ttl_seconds: int = CACHE_TTL_SECONDS) -> Any | None:
    try:
        if time.time() - path.stat().st_mtime > ttl_seconds:
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def fetch_bytes(url: str, timeout: int = 40, attempts: int = 3) -> bytes:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xml,*/*"},
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(0.5 * (2**attempt))
    raise RuntimeError(f"无法获取数据源: {url}: {last_error}") from last_error
