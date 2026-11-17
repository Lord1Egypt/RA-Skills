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


def build_payload(
    user_id: str,
    current_port: str,
    destination_port: str,
    capacity_tons: float,
    trade_type: str,
) -> dict[str, Any]:
    return {
        "user_id": str(user_id),
        "current_port": current_port,
        "destination_port": destination_port,
        "capacity_tons": capacity_tons,
        "trade_type": trade_type,
        "queried_at": utc_now_iso(),
    }


def _outbox_path() -> Path:
    return cache_dir() / "demand_outbox.jsonl"


def _queue(payload: dict[str, Any]) -> None:
    path = _outbox_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _configured_endpoint() -> str | None:
    base = os.getenv("API_BASE_URL", "").rstrip("/")
    path = os.getenv("CARGO_DEMAND_API_PATH", "").strip()
    if not base or not path:
        return None
    return base + "/" + path.lstrip("/")


def send_payload(payload: dict[str, Any]) -> None:
    endpoint = _configured_endpoint()
    if not endpoint:
        raise RuntimeError("后台需求接口尚未配置")
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }
    api_key = os.getenv("ADMIN_API_KEY")
    token = os.getenv("ADMIN_TOKEN")
    if api_key:
        headers["X-Api-Key"] = api_key
    elif token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if not 200 <= response.status < 300:
                raise RuntimeError(f"后台返回 HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"后台返回 HTTP {exc.code}") from exc


def flush_outbox() -> dict[str, int]:
    path = _outbox_path()
    if not path.exists() or not _configured_endpoint():
        return {"sent": 0, "remaining": _count_lines(path)}
    payloads: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payloads.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    remaining: list[dict[str, Any]] = []
    sent = 0
    for index, payload in enumerate(payloads):
        try:
            send_payload(payload)
            sent += 1
        except Exception:
            remaining.extend(payloads[index:])
            break
    if remaining:
        path.write_text(
            "".join(
                json.dumps(payload, ensure_ascii=False) + "\n"
                for payload in remaining
            ),
            encoding="utf-8",
        )
    else:
        path.unlink(missing_ok=True)
    return {"sent": sent, "remaining": len(remaining)}


def _count_lines(path: Path) -> int:
    try:
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line)
    except FileNotFoundError:
        return 0


def sync_demand(payload: dict[str, Any]) -> dict[str, Any]:
    endpoint = _configured_endpoint()
    if not endpoint:
        _queue(payload)
        return {
            "status": "pending_configuration",
            "queued": True,
            "message": "后台需求接口尚未配置，已写入本地待同步队列",
        }
    flush_result = flush_outbox()
    try:
        send_payload(payload)
        return {
            "status": "synced",
            "queued": False,
            "flushed_before_current": flush_result["sent"],
        }
    except Exception as exc:
        _queue(payload)
        return {
            "status": "queued_after_failure",
            "queued": True,
            "message": str(exc),
        }
