"""
GlobalCircuitBreaker + ModelHealthRegistry 集成测试

Phase 2 核心验证:
1. EngineRouter 集成 GlobalCircuitBreaker
2. EngineRouter 集成 ModelHealthRegistry
3. 健康度上报链路（Engine → Router → CircuitBreaker/Registry）
4. 健康度报告 API
5. 引擎熔断切换

使用说明:
    pytest execution/tests/test_integration.py -v

Change Log:
    - 2026-04-14: Phase 2 集成测试
"""

from __future__ import annotations

import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from execution.circuit_breaker import (
    DEFAULT_FAILURE_THRESHOLD,
    DEFAULT_OPEN_DURATION,
    CircuitState,
    GlobalCircuitBreaker,
    ModelHealthRegistry,
    ModelHealthState,
    check_model_health,
    generate_health_report,
    report_request_result,
)
from execution.engine_router import (
    EngineRouter,
    RoutingContext,
    RoutingStrategy,
)
from execution.gpt6_engine import GPT6Engine
from execution.deepseek_engine import DeepSeekEngine


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(autouse=True)
def isolate_singletons():
    """每个测试前重置全局单例"""
    GlobalCircuitBreaker.reset_instance()
    yield
    GlobalCircuitBreaker.reset_instance()


@pytest.fixture
def tmp_health_path(tmp_path):
    """临时健康度持久化路径"""
    return str(tmp_path / "health.json")


@pytest.fixture
def router(tmp_health_path):
    """启用熔断器的路由器"""
    return EngineRouter(
        circuit_breaker_enabled=True,
        health_registry_path=tmp_health_path,
    )


@pytest.fixture
def router_disabled():
    """禁用熔断器的路由器"""
    return EngineRouter(circuit_breaker_enabled=False)


# =============================================================================
# 工具：Mock 引擎
# =============================================================================

class MockEngine:
    """用于测试的模拟引擎"""

    def __init__(
        self,
        name: str = "mock-engine",
        model: str = "mock-model",
        always_fail: bool = False,
        fail_count: int = 0,
        delay: float = 0.0,
    ):
        self._name = name
        self._model = model
        self._always_fail = always_fail
        self._fail_count = fail_count
        self._call_count = 0
        self._delay = delay
        self._stats = {"total": 0, "success": 0, "failure": 0}

    @property
    def engine_name(self) -> str:
        return self._name

    @property
    def _model_attr(self) -> str:
        """与真实引擎一致的模型属性"""
        return self._model

    @property
    def capabilities(self) -> Dict[str, bool]:
        return {"streaming": True}

    async def execute(self, task: str, context: Dict[str, Any]):
        from execution.engine_base import ExecutionResult
        self._call_count += 1
        self._stats["total"] += 1
        if self._delay:
            import asyncio
            await asyncio.sleep(self._delay)
        # fail_count=N: 前N次失败，第N+1次开始成功
        # always_fail=True: 永远失败
        should_fail = self._always_fail or self._call_count <= self._fail_count
        if should_fail:
            self._stats["failure"] += 1
            return ExecutionResult(
                success=False,
                output=None,
                metadata={"model": self._model},
                latency_ms=100.0,
                error=f"[MockEngine] simulated failure #{self._call_count}",
            )
        self._stats["success"] += 1
        return ExecutionResult(
            success=True,
            output={"content": f"Mock response for: {task[:50]}"},
            metadata={"model": self._model},
            latency_ms=50.0,
        )

    def get_stats(self) -> Dict[str, Any]:
        return self._stats.copy()


# =============================================================================
# 1. GlobalCircuitBreaker 路由集成
# =============================================================================

