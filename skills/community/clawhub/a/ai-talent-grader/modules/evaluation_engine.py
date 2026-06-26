"""
评估引擎 - 六维度打分 + 双乘数加权 + 成长速度调整 + 级别判定
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class DimensionScore:
    """单个维度得分"""
    dimension: str
    score: float
    evidence: str
    cognitive_level: str


@dataclass
class WeightedResult:
    """加权计算结果"""
    average_score: float
    env_complexity: str
    env_coefficient: float
    leverage_level: str
    leverage_coefficient: float
    growth_level: str
    growth_adjustment: float
    weighted_score: float
    final_score: float


@dataclass
class FinalGrade:
    """最终定级"""
    level: int
    level_name: str
    p_level: str
    definition: str
    is_potential: bool = False
    is_weakness: bool = False
    is_downgraded: bool = False
    notes: List[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    """完整评估结果"""
    dimension_scores: List[DimensionScore]
    weighted_result: WeightedResult
    final_grade: FinalGrade
    risk_items: List[str] = field(default_factory=list)
    data_quality: Dict = field(default_factory=dict)


class EvaluationEngine:
    """AI人才评估引擎"""

    # 维度定义
    DIMENSIONS = [
        'ai_fluency',
        'human_ai_judgment',
        'architecture_design',
        'hybrid_orchestration',
        'cognitive_depth',
        'problem_modeling',
    ]

    DIMENSION_NAMES = {
        'ai_fluency': 'AI流利度',
        'human_ai_judgment': '人机判断力',
        'architecture_design': '架构设计力',
        'hybrid_orchestration': '混合编排力',
        'cognitive_depth': '认知深度',
        'problem_modeling': '问题建模能力',
    }

    # 级别定义
    LEVEL_DEFINITIONS = {
        1: {'name': 'AI工具使用者', 'p_level': 'P1-P3', 'definition': '能用工具完成指定任务'},
        2: {'name': 'AI协作者', 'p_level': 'P4-P5', 'definition': '能审校输出、识别幻觉'},
        3: {'name': 'AI架构者', 'p_level': 'P6-P7', 'definition': '设计AI驱动的业务流程，评估ROI'},
        4: {'name': 'AI战略者', 'p_level': 'P8+', 'definition': '定义AI与业务边界，规划组织演进'},
    }

    def __init__(self, config: Dict):
        self.config = config
        self.weights = config.get('weights', {})
        self.level_thresholds = config.get('level_thresholds', {})
        self.env_config = config.get('environment_complexity', {})
        self.leverage_config = config.get('personal_leverage', {})
        self.growth_config = config.get('growth_speed', {})
        self.scoring_discipline = config.get('scoring_discipline', [])
        self.non_balanced_rules = config.get('non_balanced_rules', {})

    def evaluate(
        self,
        dimension_scores: Dict[str, float],
        env_complexity: str,
        personal_leverage: str,
        growth_speed: str,
        evidence_map: Optional[Dict[str, str]] = None,
        cognitive_levels: Optional[Dict[str, str]] = None,
    ) -> EvaluationResult:
        """
        执行完整评估

        Args:
            dimension_scores: 六维度得分 {dimension: score}
            env_complexity: 环境复杂度 low/medium/high
            personal_leverage: 个人杠杆率 low/medium/high
            growth_speed: 成长速度 low/medium/high
            evidence_map: 各维度依据
            cognitive_levels: 各维度认知层级
        """
        logger.info("开始执行评估引擎...")

        # 1. 验证输入
        self._validate_input(dimension_scores)

        # 2. 构建维度得分
        evidence_map = evidence_map or {}
        cognitive_levels = cognitive_levels or {}
        scores = []
        for dim in self.DIMENSIONS:
            scores.append(DimensionScore(
                dimension=self.DIMENSION_NAMES[dim],
                score=dimension_scores.get(dim, 1),
                evidence=evidence_map.get(dim, '未提供'),
                cognitive_level=cognitive_levels.get(dim, '未评估'),
            ))

        # 3. 双乘数加权
        weighted = self._apply_double_multiplier(
            dimension_scores, env_complexity, personal_leverage, growth_speed
        )

        # 4. 级别判定
        grade = self._determine_grade(weighted, scores)

        # 5. 风险识别
        risks = self._identify_risks(scores, weighted)

        # 6. 数据质量评估
        data_quality = self._assess_data_quality(evidence_map, cognitive_levels)

        result = EvaluationResult(
            dimension_scores=scores,
            weighted_result=weighted,
            final_grade=grade,
            risk_items=risks,
            data_quality=data_quality,
        )

        logger.info(f"评估完成: L{grade.level} ({grade.level_name})")
        return result

    def _validate_input(self, scores: Dict[str, float]):
        """验证输入分数"""
        for dim in self.DIMENSIONS:
            if dim not in scores:
                raise ValueError(f"缺少维度分数: {dim}")
            score = scores[dim]
            if not (1 <= score <= 4):
                raise ValueError(f"分数超出范围(1-4): {dim}={score}")

    def _apply_double_multiplier(
        self,
        scores: Dict[str, float],
        env_complexity: str,
        personal_leverage: str,
        growth_speed: str,
    ) -> WeightedResult:
        """双乘数加权计算"""
        # 计算能力平均分
        average = sum(scores.values()) / len(scores)

        # 环境复杂度系数
        env_cfg = self.env_config.get(env_complexity, {})
        env_coef = env_cfg.get('coefficient', 1.0)

        # 个人杠杆率系数
        lev_cfg = self.leverage_config.get(personal_leverage, {})
        lev_coef = lev_cfg.get('coefficient', 1.0)

        # 成长速度调整
        growth_cfg = self.growth_config.get(growth_speed, {})
        growth_adj = growth_cfg.get('adjustment', 0)

        # 计算加权分
        weighted = (average * env_coef * lev_coef) + growth_adj
        final = weighted * 4  # 缩放到1-16

        logger.debug(
            f"加权计算: ({average:.2f} × {env_coef:.1f} × {lev_coef:.1f}) + {growth_adj:.1f} = {weighted:.2f} → {final:.2f}"
        )

        return WeightedResult(
            average_score=round(average, 2),
            env_complexity=env_complexity,
            env_coefficient=env_coef,
            leverage_level=personal_leverage,
            leverage_coefficient=lev_coef,
            growth_level=growth_speed,
            growth_adjustment=growth_adj,
            weighted_score=round(weighted, 2),
            final_score=round(final, 2),
        )

    def _determine_grade(
        self,
        weighted: WeightedResult,
        scores: List[DimensionScore],
    ) -> FinalGrade:
        """判定最终级别"""
        final_score = weighted.final_score

        # 根据阈值判定级别
        if final_score >= self.level_thresholds.get('l4', 15):
            level = 4
        elif final_score >= self.level_thresholds.get('l3', 12):
            level = 3
        elif final_score >= self.level_thresholds.get('l2', 8):
            level = 2
        else:
            level = 1

        grade_info = self.LEVEL_DEFINITIONS[level]
        grade = FinalGrade(
            level=level,
            level_name=grade_info['name'],
            p_level=grade_info['p_level'],
            definition=grade_info['definition'],
        )

        # L4硬性门槛检查
        if level == 4:
            arch_score = next((s.score for s in scores if s.dimension == '架构设计力'), 0)
            judge_score = next((s.score for s in scores if s.dimension == '人机判断力'), 0)

            if arch_score < 3 or judge_score < 3:
                grade.level = 3
                grade_info = self.LEVEL_DEFINITIONS[3]
                grade.level_name = grade_info['name']
                grade.p_level = grade_info['p_level']
                grade.definition = grade_info['definition']
                grade.is_downgraded = True
                grade.notes.append(
                    f"原始评估达L4，但架构设计力={arch_score:.0f}，人机判断力={judge_score:.0f}，"
                    f"不满足L4硬性门槛（均需≥3），降为L3"
                )

        # 非均衡型判定
        avg_level = level
        for s in scores:
            if s.score >= 3.5 and avg_level <= 2:
                grade.is_potential = True
                grade.notes.append(f"潜力型：{s.dimension}突出（得分{s.score:.0f}），综合级别L{avg_level}")
            if s.score <= 1.5 and avg_level >= 3:
                grade.is_weakness = True
                grade.notes.append(f"短板型：{s.dimension}薄弱（得分{s.score:.0f}），综合级别L{avg_level}")

        return grade

    def _identify_risks(
        self,
        scores: List[DimensionScore],
        weighted: WeightedResult,
    ) -> List[str]:
        """识别风险项"""
        risks = []

        # 短板维度风险
        for s in scores:
            if s.score <= 1.5:
                risks.append(f"短板风险：{s.dimension}得分偏低({s.score:.0f}/4)，可能影响实际工作表现")
            if s.cognitive_level in ['L1 表面使用', 'L2 知其然']:
                risks.append(f"认知深度风险：{s.dimension}认知层级为{s.cognitive_level}，建议深入考察")

        # 面试质量风险
        no_evidence_dims = [s.dimension for s in scores if s.evidence in ['未提供', '']]
        if no_evidence_dims:
            risks.append(f"依据缺失：{', '.join(no_evidence_dims)}维度缺乏评估依据，定级可信度降低")

        # 均衡性风险
        score_values = [s.score for s in scores]
        if max(score_values) - min(score_values) >= 2:
            risks.append(f"均衡性风险：能力分布不均衡（最高{max(score_values):.0f} vs 最低{min(score_values):.0f}），存在明显短板")

        return risks

    def _assess_data_quality(
        self,
        evidence_map: Dict[str, str],
        cognitive_levels: Dict[str, str],
    ) -> Dict:
        """评估数据质量"""
        provided_evidence = sum(1 for v in evidence_map.values() if v and v != '未提供')
        provided_cognitive = sum(1 for v in cognitive_levels.values() if v and v != '未评估')

        resume_completeness = min(5, max(1, provided_evidence // 2 + 1))
        interview_quality = min(5, max(1, provided_cognitive // 2 + 1))
        confidence = min(5, max(1, (provided_evidence + provided_cognitive) // 3 + 1))

        return {
            'resume_completeness': resume_completeness,
            'interview_quality': interview_quality,
            'confidence': confidence,
        }