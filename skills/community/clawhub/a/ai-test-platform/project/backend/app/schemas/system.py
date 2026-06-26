"""
系统管理相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


# ==================== AI模型配置 ====================

class AIModelConfigCreate(BaseModel):
    """创建AI模型配置请求"""
    name: str = Field(..., description="配置名称")
    model_type: str = Field(..., description="模型类型：online/local")
    provider: Optional[str] = Field(None, description="提供商：deepseek/openai/local")
    model_name: Optional[str] = Field(None, description="模型名称")
    api_key: Optional[str] = Field(None, description="API密钥")
    api_base_url: Optional[str] = Field(None, description="API基础URL")
    max_tokens: int = Field(default=2000, description="最大token数")
    temperature: int = Field(default=70, description="温度参数（0-100）")
    timeout: int = Field(default=30, description="超时时间（秒）")
    max_retries: int = Field(default=2, description="最大重试次数")
    is_default: bool = Field(default=False, description="是否默认配置")
    config_data: Optional[Dict] = Field(default={}, description="额外配置")


class AIModelConfigUpdate(BaseModel):
    """更新AI模型配置请求"""
    name: Optional[str] = None
    provider: Optional[str] = None
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[int] = None
    timeout: Optional[int] = None
    max_retries: Optional[int] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    config_data: Optional[Dict] = None


class AIModelConfigResponse(BaseModel):
    """AI模型配置响应"""
    id: int
    name: str
    model_type: str
    provider: Optional[str]
    model_name: Optional[str]
    api_base_url: Optional[str]
    max_tokens: int
    temperature: int
    timeout: int
    max_retries: int
    is_active: bool
    is_default: bool
    create_time: str
    update_time: str

    class Config:
        from_attributes = True


# ==================== 测试环境 ====================

class EnvironmentCreate(BaseModel):
    """创建测试环境请求"""
    name: str = Field(..., description="环境名称")
    env_type: str = Field(..., description="环境类型：dev/test/staging/prod")
    base_url: str = Field(..., description="基础URL")
    description: Optional[str] = Field(None, description="环境描述")
    headers: Optional[Dict] = Field(default={}, description="全局请求头")
    params: Optional[Dict] = Field(default={}, description="全局参数")
    variables: Optional[Dict] = Field(default={}, description="环境变量")
    is_default: bool = Field(default=False, description="是否默认环境")


class EnvironmentUpdate(BaseModel):
    """更新测试环境请求"""
    name: Optional[str] = None
    env_type: Optional[str] = None
    base_url: Optional[str] = None
    description: Optional[str] = None
    headers: Optional[Dict] = None
    params: Optional[Dict] = None
    variables: Optional[Dict] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class EnvironmentResponse(BaseModel):
    """测试环境响应"""
    id: int
    name: str
    env_type: str
    base_url: str
    description: Optional[str]
    is_active: bool
    is_default: bool
    create_time: str
    update_time: str

    class Config:
        from_attributes = True


# ==================== 操作日志 ====================

class OperationLogResponse(BaseModel):
    """操作日志响应"""
    id: int
    user_id: Optional[str]
    operation_type: str
    operation_module: Optional[str]
    operation_desc: Optional[str]
    request_method: Optional[str]
    request_url: Optional[str]
    response_status: Optional[int]
    ip_address: Optional[str]
    duration: Optional[int]
    create_time: str

    class Config:
        from_attributes = True


# ==================== 数据备份 ====================

class BackupCreate(BaseModel):
    """创建备份请求"""
    name: str = Field(..., description="备份名称")
    backup_type: str = Field(default="full", description="备份类型：full/incremental")
    backup_scope: str = Field(default="all", description="备份范围：database/files/all")
    backup_config: Optional[Dict] = Field(default={}, description="备份配置")


class BackupResponse(BaseModel):
    """备份响应"""
    id: int
    name: str
    backup_type: str
    backup_scope: str
    file_path: Optional[str]
    file_size: Optional[int]
    status: str
    error_message: Optional[str]
    create_time: str
    complete_time: Optional[str]

    class Config:
        from_attributes = True


class BackupRestoreRequest(BaseModel):
    """恢复备份请求"""
    backup_id: int = Field(..., description="备份ID")
    restore_scope: str = Field(default="all", description="恢复范围：database/files/all")
