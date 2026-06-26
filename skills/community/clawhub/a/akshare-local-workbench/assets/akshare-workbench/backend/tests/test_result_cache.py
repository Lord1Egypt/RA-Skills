import pandas as pd

from app.catalog.loader import get_indicator
from app.services import result_cache as cache_module
from app.services.result_cache import ResultCache


def test_result_cache_roundtrip(tmp_path, monkeypatch):
    indicator = get_indicator("stock_a_hist")
    assert indicator is not None

    monkeypatch.setattr(cache_module, "_CACHE_DIR", tmp_path)
    monkeypatch.setattr(cache_module, "_DEFAULT_TTL_SECONDS", 60)
    monkeypatch.setitem(cache_module._SOURCE_TTLS, "eastmoney", 60)

    cache = ResultCache()
    params = {"symbol": "600000", "period": "daily"}
    frame = pd.DataFrame([{"日期": "2024-01-01", "收盘": 10.5}])

    assert cache.get(indicator, params) is None
    cache.set(indicator, params, frame)

    cached = cache.get(indicator, params)
    assert cached is not None
    assert cached.to_dict(orient="records") == frame.to_dict(orient="records")


def test_result_cache_can_be_disabled(tmp_path, monkeypatch):
    indicator = get_indicator("stock_a_hist")
    assert indicator is not None

    monkeypatch.setattr(cache_module, "_CACHE_DIR", tmp_path)
    monkeypatch.setitem(cache_module._SOURCE_TTLS, "eastmoney", 0)

    cache = ResultCache()
    cache.set(indicator, {"symbol": "600000"}, pd.DataFrame([{"x": 1}]))

    assert cache.get(indicator, {"symbol": "600000"}) is None
