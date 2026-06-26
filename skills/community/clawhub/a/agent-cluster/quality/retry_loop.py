"""
QualityRetryLoop - 质量重试循环

当质量不达标时，自动触发重试机制：
1. 分析失败原因（基于 QualityReport 的 failed_dimensions）
2. 选择重试策略（REFINED_PROMPT / CHANGE_ENGINE / ADD_CONSTRAINTS / SPLIT_TASK）
3. 调整任务或上下文，调用 executor 重新执行
4. 重新评分，重复直到达标或达到最大重试次数
5. 超过最大重试次数仍不达标 → 升级人工处理（ESCALATE）

每次重试的策略调整规则：
- 完整性差 → 精化提示词（补充子任务描述）
- 准确性差 → 切换执行引擎
- 相关性差 → 精化提示词（重写任务目标）
- 时效性差 → 拆解任务分步执行
- 可用性差 → 精化提示词（指定输出格式）
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar

from .gate import QualityGate, QualityTier
from .models import AgentResult, QualityDimension, QualityReport, QualityScore, RetryStrategy, TaskContext
from .scorer import QualityScorer

logger = logging.getLogger(__name__)

T = TypeVar("T")


# =============================================================================
# 策略调整器
# =============================================================================

class StrategyAdjuster:
    """
    根据失败原因调整任务参数

    每次重试时，根据 QualityReport 的失败维度，
    调整 task_description / context / engine 等参数，
    供下一次执行使用。
    """

    def adjust(
        self,
        original_result: AgentResult,
        original_context: Optional[TaskContext],
        report: QualityReport,
        attempt: int,
        suggested_strategies: List[RetryStrategy],
    ) -> tuple[Optional[str], Optional[TaskContext], Optional[str]]:
        """
        调整任务参数

        Args:
            original_result:   原始执行结果
            original_context:  原始上下文
            report:            当前评分报告
            attempt:           当前尝试次数（1-based）
            suggested_strategies: 推荐的重试策略

        Returns:
            (new_task_description, new_context, new_engine)
            任何元素为 None 表示保持原值不变
        """
        new_description: Optional[str] = None
        new_context: Optional[TaskContext] = None
        new_engine: Optional[str] = None

        # 根据策略调整
        for strategy in suggested_strategies:
            if strategy == RetryStrategy.REFINED_PROMPT:
                new_description = self._refine_prompt(
                    original_result, report, attempt
                )
            elif strategy == RetryStrategy.CHANGE_ENGINE:
                new_engine = self._suggest_engine(original_result)
            elif strategy == RetryStrategy.ADD_CONSTRAINTS:
                new_context = self._add_constraints(original_context, report)
            elif strategy == RetryStrategy.SPLIT_TASK:
                # 拆分任务不改变描述，而是标记拆分
                new_context = self._mark_split(original_context)
            elif strategy == RetryStrategy.ESCALATE:
                logger.warning(
                    f"[StrategyAdjuster] 建议升级人工处理 | "
                    f"task_id={original_result.task_id}"
                )

        return new_description, new_context, new_engine

    def _refine_prompt(
        self,
        result: AgentResult,
        report: QualityReport,
        attempt: int,
    ) -> str:
        """
        精化提示词

        策略：
        - 第2次重试：在原描述基础上强调薄弱维度
        - 第3次重试：给出更具体的格式/范围约束
        """
        failed_labels = [d.label for d in report.failed_dimensions]
        failed_str = "、".join(failed_labels)

        base = result.task_description

        if attempt == 1:
            # 第一次重试：指出不足
            refinement = (
                f"\n\n【质量要求】请注意以下维度需要改进：{failed_str}。"
                f"当前评分偏低，请更加注重{'和'.join(failed_labels[:2])}。"
            )
        else:
            # 第二次重试：更严格的约束
            constraints = self._build_constraints(report)
            refinement = (
                f"\n\n【强制要求】"
                f"必须涵盖以下方面：{failed_str}。"
                f"输出格式要求：{constraints}"
            )

        return base + refinement

    def _build_constraints(self, report: QualityReport) -> str:
        """为每个失败维度构建约束条件"""
        constraints: List[str] = []

        if QualityDimension.COMPLETENESS in report.failed_dimensions:
            constraints.append("明确列出所有子任务及其结果")
        if QualityDimension.ACCURACY in report.failed_dimensions:
            constraints.append("每个结论必须给出数据来源或推理依据")
        if QualityDimension.RELEVANCE in report.failed_dimensions:
            constraints.append("内容必须直接回答问题，避免跑题")
        if QualityDimension.USABILITY in report.failed_dimensions:
            constraints.append(
                "使用结构化格式（JSON/表格/列表）输出，便于程序解析"
            )
        if QualityDimension.TIMELINESS in report.failed_dimensions:
            constraints.append("优先给出核心结论，详细数据按需提供")

        return "；".join(constraints) if constraints else "结构清晰、重点突出"

    def _suggest_engine(self, result: AgentResult) -> Optional[str]:
        """
        推荐执行引擎

        策略：切换到不同的引擎以获取不同能力
        """
        engine_map = {
            "claude_ma": "deepseek",
            "deepseek": "local",
            "local": "claude_ma",
            "gpt6": "claude_ma",
        }
        return engine_map.get(result.engine.lower(), "claude_ma")

    def _add_constraints(
        self,
        context: Optional[TaskContext],
        report: QualityReport,
    ) -> TaskContext:
        """添加约束条件到上下文"""
        if context is None:
            context = TaskContext(task_id=report.task_id)

        # 添加必需字段要求
        if QualityDimension.COMPLETENESS in report.failed_dimensions:
            required = context.expected_outputs or []
            required.extend(["summary", "conclusion", "next_steps"])
            context.expected_outputs = list(set(required))

        # 提高质量等级
        if not context.quality_tier or context.quality_tier == "normal":
            context.quality_tier = "high"

        return context

    def _mark_split(self, context: Optional[TaskContext]) -> TaskContext:
        """标记任务需要拆分"""
        if context is None:
            context = TaskContext(task_id="")
        # 标记拆分（后续 executor 可根据此标记执行拆分逻辑）
        context = TaskContext(
            task_id=context.task_id,
            intent_type=context.intent_type,
            user_role=context.user_role,
            expected_outputs=context.expected_outputs,
            required_tools=context.required_tools,
            subtasks=context.subtasks,
            deadline=context.deadline,
            quality_tier=context.quality_tier,
        )
        # 使用特殊标记
        context.context["_split_task"] = True
        return context


# =============================================================================
# 重试结果
# =============================================================================

@dataclass
class RetryLoopResult:
    """
    重试循环最终结果

    Attributes:
        final_report:   最终评分报告
        all_reports:    历次评分报告
        attempts:        总尝试次数
        final_output:   最终输出（从 final_report 提取）
        improved:        是否比首次有改进
        score_delta:    与首次的分数差
        escalated:      是否升级人工处理
    """

    final_report: QualityReport
    all_reports: List[QualityReport] = field(default_factory=list)
    attempts: int = 1
    final_output: Any = None
    improved: bool = False
    score_delta: float = 0.0
    escalated: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "final_overall": self.final_report.overall,
            "attempts": self.attempts,
            "improved": self.improved,
            "score_delta": round(self.score_delta, 2),
            "escalated": self.escalated,
            "all_reports": [r.to_dict() for r in self.all_reports],
        }


# =============================================================================
# 重试循环
# =============================================================================

class QualityRetryLoop:
    """
    质量重试循环

    核心逻辑：
    1. 评估当前报告（已在 QualityReviewer 中完成）
    2. 根据失败维度选择重试策略
    3. 调整任务参数
    4. 调用 executor 重新执行
    5. 重新评分
    6. 重复直到达标或达到 max_attempts

    设计要点：
    - executor 可以是同步或异步函数
    - 支持同时调整提示词、上下文、引擎
    - 记录完整的改进轨迹（all_reports）
    - 超时保护（单次重试最大等待时间）
    """

    DEFAULT_TIMEOUT_SECONDS = 60.0

    def __init__(
        self,
        scorer: QualityScorer,
        gate: QualityGate,
        max_attempts: int = 3,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    ):
        """
        初始化重试循环

        Args:
            scorer:          质量评分器
            gate:           质量门禁
            max_attempts:   最大重试次数（含首次，最大3次）
            timeout_seconds: 单次重试超时时间
        """
        self._scorer = scorer
        self._gate = gate
        self._max_attempts = max(1, min(max_attempts, 3))
        self._timeout = timeout_seconds
        self._adjuster = StrategyAdjuster()

        logger.info(
            f"[QualityRetryLoop] 初始化 | max_attempts={self._max_attempts} | "
            f"threshold={gate.threshold} | timeout={timeout_seconds}s"
        )

    async def run(
        self,
        initial_result: AgentResult,
        initial_context: Optional[TaskContext],
        executor: Optional[Callable[..., T]] = None,
        executor_args: Optional[List[Any]] = None,
        executor_kwargs: Optional[Dict[str, Any]] = None,
    ) -> RetryLoopResult:
        """
        执行重试循环

        Args:
            initial_result:    首次执行结果
            initial_context:   首次执行上下文
            executor:          重试时要调用的执行函数
                               async def execute(task: str, context: dict) -> AgentResult
            executor_args:     executor 的位置参数
            executor_kwargs:   executor 的关键字参数

        Returns:
            RetryLoopResult
        """
        all_reports: List[QualityReport] = []
        current_result = initial_result
        current_context = initial_context
        first_score = initial_result  # 占位，后续填充

        # 如果 initial_result 已经有评分（传入的是报告而非原始结果）
        # 则直接用它作为第一次评分
        if isinstance(initial_result, QualityReport):
            all_reports.append(initial_result)
            first_score = initial_result.overall
            # 没有 executor，无法重试
            return RetryLoopResult(
                final_report=initial_result,
                all_reports=all_reports,
                attempts=1,
                final_output=initial_result.metadata.get("output"),
                improved=False,
                score_delta=0.0,
                escalated=False,
            )

        first_score = 0.0  # 初始分，后面填充

        # 若无 executor，只评分不重试
        if executor is None:
            report = self._scorer.score(current_result, current_context)
            all_reports.append(report)
            return RetryLoopResult(
                final_report=report,
                all_reports=all_reports,
                attempts=1,
                final_output=current_result.output,
                improved=False,
                score_delta=0.0,
                escalated=False,
            )

        args = executor_args or []
        kwargs = executor_kwargs or {}

        for attempt in range(1, self._max_attempts + 1):
            logger.info(
                f"[QualityRetryLoop] 重试 #{attempt} | task_id={current_result.task_id}"
            )

            # 评分
            report = self._scorer.score(current_result, current_context)
            if attempt == 1:
                first_score = report.overall
            all_reports.append(report)

            # 达标 → 退出
            decision = self._gate.evaluate(report)
            if decision.passed:
                logger.info(
                    f"[QualityRetryLoop] 达标！score={report.overall:.1f} | "
                    f"attempts={attempt}"
                )
                return RetryLoopResult(
                    final_report=report,
                    all_reports=all_reports,
                    attempts=attempt,
                    final_output=current_result.output,
                    improved=attempt > 1,
                    score_delta=report.overall - first_score,
                    escalated=False,
                )

            # 未达标，但已达到最大次数
            if attempt >= self._max_attempts:
                logger.warning(
                    f"[QualityRetryLoop] 达到最大重试次数({self._max_attempts})仍未达标 | "
                    f"task_id={current_result.task_id} | final_score={report.overall:.1f}"
                )
                return RetryLoopResult(
                    final_report=report,
                    all_reports=all_reports,
                    attempts=attempt,
                    final_output=current_result.output,
                    improved=attempt > 1,
                    score_delta=report.overall - first_score,
                    escalated=True,
                )

            # 策略调整
            strategies = self._gate.get_retry_strategy(report, attempt)
            logger.info(
                f"[QualityRetryLoop] 策略建议: {[s.value for s in strategies]} | "
                f"failed_dims={[d.value for d in report.failed_dimensions]}"
            )

            new_desc, new_ctx, new_engine = self._adjuster.adjust(
                current_result, current_context, report, attempt, strategies
            )

            # 准备重试参数
            retry_kwargs = {**kwargs}

            if new_desc is not None:
                retry_kwargs["task"] = new_desc

            if new_engine is not None:
                retry_kwargs["engine"] = new_engine

            # 调用 executor 重新执行
            try:
                current_result = await asyncio.wait_for(
                    executor(*args, **retry_kwargs),
                    timeout=self._timeout,
                )
                # 更新 context
                if new_ctx is not None:
                    current_context = new_ctx

                logger.info(
                    f"[QualityRetryLoop] 重试 #{attempt+1} 执行完成 | "
                    f"engine={current_result.engine}"
                )

            except asyncio.TimeoutError:
                logger.error(
                    f"[QualityRetryLoop] 重试 #{attempt+1} 超时({self._timeout}s)"
                )
                # 超时也继续下次尝试，不中断
                current_result = AgentResult(
                    task_id=current_result.task_id + "_timeout",
                    task_description=current_result.task_description,
                    output=None,
                    success=False,
                    error=f"重试 #{attempt+1} 执行超时",
                )

            except Exception as e:
                logger.error(
                    f"[QualityRetryLoop] 重试 #{attempt+1} 执行异常: {e}"
                )
                current_result = AgentResult(
                    task_id=current_result.task_id + "_error",
                    task_description=current_result.task_description,
                    output=None,
                    success=False,
                    error=str(e),
                )

        # 兜底（理论上不会到达这里）
        return RetryLoopResult(
            final_report=all_reports[-1],
            all_reports=all_reports,
            attempts=self._max_attempts,
            final_output=all_reports[-1].metadata.get("output"),
            improved=True,
            score_delta=all_reports[-1].overall - first_score,
            escalated=True,
        )

    def run_sync(
        self,
        initial_result: AgentResult,
        initial_context: Optional[TaskContext],
        executor: Optional[Callable[..., T]] = None,
        executor_args: Optional[List[Any]] = None,
        executor_kwargs: Optional[Dict[str, Any]] = None,
    ) -> RetryLoopResult:
        """同步版本的重试循环（包装 async run）"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已经在事件循环中，创建新任务
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(
                        asyncio.run,
                        self.run(
                            initial_result,
                            initial_context,
                            executor,
                            executor_args,
                            executor_kwargs,
                        ),
                    )
                    return future.result()
            else:
                return loop.run_until_complete(
                    self.run(
                        initial_result,
                        initial_context,
                        executor,
                        executor_args,
                        executor_kwargs,
                    )
                )
        except RuntimeError:
            # 没有事件循环，直接创建
            return asyncio.run(
                self.run(
                    initial_result,
                    initial_context,
                    executor,
                    executor_args,
                    executor_kwargs,
                )
            )
