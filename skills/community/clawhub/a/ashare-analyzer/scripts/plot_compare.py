"""
Normalized price comparison chart.

Reference style:
 - Dark navy background
 - Target stock: thick yellow line
 - CSI 300: grey dashed
 - 3-5 peers: rotating teal/pink/purple/blue/orange palette
 - Right-edge labels with latest normalized value (starting value = 100)
 - Title: "<name> (<code>) vs 同行业 — 近1年归一化价格走势"
"""
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "assets"))
from chart_style import (  # noqa: E402
    BG_COLOR, TEXT_COLOR, FG_MUTED,
    TARGET_COLOR, INDEX_COLOR, PEER_PALETTE,
    setup_chinese_font, apply_dark_style, style_legend,
)


def plot_comparison(target_df: pd.DataFrame, target_name: str, target_code: str,
                    index_df: pd.DataFrame,
                    peers: list, out_path: str) -> None:
    """
    target_df / index_df: DataFrame with 'trade_date' and 'close'. Ascending.
    peers: list of dicts [{"ts_code", "name", "df": DataFrame}, ...]
    """
    setup_chinese_font()

    fig, ax = plt.subplots(figsize=(19, 10))
    apply_dark_style(fig, ax)

    # Common date range: use target_df's date range as master
    td = target_df.copy()
    td["trade_date"] = pd.to_datetime(td["trade_date"].astype(str), format="%Y%m%d",
                                      errors="coerce")
    td = td.dropna(subset=["trade_date"]).drop_duplicates(subset=["trade_date"])
    td = td.sort_values("trade_date").reset_index(drop=True)
    base_dates = pd.DatetimeIndex(td["trade_date"].values)

    def _normalize(df, base_idx):
        df = df.copy()
        # Handle both already-parsed datetimes and YYYYMMDD strings
        if pd.api.types.is_datetime64_any_dtype(df["trade_date"]):
            pass
        else:
            df["trade_date"] = pd.to_datetime(df["trade_date"].astype(str),
                                              format="%Y%m%d", errors="coerce")
        df = df.dropna(subset=["trade_date"]).drop_duplicates(subset=["trade_date"])
        df = df.sort_values("trade_date").set_index("trade_date")
        if len(df) == 0:
            return None
        df = df.reindex(base_idx, method="ffill").ffill().bfill()
        first_valid = df["close"].dropna()
        if len(first_valid) == 0:
            return None
        base = first_valid.iloc[0]
        return df["close"] / base * 100

    target_norm = _normalize(td, base_dates)
    if target_norm is None:
        raise RuntimeError("target has no valid close data")

    # Plot peers first (so target line sits on top)
    last_values = []  # [(value, label, color, linewidth)]

    # CSI 300
    if index_df is not None and len(index_df) > 0:
        idx_norm = _normalize(index_df, base_dates)
        if idx_norm is not None:
            ax.plot(base_dates, idx_norm, color=INDEX_COLOR, linewidth=1.3,
                    linestyle="--", label="沪深300", alpha=0.85)
            last_values.append((idx_norm.iloc[-1], "沪深300", INDEX_COLOR))

    # Peers
    for i, peer in enumerate(peers):
        color = PEER_PALETTE[i % len(PEER_PALETTE)]
        pnorm = _normalize(peer["df"], base_dates)
        if pnorm is None:
            continue
        ax.plot(base_dates, pnorm, color=color, linewidth=1.3,
                label=peer["name"], alpha=0.9)
        last_values.append((pnorm.iloc[-1], peer["name"], color))

    # Target (thick yellow on top)
    ax.plot(base_dates, target_norm, color=TARGET_COLOR, linewidth=2.8,
            label=f"{target_name}（目标）", alpha=1.0)
    last_values.append((target_norm.iloc[-1], target_name, TARGET_COLOR))

    # Right-side labels
    # Sort last_values so text doesn't overlap too badly (simple sort by value)
    last_values.sort(key=lambda t: t[0], reverse=True)
    xmax = base_dates[-1]
    x_offset = pd.Timedelta(days=3)
    for val, label, color in last_values:
        ax.text(xmax + x_offset, val, f"{val:.1f}",
                color=color, fontsize=11, fontweight="bold",
                va="center", ha="left")

    title = f"{target_name} ({target_code.split('.')[0]}) vs 同行业 — 近1年归一化价格走势"
    ax.set_title(title, color=TEXT_COLOR, fontsize=14, pad=12)
    ax.set_ylabel("归一化价格（起始=100）", color=TEXT_COLOR)

    leg = ax.legend(loc="upper left", frameon=True, fontsize=10)
    style_legend(leg)

    # X-axis ticks
    ax.set_xlim(base_dates[0], base_dates[-1] + pd.Timedelta(days=12))
    # Month ticks
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    plt.setp(ax.get_xticklabels(), rotation=0, color=TEXT_COLOR)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(out_path, facecolor=BG_COLOR, dpi=120, bbox_inches="tight")
    plt.close(fig)
