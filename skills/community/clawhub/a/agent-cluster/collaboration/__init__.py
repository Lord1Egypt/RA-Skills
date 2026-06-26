"""
Collaboration - 跨Agent协作流程

模块：
- task_protocol: 细粒度任务分解协议
- state_sync: Agent间状态同步
- trace_tracker: 协作链路可视化追踪
- workflow_engine: 并行/串行混合执行引擎
"""

from __future__ import annotations

from .task_protocol import (
    TaskMessage,
    TaskContext,
    TaskDependency,
    TaskPriority,
    TaskMode,
    TaskState,
    TaskDecompositionEngine,
)
from .state_sync import (
    SharedStateManager,
    StateEntry,
    StateSnapshot,
    SyncStatus,
    Subscription,
)
from .trace_tracker import (
    CollaborationTracker,
    TraceSpan,
    SpanType,
)
from .workflow_engine import (
    WorkflowEngine,
    WorkflowContext,
    AgentExecutor,
)

__all__ = [
    "TaskMessage", "TaskContext", "TaskDependency",
    "TaskPriority", "TaskMode", "TaskState", "TaskDecompositionEngine",
    "SharedStateManager", "StateEntry", "StateSnapshot", "SyncStatus", "Subscription",
    "CollaborationTracker", "TraceSpan", "SpanType",
    "WorkflowEngine", "WorkflowContext", "AgentExecutor",
]
