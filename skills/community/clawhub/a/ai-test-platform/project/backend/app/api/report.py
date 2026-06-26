"""
测试报告 API 路由

处理测试报告的生成、查询、导出和AI分析
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.services.report_service import ReportService
from app.schemas.report import (
    ReportGenerateRequest, ReportExportRequest,
    ReportResponse, ReportListResponse, AiAnalysisRequest
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/report", tags=["测试报告"])


def get_auth_code(request: Request) -> str:
    """从请求中获取授权码"""
    auth_code = request.headers.get("Authorization") or request.query_params.get("auth_code")
    if auth_code and auth_code.startswith("Bearer "):
        auth_code = auth_code[7:]
    return auth_code


@router.post("/generate", summary="生成测试报告")
def generate_report(
    request: ReportGenerateRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    根据执行记录生成测试报告

    - **record_id**: 执行记录ID
    - **include_ai_analysis**: 是否包含AI分析（默认True）
    """
    auth_code = get_auth_code(http_request)

    try:
        service = ReportService(db)
        report = service.generate_report(request, auth_code)

        return {
            "code": 200,
            "msg": "报告生成成功",
            "data": report.to_dict()
        }
    except ValueError as e:
        logger.error(f"生成报告失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"生成报告失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


@router.get("/list", summary="获取报告列表")
def list_reports(
    script_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取测试报告列表

    - **script_id**: 脚本ID（可选，不提供则返回所有报告）
    - **limit**: 返回数量限制，默认100条
    """
    service = ReportService(db)
    reports = service.list_reports(script_id=script_id, limit=limit)

    return {
        "code": 200,
        "msg": "查询成功",
        "data": [
            ReportListResponse(
                id=report.id,
                script_name=report.script_name,
                script_type=report.script_type,
                result=report.result,
                total_tests=report.total_tests,
                passed_tests=report.passed_tests,
                failed_tests=report.failed_tests,
                duration=report.duration,
                create_time=report.create_time.strftime("%Y-%m-%d %H:%M:%S")
            )
            for report in reports
        ]
    }


@router.get("/{report_id}", summary="获取报告详情")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    获取测试报告详情

    - **report_id**: 报告ID
    """
    service = ReportService(db)
    report = service.get_report(report_id)

    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": ReportResponse(**report.to_dict())
    }


@router.get("/record/{record_id}", summary="根据执行记录获取报告")
def get_report_by_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    根据执行记录ID获取测试报告

    - **record_id**: 执行记录ID
    """
    service = ReportService(db)
    report = service.get_report_by_record(record_id)

    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")

    return {
        "code": 200,
        "msg": "查询成功",
        "data": ReportResponse(**report.to_dict())
    }


@router.post("/export", summary="导出测试报告")
def export_report(
    request: ReportExportRequest,
    db: Session = Depends(get_db)
):
    """
    导出测试报告

    - **report_id**: 报告ID
    - **format**: 导出格式（html/pdf）
    - **include_screenshots**: 是否包含截图（仅PDF）
    """
    try:
        service = ReportService(db)
        file_path = service.export_report(request)

        # 确定文件类型
        if request.format == "pdf":
            media_type = "application/pdf"
        else:
            media_type = "text/html"

        return FileResponse(
            file_path,
            media_type=media_type,
            filename=os.path.basename(file_path)
        )
    except ValueError as e:
        logger.error(f"导出报告失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"导出报告失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post("/ai-analysis", summary="生成AI分析")
def generate_ai_analysis(
    request: AiAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    为测试报告生成AI分析

    - **report_id**: 报告ID
    - **log_content**: 执行日志（如果报告无日志，则使用此参数）
    """
    try:
        service = ReportService(db)
        analysis = service.generate_ai_analysis(request.report_id)

        return {
            "code": 200,
            "msg": "AI分析生成成功",
            "data": {
                "report_id": request.report_id,
                "analysis_result": analysis
            }
        }
    except ValueError as e:
        logger.error(f"生成AI分析失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"生成AI分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.delete("/{report_id}", summary="删除测试报告")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    删除测试报告

    - **report_id**: 报告ID
    """
    service = ReportService(db)
    success = service.delete_report(report_id)

    if not success:
        raise HTTPException(status_code=404, detail="报告不存在")

    return {"code": 200, "msg": "删除成功", "data": None}


# 需要导入os模块
import os
