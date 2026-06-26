"""
GlobalCircuitBreaker + ModelHealthRegistry

OpenClaw v4.0 Phase 2 - 模型解耦架构

模块职责:
    GlobalCircuitBreaker  : 跨会话断路器，全局单例
        - 60秒滑动窗口内 N 次失败触发 OPEN 状态
        - OPEN 状态拒绝所有请求，进入 HALF_OPEN 探测
        - 探测成功恢复 CLOSED，避免灾难性重试

    ModelHealthRegistry   : 持久化模型健康状态机
        - 状态: HEALTHY → DEGRADED → BLOCKED
        - 持久化到 model_health.json
        - 支持半开探测自动恢复
        - 记录失败原因、时间戳、恢复策略

Change Log:
    - 2026-04-14: Phase 2 初始实现
"""

from __future__ import annotations

import json
import logging
import threading
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# 常量配置
# =============================================================================

# 全局断路器默认值
DEFAULT_FAILURE_THRESHOLD = 5        # 60秒内超过此数量失败 → OPEN
DEFAULT_WINDOW_SECONDS = 60.0        # 滑动窗口秒数
DEFAULT_OPEN_DURATION = 30.0          # OPEN 状态持续秒数
DEFAULT_HALF_OPEN_PROBES = 3         # HALF_OPEN 允许的探测请求数
DEFAULT_RECOVERY_THRESHOLD = 2       # HALF_OPEN 中成功次数 → CLOSED

# 模型健康状态阈值
DEGRADED_ERROR_RATE = 0.3            # 错误率超过 30% → DEGRADED
BLOCKED_ERROR_RATE = 0.6            # 错误率超过 60% → BLOCKED
BLOCKED_CONSECUTIVE_FAILURES = 10   # 连续失败次数 → BLOCKED
DEGRADED_MIN_SAMPLES = 5             # 最低样本数才开始评估

# 状态文件路径
MODEL_HEALTH_FILE = "model_health.json"


# =============================================================================
# 全局断路器状态枚举
# =============================================================================

class CircuitState(Enum):
    """断路器状态"""
    CLOSED = "closed"       # 正常，允许请求通过
    OPEN = "open"           # 熔断，拒绝所有请求
    HALF_OPEN = "half_open"  # 半开，允许有限探测请求


class CircuitOpenError(Exception):
    """断路器处于 OPEN 状态，拒绝请求"""

    def __init__(self, model: str, remaining_seconds: float = 0.0):
        self.model = model
        self.remaining_seconds = remaining_seconds
        super().__init__(
            f"Circuit breaker OPEN for model '{model}'"
            + (f", retry in {remaining_seconds:.1f}s" if remaining_seconds else "")
        )


# =============================================================================
# ModelHealthRegistry：持久化状态机
# =============================================================================


