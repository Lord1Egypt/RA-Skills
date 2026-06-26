"""
面试分析模块 - 面试交叉验证与内容分析
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class VerificationStatus(Enum):
    CONFIRMED = "已确认（存疑）"
    EXCLUDED = "已排除"
    PENDING = "待验证"
    NOT_COVERED = "未覆盖"


@dataclass
class CrossVerificationItem:
    """交叉验证项"""
    audit_issue: str
    question_asked: bool
    candidate_response: Optional[str]
    status: VerificationStatus
    notes: str


@dataclass
class InterviewAnalysisResult:
    """面试分析结果"""
    total_issues: int = 0
    covered: int = 0
    confirmed: int = 0
    excluded: int = 0
    pending: int = 0
    not_covered: int = 0
    items: List[CrossVerificationItem] = field(default_factory=list)
    overall_quality_score: float = 1.0
    key_observations: List[str] = field(default_factory=list)


class InterviewAnalyzer:
    """面试记录分析器"""

    def __init__(self):
        pass

    def cross_verify(
        self,
        audit_issues: List,
        interview_text: str,
        interview_record: Optional[Dict] = None,
    ) -> InterviewAnalysisResult:
        """
        面试交叉验证：将面试记录与审计疑点逐项对比
        """
        logger.info("开始面试交叉验证...")
        result = InterviewAnalysisResult()
        result.total_issues = len(audit_issues)

        for issue in audit_issues:
            item = self._verify_single_issue(issue, interview_text)
            result.items.append(item)

            if item.status == VerificationStatus.CONFIRMED:
                result.confirmed += 1
                result.covered += 1
            elif item.status == VerificationStatus.EXCLUDED:
                result.excluded += 1
                result.covered += 1
            elif item.status == VerificationStatus.PENDING:
                result.pending += 1
                result.covered += 1
            else:
                result.not_covered += 1

        # 计算面试质量分数
        if result.total_issues > 0:
            result.overall_quality_score = result.covered / result.total_issues

        logger.info(f"交叉验证完成: 覆盖{result.covered}/{result.total_issues}")
        return result

    def _verify_single_issue(self, issue, interview_text: str) -> CrossVerificationItem:
        """验证单个审计疑点"""
        # 检查问题是否被问到
        suggested_q = getattr(issue, 'suggested_question', None)
        if suggested_q:
            # 使用关键词匹配判断问题是否被覆盖
            keywords = set(suggested_q[:30])  # 取前30个字符作为关键词
            question_asked = any(kw in interview_text for kw in keywords if len(kw) > 2)
        else:
            question_asked = False

        # 即使问题没被直接问到，如果面试中涉及相关话题也算覆盖
        category = getattr(issue, 'category', '')
        category_covered = category and category[:4] in interview_text

        is_covered = question_asked or category_covered

        if not is_covered:
            return CrossVerificationItem(
                audit_issue=issue.description,
                question_asked=False,
                candidate_response=None,
                status=VerificationStatus.NOT_COVERED,
                notes=f"面试未覆盖: {issue.category}",
            )

        # 分析回答质量（简化版：基于回答长度和关键词）
        # 在实际使用中，这部分应该由LLM进行更深入的分析
        status = VerificationStatus.PENDING
        notes = "面试已涉及但需进一步判断"

        return CrossVerificationItem(
            audit_issue=issue.description,
            question_asked=question_asked,
            candidate_response="[需要LLM分析]",
            status=status,
            notes=notes,
        )

    def extract_key_observations(
        self,
        interview_text: str,
        candidate_info: Optional[Dict] = None,
    ) -> List[str]:
        """从面试记录中提取关键观察"""
        observations = []

        # 检查面试记录的完整度
        if len(interview_text) < 500:
            observations.append("面试记录内容较少，可能不完整，评估可信度将降低")
        elif len(interview_text) < 2000:
            observations.append("面试记录内容中等，部分细节可能缺失")

        # 检查是否有结构化评估
        has_structure = any(
            kw in interview_text
            for kw in ['评分', '分数', '评价', '结论', '建议', '总结']
        )
        if not has_structure:
            observations.append("面试记录缺乏结构化评估结论")

        # 检查是否有具体案例
        has_examples = any(
            kw in interview_text
            for kw in ['例如', '比如', '案例', '举例', '具体', '当时']
        )
        if not has_examples:
            observations.append("面试回答缺乏具体案例支撑，可能停留在表面")

        return observations

    def evaluate_interview_quality(self, interview_text: str) -> Dict:
        """评估面试记录的质量"""
        quality = {
            'length': len(interview_text),
            'has_structure': False,
            'has_examples': False,
            'has_qa_format': False,
            'has_scores': False,
            'overall': 'low',
        }

        # 检查结构化程度
        quality['has_structure'] = any(
            kw in interview_text
            for kw in ['评分', '分数', '评价', '结论', '建议']
        )

        # 检查案例丰富度
        quality['has_examples'] = any(
            kw in interview_text
            for kw in ['例如', '比如', '案例', '举例']
        )

        # 检查是否有Q&A格式
        quality['has_qa_format'] = 'Q' in interview_text and 'A' in interview_text

        # 检查是否有评分
        quality['has_scores'] = any(
            kw in interview_text
            for kw in ['打分', '评级', '等级']
        )

        # 综合判断
        score = sum([
            quality['has_structure'],
            quality['has_examples'],
            quality['has_qa_format'],
            quality['has_scores'],
            quality['length'] > 2000,
        ])

        if score >= 4:
            quality['overall'] = 'high'
        elif score >= 2:
            quality['overall'] = 'medium'
        else:
            quality['overall'] = 'low'

        return quality