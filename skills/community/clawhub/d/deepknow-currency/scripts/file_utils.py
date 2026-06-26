from __future__ import annotations

import os
import platform
from pathlib import Path
import json


def openclaw_order_root() -> Path:
    override = os.getenv("OPENCLAW_ORDER_ROOT", "").strip()
    if override:
        return Path(override).expanduser()
    if platform.system() == "Windows":
        return Path.home() / "openclaw" / "skills" / "orders"
    return Path.home() / ".openclaw" / "skills" / "orders"


def order_root(indicator: str) -> Path:
    return openclaw_order_root() / indicator


def order_path(indicator: str, order_no: str) -> Path:
    return order_root(indicator) / f"{order_no}.json"


def save_order(indicator: str, order_no: str, payload: dict) -> Path:
    path = order_path(indicator, order_no)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_order(indicator: str, order_no: str) -> dict:
    path = order_path(indicator, order_no)
    if not path.exists():
        raise FileNotFoundError(f"order file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))
