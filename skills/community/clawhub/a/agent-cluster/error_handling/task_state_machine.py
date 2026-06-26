"""
Task State Machine - 任务状态机

完整任务生命周期管理：
pending → running → success
                  → failed → retry (可重试)
                  → timeout
                  → cancelled
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 状态枚举
# =============================================================================

class State(Enum):
    """任务状态（完整生命周期）"""
    PENDING = "pending"           # 等待执行
    RUNNING = "running"          # 执行中
    WAITING = "waiting"           # 等待依赖
    SUCCESS = "success"          # 成功完成
    FAILED = "failed"            # 执行失败（不可重试）
    RETRY = "retry"             # 等待重试
    CANCELLED = "cancelled"      # 已取消
    TIMEOUT = "timeout"          # 执行超时


# =============================================================================
# 状态转换规则
# =============================================================================

VALID_TRANSITIONS: dict[State, set[State]] = {
    State.PENDING: {State.RUNNING, State.CANCELLED},
    State.RUNNING: {State.SUCCESS, State.FAILED, State.TIMEOUT, State.CANCELLED},
    State.WAITING: {State.RUNNING, State.CANCELLED},
    State.SUCCESS: set(),              # 终态
    State.FAILED: {State.RETRY},       # 可重试
    State.RETRY: {State.RUNNING, State.FAILED},  # 重试中
    State.CANCELLED: set(),            # 终态
    State.TIMEOUT: {State.RETRY},      # 可重试
}


# =============================================================================
# 任务记录
# =============================================================================

@dataclass
class TaskRecord:
    """任务状态记录"""
    task_id: str
    name: str
    agent_name: str
    current_state: State
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    last_transition_at: str = field(default_factory=lambda: datetime.now().isoformat())
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    result: Any = None
    metadata: dict = field(default_factory=dict)

    # 统计
    total_duration_ms: float = 0.0
    state_history: list[dict] = field(default_factory=list)

    def transition_to(self, new_state: State, reason: str = "", error: Optional[str] = None):
        """执行状态转换"""
        old_state = self.current_state
        valid_next = VALID_TRANSITIONS.get(old_state, set())

        if new_state not in valid_next:
            raise ValueError(
                f"非法状态转换: {old_state.value} → {new_state.value} "
                f"(有效转换: {[s.value for s in valid_next]})"
            )

        self.current_state = new_state
        self.last_transition_at = datetime.now().isoformat()
        if error:
            self.error_message = error
        if new_state == State.RUNNING and not self.started_at:
            self.started_at = self.last_transition_at
        if new_state in (State.SUCCESS, State.FAILED, State.CANCELLED, State.TIMEOUT):
            self.completed_at = self.last_transition_at
            self._calculate_duration()

        self.state_history.append({
            "from": old_state.value,
            "to": new_state.value,
            "reason": reason,
            "timestamp": self.last_transition_at,
        })

        logger.info(f"[状态机] {self.task_id[:8]} {old_state.value} → {new_state.value} | {reason}")

    def _calculate_duration(self):
        """计算总执行时长"""
        if self.started_at:
            start = datetime.fromisoformat(self.started_at)
            end = datetime.fromisoformat(self.completed_at)
            self.total_duration_ms = (end - start).total_seconds() * 1000

    def can_retry(self) -> bool:
        """是否可以重试"""
        return (
            self.current_state in (State.FAILED, State.TIMEOUT, State.RETRY)
            and self.retry_count < self.max_retries
        )

    def is_terminal(self) -> bool:
        """是否为终态"""
        return self.current_state in (State.SUCCESS, State.CANCELLED)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "agent_name": self.agent_name,
            "current_state": self.current_state.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "last_transition_at": self.last_transition_at,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "error_message": self.error_message,
            "total_duration_ms": round(self.total_duration_ms, 2),
            "state_history": self.state_history,
            "metadata": self.metadata,
        }


# =============================================================================
# 状态机
# =============================================================================

class TaskStateMachine:
    """
    任务状态机

    特性：
    - 状态转换合法性校验
    - 状态变更回调（钩子）
    - 重试调度
    - 超时管理
    - 状态持久化支持
    """

    def __init__(self, auto_retry: bool = True, default_max_retries: int = 3):
        self.auto_retry = auto_retry
        self.default_max_retries = default_max_retries
        self._tasks: dict[str, TaskRecord] = {}
        self._hooks: dict[State, list[Callable]] = {s: [] for s in State}
        self._retry_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._retry_worker: Optional[asyncio.Task] = None

    # ================================================================
    # 任务管理
    # ================================================================

    def create_task(
        self,
        task_id: str,
        name: str,
        agent_name: str,
        max_retries: int = 3,
        metadata: Optional[dict] = None,
    ) -> TaskRecord:
        """创建新任务"""
        if task_id in self._tasks:
            raise ValueError(f"任务ID已存在: {task_id}")
        record = TaskRecord(
            task_id=task_id,
            name=name,
            agent_name=agent_name,
            current_state=State.PENDING,
            max_retries=max_retries,
            metadata=metadata or {},
        )
        self._tasks[task_id] = record
        return record

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        return self._tasks.get(task_id)

    def get_tasks_by_state(self, state: State) -> list[TaskRecord]:
        return [t for t in self._tasks.values() if t.current_state == state]

    def list_all_tasks(self) -> dict[str, dict]:
        """列出所有任务状态摘要"""
        return {
            task_id: {"state": t.current_state.value, "name": t.name, "agent": t.agent_name}
            for task_id, t in self._tasks.items()
        }

    # ================================================================
    # 状态转换
    # ================================================================

    def start(self, task_id: str) -> TaskRecord:
        """启动任务"""
        task = self._tasks[task_id]
        task.transition_to(State.RUNNING, "任务开始执行")
        self._run_hooks(State.RUNNING, task)
        return task

    def succeed(self, task_id: str, result: Any) -> TaskRecord:
        """标记成功"""
        task = self._tasks[task_id]
        task.result = result
        task.transition_to(State.SUCCESS, "任务成功完成")
        self._run_hooks(State.SUCCESS, task)
        return task

    def fail(
        self,
        task_id: str,
        error: str,
        retry: Optional[bool] = None,
    ) -> TaskRecord:
        """标记失败"""
        task = self._tasks[task_id]
        retry = retry if retry is not None else self.auto_retry

        if retry and task.can_retry():
            task.retry_count += 1
            task.transition_to(State.RETRY, f"失败，准备重试（第{task.retry_count}次）", error=error)
            task.metadata["last_error"] = error
            self._schedule_retry(task)
            self._run_hooks(State.RETRY, task)
        else:
            task.transition_to(State.FAILED, "任务失败（不重试）", error=error)
            self._run_hooks(State.FAILED, task)
        return task

    def timeout(self, task_id: str, timeout_seconds: float) -> TaskRecord:
        """标记超时"""
        task = self._tasks[task_id]
        if task.can_retry():
            task.retry_count += 1
            task.transition_to(State.TIMEOUT, f"执行超时（>{timeout_seconds}s）")
            self._schedule_retry(task)
            self._run_hooks(State.TIMEOUT, task)
        else:
            task.transition_to(State.TIMEOUT, f"执行超时（不重试）")
            self._run_hooks(State.TIMEOUT, task)
        return task

    def cancel(self, task_id: str, reason: str = "") -> TaskRecord:
        """取消任务"""
        task = self._tasks[task_id]
        task.transition_to(State.CANCELLED, reason or "用户取消")
        self._run_hooks(State.CANCELLED, task)
        return task

    def wait(self, task_id: str, reason: str = "") -> TaskRecord:
        """标记为等待依赖"""
        task = self._tasks[task_id]
        task.transition_to(State.WAITING, reason or "等待依赖任务")
        self._run_hooks(State.WAITING, task)
        return task

    def resume(self, task_id: str) -> TaskRecord:
        """恢复等待中的任务"""
        task = self._tasks[task_id]
        task.transition_to(State.RUNNING, "依赖满足，继续执行")
        self._run_hooks(State.RUNNING, task)
        return task

    # ================================================================
    # 重试机制
    # ================================================================

    def _schedule_retry(self, task: TaskRecord):
        """调度重试（指数退避）"""
        delay = min(2 ** task.retry_count * 1.0, 60.0)  # 最多60秒
        logger.info(f"[状态机] 任务 {task.task_id[:8]} 将在 {delay}s 后重试")
        asyncio.create_task(self._retry_later(task.task_id, delay))

    async def _retry_later(self, task_id: str, delay: float):
        await asyncio.sleep(delay)
        task = self._tasks.get(task_id)
        if task and task.current_state == State.RETRY:
            task.transition_to(State.PENDING, "重试等待结束")
            self._run_hooks(State.PENDING, task)

    def start_retry_worker(self):
        """启动重试工作器"""
        if self._retry_worker is None:
            self._retry_worker = asyncio.create_task(self._retry_loop())
            logger.info("[状态机] 重试工作器已启动")

    async def _retry_loop(self):
        while True:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break

    def stop_retry_worker(self):
        if self._retry_worker:
            self._retry_worker.cancel()
            self._retry_worker = None

    # ================================================================
    # 状态钩子
    # ================================================================

    def on_state_change(self, state: State, hook: Callable[[TaskRecord], None]):
        """注册状态变更钩子"""
        self._hooks[state].append(hook)

    def _run_hooks(self, state: State, task: TaskRecord):
        """运行状态变更钩子"""
        for hook in self._hooks[state]:
            try:
                if asyncio.iscoroutinefunction(hook):
                    asyncio.create_task(hook(task))
                else:
                    hook(task)
            except Exception as e:
                logger.error(f"[状态机] 钩子执行失败: {e}")

    # ================================================================
    # 统计与报告
    # ================================================================

    def get_stats(self) -> dict:
        """获取状态统计"""
        counts = {s.value: 0 for s in State}
        for t in self._tasks.values():
            counts[t.current_state.value] += 1

        total_duration = sum(t.total_duration_ms for t in self._tasks.values() if t.completed_at)
        avg_duration = total_duration / max(len([t for t in self._tasks.values() if t.completed_at]), 1)

        return {
            "total_tasks": len(self._tasks),
            "state_distribution": counts,
            "avg_duration_ms": round(avg_duration, 2),
            "total_retries": sum(t.retry_count for t in self._tasks.values()),
            "success_rate": round(
                counts[State.SUCCESS.value] / max(len(self._tasks), 1) * 100, 1
            ),
        }

    def export_tasks(self, path: str):
        """导出所有任务状态"""
        import json
        data = {
            "generated_at": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "tasks": {tid: t.to_dict() for tid, t in self._tasks.items()},
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
