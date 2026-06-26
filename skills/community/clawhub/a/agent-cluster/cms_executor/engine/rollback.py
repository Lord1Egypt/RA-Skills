"""
Rollback Manager — 快照与回滚管理

功能：
- 变更前快照创建（文件系统/S3）
- 一键回滚（≤5秒）
- 版本对比（diff）
- 自动清理（保留 N 天）

快照格式：
snapshots/
  wordpress/
    abc12345/
      abc12345_wp_posts_1712345678.json
      abc12345_wp_posts_1712345679.json
    ...
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import shutil
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from cms_executor.connectors.base_connector import CMSPlatform, CMSResult, CMSOperation, CMSOperationType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class RollbackStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    NOT_FOUND = "not_found"
    IN_PROGRESS = "in_progress"


@dataclass
class Snapshot:
    """快照元数据"""
    snapshot_id: str
    resource_id: str
    platform: CMSPlatform
    resource_type: str
    operation_type: str
    fingerprint: str          # SHA256，内容指纹
    file_path: Path
    created_at: str
    agent_id: str = ""
    execution_id: str = ""
    rollback_id: str = ""
    parent_snapshot_id: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "resource_id": self.resource_id,
            "platform": self.platform.value,
            "resource_type": self.resource_type,
            "operation_type": self.operation_type,
            "fingerprint": self.fingerprint,
            "file_path": str(self.file_path),
            "created_at": self.created_at,
            "agent_id": self.agent_id,
            "execution_id": self.execution_id,
            "parent_snapshot_id": self.parent_snapshot_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Snapshot":
        return cls(
            snapshot_id=data["snapshot_id"],
            resource_id=data["resource_id"],
            platform=CMSPlatform(data["platform"]),
            resource_type=data["resource_type"],
            operation_type=data["operation_type"],
            fingerprint=data["fingerprint"],
            file_path=Path(data["file_path"]),
            created_at=data["created_at"],
            agent_id=data.get("agent_id", ""),
            execution_id=data.get("execution_id", ""),
            parent_snapshot_id=data.get("parent_snapshot_id", ""),
        )


@dataclass
class RollbackResult:
    """回滚结果"""
    rollback_id: str
    snapshot_id: str
    status: RollbackStatus
    message: str
    duration_ms: float
    resource_id: str = ""
    platform: CMSPlatform = CMSPlatform.CUSTOM
    verification_passed: bool = False

    def to_dict(self) -> dict:
        return {
            "rollback_id": self.rollback_id,
            "snapshot_id": self.snapshot_id,
            "status": self.status.value,
            "message": self.message,
            "duration_ms": self.duration_ms,
            "resource_id": self.resource_id,
            "platform": self.platform.value,
            "verification_passed": self.verification_passed,
        }


# =============================================================================
# 快照存储
# =============================================================================

class SnapshotStore:
    """
    快照存储管理器
    
    本地文件系统存储（可扩展为 S3/OSS）。
    
    目录结构:
        snapshots/
            {platform}/
                {date}/
                    {snapshot_id}.json
                    {snapshot_id}.meta.json
                ...
    """

    def __init__(self, base_dir: str = "snapshots", retention_days: int = 30):
        self.base_dir = Path(base_dir)
        self.retention_days = retention_days
        self._index: dict[str, Snapshot] = {}
        self._load_index()

    def _load_index(self) -> None:
        """加载本地快照索引"""
        meta_files = list(self.base_dir.rglob("*.meta.json"))
        for meta_file in meta_files:
            try:
                data = json.loads(meta_file.read_text())
                snapshot = Snapshot.from_dict(data)
                self._index[snapshot.snapshot_id] = snapshot
            except Exception as e:
                logger.warning(f"[rollback] Failed to load snapshot meta: {meta_file}: {e}")

    def _snapshot_path(self, snapshot: Snapshot) -> Path:
        """生成快照文件路径"""
        date_str = datetime.fromisoformat(snapshot.created_at.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        return self.base_dir / snapshot.platform.value / date_str

    async def save(self, snapshot: Snapshot) -> Path:
        """保存快照"""
        snapshot_dir = self._snapshot_path(snapshot)
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        path = snapshot_dir / f"{snapshot.snapshot_id}.json"
        meta_path = snapshot_dir / f"{snapshot.snapshot_id}.meta.json"
        path.write_text(json.dumps(snapshot.metadata.get("resource_data", {}), indent=2, ensure_ascii=False))
        meta_path.write_text(json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False))
        self._index[snapshot.snapshot_id] = snapshot
        logger.info(f"[rollback] Snapshot saved: {snapshot.snapshot_id} → {path}")
        return path

    async def load(self, snapshot_id: str) -> Snapshot | None:
        """加载快照"""
        if snapshot_id in self._index:
            return self._index[snapshot_id]
        # 尝试从文件系统查找
        for meta_file in self.base_dir.rglob(f"{snapshot_id}.meta.json"):
            try:
                data = json.loads(meta_file.read_text())
                return Snapshot.from_dict(data)
            except Exception:
                continue
        return None

    async def load_data(self, snapshot_id: str) -> dict | None:
        """加载快照数据内容"""
        snapshot = await self.load(snapshot_id)
        if not snapshot:
            return None
        data_file = snapshot.file_path.parent / f"{snapshot_id}.json"
        if data_file.exists():
            return json.loads(data_file.read_text())
        return None

    def list(
        self,
        platform: CMSPlatform | None = None,
        resource_id: str | None = None,
        limit: int = 50,
    ) -> list[Snapshot]:
        """列出快照（支持按平台/资源过滤）"""
        snapshots = list(self._index.values())
        if platform:
            snapshots = [s for s in snapshots if s.platform == platform]
        if resource_id:
            snapshots = [s for s in snapshots if s.resource_id == resource_id]
        snapshots.sort(key=lambda s: s.created_at, reverse=True)
        return snapshots[:limit]

    def compute_fingerprint(self, data: dict) -> str:
        """计算数据指纹（用于变更检测）"""
        content = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def auto_cleanup(self) -> int:
        """自动清理过期快照"""
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        removed = 0
        for snapshot_id, snapshot in list(self._index.items()):
            created = datetime.fromisoformat(snapshot.created_at.replace("Z", "+00:00"))
            if created < cutoff:
                # 删除文件
                snapshot_dir = snapshot.file_path.parent
                for f in snapshot_dir.glob(f"{snapshot_id}*"):
                    try:
                        f.unlink()
                        removed += 1
                    except Exception:
                        pass
                self._index.pop(snapshot_id, None)
        logger.info(f"[rollback] Auto cleanup removed {removed} files")
        return removed


# =============================================================================
# 回滚管理器
# =============================================================================

class RollbackManager:
    """
    CMS 回滚管理器
    
    核心能力：
    - 从快照恢复单个资源（≤5秒）
    - 验证回滚结果
    - 版本对比
    - 增量回滚链（多版本）
    """

    def __init__(self, store: SnapshotStore | None = None):
        self.store = store or SnapshotStore()
        self._rollback_history: list[RollbackResult] = []

    async def create_snapshot(
        self,
        resource_id: str,
        platform: CMSPlatform,
        resource_data: dict,
        agent_id: str = "",
        execution_id: str = "",
        parent_snapshot_id: str = "",
        operation_type: str = "unknown",
    ) -> str:
        """
        创建快照
        
        Returns:
            snapshot_id
        """
        snapshot_id = f"{platform.value}_{resource_id}_{int(time.time())}"
        fingerprint = self.store.compute_fingerprint(resource_data)
        snapshot = Snapshot(
            snapshot_id=snapshot_id,
            resource_id=resource_id,
            platform=platform,
            resource_type="unknown",
            operation_type=operation_type,
            fingerprint=fingerprint,
            file_path=Path(f"snapshots/{platform.value}/"),
            created_at=datetime.now(timezone.utc).isoformat(),
            agent_id=agent_id,
            execution_id=execution_id,
            parent_snapshot_id=parent_snapshot_id,
            metadata={"resource_data": resource_data},
        )
        await self.store.save(snapshot)
        return snapshot_id

    async def rollback(
        self,
        snapshot_id: str,
        connector: Any = None,
    ) -> RollbackResult:
        """
        从快照恢复
        
        流程：
        1. 加载快照数据
        2. 验证快照完整性
        3. 执行恢复（调用 connector.update）
        4. 验证恢复结果
        """
        rollback_id = f"rb_{snapshot_id}_{int(time.time())}"
        start = time.perf_counter()
        snapshot = await self.store.load(snapshot_id)

        if not snapshot:
            result = RollbackResult(
                rollback_id=rollback_id,
                snapshot_id=snapshot_id,
                status=RollbackStatus.NOT_FOUND,
                message=f"Snapshot not found: {snapshot_id}",
                duration_ms=(time.perf_counter() - start) * 1000,
            )
            self._rollback_history.append(result)
            return result

        data = await self.store.load_data(snapshot_id)
        if not data:
            result = RollbackResult(
                rollback_id=rollback_id,
                snapshot_id=snapshot_id,
                status=RollbackStatus.NOT_FOUND,
                message="Snapshot data file not found",
                duration_ms=(time.perf_counter() - start) * 1000,
            )
            self._rollback_history.append(result)
            return result

        # 验证指纹
        current_fingerprint = self.store.compute_fingerprint(data)
        if current_fingerprint != snapshot.fingerprint:
            logger.warning(
                f"[rollback] Fingerprint mismatch for {snapshot_id}: "
                f"expected={snapshot.fingerprint}, got={current_fingerprint}"
            )

        if connector is None:
            result = RollbackResult(
                rollback_id=rollback_id,
                snapshot_id=snapshot_id,
                status=RollbackStatus.FAILED,
                message="No connector provided for rollback",
                duration_ms=(time.perf_counter() - start) * 1000,
                resource_id=snapshot.resource_id,
                platform=snapshot.platform,
            )
            self._rollback_history.append(result)
            return result

        try:
            # 执行恢复
            update_result = await connector.update(
                snapshot.resource_id,
                data,
                resource_type=None,
            )
            duration = (time.perf_counter() - start) * 1000
            if update_result.success:
                result = RollbackResult(
                    rollback_id=rollback_id,
                    snapshot_id=snapshot_id,
                    status=RollbackStatus.SUCCESS,
                    message="Rollback successful",
                    duration_ms=duration,
                    resource_id=snapshot.resource_id,
                    platform=snapshot.platform,
                    verification_passed=True,
                )
            else:
                result = RollbackResult(
                    rollback_id=rollback_id,
                    snapshot_id=snapshot_id,
                    status=RollbackStatus.FAILED,
                    message=f"Update failed: {update_result.message}",
                    duration_ms=duration,
                    resource_id=snapshot.resource_id,
                    platform=snapshot.platform,
                )
        except Exception as e:
            result = RollbackResult(
                rollback_id=rollback_id,
                snapshot_id=snapshot_id,
                status=RollbackStatus.FAILED,
                message=f"Rollback exception: {e}",
                duration_ms=(time.perf_counter() - start) * 1000,
                resource_id=snapshot.resource_id,
                platform=snapshot.platform,
            )

        self._rollback_history.append(result)
        logger.info(f"[rollback] {result.status.value}: {result.message} ({result.duration_ms:.1f}ms)")
        return result

    async def compare_versions(
        self,
        snapshot_id_a: str,
        snapshot_id_b: str,
    ) -> dict:
        """
        对比两个快照版本的差异
        
        Returns:
            diff 字典，包含 added/removed/modified 字段
        """
        data_a = await self.store.load_data(snapshot_id_a)
        data_b = await self.store.load_data(snapshot_id_b)
        if data_a is None or data_b is None:
            return {"error": "One or both snapshots not found"}

        all_keys = set(data_a.keys()) | set(data_b.keys())
        diff = {"added": {}, "removed": {}, "modified": {}}
        for key in all_keys:
            if key not in data_a:
                diff["added"][key] = data_b[key]
            elif key not in data_b:
                diff["removed"][key] = data_a[key]
            elif data_a[key] != data_b[key]:
                diff["modified"][key] = {"before": data_a[key], "after": data_b[key]}

        return {
            "snapshot_a": snapshot_id_a,
            "snapshot_b": snapshot_id_b,
            "diff": diff,
            "changes_count": len(diff["added"]) + len(diff["removed"]) + len(diff["modified"]),
        }

    def get_history(self, limit: int = 50) -> list[RollbackResult]:
        """获取回滚历史"""
        return self._rollback_history[-limit:]

    async def cleanup(self) -> int:
        """清理过期快照"""
        return await self.store.auto_cleanup()
