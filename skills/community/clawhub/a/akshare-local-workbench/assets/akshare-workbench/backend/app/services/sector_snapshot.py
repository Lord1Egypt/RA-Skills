from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Any

import pandas as pd

from app.models import SectorSnapshot, SectorSnapshotConfig, SnapshotCard, SnapshotCardConfig
from app.services.dataframe_utils import normalize_dataframe
from app.services.http_client import patch_akshare_http


logger = logging.getLogger(__name__)


_CALL_TIMEOUT_SECONDS = 60.0
# Hard ceiling for an entire snapshot response so a few slow/failing data
# sources can't hang the endpoint for minutes (which previously starved the
# browser connection pool and left other pages with an empty indicator list).
_SNAPSHOT_BUDGET_SECONDS = 60.0
_CACHE_TTL = timedelta(minutes=5)
_ERROR_CACHE_TTL = timedelta(seconds=60)


def _infer_source(ak_function: str) -> str:
    if "_em" in ak_function or ak_function.startswith("fund_"):
        return "eastmoney"
    if "_sina" in ak_function or "futures_" in ak_function:
        return "sina"
    if "_lg" in ak_function:
        return "legulegu"
    if "_jsl" in ak_function:
        return "jsl"
    if "currency_boc_safe" in ak_function:
        return "safe"
    if "fx_" in ak_function:
        return "cfdc"
    if "_csindex" in ak_function:
        return "csindex"
    if ak_function.startswith("macro_bank_usa") or ak_function.startswith("macro_usa"):
        return "jin10"
    if ak_function.startswith("macro_bank_euro"):
        return "jin10"
    if ak_function.startswith("macro_china"):
        return "nbs"
    if ak_function.startswith("macro_bank_china") or "lpr" in ak_function or "shibor" in ak_function:
        return "pbc"
    if ak_function.startswith("rate_"):
        return "akshare"
    if ak_function.startswith("bond_china"):
        return "cmec"
    if ak_function.startswith("bond_cash"):
        return "sse"
    if ak_function.startswith("bond_zh"):
        return "eastmoney"
    if "stock_zh_index_spot" in ak_function:
        return "sina"
    if ak_function.startswith("stock_zh_index_value"):
        return "csindex"
    if ak_function.startswith("sw_"):
        return "swindex"
    if "index_global" in ak_function:
        return "eastmoney"
    if "stock_hsgt" in ak_function:
        return "eastmoney"
    return "akshare"


class AKCallCache:
    def __init__(self, ttl: timedelta, error_ttl: timedelta) -> None:
        self._ttl = ttl
        self._error_ttl = error_ttl
        self._entries: dict[tuple[str, str], tuple[datetime, pd.DataFrame | Exception]] = {}
        self._lock = Lock()
        self._executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="ak-snapshot")

    def invalidate_all(self) -> None:
        with self._lock:
            self._entries.clear()

    def get_or_run(self, ak_function: str, params: dict[str, Any], source: str = "") -> pd.DataFrame:
        key = (ak_function, json.dumps(params, sort_keys=True, default=str))
        now = datetime.now(timezone.utc)
        with self._lock:
            cached = self._entries.get(key)
            if cached is not None:
                stored = cached[1]
                ttl = self._error_ttl if isinstance(stored, Exception) else self._ttl
                if now - cached[0] <= ttl:
                    if isinstance(stored, Exception):
                        raise stored
                    return stored

        try:
            import akshare as ak
        except ImportError as exc:
            raise RuntimeError("AKShare 未安装") from exc

        patch_akshare_http()

        fn = getattr(ak, ak_function, None)
        if fn is None or not callable(fn):
            raise RuntimeError(f"AKShare 函数不存在: {ak_function}")

        from app.services.rate_limiter import rate_limiter

        def _run_with_limit() -> pd.DataFrame:
            rate_limiter.acquire(source)
            try:
                return fn(**params)
            finally:
                rate_limiter.release()

        future = self._executor.submit(_run_with_limit)
        try:
            result = future.result(timeout=_CALL_TIMEOUT_SECONDS)
        except FuturesTimeout as exc:
            future.cancel()
            timeout_error = RuntimeError("数据源响应超时")
            with self._lock:
                self._entries[key] = (now, timeout_error)
            raise timeout_error from exc
        except Exception as exc:
            with self._lock:
                self._entries[key] = (now, exc)
            raise

        dataframe = normalize_dataframe(result)
        with self._lock:
            self._entries[key] = (now, dataframe)
        return dataframe


_cache = AKCallCache(_CACHE_TTL, _ERROR_CACHE_TTL)


