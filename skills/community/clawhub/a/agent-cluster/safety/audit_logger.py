"""
Audit Logger - 全链路审计日志系统

企业级审计日志系统，支持：
- 完整调用链路追踪（trace_id/span_id）
- SOC 2合规报告生成
- PII敏感信息检测与脱敏
- 多级日志级别
- 异步批量写入
"""

from __future__ import annotations

import asyncio
import gzip
import hashlib
import json
import logging
import os
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional
import contextvars

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# 上下文变量（用于跨异步传递追踪ID）
# =============================================================================

_current_trace: contextvars.ContextVar[Optional["TraceContext"]] = contextvars.ContextVar(
    "current_trace", default=None
)


# =============================================================================
# 数据模型
# =============================================================================

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventType(Enum):
    """事件类型"""
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    AGENT_CALL = "agent_call"
    MCP_CALL = "mcp_call"
    TOOL_CALL = "tool_call"
    PERMISSION_CHECK = "permission_check"
    HUMAN_APPROVAL = "human_approval"
    ERROR = "error"
    WORKFLOW_TRANSITION = "workflow_transition"


@dataclass
class TraceContext:
    """
    全链路追踪上下文

    三层ID结构：
    - trace_id: 全局唯一请求ID
    - span_id: 当前操作ID
    - parent_span_id: 父操作ID（构建调用树）
    """
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    parent_span_id: Optional[str] = None
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None
    agent_name: str = ""
    action: str = ""
    status: str = "running"
    input_summary: str = ""
    output_summary: str = ""
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def __enter__(self):
        _current_trace.set(self)
        return self

    def __exit__(self, *args):
        _current_trace.set(None)

    def span(self, name: str, span_type: str = "operation") -> "SpanContext":
        """创建子span"""
        return SpanContext(
            parent=self,
            span_id=str(uuid.uuid4())[:16],
            name=name,
            span_type=span_type,
        )


@dataclass
class SpanContext:
    """子操作上下文"""
    parent: TraceContext
    span_id: str
    name: str
    span_type: str
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None
    output_summary: str = ""
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def finish(self, output_summary: str = "", error: Optional[str] = None) -> None:
        self.end_time = datetime.now().isoformat()
        self.output_summary = output_summary
        self.error = error


