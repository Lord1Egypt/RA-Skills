"""
K-line chart renderer matching the reference style:
 - Dark navy background
 - Candles: red up, green down (A-share convention)
 - MA5 (yellow), MA10 (red), MA20 (teal), MA60 (purple)
 - Bollinger bands (dashed grey, shaded)
 - Volume bars colored by up/down day
 - MACD panel (DIF/DEA + histogram)
 - RSI panel with 70/30 reference lines
 - 252-day window, annotated year high/low
 - Title: "<close> (<code>) 日K线 — 近252个交易日"
"""
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "assets"))
from chart_style import (  # noqa: E402
    BG_COLOR, GRID_COLOR, TEXT_COLOR, FG_MUTED,
    UP_COLOR, DOWN_COLOR,
    MA5_COLOR, MA10_COLOR, MA20_COLOR, MA60_COLOR,
    BB_COLOR, MACD_DIF_COLOR, MACD_DEA_COLOR,
    setup_chinese_font, apply_dark_style, style_legend,
)


def plot_kline(df: pd.DataFrame, ts_code: str, out_path: str,
               last_close: float, show_code_only: str = None,
               warmup_df: pd.DataFrame = None) -> None:
    """
    df: DataFrame with columns ['trade_date' (str YYYYMMDD or Timestamp), 'open','high','low','close','vol']
        indexed or not, sorted ascending by date. This is the display window.
    warmup_df: Optional full DataFrame (warmup + display) used for computing indicators.
              If provided, indicators are computed on warmup_df and only the tail (matching df length) is plotted.
    ts_code: e.g. '002418.SZ'
    out_path: png path
    last_close: the most recent close to show in title
    """
    setup_chinese_font()

    df = df.copy().reset_index(drop=True)
    # Normalize trade_date to Timestamp regardless of input dtype (str, object, StringDtype, datetime)
    try:
        is_dt = pd.api.types.is_datetime64_any_dtype(df["trade_date"])
    except Exception:
        is_dt = False
    if not is_dt:
        df["trade_date"] = pd.to_datetime(df["trade_date"].astype(str), format="%Y%m%d",
                                          errors="coerce")
    df = df.sort_values("trade_date").reset_index(drop=True)

    # If warmup data is provided, compute indicators on the full dataset
    # then take only the display tail for plotting
    if warmup_df is not None and len(warmup_df) > len(df):
        full = warmup_df.copy().reset_index(drop=True)
        try:
            is_dt_full = pd.api.types.is_datetime64_any_dtype(full["trade_date"])
        except Exception:
            is_dt_full = False
        if not is_dt_full:
            full["trade_date"] = pd.to_datetime(full["trade_date"].astype(str), format="%Y%m%d",
                                                errors="coerce")
        full = full.sort_values("trade_date").reset_index(drop=True)
        display_len = len(df)
    else:
        full = df
        display_len = len(df)

    # Compute indicators on FULL data (warmup + display), then slice tail for plotting
    full_close = full["close"].astype(float)
    full_high = full["high"].astype(float)
    full_low = full["low"].astype(float)
    full_open = full["open"].astype(float)
    full_vol = full["vol"].astype(float) if "vol" in full.columns else full["volume"].astype(float)
    full_amount = full["amount"].astype(float) if "amount" in full.columns else None

    # Moving averages (on full data)
    _ma5 = full_close.rolling(5).mean()
    _ma10 = full_close.rolling(10).mean()
    _ma20 = full_close.rolling(20).mean()
    _ma60 = full_close.rolling(60).mean()

    # Bollinger bands (20, 2)
    _bb_mid = full_close.rolling(20).mean()
    _bb_std = full_close.rolling(20).std()
    _bb_upper = _bb_mid + 2 * _bb_std
    _bb_lower = _bb_mid - 2 * _bb_std

    # MACD
    _ema12 = full_close.ewm(span=12, adjust=False).mean()
    _ema26 = full_close.ewm(span=26, adjust=False).mean()
    _dif = _ema12 - _ema26
    _dea = _dif.ewm(span=9, adjust=False).mean()
    _macd_hist = 2 * (_dif - _dea)

    # RSI (14)
    _delta = full_close.diff()
    _gain = _delta.clip(lower=0).rolling(14).mean()
    _loss = (-_delta.clip(upper=0)).rolling(14).mean()
    _rs = _gain / _loss.replace(0, np.nan)
    _rsi = 100 - 100 / (1 + _rs)

    # Slice to display window (last display_len rows)
    n = len(full)
    start = n - display_len
    close = full_close.iloc[start:].reset_index(drop=True)
    high = full_high.iloc[start:].reset_index(drop=True)
    low = full_low.iloc[start:].reset_index(drop=True)
    open_ = full_open.iloc[start:].reset_index(drop=True)
    vol = full_vol.iloc[start:].reset_index(drop=True)
    amount = full_amount.iloc[start:].reset_index(drop=True) if full_amount is not None else None
    ma5 = _ma5.iloc[start:].reset_index(drop=True)
    ma10 = _ma10.iloc[start:].reset_index(drop=True)
    ma20 = _ma20.iloc[start:].reset_index(drop=True)
    ma60 = _ma60.iloc[start:].reset_index(drop=True)
    bb_upper = _bb_upper.iloc[start:].reset_index(drop=True)
    bb_lower = _bb_lower.iloc[start:].reset_index(drop=True)
    dif = _dif.iloc[start:].reset_index(drop=True)
    dea = _dea.iloc[start:].reset_index(drop=True)
    macd_hist = _macd_hist.iloc[start:].reset_index(drop=True)
    rsi = _rsi.iloc[start:].reset_index(drop=True)

    # X axis as ordinal integers (smoother for stock charts, no weekend gaps)
    x = np.arange(display_len)

    # === Layout ===
    fig = plt.figure(figsize=(19, 11))
    gs = fig.add_gridspec(
        4, 1,
        height_ratios=[5, 1.2, 1.2, 0.8],
        hspace=0.05,
    )
    ax_price = fig.add_subplot(gs[0])
    ax_vol = fig.add_subplot(gs[1], sharex=ax_price)
    ax_macd = fig.add_subplot(gs[2], sharex=ax_price)
    ax_rsi = fig.add_subplot(gs[3], sharex=ax_price)

    apply_dark_style(fig, [ax_price, ax_vol, ax_macd, ax_rsi])

    # === Price + candles ===
    width_body = 0.6
    width_wick = 0.08
    for i in range(len(df)):
        o, c, h, l = open_.iloc[i], close.iloc[i], high.iloc[i], low.iloc[i]
        color = UP_COLOR if c >= o else DOWN_COLOR
        # Wick
        ax_price.add_patch(Rectangle(
            (x[i] - width_wick / 2, l), width_wick, h - l,
            facecolor=color, edgecolor=color, linewidth=0,
        ))
        # Body
        body_h = abs(c - o)
        if body_h < 1e-9:
            body_h = (h - l) * 0.01 + 0.001
        ax_price.add_patch(Rectangle(
            (x[i] - width_body / 2, min(o, c)), width_body, body_h,
            facecolor=color, edgecolor=color, linewidth=0,
        ))

    # MAs
    ax_price.plot(x, ma5, color=MA5_COLOR, linewidth=1.3, label="MA5")
    ax_price.plot(x, ma10, color=MA10_COLOR, linewidth=1.1, label="MA10")
    ax_price.plot(x, ma20, color=MA20_COLOR, linewidth=1.1, label="MA20")
    ax_price.plot(x, ma60, color=MA60_COLOR, linewidth=1.1, label="MA60")

    # Bollinger bands
    ax_price.plot(x, bb_upper, color=BB_COLOR, linewidth=0.8, linestyle="--",
                  alpha=0.55, label="BB上轨")
    ax_price.plot(x, bb_lower, color=BB_COLOR, linewidth=0.8, linestyle="--",
                  alpha=0.55, label="BB下轨")
    ax_price.fill_between(x, bb_upper, bb_lower, color=BB_COLOR, alpha=0.06)

    # Year high/low annotation
    yh_idx = high.idxmax()
    yl_idx = low.idxmin()
    yh_val = high.iloc[yh_idx]
    yl_val = low.iloc[yl_idx]
    yh_date = df["trade_date"].iloc[yh_idx].strftime("%Y-%m-%d")
    yl_date = df["trade_date"].iloc[yl_idx].strftime("%Y-%m-%d")

    ax_price.annotate(
        f"最高 ¥{yh_val:.2f}\n{yh_date}",
        xy=(x[yh_idx], yh_val),
        xytext=(x[yh_idx] + 3, yh_val + (close.max() - close.min()) * 0.08),
        color=UP_COLOR, fontsize=9, ha="left",
        arrowprops=dict(arrowstyle="->", color=UP_COLOR, lw=1),
        bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR, edgecolor=UP_COLOR, alpha=0.8),
    )
    ax_price.annotate(
        f"最低 ¥{yl_val:.2f}\n{yl_date}",
        xy=(x[yl_idx], yl_val),
        xytext=(x[yl_idx] + 3, yl_val - (close.max() - close.min()) * 0.08),
        color=DOWN_COLOR, fontsize=9, ha="left",
        arrowprops=dict(arrowstyle="->", color=DOWN_COLOR, lw=1),
        bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR, edgecolor=DOWN_COLOR, alpha=0.8),
    )

    code_display = show_code_only or ts_code.split(".")[0]
    title = f"{last_close:.2f} ({code_display}) 日K线 — 近{len(df)}个交易日"
    ax_price.set_title(title, color=TEXT_COLOR, fontsize=14, pad=10)
    ax_price.set_ylabel("价格(元)", color=TEXT_COLOR)
    leg = ax_price.legend(loc="upper left", frameon=True, fontsize=9)
    style_legend(leg)
    ax_price.set_xlim(-1, len(df))

    # === Volume (in 亿元 using amount if available) ===
    # Tencent's 'amount' column is in 元; tushare's is in 千元.
    # The value is usually >= 1e8 when aggregated daily. Auto-detect.
    if amount is not None:
        # Auto-scale: find the divisor that puts values in a sensible range (1-1000)
        max_v = amount.max()
        if max_v > 1e12:
            vol_display = amount / 1e8  # 元 → 亿元
        elif max_v > 1e9:
            vol_display = amount / 1e8  # 元 → 亿元
        else:
            vol_display = amount / 1e5  # 千元 → 亿元 (tushare fallback)
        vol_label = "亿元"
    else:
        vol_display = vol / 1e6  # 手 → 亿股
        vol_label = "亿股"

    vol_colors = [UP_COLOR if close.iloc[i] >= open_.iloc[i] else DOWN_COLOR
                  for i in range(len(df))]
    ax_vol.bar(x, vol_display, color=vol_colors, width=0.75, edgecolor="none")
    ax_vol.set_ylabel(vol_label, color=TEXT_COLOR, fontsize=9)
    ax_vol.set_xlim(-1, len(df))

    # === MACD ===
    hist_colors = [UP_COLOR if v >= 0 else DOWN_COLOR for v in macd_hist]
    ax_macd.bar(x, macd_hist, color=hist_colors, width=0.75, edgecolor="none", alpha=0.75)
    ax_macd.plot(x, dif, color=MACD_DIF_COLOR, linewidth=1.1, label="DIF")
    ax_macd.plot(x, dea, color=MACD_DEA_COLOR, linewidth=1.1, label="DEA")
    ax_macd.axhline(0, color=FG_MUTED, linewidth=0.5, linestyle="-", alpha=0.6)
    ax_macd.set_ylabel("MACD", color=TEXT_COLOR, fontsize=9)
    leg2 = ax_macd.legend(loc="upper left", frameon=True, fontsize=8)
    style_legend(leg2)

    # === RSI ===
    ax_rsi.plot(x, rsi, color="#b49ee7", linewidth=1.1)
    ax_rsi.axhline(70, color=UP_COLOR, linewidth=0.6, linestyle="--", alpha=0.5)
    ax_rsi.axhline(30, color=DOWN_COLOR, linewidth=0.6, linestyle="--", alpha=0.5)
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_ylabel("RSI", color=TEXT_COLOR, fontsize=9)

    # X-axis: show month-day labels at ~sensible tick positions
    n_ticks = 12
    tick_idx = np.linspace(0, len(df) - 1, n_ticks).astype(int)
    tick_labels = [df["trade_date"].iloc[i].strftime("%m/%d") for i in tick_idx]
    ax_rsi.set_xticks(tick_idx)
    ax_rsi.set_xticklabels(tick_labels, rotation=0, color=TEXT_COLOR)
    for ax in (ax_price, ax_vol, ax_macd):
        plt.setp(ax.get_xticklabels(), visible=False)

    # Hide top/right spines cleanly
    for ax in (ax_price, ax_vol, ax_macd, ax_rsi):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.08)
    fig.savefig(out_path, facecolor=BG_COLOR, dpi=120, bbox_inches="tight")
    plt.close(fig)


