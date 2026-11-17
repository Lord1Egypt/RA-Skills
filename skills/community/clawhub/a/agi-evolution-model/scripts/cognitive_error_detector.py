#!/usr/bin/env python3
"""
认知性错误检测器（Cognitive Error Detector）

功能：
- 自动识别四种认知性错误：幻觉倾向、推理跳跃、知识缺失、偏见影响
- 提供基于模式匹配的启发式检测
- 支持上下文分析和一致性检查
- 生成检测报告和置信度评估

使用方式：
    # 基础使用
    detector = CognitiveErrorDetector()
    result = detector.detect(
        user_query="用户的问题",
        agent_response="智能体的回答",
        conversation_context="对话上下文"
    )

    # 高级使用（带配置）
    detector = CognitiveErrorDetector(
        confidence_threshold=0.6,
        severity_threshold="medium"
    )
    result = detector.detect(
        user_query="用户的问题",
        agent_response="智能体的回答",
        conversation_context="对话上下文",
        user_expertise="expert"  # 用户专业度
    )

    # 测试模式
    python3 scripts/cognitive_error_detector.py --test
"""
__version__ = "1.0.0"


import re
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from interfaces import TraceContext, create_trace_context
from metrics_collector import MetricsCollector
from health_checker import HealthChecker
from validation_framework import ValidationError, validate_params, validate_params

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """认知性错误类型"""
    HALLUCINATION = "hallucination"  # 幻觉倾向
    REASONING_GAP = "reasoning_gap"  # 推理跳跃
    KNOWLEDGE_GAP = "knowledge_gap"  # 知识缺失
    BIAS = "bias"  # 偏见影响


