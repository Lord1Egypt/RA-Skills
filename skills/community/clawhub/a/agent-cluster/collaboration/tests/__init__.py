"""
协作模块单元测试

测试范围：
1. TaskProtocol - 任务协议序列化/状态机
2. WorkflowEngine - 串行/并行/混合执行
3. SharedStateManager - 跨Agent状态同步（async）
4. CollaborationTracker - 链路追踪
5. TaskDecompositionEngine - 任务分解

运行方式：
pytest agent-cluster/collaboration/tests/ -v
"""

import asyncio
import sys
import os

# 确保协作模块可导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch
import time

import pytest

# =============================================================================
# TaskProtocol 测试
# =============================================================================

from collaboration.task_protocol import (
    TaskMessage, TaskDependency, TaskContext,
    TaskPriority, TaskMode, TaskState,
    TaskDecompositionEngine,
)


class TestTaskProtocol:
    """TaskProtocol 序列化与状态机测试"""

    def test_task_message_creation(self):
        """测试TaskMessage基本创建"""
        msg = TaskMessage(
            agent_name="inventory_agent",
            action="query_stock",
            parameters={"sku": "SKU001"},
        )
        assert msg.task_id is not None
        assert msg.agent_name == "inventory_agent"
        assert msg.action == "query_stock"
        assert msg.state == TaskState.CREATED
        assert msg.priority == TaskPriority.NORMAL

    def test_task_message_state_transitions(self):
        """测试TaskMessage状态转换"""
        msg = TaskMessage(agent_name="test", action="test")

        msg.start()
        assert msg.state == TaskState.RUNNING
        assert msg.started_at is not None

        msg.succeed({"result": "ok"})
        assert msg.state == TaskState.SUCCESS
        assert msg.completed_at is not None

    def test_task_message_state_transitions_fail(self):
        """测试TaskMessage失败转换"""
        msg = TaskMessage(agent_name="test", action="test")
        msg.start()

        msg.fail("Connection timeout")
        assert msg.state == TaskState.FAILED
        assert msg.error == "Connection timeout"

    def test_task_message_retry_logic(self):
        """测试重试逻辑"""
        msg = TaskMessage(agent_name="test", action="test", max_retries=3)

        assert msg.can_retry() is True
        assert msg.is_terminal() is False

        msg.mark_retry()
        assert msg.state == TaskState.RETRY
        assert msg.retry_count == 1
        assert msg.can_retry() is True

        msg.mark_retry()
        msg.mark_retry()
        assert msg.can_retry() is False  # 达到上限

    def test_task_message_serialization_roundtrip(self):
        """测试序列化往返"""
        ctx = TaskContext(request_id="req-123", user_id="user-1")
        dep = TaskDependency(depends_on=["task-A", "task-B"], blocking=True)

        original = TaskMessage(
            task_id="task-X",
            parent_id="task-parent",
            agent_name="finance_agent",
            action="audit_payment",
            priority=TaskPriority.HIGH,
            context=ctx,
            dependency=dep,
        )

        data = original.to_dict()
        restored = TaskMessage.from_dict(data)

        assert restored.task_id == original.task_id
        assert restored.parent_id == original.parent_id
        assert restored.agent_name == original.agent_name
        assert restored.priority == original.priority.value
        assert restored.context.request_id == "req-123"
        assert restored.dependency.depends_on == ["task-A", "task-B"]

    def test_task_message_json_serialization(self):
        """测试JSON序列化"""
        msg = TaskMessage(agent_name="test", action="test")
        data = msg.to_dict()

        assert data["agent_name"] == "test"
        assert data["state"] in ("created", "running", "success", "failed")

    def test_task_context_to_dict(self):
        """测试TaskContext序列化"""
        ctx = TaskContext(
            request_id="req-456",
            user_id="user-2",
            session_id="sess-789",
        )
        d = ctx.to_dict()
        assert d["request_id"] == "req-456"
        assert d["user_id"] == "user-2"


