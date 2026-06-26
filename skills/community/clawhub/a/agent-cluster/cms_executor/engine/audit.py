"""
CMS Audit Logger — CMS 专用审计日志

扩展 agent-cluster/safety/audit_logger.py 的能力，
针对 CMS 写操作提供专项审计：
- CMS_CONNECT / CMS_DISCONNECT
- CMS_READ / CMS_WRITE（核心事件）
- CMS_APPROVAL / CMS_ROLLBACK
- CMS_SANDBOX

Features:
- 实时写入（JSONL 格式）
- SOC 2 合规报告
- 变更溯源（before/after snapshot 关联）
- Agent 执行链路追踪
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

from cms_executor.connectors.base_connector import (
    CMSOperation,
    CMSResult,
    CMSPlatform,
    RiskLevel,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# CMS 审计事件类型
# =============================================================================

class CMSEventType:
    """CMS 专项事件类型（扩展通用事件类型）"""
    CMS_CONNECT = "cms_connect"
    CMS_DISCONNECT = "cms_disconnect"
    CMS_READ = "cms_read"
    CMS_WRITE = "cms_write"
    CMS_APPROVAL = "cms_approval"
    CMS_ROLLBACK = "cms_rollback"
    CMS_SANDBOX = "cms_sandbox"
    CMS_SNAPSHOT = "cms_snapshot"
    CMS_ERROR = "cms_error"


# =============================================================================
# CMS 审计记录
# =============================================================================

class CMSAuditRecord:
    """CMS 审计记录"""

    def __init__(
        self,
        event_type: str,
        platform: CMSPlatform,
        operation_id: str,
        resource_id: str,
        operation_type: str,
        risk_level: RiskLevel,
        agent_id: str,
        trace_id: str = "",
        execution_id: str = "",
        snapshot_id: str = "",
        approval_id: str = "",
        result: dict | None = None,
        error: str = "",
        duration_ms: float = 0.0,
        metadata: dict | None = None,
    ):
        self.record_id = f"cms_{event_type}_{operation_id[:16]}_{int(datetime.now(timezone.utc).timestamp())}"
        self.event_type = event_type
        self.platform = platform
        self.operation_id = operation_id
        self.resource_id = resource_id
        self.operation_type = operation_type
        self.risk_level = risk_level
        self.agent_id = agent_id
        self.trace_id = trace_id or os.environ.get("TRACE_ID", "")
        self.execution_id = execution_id
        self.snapshot_id = snapshot_id
        self.approval_id = approval_id
        self.result = result or {}
        self.error = error
        self.duration_ms = duration_ms
        self.metadata = metadata or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "event_type": self.event_type,
            "platform": self.platform.value,
            "operation_id": self.operation_id,
            "resource_id": self.resource_id,
            "operation_type": self.operation_type,
            "risk_level": self.risk_level.value,
            "agent_id": self.agent_id,
            "trace_id": self.trace_id,
            "execution_id": self.execution_id,
            "snapshot_id": self.snapshot_id,
            "approval_id": self.approval_id,
            "result": self.result,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


# =============================================================================
# CMS 审计日志器
# =============================================================================

class CMSAuditLogger:
    """
    CMS 专用审计日志器
    
    功能：
    - 实时 JSONL 写入
    - 按平台/日期/事件类型查询
    - SOC 2 合规报告生成
    - 变更溯源（关联 snapshot/rollback）
    """

    def __init__(
        self,
        log_dir: str = "cms_audit_logs",
        rotation_days: int = 90,
        enable_console: bool = True,
    ):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.rotation_days = rotation_days
        self._enable_console = enable_console
        self._pending: list[dict] = []
        self._flush_threshold = 10  # 每10条写入一次

    # ── 核心日志方法 ──────────────────────────────────────────────────────

    async def log_cms_connect(
        self,
        platform: CMSPlatform,
        agent_id: str,
        success: bool,
        error: str = "",
        **kwargs,
    ) -> str:
        """记录 CMS 连接建立"""
        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_CONNECT,
            platform=platform,
            operation_id="connect",
            resource_id="",
            operation_type="connect",
            risk_level=RiskLevel.LOW,
            agent_id=agent_id,
            error=error,
            result={"success": success},
            metadata=kwargs,
        )
        return await self._write_record(record)

    async def log_cms_read(
        self,
        operation: CMSOperation,
        result: CMSResult,
        trace_id: str = "",
    ) -> str:
        """记录 CMS 读取操作"""
        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_READ,
            platform=operation.platform,
            operation_id=operation.operation_id,
            resource_id=operation.resource_id,
            operation_type=operation.operation_type.value,
            risk_level=operation.risk_level,
            agent_id=operation.agent_id,
            trace_id=trace_id,
            execution_id=operation.execution_id,
            result=result.to_dict(),
            duration_ms=result.execution_time_ms,
            metadata={"resource_type": operation.resource_type.value},
        )
        return await self._write_record(record)

    async def log_cms_write(
        self,
        operation: CMSOperation,
        result: CMSResult | None,
        execution_context: Any = None,
        trace_id: str = "",
    ) -> str:
        """
        记录 CMS 写操作（核心事件）
        
        这是最重要的审计事件类型。
        所有 CMS 写入必须调用此方法。
        """
        snapshot_id = getattr(result, "snapshot_id", "") if result else ""
        approval_id = getattr(execution_context, "approval_id", "") if execution_context else ""

        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_WRITE,
            platform=operation.platform,
            operation_id=operation.operation_id,
            resource_id=operation.resource_id,
            operation_type=operation.operation_type.value,
            risk_level=operation.risk_level,
            agent_id=operation.agent_id,
            trace_id=trace_id,
            execution_id=operation.execution_id or getattr(execution_context, "execution_id", ""),
            snapshot_id=snapshot_id,
            approval_id=approval_id,
            result=result.to_dict() if result else {},
            error=result.message if result and not result.success else "",
            duration_ms=getattr(result, "execution_time_ms", 0.0) if result else 0.0,
            metadata={
                "idempotency_key": operation.idempotency_key,
                "rollback_available": getattr(result, "rollback_available", False) if result else False,
                "execution_context": getattr(execution_context, "to_dict", lambda: {})() if execution_context else {},
            },
        )
        return await self._write_record(record)

    async def log_cms_approval(
        self,
        approval_id: str,
        platform: CMSPlatform,
        action: str,  # "submit" | "approve" | "reject" | "escalate"
        agent_id: str,
        risk_level: RiskLevel,
        reason: str = "",
        trace_id: str = "",
    ) -> str:
        """记录审批动作"""
        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_APPROVAL,
            platform=platform,
            operation_id=approval_id,
            resource_id="",
            operation_type=action,
            risk_level=risk_level,
            agent_id=agent_id,
            trace_id=trace_id,
            approval_id=approval_id,
            result={"action": action, "reason": reason},
        )
        return await self._write_record(record)

    async def log_cms_rollback(
        self,
        rollback_result: Any,  # RollbackResult
        snapshot_id: str,
        resource_id: str,
        platform: CMSPlatform,
        agent_id: str,
        trace_id: str = "",
    ) -> str:
        """记录回滚操作"""
        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_ROLLBACK,
            platform=platform,
            operation_id=rollback_result.rollback_id,
            resource_id=resource_id,
            operation_type="rollback",
            risk_level=RiskLevel.HIGH,
            agent_id=agent_id,
            trace_id=trace_id,
            snapshot_id=snapshot_id,
            result={
                "status": rollback_result.status.value,
                "message": rollback_result.message,
                "duration_ms": rollback_result.duration_ms,
                "verification_passed": rollback_result.verification_passed,
            },
            duration_ms=rollback_result.duration_ms,
        )
        return await self._write_record(record)

    async def log_cms_sandbox(
        self,
        operation: CMSOperation,
        result: bool,
        reason: str = "",
        trace_id: str = "",
    ) -> str:
        """记录沙箱执行结果"""
        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_SANDBOX,
            platform=operation.platform,
            operation_id=operation.operation_id,
            resource_id=operation.resource_id,
            operation_type=operation.operation_type.value,
            risk_level=operation.risk_level,
            agent_id=operation.agent_id,
            trace_id=trace_id,
            result={"passed": result, "reason": reason},
        )
        return await self._write_record(record)

    async def log_cms_snapshot(
        self,
        snapshot_id: str,
        resource_id: str,
        platform: CMSPlatform,
        agent_id: str,
        trace_id: str = "",
    ) -> str:
        """记录快照创建"""
        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_SNAPSHOT,
            platform=platform,
            operation_id=snapshot_id,
            resource_id=resource_id,
            operation_type="snapshot",
            risk_level=RiskLevel.LOW,
            agent_id=agent_id,
            trace_id=trace_id,
            snapshot_id=snapshot_id,
            result={"snapshot_id": snapshot_id},
        )
        return await self._write_record(record)

    async def log_cms_error(
        self,
        operation: CMSOperation,
        error: str,
        trace_id: str = "",
    ) -> str:
        """记录 CMS 错误"""
        record = CMSAuditRecord(
            event_type=CMSEventType.CMS_ERROR,
            platform=operation.platform,
            operation_id=operation.operation_id,
            resource_id=operation.resource_id,
            operation_type=operation.operation_type.value,
            risk_level=operation.risk_level,
            agent_id=operation.agent_id,
            trace_id=trace_id,
            error=error,
        )
        return await self._write_record(record)

    # ── 写入工具 ──────────────────────────────────────────────────────────

    async def _write_record(self, record: CMSAuditRecord) -> str:
        """写入审计记录（批量 + 实时）"""
        self._pending.append(record.to_dict())
        if self._enable_console:
            logger.info(f"[CMS_AUDIT] {record.event_type} | {record.platform.value} | {record.agent_id} | {record.resource_id[:20] if record.resource_id else ''}")
        if len(self._pending) >= self._flush_threshold:
            await self._flush()
        return record.record_id

    async def _flush(self) -> None:
        """批量写入磁盘"""
        if not self._pending:
            return
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = self.log_dir / f"cms_audit_{today}.jsonl"
        lines = "\n".join(json.dumps(r, ensure_ascii=False) for r in self._pending)
        log_file.write_text(lines + "\n", mode="a")
        self._pending.clear()

    async def flush(self) -> None:
        """强制刷新待写入记录"""
        await self._flush()

    # ── 查询与报告 ────────────────────────────────────────────────────────

    def query(
        self,
        platform: CMSPlatform | None = None,
        event_type: str | None = None,
        agent_id: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """
        查询审计记录
        
        Args:
            platform: 按平台过滤
            event_type: 按事件类型过滤
            agent_id: 按执行人过滤
            start_date / end_date: 日期范围
            limit: 返回上限
        """
        records: list[dict] = []
        log_files = sorted(self.log_dir.glob("cms_audit_*.jsonl"), reverse=True)
        for log_file in log_files:
            date_str = log_file.stem.replace("cms_audit_", "")
            if start_date and date_str < start_date:
                break
            if end_date and date_str > end_date:
                continue
            try:
                for line in log_file.read_text().splitlines():
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    if platform and record.get("platform") != platform.value:
                        continue
                    if event_type and record.get("event_type") != event_type:
                        continue
                    if agent_id and record.get("agent_id") != agent_id:
                        continue
                    records.append(record)
                    if len(records) >= limit:
                        return records
            except Exception as e:
                logger.warning(f"[audit] Failed to read log file {log_file}: {e}")
        return records

    def generate_compliance_report(
        self,
        start_date: str,
        end_date: str,
    ) -> dict:
        """
        生成 SOC 2 合规报告
        
        Returns:
            包含操作统计、风险分布、合规状态的字典
        """
        records = self.query(start_date=start_date, end_date=end_date, limit=10000)
        write_records = [r for r in records if r["event_type"] == CMSEventType.CMS_WRITE]
        rollback_records = [r for r in records if r["event_type"] == CMSEventType.CMS_ROLLBACK]

        # 风险分布
        risk_counts: dict[str, int] = {}
        for r in write_records:
            level = r.get("risk_level", "unknown")
            risk_counts[level] = risk_counts.get(level, 0) + 1

        # 平台分布
        platform_counts: dict[str, int] = {}
        for r in write_records:
            p = r.get("platform", "unknown")
            platform_counts[p] = platform_counts.get(p, 0) + 1

        # 失败率
        total_writes = len(write_records)
        failed_writes = len([r for r in write_records if not r.get("result", {}).get("success", True)])
        rollback_rate = len(rollback_records) / total_writes if total_writes > 0 else 0

        # 合规检查
        missing_approval = [r for r in write_records if r.get("risk_level") in ("high", "critical") and not r.get("approval_id")]
        compliance_status = "COMPLIANT" if not missing_approval else "NON_COMPLIANT"

        return {
            "report_period": {"start": start_date, "end": end_date},
            "summary": {
                "total_cms_operations": len(records),
                "total_writes": total_writes,
                "total_rollbacks": len(rollback_records),
                "failed_writes": failed_writes,
                "write_success_rate": (total_writes - failed_writes) / total_writes if total_writes > 0 else 1.0,
                "rollback_rate": rollback_rate,
            },
            "risk_distribution": risk_counts,
            "platform_distribution": platform_counts,
            "compliance": {
                "status": compliance_status,
                "missing_approval_count": len(missing_approval),
                "missing_approval_records": missing_approval[:5],  # 前5条
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def export_audit_trail(
        self,
        start_date: str,
        end_date: str,
        output_path: str = "cms_audit_export.jsonl",
    ) -> str:
        """导出审计轨迹到文件"""
        records = self.query(start_date=start_date, end_date=end_date, limit=100000)
        output = Path(output_path)
        output.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in records),
            encoding="utf-8",
        )
        logger.info(f"[audit] Exported {len(records)} records to {output_path}")
        return str(output)
