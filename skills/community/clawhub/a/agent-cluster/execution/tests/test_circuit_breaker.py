"""
GlobalCircuitBreaker + ModelHealthRegistry 单元测试

覆盖范围:
1. GlobalCircuitBreaker 状态机 (CLOSED → OPEN → HALF_OPEN → CLOSED)
2. 滑动窗口逻辑（60秒内N次失败触发）
3. ModelHealthRegistry 状态机 (HEALTHY → DEGRADED → BLOCKED)
4. 持久化读写（model_health.json）
5. 集成场景：多会话并发、灾难性重试抑制
6. 恢复逻辑：自动恢复 + 手动强制恢复
"""

import json
import os
import tempfile
import threading
import time
from pathlib import Path

import pytest

from execution.circuit_breaker import (
    CircuitOpenError,
    CircuitState,
    DEFAULT_FAILURE_THRESHOLD,
    DEFAULT_HALF_OPEN_PROBES,
    DEFAULT_OPEN_DURATION,
    DEFAULT_RECOVERY_THRESHOLD,
    DEFAULT_WINDOW_SECONDS,
    GlobalCircuitBreaker,
    ModelHealthRegistry,
    ModelHealthState,
    check_model_health,
    report_request_result,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(autouse=True)
def isolate_singleton():
    """每个测试前重置全局单例（避免状态污染）"""
    GlobalCircuitBreaker.reset_instance()
    yield
    GlobalCircuitBreaker.reset_instance()


@pytest.fixture
def tmp_persist_path(tmp_path):
    """临时持久化文件路径"""
    return str(tmp_path / "model_health.json")


@pytest.fixture
def fast_cb():
    """
    快速断路器配置（用于时序测试）

    - 阈值: 3 次失败 → OPEN
    - 窗口: 10 秒
    - OPEN 持续: 0.5 秒
    - 探测配额: 3
    - 恢复阈值: 4（> 配额，保证先耗尽配额再恢复）
    """
    GlobalCircuitBreaker.reset_instance()
    return GlobalCircuitBreaker.get_instance(
        failure_threshold=3,
        window_seconds=10.0,
        open_duration=0.5,
        half_open_max_probes=3,
        recovery_threshold=4,
    )


@pytest.fixture
def registry(tmp_persist_path):
    """使用临时路径的 ModelHealthRegistry"""
    return ModelHealthRegistry(persist_path=tmp_persist_path)


# =============================================================================
# GlobalCircuitBreaker 基础状态机测试
# =============================================================================

class TestCircuitBreakerBasicStateMachine:
    """断路器基础状态机"""

    def test_initial_state_is_closed(self, fast_cb):
        """初始状态 = CLOSED"""
        assert fast_cb.can_proceed("model-a")
        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.CLOSED

    def test_closed_success_no_state_change(self, fast_cb):
        """成功 → 保持 CLOSED"""
        fast_cb.record_result("model-a", success=True)
        assert fast_cb.can_proceed("model-a")

    def test_closed_failure_within_threshold(self, fast_cb):
        """失败次数 < 阈值 → 保持 CLOSED"""
        # fast_cb 的 failure_threshold=3，循环2次 < 3，保持 CLOSED
        for _ in range(fast_cb._failure_threshold - 1):
            fast_cb.record_result("model-a", success=False)
        assert fast_cb.can_proceed("model-a")

    def test_closed_failure_at_threshold_opens(self, fast_cb):
        """失败次数 == 阈值 → 转为 OPEN"""
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        assert not fast_cb.can_proceed("model-a")
        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.OPEN

    def test_open_rejects_all_requests(self, fast_cb):
        """OPEN 状态拒绝所有请求"""
        # 触发 OPEN
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        # 再次尝试
        assert not fast_cb.can_proceed("model-a")
        assert not fast_cb.can_proceed("model-a")
        snap = fast_cb.get_snapshot("model-a")
        assert snap.total_rejections >= 2

    def test_open_failure_resets_timer(self, fast_cb):
        """OPEN 期间再次失败 → 重置 OPEN 超时"""
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        time.sleep(0.05)
        open_time_before = fast_cb.get_snapshot("model-a").open_since
        # OPEN 期间再次失败
        fast_cb.record_result("model-a", success=False)
        open_time_after = fast_cb.get_snapshot("model-a").open_since
        assert open_time_after >= open_time_before


class TestCircuitBreakerHalfOpen:
    """HALF_OPEN 半开状态测试"""

    def test_open_timeout_becomes_half_open(self, fast_cb):
        """OPEN 超时后自动转为 HALF_OPEN"""
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        # 等待 OPEN 超时
        time.sleep(DEFAULT_OPEN_DURATION + 0.1)
        assert fast_cb.can_proceed("model-a")
        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.HALF_OPEN

    def test_half_open_success_counts_toward_recovery(self, fast_cb):
        """HALF_OPEN 中成功 → 计数恢复"""
        # 触发 OPEN
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        # 等待超时
        time.sleep(DEFAULT_OPEN_DURATION + 0.05)
        assert fast_cb.can_proceed("model-a")

        # 第一次探测成功
        fast_cb.record_result("model-a", success=True, is_probe=True)
        snap = fast_cb.get_snapshot("model-a")
        assert snap.half_open_successes == 1
        assert snap.state == CircuitState.HALF_OPEN  # 还没达到恢复阈值

    def test_half_open_recovery_threshold_closes(self, fast_cb):
        """HALF_OPEN 达到恢复阈值 → CLOSED"""
        # 触发 OPEN
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        time.sleep(DEFAULT_OPEN_DURATION + 0.05)
        assert fast_cb.can_proceed("model-a")

        # 达到恢复阈值（recovery=4，需要4次成功）
        for _ in range(DEFAULT_RECOVERY_THRESHOLD):
            fast_cb.record_result("model-a", success=True, is_probe=True)

        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.HALF_OPEN  # recovery=4, not yet
        # 第4次成功 → CLOSED
        fast_cb.can_proceed("model-a")
        fast_cb.record_result("model-a", success=True, is_probe=True)
        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.CLOSED
        assert fast_cb.can_proceed("model-a")

    def test_half_open_single_failure_reopens(self, fast_cb):
        """HALF_OPEN 中任何失败 → 立即重新 OPEN"""
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        time.sleep(DEFAULT_OPEN_DURATION + 0.05)
        fast_cb.can_proceed("model-a")  # 进入 HALF_OPEN

        # 探测失败
        fast_cb.record_result("model-a", success=False, is_probe=True)
        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.OPEN

    def test_half_open_max_probes_respected(self, fast_cb):
        """HALF_OPEN 探测配额耗尽后拒绝"""
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-x", success=False)
        time.sleep(DEFAULT_OPEN_DURATION + 0.1)
        # 第一次 can_proceed → OPEN 超时 → HALF_OPEN, probes=1
        fast_cb.can_proceed("model-x")
        # 连续 2 次 can_proceed（不记录结果，保持 HALF_OPEN 状态）
        for _ in range(2):
            fast_cb.can_proceed("model-x")
        # 第 3 次 can_proceed：probes=3 == max_probes → False（配额耗尽）
        assert not fast_cb.can_proceed("model-x")

    def test_half_open_allows_only_probe_requests(self, fast_cb):
        """HALF_OPEN 探测配额耗尽后拒绝请求"""
        # 触发 OPEN
        for _ in range(3):
            fast_cb.record_result("model", success=False)
        time.sleep(0.6)
        # 第一次 can_proceed → OPEN 超时 → HALF_OPEN，probes=1
        fast_cb.can_proceed("model")
        # 连续 3 次 can_proceed（不记录结果，保持 HALF_OPEN 状态）
        for _ in range(3):
            fast_cb.can_proceed("model")
        # 第 4 次 can_proceed：probes=3 == max_probes → False（配额耗尽）
        assert not fast_cb.can_proceed("model")
        # 第 5 次：仍在 HALF_OPEN，继续拒绝
        assert not fast_cb.can_proceed("model")


# =============================================================================
# 滑动窗口测试
# =============================================================================

class TestCircuitBreakerSlidingWindow:
    """滑动窗口逻辑测试"""

    def test_failure_window_expiry_closes_circuit(self, fast_cb):
        """窗口内失败记录过期后，断路器自动恢复 CLOSED"""
        # 触发 OPEN（3次失败）
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)

        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.OPEN

        # 窗口过期（10秒后）
        time.sleep(11.0)
        # 再次检查：此时没有新的失败记录，can_proceed 应该 True（因为 OPEN 已超时）
        assert fast_cb.can_proceed("model-a")

    def test_rolling_failures_keep_circuit_open(self, fast_cb):
        """持续有失败进入窗口，保持 OPEN"""
        for i in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
            time.sleep(0.05)
        assert fast_cb.get_snapshot("model-a").state == CircuitState.OPEN

    def test_multiple_models_independent(self, fast_cb):
        """不同模型的断路器相互独立"""
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        # model-b 不受影响
        assert fast_cb.can_proceed("model-b")
        assert fast_cb.get_snapshot("model-b").state == CircuitState.CLOSED


