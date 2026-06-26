"""
Task Protocol - 细粒度任务分解协议

定义Agent间任务传递的标准协议，包括：
- 任务描述协议（TaskMessage）
- 依赖关系声明
- 优先级与截止时间
- 结果传递格式
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional


# =============================================================================
# 枚举定义
# =============================================================================

class TaskPriority(Enum):
    """任务优先级"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3
    CRITICAL = 4


class TaskMode(Enum):
    """执行模式"""
    SERIAL = "serial"           # 严格串行
    PARALLEL = "parallel"       # 严格并行
    HYBRID = "hybrid"           # 混合模式（可串可并）


class TaskState(Enum):
    """任务状态（完整生命周期）"""
    CREATED = "created"         # 已创建
    PENDING = "pending"         # 等待执行
    RUNNING = "running"         # 执行中
    WAITING_DEP = "waiting_dep" # 等待依赖
    SUCCESS = "success"         # 成功完成
    FAILED = "failed"           # 执行失败
    RETRY = "retry"            # 等待重试
    CANCELLED = "cancelled"     # 已取消
    TIMEOUT = "timeout"         # 执行超时


# =============================================================================
# 任务消息协议
# =============================================================================

@dataclass
class TaskDependency:
    """任务依赖声明"""
    depends_on: list[str] = field(default_factory=list)  # 依赖的任务ID
    blocking: bool = True          # 是否阻塞（False表示软依赖，可并行执行）
    shared_context: list[str] = field(default_factory=list)  # 需要共享的上下文字段


@dataclass
class TaskContext:
    """任务上下文（跨Agent共享数据）"""
    request_id: str
    user_id: str = ""
    session_id: str = ""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "metadata": self.metadata,
        }


@dataclass
class TaskMessage:
    """
    标准任务消息协议

    Agent间通信的标准格式，确保任务信息完整传递
    """
    # 身份标识
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None  # 父任务ID

    # 任务描述
    agent_name: str = ""              # 目标Agent
    action: str = ""                  # 操作类型
    parameters: dict = field(default_factory=dict)  # 操作参数
    description: str = ""             # 任务描述（可选）

    # 执行控制
    priority: TaskPriority = TaskPriority.NORMAL
    mode: TaskMode = TaskMode.SERIAL
    parallel_group: Optional[str] = None  # 并行组ID，同组内并行执行
    timeout_seconds: float = 60.0
    max_retries: int = 3

    # 依赖关系
    dependency: TaskDependency = field(default_factory=TaskDependency)

    # 上下文
    context: Optional[TaskContext] = None

    # 执行结果（完成后填写）
    state: TaskState = TaskState.CREATED
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    retry_count: int = 0

    # 创建时间
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # ================================================================
    # 序列化
    # ================================================================

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "parent_id": self.parent_id,
            "agent_name": self.agent_name,
            "action": self.action,
            "parameters": self.parameters,
            "description": self.description,
            "priority": self.priority.value,
            "mode": self.mode.value,
            "parallel_group": self.parallel_group,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "dependency": {
                "depends_on": self.dependency.depends_on,
                "blocking": self.dependency.blocking,
                "shared_context": self.dependency.shared_context,
            },
            "context": self.context.to_dict() if self.context else None,
            "state": self.state.value,
            "result": str(self.result)[:500] if self.result else None,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "retry_count": self.retry_count,
            "created_at": self.created_at,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> "TaskMessage":
        ctx_data = data.pop("context", None)
        dep_data = data.pop("dependency", {})
        priority_val = data.pop("priority", "normal")
        mode_val = data.pop("mode", "serial")
        state_val = data.pop("state", "created")

        priority = TaskPriority[priority_val.upper()] if isinstance(priority_val, str) else priority_val
        mode = TaskMode[mode_val.upper()] if isinstance(mode_val, str) else mode_val
        state = TaskState[state_val.upper()] if isinstance(state_val, str) else state_val

        dependency = TaskDependency(
            depends_on=dep_data.get("depends_on", []),
            blocking=dep_data.get("blocking", True),
            shared_context=dep_data.get("shared_context", []),
        )
        context = TaskContext(**ctx_data) if ctx_data else None

        msg = cls(
            priority=priority,
            mode=mode,
            state=state,
            dependency=dependency,
            context=context,
            **data,
        )
        return msg

    # ================================================================
    # 状态操作
    # ================================================================

    def start(self):
        """标记任务开始执行"""
        self.state = TaskState.RUNNING
        self.started_at = datetime.now().isoformat()

    def succeed(self, result: Any):
        """标记任务成功"""
        self.state = TaskState.SUCCESS
        self.result = result
        self.completed_at = datetime.now().isoformat()

    def fail(self, error: str):
        """标记任务失败"""
        self.state = TaskState.FAILED
        self.error = error
        self.completed_at = datetime.now().isoformat()

    def mark_retry(self):
        """标记为等待重试"""
        self.state = TaskState.RETRY
        self.retry_count += 1

    def can_retry(self) -> bool:
        """是否可以重试"""
        return self.retry_count < self.max_retries

    def is_terminal(self) -> bool:
        """是否处于终态"""
        return self.state in (TaskState.SUCCESS, TaskState.FAILED, TaskState.CANCELLED, TaskState.TIMEOUT)