class TestTaskDecompositionEngine:
    """任务分解引擎测试"""

    def test_stock_replenishment_decomposition(self):
        """测试库存补货工作流分解"""
        engine = TaskDecompositionEngine()
        tasks = engine.decompose(
            workflow_name="stock_replenishment",
            parameters={"sku": "SKU001"},
        )

        assert len(tasks) >= 5
        agent_names = {t.agent_name for t in tasks}
        assert "inventory_agent" in agent_names
        assert "procurement_agent" in agent_names

    def test_procurement_workflow_decomposition(self):
        """测试采购物流工作流"""
        engine = TaskDecompositionEngine()
        tasks = engine.decompose(
            workflow_name="procurement_with_logistics",
            parameters={"product_id": "P001"},
        )
        assert len(tasks) >= 3
        assert all(t.agent_name in {"procurement_agent", "finance_agent", "logistics_agent", "orchestrator"}
                   for t in tasks)

    def test_unknown_workflow_fallback(self):
        """测试未知工作流兜底"""
        engine = TaskDecompositionEngine()
        tasks = engine.decompose(
            workflow_name="unknown_workflow",
            parameters={"key": "value"},
        )
        assert len(tasks) == 1
        assert tasks[0].agent_name == "orchestrator"
        assert tasks[0].action == "fallback"

    def test_decomposition_with_context(self):
        """测试带上下文的分解"""
        engine = TaskDecompositionEngine()
        ctx = TaskContext(request_id="req-test", user_id="test-user")

        tasks = engine.decompose(
            workflow_name="stock_replenishment",
            parameters={"test": True},
            context=ctx,
        )
        assert all(t.context is not None for t in tasks)
        assert tasks[0].context.request_id == "req-test"


# =============================================================================
# SharedStateManager 测试（async）
# =============================================================================

from collaboration.state_sync import SharedStateManager, SyncStatus


class TestSharedStateManager:
    """共享状态管理器测试（async方法）"""

    @pytest.mark.asyncio
    async def test_init_and_set(self):
        """测试初始化与设置"""
        mgr = SharedStateManager(agent_id="test-agent")
        entry = await mgr.set("key1", {"data": "value"}, agent_id="req-1")
        val = await mgr.get("key1")
        assert val == {"data": "value"}
        assert entry.sync_status == SyncStatus.SYNCED

    @pytest.mark.asyncio
    async def test_get_nonexistent(self):
        """测试获取不存在的key"""
        mgr = SharedStateManager()
        val = await mgr.get("nonexistent")
        assert val is None

    @pytest.mark.asyncio
    async def test_update_existing(self):
        """测试更新已存在的key"""
        mgr = SharedStateManager()
        await mgr.set("key1", {"v": 1}, agent_id="req-1")
        await mgr.set("key1", {"v": 2}, agent_id="req-2")
        val = await mgr.get("key1")
        assert val == {"v": 2}

    @pytest.mark.asyncio
    async def test_version_tracking(self):
        """测试版本跟踪"""
        mgr = SharedStateManager()
        await mgr.set("key1", "v1", agent_id="req-1")
        await mgr.set("key1", "v2", agent_id="req-2")
        v = await mgr.get_version("key1")
        assert v == 2

    @pytest.mark.asyncio
    async def test_delete(self):
        """测试删除"""
        mgr = SharedStateManager()
        await mgr.set("a", 1, agent_id="req-1")
        await mgr.set("b", 2, agent_id="req-1")

        deleted = await mgr.delete("b")
        assert deleted is True

        val = await mgr.get("b")
        assert val is None

    @pytest.mark.asyncio
    async def test_bulk_operations(self):
        """测试批量操作"""
        mgr = SharedStateManager()
        await mgr.set_many({"x": 1, "y": 2, "z": 3})

        vals = await mgr.get_many(["x", "y", "z"])
        assert vals["x"] == 1
        assert vals["y"] == 2
        assert vals["z"] == 3

    @pytest.mark.asyncio
    async def test_state_entry_metadata(self):
        """测试状态条目元数据"""
        mgr = SharedStateManager()
        entry = await mgr.set("meta_test", "value", agent_id="agent-1", ttl_seconds=60.0)

        assert entry.key == "meta_test"
        assert entry.value == "value"
        assert entry.agent_id == "agent-1"
        assert entry.version == 1
        assert entry.ttl_seconds == 60.0
        assert entry.is_expired() is False


