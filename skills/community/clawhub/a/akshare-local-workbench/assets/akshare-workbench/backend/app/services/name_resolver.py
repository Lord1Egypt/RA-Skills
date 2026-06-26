from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Any, Callable

import pandas as pd

from app.models import Indicator

logger = logging.getLogger(__name__)

# Parameter names (in priority order) that may carry a security code.
_CODE_PARAM_KEYS = ("symbol", "code", "stock", "fund", "ts_code", "sec_id")

# If the result already contains one of these columns we don't inject our own.
_EXISTING_NAME_HINTS = ("名称", "简称", "name", "证券名称", "基金简称", "股票简称")

_A_SHARE_CODE = re.compile(r"^\d{6}$")
_CACHE_TTL = timedelta(hours=12)
_NEGATIVE_TTL = timedelta(minutes=10)


class _NameCache:
    """TTL cache for resolved (kind, code) -> name lookups."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._store: dict[tuple[str, str], tuple[datetime, str | None]] = {}

    def resolve(self, kind: str, code: str, loader: Callable[[str], str | None]) -> str | None:
        key = (kind, code)
        now = datetime.now(timezone.utc)
        with self._lock:
            cached = self._store.get(key)
            if cached is not None:
                ttl = _CACHE_TTL if cached[1] else _NEGATIVE_TTL
                if now - cached[0] <= ttl:
                    return cached[1]

        try:
            name = loader(code)
        except Exception as exc:  # network/parse errors must never break extraction
            logger.warning("Name lookup %s:%s failed: %s", kind, code, exc)
            name = None

        with self._lock:
            self._store[(kind, code)] = (now, name)
        return name


_cache = _NameCache()


def _lookup_a_share(code: str) -> str | None:
    """Single, targeted A-share name lookup (avoids downloading the universe)."""
    import akshare as ak

    from app.services.http_client import patch_akshare_http, with_rate_limit

    patch_akshare_http()
    info = with_rate_limit("eastmoney", lambda: ak.stock_individual_info_em(symbol=code))
    mapping = dict(zip(info["item"].astype(str), info["value"]))
    name = mapping.get("股票简称")
    return str(name).strip() if name not in (None, "") else None


def _lookup_fund(code: str) -> str | None:
    import akshare as ak

    from app.services.http_client import patch_akshare_http, with_rate_limit

    patch_akshare_http()
    frame = with_rate_limit("eastmoney", lambda: ak.fund_name_em())
    matched = frame[frame["基金代码"].astype(str) == code]
    if matched.empty:
        return None
    return str(matched.iloc[0]["基金简称"]).strip()


def _extract_code(params: dict[str, Any]) -> str | None:
    for key in _CODE_PARAM_KEYS:
        value = params.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def _has_name_column(dataframe: pd.DataFrame) -> bool:
    for column in dataframe.columns:
        column_text = str(column).lower()
        if any(hint.lower() in column_text for hint in _EXISTING_NAME_HINTS):
            return True
    return False


def _resolve_name(indicator: Indicator, code: str) -> str | None:
    func = indicator.ak_function
    level1 = indicator.level1

    if func.startswith("fund_") or level1 == "基金":
        return _cache.resolve("fund", code, _lookup_fund)

    looks_like_a_share = bool(_A_SHARE_CODE.match(code))
    is_stock_context = (
        "stock_zh_a" in func
        or func.startswith("stock_a")
        or func.startswith("stock_individual")
        or "股票" in level1
    )
    if looks_like_a_share and is_stock_context:
        return _cache.resolve("a_share", code, _lookup_a_share)

    return None


def enrich_with_name(
    indicator: Indicator,
    params: dict[str, Any],
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Best-effort: prepend a 名称 column when a single security code was queried.

    Never raises; on any failure the original dataframe is returned unchanged.
    """
    try:
        if dataframe.empty or _has_name_column(dataframe):
            return dataframe

        code = _extract_code(params)
        if code is None:
            return dataframe

        name = _resolve_name(indicator, code)
        if not name:
            return dataframe

        enriched = dataframe.copy()
        enriched.insert(0, "名称", name)
        return enriched
    except Exception as exc:
        logger.warning("Name enrichment skipped for %s: %s", indicator.id, exc)
        return dataframe
