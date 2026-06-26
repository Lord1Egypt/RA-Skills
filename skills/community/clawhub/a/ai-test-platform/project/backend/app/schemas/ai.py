"""
AI生成相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentUpload(BaseModel):
    """文档上传请求"""
    file_path: str = Field(..., description="文档文件路径")
    file_type: Optional[str] = Field(None, description="文件类型（自动识别）")


class TestCaseGenerateRequest(BaseModel):
    """测试用例生成请求"""
    document_content: str = Field(..., description="文档内容")
    requirements: Optional[str] = Field(None, description="额外需求说明")


class ApiScriptGenerateRequest(BaseModel):
    """API脚本生成请求"""
    document_content: str = Field(..., description="文档内容")
    api_info: Optional[str] = Field(None, description="API信息")


class UiScriptGenerateRequest(BaseModel):
    """UI脚本生成请求"""
    document_content: str = Field(..., description="文档内容")
    ui_info: Optional[str] = Field(None, description="UI信息")


class GenerateResponse(BaseModel):
    """生成响应"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    message: str = Field(..., description="提示消息")


class TaskProgressResponse(BaseModel):
    """任务进度响应"""
    task_id: str
    task_type: str
    status: str
    progress: int
    message: str
    result_data: Optional[str] = None
    create_time: str
    update_time: str

    class Config:
        from_attributes = True
