"""
UI自动化测试 API 路由

管理UI测试脚本、Playwright执行和结果查询
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.services.ui_test_service import UiTestService
from app.services.task import TaskProgressService
from app.schemas.ui_test import (
    UiScriptCreate, UiScriptUpdate,
    BrowserConfig, UiExecuteRequest, UiExecuteBatchRequest, UiExecuteResult
)
from app.schemas.ai import GenerateResponse, TaskProgressResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ui", tags=["UI自动化"])


def get_auth_code(request: Request) -> str:
    """从请求中获取授权码"""
    auth_code = request.headers.get("Authorization") or request.query_params.get("auth_code")
    if auth_code and auth_code.startswith("Bearer "):
        auth_code = auth_code[7:]
    return auth_code


@router.post("/script", summary="创建UI测试脚本")
def create_script(
    script_data: UiScriptCreate,
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    创建UI测试脚本

    - **name**: 脚本名称
    - **content**: 脚本代码（Playwright）
    - **type**: 脚本类型（ui）
    """
    auth_code = get_auth_code(request)

    try:
        service = UiTestService(db)
        result = service.create_script(script_data, created_by=auth_code)
        return {
            "code": 200,
            "msg": "创建成功",
            "data": result
        }
    except Exception as e:
        logger.error(f"创建UI脚本失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.get("/script/list", summary="获取UI脚本列表")
def list_scripts(
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    获取所有UI测试脚本列表
    """
    auth_code = get_auth_code(request)

    service = UiTestService(db)
    scripts = service.list_scripts(created_by=auth_code)

    return {
        "code": 200,
        "msg": "查询成功",
        "data": [script.to_dict() for script in scripts]
    }


@router.get("/script/{script_id}", summary="获取UI脚本详情")
def get_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    根据ID获取UI脚本详情

    - **script_id**: 脚本ID
    """
    service = UiTestService(db)
    script = service.get_script(script_id)

    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": script.to_dict()
    }


@router.put("/script/{script_id}", summary="更新UI脚本")
def update_script(
    script_id: int,
    script_data: UiScriptUpdate,
    db: Session = Depends(get_db)
):
    """
    更新UI测试脚本

    - **script_id**: 脚本ID
    """
    service = UiTestService(db)
    result = service.update_script(script_id, script_data)

    if not result:
        raise HTTPException(status_code=404, detail="脚本不存在")

    return {
        "code": 200,
        "msg": "更新成功",
        "data": result
    }


@router.delete("/script/{script_id}", summary="删除UI脚本")
def delete_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    删除UI测试脚本

    - **script_id**: 脚本ID
    """
    service = UiTestService(db)
    success = service.delete_script(script_id)

    if not success:
        raise HTTPException(status_code=404, detail="脚本不存在")

    return {"code": 200, "msg": "删除成功", "data": None}


@router.post("/browser/config", summary="配置浏览器")
def configure_browser(
    script_id: int,
    config: BrowserConfig,
    db: Session = Depends(get_db)
):
    """
    配置浏览器参数

    - **script_id**: 脚本ID
    - **browser_type**: 浏览器类型（chromium/webkit/firefox）
    - **headless**: 是否无头模式
    - **viewport**: 视口大小
    - **slow_mo**: 操作延迟（毫秒）
    """
    service = UiTestService(db)
    success = service.configure_browser(script_id, config)

    if not success:
        raise HTTPException(status_code=404, detail="脚本不存在")

    return {
        "code": 200,
        "msg": "配置成功",
        "data": {
            "script_id": script_id,
            "browser_type": config.browser_type,
            "headless": config.headless
        }
    }


@router.get("/browser/config/{script_id}", summary="获取浏览器配置")
def get_browser_config(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    获取浏览器配置

    - **script_id**: 脚本ID
    """
    service = UiTestService(db)
    config = service.get_browser_config(script_id)

    return {
        "code": 200,
        "msg": "查询成功",
        "data": config
    }


@router.post("/execute", response_model=GenerateResponse, summary="执行单个UI测试脚本")
def execute_script(
    request: UiExecuteRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    执行单个UI测试脚本

    - **script_id**: 脚本ID
    - **browser_config**: 浏览器配置（可选）
    - **timeout**: 超时时间（秒），默认600秒
    """
    auth_code = get_auth_code(http_request)
    if not auth_code:
        raise HTTPException(status_code=401, detail="未提供授权码")

    try:
        service = UiTestService(db)

        # 使用asyncio创建后台任务
        import asyncio
        import uuid
        from app.services.task import TaskProgressService

        # 创建任务
        task_service = TaskProgressService(db)
        task_id = task_service.create_task("execute")

        # 启动后台执行
        asyncio.create_task(
            _execute_ui_script_task(
                task_id, request, service, task_service, auth_code
            )
        )

        return GenerateResponse(
            task_id=task_id,
            status="processing",
            message="UI测试执行任务已创建，请通过task_id查询进度"
        )
    except Exception as e:
        logger.error(f"创建UI执行任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


async def _execute_ui_script_task(task_id: str, request: UiExecuteRequest,
                                   service: UiTestService, task_service, auth_code: str):
    """后台执行UI脚本的异步任务"""
    try:
        # 更新任务状态
        task_service.update_task(task_id, status="processing", progress=10,
                                 message="正在执行UI测试...")

        # 执行脚本
        result = service.execute_script(request)

        # 更新任务状态
        from app.models.execute_record import ExecuteRecord
        from datetime import datetime

        # 保存执行记录
        db = task_service.db
        record = ExecuteRecord(
            script_id=request.script_id,
            auth_code=auth_code,
            result=result.get("result", "fail"),
            log=result.get("log", ""),
            execute_time=datetime.now(),
            duration=result.get("duration", 0)
        )
        db.add(record)
        db.commit()

        # 更新任务完成
        task_service.update_task(
            task_id,
            status="completed",
            progress=100,
            message="执行完成",
            result_data={
                "success": result.get("result") == "success",
                "duration": result.get("duration"),
                "screenshot_count": result.get("screenshot_count", 0),
                "trace_path": result.get("trace_path")
            }
        )

    except Exception as e:
        logger.error(f"执行UI脚本失败: {str(e)}")
        task_service.update_task(
            task_id,
            status="failed",
            progress=0,
            message=f"执行失败: {str(e)}"
        )


@router.post("/execute/batch", response_model=GenerateResponse, summary="批量执行UI测试脚本")
def execute_batch(
    request: UiExecuteBatchRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    批量执行UI测试脚本

    - **script_ids**: 脚本ID列表
    - **browser_config**: 浏览器配置（可选）
    - **timeout**: 总超时时间（秒），默认1200秒
    """
    auth_code = get_auth_code(http_request)
    if not auth_code:
        raise HTTPException(status_code=401, detail="未提供授权码")

    if not request.script_ids:
        raise HTTPException(status_code=400, detail="脚本ID列表不能为空")

    try:
        service = UiTestService(db)
        task_service = TaskProgressService(db)
        task_id = task_service.create_task("execute")

        # 启动后台批量执行
        import asyncio
        asyncio.create_task(
            _execute_ui_batch_task(
                task_id, request, service, task_service, auth_code
            )
        )

        return GenerateResponse(
            task_id=task_id,
            status="processing",
            message="批量UI测试执行任务已创建，请通过task_id查询进度"
        )
    except Exception as e:
        logger.error(f"创建批量UI执行任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


async def _execute_ui_batch_task(task_id: str, request: UiExecuteBatchRequest,
                                  service: UiTestService, task_service, auth_code: str):
    """后台批量执行UI脚本的异步任务"""
    try:
        total_scripts = len(request.script_ids)
        results = []

        for i, script_id in enumerate(request.script_ids):
            # 更新进度
            progress = int((i + 1) / total_scripts * 100)
            task_service.update_task(
                task_id,
                status="processing",
                progress=progress,
                message=f"正在执行 ({i + 1}/{total_scripts})..."
            )

            # 执行单个脚本
            exec_request = UiExecuteRequest(
                script_id=script_id,
                browser_config=request.browser_config,
                timeout=request.timeout // total_scripts
            )

            try:
                result = service.execute_script(exec_request)

                # 保存执行记录
                from app.models.execute_record import ExecuteRecord
                from datetime import datetime

                db = task_service.db
                record = ExecuteRecord(
                    script_id=script_id,
                    auth_code=auth_code,
                    result=result.get("result", "fail"),
                    log=result.get("log", ""),
                    execute_time=datetime.now(),
                    duration=result.get("duration", 0)
                )
                db.add(record)

                results.append(result)

            except Exception as e:
                logger.error(f"执行UI脚本失败 (script_id={script_id}): {str(e)}")
                results.append({
                    "script_id": script_id,
                    "result": "fail",
                    "log": str(e)
                })

        db.commit()

        # 汇总结果
        success_count = sum(1 for r in results if r.get("result") == "success")

        task_service.update_task(
            task_id,
            status="completed",
            progress=100,
            message=f"批量执行完成 - 成功: {success_count}, 失败: {total_scripts - success_count}",
            result_data={
                "total": total_scripts,
                "success": success_count,
                "fail": total_scripts - success_count,
                "results": results
            }
        )

    except Exception as e:
        logger.error(f"批量执行UI脚本失败: {str(e)}")
        task_service.update_task(
            task_id,
            status="failed",
            progress=0,
            message=f"批量执行失败: {str(e)}"
        )


@router.get("/screenshot/{script_id}/{screenshot_name}", summary="获取截图文件")
def get_screenshot(
    script_id: int,
    screenshot_name: str,
    db: Session = Depends(get_db)
):
    """
    获取UI测试截图文件

    - **script_id**: 脚本ID
    - **screenshot_name**: 截图文件名
    """
    service = UiTestService(db)
    screenshot_path = service.get_screenshot(script_id, screenshot_name)

    if not screenshot_path:
        raise HTTPException(status_code=404, detail="截图文件不存在")

    return FileResponse(screenshot_path, media_type="image/png")


@router.get("/trace/{script_id}", summary="获取Trace文件")
def get_trace_file(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    获取UI测试Trace文件（用于回放）

    - **script_id**: 脚本ID
    """
    service = UiTestService(db)
    trace_path = service.get_trace_file(script_id)

    if not trace_path:
        raise HTTPException(status_code=404, detail="Trace文件不存在")

    return FileResponse(trace_path, media_type="application/zip")
