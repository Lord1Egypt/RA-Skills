#!/usr/bin/env python3
"""
Einstein Research — Strategy Templates
========================================
Ready-to-use strategy functions compatible with the backtest_engine.py interface.

Each strategy accepts:
    prices: pd.DataFrame  — Close prices, columns = ticker symbols, index = dates
    **params              — Strategy-specific hyperparameters with sensible defaults

Each strategy returns:
    signals: pd.DataFrame or pd.Series  — Position sizes, values in [-1, 0, 1]
    Same index as prices. Positions are applied with a 1-day lag by the engine.

Strategies included:
  1. momentum_strategy        — Cross-sectional and time-series momentum
  2. mean_reversion_strategy  — Bollinger Band mean reversion
  3. dual_momentum_strategy   — Gary Antonacci's dual momentum (absolute + relative)
"""

import numpy as np
import pandas as pd


# ──────────────────────────────────────────────────────────────────────────────
# 1. MOMENTUM STRATEGY
# ──────────────────────────────────────────────────────────────────────────────

def momentum_strategy(prices: pd.DataFrame,
                      lookback: int = 126,        # ~6 months of trading days
                      holding_period: int = 21,   # ~1 month
                      top_n: int = 1,             # number of top performers to hold
                      skip_recent: int = 21,      # skip last month (standard momentum skip)
                      long_only: bool = True) -> pd.DataFrame:
    """
    Cross-sectional momentum: at each rebalance, rank assets by their
    [lookback - skip_recent] return and go long the top_n performers.

    If only one ticker is provided, falls back to time-series momentum:
    long when recent return > 0, flat otherwise.

    Parameters
    ----------
    lookback       : lookback window for return calculation (default 126 ≈ 6 months)
    holding_period : rebalance frequency in trading days (default 21 ≈ 1 month)
    top_n          : number of tickers to hold long (default 1)
    skip_recent    : recent days to skip to avoid 1-month reversal (default 21)
    long_only      : if False, short the bottom_n equally (default True)

    Edge
    ----
    Jegadeesh & Titman (1993): 3-12 month momentum has historically produced
    positive risk-adjusted returns across geographies and asset classes.
    """
    n_tickers = len(prices.columns)
    signals = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)

    if n_tickers == 1:
        # Time-series momentum fallback
        ret = prices.pct_change(lookback - skip_recent).shift(skip_recent)
        signals[prices.columns[0]] = np.where(ret.squeeze() > 0, 1.0, 0.0)
        return signals

    # Cross-sectional momentum: rank on [lookback-skip_recent] return, skip last skip_recent days
    ret = prices.pct_change(lookback - skip_recent).shift(skip_recent)

    for i in range(lookback, len(prices), holding_period):
        date = prices.index[i]
        row = ret.loc[date]
        if row.isna().all():
            continue
        ranked = row.rank(ascending=False, na_option="bottom")
        # Long top_n
        longs = ranked[ranked <= top_n].index
        signals.loc[date:prices.index[min(i + holding_period - 1, len(prices) - 1)], longs] = (
            1.0 / len(longs)
        )
        # Short bottom_n (if not long-only)
        if not long_only:
            shorts = ranked[ranked > (n_tickers - top_n)].index
            signals.loc[date:prices.index[min(i + holding_period - 1, len(prices) - 1)], shorts] = (
                -1.0 / len(shorts)
            )

    return signals


# ──────────────────────────────────────────────────────────────────────────────
# 2. MEAN REVERSION STRATEGY
# ──────────────────────────────────────────────────────────────────────────────

