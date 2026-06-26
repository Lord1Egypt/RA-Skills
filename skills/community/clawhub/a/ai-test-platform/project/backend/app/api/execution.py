"""
测试执行管理 API 路由

提供执行器管理、任务调度和执行监控功能
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.services.execution_service import ExecutionManagementService
from app.schemas.execution import (
    ExecutorCreate, ExecutorResponse,
    TaskScheduleRequest, TaskCancelRequest,
    ExecutionQueueResponse, ExecutionStats
)
from app.schemas.ai import TaskProgressResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/execution", tags=["测试执行管理"])


def get_auth_code(request: Request) -> str:
    """从请求中获取授权码"""
    auth_code = request.headers.get("Authorization") or request.query_params.get("auth_code")
    if auth_code and auth_code.startswith("Bearer "):
        auth_code = auth_code[7:]
    return auth_code


# ==================== 执行器管理 ====================

@router.post("/executor", summary="创建执行器")
def create_executor(
    executor_data: ExecutorCreate,
    db: Session = Depends(get_db)
):
    """
    创建新的测试执行器

    - **name**: 执行器名称（唯一）
    - **type**: 执行器类型（api/ui）
    - **capacity**: 并发容量（默认5）
    - **max_tasks**: 最大任务数（默认100）
    - **config**: 执行器配置（可选）
    """
    if executor_data.type not in ["api", "ui"]:
        raise HTTPException(status_code=400, detail="执行器类型必须是api或ui")

    # 检查名称是否已存在
    service = ExecutionManagementService(db)
    if service.get_executor_by_name(executor_data.name):
        raise HTTPException(status_code=400, detail=f"执行器名称已存在: {executor_data.name}")

    try:
        executor = service.create_executor(executor_data)
        return {
            "code": 200,
            "msg": "执行器创建成功",
            "data": executor.to_dict()
        }
    except Exception as e:
        logger.error(f"创建执行器失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.get("/executor/list", summary="获取执行器列表")
def list_executors(
    type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取执行器列表

    - **type**: 执行器类型过滤（可选）
    - **status**: 状态过滤（可选）
    """
    service = ExecutionManagementService(db)
    executors = service.list_executors(type=type, status=status)

    return {
        "code": 200,
        "msg": "查询成功",
        "data": [ExecutorResponse(**executor.to_dict()) for executor in executors]
    }


@router.get("/executor/{executor_id}", summary="获取执行器详情")
def get_executor(
    executor_id: int,
    db: Session = Depends(get_db)
):
    """
    获取执行器详情

    - **executor_id**: 执行器ID
    """
    service = ExecutionManagementService(db)
    executor = service.get_executor(executor_id)

    if not executor:
        raise HTTPException(status_code=404, detail="执行器不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": executor.to_dict()
    }


@router.delete("/executor/{executor_id}", summary="删除执行器")
def delete_executor(
    executor_id: int,
    db: Session = Depends(get_db)
):
    """
    删除执行器

    - **executor_id**: 执行器ID
    """
    service = ExecutionManagementService(db)
    success = service.delete_executor(executor_id)

    if not success:
        raise HTTPException(status_code=404, detail="执行器不存在")

    return {"code": 200, "msg": "删除成功", "data": None}


@router.post("/executor/{executor_id}/heartbeat", summary="执行器心跳")
def executor_heartbeat(
    executor_id: int,
    current_load: Optional[int] = 0,
    db: Session = Depends(get_db)
):
    """
    执行器心跳（用于监控执行器状态）

    - **executor_id**: 执行器ID
    - **current_load**: 当前负载（可选）
    """
    service = ExecutionManagementService(db)
    success = service.heartbeat(executor_id, current_load)

    if not success:
        raise HTTPException(status_code=404, detail="执行器不存在")

    executor = service.get_executor(executor_id)
    return {
        "code": 200,
        "msg": "心跳成功",
        "data": executor.to_dict()
    }


# ==================== 任务调度 ====================

