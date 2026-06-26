"""
简历漏洞穿透审计模块 - 5项审计指标 + 测谎面试题生成
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class SuspicionLevel(Enum):
    LOW = "低嫌疑"
    MEDIUM = "中嫌疑"
    HIGH = "高嫌疑"


@dataclass
class AuditIssue:
    """审计发现的单个问题"""
    category: str
    description: str
    risk_level: SuspicionLevel
    evidence: str
    suggested_question: Optional[str] = None


@dataclass
class LieDetectionQuestion:
    """测谎面试题"""
    question_type: str
    target: str
    content: str
    priority: int = 1


@dataclass
class ResumeAuditResult:
    """简历审计结果"""
    overall_conclusion: SuspicionLevel = SuspicionLevel.LOW
    high_suspicion_count: int = 0
    medium_suspicion_count: int = 0
    low_suspicion_count: int = 0
    issues: List[AuditIssue] = field(default_factory=list)
    lie_detection_questions: List[LieDetectionQuestion] = field(default_factory=list)
    confidence_score: float = 1.0


class ResumeAuditor:
    """简历漏洞穿透审计器"""

    # AI生成特征词
    AI_PATTERNS = [
        '赋能', '驱动', '重构', '闭环', '抓手', '底层逻辑',
        '从0到1', '从零到一', '价值最大化', '降本增效',
        '全链路', '全栈', '端到端', '颗粒度', '对齐',
        '打通', '沉淀', '输出', '赋能业务', '技术驱动',
    ]

    # 三段式模板特征
    TEMPLATE_PATTERNS = [
        r'负责.+项目[,，].*使用.+技术[,，].*取得.+成果',
        r'主导.+系统[,，].*基于.+框架[,，].*实现.+目标',
    ]

    def __init__(self, reference_guide: Optional[str] = None):
        self.reference_guide = reference_guide or ""
        self.issues: List[AuditIssue] = []

    def audit(self, resume_text: str, candidate_info: Optional[Dict] = None) -> ResumeAuditResult:
        """执行完整的简历漏洞穿透审计"""
        logger.info("开始简历漏洞穿透审计...")
        self.issues = []

        # 五项审计
        self._audit_high_value(resume_text, candidate_info)
        self._audit_detail_gaps(resume_text)
        self._audit_causality(resume_text)
        self._audit_ai_patterns(resume_text)
        self._audit_consistency(resume_text, candidate_info)

        # 统计
        result = ResumeAuditResult()
        result.issues = self.issues
        result.high_suspicion_count = sum(1 for i in self.issues if i.risk_level == SuspicionLevel.HIGH)
        result.medium_suspicion_count = sum(1 for i in self.issues if i.risk_level == SuspicionLevel.MEDIUM)
        result.low_suspicion_count = sum(1 for i in self.issues if i.risk_level == SuspicionLevel.LOW)

        # 综合结论
        total_high = result.high_suspicion_count
        total_medium = result.medium_suspicion_count
        if total_high >= 4:
            result.overall_conclusion = SuspicionLevel.HIGH
        elif total_high >= 2 or total_medium >= 3:
            result.overall_conclusion = SuspicionLevel.MEDIUM
        else:
            result.overall_conclusion = SuspicionLevel.LOW

        # 生成测谎题
        result.lie_detection_questions = self._generate_lie_detection_questions(resume_text)

        # 可信度计算
        result.confidence_score = self._calculate_confidence(result)

        logger.info(f"审计完成: {result.overall_conclusion.value}, 高嫌疑{total_high}项")
        return result

    def _audit_high_value(self, text: str, candidate_info: Optional[Dict]):
        """高阶含金量审计：横向对比商业常识"""
        # 检测夸张的增幅数据
        import re

        # 检测百分比增幅
        pct_patterns = [
            (r'(?:提升|增长|增加|提高|优化)[^。.!！?\n]{0,20}(\d{2,3})%', '高增幅'),
            (r'(?:降低|减少|下降|节省)[^。.!！?\n]{0,20}(\d{2,3})%', '高降幅'),
            (r'翻[了]?(\d+)倍', '倍数增长'),
            (r'从\d+[万]?[到至]\d+[万]?', '数量级变化'),
        ]

        for pattern, label in pct_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                value = int(match) if isinstance(match, str) and match.isdigit() else 0
                is_suspicious = False

                if label == '高增幅' and value >= 200:
                    is_suspicious = True
                elif label == '高降幅' and value >= 80:
                    is_suspicious = True
                elif label == '倍数增长' and value >= 3:
                    is_suspicious = True

                if is_suspicious:
                    self.issues.append(AuditIssue(
                        category="高阶含金量审计",
                        description=f"声称{label}（{match}），缺乏行业基线对比，需验证是否成立",
                        risk_level=SuspicionLevel.MEDIUM,
                        evidence=f"检测到: {match}",
                        suggested_question=f"这个{match}的增长是在什么时间段内实现的？同期行业/竞品表现如何？有具体的对比数据吗？"
                    ))

        # 检查是否有失败案例
        negative_keywords = ['失败', '踩坑', '教训', '不如预期', '放弃', '推倒重来', '回滚']
        has_negative = any(kw in text for kw in negative_keywords)
        if not has_negative and len(self.issues) > 0:
            self.issues.append(AuditIssue(
                category="高阶含金量审计",
                description="简历中未提及任何失败或挫折案例，真实工作必然有失败和妥协",
                risk_level=SuspicionLevel.LOW,
                evidence="全正向描述，无负面案例",
                suggested_question="在这个项目中，有没有遇到预期之外的困难或者失败的尝试？"
            ))

    def _audit_detail_gaps(self, text: str):
        """高势能低细节断层检测"""
        # 检测三段式模板
        import re
        for pattern in self.TEMPLATE_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    self.issues.append(AuditIssue(
                        category="高势能低细节断层",
                        description="检测到三段式模板描述：负责→使用→取得，缺乏独特长尾细节",
                        risk_level=SuspicionLevel.HIGH,
                        evidence=match[:100],
                        suggested_question="请详细描述这个项目中你遇到的最意外的技术挑战，以及你是怎么一步步解决的？"
                    ))

        # 检测技术选型是否有代价说明
        tech_choice_patterns = re.findall(r'[选采]用[了的]?\s*([A-Za-z0-9+\-./]+)', text)
        if tech_choice_patterns:
            has_tradeoff = any(kw in text for kw in ['代价', '牺牲', '权衡', 'tradeoff', '折中', '不足', '局限'])
            if not has_tradeoff:
                suspicious_techs = list(set(tech_choice_patterns))[:3]
                self.issues.append(AuditIssue(
                    category="高势能低细节断层",
                    description=f"技术选型（{', '.join(suspicious_techs)}）未说明任何代价或取舍，真实决策必有代价",
                    risk_level=SuspicionLevel.MEDIUM,
                    evidence=f"提及技术选型但无代价说明: {', '.join(suspicious_techs)}",
                    suggested_question=f"选择{', '.join(suspicious_techs)}时，有没有考虑过其他方案？你为什么没有选择那些方案？"
                ))

    def _audit_causality(self, text: str):
        """因果链断裂检测"""
        import re

        # 检测Action → Result的因果链条
        action_result_patterns = [
            r'(?:优化|改进|重构|升级)[^。.!！?\n]{0,30}(?:后|之后|以后)[^。.!！?\n]{0,20}(?:提升|增长|增加)',
        ]

        for pattern in action_result_patterns:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    # 检查是否有中间步骤说明
                    if len(match) < 50 and '因为' not in match and '由于' not in match:
                        self.issues.append(AuditIssue(
                            category="因果链断裂检测",
                            description=f"Action到Result之间缺少因果说明: {match[:80]}",
                            risk_level=SuspicionLevel.MEDIUM,
                            evidence=match[:100],
                            suggested_question="在这个优化中，你具体做了什么？为什么这个做法能带来你描述的效果？中间经过了什么步骤？"
                        ))

        # 检测结果是否超出合理预期
        unreasonable_results = re.findall(
            r'(?:前端|UI|界面|样式|CSS).*?(?:营收|收入|转化|GMV|付费).*?(?:提升|增长|增加)',
            text
        )
        for match in unreasonable_results:
            self.issues.append(AuditIssue(
                category="因果链断裂检测",
                description="前端优化声称带来营收/转化提升，因果链可能断裂",
                risk_level=SuspicionLevel.HIGH,
                evidence=match,
                suggested_question="你做的UI优化具体是如何影响营收的？这个因果关系你是如何验证的？有没有排除其他因素的影响？"
            ))

    def _audit_ai_patterns(self, text: str):
        """AI生成痕迹识别"""
        detected_patterns = []
        for pattern in self.AI_PATTERNS:
            count = text.count(pattern)
            if count > 0:
                detected_patterns.append((pattern, count))

        total_count = sum(c for _, c in detected_patterns)

        if total_count >= 8:
            level = SuspicionLevel.HIGH
        elif total_count >= 4:
            level = SuspicionLevel.MEDIUM
        elif total_count > 0:
            level = SuspicionLevel.LOW
        else:
            return

        top_patterns = sorted(detected_patterns, key=lambda x: x[1], reverse=True)[:5]
        self.issues.append(AuditIssue(
            category="AI生成痕迹识别",
            description=f"检测到{total_count}处AI生成特征词汇（{', '.join(p for p, _ in top_patterns)}），简历可能由AI辅助生成",
            risk_level=level,
            evidence=f"特征词: {', '.join(f'{p}(×{c})' for p, c in top_patterns)}",
            suggested_question="请用你自己的话，不用任何专业术语，描述一下你最近做的一个项目？"
        ))

    def _audit_consistency(self, text: str, candidate_info: Optional[Dict]):
        """逻辑一致性校验"""
        import re

        # 检查时间线
        year_pattern = r'20\d{2}'
        years = re.findall(year_pattern, text)
        if years:
            sorted_years = sorted(set(int(y) for y in years))
            if len(sorted_years) > 1:
                # 检测GPT-4使用时间
                if any(y < 2023 for y in sorted_years) and 'GPT-4' in text:
                    self.issues.append(AuditIssue(
                        category="逻辑一致性校验",
                        description="时间线疑点：GPT-4于2023年发布，但简历中可能在更早时间提及使用GPT-4",
                        risk_level=SuspicionLevel.HIGH,
                        evidence=f"提及GPT-4但时间线可能不匹配",
                        suggested_question="你最早是什么时候开始使用GPT-4的？具体用在什么场景？"
                    ))

    def _generate_lie_detection_questions(self, text: str) -> List[LieDetectionQuestion]:
        """根据审计结果生成测谎面试题"""
        questions = []

        # 基于审计问题生成追问
        high_issues = [i for i in self.issues if i.risk_level == SuspicionLevel.HIGH]
        medium_issues = [i for i in self.issues if i.risk_level == SuspicionLevel.MEDIUM]

        # 优先处理高嫌疑问题
        for issue in high_issues + medium_issues:
            if issue.suggested_question:
                questions.append(LieDetectionQuestion(
                    question_type="细节追问",
                    target=issue.category,
                    content=issue.suggested_question,
                    priority=1 if issue.risk_level == SuspicionLevel.HIGH else 2,
                ))

        # 如果没有具体问题，生成通用题
        if not questions:
            questions = self._generate_generic_questions(text)

        # 按优先级排序，限制数量
        questions.sort(key=lambda q: q.priority)
        return questions[:8]

    def _generate_generic_questions(self, text: str) -> List[LieDetectionQuestion]:
        """生成通用测谎题"""
        return [
            LieDetectionQuestion(
                question_type="决策还原",
                target="技术选型",
                content="请详细描述一个你做过的最重要的技术决策：当时有哪些备选方案？你是基于什么标准做出选择的？如果现在重新选，你会做出不同的选择吗？",
                priority=3,
            ),
            LieDetectionQuestion(
                question_type="边界条件",
                target="问题排查",
                content="请描述一次你遇到的最复杂的线上问题：问题现象是什么？排查过程是怎样的？最终根因是什么？你从这个过程中学到了什么？",
                priority=3,
            ),
            LieDetectionQuestion(
                question_type="协作验证",
                target="团队协作",
                content="在你最重要的项目中，你和谁协作最紧密？你们是如何分工的？有没有发生过意见分歧？怎么解决的？",
                priority=3,
            ),
        ]

    def _calculate_confidence(self, result: ResumeAuditResult) -> float:
        """计算审计可信度"""
        base = 1.0
        # 高嫌疑越多，可信度越低
        base -= result.high_suspicion_count * 0.1
        base -= result.medium_suspicion_count * 0.05
        return max(0.3, base)