# =============================================================================
# 任务分解引擎
# =============================================================================

class TaskDecompositionEngine:
    """
    任务分解引擎

    将用户请求分解为细粒度、可执行的TaskMessage列表
    支持串行/并行/混合三种分解模式
    """

    # 内置分解模板
    DECOMPOSITION_TEMPLATES = {
        "stock_replenishment": {
            "description": "库存补货工作流",
            "steps": [
                {"agent": "inventory_agent", "action": "query_stock",
                 "mode": "serial", "priority": "normal"},
                {"agent": "inventory_agent", "action": "calculate_safety_stock",
                 "mode": "serial", "priority": "high", "condition": "stock_below_threshold"},
                {"agent": "procurement_agent", "action": "supplier_lookup",
                 "mode": "parallel", "parallel_group": "prep",
                 "priority": "normal", "condition": "needs_replenishment"},
                {"agent": "finance_agent", "action": "query_budget",
                 "mode": "parallel", "parallel_group": "prep",
                 "priority": "normal", "condition": "needs_replenishment"},
                {"agent": "procurement_agent", "action": "place_order",
                 "mode": "serial", "priority": "urgent",
                 "depends_on": ["prep"], "condition": "budget_sufficient"},
                {"agent": "finance_agent", "action": "audit_payment",
                 "mode": "serial", "priority": "high", "depends_on": ["place_order"]},
                {"agent": "logistics_agent", "action": "track_delivery",
                 "mode": "serial", "priority": "normal",
                 "depends_on": ["audit_payment"], "condition": "order_placed"},
            ],
        },
        "procurement_with_logistics": {
            "description": "采购物流一体化",
            "steps": [
                {"agent": "procurement_agent", "action": "supplier_lookup",
                 "mode": "serial", "priority": "normal"},
                {"agent": "procurement_agent", "action": "place_order",
                 "mode": "serial", "priority": "high"},
                {"agent": "logistics_agent", "action": "plan_route",
                 "mode": "parallel", "parallel_group": "concurrent",
                 "priority": "normal", "depends_on": ["place_order"]},
                {"agent": "finance_agent", "action": "query_budget",
                 "mode": "parallel", "parallel_group": "concurrent",
                 "priority": "normal", "depends_on": ["place_order"]},
                {"agent": "orchestrator", "action": "aggregate_results",
                 "mode": "serial", "priority": "normal", "depends_on": ["concurrent"]},
            ],
        },
        "finance_audit": {
            "description": "财务审核工作流",
            "steps": [
                {"agent": "finance_agent", "action": "query_budget",
                 "mode": "serial", "priority": "normal"},
                {"agent": "finance_agent", "action": "audit_payment",
                 "mode": "serial", "priority": "high", "depends_on": ["query_budget"]},
                {"agent": "logistics_agent", "action": "track_delivery",
                 "mode": "serial", "priority": "normal", "depends_on": ["audit_payment"],
                 "condition": "order_exists"},
            ],
        },
    }

    def __init__(self, default_timeout: float = 60.0, default_retries: int = 3):
        self.default_timeout = default_timeout
        self.default_retries = default_retries

    def decompose(
        self,
        workflow_name: str,
        parameters: dict,
        context: Optional[TaskContext] = None,
    ) -> list[TaskMessage]:
        """
        根据工作流名称分解任务

        Args:
            workflow_name: 工作流名称
            parameters: 全局参数
            context: 任务上下文

        Returns:
            TaskMessage列表（已排序：串行任务在前，并行任务在后）
        """
        template = self.DECOMPOSITION_TEMPLATES.get(workflow_name)
        if not template:
            # 兜底：单步任务
            return [
                TaskMessage(
                    agent_name="orchestrator",
                    action="fallback",
                    parameters={"original": parameters},
                    context=context,
                )
            ]

        serial_tasks: list[TaskMessage] = []
        parallel_groups: dict[str, list[TaskMessage]] = {}

        for step in template["steps"]:
            msg = self._create_task_message(step, parameters, context)
            if msg.mode == TaskMode.PARALLEL and msg.parallel_group:
                if msg.parallel_group not in parallel_groups:
                    parallel_groups[msg.parallel_group] = []
                parallel_groups[msg.parallel_group].append(msg)
            else:
                serial_tasks.append(msg)

        # 按依赖排序
        sorted_serial = self._topological_sort(serial_tasks)

        # 展开并行组：在并行组前插入分组标识
        result: list[TaskMessage] = []
        for task in sorted_serial:
            if task.parallel_group and task.parallel_group in parallel_groups:
                # 先执行并行组
                result.extend(parallel_groups[task.parallel_group])
                del parallel_groups[task.parallel_group]
            else:
                result.append(task)

        # 剩余未引用的并行组
        for group_id, tasks in parallel_groups.items():
            result.extend(tasks)

        return result

    def _create_task_message(
        self,
        step: dict,
        parameters: dict,
        context: Optional[TaskContext] = None,
    ) -> TaskMessage:
        """根据步骤配置创建TaskMessage"""
        priority_str = step.get("priority", "normal")
        priority = TaskPriority[priority_str.upper()]
        mode_str = step.get("mode", "serial")
        mode = TaskMode[mode_str.upper()]

        dep = TaskDependency(
            depends_on=step.get("depends_on", []),
            blocking=step.get("blocking", True),
            shared_context=step.get("shared_context", []),
        )

        # 合并全局参数
        params = {**parameters, **step.get("parameters", {})}

        return TaskMessage(
            agent_name=step["agent"],
            action=step["action"],
            parameters=params,
            description=step.get("description", ""),
            priority=priority,
            mode=mode,
            parallel_group=step.get("parallel_group"),
            timeout_seconds=step.get("timeout", self.default_timeout),
            max_retries=step.get("max_retries", self.default_retries),
            dependency=dep,
            context=context,
        )

    def _topological_sort(self, tasks: list[TaskMessage]) -> list[TaskMessage]:
        """基于依赖的拓扑排序"""
        task_map = {t.task_id: t for t in tasks}
        in_degree = {t.task_id: 0 for t in tasks}

        for t in tasks:
            for dep_id in t.dependency.depends_on:
                if dep_id in in_degree:
                    in_degree[t.task_id] += 1

        queue = [t for t in tasks if in_degree[t.task_id] == 0]
        sorted_tasks = []

        while queue:
            current = queue.pop(0)
            sorted_tasks.append(current)
            for t in tasks:
                if current.task_id in t.dependency.depends_on:
                    in_degree[t.task_id] -= 1
                    if in_degree[t.task_id] == 0:
                        queue.append(t)

        # 保留未排序的（循环依赖保护）
        sorted_ids = {t.task_id for t in sorted_tasks}
        sorted_tasks.extend([t for t in tasks if t.task_id not in sorted_ids])

        return sorted_tasks
