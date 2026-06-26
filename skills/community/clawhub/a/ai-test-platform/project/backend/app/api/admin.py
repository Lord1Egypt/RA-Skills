"""
管理员 API 路由
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth import AuthCodeService
from app.schemas.auth import AuthCodeResponse, AuthVerifyResponse
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/admin", tags=["管理员"])


class CreateAuthCodeRequest(BaseModel):
    """创建授权码请求"""
    permission: str  # all/generate/execute
    max_days: Optional[int] = 365
    max_count: Optional[int] = 100


class CreateAuthCodeResponse(BaseModel):
    """创建授权码响应"""
    encrypted_code: str  # 加密后的授权码（用户使用）
    permission: str
    expire_time: str
    max_count: int
    # 注意：不返回原始授权码和加密密钥，保护安全


@router.post("/create_auth", response_model=CreateAuthCodeResponse, summary="创建授权码")
def create_auth_code(
    request: CreateAuthCodeRequest,
    db: Session = Depends(get_db)
):
    """
    管理员创建授权码

    - **permission**: 权限类型 (all/generate/execute)
    - **max_days**: 有效期（天），默认365天
    - **max_count**: 最大使用次数，默认100次

    注意：此接口不受授权拦截限制，允许管理员操作
    """
    # 验证权限类型
    valid_permissions = ["all", "generate", "execute"]
    if request.permission not in valid_permissions:
        raise HTTPException(
            status_code=400,
            detail=f"无效的权限类型，必须是 {valid_permissions} 之一"
        )

    # 创建授权码
    auth_service = AuthCodeService(db)
    result = auth_service.create_auth_code(
        permission=request.permission,
        max_days=request.max_days,
        max_count=request.max_count
    )

    return CreateAuthCodeResponse(
        encrypted_code=result["encrypted_code"],
        permission=result["permission"],
        expire_time=result["expire_time"].strftime("%Y-%m-%d %H:%M:%S"),
        max_count=result["max_count"]
    )


@router.post("/verify_auth", response_model=AuthVerifyResponse, summary="验证授权码")
def verify_auth_code(
    auth_code: str,
    required_permission: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    管理员验证授权码（不增加使用次数）
    """
    auth_service = AuthCodeService(db)
    result = auth_service.verify_auth_code(auth_code, required_permission)
    return result
