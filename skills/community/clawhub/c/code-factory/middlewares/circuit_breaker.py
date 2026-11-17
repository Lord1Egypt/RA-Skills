"""
全局熔断器 —— 防止单个调用拖垮整个技能执行。

规则：
- 全局超时：整个编排流程不得超过 global_timeout 秒
- 单步骤超时：每个步骤不得超过 step_timeout 秒
- 连续失败熔断：连续 N 次步骤失败后，熔断并停止后续步骤
"""

import time
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Any, Optional


class CircuitState(str, Enum):
    CLOSED = "closed"       # 正常通行
    OPEN = "open"           # 熔断打开，拒绝所有请求
    HALF_OPEN = "half_open" # 半开，允许探测请求


@dataclass
class CircuitBreakerConfig:
    """熔断器配置"""
    global_timeout_seconds: int = 600      # 全局超时
    step_timeout_seconds: int = 120        # 单步骤超时
    failure_threshold: int = 3             # 连续失败 N 次后熔断
    recovery_timeout_seconds: int = 30     # 熔断后等待 N 秒进入半开


class CircuitBreaker:
    """全局熔断器，真单例模式"""

    _instance: Optional["CircuitBreaker"] = None
    _instance_lock = threading.Lock()

    def __new__(cls, config: Optional[CircuitBreakerConfig] = None):
        """确保全局只有一个 CircuitBreaker 实例"""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instance = instance
        return cls._instance

    def __init__(self, config: Optional[CircuitBreakerConfig] = None):
        if getattr(self, "_initialized", False):
            return
        self.config = config or CircuitBreakerConfig()
        self.state: CircuitState = CircuitState.CLOSED
        self._consecutive_failures: int = 0
        self._last_failure_time: float = 0.0
        self._global_start_time: float = 0.0
        self._lock = threading.Lock()
        self._initialized = True

    @classmethod
    def get_instance(cls, config: Optional[CircuitBreakerConfig] = None) -> "CircuitBreaker":
        """获取全局单例实例"""
        return cls(config)

    @classmethod
    def reset_instance(cls) -> None:
        """重置单例（主要用于测试）"""
        with cls._instance_lock:
            cls._instance = None

    # ── 全局超时 ──────────────────────────────────

    def start_global_timer(self) -> None:
        """启动全局计时器"""
        self._global_start_time = time.monotonic()

    def reset_global_timer(self) -> None:
        """
        重置全局计时器，每次 run() 前调用。

        防止连续 run() 调用间计时器状态污染：
        第二次 run() 的全局超时判断会基于第一次的 _global_start_time。
        """
        self._global_start_time = 0.0

    def is_global_timeout(self) -> bool:
        """检查是否已超出全局超时"""
        if self._global_start_time == 0:
            return False
        elapsed = time.monotonic() - self._global_start_time
        return elapsed > self.config.global_timeout_seconds

    def remaining_global_seconds(self) -> float:
        """剩余全局时间"""
        if self._global_start_time == 0:
            return float(self.config.global_timeout_seconds)
        elapsed = time.monotonic() - self._global_start_time
        return max(0.0, self.config.global_timeout_seconds - elapsed)

    # ── 熔断逻辑 ──────────────────────────────────

    def allow_request(self) -> bool:
        """判断当前是否允许执行请求"""
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True
            if self.state == CircuitState.OPEN:
                if time.monotonic() - self._last_failure_time > self.config.recovery_timeout_seconds:
                    self.state = CircuitState.HALF_OPEN
                    return True
                return False
            # HALF_OPEN: 仅允许一个探测请求，之后转为 OPEN 等待下次恢复窗口
            self.state = CircuitState.OPEN
            return True

    def record_success(self) -> None:
        """记录成功，重置熔断"""
        with self._lock:
            self._consecutive_failures = 0
            self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        """记录失败，可能触发熔断"""
        with self._lock:
            self._consecutive_failures += 1
            self._last_failure_time = time.monotonic()
            if self._consecutive_failures >= self.config.failure_threshold:
                self.state = CircuitState.OPEN

    # ── 带保护的执行 ──────────────────────────────

    def execute_with_timeout(
        self,
        func: Callable[[], Any],
        timeout_seconds: Optional[int] = None,
        on_timeout: Any = None,
    ) -> Any:
        """
        在独立线程中执行函数，带超时保护。

        超时时：
        1. 返回 on_timeout
        2. daemon 线程会在主进程退出时由 Python 运行时清理

        注意：Python 无法强制终止线程。超时后线程中的文件操作
        可能仍在后台继续。调用方应确保步骤函数在超时后不会产生
        影响下游步骤的副作用（参见 Orchestrator._commit_step_output 单通道设计）。
        """
        timeout = timeout_seconds or self.config.step_timeout_seconds
        result: dict = {"value": None, "error": None, "timed_out": False}

        def _target():
            try:
                result["value"] = func()
            except Exception as e:
                result["error"] = e

        thread = threading.Thread(target=_target, daemon=True)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            result["timed_out"] = True
            # daemon 线程：超时返回，线程由 Python 运行时在进程退出时清理
            return on_timeout

        if result["error"] is not None:
            raise result["error"]

        return result["value"]

    def execute_protected(
        self,
        func: Callable[[], Any],
        timeout_seconds: Optional[int] = None,
    ) -> Any:
        """
        带熔断+超时双重保护的执行。
        1. 先检查熔断状态
        2. 再检查全局超时
        3. 带步骤超时执行
        """
        if not self.allow_request():
            raise CircuitBreakerOpenError(
                f"熔断器已打开，连续失败 {self._consecutive_failures} 次"
            )

        if self.is_global_timeout():
            raise GlobalTimeoutError(
                f"全局超时 ({self.config.global_timeout_seconds}s)"
            )

        return self.execute_with_timeout(func, timeout_seconds)


class CircuitBreakerOpenError(Exception):
    """熔断器已打开"""


class GlobalTimeoutError(Exception):
    """全局超时"""


class StepTimeoutError(Exception):
    """单步骤超时"""