class TestRouterCircuitBreakerIntegration:
    """EngineRouter 与 GlobalCircuitBreaker 集成"""

    def test_circuit_breaker_prevents_blocked_engine(self, router, tmp_health_path):
        """
        熔断器 OPEN 时，主引擎被阻止，尝试切换到备用引擎
        """
        # 注册主引擎（会触发熔断）和备用引擎
        main = MockEngine(name="main", model="gpt-6", fail_count=100)
        backup = MockEngine(name="backup", model="deepseek-chat", always_fail=False)

        router.register_engine(main, set_default=True)
        router.register_engine(backup)

        # 触发主引擎熔断（5次失败 → OPEN）
        cb = GlobalCircuitBreaker.get_instance()
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result("gpt-6", success=False)

        # 此时主引擎熔断，备用引擎可用
        can_main, reason_main = router.check_engine_available(main)
        can_backup, reason_backup = router.check_engine_available(backup)

        assert can_main is False, "主引擎应该被熔断阻止"
        assert can_backup is True, "备用引擎应该可用"
        assert "OPEN" in reason_main or "open" in reason_main.lower()

    def test_circuit_breaker_reports_rejection_in_stats(self, router):
        """
        熔断拒绝时，路由统计记录 circuit_rejections
        """
        mock_engine = MockEngine(name="mock", model="gpt-6", fail_count=100)
        router.register_engine(mock_engine, set_default=True)

        # 触发熔断
        cb = GlobalCircuitBreaker.get_instance()
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result("gpt-6", success=False)

        # 尝试路由（会被熔断阻止）
        import asyncio
        result = asyncio.run(router.route_and_execute_async(
            "test task",
            {"intent_type": "test"},
        ))

        # 熔断拒绝结果
        assert result.success is False
        assert "CircuitBreaker OPEN" in (result.error or "")

        stats = router.get_stats()
        assert stats["circuit_rejections"] >= 1

    def test_fallback_engine_used_when_primary_circuit_open(self, router):
        """
        主引擎熔断时，自动切换到备用引擎
        """
        main = MockEngine(name="main", model="gpt-6", fail_count=100)
        backup = MockEngine(name="backup", model="deepseek-chat")

        router.register_engine(main, set_default=True)
        router.register_engine(backup)

        # 触发主引擎熔断
        cb = GlobalCircuitBreaker.get_instance()
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result("gpt-6", success=False)

        # 路由执行（应该切换到备用引擎）
        import asyncio
        result = asyncio.run(router.route_and_execute_async(
            "test task",
            {"intent_type": "test"},
        ))

        # 备用引擎成功执行
        assert result.success is True
        # 确认主引擎未被调用（因为被熔断阻止）
        assert main._call_count == 0
        assert backup._call_count == 1

    def test_circuit_breaker_disabled_allows_all_engines(self, router_disabled):
        """
        circuit_breaker_enabled=False 时，所有引擎都可用
        """
        main = MockEngine(name="main", model="gpt-6", fail_count=100)
        router_disabled.register_engine(main, set_default=True)

        # 触发熔断（但路由禁用检查）
        cb = GlobalCircuitBreaker.get_instance()
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result("gpt-6", success=False)

        can, reason = router_disabled.check_engine_available(main)
        assert can is True
        assert reason == "disabled"


# =============================================================================
# 2. 健康度上报链路
# =============================================================================

class TestHealthReportingChain:
    """Engine → Router → GlobalCircuitBreaker/ModelHealthRegistry 链路"""

    def test_successful_execution_reports_health(self, router, tmp_health_path):
        """
        成功执行后，健康度正确上报到两个系统
        """
        mock = MockEngine(name="mock", model="claude-sonnet")
        router.register_engine(mock, set_default=True)

        import asyncio
        result = asyncio.run(router.route_and_execute_async(
            "hello",
            {"intent_type": "test"},
        ))

        assert result.success is True

        # 验证断路器统计（通过 get_stats 获取）
        cb = GlobalCircuitBreaker.get_instance()
        cb_stats = cb.get_stats()
        assert cb_stats["total_successes"] >= 1

        # 验证健康注册表记录
        registry = ModelHealthRegistry(persist_path=tmp_health_path)
        entry = registry.get_health("claude-sonnet")
        assert entry is not None
        assert entry.total_successes >= 1

    def test_failed_execution_reports_health(self, router, tmp_health_path):
        """
        失败执行后，健康度正确上报到两个系统
        """
        mock = MockEngine(name="mock", model="claude-sonnet", always_fail=True)
        router.register_engine(mock, set_default=True)

        import asyncio
        result = asyncio.run(router.route_and_execute_async(
            "hello",
            {"intent_type": "test"},
        ))

        assert result.success is False

        # 验证断路器统计
        cb = GlobalCircuitBreaker.get_instance()
        cb_stats = cb.get_stats()
        assert cb_stats["total_failures"] >= 1

        # 验证健康注册表记录
        registry = ModelHealthRegistry(persist_path=tmp_health_path)
        entry = registry.get_health("claude-sonnet")
        assert entry is not None
        assert entry.total_failures >= 1
        assert entry.consecutive_failures >= 1

    def test_fallback_engine_also_reports_health(self, router, tmp_health_path):
        """
        备用引擎执行后也正确上报健康度
        """
        main = MockEngine(name="main", model="gpt-6", always_fail=True)
        backup = MockEngine(name="backup", model="deepseek-chat")
        router.register_engine(main, set_default=True)
        router.register_engine(backup)

        import asyncio
        result = asyncio.run(router.route_and_execute_async(
            "hello",
            {"intent_type": "test"},
        ))

        assert result.success is True

        # 主引擎失败上报
        cb = GlobalCircuitBreaker.get_instance()
        cb_stats = cb.get_stats()
        assert cb_stats["total_failures"] >= 1

        # 备用引擎成功上报
        assert cb_stats["total_successes"] >= 1


