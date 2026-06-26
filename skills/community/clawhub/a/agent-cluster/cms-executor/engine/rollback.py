"""
CMS Rollback Engine - 变更追踪与回滚。
基于操作记录（OperationRecord）实现增量回滚。
"""
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from connectors.base_connector import OperationRecord, OperationStatus, OperationType

logger = logging.getLogger(__name__)


class RollbackStrategy(Enum):
    EXACT = "exact"         # 精确回滚到操作前状态
    SNAPSHOT = "snapshot"   # 基于快照回滚
    RECREATE = "recreate"   # 重建（创建替代删除）
    MANUAL = "manual"       # 需人工介入


@dataclass
class RollbackPlan:
    """回滚计划"""
    plan_id: str
    created_at: datetime
    target_record_id: str
    strategy: RollbackStrategy
    steps: List[Dict[str, Any]]
    estimated_duration: int  # 秒
    requires_approval: bool
    status: str = "planned"  # planned | executing | completed | failed


class RollbackEngine:
    """
    回滚引擎。
    支持：单步回滚 / 批量回滚 / 定时回滚 / 回滚历史审计。
    
    使用示例:
        engine = RollbackEngine(connector=wp_connector)
        
        # 查看最近变更
        changes = engine.list_recent_changes(hours=24)
        
        # 生成回滚计划（不执行）
        plan = engine.plan_rollback(record_id="abc12345")
        
        # 确认后执行
        result = engine.execute_rollback(plan_id=plan.plan_id)
    """

    def __init__(self, connector, storage_path: str = "./rollback_snapshots.json"):
        self.connector = connector  # BaseCMSConnector 实例
        self.storage_path = storage_path
        self._snapshots: Dict[str, Dict[str, Any]] = {}
        self._plans: List[RollbackPlan] = []
        self._load()

    # ── 变更查询 ───────────────────────────────────────────
    def list_recent_changes(
        self,
        hours: int = 24,
        entity_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """列出最近的变更记录"""
        cutoff = datetime.now() - timedelta(hours=hours)
        records = self.connector.get_history(limit=200)
        result = []
        for r in records:
            ts = datetime.fromisoformat(r["timestamp"])
            if ts < cutoff:
                continue
            if entity_type and r.get("entity_type") != entity_type:
                continue
            result.append(r)
        return result

    def get_operation(self, record_id: str) -> Optional[OperationRecord]:
        """根据ID获取操作记录"""
        for r in self.connector.get_history(limit=200):
            if r["id"] == record_id:
                return OperationRecord.from_dict(r)
        return None

    # ── 快照管理 ───────────────────────────────────────────
    def take_snapshot(self, entity_type: str, entity_id: int) -> str:
        """
        执行操作前拍摄快照，返回快照ID。
        快照存储在本地，格式: {snapshot_id: {entity_type, entity_id, data, timestamp}}
        """
        snapshot_id = f"snap_{entity_type}_{entity_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        try:
            data = self.connector.get_content(entity_id)
        except Exception:
            data = {}
        self._snapshots[snapshot_id] = {
            "id": snapshot_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        self._persist_snapshots()
        return snapshot_id

    def restore_snapshot(self, snapshot_id: str) -> bool:
        """从快照恢复"""
        snap = self._snapshots.get(snapshot_id)
        if not snap:
            logger.error(f"Snapshot {snapshot_id} not found")
            return False
        entity_id = snap["entity_id"]
        data = snap["data"]
        if not data:
            return False
        # 重建内容
        from connectors.base_connector import ContentPayload
        from connectors.wordpress_connector import WordPressConnector
        payload = ContentPayload(
            title=data.get("title", {}).get("rendered", ""),
            content=data.get("content", {}).get("rendered", ""),
            status=data.get("status", "draft"),
        )
        if isinstance(self.connector, WordPressConnector):
            self.connector.update_content(entity_id, payload)
        return True

    def list_snapshots(self, entity_id: Optional[int] = None) -> List[Dict[str, Any]]:
        if entity_id:
            return [s for s in self._snapshots.values() if s["entity_id"] == entity_id]
        return list(self._snapshots.values())

    # ── 回滚计划 ───────────────────────────────────────────
    def plan_rollback(
        self,
        record_id: str,
        auto_approve: bool = False,
    ) -> Optional[RollbackPlan]:
        """生成回滚计划（不执行）"""
        record = self.get_operation(record_id)
        if not record:
            return None

        steps = []
        strategy = self._determine_strategy(record)
        requires_approval = record.operation in (OperationType.DELETE,)

        # 构建回滚步骤
        if record.operation == OperationType.CREATE:
            steps.append({
                "step": 1,
                "action": "delete",
                "entity_type": record.entity_type,
                "entity_id": record.entity_id,
                "description": f"删除新创建的内容 (ID={record.entity_id})",
            })
        elif record.operation == OperationType.UPDATE:
            # 恢复原始数据
            original = record.payload
            steps.append({
                "step": 1,
                "action": "restore",
                "entity_type": record.entity_type,
                "entity_id": record.entity_id,
                "description": f"恢复 ID={record.entity_id} 到更新前状态",
                "original_data": original,
            })
        elif record.operation == OperationType.DELETE:
            # 需人工从快照恢复
            steps.append({
                "step": 1,
                "action": "manual_snapshot_restore",
                "entity_type": record.entity_type,
                "description": "需从快照手动恢复已删除内容",
            })

        plan = RollbackPlan(
            plan_id=f"plan_{record_id}_{datetime.now().strftime('%H%M%S')}",
            created_at=datetime.now(),
            target_record_id=record_id,
            strategy=strategy,
            steps=steps,
            estimated_duration=sum(s.get("estimated_seconds", 5) for s in steps),
            requires_approval=requires_approval and not auto_approve,
        )
        self._plans.append(plan)
        return plan

    def execute_rollback(self, plan_id: str, force: bool = False) -> Dict[str, Any]:
        """执行回滚计划"""
        plan = next((p for p in self._plans if p.plan_id == plan_id), None)
        if not plan:
            return {"success": False, "error": f"Plan {plan_id} not found"}

        if plan.requires_approval and not force:
            return {
                "success": False,
                "error": "Approval required before execution",
                "plan_id": plan_id,
            }

        plan.status = "executing"
        executed_steps = []
        errors = []

        for step in plan.steps:
            try:
                if step["action"] == "delete":
                    self.connector.delete_content(step["entity_id"], force=True)
                    executed_steps.append(step)
                elif step["action"] == "restore":
                    from connectors.base_connector import ContentPayload
                    payload = ContentPayload(
                        title=step.get("original_data", {}).get("title", {}).get("raw", ""),
                        content=step.get("original_data", {}).get("content", {}).get("raw", ""),
                        status=step.get("original_data", {}).get("status", "draft"),
                    )
                    self.connector.update_content(step["entity_id"], payload)
                    executed_steps.append(step)
                elif step["action"] == "manual_snapshot_restore":
                    errors.append({"step": step, "error": "Manual intervention required"})
            except Exception as e:
                errors.append({"step": step, "error": str(e)})

        plan.status = "completed" if not errors else "failed"
        return {
            "success": plan.status == "completed",
            "plan_id": plan_id,
            "executed_steps": executed_steps,
            "errors": errors,
            "status": plan.status,
        }

    def list_plans(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        plans = self._plans
        if status:
            plans = [p for p in plans if p.status == status]
        return [
            {
                "plan_id": p.plan_id,
                "target_record_id": p.target_record_id,
                "strategy": p.strategy.value,
                "status": p.status,
                "created_at": p.created_at.isoformat(),
                "requires_approval": p.requires_approval,
            }
            for p in plans
        ]

    # ── 内部 ───────────────────────────────────────────────
    def _determine_strategy(self, record: OperationRecord) -> RollbackStrategy:
        if record.operation == OperationType.DELETE:
            return RollbackStrategy.SNAPSHOT
        elif record.operation == OperationType.UPDATE:
            return RollbackStrategy.EXACT
        elif record.operation == OperationType.CREATE:
            return RollbackStrategy.RECREATE
        return RollbackStrategy.MANUAL

    def _persist_snapshots(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self._snapshots, f, ensure_ascii=False, indent=2)

    def _load(self) -> None:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self._snapshots = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._snapshots = {}
