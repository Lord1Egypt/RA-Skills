"""
QualityGate - 质量门禁

对标 QClaw 90分达标机制：
1. 判断任务是否达标（≥90分）
2. 针对未达标维度生成改进建议
3. 支持质量等级分层（normal/high/critical）
4. 记录门禁判定历史
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .models import QualityDimension, QualityReport, QualityScore, RetryStrategy

logger = logging.getLogger(__name__)


# =============================================================================
# 质量等级
# =============================================================================

class QualityTier(Enum):
    """
    质量等级（决定达标阈值）

    - normal:   标准质量（默认，90分达标）
    - high:     高质量（95分达标）
    - critical: 关键质量（98分达标）
    """

    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def threshold(self) -> float:
        thresholds = {
            QualityTier.NORMAL: 90.0,
            QualityTier.HIGH: 95.0,
            QualityTier.CRITICAL: 98.0,
        }
        return thresholds[self]

    @classmethod
    def from_str(cls, s: str) -> "QualityTier":
        mapping = {"normal": cls.NORMAL, "high": cls.HIGH, "critical": cls.CRITICAL}
        return mapping.get(s.lower(), cls.NORMAL)


# =============================================================================
# 改进建议生成器
# =============================================================================

class ImprovementSuggester:
    """
    基于评分报告生成改进建议

    策略：
    - 针对每个未达标维度生成具体建议
    - 按影响程度（权重）排序
    - 提供可操作的行动建议
    """

    # 维度 → 通用改进策略
    STRATEGY_MAP: Dict[QualityDimension, List[str]] = {
        QualityDimension.COMPLETENESS: [
            "补充遗漏的子任务，确保所有需求都被覆盖",
            "增加工具调用以完成缺失的功能模块",
            "检查输出字段列表，补全必需字段",
        ],
        QualityDimension.ACCURACY: [
            "使用 RAG 或知识库检索验证数据准确性",
            "添加数据来源标注，便于核查",
            "避免模糊表述，给出确定性结论",
        ],
        QualityDimension.RELEVANCE: [
            "重新阅读用户问题，确保输出紧扣核心诉求",
            "过滤题外内容，聚焦任务目标",
            "使用任务关键词作为输出框架",
        ],
        QualityDimension.TIMELINESS: [
            "拆分长任务为多个子任务并行执行",
            "启用缓存机制，避免重复计算",
            "优化查询路径，减少不必要的工具调用",
        ],
        QualityDimension.USABILITY: [
            "采用结构化格式输出（JSON/表格/列表）",
            "将结论前置，提供清晰的摘要段落",
            "添加使用说明或下一步行动建议",
        ],
    }

    @classmethod
    def suggest(cls, report: QualityReport) -> List[str]:
        """
        生成改进建议

        Args:
            report: 质量评分报告

        Returns:
            按优先级排序的改进建议列表
        """
        suggestions: List[tuple[float, str]] = []  # (priority_weight, suggestion)

        for dim, score in report.scores.items():
            if score.is_pass:
                continue

            # 分数越低，权重越高
            deficit = ScoreBounds.PASS - score.score
            priority_weight = deficit  # 缺口越大，优先级越高

            # 添加维度特定建议
            for sug in cls.STRATEGY_MAP.get(dim, []):
                suggestions.append((priority_weight, sug))

            # 添加该维度的自定义建议
            for sug in score.suggestions:
                suggestions.append((priority_weight * 0.8, sug))

        # 按优先级降序排列
        suggestions.sort(key=lambda x: -x[0])
        # 去重
        seen, unique = set(), []
        for _, sug in suggestions:
            if sug not in seen:
                seen.add(sug)
                unique.append(sug)

        return unique[: 10]  # 最多返回10条


# =============================================================================
# 质量门禁
# =============================================================================

@dataclass
class GateDecision:
    """
    质量门禁判定结果

    Attributes:
        passed:         是否达标
        overall:        综合得分
        threshold:      达标线
        gap:            与达标的差距
        tier:           本次判定使用的质量等级
        suggestions:    改进建议
        failed_dims:    未达标维度
        record_at:      判定时间
    """

    passed: bool
    overall: float
    threshold: float
    gap: float
    tier: QualityTier
    suggestions: List[str]
    failed_dims: List[QualityDimension]
    record_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "overall": self.overall,
            "threshold": self.threshold,
            "gap": round(self.gap, 2),
            "tier": self.tier.value,
            "suggestions": self.suggestions,
            "failed_dimensions": [d.value for d in self.failed_dims],
            "record_at": self.record_at,
        }


@dataclass
class GateHistoryEntry:
    """门禁判定历史记录"""

    task_id: str
    report_id: str
    decision: GateDecision
    attempt: int = 1


class QualityGate:
    """
    质量门禁

    对标 QClaw 90分达标标准：
    - 综合得分 ≥ 90 → 达标，放行
    - 综合得分 < 90 → 不达标，触发改进建议 + 重试流程

    设计要点：
    1. 支持 QualityTier 分层（normal/high/critical）
    2. 记录判定历史（可追溯）
    3. 提供可解释的改进建议
    4. 可集成到 orchestrator 执行流程
    """

    DEFAULT_THRESHOLD = 90.0

    def __init__(
        self,
        threshold: float = DEFAULT_THRESHOLD,
        tier: QualityTier = QualityTier.NORMAL,
        record_history: bool = True,
    ):
        """
        初始化质量门禁

        Args:
            threshold:     达标线（默认90分）
            tier:          质量等级（决定 threshold 取值）
            record_history: 是否记录判定历史
        """
        self._threshold = tier.threshold if tier != QualityTier.NORMAL else threshold
        self._tier = tier
        self._record_history = record_history
        self._history: List[GateHistoryEntry] = []

        logger.info(
            f"[QualityGate] 初始化 | threshold={self._threshold} | "
            f"tier={tier.value} | record_history={record_history}"
        )

    @property
    def threshold(self) -> float:
        """当前达标线"""
        return self._threshold

    @property
    def tier(self) -> QualityTier:
        """当前质量等级"""
        return self._tier

    @property
    def history(self) -> List[GateHistoryEntry]:
        """判定历史"""
        return self._history.copy()

    def evaluate(self, report: QualityReport) -> GateDecision:
        """
        评估质量报告是否达标

        Args:
            report: 质量评分报告

        Returns:
            GateDecision: 门禁判定结果
        """
        passed = report.overall >= self._threshold
        gap = max(0.0, self._threshold - report.overall)
        suggestions = ImprovementSuggester.suggest(report) if not passed else []
        failed_dims = report.failed_dimensions

        decision = GateDecision(
            passed=passed,
            overall=report.overall,
            threshold=self._threshold,
            gap=gap,
            tier=self._tier,
            suggestions=suggestions,
            failed_dims=failed_dims,
        )

        if self._record_history:
            self._history.append(
                GateHistoryEntry(
                    task_id=report.task_id,
                    report_id=report.report_id,
                    decision=decision,
                )
            )

        status = "✅ 达标" if passed else "❌ 未达标"
        logger.info(
            f"[QualityGate] 判定 | task_id={report.task_id} | "
            f"score={report.overall:.1f}/{self._threshold} | {status} | "
            f"failed={len(failed_dims)}维"
        )

        return decision

    def suggest_improvements(self, report: QualityReport) -> List[str]:
        """
        针对低分维度给出改进建议（便捷方法）

        Args:
            report: 质量评分报告

        Returns:
            改进建议列表
        """
        return ImprovementSuggester.suggest(report)

    def get_retry_strategy(
        self,
        report: QualityReport,
        attempt: int,
    ) -> List[RetryStrategy]:
        """
        根据评分报告和当前尝试次数，推荐重试策略

        Args:
            report:   质量评分报告
            attempt:  当前重试次数（1-based）

        Returns:
            推荐的重试策略列表（按优先级排序）
        """
        strategies: List[RetryStrategy] = []
        failed_by_dim = {d: report.scores[d].score for d in report.failed_dimensions}

        # 完整性差 → 精化提示词 + 补充约束
        if QualityDimension.COMPLETENESS in failed_by_dim:
            strategies.extend([
                RetryStrategy.REFINED_PROMPT,
                RetryStrategy.ADD_CONSTRAINTS,
            ])

        # 相关性差 → 精化提示词（重写任务描述）
        if QualityDimension.RELEVANCE in failed_by_dim:
            strategies.append(RetryStrategy.REFINED_PROMPT)

        # 准确性差 → 知识库增强或换引擎
        if QualityDimension.ACCURACY in failed_by_dim:
            strategies.extend([
                RetryStrategy.REFINED_PROMPT,
                RetryStrategy.CHANGE_ENGINE,
            ])

        # 时效性差 → 拆分任务
        if QualityDimension.TIMELINESS in failed_by_dim:
            strategies.append(RetryStrategy.SPLIT_TASK)

        # 可用性差 → 精化提示词（指定格式）
        if QualityDimension.USABILITY in failed_by_dim:
            strategies.append(RetryStrategy.REFINED_PROMPT)

        # 多次重试后仍失败 → 升级人工处理
        if attempt >= 2 and not strategies:
            strategies.append(RetryStrategy.ESCALATE)

        return strategies[:3]  # 最多返回3个策略

    def get_stats(self) -> Dict[str, Any]:
        """获取门禁统计信息"""
        if not self._history:
            return {"total": 0, "passed": 0, "failed": 0, "pass_rate": 0.0}

        total = len(self._history)
        passed = sum(1 for e in self._history if e.decision.passed)
        failed = total - passed

        avg_score = sum(e.decision.overall for e in self._history) / total
        avg_gap = sum(e.decision.gap for e in self._history if not e.decision.passed)
        failed_count = max(1, failed)
        avg_gap = avg_gap / failed_count

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / total * 100, 2),
            "avg_score": round(avg_score, 2),
            "avg_gap_when_failed": round(avg_gap, 2),
            "threshold": self._threshold,
            "tier": self._tier.value,
        }


# 导入 ScoreBounds（来自 models 或重新定义）
from .scorer import ScoreBounds