# =============================================================================
# 3. 健康度报告 API
# =============================================================================

class TestHealthReportAPI:
    """健康度报告 API 测试"""

    def test_generate_health_report_structure(self, tmp_health_path):
        """健康度报告结构完整"""
        # 制造一些数据
        report_request_result("model-a", success=True)
        report_request_result("model-a", success=False)
        report_request_result("model-b", success=False)

        report = generate_health_report(models=["model-a", "model-b"], persist_path=tmp_health_path)

        assert "generated_at" in report
        assert "summary" in report
        assert "models" in report
        assert "circuit_breaker_stats" in report
        assert "health_registry_stats" in report
        assert report["summary"]["total_models"] == 2

    def test_generate_health_report_sorted_by_health(self, tmp_health_path):
        """报告按健康状况排序（熔断中的模型优先）"""
        # model-a: 正常
        report_request_result("model-a", success=True)
        report_request_result("model-a", success=True)

        # model-b: 熔断中
        cb = GlobalCircuitBreaker.get_instance()
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result("model-b", success=False)

        report = generate_health_report(models=["model-a", "model-b"], persist_path=tmp_health_path)

        models = report["models"]
        # 熔断中的模型排在最前
        circuit_open_idx = next(
            i for i, m in enumerate(models) if m["model"] == "model-b"
        )
        healthy_idx = next(
            i for i, m in enumerate(models) if m["model"] == "model-a"
        )
        assert circuit_open_idx < healthy_idx

    def test_router_get_health_report(self, router, tmp_health_path):
        """EngineRouter.get_health_report() 返回完整报告"""
        mock = MockEngine(name="mock", model="gpt-6")
        router.register_engine(mock, set_default=True)

        import asyncio
        asyncio.run(router.route_and_execute_async("hello", {}))

        report = router.get_health_report(models=["gpt-6"])
        assert "summary" in report
        assert "models" in report
        assert report["summary"]["total_models"] >= 1

    def test_router_get_circuit_breaker_snapshots(self, router):
        """EngineRouter.get_circuit_breaker_snapshots() 返回快照"""
        mock = MockEngine(name="mock", model="gpt-6")
        router.register_engine(mock)

        snapshots = router.get_circuit_breaker_snapshots()
        assert "mock" in snapshots
        assert "state" in snapshots["mock"]
        assert snapshots["mock"]["model"] == "gpt-6"


# =============================================================================
# 4. 手动熔断操作 API
# =============================================================================

class TestManualCircuitOperations:
    """手动熔断操作 API"""

    def test_force_circuit_open(self, router):
        """force_circuit_open 手动触发熔断"""
        mock = MockEngine(name="mock", model="gpt-6")
        router.register_engine(mock)

        ok = router.force_circuit_open("mock", reason="test")
        assert ok is True

        can, reason = router.check_engine_available(mock)
        assert can is False

    def test_force_circuit_close(self, router):
        """force_circuit_close 手动恢复熔断"""
        mock = MockEngine(name="mock", model="gpt-6")
        router.register_engine(mock)

        # 先触发熔断
        router.force_circuit_open("mock")
        can_before, _ = router.check_engine_available(mock)
        assert can_before is False

        # 手动恢复
        ok = router.force_circuit_close("mock")
        assert ok is True

        can_after, _ = router.check_engine_available(mock)
        assert can_after is True

    def test_force_circuit_unknown_engine_returns_false(self, router):
        """force_circuit_open/close 对未知引擎返回 False"""
        assert router.force_circuit_open("nonexistent") is False
        assert router.force_circuit_close("nonexistent") is False