def mean_reversion_strategy(prices: pd.DataFrame,
                             bb_window: int = 20,        # Bollinger Band window
                             bb_std: float = 2.0,        # Band width in standard deviations
                             entry_z: float = 2.0,       # Z-score to trigger entry
                             exit_z: float = 0.5,        # Z-score to trigger exit
                             rsi_window: int = 14,       # RSI filter window
                             rsi_oversold: float = 35,   # RSI oversold threshold
                             rsi_overbought: float = 65, # RSI overbought threshold
                             long_only: bool = True) -> pd.DataFrame:
    """
    Bollinger Band mean reversion with RSI confirmation filter.

    Entry:
      - Long  when price > lower band (price < mean - entry_z * std) AND RSI < rsi_oversold
      - Short when price < upper band (price > mean + entry_z * std) AND RSI > rsi_overbought
    Exit:
      - Close long  when price > mean - exit_z * std
      - Close short when price < mean + exit_z * std

    Applies independently to each ticker. Equal weight across all open positions.

    Parameters
    ----------
    bb_window    : rolling window for mean/std (default 20 days)
    bb_std       : band width in standard deviations (default 2.0)
    entry_z      : z-score threshold to open position (default 2.0)
    exit_z       : z-score threshold to close position (default 0.5 = near mean)
    rsi_window   : RSI filter lookback (default 14 days)
    rsi_oversold : RSI level to confirm long entry (default 35)
    rsi_overbought: RSI level to confirm short entry (default 65)
    long_only    : if True, only take long (oversold) signals (default True)

    Edge
    ----
    Short-horizon mean reversion is well-documented in equity indices and ETFs.
    Most reliable in range-bound (sideways) regimes.
    """
    signals = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)

    for ticker in prices.columns:
        close = prices[ticker].dropna()

        # Bollinger Bands
        mean = close.rolling(bb_window).mean()
        std = close.rolling(bb_window).std()
        upper = mean + bb_std * std
        lower = mean - bb_std * std

        # Z-score
        z = (close - mean) / std

        # RSI
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(rsi_window).mean()
        loss = (-delta.clip(upper=0)).rolling(rsi_window).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))

        # Generate raw entry signals
        long_entry = (z < -entry_z) & (rsi < rsi_oversold)
        long_exit = z > -exit_z

        if not long_only:
            short_entry = (z > entry_z) & (rsi > rsi_overbought)
            short_exit = z < exit_z
        else:
            short_entry = pd.Series(False, index=close.index)
            short_exit = pd.Series(True, index=close.index)

        # State machine: carry position until exit condition
        pos = 0.0
        position_series = []
        for date in close.index:
            if long_entry.get(date, False) and pos == 0.0:
                pos = 1.0
            elif long_exit.get(date, False) and pos == 1.0:
                pos = 0.0
            elif short_entry.get(date, False) and pos == 0.0:
                pos = -1.0
            elif short_exit.get(date, False) and pos == -1.0:
                pos = 0.0
            position_series.append(pos)

        signals[ticker] = pd.Series(position_series, index=close.index).reindex(prices.index).fillna(0)

    # Normalize so total exposure ≤ 1
    n_open = (signals != 0).sum(axis=1).replace(0, 1)
    signals = signals.div(n_open, axis=0)

    return signals


# ──────────────────────────────────────────────────────────────────────────────
# 3. DUAL MOMENTUM STRATEGY
# ──────────────────────────────────────────────────────────────────────────────

