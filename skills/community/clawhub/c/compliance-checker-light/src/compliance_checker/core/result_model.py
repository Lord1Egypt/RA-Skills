"""
检查结果数据模型 (Pydantic v2)

定义合规检查的结果数据结构。
注意：此文件只包含数据模型定义和数据访问方法，不包含业务逻辑。
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from .checker_base import CheckStatus


class MatchType(str, Enum):
    """匹配类型"""

    EXACT = "exact"  # 精确匹配
    SEMANTIC = "semantic"  # 语义匹配
    ALIAS = "alias"  # 别名匹配
    NONE = "none"  # 无匹配


class DocumentMatch(BaseModel):
    """文档匹配结果"""

    document_name: str = Field(description="清单中的文档名称")
    status: CheckStatus = Field(description="匹配状态")
    matched_file: Optional[str] = Field(default=None, description="匹配到的文件名")
    match_type: MatchType = Field(default=MatchType.NONE, description="匹配类型")
    similarity: float = Field(default=0.0, description="相似度分数(0-1)")
    requirement: str = Field(default="必须上传", description="要求说明")


class CompletenessResult(BaseModel):
    """完整性检查结果"""

    status: CheckStatus = Field(description="整体状态")
    total_required: int = Field(description="必需文档总数")
    uploaded: int = Field(description="已上传数量")
    missing: int = Field(description="缺失数量")
    details: List[DocumentMatch] = Field(default_factory=list, description="详细匹配结果")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "INCOMPLETE",
                "total_required": 10,
                "uploaded": 8,
                "missing": 2,
                "details": [],
            }
        }
    )

    def has_issues(self) -> bool:
        """是否有问题（缺失或不合格）"""
        return self.status in (CheckStatus.INCOMPLETE, CheckStatus.HAS_ISSUES) or self.missing > 0


class TimelinessDetail(BaseModel):
    """时效性检查详情"""

    document_name: str = Field(description="文档名称")
    file_path: str = Field(description="文件路径")
    validity: Dict[str, Any] = Field(description="有效期信息")
    project_period: Dict[str, str] = Field(description="项目周期")
    status: CheckStatus = Field(description="时效状态")
    message: str = Field(description="状态说明")


class TimelinessResult(BaseModel):
    """时效性检查结果"""

    status: CheckStatus = Field(description="整体状态")
    checked: int = Field(description="检查文档数")
    valid: int = Field(description="有效数量")
    expired: int = Field(description="过期数量")
    unclear: int = Field(description="不明确数量")
    details: List[TimelinessDetail] = Field(default_factory=list, description="详细检查结果")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "HAS_ISSUES",
                "checked": 8,
                "valid": 6,
                "expired": 1,
                "unclear": 1,
                "details": [],
            }
        }
    )


class ComplianceCheckItem(BaseModel):
    """单项合规检查结果"""

    point: str = Field(description="检查项名称")
    found: bool = Field(description="是否发现")
    status: CheckStatus = Field(default=CheckStatus.UNCLEAR, description="检查状态")
    value: Optional[str] = Field(default=None, description="发现的值")
    pattern: Optional[str] = Field(default=None, description="匹配的模式")
    evidence: Optional[str] = Field(default=None, description="证据文本")
    message: Optional[str] = Field(default=None, description="说明信息")


class DocumentCompliance(BaseModel):
    """单个文档的合规检查结果"""

    document_name: str = Field(description="文档名称")
    file_path: str = Field(description="文件路径")
    checks: List[ComplianceCheckItem] = Field(default_factory=list, description="检查项列表")

    def get_failed_checks(self) -> List[ComplianceCheckItem]:
        """获取失败的检查项"""
        return [c for c in self.checks if c.status in (CheckStatus.FAIL, CheckStatus.MISSING)]

    def get_passed_checks(self) -> List[ComplianceCheckItem]:
        """获取通过的检查项"""
        return [c for c in self.checks if c.status == CheckStatus.PASS]


class ComplianceResult(BaseModel):
    """合规性检查结果"""

    status: CheckStatus = Field(description="整体状态")
    details: List[DocumentCompliance] = Field(default_factory=list, description="各文档检查结果")

    def get_failed_documents(self) -> List[DocumentCompliance]:
        """获取有问题的文档"""
        return [d for d in self.details if d.get_failed_checks()]


class IssueItem(BaseModel):
    """问题项"""

    index: int = Field(description="序号")
    issue_type: str = Field(description="问题类型")
    document_name: str = Field(description="关联文件")
    description: str = Field(description="问题描述")
    screenshot_path: Optional[str] = Field(default=None, description="截图路径")
    page_num: Optional[int] = Field(default=None, description="问题所在页码")


class CheckSummary(BaseModel):
    """检查摘要"""

    project_id: Optional[str] = Field(default=None, description="项目ID")
    checklist_id: Optional[str] = Field(default=None, description="清单ID")
    check_time: datetime = Field(default_factory=datetime.now, description="检查时间")
    total_documents: int = Field(description="文档总数")
    completeness_status: CheckStatus = Field(description="完整性状态")
    timeliness_status: CheckStatus = Field(description="时效性状态")
    compliance_status: CheckStatus = Field(description="合规性状态")
    overall_status: CheckStatus = Field(description="总体状态")


class FullCheckResult(BaseModel):
    """
    完整检查结果

    包含完整性、时效性、合规性三大检查的结果
    """

    status: CheckStatus = Field(description="总体状态")
    summary: CheckSummary = Field(description="检查摘要")
    completeness: Optional[CompletenessResult] = Field(default=None, description="完整性结果")
    timeliness: Optional[TimelinessResult] = Field(default=None, description="时效性结果")
    compliance: Optional[ComplianceResult] = Field(default=None, description="合规性结果")
    issues: List[IssueItem] = Field(default_factory=list, description="问题清单")
    report_path: Optional[str] = Field(default=None, description="报告文件路径")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "HAS_ISSUES",
                "summary": {
                    "project_id": "project_123",
                    "checklist_id": "project_type_a",
                    "check_time": "2025-03-06T10:30:00",
                    "total_documents": 8,
                    "completeness_status": "INCOMPLETE",
                    "timeliness_status": "HAS_ISSUES",
                    "compliance_status": "PASS",
                    "overall_status": "HAS_ISSUES",
                },
                "issues": [],
            }
        }
    )

    def add_issue(
        self,
        issue_type: str,
        document_name: str,
        description: str,
        page_num: Optional[int] = None,
        screenshot_path: Optional[str] = None,
    ) -> None:
        """添加问题项"""
        issue = IssueItem(
            index=len(self.issues) + 1,
            issue_type=issue_type,
            document_name=document_name,
            description=description,
            page_num=page_num,
            screenshot_path=screenshot_path,
        )
        self.issues.append(issue)

    def has_issues(self) -> bool:
        """是否存在问题"""
        return len(self.issues) > 0

    def get_issues_by_type(self, issue_type: str) -> List[IssueItem]:
        """按类型获取问题"""
        return [i for i in self.issues if i.issue_type == issue_type]
