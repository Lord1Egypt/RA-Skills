"""
Execution Engine Abstract Base

执行引擎抽象基类 - 定义所有引擎的统一接口
"""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Optional
import threading

logger = logging.getLogger(__name__)


# =============================================================================
# AuthProfile：API Key 轮换与指数退避
# =============================================================================


class AuthProfileError(Exception):
    """AuthProfile 基础异常"""
    pass


class NoAvailableKeyError(AuthProfileError):
    """所有 Key 均不可用（全部处于冷却期）"""
    pass


class KeyCooldownError(AuthProfileError):
    """指定 Key 当前处于冷却期"""

    def __init__(self, key_id: str, cooldown_remaining: float, message: str = ""):
        super().__init__(message or f"Key {key_id} 冷却中，剩余 {cooldown_remaining:.1f}s")
        self.key_id = key_id
        self.cooldown_remaining = cooldown_remaining


class KeyHealthStatus(Enum):
    """Key 健康状态"""
    HEALTHY = "healthy"       # 可用
    COOLING = "cooling"       # 冷却中
    DEAD = "dead"             # 永久失败（连续失败超过阈值）


@dataclass
class AuthKeyState:
    """
    单个 API Key 的状态

    Attributes:
        key_id:        Key 的唯一标识（可自定义，或使用 key 本身前4位）
        key:           原始 Key 值（对外不暴露）
        consecutive_failures: 连续失败次数
        cooldown_until:       冷却截止时间戳（秒，time.time() 格式），0 表示不冷却
        total_requests:      累计请求数
        total_failures:      累计失败数
        total_successes:     累计成功数
        last_used_at:        最后使用时间
        last_failure_at:     最后失败时间
    """
    key_id: str
    key: str
    consecutive_failures: int = 0
    cooldown_until: float = 0.0     # Unix timestamp, 0 = no cooldown
    total_requests: int = 0
    total_failures: int = 0
    total_successes: int = 0
    last_used_at: Optional[float] = None
    last_failure_at: Optional[float] = None

    @property
    def is_in_cooldown(self) -> bool:
        """当前是否处于冷却期"""
        return self.cooldown_until > 0 and time.time() < self.cooldown_until

    @property
    def cooldown_remaining(self) -> float:
        """冷却剩余时间（秒），负数表示已过期"""
        if self.cooldown_until <= 0:
            return 0.0
        return max(0.0, self.cooldown_until - time.time())

    @property
    def health_status(self) -> KeyHealthStatus:
        """计算健康状态"""
        if self.consecutive_failures >= 5:
            return KeyHealthStatus.DEAD
        if self.is_in_cooldown:
            return KeyHealthStatus.COOLING
        return KeyHealthStatus.HEALTHY


