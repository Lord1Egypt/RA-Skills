"""
Workflow Engine - 支持并行/串行混合协作的执行引擎

功能：
- 串行/并行/混合工作流执行
- 任务状态机驱动
- 超时控制
- 中途取消
- 结果聚合
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Optional

from .task_protocol import TaskMessage, TaskState, TaskMode, TaskPriority
from .state_sync import SharedStateManager
from .trace_tracker import CollaborationTracker, SpanType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Agent执行器注册表
# =============================================================================

AgentExecutor = Callable[[TaskMessage], Any]


# =============================================================================
# 工作流执行上下文
# =============================================================================

@dataclass
class WorkflowContext:
    """工作流执行上下文"""
    request_id: str
    trace_id: str
    state_manager: SharedStateManager
    tracker: CollaborationTracker
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    cancelled: bool = False

    def cancel(self):
        self.cancelled = True


# =============================================================================
# 工作流执行器
# =============================================================================

class WorkflowEngine:
    """
    工作流执行引擎

    支持三种执行模式：
    1. 串行（Serial）：按顺序严格执行
    2. 并行（Parallel）：同组内并发执行
    3. 混合（Hybrid）：串行+并行混合编排

    使用协程实现高效的并行执行
    """

    def __init__(
        self,
        state_manager: Optional[SharedStateManager] = None,
        tracker: Optional[CollaborationTracker] = None,
        global_timeout: float = 300.0,
    ):
        self.state_manager = state_manager or SharedStateManager()
        self.tracker = tracker or CollaborationTracker()
        self.global_timeout = global_timeout
        self._executors: dict[str, AgentExecutor] = {}

    def register_executor(self, agent_name: str, executor: AgentExecutor):
        """注册Agent执行器"""
        self._executors[agent_name] = executor
        logger.info(f"已注册执行器: {agent_name}")

    async def execute(
        self,
        tasks: list[TaskMessage],
        request_id: str,
        user_input: str = "",
    ) -> dict[str, Any]:
        """
        执行工作流

        Args:
            tasks: 分解后的任务列表
            request_id: 请求ID

        Returns:
            执行结果字典
        """
        trace_id = self.tracker.start_trace(request_id, user_input)
        ctx = WorkflowContext(
            request_id=request_id,
            trace_id=trace_id,
            state_manager=self.state_manager,
            tracker=self.tracker,
        )

        # 启动根span
        root_span_id = self.tracker.start_span(
            trace_id, f"workflow:{request_id[:8]}", SpanType.ROOT
        )

        logger.info(f"[工作流] 开始执行 {len(tasks)} 个任务, trace_id={trace_id[:8]}")

        try:
            result, has_failures = await asyncio.wait_for(
                self._execute_tasks(tasks, ctx),
                timeout=self.global_timeout,
            )
            self.tracker.end_span(root_span_id, status="ok" if not has_failures else "partial")
            logger.info(f"[工作流] 完成 {request_id[:8]}, 总耗时")
            return {
                "request_id": request_id,
                "trace_id": trace_id,
                "status": "success" if not has_failures else "partial_failure",
                "results": result,
                "trace_report": self.tracker.generate_report(trace_id),
            }
        except asyncio.TimeoutError:
            self.tracker.end_span(root_span_id, status="timeout")
            logger.error(f"[工作流] 超时 {request_id[:8]}")
            return {
                "request_id": request_id,
                "trace_id": trace_id,
                "status": "timeout",
                "error": f"工作流执行超时（>{self.global_timeout}s）",
            }
        except Exception as e:
            self.tracker.end_span(root_span_id, status="error", error=str(e))
            logger.exception(f"[工作流] 失败 {request_id[:8]}: {e}")
            return {
                "request_id": request_id,
                "trace_id": trace_id,
                "status": "error",
                "error": str(e),
            }

    async def _execute_tasks(self, tasks: list[TaskMessage], ctx: WorkflowContext) -> tuple[dict[str, Any], bool]:
        """任务执行主逻辑，返回(results, has_failures)"""
        results: dict[str, Any] = {}
        task_map: dict[str, TaskMessage] = {t.task_id: t for t in tasks}
        has_failures: bool = False

        # 按并行组分类
        serial_tasks: list[TaskMessage] = []
        parallel_groups: dict[str, list[TaskMessage]] = {}
        pending_tasks: dict[str, TaskMessage] = {t.task_id: t for t in tasks}

        for task in tasks:
            if task.mode == TaskMode.PARALLEL and task.parallel_group:
                if task.parallel_group not in parallel_groups:
                    parallel_groups[task.parallel_group] = []
                parallel_groups[task.parallel_group].append(task)
            else:
                serial_tasks.append(task)

        # 拓扑排序串行任务
        serial_tasks = self._topological_sort(serial_tasks, task_map)

        # 执行串行任务
        for task in serial_tasks:
            if ctx.cancelled:
                task.state = TaskState.CANCELLED
                continue

            # 处理并行组
            if task.parallel_group and task.parallel_group in parallel_groups:
                group_results = await self._execute_parallel_group(
                    parallel_groups[task.parallel_group],
                    ctx,
                    results,
                )
                results.update(group_results)
                del parallel_groups[task.parallel_group]

            # 检查依赖
            if not self._check_dependencies(task, results):
                task.state = TaskState.WAITING_DEP
                task.error = "依赖任务未完成"
                continue

            # 执行单个任务
            result = await self._execute_single_task(task, ctx, results)
            results[task.task_id] = result
            if task.state == TaskState.FAILED:
                has_failures = True

        # 执行剩余未处理的并行组
        for group_id, group_tasks in parallel_groups.items():
            group_results = await self._execute_parallel_group(group_tasks, ctx, results)
            results.update(group_results)
            for t in group_tasks:
                if t.state == TaskState.FAILED:
                    has_failures = True

        return results, has_failures

    async def _execute_single_task(
        self,
        task: TaskMessage,
        ctx: WorkflowContext,
        previous_results: dict[str, Any],
    ) -> Any:
        """执行单个任务"""
        span_id = self.tracker.start_span(
            ctx.trace_id,
            f"{task.agent_name}:{task.action}",
            SpanType.AGENT,
            agent_name=task.agent_name,
            metadata={
                "task_id": task.task_id,
                "priority": task.priority.value,
                "parallel_group": task.parallel_group,
            },
        )

        task.state = TaskState.RUNNING
        task.started_at = datetime.now().isoformat()

        # 将依赖结果注入参数
        enriched_params = {**task.parameters}
        for dep_id in task.dependency.depends_on:
            if dep_id in previous_results:
                enriched_params[f"dep_result_{dep_id[:8]}"] = previous_results[dep_id]

        # 共享上下文
        if task.dependency.shared_context and ctx.state_manager:
            shared = await ctx.state_manager.get_many(task.dependency.shared_context)
            enriched_params["_shared_context"] = shared

        try:
            executor = self._executors.get(task.agent_name)
            if executor is None:
                # 兜底：返回模拟结果
                logger.warning(f"未找到执行器 [{task.agent_name}]，使用模拟结果")
                task.succeed({"status": "mock", "message": f"无执行器[{task.agent_name}]，返回模拟结果"})
                self.tracker.end_span(span_id, status="ok")
                return task.result

            # 超时控制
            if asyncio.iscoroutinefunction(executor):
                result = await asyncio.wait_for(
                    executor(task),
                    timeout=task.timeout_seconds,
                )
            else:
                result = executor(task)

            task.succeed(result)
            self.tracker.end_span(span_id, status="ok")

            # 写入共享状态
            if ctx.state_manager:
                await ctx.state_manager.set(
                    f"result:{task.task_id}",
                    result,
                    ttl_seconds=300,
                    agent_id=task.agent_name,
                )

            return result

        except asyncio.TimeoutError:
            task.state = TaskState.TIMEOUT
            task.error = f"执行超时（>{task.timeout_seconds}s）"
            self.tracker.end_span(span_id, status="timeout", error=task.error)
            logger.warning(f"[工作流] 任务 {task.task_id[:8]} 执行超时")
            return None

        except Exception as e:
            task.fail(str(e))
            self.tracker.end_span(span_id, status="error", error=str(e))
            logger.error(f"[工作流] 任务 {task.task_id[:8]} 执行失败: {e}")
            return None

    async def _execute_parallel_group(
        self,
        tasks: list[TaskMessage],
        ctx: WorkflowContext,
        previous_results: dict[str, Any],
    ) -> dict[str, Any]:
        """并发执行一组并行任务"""
        group_id = tasks[0].parallel_group or "unknown"

        span_id = self.tracker.start_span(
            ctx.trace_id,
            f"parallel_group:{group_id}",
            SpanType.PARALLEL_GROUP,
            metadata={"task_count": len(tasks)},
        )

        logger.info(f"[工作流] 开始并行组 {group_id}（{len(tasks)}个任务）")

        # 并发执行所有任务
        coroutines = [
            self._execute_single_task(task, ctx, previous_results)
            for task in tasks
        ]
        group_results_list = await asyncio.gather(*coroutines, return_exceptions=True)

        results = {}
        for task, result in zip(tasks, group_results_list):
            if isinstance(result, Exception):
                task.fail(str(result))
                results[task.task_id] = None
            else:
                results[task.task_id] = result

        self.tracker.end_span(span_id, status="ok")
        logger.info(f"[工作流] 并行组 {group_id} 完成")
        return results

    def _check_dependencies(self, task: TaskMessage, results: dict[str, Any]) -> bool:
        """检查依赖是否满足"""
        if not task.dependency.depends_on:
            return True
        for dep_id in task.dependency.depends_on:
            if dep_id not in results:
                return False
        return True

    def _topological_sort(
        self,
        tasks: list[TaskMessage],
        task_map: dict[str, TaskMessage],
    ) -> list[TaskMessage]:
        """拓扑排序"""
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

        sorted_ids = {t.task_id for t in sorted_tasks}
        sorted_tasks.extend([t for t in tasks if t.task_id not in sorted_ids])

        return sorted_tasks