class ModelHealthState(Enum):
    """模型健康状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BLOCKED = "blocked"


@dataclass
class ModelHealthEntry:
    """
    单个模型的健康记录

    持久化到 JSON 的数据结构
    """
    model: str                         # 模型标识符
    state: str                         # ModelHealthState.value
    consecutive_failures: int = 0      # 连续失败次数
    total_requests: int = 0           # 总请求数
    total_successes: int = 0          # 总成功数
    total_failures: int = 0           # 总失败数
    error_rate: float = 0.0           # 当前错误率 (total_failures/total_requests)
    last_failure_reason: Optional[str] = None
    last_failure_at: Optional[float] = None   # Unix timestamp
    last_success_at: Optional[float] = None
    first_degraded_at: Optional[float] = None
    first_blocked_at: Optional[float] = None
    recovery_strategy: str = "auto"   # auto / manual / retired
    probe_count: int = 0              # 半开探测次数
    probe_successes: int = 0         # 探测成功次数
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelHealthEntry:
        return cls(**d)

    @property
    def health_status(self) -> ModelHealthState:
        return ModelHealthState(self.state)

    def to_summary(self) -> Dict[str, Any]:
        """人类可读摘要（不含敏感信息）"""
        return {
            "model": self.model,
            "state": self.state,
            "error_rate": f"{self.error_rate:.1%}",
            "consecutive_failures": self.consecutive_failures,
            "total_requests": self.total_requests,
            "recovery_strategy": self.recovery_strategy,
            "last_failure_reason": self.last_failure_reason,
        }


class ModelHealthRegistry:
    """
    模型健康状态持久化注册表

    职责:
    1. 持久化状态到 model_health.json（启动加载，变更时保存）
    2. 状态机流转: HEALTHY → DEGRADED → BLOCKED
    3. 支持自动/手动恢复策略
    4. 提供健康检查接口

    使用示例:
        registry = ModelHealthRegistry()

        # 报告请求结果
        registry.report_request("claude-sonnet", success=True)
        registry.report_request("deepseek-chat", success=False, error="rate_limit")

        # 获取模型健康状态
        state = registry.get_health("claude-sonnet")

        # 健康检查（用于 EngineRouter 路由前）
        healthy_models = registry.get_healthy_models()
        blocked_models = registry.get_blocked_models()
    """

    def __init__(
        self,
        persist_path: str = MODEL_HEALTH_FILE,
        degraded_error_rate: float = DEGRADED_ERROR_RATE,
        blocked_error_rate: float = BLOCKED_ERROR_RATE,
        blocked_consecutive: int = BLOCKED_CONSECUTIVE_FAILURES,
        degraded_min_samples: int = DEGRADED_MIN_SAMPLES,
    ):
        """
        初始化注册表

        Args:
            persist_path:  状态文件路径（JSON）
            degraded_error_rate:  进入 DEGRADED 的错误率阈值
            blocked_error_rate:   进入 BLOCKED 的错误率阈值
            blocked_consecutive:   连续失败次数 → BLOCKED
            degraded_min_samples:  计算错误率的最低样本数
        """
        self._persist_path = Path(persist_path)
        self._entries: Dict[str, ModelHealthEntry] = {}
        self._lock = threading.RLock()

        # 配置
        self._degraded_error_rate = degraded_error_rate
        self._blocked_error_rate = blocked_error_rate
        self._blocked_consecutive = blocked_consecutive
        self._degraded_min_samples = degraded_min_samples

        self._load()
        logger.info(
            f"[ModelHealthRegistry] 初始化完成, "
            f"加载 {len(self._entries)} 个模型, persist={persist_path}"
        )

    # -------------------------------------------------------------------------
    # 持久化
    # -------------------------------------------------------------------------

    def _load(self) -> None:
        """从文件加载状态"""
        if not self._persist_path.exists():
            return
        try:
            with open(self._persist_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            models = data.get("models", {}) if isinstance(data, dict) else data
            for model, entry_dict in models.items():
                try:
                    self._entries[model] = ModelHealthEntry.from_dict(entry_dict)
                except Exception:
                    logger.warning(f"[ModelHealthRegistry] 跳过损坏记录: {model}")
            logger.info(f"[ModelHealthRegistry] 从 {self._persist_path} 加载了 {len(self._entries)} 条记录")
        except Exception as e:
            logger.error(f"[ModelHealthRegistry] 加载失败: {e}")

    def _save(self) -> None:
        """保存状态到文件（线程安全，写入临时文件再重命名）"""
        models_data = {
            model: entry.to_dict()
            for model, entry in self._entries.items()
        }
        payload = {
            "version": "1.0",
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "models": models_data,
        }
        try:
            tmp = self._persist_path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            tmp.replace(self._persist_path)
        except Exception as e:
            logger.error(f"[ModelHealthRegistry] 保存失败: {e}")

    # -------------------------------------------------------------------------
    # 状态报告（核心写入）
    # -------------------------------------------------------------------------

    def report_request(
        self,
        model: str,
        success: bool,
        error: Optional[str] = None,
        is_probe: bool = False,
    ) -> ModelHealthEntry:
        """
        报告单个请求结果（线程安全）

        Args:
            model:      模型标识符
            success:    请求是否成功
            error:      错误信息（失败时提供）
            is_probe:   是否为半开探测请求

        Returns:
            ModelHealthEntry: 更新后的条目
        """
        with self._lock:
            now = time.time()
            entry = self._entries.get(model)

            if entry is None:
                entry = ModelHealthEntry(model=model, state=ModelHealthState.HEALTHY.value)
                self._entries[model] = entry

            # 计数器
            entry.total_requests += 1
            entry.updated_at = now

            if success:
                self._on_success(entry, now, is_probe)
            else:
                self._on_failure(entry, error, now, is_probe)

            self._save()
            return entry

    def _on_success(self, entry: ModelHealthEntry, now: float, is_probe: bool) -> None:
        """处理成功请求"""
        entry.total_successes += 1
        entry.last_success_at = now
        entry.consecutive_failures = 0

        if is_probe:
            entry.probe_count += 1
            entry.probe_successes += 1
            logger.info(
                f"[ModelHealthRegistry] 模型 {entry.model} 探测成功 "
                f"(probe_successes={entry.probe_successes})"
            )

        # 重新计算错误率
        self._recalculate_error_rate(entry)

        # 状态降级评估（检查是否应进入 DEGRADED）
        self._evaluate_downgrade(entry, now)

        # 状态提升：DEGRADED → HEALTHY（需要错误率低于阈值的一半）
        if entry.state == ModelHealthState.DEGRADED.value:
            if entry.total_requests >= self._degraded_min_samples:
                if entry.error_rate < self._degraded_error_rate * 0.5:
                    self._transition_state(entry, ModelHealthState.HEALTHY, now)
                    logger.info(
                        f"[ModelHealthRegistry] 模型 {entry.model} 恢复 HEALTHY "
                        f"(error_rate={entry.error_rate:.1%})"
                    )

    def _on_failure(
        self,
        entry: ModelHealthEntry,
        error: Optional[str],
        now: float,
        is_probe: bool,
    ) -> None:
        """处理失败请求"""
        entry.total_failures += 1
        entry.consecutive_failures += 1
        entry.last_failure_at = now
        entry.last_failure_reason = error

        if is_probe:
            logger.warning(
                f"[ModelHealthRegistry] 模型 {entry.model} 探测失败 "
                f"(consecutive_failures={entry.consecutive_failures})"
            )

        self._recalculate_error_rate(entry)

        # 状态降级评估（在累加完成后进行）
        self._evaluate_downgrade(entry, now)

    def _recalculate_error_rate(self, entry: ModelHealthEntry) -> None:
        """重新计算错误率"""
        if entry.total_requests > 0:
            entry.error_rate = entry.total_failures / entry.total_requests

    def _evaluate_downgrade(self, entry: ModelHealthEntry, now: float) -> None:
        """评估是否需要状态降级"""
        # BLOCKED 检查（优先级最高）
        if (
            entry.state != ModelHealthState.BLOCKED.value
            and entry.consecutive_failures >= self._blocked_consecutive
        ):
            self._transition_state(entry, ModelHealthState.BLOCKED, now)
            logger.warning(
                f"[ModelHealthRegistry] 模型 {entry.model} 进入 BLOCKED "
                f"(consecutive_failures={entry.consecutive_failures})"
            )
            return

        # DEGRADED 检查
        if (
            entry.state == ModelHealthState.HEALTHY.value
            and entry.total_requests >= self._degraded_min_samples
            and entry.error_rate >= self._degraded_error_rate
        ):
            self._transition_state(entry, ModelHealthState.DEGRADED, now)
            logger.warning(
                f"[ModelHealthRegistry] 模型 {entry.model} 进入 DEGRADED "
                f"(error_rate={entry.error_rate:.1%}, requests={entry.total_requests})"
            )

    def _transition_state(
        self,
        entry: ModelHealthEntry,
        new_state: ModelHealthState,
        now: float,
    ) -> None:
        """状态流转"""
        entry.state = new_state.value
        entry.updated_at = now
        if new_state == ModelHealthState.DEGRADED:
            entry.first_degraded_at = now
        elif new_state == ModelHealthState.BLOCKED:
            entry.first_blocked_at = now
        elif new_state == ModelHealthState.HEALTHY:
            # 重置降级/阻塞标记
            entry.first_degraded_at = None
            entry.first_blocked_at = None
            entry.probe_count = 0
            entry.probe_successes = 0

    # -------------------------------------------------------------------------
    # 查询接口
    # -------------------------------------------------------------------------

    def get_health(self, model: str) -> Optional[ModelHealthEntry]:
        """获取模型健康状态（不存在返回 None）"""
        with self._lock:
            return self._entries.get(model)

    def is_healthy(self, model: str) -> bool:
        """判断模型是否完全可用"""
        entry = self.get_health(model)
        if entry is None:
            return True  # 未知模型默认健康
        return entry.state == ModelHealthState.HEALTHY.value

    def is_degraded(self, model: str) -> bool:
        """判断模型是否降级可用"""
        entry = self.get_health(model)
        return entry is not None and entry.state == ModelHealthState.DEGRADED.value

    def is_blocked(self, model: str) -> bool:
        """判断模型是否完全阻塞"""
        entry = self.get_health(model)
        return entry is not None and entry.state == ModelHealthState.BLOCKED.value

    def get_healthy_models(self) -> List[str]:
        """获取所有 HEALTHY 模型列表"""
        with self._lock:
            return [
                m for m, e in self._entries.items()
                if e.state == ModelHealthState.HEALTHY.value
            ]

    def get_degraded_models(self) -> List[str]:
        """获取所有 DEGRADED 模型列表"""
        with self._lock:
            return [
                m for m, e in self._entries.items()
                if e.state == ModelHealthState.DEGRADED.value
            ]

    def get_blocked_models(self) -> List[str]:
        """获取所有 BLOCKED 模型列表"""
        with self._lock:
            return [
                m for m, e in self._entries.items()
                if e.state == ModelHealthState.BLOCKED.value
            ]

    def get_all_summaries(self) -> List[Dict[str, Any]]:
        """获取所有模型的人类可读摘要"""
        with self._lock:
            return [e.to_summary() for e in self._entries.values()]

    # -------------------------------------------------------------------------
    # 恢复操作
    # -------------------------------------------------------------------------

    def reset_model(self, model: str, strategy: str = "auto") -> bool:
        """
        重置模型状态（手动恢复）

        Args:
            model:     模型名
            strategy:  恢复策略

        Returns:
            bool: 是否成功
        """
        with self._lock:
            if model not in self._entries:
                return False
            entry = self._entries[model]
            entry.state = ModelHealthState.HEALTHY.value
            entry.consecutive_failures = 0
            entry.error_rate = 0.0
            entry.first_degraded_at = None
            entry.first_blocked_at = None
            entry.probe_count = 0
            entry.probe_successes = 0
            entry.recovery_strategy = strategy
            entry.updated_at = time.time()
            self._save()
            logger.info(f"[ModelHealthRegistry] 模型 {model} 已重置, strategy={strategy}")
            return True

    def force_degraded(self, model: str, reason: str = "manual") -> bool:
        """强制将模型置为 DEGRADED 状态"""
        with self._lock:
            if model not in self._entries:
                self._entries[model] = ModelHealthEntry(
                    model=model, state=ModelHealthState.HEALTHY.value
                )
            entry = self._entries[model]
            entry.state = ModelHealthState.DEGRADED.value
            entry.last_failure_reason = reason
            entry.updated_at = time.time()
            self._save()
            return True

    def force_blocked(self, model: str, reason: str = "manual") -> bool:
        """强制将模型置为 BLOCKED 状态"""
        with self._lock:
            if model not in self._entries:
                self._entries[model] = ModelHealthEntry(
                    model=model, state=ModelHealthState.HEALTHY.value
                )
            entry = self._entries[model]
            entry.state = ModelHealthState.BLOCKED.value
            entry.last_failure_reason = reason
            entry.updated_at = time.time()
            self._save()
            return True

    # -------------------------------------------------------------------------
    # 统计
    # -------------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """获取全局统计"""
        with self._lock:
            healthy = sum(1 for e in self._entries.values() if e.state == ModelHealthState.HEALTHY.value)
            degraded = sum(1 for e in self._entries.values() if e.state == ModelHealthState.DEGRADED.value)
            blocked = sum(1 for e in self._entries.values() if e.state == ModelHealthState.BLOCKED.value)
            total_req = sum(e.total_requests for e in self._entries.values())
            total_fail = sum(e.total_failures for e in self._entries.values())
            return {
                "total_models": len(self._entries),
                "healthy": healthy,
                "degraded": degraded,
                "blocked": blocked,
                "total_requests": total_req,
                "total_failures": total_fail,
                "overall_error_rate": round(total_fail / max(total_req, 1), 4),
            }


# =============================================================================
# GlobalCircuitBreaker：跨会话断路器
# =============================================================================


@dataclass
class CircuitSnapshot:
    """断路器快照（用于监控）"""
    model: str
    state: CircuitState
    failures_in_window: int
    last_failure_at: Optional[float]
    open_since: Optional[float]     # 进入 OPEN 的时间
    half_open_probes: int
    half_open_successes: int
    total_rejections: int           # 被拒绝的请求数
    remaining_open_time: float     # OPEN 剩余秒数


class GlobalCircuitBreaker:
    """
    全局断路器（跨会话感知）

    设计目标:
    - 单例模式：整个进程共享一个断路器实例
    - 滑动窗口：60秒内失败次数超过阈值 → OPEN
    - OPEN → 拒绝所有请求 → 30秒后进入 HALF_OPEN
    - HALF_OPEN → 允许少量探测 → 成功则 CLOSED，失败则重新 OPEN
    - 避免 N 个会话 × M 次重试的灾难性重试风暴

    核心逻辑:
        CLOSED:  正常 → 记录每次失败（滑动窗口淘汰）
        OPEN:   全部拒绝 → 30秒后 → HALF_OPEN
        HALF_OPEN: 允许探测请求 → 成功N次 → CLOSED
                                        → 失败1次 → OPEN

    使用示例:
        cb = GlobalCircuitBreaker.get_instance()

        # 路由前检查
        if not cb.can_proceed("claude-sonnet"):
            raise CircuitOpenError("claude-sonnet")

        # 请求完成后报告
        cb.record_result("claude-sonnet", success=True)
        # 或
        cb.record_result("claude-sonnet", success=False)
    """

    _instance: Optional[GlobalCircuitBreaker] = None
    _instance_lock = threading.Lock()

    @classmethod
    def get_instance(
        cls,
        failure_threshold: int = DEFAULT_FAILURE_THRESHOLD,
        window_seconds: float = DEFAULT_WINDOW_SECONDS,
        open_duration: float = DEFAULT_OPEN_DURATION,
        half_open_max_probes: int = DEFAULT_HALF_OPEN_PROBES,
        recovery_threshold: int = DEFAULT_RECOVERY_THRESHOLD,
    ) -> GlobalCircuitBreaker:
        """
        获取单例实例（延迟初始化，线程安全）

        首次调用时创建实例，后续调用返回同一实例。
        多次调用时使用首次调用传入的参数。
        """
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls(
                        failure_threshold=failure_threshold,
                        window_seconds=window_seconds,
                        open_duration=open_duration,
                        half_open_max_probes=half_open_max_probes,
                        recovery_threshold=recovery_threshold,
                    )
                    logger.info(
                        f"[GlobalCircuitBreaker] 单例创建: "
                        f"threshold={failure_threshold}, window={window_seconds}s, "
                        f"open_duration={open_duration}s"
                    )
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """重置单例（仅用于测试）"""
        with cls._instance_lock:
            if cls._instance is not None:
                cls._instance._shutdown()
            cls._instance = None

    def __init__(
        self,
        failure_threshold: int,
        window_seconds: float,
        open_duration: float,
        half_open_max_probes: int,
        recovery_threshold: int,
    ):
        # 配置
        self._failure_threshold = failure_threshold
        self._window_seconds = window_seconds
        self._open_duration = open_duration
        self._half_open_max_probes = half_open_max_probes
        self._recovery_threshold = recovery_threshold

        # 状态
        self._lock = threading.RLock()
        self._states: Dict[str, CircuitState] = defaultdict(lambda: CircuitState.CLOSED)

        # 滑动窗口：model → 时间戳列表（每次失败的时间）
        self._failure_windows: Dict[str, List[float]] = defaultdict(list)

        # OPEN 状态开始时间：model → 时间戳
        self._open_since: Dict[str, float] = {}

        # HALF_OPEN 探测计数：model → (probes, successes)
        self._half_open_counts: Dict[str, tuple[int, int]] = defaultdict(
            lambda: (0, 0)
        )

        # 统计
        self._total_rejections: Dict[str, int] = defaultdict(int)
        self._total_successes: Dict[str, int] = defaultdict(int)
        self._total_failures: Dict[str, int] = defaultdict(int)

        logger.info(
            f"[GlobalCircuitBreaker] 初始化: threshold={failure_threshold}, "
            f"window={window_seconds}s, open_duration={open_duration}s"
        )

    # -------------------------------------------------------------------------
    # 核心 API
    # -------------------------------------------------------------------------

    def can_proceed(self, model: str) -> bool:
        """
        判断请求是否可以继续（断路器是否允许通过）

        CLOSED:  总是 True（滑动窗口内失败数 < 阈值）
        OPEN:   检查 OPEN 超时，未超时 → False，超时 → 转为 HALF_OPEN → True
        HALF_OPEN: 检查探测配额，未超配额 → True，超配额 → False

        Args:
            model: 模型标识符

        Returns:
            bool: 是否允许请求通过
        """
        with self._lock:
            state = self._states[model]

            if state == CircuitState.CLOSED:
                # 清理过期失败记录（滑动窗口淘汰）
                self._prune_window(model)
                return True

            elif state == CircuitState.OPEN:
                elapsed = time.time() - self._open_since.get(model, time.time())
                if elapsed < self._open_duration:
                    self._total_rejections[model] += 1
                    logger.debug(
                        f"[GlobalCircuitBreaker] OPEN 拒绝 {model}, "
                        f"剩余 {self._open_duration - elapsed:.1f}s"
                    )
                    return False
                else:
                    # 超时 → 进入 HALF_OPEN
                    self._transition_to_half_open(model)
                    return True

            elif state == CircuitState.HALF_OPEN:
                probes, successes = self._half_open_counts[model]
                if probes < self._half_open_max_probes:
                    return True
                self._total_rejections[model] += 1
                return False

            return False

    def record_result(
        self,
        model: str,
        success: bool,
        is_probe: bool = False,
    ) -> None:
        """
        记录请求结果（断路器状态更新）

        CLOSED:
            success  → 不操作
            failure  → 记录失败时间，触发滑动窗口，评估 OPEN
        HALF_OPEN:
            success  → probe_successes += 1，评估是否 → CLOSED
            failure  → 立即 → OPEN
        OPEN:
            success  → （不应发生，记录警告）
            failure  → 保持 OPEN，重置 OPEN 超时

        Args:
            model:    模型标识符
            success:  请求是否成功
            is_probe: 是否为探测请求（HALF_OPEN 期间）
        """
        with self._lock:
            if success:
                self._total_successes[model] += 1
                self._on_success(model, is_probe)
            else:
                self._total_failures[model] += 1
                self._on_failure(model, is_probe)

    def get_snapshot(self, model: str) -> CircuitSnapshot:
        """
        获取模型断路器快照（用于监控和调试）

        Returns:
            CircuitSnapshot: 当前状态快照
        """
        with self._lock:
            state = self._states[model]
            self._prune_window(model)
            failures = len(self._failure_windows[model])
            open_since = self._open_since.get(model)
            probes, successes = self._half_open_counts[model]

            remaining = 0.0
            if state == CircuitState.OPEN and open_since:
                remaining = max(0.0, self._open_duration - (time.time() - open_since))

            return CircuitSnapshot(
                model=model,
                state=state,
                failures_in_window=failures,
                last_failure_at=self._failure_windows[model][-1] if failures else None,
                open_since=open_since,
                half_open_probes=probes,
                half_open_successes=successes,
                total_rejections=self._total_rejections[model],
                remaining_open_time=remaining,
            )

    def get_all_snapshots(self) -> Dict[str, CircuitSnapshot]:
        """获取所有模型的快照"""
        with self._lock:
            return {model: self.get_snapshot(model) for model in list(self._states.keys())}

    def force_open(self, model: str, reason: str = "manual") -> None:
        """
        手动强制将模型断路器置为 OPEN（用于紧急熔断）

        Args:
            model:  模型标识符
            reason: 原因说明
        """
        with self._lock:
            self._transition_to_open(model)
            logger.warning(
                f"[GlobalCircuitBreaker] 手动强制 OPEN: {model}, reason={reason}"
            )

    def force_close(self, model: str) -> None:
        """
        手动强制将模型断路器重置为 CLOSED（用于恢复）

        Args:
            model:  模型标识符
        """
        with self._lock:
            self._transition_to_closed(model)
            logger.info(f"[GlobalCircuitBreaker] 手动强制 CLOSED: {model}")

    # -------------------------------------------------------------------------
    # 状态流转内部方法
    # -------------------------------------------------------------------------

    def _transition_to_open(self, model: str) -> None:
        """转为 OPEN 状态"""
        self._states[model] = CircuitState.OPEN
        self._open_since[model] = time.time()
        self._half_open_counts[model] = (0, 0)
        logger.warning(
            f"[GlobalCircuitBreaker] 模型 {model} → OPEN "
            f"(failures={len(self._failure_windows[model])} in window)"
        )

    def _transition_to_half_open(self, model: str) -> None:
        """转为 HALF_OPEN 状态"""
        self._states[model] = CircuitState.HALF_OPEN
        self._half_open_counts[model] = (0, 0)
        logger.info(f"[GlobalCircuitBreaker] 模型 {model} → HALF_OPEN (timeout)")

    def _transition_to_closed(self, model: str) -> None:
        """转为 CLOSED 状态"""
        self._states[model] = CircuitState.CLOSED
        self._failure_windows[model] = []
        self._open_since.pop(model, None)
        self._half_open_counts[model] = (0, 0)
        logger.info(f"[GlobalCircuitBreaker] 模型 {model} → CLOSED")

    def _on_success(self, model: str, is_probe: bool) -> None:
        """成功处理"""
        state = self._states[model]

        if state == CircuitState.HALF_OPEN:
            probes, successes = self._half_open_counts[model]
            successes += 1
            self._half_open_counts[model] = (probes, successes)
            logger.info(
                f"[GlobalCircuitBreaker] HALF_OPEN 探测成功 {model}: "
                f"{successes}/{self._recovery_threshold} → CLOSED"
            )
            if successes >= self._recovery_threshold:
                self._transition_to_closed(model)

        elif state == CircuitState.OPEN:
            # OPEN 期间收到成功（理论上不应该，但记录）
            logger.warning(
                f"[GlobalCircuitBreaker] OPEN 期间收到成功请求 {model}，忽略"
            )

        # CLOSED 状态下成功：清除滑动窗口（可选，保留以维持长期健康指标）

    def _on_failure(self, model: str, is_probe: bool) -> None:
        """失败处理"""
        state = self._states[model]

        if state == CircuitState.HALF_OPEN:
            # 任何失败立即重新 OPEN
            logger.warning(
                f"[GlobalCircuitBreaker] HALF_OPEN 探测失败 {model} → OPEN"
            )
            self._transition_to_open(model)

        elif state == CircuitState.CLOSED:
            # 记录失败到滑动窗口
            self._failure_windows[model].append(time.time())
            self._prune_window(model)
            failures = len(self._failure_windows[model])

            if failures >= self._failure_threshold:
                self._transition_to_open(model)

        elif state == CircuitState.OPEN:
            # 保持 OPEN，重置超时
            self._open_since[model] = time.time()
            logger.debug(
                f"[GlobalCircuitBreaker] OPEN 期间再次失败 {model}, "
                f"重置 OPEN 超时"
            )

    def _prune_window(self, model: str) -> None:
        """清理滑动窗口中超出窗口的失败记录"""
        cutoff = time.time() - self._window_seconds
        self._failure_windows[model] = [
            t for t in self._failure_windows[model] if t > cutoff
        ]

    # -------------------------------------------------------------------------
    # 统计
    # -------------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """获取全局统计"""
        with self._lock:
            open_count = sum(1 for s in self._states.values() if s == CircuitState.OPEN)
            half_open_count = sum(1 for s in self._states.values() if s == CircuitState.HALF_OPEN)
            closed_count = sum(1 for s in self._states.values() if s == CircuitState.CLOSED)
            total_rej = sum(self._total_rejections.values())
            total_suc = sum(self._total_successes.values())
            total_fail = sum(self._total_failures.values())
            return {
                "total_models": len(self._states),
                "closed": closed_count,
                "open": open_count,
                "half_open": half_open_count,
                "total_successes": total_suc,
                "total_failures": total_fail,
                "total_rejections": total_rej,
                "failure_threshold": self._failure_threshold,
                "window_seconds": self._window_seconds,
                "open_duration": self._open_duration,
                "recovery_threshold": self._recovery_threshold,
            }

    def _shutdown(self) -> None:
        """关闭清理（仅测试用）"""
        self._states.clear()
        self._failure_windows.clear()
        self._open_since.clear()
        self._half_open_counts.clear()


# =============================================================================
# 集成工具函数
# =============================================================================


def check_model_health(model: str) -> tuple[bool, str]:
    """
    快捷函数：检查模型是否允许请求

    Returns:
        (can_proceed, reason): 是否可请求 + 拒绝原因
    """
    cb = GlobalCircuitBreaker.get_instance()
    registry = _get_registry()

    if not cb.can_proceed(model):
        snap = cb.get_snapshot(model)
        if snap.remaining_open_time > 0:
            return False, f"Circuit OPEN, retry in {snap.remaining_open_time:.1f}s"
        return False, f"Circuit {snap.state.value}"

    if registry.is_blocked(model):
        return False, f"Model {model} is BLOCKED (error_rate={registry.get_health(model).error_rate:.1%})"

    if registry.is_degraded(model):
        entry = registry.get_health(model)
        return True, f"DEGRADED (error_rate={entry.error_rate:.1%})"

    return True, "OK"


# 默认持久化路径（可被 EngineRouter 覆盖）
_DEFAULT_PERSIST_PATH: str = MODEL_HEALTH_FILE

# 全局注册表缓存（EngineRouter 初始化时共享）
_global_registry: Optional["ModelHealthRegistry"] = None


def set_global_registry(registry: "ModelHealthRegistry") -> None:
    """由 EngineRouter 调用，设置全局健康注册表"""
    global _global_registry
    _global_registry = registry


def _get_registry(persist_path: Optional[str] = None) -> "ModelHealthRegistry":
    """
    获取健康注册表实例

    优先级:
        1. 全局注册表（EngineRouter 已初始化）
        2. 指定 persist_path
        3. 默认路径
    """
    global _global_registry
    if _global_registry is not None:
        return _global_registry
    return ModelHealthRegistry(persist_path=persist_path or _DEFAULT_PERSIST_PATH)


def report_request_result(
    model: str,
    success: bool,
    error: Optional[str] = None,
    is_probe: bool = False,
    persist_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    统一报告函数：同时更新断路器和健康注册表

    Args:
        model:        模型标识符
        success:      请求是否成功
        error:        错误信息（失败时）
        is_probe:     是否为探测请求
        persist_path:  持久化路径（None = 使用全局/默认路径）

    Returns:
        Dict: {
            "circuit_state": str,   # CLOSED/OPEN/HALF_OPEN
            "health_state": str,   # HEALTHY/DEGRADED/BLOCKED
            "model_health": dict    # ModelHealthEntry.to_summary()
            "circuit_snapshot": dict
        }
    """
    cb = GlobalCircuitBreaker.get_instance()
    registry = _get_registry(persist_path)

    # 断路器记录
    cb.record_result(model, success=success, is_probe=is_probe)

    # 健康注册表记录
    entry = registry.report_request(model, success=success, error=error, is_probe=is_probe)

    snap = cb.get_snapshot(model)

    return {
        "circuit_state": snap.state.value,
        "health_state": entry.state,
        "model_health": entry.to_summary(),
        "circuit_snapshot": {
            "failures_in_window": snap.failures_in_window,
            "total_rejections": snap.total_rejections,
            "remaining_open_time": snap.remaining_open_time,
        },
    }


