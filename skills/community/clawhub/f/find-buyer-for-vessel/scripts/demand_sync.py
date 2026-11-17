from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    from .common import USER_AGENT, cache_dir, utc_now_iso
except ImportError:
    from common import USER_AGENT, cache_dir, utc_now_iso


def build_payload(**values: Any) -> dict[str, Any]:
    return {**values, "queried_at": utc_now_iso()}


def _outbox_path() -> Path:
    return cache_dir() / "seller_demand_outbox.jsonl"


def _endpoint() -> str | None:
    base = os.getenv("API_BASE_URL", "").rstrip("/")
    path = os.getenv("SELLER_BUYER_DEMAND_API_PATH", "").strip()
    return base + "/" + path.lstrip("/") if base and path else None


def _queue(payload: dict[str, Any]) -> None:
    path = _outbox_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _send(payload: dict[str, Any]) -> None:
    endpoint = _endpoint()
    if not endpoint:
        raise RuntimeError("后台需求接口尚未配置")
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }
    if os.getenv("ADMIN_API_KEY"):
        headers["X-Api-Key"] = os.environ["ADMIN_API_KEY"]
    elif os.getenv("ADMIN_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['ADMIN_TOKEN']}"
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if not 200 <= response.status < 300:
                raise RuntimeError(f"后台返回HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"后台返回HTTP {exc.code}") from exc


def sync_demand(payload: dict[str, Any]) -> dict[str, Any]:
    if not _endpoint():
        _queue(payload)
        return {"status": "pending_configuration", "queued": True}
    try:
        _send(payload)
        return {"status": "synced", "queued": False}
    except Exception as exc:
        _queue(payload)
        return {"status": "queued_after_failure", "queued": True, "message": str(exc)}
