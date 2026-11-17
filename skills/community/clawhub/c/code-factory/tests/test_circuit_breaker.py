"""
熔断器单元测试
"""

import pytest
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from middlewares.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    CircuitBreakerOpenError,
    GlobalTimeoutError,
)


class TestCircuitBreakerConfig:
    """熔断器配置测试"""

    def test_default_config(self):
        config = CircuitBreakerConfig()
        assert config.global_timeout_seconds == 600
        assert config.step_timeout_seconds == 120
        assert config.failure_threshold == 3

    def test_custom_config(self):
        config = CircuitBreakerConfig(
            global_timeout_seconds=300,
            step_timeout_seconds=60,
            failure_threshold=5,
        )
        assert config.global_timeout_seconds == 300
        assert config.failure_threshold == 5


class TestCircuitBreaker:
    """熔断器功能测试"""

    def setup_method(self):
        """每个测试前重置单例"""
        CircuitBreaker.reset_instance()

    def teardown_method(self):
        """每个测试后重置单例"""
        CircuitBreaker.reset_instance()

    def test_singleton_pattern(self):
        """真单例模式"""
        cb1 = CircuitBreaker.get_instance()
        cb2 = CircuitBreaker.get_instance()
        assert cb1 is cb2

    def test_initial_state_closed(self):
        """初始状态为 CLOSED"""
        cb = CircuitBreaker.get_instance()
        assert cb.state == CircuitState.CLOSED
        assert cb.allow_request()

    def test_record_failure_increments(self):
        """记录失败增加计数"""
        cb = CircuitBreaker.get_instance()
        cb.record_failure()
        cb.record_failure()
        assert cb._consecutive_failures == 2

    def test_opens_after_threshold(self):
        """连续失败超过阈值后熔断打开"""
        cb = CircuitBreaker.get_instance(
            CircuitBreakerConfig(failure_threshold=2)
        )
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        assert not cb.allow_request()

    def test_record_success_resets(self):
        """记录成功重置熔断"""
        cb = CircuitBreaker.get_instance()
        cb.record_failure()
        cb.record_failure()
        cb.record_success()
        assert cb._consecutive_failures == 0
        assert cb.state == CircuitState.CLOSED

    def test_execute_protected_success(self):
        """带保护执行：成功情况"""
        cb = CircuitBreaker.get_instance()
        result = cb.execute_protected(lambda: 42)
        assert result == 42

    def test_execute_protected_raises(self):
        """带保护执行：异常传播"""
        cb = CircuitBreaker.get_instance()

        def failing():
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            cb.execute_protected(failing)

    def test_execute_protected_circuit_open(self):
        """熔断打开时拒绝执行"""
        cb = CircuitBreaker.get_instance(
            CircuitBreakerConfig(failure_threshold=1)
        )
        cb.record_failure()  # 打开熔断

        with pytest.raises(CircuitBreakerOpenError):
            cb.execute_protected(lambda: 42)

    def test_execute_with_timeout_normal(self):
        """正常执行不超时"""
        cb = CircuitBreaker.get_instance()
        result = cb.execute_with_timeout(
            lambda: "done",
            timeout_seconds=5,
            on_timeout="timeout",
        )
        assert result == "done"

    def test_execute_with_timeout_exceeded(self):
        """执行超时返回 on_timeout"""
        cb = CircuitBreaker.get_instance()

        def slow():
            time.sleep(10)
            return "too late"

        result = cb.execute_with_timeout(
            slow,
            timeout_seconds=0.1,
            on_timeout="timeout",
        )
        assert result == "timeout"

    def test_global_timer(self):
        """全局超时计时器"""
        cb = CircuitBreaker.get_instance(
            CircuitBreakerConfig(global_timeout_seconds=0.01)
        )
        cb.start_global_timer()
        time.sleep(0.02)
        assert cb.is_global_timeout()

    def test_global_timer_not_started(self):
        """未启动计时器时不超时"""
        cb = CircuitBreaker.get_instance()
        assert not cb.is_global_timeout()

    def test_remaining_seconds(self):
        """剩余时间计算"""
        cb = CircuitBreaker.get_instance(
            CircuitBreakerConfig(global_timeout_seconds=600)
        )
        cb.start_global_timer()
        remaining = cb.remaining_global_seconds()
        assert remaining > 0
        assert remaining <= 600

    def test_half_open_allows_probe(self):
        """半开状态允许探测请求"""
        cb = CircuitBreaker.get_instance(
            CircuitBreakerConfig(
                failure_threshold=1,
                recovery_timeout_seconds=0,  # 立即进入半开
            )
        )
        cb.record_failure()  # → OPEN
        # 由于 recovery_timeout=0，下一次 allow_request 会进入 HALF_OPEN
        assert cb.allow_request()  # HALF_OPEN 允许探测
        assert cb.state == CircuitState.HALF_OPEN

    def test_reset_instance(self):
        """重置单例"""
        cb1 = CircuitBreaker.get_instance()
        CircuitBreaker.reset_instance()
        cb2 = CircuitBreaker.get_instance()
        assert cb1 is not cb2

    def test_execute_protected_global_timeout(self):
        """全局超时时拒绝执行"""
        cb = CircuitBreaker.get_instance(
            CircuitBreakerConfig(global_timeout_seconds=0.01)
        )
        cb.start_global_timer()
        time.sleep(0.02)

        with pytest.raises(GlobalTimeoutError):
            cb.execute_protected(lambda: 42)
