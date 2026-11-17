"""JSON 文件注册表 — 记录已安装的 CLI wrapper。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_DIR = Path.home() / ".clam"
REGISTRY_FILE = REGISTRY_DIR / "registry.json"


def _ensure_dir() -> None:
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)


def load() -> dict:
    """从磁盘加载注册表，不存在则返回空结构。"""
    if not REGISTRY_FILE.exists():
        return {"version": 1, "wrappers": {}}
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    """将注册表写入磁盘。"""
    _ensure_dir()
    REGISTRY_FILE.write_text(
        json.dumps(data, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


def register(
    app_id: str,
    app_name: str,
    sdef_path: str,
    wrapper_dir: str,
    command_count: int,
    property_count: int,
) -> None:
    """记录一个新安装的 wrapper。"""
    data = load()
    data["wrappers"][app_id] = {
        "app_name": app_name,
        "entry_point": f"clam-{app_id}",
        "sdef_path": sdef_path,
        "wrapper_dir": wrapper_dir,
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "command_count": command_count,
        "property_count": property_count,
    }
    save(data)


def unregister(app_id: str) -> bool:
    """从注册表移除 wrapper，返回是否存在。"""
    data = load()
    if app_id not in data["wrappers"]:
        return False
    del data["wrappers"][app_id]
    save(data)
    return True


def get(app_id: str) -> dict | None:
    """获取单个 wrapper 信息。"""
    data = load()
    return data["wrappers"].get(app_id)


def list_all() -> dict[str, dict]:
    """返回所有已注册的 wrapper。"""
    return load()["wrappers"]