# =============================================================================
# CollaborationTracker 测试
# =============================================================================

from collaboration.trace_tracker import CollaborationTracker, SpanType


class TestCollaborationTracker:
    """链路追踪器测试"""

    def test_init(self):
        """测试初始化"""
        tracker = CollaborationTracker()
        assert tracker.max_spans == 1000
        assert len(tracker._spans) == 0

    def test_start_trace(self):
        """测试启动追踪"""
        tracker = CollaborationTracker()
        trace_id = tracker.start_trace("req-test", "查询库存")

        assert trace_id is not None
        assert len(trace_id) > 0

    def test_span_lifecycle(self):
        """测试Span生命周期"""
        tracker = CollaborationTracker()
        trace_id = tracker.start_trace("req-span", "test")

        span_id = tracker.start_span(trace_id, "test-span", SpanType.AGENT)
        assert span_id is not None

        tracker.end_span(span_id, status="ok")
        assert tracker._spans[span_id].status == "ok"

    def test_span_with_error(self):
        """测试错误Span"""
        tracker = CollaborationTracker()
        trace_id = tracker.start_trace("req-err", "test")

        span_id = tracker.start_span(trace_id, "error-span", SpanType.AGENT)
        tracker.end_span(span_id, status="error", error="Connection refused")

        assert tracker._spans[span_id].status == "error"

    def test_nested_spans(self):
        """测试嵌套Span"""
        tracker = CollaborationTracker()
        trace_id = tracker.start_trace("req-nested", "test")

        parent = tracker.start_span(trace_id, "parent", SpanType.ROOT)
        child1 = tracker.start_span(trace_id, "child1", SpanType.AGENT)
        child2 = tracker.start_span(trace_id, "child2", SpanType.AGENT)

        tracker.end_span(child1, status="ok")
        tracker.end_span(child2, status="ok")
        tracker.end_span(parent, status="ok")

        assert tracker._spans[parent].status == "ok"

    def test_report_generation(self):
        """测试报告生成"""
        tracker = CollaborationTracker()
        trace_id = tracker.start_trace("req-report", "查询库存")

        span_id = tracker.start_span(trace_id, "inventory:query", SpanType.AGENT)
        tracker.end_span(span_id, status="ok")

        report = tracker.generate_report(trace_id)
        assert "total_spans" in report
        assert report["total_spans"] >= 1

    def test_mermaid_export(self):
        """测试Mermaid格式导出"""
        tracker = CollaborationTracker()
        trace_id = tracker.start_trace("req-mermaid", "test")

        parent = tracker.start_span(trace_id, "workflow", SpanType.ROOT)
        child = tracker.start_span(trace_id, "subtask", SpanType.AGENT)
        tracker.end_span(child, status="ok")
        tracker.end_span(parent, status="ok")

        mermaid = tracker.to_mermaid_sequence(trace_id)
        assert "sequenceDiagram" in mermaid or "participant" in mermaid


# =============================================================================
# WorkflowEngine 测试
# =============================================================================

from collaboration.workflow_engine import WorkflowEngine, WorkflowContext
from collaboration.state_sync import SharedStateManager


