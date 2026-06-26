"""
测试执行 API 路由

处理测试任务的调度、执行和结果查询
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.services.execute_service import ExecuteService
from app.schemas.api_test import ExecuteRequest, ExecuteBatchRequest, ExecuteResult
from app.schemas.ai import GenerateResponse, TaskProgressResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/execute", tags=["测试执行"])


def get_auth_code(request: Request) -> str:
    """从请求中获取授权码"""
    auth_code = request.headers.get("Authorization") or request.query_params.get("auth_code")
    if auth_code and auth_code.startswith("Bearer "):
        auth_code = auth_code[7:]
    return auth_code


@router.post("/run", response_model=GenerateResponse, summary="执行单个测试脚本")
def execute_script(
    request: ExecuteRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    执行单个API测试脚本

    - **script_id**: 脚本ID
    - **environment**: 环境名称（可选）
    - **timeout**: 超时时间（秒），默认300秒
    """
    auth_code = get_auth_code(http_request)
    if not auth_code:
        raise HTTPException(status_code=401, detail="未提供授权码")

    try:
        service = ExecuteService(db)
        task_id = service.execute_script_async(request, auth_code)

        return GenerateResponse(
            task_id=task_id,
            status="processing",
            message="测试执行任务已创建，请通过task_id查询进度"
        )
    except Exception as e:
        logger.error(f"创建执行任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.post("/batch", response_model=GenerateResponse, summary="批量执行测试脚本")
def execute_batch(
    request: ExecuteBatchRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    批量执行测试脚本

    - **script_ids**: 脚本ID列表
    - **environment**: 环境名称（可选）
    - **timeout**: 总超时时间（秒），默认600秒
    """
    auth_code = get_auth_code(http_request)
    if not auth_code:
        raise HTTPException(status_code=401, detail="未提供授权码")

    if not request.script_ids:
        raise HTTPException(status_code=400, detail="脚本ID列表不能为空")

    try:
        service = ExecuteService(db)
        task_id = service.execute_batch_async(request, auth_code)

        return GenerateResponse(
            task_id=task_id,
            status="processing",
            message="批量执行任务已创建，请通过task_id查询进度"
        )
    except Exception as e:
        logger.error(f"创建批量执行任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.get("/progress/{task_id}", response_model=TaskProgressResponse, summary="查询执行进度")
def get_execute_progress(
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    查询测试执行任务的进度和结果

    - **task_id**: 任务ID
    """
    from app.services.task import TaskProgressService

    task_service = TaskProgressService(db)
    task_status = task_service.get_task_status(task_id)

    if not task_status:
        raise HTTPException(status_code=404, detail="任务不存在")

    return TaskProgressResponse(**task_status)


@router.get("/records", summary="获取执行记录列表")
def get_execute_records(
    script_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    获取执行记录列表

    - **script_id**: 脚本ID（可选，不提供则返回所有记录）
    - **limit**: 返回数量限制，默认100条
    """
    auth_code = get_auth_code(request)

    service = ExecuteService(db)
    records = service.get_execute_records(script_id=script_id, auth_code=auth_code, limit=limit)

    return {
        "code": 200,
        "msg": "查询成功",
        "data": records
    }


@router.get("/record/{record_id}", summary="获取执行记录详情")
def get_execute_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    获取执行记录详情

    - **record_id**: 记录ID
    """
    service = ExecuteService(db)
    record = service.get_record_detail(record_id)

    if not record:
        raise HTTPException(status_code=404, detail="执行记录不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": record
    }