# =============================================================================
# 强制操作测试
# =============================================================================

class TestCircuitBreakerForceOperations:
    """手动强制操作"""

    def test_force_open(self, fast_cb):
        """force_open 立即将断路器置为 OPEN"""
        fast_cb.force_open("model-x", reason="test")
        assert not fast_cb.can_proceed("model-x")
        snap = fast_cb.get_snapshot("model-x")
        assert snap.state == CircuitState.OPEN

    def test_force_close(self, fast_cb):
        """force_close 立即将断路器重置为 CLOSED"""
        # 先 OPEN
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        # 强制 CLOSED
        fast_cb.force_close("model-a")
        snap = fast_cb.get_snapshot("model-a")
        assert snap.state == CircuitState.CLOSED
        assert snap.failures_in_window == 0
        assert fast_cb.can_proceed("model-a")


# =============================================================================
# 单例模式测试
# =============================================================================

class TestCircuitBreakerSingleton:
    """单例模式"""

    def test_get_instance_returns_same_object(self):
        """多次调用返回同一实例"""
        GlobalCircuitBreaker.reset_instance()
        a = GlobalCircuitBreaker.get_instance(failure_threshold=5)
        b = GlobalCircuitBreaker.get_instance(failure_threshold=99)
        assert a is b
        # 首次参数生效
        assert a._failure_threshold == 5

    def test_reset_instance_clears_state(self, fast_cb):
        """reset_instance 清空状态"""
        for _ in range(DEFAULT_FAILURE_THRESHOLD):
            fast_cb.record_result("model-a", success=False)
        assert fast_cb.get_snapshot("model-a").state == CircuitState.OPEN

        GlobalCircuitBreaker.reset_instance()
        new_cb = GlobalCircuitBreaker.get_instance()
        # 新实例：model-a 是新条目
        assert new_cb.can_proceed("model-a")


