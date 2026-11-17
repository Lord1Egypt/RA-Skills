"""FastAPI 网关入口：意图识别 Skill 的独立服务。"""
from __future__ import annotations

import logging
import sys

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .config import get_settings
from .pipeline import IntentResult, run_intent_pipeline

# ---------------------------------------------------------------------------
# 埋点日志：结构化输出到 stdout，便于接入 ELK/Loki 做风控统计与 badcase 复盘
# ---------------------------------------------------------------------------

if not logging.getLogger("intent_skill").handlers:
    import json as _json

    class _StructuredFilter(logging.Filter):
        """把 extra 字段打包进 record.structured，输出单行 JSON 便于 ELK/Loki 采集。"""

        def filter(self, record: logging.LogRecord) -> bool:
            standard = {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "taskName",
                "message", "asctime",
            }
            data = {k: v for k, v in record.__dict__.items() if k not in standard}
            record.structured = _json.dumps(data, ensure_ascii=False, default=str)
            return True

    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter(
        fmt='{"ts":"%(asctime)s","logger":"%(name)s","msg":"%(message)s","data":%(structured)s}'))
    _handler.addFilter(_StructuredFilter())
    _intent_logger = logging.getLogger("intent_skill")
    _intent_logger.addHandler(_handler)
    _intent_logger.setLevel(logging.INFO)


class IntentCheckRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=8000, description="用户原始输入")


class IntentCheckResponse(BaseModel):
    request_id: str
    action: str = Field(..., description="forward/intercept/platform_qa/degrade_block/degrade_loose")
    is_allow_forward: bool
    risk_level: str
    reply_to_user: str = ""
    intent_type: str = ""
    intent_desc: str = ""
    refuse_reason: str = ""
    result: dict | None = Field(
        None, description="action=forward 时返回给调度器的任务上下文对象")


app = FastAPI(title="ETF Intent Skill Gateway", version="1.0.0")


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/intent/check", response_model=IntentCheckResponse)
async def intent_check(req: IntentCheckRequest) -> IntentCheckResponse:
    settings = get_settings()
    result: IntentResult = await run_intent_pipeline(req.query, settings)

    return IntentCheckResponse(
        request_id=result.request_id,
        action=result.action,
        is_allow_forward=result.is_allow_forward,
        risk_level=result.risk_level,
        reply_to_user=result.reply_to_user,
        intent_type=result.intent_type,
        intent_desc=result.intent_desc,
        refuse_reason=result.refuse_reason,
        result=result.to_task_context() if result.is_allow_forward else None,
    )
