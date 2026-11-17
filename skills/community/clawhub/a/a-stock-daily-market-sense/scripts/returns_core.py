# -*- coding: utf-8 -*-
"""前向相对收益度量层（skill 本地公共能力）。

这是回测引擎（factor_backtest.py）使用的度量原子：规模/板块匹配基准、
后复权前向收益与 6 格相对收益。

为什么放 skill 本地 scripts/ 而不是 _shared/：`matched_benchmark` 编码了
「板块→基准、主板内按市值档」这类**领域判断**，按本仓库 shared-vs-skill 边界
原则（通用能力放 _shared、领域判断留 skill），它属于 skill 域。DB 连接仍走
_shared/db_core。

口径（与 references/methodology/factor_mining.md §二 一致）：
  - 信号日 T：个股入选当天。
  - 进场 T+1 开盘 / T+1 尾盘；持有到 T+3 / T+5 / T+10 收盘 → 6 格。
  - 价格后复权（adj_factor），相对收益 = 个股收益 − 匹配基准同窗口收益。
  - 沪深300 另作宽基对照列（relo_k_w / relc_k_w）。
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

HERE = Path(__file__).resolve().parent
_BUNDLED_SHARED = HERE / "_shared"
_DEV_SHARED = HERE.parents[2] / "shared" / "data"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from db_core import get_connection  # noqa: E402

# 规模/板块匹配基准（用户决策：先按板块、主板内再按市值档）。沪深300 另作宽基对照。
WIDE_BASE = "sh.000300"  # 沪深300，宽基对照列
BENCHMARK_CODES = ["000688.SH", "399006.SZ", "sh.000300", "sh.000905", "sh.000852", "sz.399303"]
HORIZONS = [3, 5, 10]


def matched_benchmark(ts_code: str, total_mv_wan: Optional[float]) -> str:
    """逐观测按板块 + 市值档分配基准代码。"""
    prefix = str(ts_code)[:3]
    if prefix in ("688", "689"):
        return "000688.SH"  # 科创50
    if prefix in ("300", "301"):
        return "399006.SZ"  # 创业板指
    mv_yi = (total_mv_wan or 0) / 1e4
    if mv_yi >= 300:
        return "sh.000300"  # 沪深300
    if mv_yi >= 80:
        return "sh.000905"  # 中证500
    return "sh.000852"      # 中证1000


def board_of(ts_code: str) -> str:
    p = str(ts_code)[:3]
    if p in ("688", "689"):
        return "科创板"
    if p in ("300", "301"):
        return "创业板"
    if p[0] in ("8", "4"):
        return "北交所"
    if p in ("600", "601", "603", "605"):
        return "沪主板"
    return "深主板"


def _f(x: Any) -> Optional[float]:
    try:
        v = float(x)
        return v if np.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def _r(x: Any, n: int = 2) -> Optional[float]:
    v = _f(x)
    return round(v, n) if v is not None else None


def _ymd(s: "pd.Series") -> "pd.Series":
    """统一交易日为 YYYYMMDD 字符串。

    DB 的 trade_date 是 DATE 列，原生读出是日期对象/带横杠字符串；而生产函数
    （月线解析用 format='%Y%m%d'）、Tushare API 都要 YYYYMMDD。所有 DB 读取后必须
    过这一层，否则月线趋势过滤会整列判 None。
    """
    return pd.to_datetime(s).dt.strftime("%Y%m%d")


# ----------------------------------------------------------------------------
# 数据加载（价格 / 复权因子 / 指数 / 日历）
# ----------------------------------------------------------------------------
def load_calendar() -> List[str]:
    with get_connection() as conn:
        df = pd.read_sql(
            "SELECT DISTINCT trade_date FROM stock_daily ORDER BY trade_date", conn
        )
    return sorted(_ymd(df["trade_date"]).tolist())


def load_daily(ts_codes: Optional[List[str]] = None) -> pd.DataFrame:
    cols = "ts_code,trade_date,open,high,low,close,pre_close,pct_chg,vol,amount"
    with get_connection() as conn:
        if ts_codes:
            ph = ",".join(["%s"] * len(ts_codes))
            df = pd.read_sql(
                f"SELECT {cols} FROM stock_daily WHERE ts_code IN ({ph})",
                conn, params=ts_codes,
            )
        else:
            df = pd.read_sql(f"SELECT {cols} FROM stock_daily", conn)
    df["trade_date"] = _ymd(df["trade_date"])
    return df


def load_adj(ts_codes: List[str]) -> pd.DataFrame:
    ph = ",".join(["%s"] * len(ts_codes))
    with get_connection() as conn:
        df = pd.read_sql(
            f"SELECT ts_code,trade_date,adj_factor FROM stock_adj_factor WHERE ts_code IN ({ph})",
            conn, params=ts_codes,
        )
    df["trade_date"] = _ymd(df["trade_date"])
    return df


def load_index(codes: List[str]) -> pd.DataFrame:
    ph = ",".join(["%s"] * len(codes))
    with get_connection() as conn:
        df = pd.read_sql(
            f"SELECT ts_code,trade_date,open,close FROM stock_index_daily WHERE ts_code IN ({ph})",
            conn, params=codes,
        )
    df["trade_date"] = _ymd(df["trade_date"])
    return df


# ----------------------------------------------------------------------------
# 6 格前向相对收益（匹配基准 + 宽基对照）
# ----------------------------------------------------------------------------
def compute_forward_returns(sig_df: pd.DataFrame, calendar: List[str]) -> pd.DataFrame:
    """对每个 (个股, 信号日 T) 算 6 格前向收益，并入相对匹配基准/宽基对照。

    入参 sig_df 至少含 ts_code、signal_date；若含 total_mv_100m_yuan 则用于匹配基准，
    否则按缺省（市值未知）落入小盘基准。返回原 df + 各格列：
      ro_k/rc_k（绝对，open/close 进场）、relo_k/relc_k（相对匹配基准）、
      relo_k_w/relc_k_w（相对沪深300 宽基）、t1_gap、benchmark、board。
    """
    if sig_df.empty:
        return sig_df
    codes = sorted(sig_df["ts_code"].unique().tolist())
    px = load_daily(codes)[["ts_code", "trade_date", "open", "close", "pre_close"]].copy()
    adj = load_adj(codes)
    px = px.merge(adj, on=["ts_code", "trade_date"], how="left")
    px = px.sort_values(["ts_code", "trade_date"])
    px["adj_factor"] = px.groupby("ts_code")["adj_factor"].ffill().fillna(1.0)
    for col in ("open", "close", "pre_close"):
        px[col] = pd.to_numeric(px[col], errors="coerce")
    px["adj_open"] = px["open"] * px["adj_factor"]
    px["adj_close"] = px["close"] * px["adj_factor"]

    idx = load_index(BENCHMARK_CODES)
    for col in ("open", "close"):
        idx[col] = pd.to_numeric(idx[col], errors="coerce")
    idx_open = {(r.ts_code, r.trade_date): r.open for r in idx.itertuples()}
    idx_close = {(r.ts_code, r.trade_date): r.close for r in idx.itertuples()}

    aopen = {(r.ts_code, r.trade_date): r.adj_open for r in px.itertuples()}
    aclose = {(r.ts_code, r.trade_date): r.adj_close for r in px.itertuples()}
    rawopen = {(r.ts_code, r.trade_date): r.open for r in px.itertuples()}
    preclose = {(r.ts_code, r.trade_date): r.pre_close for r in px.itertuples()}

    cal_idx = {d: i for i, d in enumerate(calendar)}

    def offset(d: str, k: int) -> Optional[str]:
        i = cal_idx.get(d)
        if i is None or i + k >= len(calendar):
            return None
        return calendar[i + k]

    def idx_ret(code: str, d_from: str, d_to: str, use_open: bool) -> Optional[float]:
        base = idx_open.get((code, d_from)) if use_open else idx_close.get((code, d_from))
        end = idx_close.get((code, d_to))
        if base and end and base != 0:
            return (end / base - 1.0) * 100.0
        return None

    rows = []
    for r in sig_df.itertuples():
        tc, T = r.ts_code, r.signal_date
        t1 = offset(T, 1)
        rec: Dict[str, Any] = {"ts_code": tc, "signal_date": T}
        if t1 is None:
            rows.append(rec)
            continue
        e_open = aopen.get((tc, t1))
        e_close = aclose.get((tc, t1))
        pc1 = preclose.get((tc, t1))
        ro1 = rawopen.get((tc, t1))
        rec["t1_date"] = t1
        if e_open is None or e_close is None:
            rows.append(rec)
            continue
        rec["t1_gap"] = (ro1 / pc1 - 1.0) * 100.0 if (ro1 and pc1) else None
        rec["t1_open"] = _f(ro1)
        rec["t1_close"] = _f(e_close)
        total_mv_wan = getattr(r, "total_mv_100m_yuan", None)
        total_mv_wan = total_mv_wan * 1e4 if total_mv_wan else None
        bench = getattr(r, "benchmark", None) or matched_benchmark(tc, total_mv_wan)
        rec["benchmark"] = bench
        rec["board"] = board_of(tc)
        for k in HORIZONS:
            tk = offset(T, k)
            rec[f"t{k}_date"] = tk
            xc = aclose.get((tc, tk)) if tk else None
            if xc is None:
                continue
            rec[f"t{k}_close"] = _f(xc)
            ro = (xc / e_open - 1.0) * 100.0
            rc = (xc / e_close - 1.0) * 100.0
            rec[f"ro_{k}"] = ro
            rec[f"rc_{k}"] = rc
            bo = idx_ret(bench, t1, tk, True)
            bc = idx_ret(bench, t1, tk, False)
            rec[f"relo_{k}"] = (ro - bo) if bo is not None else None
            rec[f"relc_{k}"] = (rc - bc) if bc is not None else None
            wo = idx_ret(WIDE_BASE, t1, tk, True)
            wc = idx_ret(WIDE_BASE, t1, tk, False)
            rec[f"relo_{k}_w"] = (ro - wo) if wo is not None else None
            rec[f"relc_{k}_w"] = (rc - wc) if wc is not None else None
        rows.append(rec)

    fwd = pd.DataFrame(rows)
    return sig_df.merge(fwd, on=["ts_code", "signal_date"], how="left", suffixes=("", "_fwd"))
