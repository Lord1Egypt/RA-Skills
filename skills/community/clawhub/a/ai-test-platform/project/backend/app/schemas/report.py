"""
测试报告相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional


class ReportGenerateRequest(BaseModel):
    """生成报告请求"""
    record_id: int = Field(..., description="执行记录ID")
    include_ai_analysis: bool = Field(default=True, description="是否包含AI分析")


class ReportExportRequest(BaseModel):
    """导出报告请求"""
    report_id: int = Field(..., description="报告ID")
    format: str = Field(..., description="导出格式：html/pdf")
    include_screenshots: bool = Field(default=True, description="是否包含截图")


class ReportResponse(BaseModel):
    """报告响应"""
    id: int
    record_id: int
    script_id: int
    script_name: str
    script_type: str
    result: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    duration: int
    report_path: Optional[str]
    log_content: Optional[str]
    ai_analysis: Optional[str]
    create_time: str

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    """报告列表响应"""
    id: int
    script_name: str
    script_type: str
    result: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    duration: int
    create_time: str


class AiAnalysisRequest(BaseModel):
    """AI分析请求"""
    report_id: int = Field(..., description="报告ID")
    log_content: str = Field(..., description="执行日志")


class AiAnalysisResponse(BaseModel):
    """AI分析响应"""
    report_id: int
    analysis_result: str
    failure_reason: str
    suggestions: str
