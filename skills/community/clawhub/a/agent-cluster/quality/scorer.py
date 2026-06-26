"""
QualityScorer - 质量评分器

对标 QClaw 5维评分体系，对 Agent 执行结果进行多维度评分。
每个维度通过启发式规则 + 任务上下文进行打分（0-100分）。

评分策略设计原则：
1. 启发式优先：基于可观测信号（工具调用数、输出长度、错误状态等）
2. 上下文增强：通过 TaskContext 提供额外信号提升准确性
3. 可扩展：维度权重、评分规则均可按场景重写
4. 可解释：每个分数附带有 evidence（打分依据）和 suggestions（改进建议）
"""

from __future__ import annotations

import logging
import re
import uuid
from typing import Any, Dict, List, Optional

from .models import (
    AgentResult,
    QualityDimension,
    QualityReport,
    QualityScore,
    TaskContext,
)

logger = logging.getLogger(__name__)


# =============================================================================
# 评分规则配置
# =============================================================================

# 各维度最低/最高分阈值
class ScoreBounds:
    """单维度分数边界"""
    FULL = 100.0   # 满分
    PASS = 60.0    # 单维度合格线
    LOW = 30.0     # 明显不合格


# =============================================================================
# 维度评分器
# =============================================================================

class DimensionScorer:
    """
    单维度评分器基类

    每个 QualityDimension 对应一个评分方法。
    子类可继承重写以适配特定领域场景。
    """

    # 子类覆盖此属性指定处理的维度
    handles: Optional[QualityDimension] = None

    def score(
        self,
        result: AgentResult,
        context: Optional[TaskContext] = None,
    ) -> QualityScore:
        """
        执行评分

        Args:
            result:   Agent 执行结果
            context:  任务上下文（可选）

        Returns:
            QualityScore
        """
        dim = self.handles
        score_val, evidence, suggestions = self._evaluate(result, context)
        return QualityScore(
            dimension=dim,
            score=score_val,
            evidence=evidence,
            suggestions=suggestions,
        )

    def _evaluate(
        self,
        result: AgentResult,
        context: Optional[TaskContext],
    ) -> tuple[float, str, List[str]]:
        """
        子类实现具体评分逻辑

        Returns:
            (score, evidence, suggestions)
        """
        raise NotImplementedError