def invalidate_cache() -> None:
    _cache.invalidate_all()


def _format_number(value: float | None, decimals: int) -> str:
    if value is None:
        return "—"
    if pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}"


def _coerce_float(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").rstrip("%")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _pick_value(dataframe: pd.DataFrame, card: SnapshotCardConfig) -> tuple[Any, Any]:
    if dataframe.empty:
        raise RuntimeError("结果为空")

    if card.mode == "filter_row":
        if card.filter_column is None or card.filter_value is None:
            raise RuntimeError("缺少过滤条件")
        if card.filter_column not in dataframe.columns:
            raise RuntimeError(f"缺少列 {card.filter_column}")
        matches = dataframe[dataframe[card.filter_column].astype(str) == str(card.filter_value)]
        if matches.empty:
            raise RuntimeError(f"未找到 {card.filter_value}")
        row = matches.iloc[0]
    elif card.mode in ("latest_row", "first_row"):
        if card.value_field not in dataframe.columns:
            raise RuntimeError(f"缺少列 {card.value_field}")
        if card.mode == "latest_row":
            indices = range(len(dataframe) - 1, -1, -1)
        else:
            indices = range(len(dataframe))
        row = None
        for idx in indices:
            candidate_row = dataframe.iloc[idx]
            value = candidate_row[card.value_field]
            if value is not None and not (isinstance(value, float) and pd.isna(value)):
                row = candidate_row
                break
        if row is None:
            row = dataframe.iloc[-1 if card.mode == "latest_row" else 0]
    elif card.mode == "top_n":
        row = dataframe.iloc[0]
    else:
        raise RuntimeError(f"未知模式: {card.mode}")

    if card.value_field not in dataframe.columns:
        raise RuntimeError(f"缺少列 {card.value_field}")
    value = row[card.value_field]
    change = row[card.change_field] if card.change_field and card.change_field in dataframe.columns else None
    return value, change


def render_card(card: SnapshotCardConfig) -> SnapshotCard:
    try:
        source = _infer_source(card.ak_function)
        dataframe = _cache.get_or_run(card.ak_function, card.params, source=source)
        raw_value, raw_change = _pick_value(dataframe, card)
    except Exception as exc:
        logger.warning("Snapshot card %s failed: %s", card.title, exc)
        return SnapshotCard(
            title=card.title,
            value=None,
            value_display="—",
            unit=card.unit,
            decimals=card.decimals,
            description=card.description,
            error=str(exc),
        )

    value_number = _coerce_float(raw_value)
    change_number = _coerce_float(raw_change)
    return SnapshotCard(
        title=card.title,
        value=value_number,
        value_display=_format_number(value_number, card.decimals),
        change=change_number,
        change_display=(_format_number(change_number, 2) + "%") if change_number is not None else None,
        unit=card.unit,
        decimals=card.decimals,
        description=card.description,
    )


def _pending_card(card: SnapshotCardConfig, error: str) -> SnapshotCard:
    return SnapshotCard(
        title=card.title,
        value=None,
        value_display="—",
        unit=card.unit,
        decimals=card.decimals,
        description=card.description,
        error=error,
    )


def build_snapshot(sector_id: str, config: SectorSnapshotConfig) -> SectorSnapshot:
    card_configs = config.cards
    if not card_configs:
        return SectorSnapshot(
            sector_id=sector_id,
            generated_at=datetime.now(timezone.utc),
            cards=[],
        )

    results: dict[int, SnapshotCard] = {}
    executor = ThreadPoolExecutor(
        max_workers=min(4, len(card_configs)),
        thread_name_prefix="snapshot-build",
    )
    try:
        future_to_index = {
            executor.submit(render_card, card): index
            for index, card in enumerate(card_configs)
        }
        deadline = time.monotonic() + _SNAPSHOT_BUDGET_SECONDS
        for future, index in future_to_index.items():
            remaining = deadline - time.monotonic()
            try:
                results[index] = future.result(timeout=max(0.0, remaining))
            except FuturesTimeout:
                future.cancel()
                results[index] = _pending_card(
                    card_configs[index], "数据源响应较慢，已跳过（稍后刷新重试）"
                )
            except Exception as exc:  # render_card normally swallows errors itself
                logger.warning("Snapshot card %s crashed: %s", card_configs[index].title, exc)
                results[index] = _pending_card(card_configs[index], str(exc))
    finally:
        executor.shutdown(wait=False)

    cards = [results[index] for index in range(len(card_configs))]
    return SectorSnapshot(
        sector_id=sector_id,
        generated_at=datetime.now(timezone.utc),
        cards=cards,
    )