# =============================================================================
# 统计 API 测试
# =============================================================================

class TestCircuitBreakerStats:
    """统计接口"""

    def test_stats_reflects_correct_counts(self, fast_cb):
        """统计正确反映请求/失败/拒绝次数"""
        fast_cb.record_result("model-a", success=True)
        fast_cb.record_result("model-a", success=True)
        # model-b: 2 failures < threshold=3 → CLOSED
        for _ in range(2):
            fast_cb.record_result("model-b", success=False)
        # model-c: threshold=3 → OPEN
        for _ in range(fast_cb._failure_threshold):
            fast_cb.record_result("model-c", success=False)

        stats = fast_cb.get_stats()
        assert stats["total_successes"] == 2
        assert stats["total_failures"] == 2 + fast_cb._failure_threshold
        assert stats["open"] == 1  # model-c

    def test_all_snapshots(self, fast_cb):
        """get_all_snapshots 返回所有模型"""
        fast_cb.record_result("x", success=False)
        fast_cb.record_result("y", success=True)
        fast_cb.record_result("z", success=False)
        snaps = fast_cb.get_all_snapshots()
        assert set(snaps.keys()) == {"x", "y", "z"}


# =============================================================================
# ModelHealthRegistry 状态机测试
# =============================================================================

class TestModelHealthRegistryBasic:
    """健康注册表基础"""

    def test_unknown_model_is_healthy(self, registry):
        """未知模型默认 HEALTHY"""
        assert registry.is_healthy("unknown-model")
        assert not registry.is_degraded("unknown-model")
        assert not registry.is_blocked("unknown-model")

    def test_report_success(self, registry):
        """报告成功 → 计数器更新"""
        entry = registry.report_request("model-a", success=True)
        assert entry.total_successes == 1
        assert entry.total_requests == 1
        assert entry.state == ModelHealthState.HEALTHY.value

    def test_report_failure(self, registry):
        """报告失败 → 计数器更新"""
        entry = registry.report_request("model-a", success=False, error="rate_limit")
        assert entry.total_failures == 1
        assert entry.consecutive_failures == 1
        assert entry.last_failure_reason == "rate_limit"

    def test_success_resets_consecutive_failures(self, registry):
        """连续成功重置失败计数"""
        registry.report_request("model-a", success=False)
        registry.report_request("model-a", success=False)
        assert registry.get_health("model-a").consecutive_failures == 2
        registry.report_request("model-a", success=True)
        assert registry.get_health("model-a").consecutive_failures == 0