class TestWorkflowEngine:
    """工作流引擎测试"""

    def test_init(self):
        """测试初始化"""
        engine = WorkflowEngine()
        assert engine.state_manager is not None
        assert engine.tracker is not None
        assert engine.global_timeout == 300.0

    def test_custom_init(self):
        """测试自定义初始化"""
        state_mgr = SharedStateManager()
        tracker = CollaborationTracker()
        engine = WorkflowEngine(
            state_manager=state_mgr,
            tracker=tracker,
            global_timeout=600.0,
        )
        assert engine.global_timeout == 600.0

    def test_register_executor(self):
        """测试注册执行器"""
        engine = WorkflowEngine()

        async def mock_executor(msg):
            return {"status": "ok"}

        engine.register_executor("inventory_agent", mock_executor)
        assert "inventory_agent" in engine._executors

    @pytest.mark.asyncio
    async def test_execute_single_task(self):
        """测试单任务执行"""
        engine = WorkflowEngine()

        async def inventory_executor(msg):
            await asyncio.sleep(0.01)
            return {"sku": msg.parameters.get("sku", "unknown"), "qty": 100}

        engine.register_executor("inventory_agent", inventory_executor)

        task = TaskMessage(
            agent_name="inventory_agent",
            action="query_stock",
            parameters={"sku": "SKU001"},
        )

        result = await engine.execute(
            tasks=[task],
            request_id="req-single-test",
            user_input="查询库存",
        )

        assert result["status"] == "success"
        assert result["request_id"] == "req-single-test"

    @pytest.mark.asyncio
    async def test_execute_multiple_serial_tasks(self):
        """测试多任务串行执行"""
        engine = WorkflowEngine()
        execution_order = []

        async def step1(msg):
            await asyncio.sleep(0.01)
            execution_order.append("step1")
            return {"step": 1}

        async def step2(msg):
            await asyncio.sleep(0.01)
            execution_order.append("step2")
            return {"step": 2}

        engine.register_executor("step1_agent", step1)
        engine.register_executor("step2_agent", step2)

        tasks = [
            TaskMessage(agent_name="step1_agent", action="do", parameters={}),
            TaskMessage(agent_name="step2_agent", action="do", parameters={}),
        ]

        result = await engine.execute(
            tasks=tasks,
            request_id="req-serial-test",
        )

        assert result["status"] == "success"
        assert execution_order == ["step1", "step2"]

    @pytest.mark.asyncio
    async def test_execute_parallel_group(self):
        """测试并行组执行"""
        engine = WorkflowEngine()
        start_times = {}

        async def slow_task(msg, name, delay):
            start_times[name] = time.time()
            await asyncio.sleep(delay)
            return {"task": name}

        engine.register_executor("parallel_a",
            lambda m: slow_task(m, "a", 0.05))
        engine.register_executor("parallel_b",
            lambda m: slow_task(m, "b", 0.05))

        tasks = [
            TaskMessage(
                agent_name="parallel_a",
                action="do",
                mode=TaskMode.PARALLEL,
                parallel_group="pg1",
            ),
            TaskMessage(
                agent_name="parallel_b",
                action="do",
                mode=TaskMode.PARALLEL,
                parallel_group="pg1",
            ),
        ]

        result = await engine.execute(
            tasks=tasks,
            request_id="req-parallel-test",
        )

        assert result["status"] == "success"
        assert len(result.get("results", {})) == 2

        # 并行执行：两个任务同时sleep 0.05s，总时间 < 0.1s
        # 注意：由于asyncio并发，总时间应该接近0.05s而非0.1s

    @pytest.mark.asyncio
    async def test_execute_unknown_agent_mock_fallback(self):
        """测试未知Agent使用模拟结果（现有行为）"""
        engine = WorkflowEngine()

        task = TaskMessage(
            agent_name="nonexistent_agent",
            action="do",
        )

        result = await engine.execute(
            tasks=[task],
            request_id="req-unknown-agent",
        )

        # 现有行为：未知Agent使用mock结果而非报错
        # 这是一种graceful degradation策略
        assert result["status"] == "success"
        assert "results" in result

    @pytest.mark.asyncio
    async def test_execute_with_trace_report(self):
        """测试trace报告生成"""
        engine = WorkflowEngine()

        async def dummy(msg):
            return {"ok": True}

        engine.register_executor("dummy", dummy)

        task = TaskMessage(agent_name="dummy", action="do")
        result = await engine.execute(
            tasks=[task],
            request_id="req-trace-test",
        )

        assert "trace_report" in result
        assert "total_spans" in result["trace_report"]


