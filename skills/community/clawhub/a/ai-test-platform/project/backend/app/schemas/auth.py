"""
授权相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AuthCodeCreate(BaseModel):
    """创建授权码请求"""
    code: str = Field(..., description="加密后的授权码")
    permission: str = Field(..., description="权限类型：all/generate/execute")
    expire_time: datetime = Field(..., description="过期时间")
    max_count: int = Field(..., description="最大使用次数")


class AuthCodeVerify(BaseModel):
    """验证授权码请求"""
    auth_code: str = Field(..., description="授权码")
    required_permission: Optional[str] = Field(None, description="需要的权限类型")


class AuthCodeResponse(BaseModel):
    """授权码响应"""
    id: int
    code: str
    permission: str
    expire_time: str
    use_count: int
    max_count: int
    is_active: int
    create_time: str

    class Config:
        from_attributes = True


class AuthVerifyResponse(BaseModel):
    """验证授权码响应"""
    valid: bool
    message: str
    permission: Optional[str] = None
    remaining_count: Optional[int] = None