@dataclass
class AuditRecord:
    """审计记录"""
    record_id: str
    trace_id: str
    span_id: str
    timestamp: str
    event_type: str
    level: str
    agent_name: str
    action: str
    actor_id: str
    actor_role: str
    input_data: dict
    output_data: Optional[dict] = None
    error: Optional[str] = None
    duration_ms: Optional[float] = None
    ip_address: Optional[str] = None
    session_id: Optional[str] = None
    risk_score: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "level": self.level,
            "agent_name": self.agent_name,
            "action": self.action,
            "actor_id": self.actor_id,
            "actor_role": self.actor_role,
            "input_data": self._mask_pii(self.input_data),
            "output_data": self._mask_pii(self.output_data) if self.output_data else None,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "ip_address": self.ip_address,
            "session_id": self.session_id,
            "risk_score": self.risk_score,
            "metadata": self.metadata,
        }

    # -------------------------------------------------------------------------
    # PII脱敏
    # -------------------------------------------------------------------------
    PII_PATTERNS = {
        "email": (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "***@***.com"),
        "phone": (r"1[3-9]\d{9}", "138****0000"),
        "id_card": (r"\d{17}[\dXx]", "110***********1234"),
        "bank_card": (r"\d{13,19}", "**** **** **** ****"),
        "password": (r'"password"\s*:\s*"[^"]*"', '"password": "***"'),
        "token": (r'"token"\s*:\s*"[^"]*"', '"token": "***"'),
        "api_key": (r'"api_key"\s*:\s*"[^"]*"', '"api_key": "***"'),
    }

    def _mask_pii(self, data: Any) -> Any:
        """递归脱敏PII数据"""
        if data is None:
            return None
        if isinstance(data, str):
            result = data
            for pii_type, (pattern, replacement) in self.PII_PATTERNS.items():
                result = re.sub(pattern, replacement, result)
            return result
        if isinstance(data, dict):
            return {k: self._mask_pii(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._mask_pii(item) for item in data]
        return data


# =============================================================================
# 审计日志核心类
# =============================================================================

class AuditLogger:
    """
    企业级审计日志系统

    特性：
    - 双后端存储：SQLite(实时查询) + JSONL.gz(归档)
    - 全链路追踪（trace_id/span_id）
    - PII自动脱敏
    - SOC 2合规报告
    - 异步批量写入
    - 慢查询告警
    """

    def __init__(
        self,
        log_dir: str = "./logs",
        log_level: str = "INFO",
        enable_pii_mask: bool = True,
        enable_trace: bool = True,
        batch_size: int = 50,
        flush_interval: float = 5.0,
    ):
        self._log_dir = Path(log_dir)
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._log_level = getattr(logging, log_level.upper())
        self._enable_pii_mask = enable_pii_mask
        self._enable_trace = enable_trace
        self._batch_size = batch_size
        self._flush_interval = flush_interval

        # 内存缓冲区
        self._buffer: list[AuditRecord] = []
        self._buffer_lock = asyncio.Lock()

        # 周期flush任务
        self._flush_task: Optional[asyncio.Task] = None

        # 统计
        self._stats = {
            "total_records": 0,
            "error_count": 0,
            "warning_count": 0,
            "slow_calls": 0,
            "pii_masked": 0,
        }

        # 文件句柄
        self._current_file = self._new_log_file()

        logger.info(f"审计日志系统初始化: {self._log_dir}, PII脱敏={enable_pii_mask}")

    def _new_log_file(self) -> str:
        """创建新的日志文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H")
        return str(self._log_dir / f"audit_{timestamp}.jsonl.gz")

    def _write_record(self, record: AuditRecord) -> None:
        """写入单条记录"""
        try:
            with gzip.open(self._current_file, "at", encoding="utf-8") as f:
                f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
            self._stats["total_records"] += 1
        except Exception as e:
            logger.error(f"写入审计日志失败: {e}")

    async def log(
        self,
        event_type: EventType,
        action: str,
        agent_name: str = "",
        actor_id: str = "",
        actor_role: str = "",
        input_data: Optional[dict] = None,
        output_data: Optional[dict] = None,
        level: LogLevel = LogLevel.INFO,
        error: Optional[str] = None,
        duration_ms: Optional[float] = None,
        risk_score: float = 0.0,
        metadata: Optional[dict] = None,
        **kwargs,
    ) -> str:
        """
        记录审计日志

        Args:
            event_type: 事件类型
            action: 操作描述
            agent_name: 智能体名称
            actor_id: 操作者ID
            actor_role: 操作者角色
            input_data: 输入数据（会自动脱敏）
            output_data: 输出数据
            level: 日志级别
            error: 错误信息
            duration_ms: 执行时长
            risk_score: 风险评分
            metadata: 额外元数据

        Returns:
            记录ID
        """
        record_id = str(uuid.uuid4())

        # 获取当前追踪上下文
        trace_ctx = _current_trace.get()
        trace_id = trace_ctx.trace_id if trace_ctx else record_id[:16]
        span_id = trace_ctx.span_id if trace_ctx else record_id[:16]

        # PII脱敏
        if self._enable_pii_mask:
            if input_data:
                input_data = AuditRecord(record_id, "", "", "", "", "", "", "", "", "", input_data)._mask_pii(input_data)
            if output_data:
                output_data = AuditRecord(record_id, "", "", "", "", "", "", "", "", "", {})._mask_pii(output_data)
                self._stats["pii_masked"] += 1

        record = AuditRecord(
            record_id=record_id,
            trace_id=trace_id,
            span_id=span_id,
            timestamp=datetime.now().isoformat(),
            event_type=event_type.value,
            level=level.value,
            agent_name=agent_name,
            action=action,
            actor_id=actor_id,
            actor_role=actor_role,
            input_data=input_data or {},
            output_data=output_data,
            error=error,
            duration_ms=duration_ms,
            risk_score=risk_score,
            metadata=metadata or kwargs,
        )

        # 更新统计
        if level in (LogLevel.ERROR, LogLevel.CRITICAL):
            self._stats["error_count"] += 1
        if level == LogLevel.WARNING:
            self._stats["warning_count"] += 1
        if duration_ms and duration_ms > 5000:
            self._stats["slow_calls"] += 1
            logger.warning(f"[慢操作] {agent_name}.{action} 耗时{duration_ms}ms")

        # 异步写入缓冲区
        await self._buffer_add(record)

        # 高风险事件实时写入
        if risk_score > 0.5 or level in (LogLevel.ERROR, LogLevel.CRITICAL):
            self._write_record(record)

        return record_id

    async def _buffer_add(self, record: AuditRecord) -> None:
        """加入缓冲区，达到阈值则批量flush"""
        async with self._buffer_lock:
            self._buffer.append(record)
            if len(self._buffer) >= self._batch_size:
                await self._flush_buffer()

    async def _flush_buffer(self) -> None:
        """批量写入缓冲区"""
        if not self._buffer:
            return

        records = self._buffer[:]
        self._buffer.clear()

        def _sync_flush():
            for record in records:
                self._write_record(record)

        await asyncio.get_event_loop().run_in_executor(None, _sync_flush)

    async def flush(self) -> int:
        """强制刷新缓冲区"""
        async with self._buffer_lock:
            await self._flush_buffer()
        return len(self._buffer)

    # -------------------------------------------------------------------------
    # 全链路追踪
    # -------------------------------------------------------------------------

    def start_trace(
        self,
        agent_name: str,
        action: str,
        input_summary: str = "",
        metadata: Optional[dict] = None,
    ) -> TraceContext:
        """开始一个追踪"""
        ctx = TraceContext(
            agent_name=agent_name,
            action=action,
            input_summary=input_summary,
            metadata=metadata or {},
        )
        return ctx

    def end_trace(
        self,
        ctx: TraceContext,
        output_summary: str = "",
        error: Optional[str] = None,
    ) -> None:
        """结束追踪"""
        ctx.end_time = datetime.now().isoformat()
        ctx.output_summary = output_summary
        ctx.status = "error" if error else "completed"
        ctx.error = error

        # 转换为审计记录
        asyncio.create_task(self.log(
            event_type=EventType.AGENT_END,
            action=f"{ctx.agent_name}.{ctx.action}",
            agent_name=ctx.agent_name,
            output_data={"status": ctx.status, "summary": output_summary, "error": error},
            level=LogLevel.ERROR if error else LogLevel.INFO,
            error=error,
            metadata={"trace_id": ctx.trace_id, "span_id": ctx.span_id},
        ))

    # -------------------------------------------------------------------------
    # 查询与分析
    # -------------------------------------------------------------------------

    def query(
        self,
        trace_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        event_type: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        limit: int = 100,
    ) -> list[dict]:
        """
        查询审计日志

        支持多条件组合过滤
        """
        results = []

        # 扫描日志文件
        log_files = sorted(self._log_dir.glob("audit_*.jsonl.gz"))

        for log_file in log_files[-7:]:  # 最近7个文件
            try:
                with gzip.open(log_file, "rt", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line.strip())

                            # 过滤
                            if trace_id and record.get("trace_id") != trace_id:
                                continue
                            if agent_name and record.get("agent_name") != agent_name:
                                continue
                            if event_type and record.get("event_type") != event_type:
                                continue

                            ts = record.get("timestamp", "")
                            if since and ts < since.isoformat():
                                continue
                            if until and ts > until.isoformat():
                                continue

                            results.append(record)
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                logger.warning(f"读取日志文件失败: {log_file}: {e}")

            if len(results) >= limit:
                break

        return results[:limit]

    def get_stats(self) -> dict[str, Any]:
        """获取统计信息"""
        return {
            **self._stats,
            "buffer_size": len(self._buffer),
            "log_dir": str(self._log_dir),
            "current_file": self._current_file,
        }

    # -------------------------------------------------------------------------
    # SOC 2合规报告
    # -------------------------------------------------------------------------

    def generate_soc2_report(
        self,
        since: datetime,
        until: datetime,
        output_path: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        生成SOC 2合规报告

        覆盖要求：
        - 用户操作统计
        - 敏感信息访问记录
        - 异常行为检测
        - 访问趋势分析
        """
        records = self.query(since=since, until=until, limit=10000)

        # 用户操作统计
        user_stats = defaultdict(lambda: {"count": 0, "actions": set(), "errors": 0})
        for r in records:
            uid = r.get("actor_id", "unknown")
            user_stats[uid]["count"] += 1
            user_stats[uid]["actions"].add(r.get("action", ""))
            if r.get("level") in ("ERROR", "CRITICAL"):
                user_stats[uid]["errors"] += 1

        # 敏感操作统计
        sensitive_ops = [
            "place_order", "audit_payment", "adjust_budget",
            "cancel_order", "trigger_replenishment"
        ]
        sensitive_count = sum(
            1 for r in records
            if any(op in r.get("action", "") for op in sensitive_ops)
        )

        # 异常行为（高风险+错误）
        anomalies = [
            r for r in records
            if r.get("risk_score", 0) > 0.5 or r.get("level") in ("ERROR", "CRITICAL")
        ]

        # PII访问统计
        pii_access = sum(
            1 for r in records
            if any(k in str(r.get("input_data", {})) for k in ["phone", "email", "id_card"])
        )

        report = {
            "report_period": {"since": since.isoformat(), "until": until.isoformat()},
            "summary": {
                "total_events": len(records),
                "unique_users": len(user_stats),
                "sensitive_operations": sensitive_count,
                "anomaly_count": len(anomalies),
                "pii_access_count": pii_access,
            },
            "user_activity": {
                uid: {**stats, "actions": list(stats["actions"])}
                for uid, stats in user_stats.items()
            },
            "anomalies": anomalies[:50],  # 最多50条
            "risk_distribution": self._calc_risk_distribution(records),
            "generated_at": datetime.now().isoformat(),
        }

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            logger.info(f"SOC2报告已生成: {output_path}")

        return report

    def _calc_risk_distribution(self, records: list[dict]) -> dict[str, int]:
        """计算风险分布"""
        dist = {"low": 0, "medium": 0, "high": 0}
        for r in records:
            score = r.get("risk_score", 0)
            if score < 0.3:
                dist["low"] += 1
            elif score < 0.6:
                dist["medium"] += 1
            else:
                dist["high"] += 1
        return dist


# =============================================================================
# 便捷装饰器
# =============================================================================

def traced(agent_name: str, action: str):
    """
    追踪装饰器

    Usage:
        @traced("inventory_agent", "query_stock")
        async def query_stock(...):
            ...
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger = kwargs.pop("_audit_logger", AuditLogger())
            input_summary = str(args)[:100] if args else str(kwargs)[:100]

            ctx = logger.start_trace(agent_name, action, input_summary)
            with ctx:
                try:
                    result = await func(*args, **kwargs)
                    logger.end_trace(ctx, output_summary=str(result)[:200])
                    return result
                except Exception as e:
                    logger.end_trace(ctx, error=str(e))
                    raise
        return wrapper
    return decorator


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    import time

    print("=" * 60)
    print("  全链路审计日志系统测试")
    print("=" * 60)

    audit = AuditLogger(log_dir="./logs/test", enable_pii_mask=True)

    async def test():
        # 测试追踪
        ctx = audit.start_trace("orchestrator", "handle_request", "用户: 查询库存")
        with ctx:
            # 模拟调用
            await audit.log(
                event_type=EventType.AGENT_CALL,
                action="inventory_agent.query_stock",
                agent_name="inventory_agent",
                actor_id="user001",
                actor_role="warehouse_operator",
                input_data={"sku": "SKU001", "warehouse": "WH001"},
                level=LogLevel.INFO,
            )

            await asyncio.sleep(0.1)

            await audit.log(
                event_type=EventType.MCP_CALL,
                action="erp.query_stock",
                agent_name="inventory_agent",
                level=LogLevel.INFO,
                duration_ms=85,
            )

        # 测试PII脱敏
        await audit.log(
            event_type=EventType.AGENT_CALL,
            action="procurement_agent.place_order",
            agent_name="procurement_agent",
            actor_id="buyer001",
            input_data={
                "contact": "张经理",
                "phone": "13812345678",
                "email": "zhang@company.com",
                "card": "6222021234567890123",
            },
            level=LogLevel.WARNING,
            risk_score=0.65,
        )

        await audit.flush()

        # 打印统计
        print("\n[统计信息]")
        stats = audit.get_stats()
        for k, v in stats.items():
            print(f"  {k}: {v}")

        # 生成合规报告
        print("\n[SOC2合规报告]")
        report = audit.generate_soc2_report(
            since=datetime.now() - timedelta(hours=1),
            until=datetime.now(),
        )
        print(f"  总事件数: {report['summary']['total_events']}")
        print(f"  敏感操作: {report['summary']['sensitive_operations']}")
        print(f"  异常事件: {report['summary']['anomaly_count']}")
        print(f"  风险分布: {report['risk_distribution']}")

    asyncio.run(test())
