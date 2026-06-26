"""共享测试 fixtures"""
import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


@pytest.fixture
def sample_df():
    """标准测试 DataFrame（200 行）"""
    np.random.seed(42)
    n = 200
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    close = 10 + np.cumsum(np.random.randn(n) * 0.3)
    close = np.maximum(close, 1)
    high = close * (1 + np.abs(np.random.randn(n) * 0.01))
    low = close * (1 - np.abs(np.random.randn(n) * 0.01))
    opn = close * (1 + np.random.randn(n) * 0.005)
    volume = np.random.randint(100000, 1000000, n).astype(float)
    return pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": opn, "high": high, "low": low, "close": close,
        "volume": volume, "amount": volume * close
    })


@pytest.fixture
def uptrend_df():
    """构造上升趋势数据"""
    np.random.seed(123)
    n = 100
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    base = 10
    trend = np.linspace(0, 5, n)  # 线性上升
    noise = np.random.randn(n) * 0.1
    close = base + trend + noise
    high = close * 1.01
    low = close * 0.99
    opn = close * 1.005
    volume = np.random.randint(500000, 2000000, n).astype(float)
    # 上升趋势中成交量递增
    volume = volume * (1 + np.linspace(0, 0.5, n))
    return pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": opn, "high": high, "low": low, "close": close,
        "volume": volume, "amount": volume * close
    })


@pytest.fixture
def downtrend_df():
    """构造下降趋势数据"""
    np.random.seed(456)
    n = 100
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    base = 20
    trend = np.linspace(0, -8, n)  # 线性下降
    noise = np.random.randn(n) * 0.1
    close = base + trend + noise
    close = np.maximum(close, 1)
    high = close * 1.01
    low = close * 0.99
    opn = close * 0.995
    volume = np.random.randint(500000, 2000000, n).astype(float)
    return pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": opn, "high": high, "low": low, "close": close,
        "volume": volume, "amount": volume * close
    })


@pytest.fixture
def sideways_df():
    """构造震荡行情数据"""
    np.random.seed(789)
    n = 100
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    base = 15
    noise = np.random.randn(n) * 0.2
    close = base + noise
    close = np.maximum(close, 1)
    high = close * 1.005
    low = close * 0.995
    opn = close
    volume = np.random.randint(300000, 800000, n).astype(float)
    return pd.DataFrame({
        "date": dates.strftime("%Y%m%d"),
        "open": opn, "high": high, "low": low, "close": close,
        "volume": volume, "amount": volume * close
    })


@pytest.fixture
def computed_df(sample_df):
    """带技术指标的 DataFrame"""
    from stock_skill.indicators import compute_all
    return compute_all(sample_df)


@pytest.fixture
def mock_tushare_response():
    """Mock Tushare API 响应"""
    return pd.DataFrame({
        "ts_code": ["600036.SH"] * 5,
        "trade_date": ["20240101", "20240102", "20240103", "20240104", "20240105"],
        "open": [35.0, 35.5, 36.0, 35.8, 36.2],
        "high": [35.8, 36.2, 36.5, 36.3, 36.8],
        "low": [34.8, 35.2, 35.8, 35.5, 36.0],
        "close": [35.5, 36.0, 35.8, 36.2, 36.5],
        "vol": [1000000, 1200000, 1100000, 1300000, 1400000],
        "amount": [35500000, 43200000, 39380000, 47060000, 51100000]
    })


@pytest.fixture
def mock_eastmoney_quote():
    """Mock 东方财富行情响应"""
    return {
        "data": {
            "f57": "600036",
            "f58": "招商银行",
            "f43": 3650,  # 价格 * 100
            "f169": 50,   # 涨跌额 * 100
            "f170": 137,  # 涨跌幅 * 100
            "f46": 1400000,  # 成交量
            "f44": 3680,  # 最高价 * 100
            "f51": 3600,  # 最低价 * 100
        }
    }
