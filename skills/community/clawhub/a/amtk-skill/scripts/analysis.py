"""Technical analysis module for AMtkSkill data."""

import numpy as np
import pandas as pd

from query import load_market_daily, load_adj_factor, load_full_daily


# ---------------------------------------------------------------------------
# Adjusted prices
# ---------------------------------------------------------------------------

def forward_adjusted_prices(
    ts_code: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Return OHLCV with forward-adjusted (前复权) prices.

    Formula: adjusted = price * adj_factor / latest_adj_factor
    """
    data = load_full_daily(ts_code, start_date, end_date)
    if data.empty or "adj_factor" not in data.columns:
        return data

    latest_adj = data["adj_factor"].iloc[-1]
    if pd.isna(latest_adj) or latest_adj == 0:
        return data

    price_cols = ["open", "high", "low", "close", "vwap"]
    for col in price_cols:
        if col in data.columns:
            data[f"{col}_adj"] = (data[col] * data["adj_factor"] / latest_adj).round(4)

    return data


def backward_adjusted_prices(
    ts_code: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Return OHLCV with backward-adjusted (后复权) prices.

    Formula: adjusted = price * adj_factor
    """
    data = load_full_daily(ts_code, start_date, end_date)
    if data.empty or "adj_factor" not in data.columns:
        return data

    price_cols = ["open", "high", "low", "close", "vwap"]
    for col in price_cols:
        if col in data.columns:
            data[f"{col}_adj"] = (data[col] * data["adj_factor"]).round(4)

    return data


# ---------------------------------------------------------------------------
# Technical indicators
# ---------------------------------------------------------------------------

def _get_adjusted_close(
    ts_code: str,
    start_date: str | None = None,
    end_date: str | None = None,
    adjusted: bool = True,
) -> pd.DataFrame:
    """Load close prices, optionally forward-adjusted."""
    if adjusted:
        data = forward_adjusted_prices(ts_code, start_date, end_date)
        close_col = "close_adj" if "close_adj" in data.columns else "close"
    else:
        data = load_market_daily(ts_code, start_date, end_date)
        close_col = "close"

    if data.empty:
        return data

    result = data[["ts_code", "trade_date"]].copy()
    result["close"] = data[close_col]
    return result


def moving_average(
    ts_code: str,
    windows: list[int] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    adjusted: bool = True,
) -> pd.DataFrame:
    """Calculate simple moving averages on (adjusted) close prices."""
    if windows is None:
        windows = [5, 10, 20, 60]

    data = _get_adjusted_close(ts_code, start_date, end_date, adjusted)
    if data.empty:
        return data

    for w in windows:
        data[f"ma{w}"] = data["close"].rolling(window=w, min_periods=w).mean().round(4)

    return data


def rsi(
    ts_code: str,
    period: int = 14,
    start_date: str | None = None,
    end_date: str | None = None,
    adjusted: bool = True,
) -> pd.DataFrame:
    """Calculate Relative Strength Index."""
    data = _get_adjusted_close(ts_code, start_date, end_date, adjusted)
    if data.empty:
        return data

    delta = data["close"].diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    data["rsi"] = (100 - 100 / (1 + rs)).round(2)

    return data


def macd(
    ts_code: str,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
    start_date: str | None = None,
    end_date: str | None = None,
    adjusted: bool = True,
) -> pd.DataFrame:
    """Calculate MACD, signal line, and histogram."""
    data = _get_adjusted_close(ts_code, start_date, end_date, adjusted)
    if data.empty:
        return data

    ema_fast = data["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = data["close"].ewm(span=slow, adjust=False).mean()

    data["macd"] = (ema_fast - ema_slow).round(4)
    data["macd_signal"] = data["macd"].ewm(span=signal, adjust=False).mean().round(4)
    data["macd_hist"] = (data["macd"] - data["macd_signal"]).round(4)

    return data


def bollinger_bands(
    ts_code: str,
    window: int = 20,
    num_std: float = 2.0,
    start_date: str | None = None,
    end_date: str | None = None,
    adjusted: bool = True,
) -> pd.DataFrame:
    """Calculate Bollinger Bands."""
    data = _get_adjusted_close(ts_code, start_date, end_date, adjusted)
    if data.empty:
        return data

    rolling = data["close"].rolling(window=window, min_periods=window)
    data["bb_mid"] = rolling.mean().round(4)
    std = rolling.std()
    data["bb_upper"] = (data["bb_mid"] + num_std * std).round(4)
    data["bb_lower"] = (data["bb_mid"] - num_std * std).round(4)

    return data


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def price_statistics(
    ts_code: str,
    start_date: str | None = None,
    end_date: str | None = None,
    adjusted: bool = True,
) -> dict:
    """Return summary statistics: return, volatility, max drawdown, Sharpe-like ratio."""
    data = _get_adjusted_close(ts_code, start_date, end_date, adjusted)
    if data.empty or len(data) < 2:
        return {}

    close = data["close"].dropna()
    if len(close) < 2:
        return {}

    daily_returns = close.pct_change().dropna()
    trading_days = len(daily_returns)

    total_return = (close.iloc[-1] / close.iloc[0] - 1) * 100
    annualized_return = ((1 + total_return / 100) ** (252 / trading_days) - 1) * 100 if trading_days > 0 else 0
    daily_vol = daily_returns.std()
    annualized_vol = daily_vol * np.sqrt(252) * 100

    # Max drawdown
    cummax = close.cummax()
    drawdown = (close - cummax) / cummax
    max_drawdown = drawdown.min() * 100

    # Sharpe ratio (assuming 0 risk-free rate)
    sharpe = (daily_returns.mean() / daily_vol * np.sqrt(252)) if daily_vol > 0 else 0

    return {
        "ts_code": ts_code,
        "start_date": str(data["trade_date"].iloc[0].date()),
        "end_date": str(data["trade_date"].iloc[-1].date()),
        "trading_days": trading_days,
        "total_return_pct": round(total_return, 2),
        "annualized_return_pct": round(annualized_return, 2),
        "annualized_volatility_pct": round(annualized_vol, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
        "sharpe_ratio": round(sharpe, 4),
    }


def detect_corporate_actions(
    ts_code: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Find dates where adj_factor changed (splits, dividends)."""
    adj = load_adj_factor(ts_code, start_date, end_date)
    if adj.empty or "adj_factor" not in adj.columns:
        return pd.DataFrame()

    adj = adj.sort_values("trade_date").reset_index(drop=True)
    adj["prev_adj"] = adj["adj_factor"].shift(1)
    adj["adj_change"] = (adj["adj_factor"] - adj["prev_adj"]).round(6)

    actions = adj[adj["adj_change"].abs() > 1e-6].copy()
    actions["adj_ratio"] = (actions["adj_factor"] / actions["prev_adj"]).round(6)

    return actions[["ts_code", "trade_date", "prev_adj", "adj_factor", "adj_change", "adj_ratio"]].reset_index(drop=True)