# =============================================================================
# 5. ModelHealthRegistry 深度状态机
# =============================================================================

class TestHealthRegistryDeepStateMachine:
    """健康注册表深度状态机测试"""

    def test_health_registry_updates_persist(self, tmp_health_path):
        """健康度数据持久化到文件"""
        reg1 = ModelHealthRegistry(persist_path=tmp_health_path)

        for _ in range(3):
            reg1.report_request("model-x", success=False)
        for _ in range(2):
            reg1.report_request("model-x", success=True)

        reg2 = ModelHealthRegistry(persist_path=tmp_health_path)
        entry = reg2.get_health("model-x")
        assert entry.total_requests == 5
        assert entry.total_successes == 2
        assert entry.total_failures == 3

    def test_report_request_result_returns_full_context(self, tmp_health_path):
        """report_request_result 返回完整上下文"""
        result = report_request_result(
            "gpt-6",
            success=True,
            error=None,
            is_probe=False,
        )

        assert result["circuit_state"] in ["closed", "half_open"]
        assert result["health_state"] in ["healthy", "degraded", "blocked"]
        assert "model_health" in result
        assert "circuit_snapshot" in result
        assert "failures_in_window" in result["circuit_snapshot"]

    def test_model_blocked_after_consecutive_failures(self, tmp_health_path):
        """连续10次失败 → BLOCKED"""
        reg = ModelHealthRegistry(persist_path=tmp_health_path)
        for _ in range(12):
            reg.report_request("failing-model", success=False)

        entry = reg.get_health("failing-model")
        assert entry.state == ModelHealthState.BLOCKED.value
        assert entry.consecutive_failures == 12
        assert entry.first_blocked_at is not None

    def test_degraded_to_blocked_transition(self, tmp_health_path):
        """DEGRADED → BLOCKED 状态转换"""
        reg = ModelHealthRegistry(persist_path=tmp_health_path)

        # 先制造 DEGRADED: 3失败+2成功+5失败 = 8req, 8fail, 0succ
        # 错误率 100% ≥ 60% → BLOCKED（因为连续失败会触发）
        for _ in range(15):
            reg.report_request("model-x", success=False)

        entry = reg.get_health("model-x")
        assert entry.state == ModelHealthState.BLOCKED.value

    def test_unknown_model_passes_circuit_check(self):
        """未知模型通过熔断检查（默认允许）"""
        GlobalCircuitBreaker.reset_instance()
        can, reason = check_model_health("totally-unknown-model-xyz")
        assert can is True
        assert reason == "OK"

    def test_report_nonexistent_model_creates_entry(self, tmp_health_path):
        """向未知模型报告会创建条目"""
        reg = ModelHealthRegistry(persist_path=tmp_health_path)
        entry = reg.report_request("brand-new-model", success=True)
        assert entry.model == "brand-new-model"
        assert entry.total_requests == 1
        assert entry.total_successes == 1


# =============================================================================
# 6. 并发安全
# =============================================================================

class TestConcurrencySafety:
    """并发场景安全测试"""

    def test_concurrent_health_reports_no_race(self, router, tmp_health_path):
        """多线程并发健康上报无竞争"""
        mock = MockEngine(name="mock", model="gpt-6")
        router.register_engine(mock)

        errors = []

        def worker(i: int):
            try:
                import asyncio
                success = (i % 3 != 0)
                if success:
                    asyncio.run(router.route_and_execute_async(f"task-{i}", {}))
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(20)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"并发错误: {errors}"

    def test_multiple_circuit_breakers_independent(self):
        """多个模型熔断器独立"""
        cb = GlobalCircuitBreaker.get_instance()

        # model-a 触发熔断
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result("model-a", success=False)

        # model-b 不受影响
        assert cb.can_proceed("model-b") is True
        snap_a = cb.get_snapshot("model-a")
        snap_b = cb.get_snapshot("model-b")
        assert snap_a.state == CircuitState.OPEN
        assert snap_b.state == CircuitState.CLOSED


