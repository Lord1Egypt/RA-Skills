"""
State Synchronization - Agent间状态同步机制

功能：
- 跨Agent共享状态管理
- 状态变更订阅与通知
- 最终一致性保证
- 状态快照与回溯
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 枚举与数据模型
# =============================================================================

class SyncStatus(Enum):
    """同步状态"""
    SYNCED = "synced"
    PENDING = "pending"
    CONFLICT = "conflict"
    STALE = "stale"           # 过期数据


@dataclass
class StateEntry:
    """状态条目"""
    key: str
    value: Any
    version: int = 1
    agent_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    ttl_seconds: float = 300.0   # 默认5分钟过期
    sync_status: SyncStatus = SyncStatus.SYNCED

    def is_expired(self) -> bool:
        elapsed = (datetime.now() - datetime.fromisoformat(self.timestamp)).total_seconds()
        return elapsed > self.ttl_seconds

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
            "version": self.version,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "ttl_seconds": self.ttl_seconds,
            "sync_status": self.sync_status.value,
        }


@dataclass
class StateSnapshot:
    """状态快照"""
    snapshot_id: str
    timestamp: str
    request_id: str
    agent_states: dict[str, dict]
    shared_context: dict[str, Any]


# =============================================================================
# 状态变更订阅
# =============================================================================

@dataclass
class Subscription:
    """状态变更订阅"""
    subscription_id: str
    key_pattern: str          # 支持通配符 * ?
    callback: Callable[[str, Any, StateEntry], None]
    subscriber: str           # 订阅者名称
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


# =============================================================================
# 共享状态管理器
# =============================================================================

class SharedStateManager:
    """
    Agent间共享状态管理器

    特性：
    - K-V存储，支持TTL
    - 版本控制
    - 变更订阅/通知
    - 快照保存
    - 并发安全（asyncio锁）
    """

    def __init__(self, agent_id: str = "system"):
        self.agent_id = agent_id
        self._store: dict[str, StateEntry] = {}
        self._snapshots: list[StateSnapshot] = []
        self._subscriptions: list[Subscription] = []
        self._lock = asyncio.Lock()
        self._version_counter: dict[str, int] = {}

    # ================================================================
    # 核心读写操作
    # ================================================================

    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: float = 300.0,
        agent_id: Optional[str] = None,
    ) -> StateEntry:
        """设置状态值"""
        async with self._lock:
            # 版本递增
            self._version_counter[key] = self._version_counter.get(key, 0) + 1
            version = self._version_counter[key]

            entry = StateEntry(
                key=key,
                value=value,
                version=version,
                agent_id=agent_id or self.agent_id,
                timestamp=datetime.now().isoformat(),
                ttl_seconds=ttl_seconds,
                sync_status=SyncStatus.SYNCED,
            )
            old_entry = self._store.get(key)
            self._store[key] = entry

            # 触发订阅通知
            await self._notify_subscribers(key, value, entry)

            logger.debug(f"[状态同步] SET {key}={value} (v{version}, {agent_id or self.agent_id})")
            return entry

    async def get(self, key: str, default: Any = None) -> Any:
        """获取状态值（自动清理过期数据）"""
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default
            if entry.is_expired():
                del self._store[key]
                return default
            return entry.value

    async def get_entry(self, key: str) -> Optional[StateEntry]:
        """获取完整状态条目"""
        async with self._lock:
            entry = self._store.get(key)
            if entry and not entry.is_expired():
                return entry
            return None

    async def delete(self, key: str) -> bool:
        """删除状态"""
        async with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    async def get_many(self, keys: list[str]) -> dict[str, Any]:
        """批量获取"""
        result = {}
        for key in keys:
            val = await self.get(key)
            if val is not None:
                result[key] = val
        return result

    async def set_many(self, entries: dict[str, Any], ttl_seconds: float = 300.0):
        """批量设置"""
        for key, value in entries.items():
            await self.set(key, value, ttl_seconds=ttl_seconds)

    # ================================================================
    # 版本控制
    # ================================================================

    async def get_version(self, key: str) -> int:
        """获取当前版本号"""
        return self._version_counter.get(key, 0)

    async def check_version(self, key: str, expected_version: int) -> bool:
        """乐观锁版本检查"""
        current = await self.get_version(key)
        return current == expected_version

    # ================================================================
    # 批量/范围操作
    # ================================================================

    async def keys(self, pattern: str = "*") -> list[str]:
        """查询匹配的key（支持*和?通配符）"""
        import fnmatch
        async with self._lock:
            return [k for k in self._store if fnmatch.fnmatch(k, pattern)]

    async def all_entries(self) -> dict[str, StateEntry]:
        """获取所有未过期的状态"""
        async with self._lock:
            now = datetime.now()
            result = {}
            for key, entry in list(self._store.items()):
                if not entry.is_expired():
                    result[key] = entry
                else:
                    del self._store[key]
            return result

    async def cleanup_expired(self):
        """清理过期数据"""
        async with self._lock:
            expired = [k for k, e in self._store.items() if e.is_expired()]
            for k in expired:
                del self._store[k]
            if expired:
                logger.info(f"[状态同步] 清理了 {len(expired)} 个过期条目")

    # ================================================================
    # 订阅机制
    # ================================================================

    def subscribe(
        self,
        key_pattern: str,
        callback: Callable[[str, Any, StateEntry], None],
        subscriber: str = "",
    ) -> str:
        """订阅状态变更"""
        sub_id = str(uuid.uuid4())
        sub = Subscription(
            subscription_id=sub_id,
            key_pattern=key_pattern,
            callback=callback,
            subscriber=subscriber or self.agent_id,
        )
        self._subscriptions.append(sub)
        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """取消订阅"""
        for i, sub in enumerate(self._subscriptions):
            if sub.subscription_id == subscription_id:
                del self._subscriptions[i]
                return True
        return False

    async def _notify_subscribers(self, key: str, value: Any, entry: StateEntry):
        """通知所有匹配的订阅者"""
        import fnmatch
        for sub in self._subscriptions:
            if fnmatch.fnmatch(key, sub.key_pattern):
                try:
                    if asyncio.iscoroutinefunction(sub.callback):
                        await sub.callback(key, value, entry)
                    else:
                        sub.callback(key, value, entry)
                except Exception as e:
                    logger.error(f"[状态同步] 订阅回调异常 {sub.subscriber}: {e}")

    # ================================================================
    # 快照管理
    # ================================================================

    async def save_snapshot(self, request_id: str) -> StateSnapshot:
        """保存当前状态快照"""
        async with self._lock:
            snapshot = StateSnapshot(
                snapshot_id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                request_id=request_id,
                agent_states={},  # 可扩展：各Agent独立状态
                shared_context={k: e.value for k, e in self._store.items() if not e.is_expired()},
            )
            self._snapshots.append(snapshot)
            # 保留最近50个快照
            if len(self._snapshots) > 50:
                self._snapshots = self._snapshots[-50:]
            return snapshot

    async def restore_snapshot(self, snapshot_id: str) -> bool:
        """从快照恢复状态"""
        async with self._lock:
            snapshot = next((s for s in self._snapshots if s.snapshot_id == snapshot_id), None)
            if not snapshot:
                return False
            for key, value in snapshot.shared_context.items():
                self._store[key] = StateEntry(
                    key=key,
                    value=value,
                    agent_id="snapshot_restore",
                    timestamp=snapshot.timestamp,
                )
            logger.info(f"[状态同步] 从快照 {snapshot_id} 恢复了 {len(snapshot.shared_context)} 条状态")
            return True

    def get_snapshots(self, request_id: Optional[str] = None, limit: int = 10) -> list[StateSnapshot]:
        """获取快照列表"""
        snaps = self._snapshots
        if request_id:
            snaps = [s for s in snaps if s.request_id == request_id]
        return snaps[-limit:]

    def export_state(self) -> str:
        """导出当前状态（JSON）"""
        return json.dumps(
            {k: e.to_dict() for k, e in self._store.items()},
            ensure_ascii=False,
            indent=2,
        )