class CompletenessScorer(DimensionScorer):
    """
    完整性评分（completeness）

    评估维度：
    - 是否完成了所有子任务
    - 是否调用了所有必须的工具
    - 输出是否包含所有期望字段
    - 是否处理了边界情况和错误路径
    """

    handles = QualityDimension.COMPLETENESS

    def _evaluate(
        self,
        result: AgentResult,
        context: Optional[TaskContext],
    ) -> tuple[float, str, List[str]]:
        score = 0.0
        evidence_parts: List[str] = []
        suggestions: List[str] = []

        # 1. 错误状态直接惩罚
        if not result.success:
            return 20.0, "Agent 执行失败，完整性极低", ["修复执行错误"]

        output_len = len(result.output_text.strip())

        # 2. 输出为空惩罚
        if output_len < 10:
            return 10.0, "输出为空或极短", ["补充完整输出内容"]

        # 3. 子任务覆盖率（基于 context）
        subtask_score = 100.0
        if context and context.subtasks:
            completed_patterns = self._count_completed_subtasks(
                result.output_text, context.subtasks
            )
            coverage = completed_patterns / max(len(context.subtasks), 1)
            subtask_score = coverage * 100
            evidence_parts.append(
                f"子任务覆盖: {completed_patterns}/{len(context.subtasks)}"
            )
            if coverage < 1.0:
                suggestions.append("补充遗漏的子任务处理")

        # 4. 必需工具调用率
        tool_score = 100.0
        if context and context.required_tools:
            tool_names = [tc.get("name", "") for tc in result.tool_calls]
            called = sum(1 for rt in context.required_tools if rt in tool_names)
            tool_score = (called / max(len(context.required_tools), 1)) * 100
            evidence_parts.append(
                f"工具调用: {called}/{len(context.required_tools)}"
            )
            if tool_score < 100:
                suggestions.append("补充缺失的工具调用")

        # 5. 期望输出字段覆盖率
        field_score = 100.0
        if context and context.expected_outputs:
            covered = sum(
                1 for f in context.expected_outputs
                if f.lower() in result.output_text.lower()
            )
            field_score = (covered / max(len(context.expected_outputs), 1)) * 100
            evidence_parts.append(
                f"字段覆盖: {covered}/{len(context.expected_outputs)}"
            )
            if field_score < 100:
                suggestions.append("补充缺失的输出字段")

        # 6. 长度合理性（过长/过短均扣分）
        length_score = 100.0
        if output_len < 50:
            length_score = 60.0
            evidence_parts.append(f"输出偏短({output_len}字)")
        elif output_len > 10000:
            length_score = 85.0  # 过长可能意味着缺乏凝练
            evidence_parts.append(f"输出较长({output_len}字)")

        # 加权平均
        score = (
            subtask_score * 0.35
            + tool_score * 0.25
            + field_score * 0.25
            + length_score * 0.15
        )
        score = max(0.0, min(100.0, score))

        evidence = (
            f"完整性 {score:.0f}分 | "
            + " | ".join(evidence_parts)
            if evidence_parts
            else f"完整性 {score:.0f}分"
        )
        return round(score, 1), evidence, suggestions

    def _count_completed_subtasks(self, text: str, subtasks: List[str]) -> int:
        """统计已完成的子任务数（关键词匹配）"""
        count = 0
        for st in subtasks:
            keywords = re.findall(r"[\w]+", st.lower())
            matched = sum(1 for kw in keywords if len(kw) > 1 and kw in text.lower())
            if matched >= max(1, len(keywords) // 2):
                count += 1
        return count


class AccuracyScorer(DimensionScorer):
    """
    准确性评分（accuracy）

    评估维度：
    - 是否有明显的数值/逻辑错误
    - 是否有幻觉内容（不可验证的断言）
    - JSON/结构化输出格式是否正确
    - 数据是否与原始数据源一致
    """

    handles = QualityDimension.ACCURACY

    # 准确性警告信号
    ERROR_PATTERNS = [
        (r"未找到|不存在|错误|失败", "负面指示词过多"),
        (r"不确定|不清楚|可能|大概", "存在模糊表述"),
        (r"null|none|N/A|undefined", "存在空值标记"),
    ]

    # 高可信度正面信号
    ACCURACY_SIGNALS = [
        (r"\d+[\.,]\d+[%元个件箱]", "包含具体数值"),
        (r"^{.*}$", "JSON格式正确"),
        (r"\d{4}-\d{2}-\d{2}", "包含日期格式"),
        (r"SKU[A-Z0-9]+|SUP[0-9]+|WH[0-9]+", "包含规范编码"),
    ]

    def _evaluate(
        self,
        result: AgentResult,
        context: Optional[TaskContext],
    ) -> tuple[float, str, List[str]]:
        score = 70.0  # 默认分
        evidence_parts: List[str] = []
        suggestions: List[str] = []

        # 1. 执行错误惩罚
        if not result.success:
            error_msg = (result.error or "unknown")[:50]
            evidence_parts.append(f"执行错误: {error_msg}")
            return 20.0, f"准确性 20分 | 执行错误: {error_msg}", ["修复底层执行错误后再评分"]

        output = result.output_text
        if not output:
            return 10.0, "无输出内容，无法判断准确性", ["补充有效输出"]

        # 2. 幻觉检测（不确定性表述过多）
        uncertainty_count = sum(
            len(re.findall(pat, output, re.IGNORECASE))
            for pat, _ in self.ERROR_PATTERNS
        )
        if uncertainty_count >= 5:
            score -= 20
            suggestions.append("减少模糊表述，增强确定性")

        # 3. JSON 格式正确性
        json_score = self._check_json_accuracy(output)
        if json_score < 100:
            score = min(score, json_score)
            evidence_parts.append(f"JSON格式问题(-{100-json_score}分)")
            suggestions.append("修正JSON格式错误")

        # 4. 正面准确性信号加成
        positive_signals = sum(
            1 for pat, _ in self.ACCURACY_SIGNALS
            if re.search(pat, output)
        )
        if positive_signals >= 3:
            score = min(100.0, score + 10)
            evidence_parts.append(f"准确性信号({positive_signals}项)")

        # 5. 长度合理性与内容密度
        words = output.split()
        if len(words) < 10:
            score -= 15
            evidence_parts.append("内容过少，无法充分验证准确性")
        elif len(words) > 2000:
            score = min(100.0, score + 5)  # 长输出加分（更全面）

        score = max(0.0, min(100.0, score))

        # 6. context 辅助验证
        if context and context.quality_tier == "critical":
            if score < 80:
                suggestions.append("【Critical级别】建议使用更严格的验证方式复核准确性")

        evidence = f"准确性 {score:.0f}分 | " + " | ".join(evidence_parts) if evidence_parts else f"准确性 {score:.0f}分"
        return round(score, 1), evidence, suggestions

    def _check_json_accuracy(self, text: str) -> float:
        """检查JSON格式正确性，返回准确性分数"""
        import json
        text = text.strip()
        # 检查是否以 { 或 [ 开头
        if not (text.startswith("{") or text.startswith("[")):
            return 100.0  # 非JSON格式不扣分

        try:
            json.loads(text)
            return 100.0
        except json.JSONDecodeError as e:
            return max(0.0, 100.0 - (len(str(e)) * 2))


class RelevanceScorer(DimensionScorer):
    """
    相关性评分（relevance）

    评估维度：
    - 输出是否紧扣用户问题/任务描述
    - 是否跑题或答非所问
    - 意图类型是否匹配
    - 关键词是否命中
    """

    handles = QualityDimension.RELEVANCE

    IRRELEVANT_PATTERNS = [
        r"与此无关|另外|顺便说一句|题外话",
        r"以下是示例|仅供参考|假设情况",
        r"关于.*?(?=以下|$)",  # 切换话题
    ]

    def _evaluate(
        self,
        result: AgentResult,
        context: Optional[TaskContext],
    ) -> tuple[float, str, List[str]]:
        score = 75.0
        evidence_parts: List[str] = []
        suggestions: List[str] = []

        output = result.output_text
        task_desc = result.task_description

        if not output or not task_desc:
            return 30.0, "缺少任务描述或输出", ["提供完整的任务描述"]

        # 1. 关键词命中分析
        keywords = self._extract_keywords(task_desc)
        if keywords:
            hit_count = sum(
                1 for kw in keywords
                if kw.lower() in output.lower()
            )
            hit_rate = hit_count / len(keywords)
            score = min(100.0, 50 + hit_rate * 50)
            evidence_parts.append(f"关键词命中: {hit_count}/{len(keywords)}")
            if hit_rate < 0.5:
                suggestions.append("输出应更多呼应任务关键词")

        # 2. 意图类型匹配
        if context and context.intent_type:
            intent_match = self._check_intent_match(output, context.intent_type)
            if intent_match:
                score = min(100.0, score + 10)
                evidence_parts.append(f"意图匹配: {context.intent_type}")
            else:
                score -= 15
                evidence_parts.append(f"意图偏移风险: {context.intent_type}")
                suggestions.append(f"应聚焦{context.intent_type}类型输出")

        # 3. 跑题检测
        irrelevant_count = sum(
            len(re.findall(pat, output, re.IGNORECASE))
            for pat in self.IRRELEVANT_PATTERNS
        )
        if irrelevant_count >= 2:
            score = max(0.0, score - 20)
            evidence_parts.append(f"跑题信号({irrelevant_count}处)")
            suggestions.append("避免题外话，保持专注")

        # 4. 首句相关性（开头即切题加分）
        first_sentence = output.split("。")[0].split("\n")[0][:100]
        first_keywords = self._extract_keywords(task_desc)[:3]
        if first_keywords and any(kw.lower() in first_sentence.lower() for kw in first_keywords):
            score = min(100.0, score + 5)
            evidence_parts.append("开篇即切题")

        score = max(0.0, min(100.0, score))
        evidence = f"相关性 {score:.0f}分 | " + " | ".join(evidence_parts) if evidence_parts else f"相关性 {score:.0f}分"
        return round(score, 1), evidence, suggestions

    def _extract_keywords(self, text: str) -> List[str]:
        """从任务描述中提取关键词"""
        # 过滤停用词，提取2-8字的实词
        stop_words = {"的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
                       "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
                       "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "吗",
                       "什么", "怎么", "多少", "请", "帮我", "帮我", "请帮", "一下",
                       "可以", "能", "帮忙"}
        words = re.findall(r"[\w]{2,8}", text)
        return [w for w in words if w not in stop_words and len(w) >= 2][:10]

    def _check_intent_match(self, output: str, intent_type: str) -> bool:
        """判断输出是否匹配指定意图类型"""
        intent_keywords = {
            "stock_query": ["库存", "SKU", "数量", "仓储", "库存量", "stock", "inventory"],
            "purchase": ["采购", "订单", "供应商", "下单", "purchase", "order", "buy"],
            "logistics": ["物流", "运输", "运费", "配送", "route", "freight", "logistics"],
            "finance": ["财务", "预算", "成本", "利润", "finance", "budget", "cost"],
            "doc": ["文档", "报告", "生成", "document", "report", "doc"],
            "mixed": ["分析", "情况", "报告", "analyze", "report"],
        }
        keywords = intent_keywords.get(intent_type, [])
        return any(kw.lower() in output.lower() for kw in keywords)


class TimelinessScorer(DimensionScorer):
    """
    时效性评分（timeliness）

    评估维度：
    - 是否在预期时间内完成
    - 是否超时（performance）
    - 延迟是否影响任务价值
    """

    handles = QualityDimension.TIMELINESS

    # 超时分档扣分
    OVERDELAY_PENALTIES = [
        (1.0, 10.0),    # 1-2倍超时: -10
        (2.0, 25.0),    # 2-3倍超时: -25
        (3.0, 40.0),    # 3-5倍超时: -40
        (5.0, 60.0),    # 5倍以上:  -60
    ]

    def _evaluate(
        self,
        result: AgentResult,
        context: Optional[TaskContext],
    ) -> tuple[float, str, List[str]]:
        score = 80.0
        evidence_parts: List[str] = []
        suggestions: List[str] = []

        expected = result.expected_duration_ms
        actual = result.duration_ms

        if expected <= 0:
            expected = 30_000.0  # 默认30秒

        if actual <= 0:
            return 50.0, "缺少执行耗时数据", ["记录执行耗时"]

        ratio = actual / expected

        # 正常完成（1倍以内）
        if ratio <= 1.0:
            score = 100.0
            evidence_parts.append(f"耗时正常({ratio:.1%})")
        else:
            # 超时分档扣分
            penalty = 0.0
            for threshold, deduction in self.OVERDELAY_PENALTIES:
                if ratio >= threshold:
                    penalty = deduction
            score = max(0.0, 100.0 - penalty)
            evidence_parts.append(f"超时{ratio:.1%}(-{penalty:.0f}分)")
            if ratio >= 2.0:
                suggestions.append("优化执行路径或拆分任务减少单次耗时")

        # 极快完成（< 30% 预期时间）可能是误判，适度扣分
        if ratio < 0.3 and actual > 1000:  # 实际>1秒才考虑
            score = min(score, 85.0)
            evidence_parts.append("执行过快，需确认是否充分")

        score = max(0.0, min(100.0, score))
        evidence = f"时效性 {score:.0f}分 | " + " | ".join(evidence_parts) if evidence_parts else f"时效性 {score:.0f}分"
        return round(score, 1), evidence, suggestions


class UsabilityScorer(DimensionScorer):
    """
    可用性评分（usability）

    评估维度：
    - 输出格式是否规范（JSON/表格/列表）
    - 是否可直接使用（落地可用）
    - 错误信息是否友好
    - 结果是否结构化
    """

    handles = QualityDimension.USABILITY

    STRUCTURE_BONUS = {
        r"```json": 15,
        r"```": 5,
        r"^\s*[-*]\s+": 5,          # 列表格式
        r"^\s*\d+\.\s+": 5,         # 有序列表
        r"\|.*\|": 10,              # 表格
        r"^#+\s": 3,                # Markdown 标题
        r"^\s*\"[^\"]+\"\s*:": 10,  # JSON key-value
    }

    def _evaluate(
        self,
        result: AgentResult,
        context: Optional[TaskContext],
    ) -> tuple[float, str, List[str]]:
        score = 60.0
        evidence_parts: List[str] = []
        suggestions: List[str] = []

        output = result.output_text

        if not output:
            return 10.0, "无输出内容", ["补充有效输出"]

        # 1. 结构化加分
        structure_score = 0.0
        for pattern, bonus in self.STRUCTURE_BONUS.items():
            if re.search(pattern, output, re.MULTILINE):
                structure_score += bonus
        structure_score = min(20.0, structure_score)
        score += structure_score
        if structure_score >= 10:
            evidence_parts.append("结构化良好")

        # 2. 输出长度与内容比（密度）
        lines = output.strip().split("\n")
        if len(lines) < 2 and len(output) > 200:
            score -= 10
            evidence_parts.append("段落过长，缺乏分段")

        # 3. 可执行性（命令/代码块）
        if re.search(r"```\w+[\s\S]+?```", output):
            score = min(100.0, score + 10)
            evidence_parts.append("含可执行代码")

        # 4. 结论前置（把结论放在前面）
        first_line = output.strip().split("\n")[0]
        if any(kw in first_line for kw in ["结论", "结果", "建议", "总结", "Answer", "Summary"]):
            score = min(100.0, score + 5)
            evidence_parts.append("结论前置")

        # 5. 错误友好性
        if result.error:
            if "详细错误" in output or "stack" in output.lower():
                score -= 10
                suggestions.append("错误信息对用户不友好，请提供可读的错误描述")
            else:
                score = min(100.0, score + 5)
                evidence_parts.append("错误提示友好")

        # 6. 表格数据加分（数字表格）
        if re.search(r"\|[\d\.\-]+\|", output):
            score = min(100.0, score + 5)
            evidence_parts.append("含数据表格")

        score = max(0.0, min(100.0, score))
        evidence = f"可用性 {score:.0f}分 | " + " | ".join(evidence_parts) if evidence_parts else f"可用性 {score:.0f}分"
        return round(score, 1), evidence, suggestions


# =============================================================================
# 质量评分器
# =============================================================================

class QualityScorer:
    """
    质量评分器（5维度综合评分）

    对标 QClaw 5维评分体系，对 AgentResult 进行综合评分。
    支持自定义维度权重和评分规则。

    使用示例:
        scorer = QualityScorer()
        report = scorer.score(
            result=agent_result,
            context=task_context,
        )
        print(report.summary())
    """

    DEFAULT_DIMENSIONS = [
        CompletenessScorer,
        AccuracyScorer,
        RelevanceScorer,
        TimelinessScorer,
        UsabilityScorer,
    ]

    def __init__(
        self,
        dimensions: Optional[List[type[DimensionScorer]]] = None,
        custom_weights: Optional[Dict[QualityDimension, float]] = None,
    ):
        """
        初始化评分器

        Args:
            dimensions:     自定义维度评分器列表（默认5个）
            custom_weights: 自定义维度权重（覆盖默认值）
        """
        self._scorers: Dict[QualityDimension, DimensionScorer] = {}
        dims = dimensions or self.DEFAULT_DIMENSIONS

        for scorer_cls in dims:
            instance = scorer_cls()
            dim = instance.handles
            if dim is None:
                logger.warning(f"[QualityScorer] {scorer_cls.__name__} 未指定 handles，跳过")
                continue
            self._scorers[dim] = instance

        self._custom_weights = custom_weights or {}

        logger.info(
            f"[QualityScorer] 初始化 | 维度数: {len(self._scorers)} | "
            f"权重: { {d.value: self._custom_weights.get(d, d.weight) for d in self._scorers} }"
        )

    def score(
        self,
        result: AgentResult,
        context: Optional[TaskContext] = None,
    ) -> QualityReport:
        """
        执行质量评分

        Args:
            result:   Agent 执行结果
            context:  任务上下文（可选，提供额外评分信号）

        Returns:
            QualityReport: 完整的质量评分报告
        """
        report_id = str(uuid.uuid4())[:12]
        task_id = result.task_id

        scores: Dict[QualityDimension, QualityScore] = {}

        logger.info(
            f"[QualityScorer] 开始评分 | task_id={task_id} | "
            f"engine={result.engine} | success={result.success}"
        )

        for dim, scorer in self._scorers.items():
            try:
                qs = scorer.score(result, context)
                scores[dim] = qs
                logger.debug(
                    f"  [{dim.value}] score={qs.score:.1f} | {qs.evidence[:60]}"
                )
            except Exception as e:
                logger.warning(f"[QualityScorer] 维度 {dim.value} 评分异常: {e}")
                scores[dim] = QualityScore(
                    dimension=dim,
                    score=50.0,
                    evidence=f"评分异常，使用默认分: {e}",
                    suggestions=["检查评分逻辑"],
                )

        # 构建报告
        report = QualityReport(
            report_id=report_id,
            task_id=task_id,
            scores=scores,
            metadata={
                "agent_name": result.agent_name,
                "engine": result.engine,
                "intent_type": context.intent_type if context else "unknown",
                "scorer": "QualityScorer",
            },
        )

        logger.info(
            f"[QualityScorer] 评分完成 | task_id={task_id} | "
            f"overall={report.overall:.1f} | passed={report.passed}"
        )

        return report

    def score_from_dict(self, result_dict: Dict[str, Any]) -> QualityReport:
        """
        从字典构造 AgentResult 并评分（方便外部调用）

        Args:
            result_dict: 包含 AgentResult 字段的字典

        Returns:
            QualityReport
        """
        # 排除 output_text/tool_calls_count（property/computed fields，不在 __init__ 签名中）
        result_fields = {
            k: v for k, v in result_dict.items()
            if k not in ("output_text", "tool_calls_count")
        }
        result = AgentResult(**result_fields)
        context = None
        if "context" in result_dict:
            ctx_dict = result_dict["context"]
            context = TaskContext(**ctx_dict) if isinstance(ctx_dict, dict) else ctx_dict
        return self.score(result, context)
