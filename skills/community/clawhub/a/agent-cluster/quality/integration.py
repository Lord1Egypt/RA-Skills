"""
Quality Integration - 与 Orchestrator 的集成桥接

此模块提供 Orchestrator 与 QualityReviewer 的集成方式：

1. 任务后置审查：Agent 执行完成后 → QualityReviewer 评分
2. 不达标自动重试：Orchestrator 调用 review_async 触发重试循环
3. 质量报告持久化：审查结果记录到审计日志

集成示例（见 Orchestrator.execute_task_flow）:

    from quality import QualityReviewer
    from quality.models import AgentResult, TaskContext

    reviewer = QualityReviewer()

    async def execute_with_quality(task_desc, context):
        # 1. 执行 Agent
        result = await agent.execute(task_desc, context)
        # 2. 质量审查
        review = await reviewer.review_async(
            result,
            TaskContext(task_id=result.task_id, intent_type=context.get('intent_type')),
            executor=agent.execute,   # 重试时重新调用
        )
        # 3. 返回结果
        if review.passed:
            return review.final_report.output
        elif review.escalated:
            return "【人工接管】质量多次不达标，需人工处理"
        else:
            return review.final_report.output  # 最后一次结果

可配置项（通过环境变量）：
    QUALITY_THRESHOLD=90          # 达标线
    QUALITY_MAX_ATTEMPTS=3        # 最大重试次数
    QUALITY_AUTO_RETRY=true        # 是否自动重试
    QUALITY_TIER=normal            # 质量等级 (normal/high/critical)
"""

from __future__ import annotations

import logging
import os
from typing import Any, Callable, Dict, Optional, TypeVar

from .gate import QualityGate, QualityTier
from .models import AgentResult, TaskContext
from .reviewer import QualityReviewer, ReviewResult
from .scorer import QualityScorer

logger = logging.getLogger(__name__)

T = TypeVar("T")

# =============================================================================
# 配置
# =============================================================================

QUALITY_THRESHOLD = float(os.getenv("QUALITY_THRESHOLD", "90"))
QUALITY_MAX_ATTEMPTS = int(os.getenv("QUALITY_MAX_ATTEMPTS", "3"))
QUALITY_AUTO_RETRY = os.getenv("QUALITY_AUTO_RETRY", "true").lower() == "true"
QUALITY_TIER_STR = os.getenv("QUALITY_TIER", "normal")


def create_quality_reviewer() -> QualityReviewer:
    """
    从环境变量创建 QualityReviewer 实例

    Returns:
        配置好的 QualityReviewer
    """
    tier = QualityTier.from_str(QUALITY_TIER_STR)
    gate = QualityGate(threshold=tier.threshold, tier=tier)
    scorer = QualityScorer()
    reviewer = QualityReviewer(
        scorer=scorer,
        gate=gate,
        max_attempts=QUALITY_MAX_ATTEMPTS,
        auto_retry=QUALITY_AUTO_RETRY,
    )
    logger.info(
        f"[QualityIntegration] QualityReviewer 创建 | "
        f"threshold={gate.threshold} | tier={tier.value} | "
        f"max_attempts={QUALITY_MAX_ATTEMPTS} | auto_retry={QUALITY_AUTO_RETRY}"
    )
    return reviewer


# =============================================================================
# 便捷封装
# =============================================================================

async def execute_with_quality_review(
    result: AgentResult,
    context: Optional[TaskContext],
    executor: Optional[Callable[..., T]] = None,
    tier: Optional[QualityTier] = None,
) -> ReviewResult:
    """
    执行质量审查的便捷封装

    Args:
        result:    Agent 执行结果
        context:   任务上下文
        executor:  重试时要调用的执行函数（异步）
        tier:      质量等级（覆盖默认配置）

    Returns:
        ReviewResult
    """
    reviewer = create_quality_reviewer()
    return await reviewer.review_async(
        result=result,
        context=context,
        executor=executor,
        tier=tier,
    )


def execute_with_quality_review_sync(
    result: AgentResult,
    context: Optional[TaskContext],
) -> ReviewResult:
    """
    同步版本的质量审查（不重试）

    适用于轻量级场景，或调用方自行控制重试逻辑。
    """
    reviewer = create_quality_reviewer()
    return reviewer.review(result, context)


# =============================================================================
# 集成钩子（供 Orchestrator 调用）
# =============================================================================

def build_task_context(
    task_id: str,
    intent_type: str,
    subtasks: list = None,
    required_tools: list = None,
    expected_outputs: list = None,
    quality_tier: str = None,
) -> TaskContext:
    """
    从 Orchestrator 的任务信息构建 TaskContext

    方便在 Orchestrator 的各个执行节点直接调用。
    """
    tier = quality_tier or QUALITY_TIER_STR
    return TaskContext(
        task_id=task_id,
        intent_type=intent_type,
        subtasks=subtasks or [],
        required_tools=required_tools or [],
        expected_outputs=expected_outputs or [],
        quality_tier=tier,
    )
