from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.catalog.loader import (
    get_indicator,
    get_sector,
    list_indicator_summaries,
    list_sector_summaries,
    list_source_summaries,
)
from app.models import (
    AIConfigPublic,
    AIConfigUpdate,
    AIPlanRequest,
    AIPlanResponse,
    ExportFormat,
    Indicator,
    IndicatorSummary,
    PreviewResponse,
    RunRequest,
    RunResponse,
    Sector,
    SectorSnapshot,
    SectorSummary,
    SourceSummary,
)
from app.services.akshare_runner import run_indicator
from app.services.dataframe_utils import dataframe_preview
from app.services.exporter import MEDIA_TYPES, export_dataframe
from app.services.sector_snapshot import build_snapshot
from app.services.task_store import TaskRecord, task_store


router = APIRouter(prefix="/api")


def _record_to_run_response(record: TaskRecord) -> RunResponse:
    return RunResponse(
        task_id=record.task_id,
        indicator_id=record.indicator_id,
        indicator_name=record.indicator_name,
        row_count=len(record.data),
        column_count=len(record.data.columns),
        columns=[str(column) for column in record.data.columns],
        preview=dataframe_preview(record.data, limit=500),
        created_at=record.created_at,
        expires_at=record.expires_at,
    )


def _record_to_preview_response(record: TaskRecord, limit: int) -> PreviewResponse:
    return PreviewResponse(
        task_id=record.task_id,
        row_count=len(record.data),
        column_count=len(record.data.columns),
        columns=[str(column) for column in record.data.columns],
        preview=dataframe_preview(record.data, limit=limit),
        created_at=record.created_at,
        expires_at=record.expires_at,
    )


def _get_record_or_404(task_id: str) -> TaskRecord:
    record = task_store.get(task_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在或已过期，请重新提取数据。",
        )
    return record


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/sectors", response_model=list[SectorSummary])
def list_sectors() -> list[SectorSummary]:
    return list_sector_summaries()


@router.get("/sectors/{sector_id}", response_model=Sector)
def read_sector(sector_id: str) -> Sector:
    sector = get_sector(sector_id)
    if sector is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="板块不存在")
    return sector


@router.get("/sectors/{sector_id}/snapshot", response_model=SectorSnapshot)
def read_sector_snapshot(
    sector_id: str,
    refresh: bool = Query(False),
) -> SectorSnapshot:
    sector = get_sector(sector_id)
    if sector is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="板块不存在")
    if refresh:
        from app.services.sector_snapshot import invalidate_cache
        invalidate_cache()
    return build_snapshot(sector.id, sector.snapshot)


@router.get("/indicators", response_model=list[IndicatorSummary])
def list_indicators(
    source: str | None = Query(None),
    q: str | None = Query(None),
) -> list[IndicatorSummary]:
    return list_indicator_summaries(source=source, query=q)


@router.get("/indicators/{indicator_id}", response_model=Indicator)
def read_indicator(indicator_id: str) -> Indicator:
    indicator = get_indicator(indicator_id)
    if indicator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="指标不存在")
    return indicator


@router.get("/sources", response_model=list[SourceSummary])
def list_sources() -> list[SourceSummary]:
    return list_source_summaries()


@router.post("/tasks/run", response_model=RunResponse)
def run_task(request: RunRequest) -> RunResponse:
    indicator = get_indicator(request.indicator_id)
    if indicator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="指标不存在")

    dataframe = run_indicator(indicator, request.params, use_cache=not request.refresh)
    record = task_store.create(indicator, dataframe)
    return _record_to_run_response(record)


@router.get("/tasks/{task_id}/preview", response_model=PreviewResponse)
def preview_task(task_id: str, limit: int = Query(100, ge=1, le=1000)) -> PreviewResponse:
    record = _get_record_or_404(task_id)
    return _record_to_preview_response(record, limit)


@router.get("/tasks/{task_id}/export")
def export_task(task_id: str, file_format: ExportFormat = Query(..., alias="format")) -> Response:
    record = _get_record_or_404(task_id)
    payload = export_dataframe(record.data, file_format)
    filename = f"{record.indicator_id}_{record.task_id}.{file_format}"
    return Response(
        content=payload,
        media_type=MEDIA_TYPES[file_format],
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> Response:
    task_store.delete(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/tasks", status_code=status.HTTP_204_NO_CONTENT)
def clear_tasks() -> Response:
    task_store.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/cache/results", status_code=status.HTTP_204_NO_CONTENT)
def clear_result_cache() -> Response:
    from app.services.result_cache import result_cache

    result_cache.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ─── AI 智能取数 ───


@router.get("/ai/config", response_model=AIConfigPublic)
def read_ai_config() -> AIConfigPublic:
    from app.services.ai_config import load_config

    config = load_config()
    if config is None:
        return AIConfigPublic(configured=False)
    return AIConfigPublic(
        configured=True,
        base_url=config.base_url,
        model=config.model,
        has_key=bool(config.api_key),
    )


@router.put("/ai/config", response_model=AIConfigPublic)
def update_ai_config(payload: AIConfigUpdate) -> AIConfigPublic:
    from app.services.ai_config import load_config, save_config

    if not payload.base_url.strip() or not payload.model.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="base_url 与 model 不能为空。",
        )

    api_key = payload.api_key.strip()
    if not api_key:
        existing = load_config()
        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="首次配置必须填写 api_key。",
            )
        api_key = existing.api_key

    config = save_config(payload.base_url, payload.model, api_key)
    return AIConfigPublic(
        configured=True,
        base_url=config.base_url,
        model=config.model,
        has_key=True,
    )


@router.post("/ai/plan", response_model=AIPlanResponse)
def ai_plan(request: AIPlanRequest) -> AIPlanResponse:
    from app.services.ai_router import plan

    if not request.messages:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="对话内容不能为空。",
        )
    return plan(request.messages)
