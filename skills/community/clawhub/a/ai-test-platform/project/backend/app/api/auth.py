"""
授权管理 API 路由
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth import AuthCodeService
from app.schemas.auth import (
    AuthCodeCreate,
    AuthCodeVerify,
    AuthCodeResponse,
    AuthVerifyResponse
)
from typing import List
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["授权管理"])


@router.post("/verify", response_model=AuthVerifyResponse, summary="验证授权码")
def verify_auth_code(
    request: AuthCodeVerify,
    db: Session = Depends(get_db)
):
    """
    验证授权码有效性

    - **auth_code**: 授权码（加密后的）
    - **required_permission**: 需要的权限类型（可选）
    """
    auth_service = AuthCodeService(db)
    result = auth_service.verify_auth_code(request.auth_code, request.required_permission)
    return result


@router.get("/list", response_model=List[AuthCodeResponse], summary="获取所有授权码")
def list_auth_codes(db: Session = Depends(get_db)):
    """
    获取所有授权码列表
    """
    auth_service = AuthCodeService(db)
    auth_codes = auth_service.get_all_auth_codes()
    return [AuthCodeResponse(**auth_code.to_dict()) for auth_code in auth_codes]


@router.get("/{auth_code_id}", response_model=AuthCodeResponse, summary="获取授权码详情")
def get_auth_code(auth_code_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取授权码详情
    """
    auth_service = AuthCodeService(db)
    auth_code = auth_service.get_auth_code(auth_code_id)

    if not auth_code:
        raise HTTPException(status_code=404, detail="授权码不存在")

    return AuthCodeResponse(**auth_code.to_dict())


@router.post("/{auth_code_id}/disable", summary="禁用授权码")
def disable_auth_code(auth_code_id: int, db: Session = Depends(get_db)):
    """
    禁用授权码
    """
    auth_service = AuthCodeService(db)
    success = auth_service.disable_auth_code(auth_code_id)

    if not success:
        raise HTTPException(status_code=404, detail="授权码不存在")

    return {"code": 200, "msg": "禁用成功", "data": None}


@router.post("/{auth_code_id}/enable", summary="启用授权码")
def enable_auth_code(auth_code_id: int, db: Session = Depends(get_db)):
    """
    启用授权码
    """
    auth_service = AuthCodeService(db)
    success = auth_service.enable_auth_code(auth_code_id)

    if not success:
        raise HTTPException(status_code=404, detail="授权码不存在")

    return {"code": 200, "msg": "启用成功", "data": None}