def dual_momentum_strategy(prices: pd.DataFrame,
                            lookback: int = 252,            # 12 months for relative/absolute test
                            risk_free_ticker: str = None,   # proxy for cash (e.g. 'BIL' or 'SHY')
                            cash_return_annual: float = 0.04) -> pd.DataFrame:
    """
    Gary Antonacci's Dual Momentum (from "Dual Momentum Investing", 2014).

    Two filters applied every month:
      1. Absolute Momentum: is the best relative performer's return > risk-free rate?
         If no → go to cash (flat position)
      2. Relative Momentum: among the risky assets, hold the one with best 12-month return.

    Works best with 2-3 risky asset classes (e.g. SPY + EFA, or SPY + QQQ + IWM).
    The last ticker in the DataFrame (or risk_free_ticker if provided) is treated as
    the safe haven / cash equivalent.

    Parameters
    ----------
    lookback           : return lookback period in trading days (default 252 ≈ 12 months)
    risk_free_ticker   : if provided and present in prices, use it as cash proxy
    cash_return_annual : annualized cash return assumption when no proxy available (default 4%)

    Edge
    ----
    Antonacci (2012): Dual momentum beat all individual momentum strategies and SPY B&H
    on 1973-2012 data. The absolute momentum filter significantly reduces bear market losses.
    """
    tickers = list(prices.columns)
    signals = pd.DataFrame(0.0, index=prices.index, columns=tickers)

    # Identify risky assets vs safe haven
    if risk_free_ticker and risk_free_ticker in tickers:
        risky = [t for t in tickers if t != risk_free_ticker]
        has_cash_asset = True
    else:
        risky = tickers
        has_cash_asset = False

    # Daily cash return
    cash_daily = (1 + cash_return_annual) ** (1 / 252) - 1

    # Rebalance monthly (every ~21 trading days)
    rebalance_dates = prices.index[lookback::21]

    prev_signal = pd.Series(0.0, index=tickers)

    for i, date in enumerate(prices.index):
        if date not in rebalance_dates:
            signals.loc[date] = prev_signal
            continue

        window = prices.loc[:date].tail(lookback + 1)
        if len(window) < lookback:
            signals.loc[date] = prev_signal
            continue

        # Lookback return for each risky asset
        risky_returns = {}
        for t in risky:
            if t in window.columns:
                ret = window[t].iloc[-1] / window[t].iloc[0] - 1
                risky_returns[t] = ret

        if not risky_returns:
            signals.loc[date] = prev_signal
            continue

        # Step 1: Relative momentum — find best risky asset
        best_ticker = max(risky_returns, key=risky_returns.get)
        best_return = risky_returns[best_ticker]

        # Step 2: Absolute momentum — compare best to cash
        cash_period_return = (1 + cash_daily) ** lookback - 1

        new_signal = pd.Series(0.0, index=tickers)
        if best_return > cash_period_return:
            # Risky asset passes both filters → hold it
            new_signal[best_ticker] = 1.0
        elif has_cash_asset:
            # Fails absolute momentum → go to cash proxy
            new_signal[risk_free_ticker] = 1.0
        # else: flat (no safe haven in portfolio)

        signals.loc[date] = new_signal
        prev_signal = new_signal

    return signals


# ──────────────────────────────────────────────────────────────────────────────
# TEMPLATE: Custom Strategy Skeleton
# ──────────────────────────────────────────────────────────────────────────────

def custom_strategy_template(prices: pd.DataFrame,
                               param_a: int = 14,
                               param_b: float = 0.5) -> pd.DataFrame:
    """
    Template for building a custom strategy.

    Copy this function to your own file, implement the signal logic, and pass
    it to backtest_engine.py via --strategy-file / --strategy-fn.

    Returns a DataFrame of position sizes in [-1, 0, 1] with the same index as prices.
    """
    signals = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)

    # ── YOUR SIGNAL LOGIC HERE ────────────────────────────────────────────────
    # Example: simple RSI-based long signal
    for ticker in prices.columns:
        close = prices[ticker].dropna()
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(param_a).mean()
        loss = (-delta.clip(upper=0)).rolling(param_a).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        signals[ticker] = np.where(rsi < (50 * param_b), 1.0, 0.0)
    # ─────────────────────────────────────────────────────────────────────────

    return signals


# ──────────────────────────────────────────────────────────────────────────────
# Strategy Registry (for programmatic access)
# ──────────────────────────────────────────────────────────────────────────────

STRATEGY_REGISTRY = {
    "momentum": momentum_strategy,
    "mean_reversion": mean_reversion_strategy,
    "dual_momentum": dual_momentum_strategy,
    "template": custom_strategy_template,
}


def get_strategy(name: str):
    """Retrieve a strategy function by name."""
    if name not in STRATEGY_REGISTRY:
        raise ValueError(f"Unknown strategy: '{name}'. Available: {list(STRATEGY_REGISTRY.keys())}")
    return STRATEGY_REGISTRY[name]


if __name__ == "__main__":
    # Quick sanity check
    import yfinance as yf
    print("Fetching SPY, QQQ, IWM for strategy sanity check...")
    prices = yf.download(["SPY", "QQQ", "IWM"], start="2020-01-01", end="2024-12-31",
                          auto_adjust=True, progress=False)["Close"]
    prices.dropna(inplace=True)

    for name, fn in [("momentum", momentum_strategy),
                     ("mean_reversion", mean_reversion_strategy),
                     ("dual_momentum", dual_momentum_strategy)]:
        sig = fn(prices)
        print(f"  {name:20s}: signal shape={sig.shape}, "
              f"non-zero rows={int((sig != 0).any(axis=1).sum())}")
    print("All strategy templates OK.")
