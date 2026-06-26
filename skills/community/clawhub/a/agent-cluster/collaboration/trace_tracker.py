"""
Collaboration Trace Tracker - 协作链路可视化追踪

功能：
- 全链路追踪（trace_id/span_id）
- Agent执行时序图生成
- 协作瓶颈分析
- 可视化JSON输出（供前端或Mermaid渲染）
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


# =============================================================================
# 数据模型
# =============================================================================

class SpanType(Enum):
    """Span类型"""
    ROOT = "root"                 # 根节点（用户请求）
    AGENT = "agent"              # Agent执行
    PARALLEL_GROUP = "parallel_group"  # 并行组
    SERIAL_STEP = "serial_step"  # 串行步骤
    API_CALL = "api_call"        # API调用
    DEPENDENCY_WAIT = "dep_wait" # 等待依赖


@dataclass
class TraceSpan:
    """追踪跨度"""
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]

    name: str                    # 操作名称
    span_type: SpanType
    agent_name: str = ""        # 所属Agent

    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ended_at: Optional[str] = None
    duration_ms: float = 0.0    # 持续时间（毫秒）

    status: str = "ok"          # ok / error / timeout
    error_message: Optional[str] = None

    metadata: dict = field(default_factory=dict)
    children: list[str] = field(default_factory=list)  # 子span ID

    def end(self, status: str = "ok", error: Optional[str] = None):
        self.ended_at = datetime.now().isoformat()
        self.status = status
        self.error_message = error
        start = datetime.fromisoformat(self.started_at)
        end_dt = datetime.fromisoformat(self.ended_at)
        self.duration_ms = (end_dt - start).total_seconds() * 1000


# =============================================================================
# 追踪器
# =============================================================================

class CollaborationTracker:
    """
    协作链路追踪器

    功能：
    - 为每个请求创建独立的trace_id
    - 记录每个Agent/步骤的起止时间
    - 生成时序图JSON
    - 检测串行瓶颈
    - 支持Mermaid格式导出
    """

    def __init__(self, max_spans: int = 1000):
        self.max_spans = max_spans
        self._spans: dict[str, TraceSpan] = {}
        self._active_spans: dict[str, float] = {}  # span_id -> start_time

    def start_trace(self, request_id: str, user_input: str = "") -> str:
        """开始新的追踪"""
        trace_id = str(uuid.uuid4())
        root_span = TraceSpan(
            span_id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_span_id=None,
            name=f"request:{request_id[:8]}",
            span_type=SpanType.ROOT,
            started_at=datetime.now().isoformat(),
            metadata={"user_input": user_input[:200]},
        )
        self._spans[root_span.span_id] = root_span
        self._active_spans[root_span.span_id] = time.time()
        return trace_id

    def start_span(
        self,
        trace_id: str,
        name: str,
        span_type: SpanType,
        parent_span_id: Optional[str] = None,
        agent_name: str = "",
        metadata: Optional[dict] = None,
    ) -> str:
        """开始一个新的span"""
        span_id = str(uuid.uuid4())

        # 如果没有指定parent，自动找到当前活跃span
        if parent_span_id is None:
            parent_span_id = self._find_active_parent(trace_id)

        span = TraceSpan(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            name=name,
            span_type=span_type,
            agent_name=agent_name,
            started_at=datetime.now().isoformat(),
            metadata=metadata or {},
        )

        self._spans[span_id] = span
        self._active_spans[span_id] = time.time()

        # 维护父子关系
        if parent_span_id and parent_span_id in self._spans:
            parent = self._spans[parent_span_id]
            if span_id not in parent.children:
                parent.children.append(span_id)

        return span_id

    def end_span(self, span_id: str, status: str = "ok", error: Optional[str] = None):
        """结束一个span"""
        if span_id in self._spans:
            span = self._spans[span_id]
            span.end(status=status, error=error)

        if span_id in self._active_spans:
            del self._active_spans[span_id]

    def _find_active_parent(self, trace_id: str) -> Optional[str]:
        """找到当前活跃的父span"""
        for span_id, start_time in list(self._active_spans.items()):
            span = self._spans.get(span_id)
            if span and span.trace_id == trace_id:
                return span_id
        return None

    def get_trace(self, trace_id: str) -> list[TraceSpan]:
        """获取完整追踪链路"""
        return sorted(
            [s for s in self._spans.values() if s.trace_id == trace_id],
            key=lambda s: s.started_at,
        )

    def get_timeline(self, trace_id: str) -> list[dict]:
        """生成时间线JSON（用于可视化）"""
        spans = self.get_trace(trace_id)
        timeline = []
        for span in spans:
            timeline.append({
                "id": span.span_id,
                "parentId": span.parent_span_id,
                "name": span.name,
                "type": span.span_type.value,
                "agent": span.agent_name,
                "start": span.started_at,
                "end": span.ended_at,
                "duration": round(span.duration_ms, 2),
                "status": span.status,
                "error": span.error_message,
                "metadata": span.metadata,
            })
        return timeline

    def get_parallel_groups(self, trace_id: str) -> dict[str, list[dict]]:
        """分析并行组执行情况"""
        spans = self.get_trace(trace_id)
        groups: dict[str, list[dict]] = {}
        for span in spans:
            if span.span_type == SpanType.PARALLEL_GROUP:
                groups[span.name] = []
        for span in spans:
            if span.metadata.get("parallel_group"):
                pg = span.metadata["parallel_group"]
                if pg not in groups:
                    groups[pg] = []
                groups[pg].append({
                    "span_id": span.span_id,
                    "name": span.name,
                    "agent": span.agent_name,
                    "duration": round(span.duration_ms, 2),
                    "status": span.status,
                })
        return groups

    def detect_bottlenecks(self, trace_id: str) -> list[dict]:
        """检测串行瓶颈（执行时间 > 均值2倍 的步骤）"""
        spans = self.get_trace(trace_id)
        serial_spans = [s for s in spans if s.span_type == SpanType.AGENT and s.duration_ms > 0]
        if not serial_spans:
            return []

        avg_duration = sum(s.duration_ms for s in serial_spans) / len(serial_spans)
        bottlenecks = []
        for span in serial_spans:
            if span.duration_ms > avg_duration * 2:
                bottlenecks.append({
                    "span_id": span.span_id,
                    "name": span.name,
                    "agent": span.agent_name,
                    "duration_ms": round(span.duration_ms, 2),
                    "avg_ms": round(avg_duration, 2),
                    "ratio": round(span.duration_ms / avg_duration, 1),
                    "recommendation": f"建议优化或改为并行执行",
                })
        return bottlenecks

    def to_mermaid_sequence(self, trace_id: str) -> str:
        """导出为Mermaid时序图"""
        spans = self.get_trace(trace_id)
        lines = ["sequenceDiagram"]

        agents = sorted(set(s.agent_name for s in spans if s.agent_name))
        if agents:
            for agent in agents:
                lines.append(f"    participant {agent}")

        for span in spans:
            if span.parent_span_id:
                parent = self._spans.get(span.parent_span_id)
                parent_name = parent.agent_name if parent else "system"
                current_name = span.agent_name or span.name
                duration_ms = round(span.duration_ms, 2)
                status_icon = "⚠️" if span.status != "ok" else "✅"
                lines.append(
                    f"    {parent_name}->>+{current_name}: {span.name} ({duration_ms}ms) {status_icon}"
                )
                if span.error_message:
                    lines.append(f"    Note over {current_name}: 错误: {span.error_message[:80]}")

        return "\n".join(lines)

    def to_mermaid_gantt(self, trace_id: str) -> str:
        """导出为Mermaid甘特图（展示时间轴）"""
        spans = self.get_trace(trace_id)
        lines = ["gantt", "    title 协作链路时间轴", "    dateFormat X", "    axisFormat %sms"]

        for span in spans:
            if span.ended_at and span.duration_ms > 1:
                color = {
                    SpanType.ROOT: "red",
                    SpanType.AGENT: "blue",
                    SpanType.PARALLEL_GROUP: "green",
                    SpanType.API_CALL: "orange",
                }.get(span.span_type, "gray")
                lines.append(
                    f'    {span.agent_name or span.name} : {span.name}, '
                    f'0, {round(span.duration_ms)}ms, {color}'
                )

        return "\n".join(lines)

    def generate_report(self, trace_id: str) -> dict:
        """生成完整追踪报告"""
        spans = self.get_trace(trace_id)
        total_duration = 0.0
        for span in spans:
            if span.span_type == SpanType.ROOT and span.duration_ms > 0:
                total_duration = span.duration_ms
                break

        error_spans = [s for s in spans if s.status == "error"]
        parallel_groups = self.get_parallel_groups(trace_id)
        bottlenecks = self.detect_bottlenecks(trace_id)

        return {
            "trace_id": trace_id,
            "total_spans": len(spans),
            "total_duration_ms": round(total_duration, 2),
            "root_span_id": next((s.span_id for s in spans if s.span_type == SpanType.ROOT), None),
            "agents_involved": sorted(set(s.agent_name for s in spans if s.agent_name)),
            "error_count": len(error_spans),
            "parallel_groups": {k: len(v) for k, v in parallel_groups.items()},
            "bottlenecks": bottlenecks,
            "mermaid_sequence": self.to_mermaid_sequence(trace_id),
            "mermaid_gantt": self.to_mermaid_gantt(trace_id),
            "spans": self.get_timeline(trace_id),
        }

    def export_trace(self, trace_id: str, path: str):
        """导出追踪JSON到文件"""
        report = self.generate_report(trace_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    def cleanup_old_traces(self, max_traces: int = 100):
        """清理旧追踪记录"""
        trace_ids = set(s.trace_id for s in self._spans.values())
        if len(trace_ids) > max_traces:
            old_ids = sorted(trace_ids)[:-max_traces]
            for tid in old_ids:
                span_ids = [s.span_id for s in self._spans.values() if s.trace_id == tid]
                for sid in span_ids:
                    if sid in self._spans:
                        del self._spans[sid]
                    if sid in self._active_spans:
                        del self._active_spans[sid]
