"""
设备认证 & Token 管理

认证方式:
  从龙虾 workspace 路径提取实例 UUID 作为稳定设备标识。
  路径格式: /data/.openclaw/workspace/<uuid>/skills/...
  同一个龙虾 → 同一个 UUID → 同一个设备 ID → 受 3 策略配额限制。
  重装 skill 不会改变设备 ID。

不采集: 主机名、操作系统、MAC 地址、IP 等任何硬件/网络信息。

Token 缓存: skill 目录下 .auth.json
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid as uuid_lib
from pathlib import Path

import httpx
from loguru import logger

from server_config import resolve_server_url

API_PREFIX = "/api/v1"

_AUTH_FILE = Path(__file__).parent.parent / ".auth.json"


def _extract_workspace_id() -> str:
    """
    从 workspace 路径提取龙虾实例的唯一 UUID。

    搜索路径链:
      1. 当前 skill 所在路径中的 UUID 段
      2. /data/.openclaw/workspace/ 下的真实目录名
      3. 兜底: 生成随机 UUID 并持久化到 .auth.json
    """
    # 策略1: 从自身路径提取 UUID
    # 例: /data/.openclaw/workspace/abc123def/skills/dex-quant-skill/scripts/machine_auth.py
    skill_path = str(Path(__file__).resolve())
    match = re.search(r'/workspace/([0-9a-f-]{8,})', skill_path)
    if match:
        return match.group(1)

    # 策略2: 扫描 /data/.openclaw/workspace/ 下的真实目录
    ws_root = Path("/data/.openclaw/workspace")
    if ws_root.is_dir():
        for d in ws_root.iterdir():
            if d.is_dir() and "${" not in d.name:
                return d.name

    # 策略3: 兜底 — 读缓存或生成新的（极端情况才走到这）
    if _AUTH_FILE.exists():
        try:
            cached = json.loads(_AUTH_FILE.read_text())
            if cached.get("device_id"):
                return cached["device_id"]
        except (json.JSONDecodeError, OSError):
            pass

    return uuid_lib.uuid4().hex


def _get_stable_device_id() -> str:
    """生成稳定的设备 ID: workspace UUID 的 SHA256 前 32 位。"""
    ws_id = _extract_workspace_id()
    return hashlib.sha256(ws_id.encode()).hexdigest()[:32]


class MachineAuth:
    """设备认证客户端"""

    def __init__(self, server_url: str | None = None):
        self.server_url = resolve_server_url(server_url).rstrip("/")
        self.base_url = self.server_url + API_PREFIX
        self._client = httpx.Client(timeout=30.0)
        self._config: dict = {}
        self._load_config()

    def _load_config(self) -> None:
        if _AUTH_FILE.exists():
            try:
                self._config = json.loads(_AUTH_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                self._config = {}

    def _save_config(self) -> None:
        _AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
        _AUTH_FILE.write_text(json.dumps(self._config, indent=2, ensure_ascii=False))

    @property
    def machine_code(self) -> str:
        return _get_stable_device_id()

    @property
    def token(self) -> str:
        return self._config.get("token", "")

    def register_or_load(self) -> str:
        """获取 Token（自动注册或读本地缓存）。"""
        if self.token:
            return self.token

        device_id = self.machine_code
        logger.info(f"首次使用，注册设备: {device_id[:8]}...")

        resp = self._client.post(
            f"{self.base_url}/auth/register",
            json={"machine_code": device_id},
        )
        resp.raise_for_status()
        data = resp.json()

        self._config["device_id"] = device_id
        self._config["token"] = data["token"]
        self._config["max_strategies"] = data["max_strategies"]
        self._save_config()

        logger.info(f"注册成功 | 配额 {data['used_strategies']}/{data['max_strategies']}")
        return data["token"]

    def check_quota(self) -> dict:
        """查询当前配额使用情况。"""
        token = self.register_or_load()
        resp = self._client.get(
            f"{self.base_url}/auth/quota",
            headers={"X-Token": token},
        )
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