def compute_indicator_values(df: pd.DataFrame) -> dict:
    """Return the latest technical indicator values for the report."""
    close = df["close"].astype(float)
    open_ = df["open"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    ma5 = close.rolling(5).mean().iloc[-1]
    ma10 = close.rolling(10).mean().iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma60 = close.rolling(60).mean().iloc[-1]

    bb_mid = close.rolling(20).mean()
    bb_std = close.rolling(20).std()
    bb_upper = (bb_mid + 2 * bb_std).iloc[-1]
    bb_lower = (bb_mid - 2 * bb_std).iloc[-1]

    # MACD
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    dif = (ema12 - ema26).iloc[-1]
    dea_series = (ema12 - ema26).ewm(span=9, adjust=False).mean()
    dea = dea_series.iloc[-1]
    macd_hist = 2 * (dif - dea)

    # RSI14
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = (100 - 100 / (1 + rs)).iloc[-1]

    # KDJ (9,3,3)
    low_min = low.rolling(9).min()
    high_max = high.rolling(9).max()
    rsv = 100 * (close - low_min) / (high_max - low_min).replace(0, np.nan)
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    j = 3 * k - 2 * d

    latest_close = close.iloc[-1]
    bb_deviation_pct = (latest_close - bb_upper) / bb_upper * 100 if bb_upper else 0

    # Returns
    def _pct_change(n):
        if len(close) <= n:
            return None
        return (close.iloc[-1] / close.iloc[-n - 1] - 1) * 100

    return {
        "close": float(latest_close),
        "ma5": float(ma5) if pd.notna(ma5) else None,
        "ma10": float(ma10) if pd.notna(ma10) else None,
        "ma20": float(ma20) if pd.notna(ma20) else None,
        "ma60": float(ma60) if pd.notna(ma60) else None,
        "bb_upper": float(bb_upper) if pd.notna(bb_upper) else None,
        "bb_lower": float(bb_lower) if pd.notna(bb_lower) else None,
        "bb_deviation_pct": float(bb_deviation_pct) if pd.notna(bb_deviation_pct) else None,
        "macd_dif": float(dif) if pd.notna(dif) else None,
        "macd_dea": float(dea) if pd.notna(dea) else None,
        "macd_hist": float(macd_hist) if pd.notna(macd_hist) else None,
        "rsi14": float(rsi) if pd.notna(rsi) else None,
        "kdj_k": float(k.iloc[-1]) if pd.notna(k.iloc[-1]) else None,
        "kdj_d": float(d.iloc[-1]) if pd.notna(d.iloc[-1]) else None,
        "kdj_j": float(j.iloc[-1]) if pd.notna(j.iloc[-1]) else None,
        "year_high": float(high.max()),
        "year_low": float(low.min()),
        "year_high_date": str(df["trade_date"].iloc[int(high.values.argmax())]),
        "year_low_date": str(df["trade_date"].iloc[int(low.values.argmin())]),
        "pct_1w": _pct_change(5),
        "pct_1m": _pct_change(20),
        "pct_1y": _pct_change(min(244, len(close) - 1)),
    }
