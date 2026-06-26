"""
接口自动化测试相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class ScriptCreate(BaseModel):
    """创建脚本请求"""
    name: str = Field(..., description="脚本名称")
    content: str = Field(..., description="脚本代码")
    type: str = Field(..., description="脚本类型：api/ui")


class ScriptUpdate(BaseModel):
    """更新脚本请求"""
    name: Optional[str] = Field(None, description="脚本名称")
    content: Optional[str] = Field(None, description="脚本代码")
    status: Optional[str] = Field(None, description="状态：active/archived")


class ScriptResponse(BaseModel):
    """脚本响应"""
    id: int
    name: str
    content: str
    type: str
    status: str
    created_by: Optional[str]
    create_time: str
    update_time: str

    class Config:
        from_attributes = True


class EnvironmentConfig(BaseModel):
    """环境配置"""
    name: str = Field(..., description="环境名称")
    base_url: str = Field(..., description="基础URL")
    headers: Optional[Dict[str, str]] = Field(default={}, description="全局请求头")
    params: Optional[Dict[str, str]] = Field(default={}, description="全局参数")


class ExecuteRequest(BaseModel):
    """执行请求"""
    script_id: int = Field(..., description="脚本ID")
    environment: Optional[str] = Field(None, description="环境名称")
    timeout: Optional[int] = Field(default=300, description="超时时间（秒）")


class ExecuteBatchRequest(BaseModel):
    """批量执行请求"""
    script_ids: List[int] = Field(..., description="脚本ID列表")
    environment: Optional[str] = Field(None, description="环境名称")
    timeout: Optional[int] = Field(default=600, description="总超时时间（秒）")


class ExecuteResult(BaseModel):
    """执行结果"""
    script_id: int
    script_name: str
    result: str  # success/fail
    duration: int  # 执行耗时（秒）
    log: str
    report_path: Optional[str] = None
