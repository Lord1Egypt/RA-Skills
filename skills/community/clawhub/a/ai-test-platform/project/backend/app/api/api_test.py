"""
接口自动化测试 API 路由

管理API测试脚本、配置、调试和执行
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.services.api_test_service import ApiTestService
from app.schemas.api_test import (
    ScriptCreate, ScriptUpdate, ScriptResponse,
    EnvironmentConfig, ExecuteRequest, ExecuteBatchRequest, ExecuteResult
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["接口自动化"])


def get_auth_code(request: Request) -> str:
    """从请求中获取授权码"""
    auth_code = request.headers.get("Authorization") or request.query_params.get("auth_code")
    if auth_code and auth_code.startswith("Bearer "):
        auth_code = auth_code[7:]
    return auth_code


@router.post("/script", response_model=ScriptResponse, summary="创建API测试脚本")
def create_script(
    script_data: ScriptCreate,
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    创建API测试脚本

    - **name**: 脚本名称
    - **content**: 脚本代码（Pytest + Requests）
    - **type**: 脚本类型（api）
    """
    auth_code = get_auth_code(request)

    if script_data.type != "api":
        raise HTTPException(status_code=400, detail="脚本类型必须是api")

    try:
        service = ApiTestService(db)
        result = service.create_script(script_data, created_by=auth_code)
        return result
    except Exception as e:
        logger.error(f"创建脚本失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.get("/script/list", response_model=List[ScriptResponse], summary="获取脚本列表")
def list_scripts(
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    获取所有API测试脚本列表
    """
    auth_code = get_auth_code(request)

    service = ApiTestService(db)
    scripts = service.list_scripts(created_by=auth_code)

    return [ScriptResponse(**script.to_dict()) for script in scripts]


@router.get("/script/{script_id}", response_model=ScriptResponse, summary="获取脚本详情")
def get_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    根据ID获取脚本详情

    - **script_id**: 脚本ID
    """
    service = ApiTestService(db)
    script = service.get_script(script_id)

    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    return ScriptResponse(**script.to_dict())


@router.put("/script/{script_id}", response_model=ScriptResponse, summary="更新脚本")
def update_script(
    script_id: int,
    script_data: ScriptUpdate,
    db: Session = Depends(get_db)
):
    """
    更新API测试脚本

    - **script_id**: 脚本ID
    - **name**: 脚本名称（可选）
    - **content**: 脚本代码（可选）
    - **status**: 状态（可选）
    """
    service = ApiTestService(db)
    result = service.update_script(script_id, script_data)

    if not result:
        raise HTTPException(status_code=404, detail="脚本不存在")

    return result


@router.delete("/script/{script_id}", summary="删除脚本")
def delete_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    删除API测试脚本

    - **script_id**: 脚本ID
    """
    service = ApiTestService(db)
    success = service.delete_script(script_id)

    if not success:
        raise HTTPException(status_code=404, detail="脚本不存在")

    return {"code": 200, "msg": "删除成功", "data": None}


@router.post("/script/{script_id}/debug", summary="调试脚本")
def debug_script(
    script_id: int,
    environment: str = None,
    db: Session = Depends(get_db)
):
    """
    调试API测试脚本（单次执行，不保存结果）

    - **script_id**: 脚本ID
    - **environment**: 环境名称（可选）
    """
    service = ApiTestService(db)
    result = service.debug_script(script_id, environment)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "code": 200,
        "msg": "调试完成",
        "data": result
    }


@router.post("/environment", summary="配置测试环境")
def configure_environment(
    config: EnvironmentConfig,
    db: Session = Depends(get_db)
):
    """
    配置测试环境

    - **name**: 环境名称（如：dev/test/prod）
    - **base_url**: 基础URL
    - **headers**: 全局请求头
    - **params**: 全局参数
    """
    service = ApiTestService(db)
    service.configure_environment(config)

    return {
        "code": 200,
        "msg": "环境配置成功",
        "data": {
            "name": config.name,
            "base_url": config.base_url
        }
    }


@router.get("/environment/{name}", summary="获取环境配置")
def get_environment(
    name: str,
    db: Session = Depends(get_db)
):
    """
    获取环境配置

    - **name**: 环境名称
    """
    service = ApiTestService(db)
    env = service.get_environment(name)

    if not env:
        raise HTTPException(status_code=404, detail="环境配置不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": env
    }