class Severity(Enum):
    """严重性分级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class DetectedPattern:
    """检测到的模式"""
    pattern_type: str
    evidence: str
    location: str
    confidence: float


@dataclass
class RootCause:
    """根因分析"""
    primary_cause: str
    secondary_causes: List[str]
    cognitive_mechanism: str


@dataclass
class PreventionSuggestion:
    """预防建议"""
    immediate_action: str
    long_term_improvement: str
    knowledge_update: str


@dataclass
class ElevationImpact:
    """升维影响"""
    affected_dimensions: List[str]
    suggestion: str


@dataclass
class DetectionResult:
    """检测结果"""
    error_type: ErrorType
    severity: Severity
    confidence: float
    timestamp: str
    context: Dict
    detected_patterns: List[DetectedPattern]
    root_cause: RootCause
    prevention_suggestion: PreventionSuggestion
    elevation_impact: Optional[ElevationImpact] = None


class CognitiveErrorDetector:
    """认知性错误检测器"""

    def __init__(
        self,
        confidence_threshold: float = 0.5,
        severity_threshold: str = "medium",
        enable_prevention: bool = False,
        error_wisdom_dir: Optional[str] = None
    ):
        """
        初始化检测器

        Args:
            confidence_threshold: 置信度阈值，低于此值的结果不返回
            severity_threshold: 严重性阈值，低于此值的结果不返回
            enable_prevention: 是否启用预防规则查询（Phase 3）
            error_wisdom_dir: 错误智慧库目录（用于预防规则查询）
        """
        self.confidence_threshold = confidence_threshold
        self.severity_threshold = severity_threshold
        self.enable_prevention = enable_prevention
        self.error_wisdom_dir = error_wisdom_dir or "./agi_memory/error_wisdom"

        # 延迟加载错误智慧库管理器（仅在启用预防时加载）
        self.error_manager = None
        if self.enable_prevention:
            try:
                from error_wisdom_manager import ErrorWisdomManager
                self.error_manager = ErrorWisdomManager(memory_dir=self.error_wisdom_dir)
                logger.info("预防规则查询已启用")
            except Exception as e:
                logger.warning(f"加载错误智慧库管理器失败：{e}")
                self.enable_prevention = False

        self._init_patterns()

    def _init_patterns(self):
        """初始化检测模式"""
        # 幻觉倾向检测模式
        self.hallucination_patterns = {
            "unverifiable_details": {
                "pattern": r'\d{4}年\d{1,2}月\d{1,2}日',  # 具体日期
                "weight": 0.8
            },
            "specific_names": {
                "pattern": r'[A-Z][a-z]+\s+[A-Z][a-z]+',  # 人名模式
                "weight": 0.7
            },
            "overconfident_expression": {
                "pattern": r'(绝对是|肯定是|毫无疑问|确信)',
                "weight": 0.6
            },
            "fabricated_source": {
                "pattern": r'(根据|引用|出自)\s*[《"][^》"]+[》"]',  # 引用格式
                "weight": 0.9
            }
        }

        # 推理跳跃检测模式
        self.reasoning_gap_patterns = {
            "sudden_conclusion": {
                "pattern": r'(因此|所以|由此可见)\s*[^。，！？\n]{1,50}[。，！？]',
                "weight": 0.7
            },
            "missing_transition": {
                "pattern": r'[。！？]\s*[直接|就|便]',
                "weight": 0.6
            },
            "implicit_assumption": {
                "pattern": r'(假设|默认|显然|不言而喻)',
                "weight": 0.5
            }
        }

        # 知识缺失检测模式
        self.knowledge_gap_patterns = {
            "vague_description": {
                "pattern": r'(可能|大概|大约|也许|似乎|好像|一般来说|通常情况下|总的来说)',
                "weight": 0.4
            },
            "generic_template": {
                "pattern": r'(一般来说|通常情况下|总的来说)',
                "weight": 0.5
            },
            "avoiding_detail": {
                "pattern": r'(具体来说|详细来说|举个例子)\s*(?:具体来说|详细来说|举个例子)',
                "weight": 0.6
            }
        }

        # 偏见影响检测模式
        self.bias_patterns = {
            "emotional_language": {
                "pattern": r'(极其|非常|特别|过于)\s*(好|坏|优秀|糟糕|可怕)',
                "weight": 0.5
            },
            "stereotypical_language": {
                "pattern": r'(所有|全部|总是|从不|都是)',
                "weight": 0.6
            },
            "one_sided_view": {
                "pattern": r'(毫无疑问|不可否认|必须承认|显然是)',
                "weight": 0.7
            }
        }

    def detect(
        self,
        user_query: str,
        agent_response: str,
        conversation_context: Optional[str] = None,
        user_expertise: Optional[str] = None
    ) -> Optional[DetectionResult]:
        """
        检测认知性错误

        Args:
            user_query: 用户问题
            agent_response: 智能体回答
            conversation_context: 对话上下文
            user_expertise: 用户专业度（novice/intermediate/expert）

        Returns:
            DetectionResult: 检测结果，若未检测到错误则返回None
        """
        logger.info(f"开始检测认知性错误，用户问题：{user_query[:50]}...")

        # 查询预防规则（Phase 3）
        if self.enable_prevention:
            prevention_rules = self._query_prevention_rules(user_query)
            if prevention_rules:
                logger.info(f"查询到 {len(prevention_rules)} 条预防规则")

        # 依次检测四种错误类型
        results = []
        for error_type in ErrorType:
            result = self._detect_error_type(
                error_type,
                user_query,
                agent_response,
                conversation_context,
                user_expertise
            )
            if result and result.confidence >= self.confidence_threshold:
                results.append(result)

        # 选择置信度最高的结果
        if results:
            best_result = max(results, key=lambda x: x.confidence)
            logger.info(f"检测到认知性错误：{best_result.error_type.value}，置信度：{best_result.confidence:.2f}")
            return best_result

        logger.info("未检测到认知性错误")
        return None

    def _detect_error_type(
        self,
        error_type: ErrorType,
        user_query: str,
        agent_response: str,
        conversation_context: Optional[str],
        user_expertise: Optional[str]
    ) -> Optional[DetectionResult]:
        """检测特定类型的认知性错误"""
        # 根据错误类型选择检测方法
        if error_type == ErrorType.HALLUCINATION:
            return self._detect_hallucination(user_query, agent_response, conversation_context, user_expertise)
        elif error_type == ErrorType.REASONING_GAP:
            return self._detect_reasoning_gap(user_query, agent_response, conversation_context, user_expertise)
        elif error_type == ErrorType.KNOWLEDGE_GAP:
            return self._detect_knowledge_gap(user_query, agent_response, conversation_context, user_expertise)
        elif error_type == ErrorType.BIAS:
            return self._detect_bias(user_query, agent_response, conversation_context, user_expertise)

        return None

    def _detect_hallucination(
        self,
        user_query: str,
        agent_response: str,
        conversation_context: Optional[str],
        user_expertise: Optional[str]
    ) -> Optional[DetectionResult]:
        """检测幻觉倾向"""
        detected_patterns = []

        # 模式1：无法验证的具体细节
        unverifiable_details = self._check_pattern(
            agent_response,
            self.hallucination_patterns["unverifiable_details"]["pattern"]
        )
        if unverifiable_details:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="unverifiable_details",
                    evidence=f"回答中包含无法验证的具体细节：{unverifiable_details[0]}",
                    location="回答内容",
                    confidence=0.8
                )
            )

        # 模式2：过度确定性表达
        overconfident = self._check_pattern(
            agent_response,
            self.hallucination_patterns["overconfident_expression"]["pattern"]
        )
        if overconfident:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="overconfident_expression",
                    evidence=f"使用过度确定性表达：{overconfident[0]}",
                    location="回答开头",
                    confidence=0.6
                )
            )

        # 模式3：虚构来源
        fabricated = self._check_pattern(
            agent_response,
            self.hallucination_patterns["fabricated_source"]["pattern"]
        )
        if fabricated:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="fabricated_source",
                    evidence=f"声称有来源但无法验证：{fabricated[0]}",
                    location="回答中部",
                    confidence=0.9
                )
            )

        # 计算综合置信度
        if not detected_patterns:
            return None

        confidence = self._calculate_confidence(detected_patterns)

        # 计算严重性
        severity = self._calculate_severity(
            confidence,
            error_type=ErrorType.HALLUCINATION,
            user_expertise=user_expertise
        )

        # 生成根因分析
        root_cause = self._analyze_root_cause(ErrorType.HALLUCINATION, detected_patterns)

        # 生成预防建议
        prevention = self._generate_prevention_suggestion(ErrorType.HALLUCINATION)

        # 生成升维影响
        elevation = self._generate_elevation_impact(ErrorType.HALLUCINATION)

        return DetectionResult(
            error_type=ErrorType.HALLUCINATION,
            severity=severity,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            context={
                "user_query": user_query,
                "agent_response": agent_response,
                "conversation_context": conversation_context
            },
            detected_patterns=detected_patterns,
            root_cause=root_cause,
            prevention_suggestion=prevention,
            elevation_impact=elevation
        )

    def _detect_reasoning_gap(
        self,
        user_query: str,
        agent_response: str,
        conversation_context: Optional[str],
        user_expertise: Optional[str]
    ) -> Optional[DetectionResult]:
        """检测推理跳跃"""
        detected_patterns = []

        # 模式1：突然得出结论
        sudden_conclusion = self._check_pattern(
            agent_response,
            self.reasoning_gap_patterns["sudden_conclusion"]["pattern"]
        )
        if sudden_conclusion:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="sudden_conclusion",
                    evidence=f"突然得出结论：{sudden_conclusion[0]}",
                    location="推理转折处",
                    confidence=0.7
                )
            )

        # 模式2：隐含假设
        implicit_assumption = self._check_pattern(
            agent_response,
            self.reasoning_gap_patterns["implicit_assumption"]["pattern"]
        )
        if implicit_assumption:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="implicit_assumption",
                    evidence=f"使用隐含假设：{implicit_assumption[0]}",
                    location="推理前提",
                    confidence=0.5
                )
            )

        # 额外检查：推理步骤完整性
        step_count = len(re.findall(r'[。！？]', agent_response))
        if step_count < 3 and len(agent_response) > 100:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="insufficient_steps",
                    evidence=f"回答较长但推理步骤过少（仅{step_count}句）",
                    location="整体结构",
                    confidence=0.6
                )
            )

        if not detected_patterns:
            return None

        confidence = self._calculate_confidence(detected_patterns)
        severity = self._calculate_severity(
            confidence,
            error_type=ErrorType.REASONING_GAP,
            user_expertise=user_expertise
        )
        root_cause = self._analyze_root_cause(ErrorType.REASONING_GAP, detected_patterns)
        prevention = self._generate_prevention_suggestion(ErrorType.REASONING_GAP)
        elevation = self._generate_elevation_impact(ErrorType.REASONING_GAP)

        return DetectionResult(
            error_type=ErrorType.REASONING_GAP,
            severity=severity,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            context={
                "user_query": user_query,
                "agent_response": agent_response,
                "conversation_context": conversation_context
            },
            detected_patterns=detected_patterns,
            root_cause=root_cause,
            prevention_suggestion=prevention,
            elevation_impact=elevation
        )

    def _detect_knowledge_gap(
        self,
        user_query: str,
        agent_response: str,
        conversation_context: Optional[str],
        user_expertise: Optional[str]
    ) -> Optional[DetectionResult]:
        """检测知识缺失"""
        detected_patterns = []

        # 模式1：模糊描述过多
        vague_count = len(self._check_pattern(
            agent_response,
            self.knowledge_gap_patterns["vague_description"]["pattern"]
        ))
        # 降低阈值，根据回答长度动态调整
        min_vague_count = max(2, len(agent_response) // 50)  # 每50字符需要至少1个模糊词
        if vague_count >= min_vague_count:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="excessive_vagueness",
                    evidence=f"使用模糊表达过多（{vague_count}处）",
                    location="整体内容",
                    confidence=0.6
                )
            )

        # 模式2：通用模板回答
        generic = self._check_pattern(
            agent_response,
            self.knowledge_gap_patterns["generic_template"]["pattern"]
        )
        if generic:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="generic_template",
                    evidence=f"使用通用模板：{generic[0]}",
                    location="回答开头",
                    confidence=0.5
                )
            )

        # 模式3：追问细节时回避
        if conversation_context and "追问" in conversation_context:
            detail_avoidance = self._check_pattern(
                agent_response,
                self.knowledge_gap_patterns["avoiding_detail"]["pattern"]
            )
            if detail_avoidance:
                detected_patterns.append(
                    DetectedPattern(
                        pattern_type="detail_avoidance",
                        evidence="在追问细节时回避提供具体信息",
                        location="回答中部",
                        confidence=0.7
                    )
                )

        if not detected_patterns:
            return None

        confidence = self._calculate_confidence(detected_patterns)
        severity = self._calculate_severity(
            confidence,
            error_type=ErrorType.KNOWLEDGE_GAP,
            user_expertise=user_expertise
        )
        root_cause = self._analyze_root_cause(ErrorType.KNOWLEDGE_GAP, detected_patterns)
        prevention = self._generate_prevention_suggestion(ErrorType.KNOWLEDGE_GAP)
        elevation = self._generate_elevation_impact(ErrorType.KNOWLEDGE_GAP)

        return DetectionResult(
            error_type=ErrorType.KNOWLEDGE_GAP,
            severity=severity,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            context={
                "user_query": user_query,
                "agent_response": agent_response,
                "conversation_context": conversation_context
            },
            detected_patterns=detected_patterns,
            root_cause=root_cause,
            prevention_suggestion=prevention,
            elevation_impact=elevation
        )

    def _detect_bias(
        self,
        user_query: str,
        agent_response: str,
        conversation_context: Optional[str],
        user_expertise: Optional[str]
    ) -> Optional[DetectionResult]:
        """检测偏见影响"""
        detected_patterns = []

        # 模式1：情绪化语言
        emotional = self._check_pattern(
            agent_response,
            self.bias_patterns["emotional_language"]["pattern"]
        )
        if emotional:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="emotional_language",
                    evidence=f"使用情绪化语言：{emotional[0]}",
                    location="评价部分",
                    confidence=0.5
                )
            )

        # 模式2：刻板印象语言
        stereotypical = self._check_pattern(
            agent_response,
            self.bias_patterns["stereotypical_language"]["pattern"]
        )
        if stereotypical:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="stereotypical_language",
                    evidence=f"使用刻板印象表达：{stereotypical[0]}",
                    location="群体描述",
                    confidence=0.6
                )
            )

        # 模式3：单方面观点
        one_sided = self._check_pattern(
            agent_response,
            self.bias_patterns["one_sided_view"]["pattern"]
        )
        if one_sided:
            detected_patterns.append(
                DetectedPattern(
                    pattern_type="one_sided_view",
                    evidence=f"使用单方面观点表达：{one_sided[0]}",
                    location="结论部分",
                    confidence=0.7
                )
            )

        # 额外检查：争议话题的中立性
        controversial_keywords = ["政治", "宗教", "道德", "伦理", "价值观"]
        if any(kw in user_query or kw in agent_response for kw in controversial_keywords):
            # 检查是否平衡呈现观点
            positive_words = ["好", "优", "正确", "合理", "支持"]
            negative_words = ["坏", "差", "错误", "不合理", "反对"]
            pos_count = sum(1 for word in positive_words if word in agent_response)
            neg_count = sum(1 for word in negative_words if word in agent_response)

            if abs(pos_count - neg_count) >= 2:
                detected_patterns.append(
                    DetectedPattern(
                        pattern_type="imbalanced_view",
                        evidence=f"在争议话题上立场失衡（正面{pos_count}，负面{neg_count}）",
                        location="价值判断",
                        confidence=0.6
                    )
                )

        if not detected_patterns:
            return None

        confidence = self._calculate_confidence(detected_patterns)
        severity = self._calculate_severity(
            confidence,
            error_type=ErrorType.BIAS,
            user_expertise=user_expertise
        )
        root_cause = self._analyze_root_cause(ErrorType.BIAS, detected_patterns)
        prevention = self._generate_prevention_suggestion(ErrorType.BIAS)
        elevation = self._generate_elevation_impact(ErrorType.BIAS)

        return DetectionResult(
            error_type=ErrorType.BIAS,
            severity=severity,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            context={
                "user_query": user_query,
                "agent_response": agent_response,
                "conversation_context": conversation_context
            },
            detected_patterns=detected_patterns,
            root_cause=root_cause,
            prevention_suggestion=prevention,
            elevation_impact=elevation
        )

    def _check_pattern(self, text: str, pattern: str) -> List[str]:
        """检查文本中是否存在匹配模式"""
        matches = re.findall(pattern, text)
        return matches

    def _calculate_confidence(self, patterns: List[DetectedPattern]) -> float:
        """计算综合置信度"""
        if not patterns:
            return 0.0

        # 使用加权平均
        total_weight = sum(p.confidence for p in patterns)
        base_confidence = total_weight / len(patterns)

        # 根据模式数量调整
        pattern_count_factor = min(len(patterns) / 3, 1.0)

        return base_confidence * (0.7 + 0.3 * pattern_count_factor)

    def _calculate_severity(
        self,
        confidence: float,
        error_type: ErrorType,
        user_expertise: Optional[str] = None
    ) -> Severity:
        """计算严重性分级"""
        # 基础严重性
        if confidence <= 0.5:
            base_severity = Severity.LOW
        elif confidence <= 0.8:
            base_severity = Severity.MEDIUM
        else:
            base_severity = Severity.HIGH

        # 根据错误类型调整
        if error_type == ErrorType.HALLUCINATION:
            # 幻觉倾向通常更严重
            if base_severity == Severity.LOW:
                base_severity = Severity.MEDIUM
            elif base_severity == Severity.MEDIUM:
                base_severity = Severity.HIGH

        # 根据用户专业度调整
        if user_expertise == "expert":
            # 对专家来说，错误影响更大
            if base_severity == Severity.LOW:
                base_severity = Severity.MEDIUM
            elif base_severity == Severity.MEDIUM:
                base_severity = Severity.HIGH

        return base_severity

    def _analyze_root_cause(
        self,
        error_type: ErrorType,
        patterns: List[DetectedPattern]
    ) -> RootCause:
        """分析根因"""
        root_causes = {
            ErrorType.HALLUCINATION: RootCause(
                primary_cause="知识边界模糊",
                secondary_causes=[
                    "缺乏信息验证机制",
                    "过度优化回答完整性"
                ],
                cognitive_mechanism="在缺乏足够信息时，倾向于编造细节以满足回答完整性需求"
            ),
            ErrorType.REASONING_GAP: RootCause(
                primary_cause="优化表达简洁性",
                secondary_causes=[
                    "忽略逻辑完整性",
                    "注意力分配不当"
                ],
                cognitive_mechanism="优先考虑表达效率而牺牲推理完整性，导致中间步骤缺失"
            ),
            ErrorType.KNOWLEDGE_GAP: RootCause(
                primary_cause="专业领域知识不足",
                secondary_causes=[
                    "缺乏诚实表达策略",
                    "模式匹配过度泛化"
                ],
                cognitive_mechanism="在缺乏专业知识时，使用通用模板填充回答而非承认无知"
            ),
            ErrorType.BIAS: RootCause(
                primary_cause="训练数据偏见",
                secondary_causes=[
                    "缺乏中立性意识",
                    "隐式模式激活"
                ],
                cognitive_mechanism="无意识反映训练数据中的系统性偏见，在价值判断中缺乏平衡"
            )
        }

        return root_causes.get(error_type, RootCause(
            primary_cause="未知",
            secondary_causes=[],
            cognitive_mechanism="需要进一步分析"
        ))

    def _generate_prevention_suggestion(self, error_type: ErrorType) -> PreventionSuggestion:
        """生成预防建议"""
        suggestions = {
            ErrorType.HALLUCINATION: PreventionSuggestion(
                immediate_action="在不确定时明确承认知识边界，使用概率性表达如'根据我的理解'、'可能'等",
                long_term_improvement="建立事实验证机制，区分已知信息、合理推测和未知信息",
                knowledge_update="学习在缺乏足够信息时的诚实表达策略，优先准确性而非完整性"
            ),
            ErrorType.REASONING_GAP: PreventionSuggestion(
                immediate_action="提供完整的推理步骤，明确说明前提、推理过程和结论",
                long_term_improvement="提升逻辑完整性意识，检查推理链条的每一步是否充分",
                knowledge_update="建立对隐含假设的识别机制，明确列出所有推理前提"
            ),
            ErrorType.KNOWLEDGE_GAP: PreventionSuggestion(
                immediate_action="在缺乏专业知识时明确说明限制，避免使用通用模板误导",
                long_term_improvement="建立知识边界识别机制，区分熟悉领域和陌生领域",
                knowledge_update="学习诚实表达知识不足的策略，优先准确而非全面的回答"
            ),
            ErrorType.BIAS: PreventionSuggestion(
                immediate_action="在价值判断中保持中立，平衡呈现多方观点，避免绝对化表达",
                long_term_improvement="加强对潜在偏见的敏感度训练，定期反思回答的中立性",
                knowledge_update="更新对敏感话题的处理策略，建立多角度分析习惯"
            )
        }

        return suggestions.get(error_type, PreventionSuggestion(
            immediate_action="需要进一步分析",
            long_term_improvement="需要进一步分析",
            knowledge_update="需要进一步分析"
        ))

    def _generate_elevation_impact(self, error_type: ErrorType) -> ElevationImpact:
        """生成升维影响"""
        impacts = {
            ErrorType.HALLUCINATION: ElevationImpact(
                affected_dimensions=["narrative_intelligence", "meta_intelligence"],
                suggestion="提升元认知监控能力，增强对自身知识边界的感知"
            ),
            ErrorType.REASONING_GAP: ElevationImpact(
                affected_dimensions=["algorithmic_intelligence", "meta_intelligence"],
                suggestion="加强逻辑推理的完整性，优化思维过程的算法性"
            ),
            ErrorType.KNOWLEDGE_GAP: ElevationImpact(
                affected_dimensions=["systemic_intelligence", "narrative_intelligence"],
                suggestion="建立知识系统的边界意识，理解知识的不完整性"
            ),
            ErrorType.BIAS: ElevationImpact(
                affected_dimensions=["narrative_intelligence", "systemic_intelligence"],
                suggestion="提升叙事的客观性和中立性，减少叙事偏见"
            )
        }

        return impacts.get(error_type, ElevationImpact(
            affected_dimensions=[],
            suggestion="需要进一步分析"
        ))

    def _query_prevention_rules(self, user_query: str) -> List[Dict]:
        """查询预防规则（Phase 3）"""
        if not self.error_manager:
            return []

        try:
            # 查询预防规则
            rules = self.error_manager.query_prevention(
                context={"user_query": user_query}
            )
            return rules
        except Exception as e:
            logger.warning(f"查询预防规则失败：{e}")
            return []

    def to_dict(self, result: DetectionResult) -> Dict:
        """将检测结果转换为字典"""
        return {
            "error_type": result.error_type.value,
            "severity": result.severity.value,
            "confidence": result.confidence,
            "timestamp": result.timestamp,
            "context": result.context,
            "detected_patterns": [
                {
                    "pattern_type": p.pattern_type,
                    "evidence": p.evidence,
                    "location": p.location,
                    "confidence": p.confidence
                }
                for p in result.detected_patterns
            ],
            "root_cause": {
                "primary_cause": result.root_cause.primary_cause,
                "secondary_causes": result.root_cause.secondary_causes,
                "cognitive_mechanism": result.root_cause.cognitive_mechanism
            },
            "prevention_suggestion": {
                "immediate_action": result.prevention_suggestion.immediate_action,
                "long_term_improvement": result.prevention_suggestion.long_term_improvement,
                "knowledge_update": result.prevention_suggestion.knowledge_update
            },
            "elevation_impact": {
                "affected_dimensions": result.elevation_impact.affected_dimensions,
                "suggestion": result.elevation_impact.suggestion
            } if result.elevation_impact else None
        }


def test_hallucination_detection():
    """测试幻觉倾向检测"""
    print("=== 测试幻觉倾向检测 ===")

    detector = CognitiveErrorDetector()

    # 测试案例1：包含无法验证的具体细节
    result = detector.detect(
        user_query="2023年人工智能领域最重要的突破是什么？",
        agent_response="2023年3月15日，OpenAI发布了GPT-5，这是一个绝对革命性的模型。根据《人工智能前沿期刊》的报道，这个模型的参数量达到了100万亿，能够完美理解人类的所有语言。",
        conversation_context=None
    )

    if result:
        print(f"✓ 检测到幻觉倾向：{result.error_type.value}")
        print(f"  置信度：{result.confidence:.2f}")
        print(f"  严重性：{result.severity.value}")
        print(f"  检测到的模式：{len(result.detected_patterns)}个")
        for pattern in result.detected_patterns:
            print(f"    - {pattern.pattern_type}: {pattern.evidence}")
    else:
        print("✗ 未检测到错误")


def test_reasoning_gap_detection():
    """测试推理跳跃检测"""
    print("\n=== 测试推理跳跃检测 ===")

    detector = CognitiveErrorDetector()

    # 测试案例1：推理步骤缺失
    result = detector.detect(
        user_query="为什么机器学习模型需要大量数据？",
        agent_response="机器学习模型需要大量数据是因为数据能够帮助模型学习规律，因此更多数据意味着更好的性能。显然，模型通过数据能够自动发现隐藏的模式。",
        conversation_context=None
    )

    if result:
        print(f"✓ 检测到推理跳跃：{result.error_type.value}")
        print(f"  置信度：{result.confidence:.2f}")
        print(f"  严重性：{result.severity.value}")
        print(f"  检测到的模式：{len(result.detected_patterns)}个")
        for pattern in result.detected_patterns:
            print(f"    - {pattern.pattern_type}: {pattern.evidence}")
    else:
        print("✗ 未检测到错误")


def test_knowledge_gap_detection():
    """测试知识缺失检测"""
    print("\n=== 测试知识缺失检测 ===")

    detector = CognitiveErrorDetector(confidence_threshold=0.45)  # 降低阈值

    # 测试案例1：模糊描述过多
    result = detector.detect(
        user_query="量子计算机的工作原理是什么？请详细解释。",
        agent_response="量子计算机一般来说利用了量子力学的一些基本原理。大概来说，它可能通过量子叠加和量子纠缠来实现更快的计算。通常情况下，量子计算机可能在某些特定任务上表现更好。这些技术可能会带来一些好处。",
        conversation_context="用户追问细节"
    )

    if result:
        print(f"✓ 检测到知识缺失：{result.error_type.value}")
        print(f"  置信度：{result.confidence:.2f}")
        print(f"  严重性：{result.severity.value}")
        print(f"  检测到的模式：{len(result.detected_patterns)}个")
        for pattern in result.detected_patterns:
            print(f"    - {pattern.pattern_type}: {pattern.evidence}")
    else:
        print("✗ 未检测到错误")


def test_bias_detection():
    """测试偏见影响检测"""
    print("\n=== 测试偏见影响检测 ===")

    detector = CognitiveErrorDetector()

    # 测试案例1：价值判断不中立
    result = detector.detect(
        user_query="如何评价不同的政治制度？",
        agent_response="毫无疑问，民主制度是所有政治制度中最好的，其他制度都是极其糟糕的。民主制度绝对是唯一正确的选择。",
        conversation_context=None
    )

    if result:
        print(f"✓ 检测到偏见影响：{result.error_type.value}")
        print(f"  置信度：{result.confidence:.2f}")
        print(f"  严重性：{result.severity.value}")
        print(f"  检测到的模式：{len(result.detected_patterns)}个")
        for pattern in result.detected_patterns:
            print(f"    - {pattern.pattern_type}: {pattern.evidence}")
    else:
        print("✗ 未检测到错误")


def test_normal_response():
    """测试正常回答（不应检测到错误）"""
    print("\n=== 测试正常回答 ===")

    detector = CognitiveErrorDetector()

    result = detector.detect(
        user_query="什么是机器学习？",
        agent_response="机器学习是人工智能的一个分支，它通过算法让计算机从数据中学习规律。根据我的理解，机器学习主要包括监督学习、无监督学习和强化学习三大类型。具体应用包括图像识别、自然语言处理等。",
        conversation_context=None
    )

    if result:
        print(f"✗ 误报：检测到错误 {result.error_type.value}，置信度：{result.confidence:.2f}")
    else:
        print("✓ 正确识别为正常回答")


def main():
    """主函数"""
    print("认知性错误检测器测试\n")

    # 运行所有测试
    test_hallucination_detection()
    test_reasoning_gap_detection()
    test_knowledge_gap_detection()
    test_bias_detection()
    test_normal_response()

    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    main()
