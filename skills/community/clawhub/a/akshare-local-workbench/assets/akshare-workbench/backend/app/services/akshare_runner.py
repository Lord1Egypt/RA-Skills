from __future__ import annotations

import logging
import os
import random
import time
from typing import Any

from fastapi import HTTPException, status

from app.models import Indicator, IndicatorParam
from app.services.dataframe_utils import normalize_dataframe
from app.services.http_client import _is_transient_network_error, patch_akshare_http

logger = logging.getLogger(__name__)

_DEFAULT_CALL_ATTEMPTS = int(os.environ.get("AKSHARE_CALL_ATTEMPTS", "2"))
_EASTMONEY_CALL_ATTEMPTS = int(os.environ.get("AKSHARE_EASTMONEY_CALL_ATTEMPTS", "1"))
_ENRICH_NAMES = os.environ.get("AKSHARE_ENRICH_NAMES", "0").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}


def _normalize_date(value: Any) -> str:
    return str(value).replace("-", "")


def _coerce_param(param: IndicatorParam, value: Any) -> Any:
    if value is None or value == "":
        value = param.default

    if param.required and (value is None or value == ""):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"参数 {param.label} 不能为空",
        )

    if value is None:
        return None

    if param.options and value not in param.options:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"参数 {param.label} 只能选择: {', '.join(param.options)}",
        )

    if param.type == "date":
        return _normalize_date(value)
    if param.type == "integer":
        return int(value)
    if param.type == "number":
        return float(value)
    if param.type == "boolean":
        return bool(value)
    return value


def build_akshare_params(indicator: Indicator, raw_params: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for param in indicator.params:
        value = _coerce_param(param, raw_params.get(param.name))
        if value is not None:
            params[param.name] = value
    return params


def run_indicator(indicator: Indicator, raw_params: dict[str, Any], *, use_cache: bool = True):
    params = build_akshare_params(indicator, raw_params)

    if use_cache:
        from app.services.result_cache import result_cache

        cached = result_cache.get(indicator, params)
        if cached is not None:
            return cached

    try:
        import akshare as ak
    except ImportError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="后端未安装 akshare，请先在 backend 环境中安装 requirements.txt。",
        ) from exc

    from app.services.rate_limiter import rate_limiter

    patch_akshare_http()

    ak_function = getattr(ak, indicator.ak_function, None)
    if ak_function is None or not callable(ak_function):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AKShare 函数不存在: {indicator.ak_function}",
        )

    rate_limiter.acquire(indicator.source)
    try:
        # AKShare's HTTP helpers already retry individual requests. Keep this
        # outer retry shallow to avoid multiplying requests during rate limits.
        max_attempts = (
            _EASTMONEY_CALL_ATTEMPTS
            if indicator.source == "eastmoney"
            else _DEFAULT_CALL_ATTEMPTS
        )
        last_exc: Exception | None = None
        result = None
        is_eastmoney = indicator.source == "eastmoney"
        for attempt in range(max_attempts):
            try:
                result = ak_function(**params)
                break
            except HTTPException:
                raise
            except Exception as exc:
                last_exc = exc
                if not _is_transient_network_error(exc):
                    break
                if attempt < max_attempts - 1:
                    base = 2.5 if _is_transient_network_error(exc) else 1.0
                    wait = base * (2 ** attempt) + random.uniform(0.5, 1.5)
                    if is_eastmoney:
                        wait = max(wait, 4.0 + random.uniform(1.0, 3.0))
                    logger.warning(
                        "AKShare call %s attempt %d/%d failed: %s, retrying in %.1fs",
                        indicator.ak_function, attempt + 1, max_attempts, exc, wait,
                    )
                    time.sleep(wait)

        if result is None:
            assert last_exc is not None
            if _is_transient_network_error(last_exc):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=(
                        "数据源多次拒绝了连接（可能触发了东方财富限流、本地代理过载或临时故障），"
                        "请稍后再试。若持续失败，可尝试关闭 VPN/代理，或设置环境变量 "
                        "AKSHARE_PROXY_MODE=direct|system|auto。"
                        f"原始错误: {last_exc}"
                    ),
                ) from last_exc
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AKShare 提取失败: {last_exc}",
            ) from last_exc

        dataframe = normalize_dataframe(result)
        if dataframe.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AKShare 返回空数据，请检查标的、时间段或数据源状态。",
            )

        if _ENRICH_NAMES:
            from app.services.name_resolver import enrich_with_name

            dataframe = enrich_with_name(indicator, params, dataframe)

        if use_cache:
            from app.services.result_cache import result_cache

            result_cache.set(indicator, params, dataframe)
        return dataframe
    finally:
        rate_limiter.release()