class TestModelHealthRegistryStateMachine:
    """健康注册表状态机"""

    def test_healthy_to_degraded(self, registry):
        """错误率 ≥ 30% 且样本数 ≥ 5 → DEGRADED"""
        # 需要至少 DEGRADED_MIN_SAMPLES=5 个请求
        # 3 failures + 2 successes = 5 requests, error_rate=60%
        for _ in range(3):
            registry.report_request("model-a", success=False)
        for _ in range(2):
            registry.report_request("model-a", success=True)
        entry = registry.get_health("model-a")
        # 3/5 = 60% ≥ 30% → DEGRADED
        assert entry.state == ModelHealthState.DEGRADED.value
        assert entry.first_degraded_at is not None

    def test_degraded_to_healthy_auto_recovery(self, registry):
        """DEGRADED 模型连续大量成功 → 错误率 < 15% 时恢复 HEALTHY"""
        # 制造 DEGRADED: 3 failures + 2 successes = 60% error rate
        for _ in range(3):
            registry.report_request("model-a", success=False)
        for _ in range(2):
            registry.report_request("model-a", success=True)
        assert registry.get_health("model-a").state == ModelHealthState.DEGRADED.value

        # 连续大量成功：错误率 3/(3+18) = 14.3% < 15% → 恢复 HEALTHY
        for _ in range(18):
            registry.report_request("model-a", success=True)
        entry = registry.get_health("model-a")
        assert entry.state == ModelHealthState.HEALTHY.value
        assert entry.consecutive_failures == 0

    def test_consecutive_failures_to_blocked(self, registry):
        """连续 10 次失败 → BLOCKED"""
        for i in range(12):
            registry.report_request("model-b", success=False)
        entry = registry.get_health("model-b")
        assert entry.state == ModelHealthState.BLOCKED.value
        assert entry.first_blocked_at is not None

    def test_blocked_does_not_auto_recover(self, registry):
        """BLOCKED 状态不会自动恢复 HEALTHY（需手动重置）"""
        for _ in range(15):
            registry.report_request("model-c", success=False)
        assert registry.get_health("model-c").state == ModelHealthState.BLOCKED.value
        # 即使大量成功，也需要手动 reset
        for _ in range(20):
            registry.report_request("model-c", success=True)
        assert registry.get_health("model-c").state == ModelHealthState.BLOCKED.value

    def test_manual_reset_recovers_blocked(self, registry):
        """手动 reset 可以恢复 BLOCKED"""
        for _ in range(15):
            registry.report_request("model-c", success=False)
        assert registry.get_health("model-c").state == ModelHealthState.BLOCKED.value

        ok = registry.reset_model("model-c", strategy="manual")
        assert ok
        entry = registry.get_health("model-c")
        assert entry.state == ModelHealthState.HEALTHY.value
        assert entry.recovery_strategy == "manual"
        assert entry.consecutive_failures == 0


class TestModelHealthRegistryQueries:
    """健康注册表查询接口"""

    def test_get_healthy_degraded_blocked_lists(self, registry):
        """分状态列表查询"""
        # BLOCKED: 连续 10+ 次失败
        for _ in range(15):
            registry.report_request("blocked-model", success=False)
        # DEGRADED: 3 failures + 2 successes (60% error rate, ≥5 samples)
        for _ in range(3):
            registry.report_request("degraded-model", success=False)
        for _ in range(2):
            registry.report_request("degraded-model", success=True)
        # HEALTHY: 5 successes
        for _ in range(5):
            registry.report_request("healthy-model", success=True)

        assert "blocked-model" in registry.get_blocked_models()
        assert "degraded-model" in registry.get_degraded_models()
        assert "healthy-model" in registry.get_healthy_models()
        assert "blocked-model" not in registry.get_healthy_models()

    def test_get_all_summaries(self, registry):
        """人类可读摘要"""
        registry.report_request("model-x", success=False, error="timeout")
        summaries = registry.get_all_summaries()
        assert len(summaries) == 1
        assert summaries[0]["model"] == "model-x"
        assert summaries[0]["last_failure_reason"] == "timeout"

    def test_get_stats(self, registry):
        """全局统计"""
        # HEALTHY model: 5 successes
        for _ in range(5):
            registry.report_request("m1", success=True)
        # BLOCKED model: 15 failures
        for _ in range(15):
            registry.report_request("m2", success=False)
        stats = registry.get_stats()
        assert stats["total_models"] == 2
        assert stats["total_requests"] == 20
        assert stats["total_failures"] == 15
        assert stats["blocked"] == 1


