"""
QualityReviewer - 质量审查Agent

质量审查的顶层 Agent，封装 QualityScorer + QualityGate + RetryLoop。
作为 orchestrator 的质量审查入口，对每一次 Agent 执行结果进行：
1. 5维度评分（QualityScorer）
2. 达标判断（QualityGate，90分达标）
3. 不达标时触发重试（RetryLoop，最多3次）
4. 返回最终结果（ReviewResult）

集成到 Orchestrator 的执行流程：
    Orchestrator.execute()
        → Agent 执行
        → QualityReviewer.review(result)   ← 质量审查
            → QualityScorer.score()          5维度评分
            → QualityGate.evaluate()         达标判断
            → (不达标) RetryLoop.run()       自动重试
        → 返回 ReviewResult
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, TypeVar

from .gate import GateDecision, QualityGate, QualityTier
from .models import AgentResult, QualityReport, RetryStrategy, TaskContext
from .retry_loop import QualityRetryLoop
from .scorer import QualityScorer

logger = logging.getLogger(__name__)

T = TypeVar("T")


# =============================================================================
# 审查结果
# =============================================================================

@dataclass
class ReviewResult:
    """
    质量审查最终结果

    Attributes:
        task_id:         任务ID
        final_report:    最终通过的质量报告（最后一次评分）
        all_reports:     历次评分报告（用于分析改进轨迹）
        decision:        最终门禁判定
        attempts:        总尝试次数
        passed:          最终是否达标
        escalated:       是否升级人工处理
        review_at:       审查完成时间
        duration_ms:     整个审查流程耗时
    """

    task_id: str
    final_report: QualityReport
    all_reports: List[QualityReport] = field(default_factory=list)
    decision: Optional[GateDecision] = None
    attempts: int = 1
    passed: bool = False
    escalated: bool = False
    review_at: str = field(default_factory=lambda: datetime.now().isoformat())
    duration_ms: float = 0.0

    def summary(self) -> str:
        """生成审查摘要"""
        lines = [
            f"【质量审查结果 #{self.task_id[:8]}】",
            f"最终得分: {self.final_report.overall:.1f} / 90",
            f"{'✅ 达标' if self.passed else '❌ 未达标'}",
            f"尝试次数: {self.attempts}次",
            "",
        ]
        if self.all_reports:
            score_trail = " → ".join(
                f"{r.overall:.1f}" for r in self.all_reports
            )
            lines.append(f"得分轨迹: {score_trail}")
        if self.escalated:
            lines.append("⚠️ 已升级人工处理")
        if self.decision and self.decision.suggestions:
            lines.append("改进建议:")
            for s in self.decision.suggestions[:5]:
                lines.append(f"  → {s}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "final_overall": self.final_report.overall,
            "passed": self.passed,
            "attempts": self.attempts,
            "escalated": self.escalated,
            "review_at": self.review_at,
            "duration_ms": round(self.duration_ms, 2),
            "final_report": self.final_report.to_dict(),
            "all_reports": [r.to_dict() for r in self.all_reports],
            "decision": self.decision.to_dict() if self.decision else None,
        }


# =============================================================================
# 质量审查Agent
# =============================================================================

class QualityReviewer:
    """
    质量审查Agent

    封装 评分器 + 门禁 + 重试循环，提供一站式的质量审查能力。

    使用示例:

        reviewer = QualityReviewer()

        # 同步审查（单次）
        result = reviewer.review(agent_result)
        if result.passed:
            return result.final_report.output
        else:
            return f"质量不达标: {result.decision.suggestions}"

        # 异步审查（支持重试）
        result = await reviewer.review_async(
            agent_result,
            task_context,
            executor=my_agent_executor,  # 传入重试时要调用的执行函数
        )
    """

    DEFAULT_MAX_ATTEMPTS = 3
    DEFAULT_THRESHOLD = 90.0

    def __init__(
        self,
        scorer: Optional[QualityScorer] = None,
        gate: Optional[QualityGate] = None,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        auto_retry: bool = True,
    ):
        """
        初始化质量审查Agent

        Args:
            scorer:      质量评分器（默认新建）
            gate:        质量门禁（默认新建，90分达标）
            max_attempts: 最大重试次数（默认3次）
            auto_retry:  不达标时是否自动重试（默认True）
        """
        self._scorer = scorer or QualityScorer()
        self._gate = gate or QualityGate(threshold=self.DEFAULT_THRESHOLD)
        self._max_attempts = max_attempts
        self._auto_retry = auto_retry

        logger.info(
            f"[QualityReviewer] 初始化 | threshold={self._gate.threshold} | "
            f"max_attempts={max_attempts} | auto_retry={auto_retry}"
        )

    @property
    def gate(self) -> QualityGate:
        """获取质量门禁（可访问统计信息）"""
        return self._gate

    @property
    def scorer(self) -> QualityScorer:
        """获取评分器"""
        return self._scorer

    def review(
        self,
        result: AgentResult,
        context: Optional[TaskContext] = None,
        tier: Optional[QualityTier] = None,
    ) -> ReviewResult:
        """
        同步质量审查（单次评分，不含重试）

        适用于：轻量级场景，或由调用方控制重试逻辑。

        Args:
            result:   Agent 执行结果
            context:  任务上下文
            tier:     质量等级（覆盖 gate 默认值）

        Returns:
            ReviewResult
        """
        import time
        start = time.perf_counter()

        # 动态调整门禁等级
        gate = self._gate
        if tier:
            gate = QualityGate(threshold=tier.threshold, tier=tier)

        # 评分
        report = self._scorer.score(result, context)

        # 判定
        decision = gate.evaluate(report)

        duration_ms = (time.perf_counter() - start) * 1000

        return ReviewResult(
            task_id=result.task_id,
            final_report=report,
            all_reports=[report],
            decision=decision,
            attempts=1,
            passed=decision.passed,
            escalated=False,
            duration_ms=duration_ms,
        )

    async def review_async(
        self,
        result: AgentResult,
        context: Optional[TaskContext] = None,
        executor: Optional[Callable[..., T]] = None,
        executor_args: Optional[List[Any]] = None,
        executor_kwargs: Optional[Dict[str, Any]] = None,
        tier: Optional[QualityTier] = None,
    ) -> ReviewResult:
        """
        异步质量审查（支持自动重试）

        当 QualityGate 判断不达标时，自动触发重试：
        1. 根据失败维度选择重试策略
        2. 调整提示词（REFINED_PROMPT）或切换引擎（CHANGE_ENGINE）
        3. 重新执行并评分
        4. 重复直到达标或达到最大重试次数

        Args:
            result:           Agent 执行结果（初次）
            context:          任务上下文
            executor:         重试时要调用的执行函数
                              签名: async def execute(task: str, context: dict) -> AgentResult
            executor_args:    executor 的位置参数
            executor_kwargs:  executor 的关键字参数
            tier:             质量等级

        Returns:
            ReviewResult: 包含所有尝试的最终结果
        """
        import time
        start = time.perf_counter()

        gate = self._gate
        if tier:
            gate = QualityGate(threshold=tier.threshold, tier=tier)

        all_reports: List[QualityReport] = []
        current_result = result
        retry_loop = QualityRetryLoop(
            scorer=self._scorer,
            gate=gate,
            max_attempts=self._max_attempts,
        )

        # 第一次评分（当前结果）
        report = self._scorer.score(current_result, context)
        all_reports.append(report)
        decision = gate.evaluate(report)

        logger.info(
            f"[QualityReviewer] 第1次评分 | score={report.overall:.1f} | "
            f"passed={decision.passed} | failed_dims={len(decision.failed_dims)}"
        )

        # 已达标 → 直接返回
        if decision.passed:
            return ReviewResult(
                task_id=result.task_id,
                final_report=report,
                all_reports=all_reports,
                decision=decision,
                attempts=1,
                passed=True,
                escalated=False,
                duration_ms=(time.perf_counter() - start) * 1000,
            )

        # 不达标 → 进入重试循环
        if not self._auto_retry:
            return ReviewResult(
                task_id=result.task_id,
                final_report=report,
                all_reports=all_reports,
                decision=decision,
                attempts=1,
                passed=False,
                escalated=False,
                duration_ms=(time.perf_counter() - start) * 1000,
            )

        # 执行重试
        retry_result = await retry_loop.run(
            initial_result=current_result,
            initial_context=context,
            executor=executor,
            executor_args=executor_args or [],
            executor_kwargs=executor_kwargs or {},
        )

        all_reports.extend(retry_result.all_reports)

        # 取最后一次评分
        final_report = retry_result.final_report
        final_decision = gate.evaluate(final_report)

        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            f"[QualityReviewer] 审查完成 | task_id={result.task_id} | "
            f"attempts={retry_result.attempts} | final_score={final_report.overall:.1f} | "
            f"passed={final_decision.passed} | escalated={retry_result.escalated}"
        )

        return ReviewResult(
            task_id=result.task_id,
            final_report=final_report,
            all_reports=all_reports,
            decision=final_decision,
            attempts=retry_result.attempts,
            passed=final_decision.passed,
            escalated=retry_result.escalated,
            duration_ms=duration_ms,
        )

    def review_batch(
        self,
        results: List[AgentResult],
        contexts: Optional[List[Optional[TaskContext]]] = None,
    ) -> List[ReviewResult]:
        """
        批量质量审查

        Args:
            results:   Agent 执行结果列表
            contexts:  对应的上下文列表（与 results 一一对应）

        Returns:
            审查结果列表
        """
        if contexts is None:
            contexts = [None] * len(results)

        return [
            self.review(result, ctx)
            for result, ctx in zip(results, contexts)
        ]

    def get_stats(self) -> Dict[str, Any]:
        """获取审查统计"""
        gate_stats = self._gate.get_stats()
        return {
            "max_attempts": self._max_attempts,
            "auto_retry": self._auto_retry,
            "gate_stats": gate_stats,
        }