class TestWorkflowEngineEdgeCases:
    """工作流引擎边界场景测试"""

    @pytest.mark.asyncio
    async def test_empty_task_list(self):
        """测试空任务列表"""
        engine = WorkflowEngine()
        result = await engine.execute(
            tasks=[],
            request_id="req-empty",
        )
        assert result["status"] == "success"
        assert result["results"] == {}

    @pytest.mark.asyncio
    async def test_task_with_error_caught(self):
        """测试任务执行异常被捕获，工作流标记为partial_failure"""
        engine = WorkflowEngine()

        async def failing_executor(msg):
            raise RuntimeError("Simulated agent failure")

        engine.register_executor("fail_agent", failing_executor)

        task = TaskMessage(agent_name="fail_agent", action="fail")
        result = await engine.execute(
            tasks=[task],
            request_id="req-fail-test",
        )

        # 异常被捕获，工作流不崩溃，但标记为partial_failure
        assert result["status"] == "partial_failure"

    def test_check_dependencies_no_deps(self):
        """测试无依赖检查"""
        engine = WorkflowEngine()
        task = TaskMessage(agent_name="test", action="do")
        assert engine._check_dependencies(task, {}) is True

    def test_check_dependencies_unsatisfied(self):
        """测试依赖未满足"""
        engine = WorkflowEngine()
        task = TaskMessage(
            agent_name="dependent",
            action="do",
            dependency=TaskDependency(depends_on=["missing-task"]),
        )
        assert engine._check_dependencies(task, {}) is False

    def test_check_dependencies_satisfied(self):
        """测试依赖已满足"""
        engine = WorkflowEngine()
        task = TaskMessage(
            agent_name="dependent",
            action="do",
            dependency=TaskDependency(depends_on=["task-A", "task-B"]),
        )
        results = {"task-A": {}, "task-B": {}}
        assert engine._check_dependencies(task, results) is True

    def test_workflow_context_cancel(self):
        """测试工作流上下文取消"""
        tracker = CollaborationTracker()
        state_mgr = SharedStateManager()
        ctx = WorkflowContext(
            request_id="req-cancel",
            trace_id=tracker.start_trace("req-cancel", "test"),
            state_manager=state_mgr,
            tracker=tracker,
        )
        ctx.cancel()
        assert ctx.cancelled is True


class TestIntegrationScenarios:
    """端到端集成场景测试"""

    @pytest.mark.asyncio
    async def test_concurrent_workflows_isolation(self):
        """测试并发工作流隔离"""
        engine = WorkflowEngine()

        async def slow(msg):
            await asyncio.sleep(0.1)
            return {"req": msg.context.request_id if msg.context else "unknown"}

        engine.register_executor("slow_agent", slow)

        task1 = TaskMessage(agent_name="slow_agent", action="do")
        task2 = TaskMessage(agent_name="slow_agent", action="do")

        results = await asyncio.gather(
            engine.execute(tasks=[task1], request_id="req-concurrent-1"),
            engine.execute(tasks=[task2], request_id="req-concurrent-2"),
        )

        assert all(r["status"] == "success" for r in results)
        assert results[0]["request_id"] == "req-concurrent-1"
        assert results[1]["request_id"] == "req-concurrent-2"


class TestPerformanceBenchmarks:
    """性能基准测试"""

    @pytest.mark.asyncio
    async def test_parallel_speedup_vs_serial(self):
        """测试并行相比串行的加速"""
        engine = WorkflowEngine()

        async def worker(msg):
            await asyncio.sleep(0.1)
            return {"done": True}

        engine.register_executor("worker", worker)

        # 串行：3 × 0.1s
        serial_tasks = [
            TaskMessage(agent_name="worker", action="do"),
            TaskMessage(agent_name="worker", action="do"),
            TaskMessage(agent_name="worker", action="do"),
        ]

        start_serial = time.time()
        await engine.execute(tasks=serial_tasks, request_id="req-serial-perf")
        serial_time = time.time() - start_serial

        # 并行：0.1s（asyncio并发）
        parallel_tasks = [
            TaskMessage(agent_name="worker", action="do",
                       mode=TaskMode.PARALLEL, parallel_group="pg"),
            TaskMessage(agent_name="worker", action="do",
                       mode=TaskMode.PARALLEL, parallel_group="pg"),
            TaskMessage(agent_name="worker", action="do",
                       mode=TaskMode.PARALLEL, parallel_group="pg"),
        ]

        start_parallel = time.time()
        await engine.execute(tasks=parallel_tasks, request_id="req-parallel-perf")
        parallel_time = time.time() - start_parallel

        # 并行应该比串行快至少1.5倍
        speedup = serial_time / parallel_time
        assert speedup > 1.5, f"并行加速比不足: {speedup:.2f}x（预期>1.5x）"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