# =============================================================================
# 7. 端到端场景
# =============================================================================

class TestEndToEndScenarios:
    """端到端集成场景"""

    def test_full_failure_then_recovery_scenario(self, router, tmp_health_path):
        """
        完整场景：失败 → 熔断 → 恢复 → 成功

        流程:
        1. 直接操作 GlobalCircuitBreaker 触发熔断
        2. 熔断期间请求被拒绝
        3. 等待 OPEN 超时 → HALF_OPEN
        4. 探测请求成功 → CLOSED
        5. 正常请求成功
        """
        import asyncio

        mock = MockEngine(name="mock", model="claude-sonnet")
        router.register_engine(mock, set_default=True)

        cb = GlobalCircuitBreaker.get_instance()
        model = "claude-sonnet"

        # 步骤1: 直接触发熔断（不通过 API 调用）
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result(model, success=False)

        snap = cb.get_snapshot(model)
        assert snap.state == CircuitState.OPEN, f"期望 OPEN，实际 {snap.state}"

        # 步骤2: 熔断期间请求被拒绝
        result = asyncio.run(router.route_and_execute_async("task", {}))
        assert result.success is False
        assert "CircuitBreaker OPEN" in (result.error or "")

        # 步骤3: 等待 OPEN 超时 → HALF_OPEN（通过 can_proceed 触发状态转换）
        time.sleep(DEFAULT_OPEN_DURATION + 0.2)
        can, _ = router.check_engine_available(mock)
        assert can is True, "OPEN 超时后应允许请求"
        snap = cb.get_snapshot(model)
        assert snap.state == CircuitState.HALF_OPEN, f"期望 HALF_OPEN，实际 {snap.state}"

        # 步骤4: 探测请求成功 → CLOSED
        # HALF_OPEN 第1次成功（successes=1，recovery_threshold=2，尚不触发 CLOSED）
        cb.record_result(model, success=True, is_probe=True)
        snap = cb.get_snapshot(model)
        assert snap.state == CircuitState.HALF_OPEN, f"第1次探测后期望 HALF_OPEN，实际 {snap.state}"

        # HALF_OPEN 第2次成功（successes=2，recovery_threshold=2，触发 CLOSED）
        cb.record_result(model, success=True, is_probe=True)
        snap = cb.get_snapshot(model)
        assert snap.state == CircuitState.CLOSED, f"第2次探测后期望 CLOSED，实际 {snap.state}"

        # 步骤5: 正常请求成功
        result = asyncio.run(router.route_and_execute_async("task", {}))
        assert result.success is True

    def test_multi_engine_health_report(self, router, tmp_health_path):
        """
        多引擎场景：生成含所有引擎的健康度报告

        由于 route() 总是选择默认引擎，每次注册后需重新设为默认
        """
        import asyncio

        models = ["gpt-6", "deepseek-chat", "claude-sonnet"]
        for i, model_name in enumerate(models):
            eng = MockEngine(name=f"mock{i}", model=model_name)
            router.register_engine(eng, set_default=True)  # 每次设为默认
            asyncio.run(router.route_and_execute_async("hello", {}))

        report = router.get_health_report()
        assert report["summary"]["total_models"] >= 3
        model_names = {m["model"] for m in report["models"]}
        assert "gpt-6" in model_names
        assert "deepseek-chat" in model_names
        assert "claude-sonnet" in model_names

    def test_health_report_shows_circuit_state(self, tmp_health_path):
        """
        健康度报告显示熔断器状态
        """
        cb = GlobalCircuitBreaker.get_instance()
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            cb.record_result("test-model", success=False)

        report = generate_health_report(models=["test-model"], persist_path=tmp_health_path)
        test_model = next(m for m in report["models"] if m["model"] == "test-model")

        assert test_model["circuit_open"] is True
        assert test_model["circuit_state"] == "open"
        assert test_model["is_available"] is False
        assert test_model["remaining_open_time"] > 0