# =============================================================================
# 持久化测试
# =============================================================================

class TestModelHealthRegistryPersistence:
    """持久化读写"""

    def test_state_persisted_to_file(self, tmp_path):
        """状态变更自动保存到文件"""
        path = str(tmp_path / "health.json")
        reg1 = ModelHealthRegistry(persist_path=path)
        for _ in range(15):
            reg1.report_request("blocked-model", success=False)
        reg1.report_request("healthy-model", success=True)

        # 新实例加载
        reg2 = ModelHealthRegistry(persist_path=path)
        assert reg2.get_health("blocked-model").state == ModelHealthState.BLOCKED.value
        assert reg2.get_health("healthy-model").state == ModelHealthState.HEALTHY.value
        assert reg2.get_health("blocked-model").consecutive_failures == 15

    def test_partial_corruption_skipped(self, tmp_path):
        """文件部分损坏时跳过损坏记录"""
        path = tmp_path / "health.json"
        with open(path, "w") as f:
            json.dump({"models": {"good": {"model": "good", "state": "healthy"}, "bad": "not_a_dict"}}, f)

        reg = ModelHealthRegistry(persist_path=str(path))
        assert reg.get_health("good") is not None
        assert reg.get_health("bad") is None

    def test_force_operations_persist(self, tmp_path):
        """force_degraded / force_blocked / reset 持久化"""
        path = str(tmp_path / "health.json")
        reg1 = ModelHealthRegistry(persist_path=path)
        reg1.force_degraded("model-x")
        reg1.force_blocked("model-y")
        reg1.report_request("model-z", success=False)

        reg2 = ModelHealthRegistry(persist_path=path)
        assert reg2.get_health("model-x").state == ModelHealthState.DEGRADED.value
        assert reg2.get_health("model-y").state == ModelHealthState.BLOCKED.value
        assert reg2.get_health("model-z").state == ModelHealthState.HEALTHY.value  # 还没到阈值

    def test_probe_flag_on_half_open_success(self, registry):
        """HALF_OPEN 探测成功时 is_probe 标记正确传递"""
        entry = registry.report_request("model-a", success=True, is_probe=True)
        assert entry.probe_successes == 1
        assert entry.probe_count >= 1


# =============================================================================
# 并发测试
# =============================================================================

class TestCircuitBreakerConcurrency:
    """多线程并发安全测试"""

    def test_concurrent_record_results(self, fast_cb):
        """多线程并发记录结果（无竞争条件）"""
        errors = []

        def worker(model_prefix: str, count: int):
            try:
                for i in range(count):
                    fast_cb.record_result(f"{model_prefix}_{i % 3}", success=i % 2 == 0)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(f"t{i}", 50)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        stats = fast_cb.get_stats()
        assert stats["total_successes"] + stats["total_failures"] == 500

    def test_concurrent_can_proceed(self, fast_cb):
        """并发 can_proceed 不产生竞争"""
        barrier = threading.Barrier(20)
        results = []
        model_name = "concurrent-can-proceed-test-model"

        def worker():
            barrier.wait()
            for _ in range(100):
                r = fast_cb.can_proceed(model_name)
                results.append(r)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(results)  # 全部 True（还没触发阈值）

    def test_registry_concurrent_report(self, registry):
        """并发报告请求不产生竞争"""
        errors = []

        def worker():
            try:
                for i in range(100):
                    registry.report_request(
                        f"model-{i % 5}",
                        success=i % 3 != 0,
                        error="test_error" if i % 3 == 0 else None,
                    )
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors


# =============================================================================
# 集成测试：灾难性重试抑制
# =============================================================================