# =============================================================================
# 健康报告生成器
# =============================================================================


def generate_health_report(
    models: Optional[List[str]] = None,
    persist_path: str = MODEL_HEALTH_FILE,
) -> Dict[str, Any]:
    """
    生成健康度报告（用于监控面板 / 健康检查接口）

    Args:
        models:      要报告的模型列表（None = 所有模型）
        persist_path: model_health.json 路径

    Returns:
        Dict: 完整健康报告 {
            "generated_at": ISO8601,
            "summary": {...},
            "models": [...],
            "circuit_breaker": {...},
        }
    """
    from datetime import datetime, timezone

    registry = _get_registry(persist_path=persist_path)
    cb = GlobalCircuitBreaker.get_instance()

    # 确定要报告的模型
    if models:
        targets = [m for m in models if registry.get_health(m) or True]
    else:
        targets = list(registry._entries.keys())

    model_reports = []
    for model in targets:
        health = registry.get_health(model)
        snap = cb.get_snapshot(model)
        report = {
            "model": model,
            "health_state": health.state if health else "unknown",
            "error_rate": round(health.error_rate, 4) if health else None,
            "consecutive_failures": health.consecutive_failures if health else 0,
            "total_requests": health.total_requests if health else 0,
            "circuit_state": snap.state.value,
            "circuit_failures_in_window": snap.failures_in_window,
            "circuit_open": snap.state == CircuitState.OPEN,
            "remaining_open_time": round(snap.remaining_open_time, 2),
            "total_rejections": snap.total_rejections,
            "last_failure_reason": health.last_failure_reason if health else None,
            "last_failure_at": health.last_failure_at if health else None,
            "is_available": snap.state != CircuitState.OPEN,
        }
        model_reports.append(report)

    model_reports.sort(key=lambda x: (
        0 if x["circuit_open"] else 1,
        -x["total_requests"] if x["total_requests"] else 2,
    ))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_models": len(model_reports),
            "available": sum(1 for r in model_reports if r["is_available"]),
            "circuit_open": sum(1 for r in model_reports if r["circuit_open"]),
            "blocked": sum(1 for r in model_reports if r["health_state"] == "blocked"),
            "degraded": sum(1 for r in model_reports if r["health_state"] == "degraded"),
        },
        "models": model_reports,
        "circuit_breaker_stats": cb.get_stats(),
        "health_registry_stats": registry.get_stats(),
    }