class AuthProfile:
    """
    API Key 轮换与指数退避管理

    核心能力:
    1. 多 Key 轮换（Round-Robin）
    2. 指数退避冷却（初始30s，指数增长，最大5分钟）
    3. 失败计数自动递增，成功调用重置计数
    4. 线程安全（支持异步多并发调用）

    退避公式:
        cooldown_seconds = min(INITIAL_COOLDOWN * (2 ** failures), MAX_COOLDOWN)
        - 0次失败:  30s
        - 1次失败:  60s
        - 2次失败:  120s
        - 3次失败:  240s
        - 4次失败:  300s (封顶)

    使用示例:
        profile = AuthProfile(
            keys=["key1", "key2", "key3"],
            initial_cooldown=30.0,
            max_cooldown=300.0,
        )
        # 获取可用 Key
        key_state = profile.get_available_key()
        # ...
        profile.report_success(key_state.key_id)   # 成功：重置计数
        profile.report_failure(key_state.key_id)  # 失败：冷却 + 递增
    """

    DEFAULT_INITIAL_COOLDOWN = 30.0   # 秒
    DEFAULT_MAX_COOLDOWN = 300.0      # 5 分钟
    DEFAULT_BACKOFF_MULTIPLIER = 2.0  # 指数乘数
    MAX_CONSECUTIVE_FAILURES = 5      # 超过此值标记为 DEAD

    def __init__(
        self,
        keys: Optional[List[str]] = None,
        key_ids: Optional[List[str]] = None,
        initial_cooldown: float = DEFAULT_INITIAL_COOLDOWN,
        max_cooldown: float = DEFAULT_MAX_COOLDOWN,
        backoff_multiplier: float = DEFAULT_BACKOFF_MULTIPLIER,
    ):
        """
        初始化 AuthProfile

        Args:
            keys:            API Key 列表
            key_ids:         每个 Key 的自定义标识列表（与 keys 一一对应）
                             若不提供则自动用 Key 前4位作为标识
            initial_cooldown: 首次失败后的冷却时间（秒）
            max_cooldown:     最大冷却时间（秒）
            backoff_multiplier: 退避乘数（2 = 每次翻倍）
        """
        self._keys: List[AuthKeyState] = []
        self._initial_cooldown = initial_cooldown
        self._max_cooldown = max_cooldown
        self._backoff_multiplier = backoff_multiplier
        self._round_robin_index = 0
        self._lock = threading.Lock()

        if keys:
            self.add_keys(keys, key_ids)

        logger.info(
            f"[AuthProfile] 初始化 | keys={len(self._keys)} | "
            f"initial_cooldown={initial_cooldown}s | max_cooldown={max_cooldown}s"
        )

    # -------------------------------------------------------------------------
    # Key 管理
    # -------------------------------------------------------------------------

    def add_keys(self, keys: List[str], key_ids: Optional[List[str]] = None) -> None:
        """
        批量添加 Key

        Args:
            keys:    API Key 列表
            key_ids: 自定义 ID 列表（可选，与 keys 一一对应）
        """
        for i, key in enumerate(keys):
            kid = (key_ids[i] if key_ids and i < len(key_ids) else self._make_key_id(key))
            self.add_key(key, kid)

    def add_key(self, key: str, key_id: Optional[str] = None) -> None:
        """
        添加单个 Key

        Args:
            key:    API Key
            key_id: 自定义 ID（可选，默认使用 key 前4位）
        """
        kid = key_id or self._make_key_id(key)
        if any(k.key_id == kid for k in self._keys):
            logger.warning(f"[AuthProfile] Key ID {kid} 已存在，跳过")
            return
        self._keys.append(AuthKeyState(key_id=kid, key=key))
        logger.debug(f"[AuthProfile] 添加 Key: {kid}")

    def remove_key(self, key_id: str) -> bool:
        """移除 Key"""
        with self._lock:
            before = len(self._keys)
            self._keys = [k for k in self._keys if k.key_id != key_id]
            if len(self._keys) < before:
                logger.info(f"[AuthProfile] 移除 Key: {key_id}")
                return True
            return False

    # -------------------------------------------------------------------------
    # 核心轮换与退避
    # -------------------------------------------------------------------------

    def get_available_key(self) -> AuthKeyState:
        """
        获取当前可用的 Key（Round-Robin + 冷却过滤）

        Returns:
            AuthKeyState: 可用的 Key 状态

        Raises:
            NoAvailableKeyError: 所有 Key 均处于冷却期

        策略:
            1. 从当前 round-robin 位置开始扫描，跳过冷却中的 Key
            2. 若扫描一圈无结果，抛出 NoAvailableKeyError
            3. 每次成功调用后轮换到下一位
        """
        with self._lock:
            if not self._keys:
                raise NoAvailableKeyError("AuthProfile 中没有任何 Key")

            # 最多扫描两圈（第一圈找可用，第二圈确认全在冷却）
            num_keys = len(self._keys)

            for _ in range(num_keys):
                idx = self._round_robin_index % num_keys
                key_state = self._keys[idx]

                if not key_state.is_in_cooldown:
                    # 找到可用 Key，轮换到下一个
                    key_state.last_used_at = time.time()
                    key_state.total_requests += 1
                    self._round_robin_index = idx + 1
                    return key_state

                self._round_robin_index += 1

            # 所有 Key 都在冷却，计算剩余时间
            earliest_cooldown = min(k.cooldown_remaining for k in self._keys)
            raise NoAvailableKeyError(
                f"所有 {num_keys} 个 Key 均处于冷却期，最早冷却结束: {earliest_cooldown:.1f}s 后"
            )

    def get_available_key_sync(self) -> AuthKeyState:
        """同步版本的 get_available_key（内部加锁调用）"""
        return self.get_available_key()

    def report_success(self, key_id: str) -> None:
        """
        报告 Key 调用成功

        效果:
            - 重置 consecutive_failures 为 0
            - 取消冷却状态
            - total_successes += 1
        """
        with self._lock:
            key_state = self._find_key(key_id)
            if key_state is None:
                logger.warning(f"[AuthProfile] report_success: 未找到 key_id={key_id}")
                return

            was_failing = key_state.consecutive_failures > 0
            key_state.consecutive_failures = 0
            key_state.cooldown_until = 0.0
            key_state.total_successes += 1

            if was_failing:
                logger.info(
                    f"[AuthProfile] Key {key_id} 成功调用，"
                    f"退避状态已重置（此前连续失败 {key_state.consecutive_failures} 次）"
                )

    def report_failure(
        self,
        key_id: str,
        retryable: bool = True,
    ) -> Optional[float]:
        """
        报告 Key 调用失败

        效果:
            - consecutive_failures += 1
            - 若 retryable=True: 按指数退避设置冷却时间
            - total_failures += 1

        Args:
            key_id:    失败的 Key ID
            retryable: 是否可重试（True → 触发退避冷却，False → 标记 DEAD 但不冷却）

        Returns:
            float: 本次退避时长（秒），若不可重试则返回 None
        """
        with self._lock:
            key_state = self._find_key(key_id)
            if key_state is None:
                logger.warning(f"[AuthProfile] report_failure: 未找到 key_id={key_id}")
                return None

            key_state.consecutive_failures += 1
            key_state.total_failures += 1
            key_state.last_failure_at = time.time()

            cooldown: Optional[float] = None
            if retryable:
                cooldown = self._calc_cooldown(key_state)
                key_state.cooldown_until = time.time() + cooldown
                logger.warning(
                    f"[AuthProfile] Key {key_id} 失败 #{key_state.consecutive_failures}，"
                    f"进入冷却 {cooldown:.1f}s（下次退避: {self._calc_next_cooldown(key_state):.1f}s）"
                )
            else:
                logger.error(
                    f"[AuthProfile] Key {key_id} 不可重试失败，"
                    f"已标记为 DEAD（连续失败 {key_state.consecutive_failures} 次）"
                )

            return cooldown

    def get_cooldown_remaining(self, key_id: str) -> float:
        """查询指定 Key 的冷却剩余时间"""
        with self._lock:
            key_state = self._find_key(key_id)
            if key_state is None:
                return 0.0
            return key_state.cooldown_remaining

    def force_reset_key(self, key_id: str) -> bool:
        """强制重置指定 Key（清除冷却和失败计数）"""
        with self._lock:
            key_state = self._find_key(key_id)
            if key_state is None:
                return False
            key_state.consecutive_failures = 0
            key_state.cooldown_until = 0.0
            logger.info(f"[AuthProfile] 强制重置 Key {key_id}")
            return True

    # -------------------------------------------------------------------------
    # 统计与诊断
    # -------------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """
        获取 AuthProfile 全局统计

        Returns:
            Dict: 统计信息（不含敏感 Key 值）
        """
        with self._lock:
            total_req = sum(k.total_requests for k in self._keys)
            total_suc = sum(k.total_successes for k in self._keys)
            total_fail = sum(k.total_failures for k in self._keys)
            healthy = [k for k in self._keys if k.health_status == KeyHealthStatus.HEALTHY]
            cooling = [k for k in self._keys if k.health_status == KeyHealthStatus.COOLING]
            dead = [k for k in self._keys if k.health_status == KeyHealthStatus.DEAD]

            return {
                "total_keys": len(self._keys),
                "total_requests": total_req,
                "total_successes": total_suc,
                "total_failures": total_fail,
                "overall_success_rate": round(total_suc / max(total_req, 1) * 100, 2),
                "healthy_keys": len(healthy),
                "cooling_keys": len(cooling),
                "dead_keys": len(dead),
                "keys": [
                    {
                        "key_id": k.key_id,
                        "status": k.health_status.value,
                        "consecutive_failures": k.consecutive_failures,
                        "cooldown_remaining": round(k.cooldown_remaining, 1),
                        "total_requests": k.total_requests,
                        "total_successes": k.total_successes,
                        "total_failures": k.total_failures,
                    }
                    for k in self._keys
                ],
            }

    # -------------------------------------------------------------------------
    # 内部方法
    # -------------------------------------------------------------------------

    def _find_key(self, key_id: str) -> Optional[AuthKeyState]:
        """根据 key_id 查找 Key 状态"""
        for k in self._keys:
            if k.key_id == key_id:
                return k
        return None

    def _make_key_id(self, key: str) -> str:
        """从 Key 值生成脱敏 ID"""
        return f"key_{key[:4]}***"

    def _calc_cooldown(self, key_state: AuthKeyState) -> float:
        """计算退避冷却时间"""
        failures = key_state.consecutive_failures
        cooldown = min(
            self._initial_cooldown * (self._backoff_multiplier ** (failures - 1)),
            self._max_cooldown,
        )
        return cooldown

    def _calc_next_cooldown(self, key_state: AuthKeyState) -> float:
        """计算下次失败的退避时长（预览）"""
        fake_state = AuthKeyState(
            key_id=key_state.key_id,
            key=key_state.key,
            consecutive_failures=key_state.consecutive_failures + 1,
        )
        return self._calc_cooldown(fake_state)


# =============================================================================
# 数据模型
# =============================================================================


@dataclass
class ExecutionResult:
    """
    执行结果

    所有引擎执行完成后返回的标准化结果结构
    """
    success: bool
    output: Any                                    # 执行输出
    metadata: Dict[str, Any] = field(default_factory=dict)  # 附加元数据
    tokens_used: int = 0                            # 消耗的 token 数
    latency_ms: float = 0.0                        # 执行延迟（毫秒）
    error: Optional[str] = None                    # 错误信息（失败时填充）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "metadata": self.metadata,
            "tokens_used": self.tokens_used,
            "latency_ms": round(self.latency_ms, 2),
            "error": self.error,
        }


@dataclass
class StreamChunk:
    """
    流式输出块

    用于流式执行的增量输出
    """
    content: str           # 本次增量内容
    done: bool             # 是否为最后一块
    delta_ms: float = 0.0  # 与上一块的间隔（毫秒）


# =============================================================================
# 抽象基类
# =============================================================================


class ExecutionEngine(ABC):
    """
    执行引擎抽象基类

    所有执行引擎（Claude MA / Local / DeepSeek）必须实现此接口。
    统一抽象确保引擎可替换、热切换。

    设计原则：
    1. 最小接口：execute / stream / engine_name / capabilities
    2. 结果标准化：统一返回 ExecutionResult
    3. 配置外部化：敏感参数通过 context 传入，不硬编码
    4. 日志完整：引擎切换、执行路径全程可追踪

    Extension Points:
        - 初始化时注入 logger / metrics collector
        - 可重写 _validate_context 做上下文校验
        - 可重写 _build_metadata 添加引擎特定元数据
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化引擎

        Args:
            config: 引擎配置（如 API key、endpoint、model 等）
        """
        self._config = config or {}
        cls_name = self.__class__.__name__
        self._stats = {
            "total_requests": 0,
            "success": 0,
            "failed": 0,
            "total_tokens": 0,
            "total_latency_ms": 0.0,
        }
        logger.info(f"[{cls_name}] 引擎初始化, config_keys={list(self._config.keys())}")

    # -------------------------------------------------------------------------
    # 抽象接口（子类必须实现）
    # -------------------------------------------------------------------------

    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> ExecutionResult:
        """
        执行任务（阻塞模式）

        Args:
            task: 任务描述（自然语言）
            context: 执行上下文，包含：
                - user_id: str          用户ID
                - user_role: str        用户角色
                - intent_type: str      意图类型
                - parameters: dict      额外参数

        Returns:
            ExecutionResult: 标准执行结果
        """
        pass

    @abstractmethod
    async def stream(self, task: str, context: Dict[str, Any]) -> AsyncIterator[StreamChunk]:
        """
        流式执行（增量输出）

        Args:
            task: 任务描述
            context: 执行上下文

        Yields:
            StreamChunk: 增量输出块
        """
        yield  # 确保是 async generator

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """引擎名称（唯一标识）"""
        pass

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        引擎能力矩阵

        Returns:
            Dict[str, bool], 可能的 key:
                - session_persistence: 会话保持
                - harness_control:    工具调用控制
                - sandbox:            沙箱隔离
                - credential_management: 凭证管理
                - self_evolution:     自进化支持
                - vertical_knowledge: 垂直领域知识
                - streaming:           流式输出
                - multi_modal:         多模态支持
                - compliance_certified: 合规认证（等保/信创）
        """
        pass

    # -------------------------------------------------------------------------
    # 默认实现（可重写）
    # -------------------------------------------------------------------------

    async def health_check(self) -> bool:
        """
        健康检查

        Returns:
            bool: 引擎是否可用
        """
        try:
            result = await self.execute(
                task="health_check",
                context={"_health_check": True},
            )
            return result.success
        except Exception as e:
            logger.warning(f"[{self.engine_name}] 健康检查失败: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息"""
        total = self._stats["total_requests"]
        return {
            **self._stats,
            "engine": self.engine_name,
            "success_rate": round(
                self._stats["success"] / max(total, 1) * 100, 2
            ),
            "avg_latency_ms": round(
                self._stats["total_latency_ms"] / max(total, 1), 2
            ),
        }

    # -------------------------------------------------------------------------
    # 内部工具方法（子类可复用）
    # -------------------------------------------------------------------------

    def _record_stats(self, result: ExecutionResult) -> None:
        """记录执行统计"""
        self._stats["total_requests"] += 1
        if result.success:
            self._stats["success"] += 1
        else:
            self._stats["failed"] += 1
        self._stats["total_tokens"] += result.tokens_used
        self._stats["total_latency_ms"] += result.latency_ms

    def _validate_context(self, context: Dict[str, Any]) -> None:
        """
        校验上下文（子类可重写添加额外校验）

        Raises:
            ValueError: 必要字段缺失
        """
        required = ["user_id", "user_role"]
        missing = [k for k in required if k not in context]
        if missing:
            raise ValueError(f"执行上下文缺少必要字段: {missing}")

    def _build_metadata(
        self,
        context: Dict[str, Any],
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """构建元数据（子类可扩展）"""
        meta = {
            "engine": self.engine_name,
            "timestamp": datetime.now().isoformat(),
            "intent_type": context.get("intent_type", "unknown"),
        }
        if extra:
            meta.update(extra)
        return meta

    def _timed_execute(self, coro):
        """
        执行协程并测量延迟的装饰器模式

        用法:
            async def _do_execute(self, task, context):
                return await self._timed_execute(
                    self._raw_execute(task, context)
                )
        """
        start = time.perf_counter()

        async def wrapper():
            result = await coro
            result.latency_ms = (time.perf_counter() - start) * 1000
            self._record_stats(result)
            return result

        return wrapper()