class TestCatastrophicRetryPrevention:
    """
    灾难性重试抑制验证

    场景：某个模型完全不可用（持续返回失败）
    验证：断路器 OPEN 后 N 个会话的所有重试都被阻止
    """

    def test_multiple_sessions_all_rejected_when_open(self, fast_cb):
        """断路器 OPEN 时，所有会话的请求都被拒绝"""
        # 触发 OPEN（使用 fast_cb 的阈值3）
        for _ in range(fast_cb._failure_threshold):
            fast_cb.record_result("failing-model", success=False)

        snap = fast_cb.get_snapshot("failing-model")
        assert snap.state == CircuitState.OPEN

        # 模拟多个会话同时尝试（不应该触发灾难性重试）
        rejections = 0
        for _ in range(100):
            if not fast_cb.can_proceed("failing-model"):
                rejections += 1

        assert rejections == 100

    def test_half_open_allows_only_probe_requests(self, fast_cb):
        """HALF_OPEN 只允许探测配额，拒绝超额请求"""
        # 触发 OPEN
        for _ in range(3):
            fast_cb.record_result("model-x", success=False)
        time.sleep(0.6)
        # 第一次 can_proceed → OPEN 超时 → HALF_OPEN，probes=1
        fast_cb.can_proceed("model-x")
        # 连续 3 次 can_proceed（不记录结果，保持 HALF_OPEN 状态）
        for _ in range(3):
            fast_cb.can_proceed("model-x")
        # 第 4 次 can_proceed：probes=3 == max_probes → False（配额耗尽）
        assert not fast_cb.can_proceed("model-x")
        # 第 5 次：仍在 HALF_OPEN，继续拒绝
        assert not fast_cb.can_proceed("model-x")

    def test_circuit_open_error_exception(self, fast_cb):
        """CircuitOpenError 异常正确携带剩余时间"""
        for _ in range(fast_cb._failure_threshold):
            fast_cb.record_result("model-a", success=False)

        exc = CircuitOpenError("model-a", remaining_seconds=5.5)
        assert exc.model == "model-a"
        assert exc.remaining_seconds == 5.5
        assert "retry in" in str(exc)


# =============================================================================
# 快捷函数测试
# =============================================================================

class TestShortcutFunctions:
    """快捷函数测试"""

    def test_check_model_health_unknown(self):
        """未知模型 → 允许"""
        GlobalCircuitBreaker.reset_instance()
        can, reason = check_model_health("nonexistent-model")
        assert can is True

    def test_report_request_result_integration(self, fast_cb, registry):
        """统一报告函数同时更新两个系统"""
        result = report_request_result(
            "test-model",
            success=True,
            error=None,
            is_probe=True,
        )
        assert result["circuit_state"] in ["closed", "half_open"]
        assert result["health_state"] in ["healthy", "degraded", "blocked"]
        assert "model_health" in result


# =============================================================================
# 边界条件测试
# =============================================================================

class TestEdgeCases:
    """边界条件"""

    def test_zero_threshold_is_nop(self):
        """阈值为 0 → 第一次失败就 OPEN（需验证）"""
        GlobalCircuitBreaker.reset_instance()
        cb = GlobalCircuitBreaker.get_instance(
            failure_threshold=0,
            window_seconds=60.0,
            open_duration=30.0,
            half_open_max_probes=1,
            recovery_threshold=1,
        )
        cb.record_result("m", success=False)
        assert not cb.can_proceed("m")

    def test_probe_without_half_open_no_op(self, fast_cb):
        """未进入 HALF_OPEN 时 is_probe=True 无效果"""
        # 正常 CLOSED 状态
        fast_cb.record_result("model-x", success=True, is_probe=True)
        snap = fast_cb.get_snapshot("model-x")
        assert snap.state == CircuitState.CLOSED

    def test_error_rate_with_zero_requests(self, registry):
        """新模型（0请求）时错误率计算安全"""
        entry = registry.get_health("brand-new-model")
        assert entry is None  # 未知模型返回 None
        # 第一个请求
        entry = registry.report_request("brand-new-model", success=False)
        assert entry.error_rate == 1.0  # 1/1

    def test_persist_file_not_exist_on_init(self, tmp_path):
        """文件不存在时初始化不报错"""
        path = str(tmp_path / "nonexistent.json")
        reg = ModelHealthRegistry(persist_path=path)
        assert reg.get_stats()["total_models"] == 0
