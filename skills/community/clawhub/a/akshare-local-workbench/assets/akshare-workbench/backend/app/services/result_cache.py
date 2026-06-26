from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from pathlib import Path
from threading import Lock
from typing import Any

import pandas as pd

from app.models import Indicator

logger = logging.getLogger(__name__)

_CACHE_DIR = Path(
    os.environ.get(
        "AKSHARE_RESULT_CACHE_DIR",
        Path(__file__).resolve().parents[2] / ".cache" / "results",
    )
)
_DEFAULT_TTL_SECONDS = int(os.environ.get("AKSHARE_RESULT_CACHE_TTL_SECONDS", "900"))
_SOURCE_TTLS = {
    "eastmoney": int(os.environ.get("AKSHARE_EASTMONEY_CACHE_TTL_SECONDS", "1800")),
    "sina": int(os.environ.get("AKSHARE_SINA_CACHE_TTL_SECONDS", "300")),
}
_lock = Lock()


def _ttl_for(indicator: Indicator) -> int:
    return _SOURCE_TTLS.get(indicator.source, _DEFAULT_TTL_SECONDS)


def _cache_key(indicator: Indicator, params: dict[str, Any]) -> str:
    payload = {
        "indicator_id": indicator.id,
        "ak_function": indicator.ak_function,
        "source": indicator.source,
        "params": params,
        "schema": 1,
    }
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class ResultCache:
    """Small disk cache for single-user repeated AKShare calls."""

    def get(self, indicator: Indicator, params: dict[str, Any]) -> pd.DataFrame | None:
        ttl = _ttl_for(indicator)
        if ttl <= 0:
            return None

        path = _CACHE_DIR / f"{_cache_key(indicator, params)}.pkl"
        try:
            if not path.exists():
                return None
            if time.time() - path.stat().st_mtime > ttl:
                return None
            with _lock:
                dataframe = pd.read_pickle(path)
            if isinstance(dataframe, pd.DataFrame):
                logger.info("AKShare result cache hit: %s", indicator.id)
                return dataframe.copy()
        except Exception as exc:
            logger.warning("Failed to read result cache %s: %s", path, exc)
        return None

    def set(self, indicator: Indicator, params: dict[str, Any], dataframe: pd.DataFrame) -> None:
        ttl = _ttl_for(indicator)
        if ttl <= 0:
            return

        path = _CACHE_DIR / f"{_cache_key(indicator, params)}.pkl"
        try:
            with _lock:
                _CACHE_DIR.mkdir(parents=True, exist_ok=True)
                dataframe.to_pickle(path)
        except Exception as exc:
            logger.warning("Failed to write result cache %s: %s", path, exc)

    def clear(self) -> int:
        if not _CACHE_DIR.exists():
            return 0
        count = 0
        with _lock:
            for path in _CACHE_DIR.glob("*.pkl"):
                try:
                    path.unlink()
                    count += 1
                except OSError as exc:
                    logger.warning("Failed to remove result cache %s: %s", path, exc)
        return count


result_cache = ResultCache()
