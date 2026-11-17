# -*- coding: utf-8 -*-
"""跨技能因子 provider（v1）：把 earnings-forecast 与 theme 台账里"信号日当日可知"的
确定性信息，作为额外因子并入因子挖掘的分层观察（覆盖足够时才进叠加网格）。

红线（防未来函数）：并入信号日 T 的因子，其信息可得时间必须 ≤ T 当晚（进场是 T+1）。
  - forecast：只取 first_ann_date <= T 的预告（T 当天已披露）；预告修订的更晚版本不得泄漏。
  - theme：只用 T 当日 theme_daily_state；台账覆盖窗口外一律 null（不臆造 0）。
  - **禁用 forecast_verdict.tier**：那是模型事后判分，判定时间不可考，v1 不入因子面。

覆盖诚实：theme members_sample 是**样本非全集**（under-inclusive），且按股票名匹配；命中=1
可信，未命中=0 只表示"不在这份样本里"，不等于"不在该主题"。meta.factor_coverage 报 null 占比。

这些 provider 全部只读 forecast_* / theme_* 台账（它们分别由 earnings-forecast / daily-market-sense
维护），本模块不写任何表。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_BUNDLED_SHARED = HERE / "_shared"
_DEV_SHARED = HERE.parents[2] / "shared" / "data"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from db_core import get_connection, table_exists  # noqa: E402

# "强势在场"状态集（对齐 theme_lifecycle.md / HTML 泳道图"红=强势在场、闪电=低位启动"语义）。
ACTIVE_THEME_STATES = ("主线确认", "在场候选", "低位启动", "再聚焦")

# 覆盖率闸门：null 占比 > 此值的 provider 因子只进分层观察、不进叠加网格（防在小子集上挑假条件）。
MAX_NULL_FRAC_FOR_OVERLAY = 0.60


# --------------------------------------------------------------------------- #
# 数据加载（一次性拉小表进内存建查找，规模都很小：forecast 数十行、theme 数百行）
# --------------------------------------------------------------------------- #
def _load_forecast() -> Dict[str, List[Tuple[str, Optional[float]]]]:
    """ts_code -> [(first_ann_date, cum_yoy_med), ...] 按 first_ann_date 升序。"""
    out: Dict[str, List[Tuple[str, Optional[float]]]] = {}
    with get_connection() as conn:
        if not table_exists(conn, "forecast_cache"):
            return out
        cur = conn.cursor()
        cur.execute("SELECT ts_code, first_ann_date, ann_date, p_change_min, p_change_max FROM forecast_cache")
        rows = cur.fetchall()
    for ts_code, first_ann, ann, pmin, pmax in rows:
        ann_date = str(first_ann or ann or "")
        if not ann_date:
            continue
        vals = [v for v in (pmin, pmax) if v is not None]
        cum_yoy = float(np.mean(vals)) if vals else None
        out.setdefault(ts_code, []).append((ann_date, cum_yoy))
    for ts_code in out:
        out[ts_code].sort(key=lambda r: r[0])
    return out


def _load_theme() -> Tuple[Dict[str, set], Optional[str], Optional[str]]:
    """trade_date -> 该日处于"强势在场"状态的主线成员名集合；外加台账覆盖窗口 [min,max]。"""
    active_by_date: Dict[str, set] = {}
    dates: List[str] = []
    with get_connection() as conn:
        if not table_exists(conn, "theme_daily_state"):
            return active_by_date, None, None
        cur = conn.cursor()
        cur.execute("SELECT trade_date, state, members_sample FROM theme_daily_state")
        rows = cur.fetchall()
    for trade_date, state, members in rows:
        d = str(trade_date).replace("-", "")
        dates.append(d)
        if state not in ACTIVE_THEME_STATES or not members:
            continue
        names = active_by_date.setdefault(d, set())
        for m in members:
            if isinstance(m, str):
                names.add(m)
            elif isinstance(m, dict):
                names.add(m.get("name") or m.get("ts_code"))
    if not dates:
        return active_by_date, None, None
    return active_by_date, min(dates), max(dates)


# --------------------------------------------------------------------------- #
# provider 计算（返回与 sig_df.index 对齐的 Series）
# --------------------------------------------------------------------------- #
def _days_between(calendar_index: Dict[str, int], d0: str, d1: str) -> Optional[int]:
    i0, i1 = calendar_index.get(d0), calendar_index.get(d1)
    return (i1 - i0) if (i0 is not None and i1 is not None) else None


def _latest_forecast(fc_rows: List[Tuple[str, Optional[float]]], asof: str) -> Optional[Tuple[str, Optional[float]]]:
    """first_ann_date <= asof 的最新一条（as-of，防未来）。"""
    eligible = [r for r in fc_rows if r[0] <= asof]
    return eligible[-1] if eligible else None


def compute_providers(sig_df: pd.DataFrame, calendar: List[str]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """给 sig_df 附三个跨技能因子列，返回 (sig_df, coverage)。sig_df 需含 ts_code/name/signal_date。"""
    df = sig_df.copy()
    cal_index = {d: i for i, d in enumerate(calendar)}
    forecast = _load_forecast()
    active_by_date, th_min, th_max = _load_theme()

    days_since, cum_yoy, in_theme = [], [], []
    for r in df.itertuples():
        tc, name, T = getattr(r, "ts_code", None), getattr(r, "name", None), str(getattr(r, "signal_date", ""))
        # forecast（as-of: first_ann_date <= T）
        fc = _latest_forecast(forecast.get(tc, []), T) if tc in forecast else None
        if fc is None:
            days_since.append(None); cum_yoy.append(None)
        else:
            days_since.append(_days_between(cal_index, fc[0], T))
            cum_yoy.append(fc[1])
        # theme（覆盖窗口外 = null；窗口内命中"强势在场"成员 = 1，否则 0）
        if th_min is None or T < th_min or T > th_max:
            in_theme.append(None)
        else:
            in_theme.append(1 if (name and name in active_by_date.get(T, set())) else 0)

    df["days_since_forecast_ann"] = days_since
    df["forecast_cum_yoy_med"] = cum_yoy
    df["in_active_theme"] = in_theme

    coverage = {}
    for col in PROVIDER_COLS:
        n = len(df)
        null_frac = float(df[col].isna().mean()) if n else 1.0
        coverage[col] = {
            "n_total": n,
            "n_non_null": int(df[col].notna().sum()),
            "null_frac": round(null_frac, 3),
            "enters_overlay": bool(null_frac <= MAX_NULL_FRAC_FOR_OVERLAY),
        }
    coverage["_theme_window"] = [th_min, th_max]
    coverage["_note"] = ("theme members_sample 是 under-inclusive 样本、按股票名匹配；"
                         "命中=1 可信，未命中=0 仅表示不在该样本内。禁用 forecast_verdict.tier 防事后泄漏。")
    return df, coverage


# provider 因子的分箱定义（并入 factor_layers / 满足覆盖时并入 overlay）。
PROVIDER_BINS: Dict[str, Tuple[list, list]] = {
    "days_since_forecast_ann": ([0, 5, 20, 60, 1e9], ["≤5d", "5-20d", "20-60d", ">60d"]),
    "forecast_cum_yoy_med": ([-1e9, 0, 30, 100, 1e9], ["<0", "0-30%", "30-100%", ">100%"]),
    "in_active_theme": ([-0.5, 0.5, 1.5], ["非在场", "强势在场"]),
}
PROVIDER_COLS = list(PROVIDER_BINS.keys())
