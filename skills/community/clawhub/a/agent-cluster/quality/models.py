"""
Quality Models - 质量评分数据模型

定义质量评分所需的全部数据结构，与 QClaw 5维评分体系对齐。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# =============================================================================
# 枚举定义
# =============================================================================

class QualityDimension(Enum):
    """
    5个质量评分维度

    对标 QClaw 质量评分体系：
    - completeness: 完整性（是否完成所有要求）
    - accuracy:    准确性（结果是否正确）
    - relevance:  相关性（是否切题）
    - timeliness:  时效性（是否按时完成）
    - usability:  可用性（结果是否可直接使用）
    """

    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    TIMELINESS = "timeliness"
    USABILITY = "usability"

    @property
    def label(self) -> str:
        """中文标签"""
        labels = {
            QualityDimension.COMPLETENESS: "完整性",
            QualityDimension.ACCURACY: "准确性",
            QualityDimension.RELEVANCE: "相关性",
            QualityDimension.TIMELINESS: "时效性",
            QualityDimension.USABILITY: "可用性",
        }
        return labels[self]

    @property
    def description(self) -> str:
        """评分说明"""
        descs = {
            QualityDimension.COMPLETENESS: "是否覆盖所有子任务、满足全部约束条件",
            QualityDimension.ACCURACY: "结果数值/逻辑是否正确，有无误判或幻觉",
            QualityDimension.RELEVANCE: "输出内容是否紧扣用户需求，切中要害",
            QualityDimension.TIMELINESS: "是否在约定时间内完成，是否有延迟",
            QualityDimension.USABILITY: "结果格式是否规范，可直接使用或落地",
        }
        return descs[self]

    @property
    def weight(self) -> float:
        """
        维度权重（可按场景调整）

        默认权重：完整性和准确性权重最高（25%），其余各20%
        """
        weights = {
            QualityDimension.COMPLETENESS: 0.25,
            QualityDimension.ACCURACY: 0.25,
            QualityDimension.RELEVANCE: 0.20,
            QualityDimension.TIMELINESS: 0.15,
            QualityDimension.USABILITY: 0.15,
        }
        return weights[self]


class RetryStrategy(Enum):
    """
    质量不达标时的重试策略调整方式
    """

    REFINED_PROMPT = "refined_prompt"    # 精化提示词（默认）
    CHANGE_ENGINE = "change_engine"      # 切换执行引擎
    ADD_CONSTRAINTS = "add_constraints"   # 添加更多约束条件
    SPLIT_TASK = "split_task"            # 拆解任务分步执行
    ESCALATE = "escalate"                # 升级人工处理


# =============================================================================
# 数据类
# =============================================================================

@dataclass
class QualityScore:
    """
    单维度评分结果

    Attributes:
        dimension:       评分维度
        score:           分数（0-100）
        evidence:         打分依据（具体理由）
        suggestions:     该维度的改进建议列表
    """

    dimension: QualityDimension
    score: float = 0.0
    evidence: str = ""
    suggestions: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.score = max(0.0, min(100.0, float(self.score)))

    @property
    def is_pass(self) -> bool:
        """单维度是否达标（≥60分为单维度合格线）"""
        return self.score >= 60.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension.value,
            "dimension_label": self.dimension.label,
            "score": round(self.score, 1),
            "evidence": self.evidence,
            "suggestions": self.suggestions,
            "is_pass": self.is_pass,
        }


@dataclass
class QualityReport:
    """
    质量评分报告（5维度综合报告）

    Attributes:
        report_id:       报告唯一ID
        task_id:         对应任务ID
        scores:          5个维度的评分
        overall:         综合得分（加权平均，0-100）
        passed:          是否达标（≥90分）
        failed_dimensions: 未达标维度列表
        created_at:      报告生成时间
        metadata:        附加元数据（任务类型、引擎等）
    """

    report_id: str
    task_id: str
    scores: Dict[QualityDimension, QualityScore]
    overall: float = 0.0
    passed: bool = False
    failed_dimensions: List[QualityDimension] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # 计算综合分（加权平均）
        if self.scores:
            total_weight = sum(d.weight for d in self.scores)
            self.overall = sum(
                self.scores[d].score * d.weight for d in self.scores
            ) / total_weight
            self.overall = round(self.overall, 2)
        self.passed = self.overall >= 90.0
        self.failed_dimensions = [
            d for d, s in self.scores.items()
            if not s.is_pass
        ]

    def summary(self) -> str:
        """生成文字摘要"""
        lines = [
            f"【质量评分报告 #{self.report_id[:8]}】",
            f"任务: {self.task_id}",
            f"综合得分: {self.overall:.1f} / 100  {'✅ 达标' if self.passed else '❌ 未达标'}",
            "",
        ]
        for dim, score in self.scores.items():
            flag = "✅" if score.is_pass else "❌"
            lines.append(f"  {flag} {dim.label}: {score.score:.1f} — {score.evidence}")
            if score.suggestions:
                for sug in score.suggestions:
                    lines.append(f"     → {sug}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "task_id": self.task_id,
            "overall": self.overall,
            "passed": self.passed,
            "failed_dimensions": [d.value for d in self.failed_dimensions],
            "created_at": self.created_at,
            "scores": {d.value: s.to_dict() for d, s in self.scores.items()},
            "metadata": self.metadata,
        }


@dataclass
class AgentResult:
    """
    Agent 执行结果（质量评分的输入）

    这是质量评分的"原材料"，由执行引擎或 Agent 返回。
    QualityScorer 消费此结构进行评分。

    Attributes:
        task_id:         任务ID
        task_description: 任务原始描述（用于相关性判断）
        output:          Agent 输出内容
        raw_output:      原始输出（可能含调试信息）
        success:         是否执行成功
        error:           错误信息（如有）
        duration_ms:     执行耗时（毫秒）
        expected_duration_ms: 预期耗时（毫秒，用于时效性判断）
        tokens_used:     消耗 token 数
        tool_calls:       工具调用记录（用于完整性判断）
        agent_name:      执行 Agent 名称
        engine:          执行引擎名称
        context:         附加上下文（用户角色、意图类型等）
    """

    task_id: str
    task_description: str
    output: Any = None
    raw_output: Any = None
    success: bool = True
    error: Optional[str] = None
    duration_ms: float = 0.0
    expected_duration_ms: float = 30_000.0   # 默认30秒超时
    tokens_used: int = 0
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    agent_name: str = "unknown"
    engine: str = "unknown"
    context: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.task_id:
            self.task_id = str(uuid.uuid4())[:8]

    @property
    def output_text(self) -> str:
        """统一获取输出文本"""
        if isinstance(self.output, str):
            return self.output
        if isinstance(self.output, dict):
            import json
            return json.dumps(self.output, ensure_ascii=False)
        return str(self.output)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_description": self.task_description,
            "output_text": self.output_text[:500],  # 截断防过大
            "success": self.success,
            "error": self.error,
            "duration_ms": round(self.duration_ms, 2),
            "expected_duration_ms": self.expected_duration_ms,
            "tokens_used": self.tokens_used,
            "tool_calls_count": len(self.tool_calls),
            "agent_name": self.agent_name,
            "engine": self.engine,
        }


@dataclass
class TaskContext:
    """
    任务执行上下文（QualityScorer 的辅助输入）

    用于在评分时提供额外参考信息，提高评分准确性。
    """

    task_id: str
    intent_type: str = "unknown"         # 意图类型
    user_role: str = "viewer"             # 用户角色
    expected_outputs: List[str] = field(default_factory=list)   # 期望的输出字段
    required_tools: List[str] = field(default_factory=list)      # 必须调用的工具
    subtasks: List[str] = field(default_factory=list)            # 子任务列表
    deadline: Optional[str] = None        # 截止时间 ISO格式
    quality_tier: str = "normal"          # 质量等级 normal/high/critical

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "intent_type": self.intent_type,
            "user_role": self.user_role,
            "expected_outputs": self.expected_outputs,
            "required_tools": self.required_tools,
            "subtasks": self.subtasks,
            "deadline": self.deadline,
            "quality_tier": self.quality_tier,
        }
