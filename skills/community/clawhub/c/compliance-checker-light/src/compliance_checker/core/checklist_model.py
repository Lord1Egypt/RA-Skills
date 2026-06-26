"""
清单数据模型 (Pydantic v2)

定义审核清单的数据结构。
注意：此文件只包含数据模型定义和数据访问方法，不包含业务逻辑。
"""

import uuid
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class CheckMethod(str, Enum):
    """合规检查方法"""

    VISUAL = "visual"  # 视觉检查（印章、签名）
    TEXT = "text"  # 文本检查（编号、日期）
    BOTH = "both"  # 两者都需要


class SupportedFileType(str, Enum):
    """支持的文件类型"""

    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    TIFF = "tiff"
    BMP = "bmp"


class ValidityRule(BaseModel):
    """有效期规则"""

    cover_project: bool = Field(default=False, description="是否需覆盖项目周期")
    valid_from: Optional[str] = Field(default=None, description="有效期开始（YYYY-MM格式）")
    valid_to: Optional[str] = Field(default=None, description="有效期结束（YYYY-MM格式）")
    issue_after: Optional[str] = Field(default=None, description="签发日期不早于")
    issue_before: Optional[str] = Field(default=None, description="签发日期不晚于")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"cover_project": True, "valid_from": "2024-01", "valid_to": "2027-12"}
        }
    )


class CompliancePoint(BaseModel):
    """合规检查要点"""

    point: str = Field(description="检查项名称（如'公章'、'签字'）")
    required: bool = Field(default=True, description="是否必需")
    check_method: CheckMethod = Field(default=CheckMethod.TEXT, description="检查方法")
    search_context: Optional[str] = Field(default=None, description="OCR定位关键词")
    pattern: Optional[str] = Field(default=None, description="正则表达式（用于文本检查）")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "point": "公章",
                "required": True,
                "check_method": "visual",
                "search_context": "公章",
            }
        }
    )


class DocumentCheck(BaseModel):
    """文档检查项定义"""

    type: str = Field(description="检查类型 (completeness/timeliness/compliance/visual)")
    required: bool = Field(default=True, description="是否必需")
    # 时效性检查参数
    date_rules: Optional[List[Dict[str, Any]]] = Field(default=None, description="日期规则")
    # 合规性检查参数
    points: Optional[List[str]] = Field(default=None, description="检查要点列表")
    # 视觉检查参数
    target: Optional[str] = Field(default=None, description="视觉检测目标 (seal/signature)")
    search_context: Optional[str] = Field(default=None, description="OCR定位关键词")


class RequiredDocument(BaseModel):
    """必需文档定义"""

    name: str = Field(description="文档名称")
    aliases: List[str] = Field(default_factory=list, description="别名列表")
    file_types: List[SupportedFileType] = Field(
        default_factory=lambda: [SupportedFileType.PDF], description="支持的文件类型"
    )
    required: bool = Field(default=True, description="是否必需")
    validity: Optional[ValidityRule] = Field(default=None, description="有效期规则")
    compliance_points: List[CompliancePoint] = Field(
        default_factory=list, description="合规检查要点"
    )
    checks: List[DocumentCheck] = Field(default_factory=list, description="检查项配置列表")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "项目立项批复文件",
                "aliases": ["立项批复", "项目批复"],
                "type": ["pdf", "docx"],
                "required": True,
                "validity": {"cover_project": True},
                "compliance_points": [
                    {"point": "公章", "required": True, "check_method": "visual"}
                ],
            }
        }
    )


class ProjectPeriod(BaseModel):
    """项目周期"""

    start: Optional[str] = Field(default=None, description="项目开始时间（YYYY-MM格式）")
    end: Optional[str] = Field(default=None, description="项目结束时间（YYYY-MM格式）")

    model_config = ConfigDict(json_schema_extra={"example": {"start": "2025-01", "end": "2027-12"}})


class Checklist(BaseModel):
    """审核清单"""

    id: str = Field(default_factory=lambda: f"chk_{uuid.uuid4().hex[:8]}", description="清单ID")
    name: str = Field(description="清单名称")
    version: str = Field(default="1.0", description="版本号")
    project_period: Optional[ProjectPeriod] = Field(default=None, description="项目周期")
    required_documents: List[RequiredDocument] = Field(
        default_factory=list, description="必需文档列表"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "project_type_a",
                "name": "标准工程项目手续清单",
                "version": "1.0",
                "project_period": {"start": "2025-01", "end": "2027-12"},
                "required_documents": [],
            }
        }
    )

    def get_required_doc_by_name(self, name: str) -> Optional[RequiredDocument]:
        """根据名称获取必需文档定义"""
        for doc in self.required_documents:
            if doc.name == name or name in doc.aliases:
                return doc
        return None

    def get_all_required_names(self) -> List[str]:
        """获取所有必需文档的名称（包括别名）"""
        names = []
        for doc in self.required_documents:
            names.append(doc.name)
            names.extend(doc.aliases)
        return names


class ChecklistSummary(BaseModel):
    """清单摘要信息"""

    id: str
    name: str
    version: str
    total_documents: int
    required_count: int
    optional_count: int
