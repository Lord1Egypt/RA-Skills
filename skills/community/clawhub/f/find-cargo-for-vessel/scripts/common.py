from __future__ import annotations

import json
import math
import os
import re
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


USER_AGENT = "ShippingClaw-CargoMatcher/1.0"


def cache_dir() -> Path:
    configured = os.getenv("CARGO_MATCHER_CACHE_DIR")
    if configured:
        path = Path(configured)
    elif os.name == "nt" and os.getenv("LOCALAPPDATA"):
        path = Path(os.environ["LOCALAPPDATA"]) / "ShippingClaw" / "find-cargo-for-vessel"
    else:
        path = Path(tempfile.gettempdir()) / "shippingclaw-find-cargo-for-vessel"
    path.mkdir(parents=True, exist_ok=True)
    return path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json_cache(path: Path, ttl_seconds: int) -> Any | None:
    try:
        if time.time() - path.stat().st_mtime > ttl_seconds:
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(path)


def fetch_bytes(url: str, timeout: int = 30, attempts: int = 3) -> bytes:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/json,text/csv,*/*",
                },
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except Exception as exc:  # network failures differ by platform
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(0.5 * (2**attempt))
    raise RuntimeError(f"无法获取数据源: {url}: {last_error}") from last_error


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def haversine_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_nm = 3440.065
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return radius_nm * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
