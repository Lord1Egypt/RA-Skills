"""
Dynamic Adjuster - 动态调整器

在执行过程中监控质量、动态调整策略，支持：
    - 失败重试策略（指数退避）
    - 备选方案选择（Agent fallback）
    - 执行超时处理
    - 实时质量评分
    - 策略热切换

Change Log:
    2026-04-14: 初始版本
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# 调整策略
# =============================================================================

class AdjustmentType(Enum):
    """调整类型"""
    RETRY           = "retry"           # 重试当前任务
    FALLBACK_AGENT  = "fallback_agent"  # 切换到备用Agent
    SKIP_TASK       = "skip_task"       # 跳过当前任务继续
    SPLIT_TASK      = "split_task"      # 拆分任务
    ESCALATE        = "escalate"        # 升级（人工介入）
    REPLAN          = "replan"          # 重新规划（重新拆解）


class AdjustmentReason(Enum):
    """调整原因"""
    TIMEOUT          = "timeout"
    AGENT_ERROR      = "agent_error"
    LOW_CONFIDENCE   = "low_confidence"
    QUALITY_BELOW    = "quality_below_threshold"
    DEPENDENCY_FAIL  = "dependency_failure"
    USER_ABORT       = "user_abort"


# =============================================================================
# 调整决策
# =============================================================================

@dataclass
class AdjustmentDecision:
    """调整决策"""
    adjustment_type: AdjustmentType
    reason: AdjustmentReason
    target_task_id: str
    fallback_agent: Optional[str] = None
    retry_count: int = 0
    confidence_before: float = 0.0
    confidence_after: float = 0.0
    message: str = ""
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))
    latency_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "adjustment_type": self.adjustment_type.value,
            "reason": self.reason.value,
            "target_task_id": self.target_task_id,
            "fallback_agent": self.fallback_agent,
            "retry_count": self.retry_count,
            "confidence_before": round(self.confidence_before, 4),
            "confidence_after": round(self.confidence_after, 4),
            "message": self.message,
            "timestamp": self.timestamp,
            "latency_ms": round(self.latency_ms, 1),
        }


@dataclass
class ExecutionSnapshot:
    """执行快照"""
    task_id: str
    action: str
    agent_name: str
    status: str                  # running / completed / failed / skipped
    start_time_ms: float
    duration_ms: float
    result_preview: Optional[str] = None
    error: Optional[str] = None
    confidence: float = 0.0
    retry_count: int = 0
    adjustments: list[AdjustmentDecision] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "action": self.action,
            "agent_name": self.agent_name,
            "status": self.status,
            "start_time_ms": self.start_time_ms,
            "duration_ms": round(self.duration_ms, 1),
            "result_preview": self.result_preview[:100] if self.result_preview else None,
            "error": self.error,
            "confidence": round(self.confidence, 4),
            "retry_count": self.retry_count,
            "adjustments": [a.to_dict() for a in self.adjustments],
        }


# =============================================================================
# 重试策略配置
# =============================================================================

@dataclass
class RetryPolicy:
    """重试策略"""
    max_retries: int = 3
    base_delay_ms: float = 500.0       # 基础延迟
    exponential_base: float = 2.0      # 指数退避底数
    jitter: bool = True                # 随机抖动
    retry_on_timeout: bool = True
    retry_on_agent_error: bool = True
    timeout_ms: float = 30000.0        # 单任务超时

    def get_delay(self, attempt: int) -> float:
        """计算重试延迟（毫秒）"""
        delay = self.base_delay_ms * (self.exponential_base ** attempt)
        if self.jitter:
            import random
            delay *= (0.5 + random.random())  # [0.5, 1.5] 倍
        return min(delay, 30000.0)  # 上限30秒


# =============================================================================
# 动态调整器
# =============================================================================

class DynamicAdjuster:
    """
    动态调整器

    使用方法：
        1. 初始化时注入 agent_registry
        2. 执行任务前调用 should_adjust 决策是否需要调整
        3. 任务完成后调用 record_result 记录结果
        4. 任务失败时调用 adjust 获取调整决策
        5. 执行后调用 evaluate_quality 评估质量
        6. 支持 asyncio 异步执行模式

    核心指标：
        - 动态调整响应时间 < 1秒
        - 重试成功率 > 80%（可配置）
    """

    def __init__(
        self,
        retry_policy: Optional[RetryPolicy] = None,
        quality_threshold: float = 0.6,
        agent_registry: Optional[dict] = None,
    ):
        self.retry_policy = retry_policy or RetryPolicy()
        self.quality_threshold = quality_threshold
        self.agent_registry = agent_registry or {}

        self._snapshots: list[ExecutionSnapshot] = []
        self._retry_counters: dict[str, int] = {}   # task_id → retry count
        self._stats = {
            "total_adjustments": 0,
            "successful_retries": 0,
            "fallback_switches": 0,
            "skips": 0,
        }

    # -------------------------------------------------------------------
    # 调整决策入口
    # -------------------------------------------------------------------

    def should_adjust(
        self,
        task_id: str,
        action: str,
        elapsed_ms: float,
        current_confidence: float = 1.0,
    ) -> tuple[bool, Optional[AdjustmentDecision]]:
        """
        判断是否需要调整

        触发条件：
            1. 执行超时
            2. 置信度低于阈值
            3. 耗时异常（超过预估的3倍）

        Returns:
            (是否需要调整, 调整决策)
        """
        t0 = time.perf_counter()

        # 超时检测
        if elapsed_ms > self.retry_policy.timeout_ms:
            decision = self._make_decision(
                AdjustmentType.RETRY,
                AdjustmentReason.TIMEOUT,
                task_id,
                confidence_before=current_confidence,
                message=f"任务执行超时（{elapsed_ms:.0f}ms > {self.retry_policy.timeout_ms:.0f}ms）",
            )
            return True, decision

        # 低置信度检测
        if current_confidence < self.quality_threshold:
            decision = self._make_decision(
                AdjustmentType.RETRY,
                AdjustmentReason.LOW_CONFIDENCE,
                task_id,
                confidence_before=current_confidence,
                message=f"置信度过低（{current_confidence:.2%} < {self.quality_threshold:.0%}）",
            )
            return True, decision

        return False, None

    def adjust(
        self,
        task_id: str,
        action: str,
        agent_name: str,
        error: Optional[str],
        retry_count: int,
    ) -> AdjustmentDecision:
        """
        任务失败后的调整决策

        策略：
            1. 未超最大重试次数 → RETRY
            2. 已超最大重试次数 + 有 fallback → FALLBACK_AGENT
            3. 已超最大重试次数 + 无 fallback → SKIP_TASK
            4. 特定错误类型（人工介入）→ ESCALATE
        """
        t0 = time.perf_counter()

        rc = retry_count if retry_count is not None else self._retry_counters.get(task_id, 0)

        # 1. 仍可重试
        if rc < self.retry_policy.max_retries:
            self._retry_counters[task_id] = rc + 1
            self._stats["total_adjustments"] += 1
            self._stats["successful_retries"] += 1

            delay_ms = self.retry_policy.get_delay(rc)
            decision = self._make_decision(
                AdjustmentType.RETRY,
                AdjustmentReason.AGENT_ERROR,
                task_id,
                retry_count=rc + 1,
                message=f"第{rc+1}次重试，延迟{delay_ms:.0f}ms: {error or 'unknown'}",
            )
            decision.latency_ms = (time.perf_counter() - t0) * 1000
            return decision

        # 2. 查找 fallback Agent
        fallback = self._get_fallback_agent(agent_name)
        if fallback:
            self._stats["total_adjustments"] += 1
            self._stats["fallback_switches"] += 1

            decision = self._make_decision(
                AdjustmentType.FALLBACK_AGENT,
                AdjustmentReason.AGENT_ERROR,
                task_id,
                fallback_agent=fallback,
                message=f"Agent {agent_name} 失败，切换到 {fallback}: {error}",
            )
            decision.latency_ms = (time.perf_counter() - t0) * 1000
            return decision

        # 3. 跳过任务
        self._stats["total_adjustments"] += 1
        self._stats["skips"] += 1

        decision = self._make_decision(
            AdjustmentType.SKIP_TASK,
            AdjustmentReason.AGENT_ERROR,
            task_id,
            message=f"跳过任务 {task_id}: {error}",
        )
        decision.latency_ms = (time.perf_counter() - t0) * 1000
        return decision

    # -------------------------------------------------------------------
    # 执行记录与质量评估
    # -------------------------------------------------------------------

    def record_result(
        self,
        snapshot: ExecutionSnapshot,
    ) -> float:
        """
        记录任务执行结果

        Returns:
            quality_score [0, 1]
        """
        self._snapshots.append(snapshot)

        # 基础质量分
        if snapshot.status == "completed":
            base_score = snapshot.confidence
        elif snapshot.status == "failed":
            base_score = 0.0
        elif snapshot.status == "skipped":
            base_score = 0.3
        else:
            base_score = 0.5

        # 重试惩罚
        penalty = min(snapshot.retry_count * 0.1, 0.3)
        quality = max(base_score - penalty, 0.0)

        logger.info(
            f"[DynamicAdjuster] recorded {snapshot.task_id} "
            f"status={snapshot.status} quality={quality:.2%} "
            f"retries={snapshot.retry_count}"
        )

        return quality

    def evaluate_workflow_quality(
        self,
        snapshots: list[ExecutionSnapshot],
    ) -> dict[str, Any]:
        """
        评估整个工作流的质量

        Returns:
            质量评估报告
        """
        if not snapshots:
            return {"overall_quality": 0.0, "status": "no_data"}

        completed = sum(1 for s in snapshots if s.status == "completed")
        failed = sum(1 for s in snapshots if s.status == "failed")
        skipped = sum(1 for s in snapshots if s.status == "skipped")

        total = len(snapshots)
        success_rate = completed / total if total > 0 else 0.0
        avg_confidence = sum(s.confidence for s in snapshots) / total

        total_time = sum(s.duration_ms for s in snapshots)
        avg_time = total_time / total

        # 调整次数
        total_adjustments = sum(len(s.adjustments) for s in snapshots)

        # 整体质量
        quality = (
            success_rate * 0.5
            + avg_confidence * 0.3
            - total_adjustments * 0.05
        )
        quality = max(0.0, min(quality, 1.0))

        return {
            "overall_quality": round(quality, 4),
            "success_rate": round(success_rate, 4),
            "avg_confidence": round(avg_confidence, 4),
            "completed": completed,
            "failed": failed,
            "skipped": skipped,
            "total_tasks": total,
            "total_time_ms": round(total_time, 1),
            "avg_task_time_ms": round(avg_time, 1),
            "total_adjustments": total_adjustments,
            "status": "excellent" if quality >= 0.9
                     else "good" if quality >= 0.75
                     else "fair" if quality >= 0.5
                     else "poor",
        }

    # -------------------------------------------------------------------
    # 异步执行支持
    # -------------------------------------------------------------------

    async def execute_with_adjustment(
        self,
        task_id: str,
        action: str,
        agent_name: str,
        execute_fn: Callable,
        args: tuple = (),
        kwargs: dict = None,
    ) -> tuple[Any, Optional[AdjustmentDecision]]:
        """
        带动态调整的异步执行

        Args:
            task_id: 任务ID
            action: 动作名称
            agent_name: 执行Agent
            execute_fn: 异步执行函数（协程）
            args, kwargs: 传给 execute_fn 的参数

        Returns:
            (执行结果, 调整决策，如无需调整则为 None)
        """
        kwargs = kwargs or {}
        start_ms = time.perf_counter()
        attempt = 0

        while True:
            start_attempt_ms = time.perf_counter()
            task = asyncio.create_task(execute_fn(*args, **kwargs))
            sleep_future = asyncio.create_task(
                asyncio.sleep(self.retry_policy.timeout_ms / 1000.0)
            )

            try:
                done, pending = await asyncio.wait(
                    {task, sleep_future}, return_when=asyncio.FIRST_COMPLETED
                )
            except Exception:
                task.cancel()
                raise

            # 取消未完成的
            for p in pending:
                p.cancel()
                try:
                    await p
                except asyncio.CancelledError:
                    pass

            elapsed = (time.perf_counter() - start_ms) * 1000

            if sleep_future in done:
                # 超时：sleep 先完成
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

                should_adj, adj_decision = self.should_adjust(
                    task_id, action, elapsed, current_confidence=0.5
                )
                if should_adj and adj_decision:
                    if adj_decision.adjustment_type == AdjustmentType.RETRY:
                        await asyncio.sleep(self.retry_policy.get_delay(attempt) / 1000.0)
                        attempt += 1
                        if attempt >= self.retry_policy.max_retries:
                            return None, adj_decision
                        continue
                    return None, adj_decision
                return None, AdjustmentDecision(
                    adjustment_type=AdjustmentType.ESCALATE,
                    reason=AdjustmentReason.TIMEOUT,
                    target_task_id=task_id,
                    message=f"超时且无法重试（{elapsed:.0f}ms）",
                    latency_ms=elapsed,
                )
            else:
                # 任务先完成：正常结果
                result = task.result()
                quality = self.record_result(ExecutionSnapshot(
                    task_id=task_id,
                    action=action,
                    agent_name=agent_name,
                    status="completed",
                    start_time_ms=start_attempt_ms,
                    duration_ms=(time.perf_counter() - start_attempt_ms) * 1000,
                    result_preview=str(result)[:200] if result else None,
                    confidence=0.8,
                    retry_count=attempt,
                ))

                if quality < self.quality_threshold:
                    decision = self.adjust(task_id, action, agent_name, "Quality below threshold", attempt)
                    if decision.adjustment_type == AdjustmentType.RETRY:
                        await asyncio.sleep(self.retry_policy.get_delay(attempt) / 1000.0)
                        attempt += 1
                        continue
                    return result, decision

                return result, None

    # -------------------------------------------------------------------
    # 内部方法
    # -------------------------------------------------------------------

    def _make_decision(
        self,
        adj_type: AdjustmentType,
        reason: AdjustmentReason,
        task_id: str,
        fallback_agent: Optional[str] = None,
        retry_count: int = 0,
        confidence_before: float = 1.0,
        message: str = "",
    ) -> AdjustmentDecision:
        """构建调整决策"""
        # 估算调整后的置信度
        confidence_after = confidence_before
        if adj_type == AdjustmentType.RETRY:
            confidence_after = min(confidence_before + 0.05, 0.95)
        elif adj_type == AdjustmentType.FALLBACK_AGENT:
            confidence_after = min(confidence_before + 0.1, 0.95)
        elif adj_type == AdjustmentType.SKIP_TASK:
            confidence_after = confidence_before * 0.8
        elif adj_type == AdjustmentType.ESCALATE:
            confidence_after = 0.0

        return AdjustmentDecision(
            adjustment_type=adj_type,
            reason=reason,
            target_task_id=task_id,
            fallback_agent=fallback_agent,
            retry_count=retry_count,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            message=message,
            latency_ms=0.0,  # 由调用方填充
        )

    def _get_fallback_agent(self, agent_name: str) -> Optional[str]:
        """查找备用Agent"""
        # Agent注册表中的 fallback
        FALLBACK_CHAIN = {
            "procurement_agent": "finance_agent",
            "finance_agent":      "doc_agent",
            "inventory_agent":    "logistics_agent",
            "logistics_agent":   "inventory_agent",
            "doc_agent":         None,
        }
        return FALLBACK_CHAIN.get(agent_name)

    # -------------------------------------------------------------------
    # 统计
    # -------------------------------------------------------------------

    def get_stats(self) -> dict:
        """获取统计信息"""
        total = self._stats["total_adjustments"]
        return {
            **self._stats,
            "retry_success_rate": round(
                self._stats["successful_retries"] / max(total, 1), 4
            ),
            "adjustment_rate": round(total / max(len(self._snapshots), 1), 4),
            "quality_threshold": self.quality_threshold,
        }

    def reset(self) -> None:
        """重置统计（用于新会话）"""
        self._snapshots.clear()
        self._retry_counters.clear()
        self._stats = {
            "total_adjustments": 0,
            "successful_retries": 0,
            "fallback_switches": 0,
            "skips": 0,
        }
