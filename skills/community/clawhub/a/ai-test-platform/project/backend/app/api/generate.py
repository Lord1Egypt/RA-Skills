"""
AI生成 API 路由

处理测试用例、API脚本、UI脚本的生成请求
"""

import os
import asyncio
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.core.config import settings
from app.services.ai_generator import AIGeneratorService
from app.services.document_parser import DocumentParser
from app.services.task import TaskProgressService
from app.schemas.ai import (
    TestCaseGenerateRequest,
    ApiScriptGenerateRequest,
    UiScriptGenerateRequest,
    GenerateResponse,
    TaskProgressResponse
)
from app.models.test_case import TestCase
from app.models.script import AutoScript

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/generate", tags=["AI生成"])


def get_auth_code(request: Request) -> str:
    """从请求中获取授权码"""
    auth_code = request.headers.get("Authorization") or request.query_params.get("auth_code")
    if auth_code and auth_code.startswith("Bearer "):
        auth_code = auth_code[7:]
    return auth_code


@router.post("/case", response_model=GenerateResponse, summary="生成测试用例")
async def generate_test_case(
    document_content: str = Form(..., description="文档内容"),
    requirements: Optional[str] = Form(None, description="额外需求说明"),
    file: Optional[UploadFile] = File(None, description="上传文档文件"),
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    生成测试用例

    - **document_content**: 文档内容（文本格式）
    - **requirements**: 额外需求说明（可选）
    - **file**: 上传文档文件（可选，支持 Word/Excel/PDF/Markdown）
    """
    # 获取授权码
    auth_code = get_auth_code(request)
    if not auth_code:
        raise HTTPException(status_code=401, detail="未提供授权码")

    try:
        # 创建任务
        task_service = TaskProgressService(db)
        task_id = task_service.create_task("generate")
        task_service.update_task(task_id, status="processing", progress=10, message="正在解析文档...")

        # 解析上传的文件（如果有）
        if file:
            file_path = f"data/uploads/{task_id}_{file.filename}"
            os.makedirs("data/uploads", exist_ok=True)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            # 解析文档
            document_content = DocumentParser.parse_document(file_path)
            logger.info(f"已解析文档: {file.filename}")

        # 更新任务进度
        task_service.update_task(task_id, progress=30, message="文档解析完成，正在生成测试用例...")

        # 异步生成测试用例
        async def generate_content():
            try:
                ai_service = AIGeneratorService(settings.DEEPSEEK_API_KEY)
                result = ai_service.generate_test_cases(document_content, requirements)

                # 保存测试用例到数据库
                test_case = TestCase(
                    title=f"AI生成测试用例-{task_id}",
                    content=result,
                    type="api",
                    created_by=auth_code
                )
                db.add(test_case)
                db.commit()

                # 更新任务状态
                task_service.update_task(
                    task_id,
                    status="completed",
                    progress=100,
                    message="生成完成",
                    result_data={"test_case_id": test_case.id, "content": result}
                )

            except Exception as e:
                logger.error(f"生成测试用例失败: {str(e)}")
                task_service.update_task(
                    task_id,
                    status="failed",
                    progress=0,
                    message=f"生成失败: {str(e)}"
                )

        # 启动后台任务
        asyncio.create_task(generate_content())

        return GenerateResponse(
            task_id=task_id,
            status="processing",
            message="测试用例生成任务已创建，请通过task_id查询进度"
        )

    except Exception as e:
        logger.error(f"创建生成任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.post("/api", response_model=GenerateResponse, summary="生成API自动化脚本")
async def generate_api_script(
    document_content: str = Form(..., description="文档内容"),
    api_info: Optional[str] = Form(None, description="API信息"),
    file: Optional[UploadFile] = File(None, description="上传文档文件"),
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    生成API自动化测试脚本（Pytest + Requests）

    - **document_content**: 文档内容（应包含API接口信息）
    - **api_info**: API信息（可选，覆盖文档中的API信息）
    - **file**: 上传文档文件（可选）
    """
    # 获取授权码
    auth_code = get_auth_code(request)
    if not auth_code:
        raise HTTPException(status_code=401, detail="未提供授权码")

    try:
        # 创建任务
        task_service = TaskProgressService(db)
        task_id = task_service.create_task("generate")
        task_service.update_task(task_id, status="processing", progress=10, message="正在解析文档...")

        # 解析上传的文件（如果有）
        if file:
            file_path = f"data/uploads/{task_id}_{file.filename}"
            os.makedirs("data/uploads", exist_ok=True)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            # 解析文档
            document_content = DocumentParser.parse_document(file_path)
            logger.info(f"已解析文档: {file.filename}")

        # 更新任务进度
        task_service.update_task(task_id, progress=30, message="文档解析完成，正在生成脚本...")

        # 异步生成脚本
        async def generate_content():
            try:
                ai_service = AIGeneratorService(settings.DEEPSEEK_API_KEY)
                result = ai_service.generate_api_script(document_content, api_info)

                # 保存脚本到数据库和文件
                script = AutoScript(
                    name=f"API脚本-{task_id}",
                    content=result,
                    type="api",
                    created_by=auth_code
                )
                db.add(script)
                db.commit()

                # 保存到文件
                script_path = f"data/scripts/api_script_{task_id}.py"
                os.makedirs("data/scripts", exist_ok=True)
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(result)

                # 更新任务状态
                task_service.update_task(
                    task_id,
                    status="completed",
                    progress=100,
                    message="生成完成",
                    result_data={"script_id": script.id, "file_path": script_path, "content": result}
                )

            except Exception as e:
                logger.error(f"生成API脚本失败: {str(e)}")
                task_service.update_task(
                    task_id,
                    status="failed",
                    progress=0,
                    message=f"生成失败: {str(e)}"
                )

        # 启动后台任务
        asyncio.create_task(generate_content())

        return GenerateResponse(
            task_id=task_id,
            status="processing",
            message="API脚本生成任务已创建，请通过task_id查询进度"
        )

    except Exception as e:
        logger.error(f"创建生成任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.post("/ui", response_model=GenerateResponse, summary="生成UI自动化脚本")
async def generate_ui_script(
    document_content: str = Form(..., description="文档内容"),
    ui_info: Optional[str] = Form(None, description="UI信息"),
    file: Optional[UploadFile] = File(None, description="上传文档文件"),
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    生成UI自动化测试脚本（Playwright）

    - **document_content**: 文档内容（应包含页面操作信息）
    - **ui_info**: UI信息（可选，覆盖文档中的UI信息）
    - **file**: 上传文档文件（可选）
    """
    # 获取授权码
    auth_code = get_auth_code(request)
    if not auth_code:
        raise HTTPException(status_code=401, detail="未提供授权码")

    try:
        # 创建任务
        task_service = TaskProgressService(db)
        task_id = task_service.create_task("generate")
        task_service.update_task(task_id, status="processing", progress=10, message="正在解析文档...")

        # 解析上传的文件（如果有）
        if file:
            file_path = f"data/uploads/{task_id}_{file.filename}"
            os.makedirs("data/uploads", exist_ok=True)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            # 解析文档
            document_content = DocumentParser.parse_document(file_path)
            logger.info(f"已解析文档: {file.filename}")

        # 更新任务进度
        task_service.update_task(task_id, progress=30, message="文档解析完成，正在生成脚本...")

        # 异步生成脚本
        async def generate_content():
            try:
                ai_service = AIGeneratorService(settings.DEEPSEEK_API_KEY)
                result = ai_service.generate_ui_script(document_content, ui_info)

                # 保存脚本到数据库和文件
                script = AutoScript(
                    name=f"UI脚本-{task_id}",
                    content=result,
                    type="ui",
                    created_by=auth_code
                )
                db.add(script)
                db.commit()

                # 保存到文件
                script_path = f"data/scripts/ui_script_{task_id}.py"
                os.makedirs("data/scripts", exist_ok=True)
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(result)

                # 更新任务状态
                task_service.update_task(
                    task_id,
                    status="completed",
                    progress=100,
                    message="生成完成",
                    result_data={"script_id": script.id, "file_path": script_path, "content": result}
                )

            except Exception as e:
                logger.error(f"生成UI脚本失败: {str(e)}")
                task_service.update_task(
                    task_id,
                    status="failed",
                    progress=0,
                    message=f"生成失败: {str(e)}"
                )

        # 启动后台任务
        asyncio.create_task(generate_content())

        return GenerateResponse(
            task_id=task_id,
            status="processing",
            message="UI脚本生成任务已创建，请通过task_id查询进度"
        )

    except Exception as e:
        logger.error(f"创建生成任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.get("/progress/{task_id}", response_model=TaskProgressResponse, summary="获取任务进度")
def get_task_progress(
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    根据任务ID查询任务进度和结果

    - **task_id**: 任务ID
    """
    task_service = TaskProgressService(db)
    task_status = task_service.get_task_status(task_id)

    if not task_status:
        raise HTTPException(status_code=404, detail="任务不存在")

    return TaskProgressResponse(**task_status)