@router.post("/task/schedule", response_model=TaskProgressResponse, summary="调度测试任务")
def schedule_task(
    request: TaskScheduleRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    调度测试任务到执行队列

    - **script_id**: 脚本ID
    - **script_type**: 脚本类型
    - **priority**: 优先级（1-10，数字越小优先级越高）
    - **scheduled_time**: 计划执行时间（可选，默认立即执行）
    - **max_retries**: 最大重试次数（默认2）
    - **config**: 执行配置（可选）
    """
    auth_code = get_auth_code(http_request)

    if request.script_type not in ["api", "ui"]:
        raise HTTPException(status_code=400, detail="脚本类型必须是api或ui")

    try:
        service = ExecutionManagementService(db)
        task = service.schedule_task(request, auth_code)

        # 尝试自动分配
        scheduled = service.auto_schedule()

        return TaskProgressResponse(
            task_id=task.task_id,
            task_type=request.script_type,
            status=task.status,
            progress=0 if task.status == "pending" else 10,
            message="任务已调度" if scheduled else "任务已调度，等待执行器",
            result_data=None,
            create_time=task.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            update_time=task.create_time.strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        logger.error(f"调度任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"调度失败: {str(e)}")


@router.get("/task/list", summary="获取任务列表")
def list_tasks(
    status: Optional[str] = None,
    script_type: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取任务列表

    - **status**: 状态过滤（可选）
    - **script_type**: 脚本类型过滤（可选）
    - **limit**: 返回数量限制（默认100）
    """
    service = ExecutionManagementService(db)
    tasks = service.list_tasks(status=status, script_type=script_type, limit=limit)

    return {
        "code": 200,
        "msg": "查询成功",
        "data": [ExecutionQueueResponse(**task.to_dict()) for task in tasks]
    }


@router.get("/task/{task_id}", summary="获取任务详情")
def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    获取任务详情

    - **task_id**: 任务ID
    """
    service = ExecutionManagementService(db)
    task = service.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": task.to_dict()
    }


@router.post("/task/cancel", summary="取消任务")
def cancel_task(
    request: TaskCancelRequest,
    db: Session = Depends(get_db)
):
    """
    取消待执行的任务

    - **task_id**: 任务ID
    """
    service = ExecutionManagementService(db)
    success = service.cancel_task(request.task_id)

    if not success:
        raise HTTPException(status_code=400, detail="任务不存在或无法取消")

    return {"code": 200, "msg": "取消成功", "data": None}


# ==================== 执行监控 ====================

@router.get("/stats", summary="获取执行统计")
def get_execution_stats(
    db: Session = Depends(get_db)
):
    """
    获取执行统计信息

    返回：
    - 执行器统计（总数、活跃、空闲、忙碌、离线）
    - 任务统计（总数、等待中、运行中、已完成、失败）
    """
    service = ExecutionManagementService(db)
    stats = service.get_execution_stats()

    return {
        "code": 200,
        "msg": "查询成功",
        "data": stats.dict()
    }


@router.post("/auto-schedule", summary="自动调度任务")
def auto_schedule(
    db: Session = Depends(get_db)
):
    """
    自动调度：将待执行任务分配给空闲执行器

    返回成功调度的任务数量
    """
    try:
        service = ExecutionManagementService(db)
        count = service.auto_schedule()

        return {
            "code": 200,
            "msg": f"自动调度完成，分配了{count}个任务",
            "data": {"scheduled_count": count}
        }
    except Exception as e:
        logger.error(f"自动调度失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"调度失败: {str(e)}")


@router.post("/cleanup", summary="清理过期任务")
def cleanup_expired_tasks(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """
    清理过期任务

    - **hours**: 清理超过多少小时的已完成/失败任务（默认24小时）
    """
    try:
        service = ExecutionManagementService(db)
        count = service.cleanup_expired_tasks(hours)

        return {
            "code": 200,
            "msg": f"清理完成，删除了{count}个过期任务",
            "data": {"cleaned_count": count}
        }
    except Exception as e:
        logger.error(f"清理过期任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"清理失败: {str(e)}")
