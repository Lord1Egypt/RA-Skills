# -*- coding: utf-8 -*-
"""特征分组 · 量化回溯相对收益因子挖掘引擎。

用途：你提出一个特征分组，引擎
  1) 用 DB 历史回放该分组的硬筛规则，
  2) 对每个命中 (个股, 信号日 T) 算 6 格前向相对收益
     （进场 T+1 开盘 / T+1 尾盘 × 持有 T+3 / T+5 / T+10，后复权，相对“规模/板块匹配基准”），
  3) 在分组之上铺单因子 + 配对叠加网格 + 过拟合护栏，输出候选叠加条件及其证据。

分组来源（--group）：
  - discount_relaunch：内置折扣启动（多日序列条件，复用 market_panel 生产函数，语义与线上一致）。
  - custom：你用 --spec FILE 给一份 filter spec（单日特征阈值条件），引擎按它历史回放。
    适合“市值>X、涨幅>Y、换手<Z、回撤>W”这类单日条件组（含容量上涨式）；折扣这类多日
    序列组走内置路径。spec 例见 references/methodology/factor_mining.md。

边界：脚本只铺确定性证据（命中、6 格收益、因子分层、单/配对候选叠加条件 + 护栏标记），
**不挑选“最优解”、不下结论**——叠加条件最优解由模型读 JSON 后判断。

输出：reports/factor_mining_<group>_<asof>.json（证据包）。

环境：
    TUSHARE_TOKEN（回补 daily_basic 用）
    ALPHA_DB_BACKEND=postgresql
    ALPHA_PG_URL=postgresql://alpha_user:alpha_pass@/alpha_data?host=/tmp
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# 直接用 psycopg2 连接走 pd.read_sql 会触发 SQLAlchemy 提示，与 market_panel 同源，无害。
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # market_panel, db_adapter
_BUNDLED_SHARED = HERE / "_shared"
_DEV_SHARED = HERE.parents[2] / "shared" / "data"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from db_core import BACKEND, Backend, get_connection  # noqa: E402
from factor_experiment import log_experiment  # noqa: E402
from market_panel import (  # noqa: E402
    add_numeric_features,
    attach_discount_after_high,
    build_discount_relaunch_samples,
    fetch_by_trade_dates,
    get_pro,
)
from returns_core import (  # noqa: E402
    BENCHMARK_CODES,  # noqa: F401  (保留导出，供调试/向后兼容)
    HORIZONS,
    WIDE_BASE,  # noqa: F401
    _f,
    _r,
    _ymd,
    board_of,  # noqa: F401
    compute_forward_returns,
    load_adj,  # noqa: F401
    load_calendar,
    load_daily,
    load_index,  # noqa: F401
    matched_benchmark,  # noqa: F401
)

REPORTS_DIR = HERE.parent / "reports"

# 规模/板块匹配基准、后复权前向收益、小工具（_f/_r/_ymd）与 DB 价格加载
# （load_calendar/load_daily/load_adj/load_index）已抽到 returns_core。本文件只保留
# 因子挖掘特有的 daily_basic 加载与回补。


_OPS = {">": lambda s, v: s > v, ">=": lambda s, v: s >= v,
        "<": lambda s, v: s < v, "<=": lambda s, v: s <= v, "==": lambda s, v: s == v}


def _apply_cond(series: "pd.Series", op: str, val: float) -> "pd.Series":
    s = pd.to_numeric(series, errors="coerce")
    if op not in _OPS:
        raise SystemExit(f"不支持的操作符：{op}（仅 > >= < <= ==）")
    return _OPS[op](s, val).fillna(False)


# ----------------------------------------------------------------------------
# 数据加载（daily_basic 为回测特有：换手/市值/量比历史 + Tushare 回补）
# load_calendar/load_daily/load_adj/load_index 已移至 returns_core。
# ----------------------------------------------------------------------------
def load_daily_basic(signal_days: List[str]) -> pd.DataFrame:
    lo, hi = min(signal_days), max(signal_days)
    with get_connection() as conn:
        df = pd.read_sql(
            "SELECT ts_code,trade_date,turnover_rate,volume_ratio,total_mv,circ_mv "
            "FROM stock_daily_basic WHERE trade_date BETWEEN %s AND %s",
            conn, params=[lo, hi],
        )
    df["trade_date"] = _ymd(df["trade_date"])
    return df


def load_basic_names() -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql("SELECT ts_code,name,market FROM stock_basic", conn)
    return df


def backfill_daily_basic(signal_days: List[str], max_workers: int = 4,
                         refresh: bool = False) -> Optional[str]:
    """把信号窗口内缺失的 daily_basic 从 Tushare 回补并入 PG 缓存。

    signal_days 必须是 YYYYMMDD（Tushare 要求）。refresh=True 时整窗重取（修复脏缓存）。
    """
    try:
        pro = get_pro()
    except Exception as exc:  # noqa: BLE001
        return f"get_pro failed: {exc}"
    try:
        fetch_by_trade_dates(
            pro,
            "daily_basic",
            signal_days,
            fields="ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv,circ_mv",
            sleep_seconds=0.0,
            cache_enabled=True,
            refresh_cache=refresh,
            max_workers=max_workers,
        )
    except Exception as exc:  # noqa: BLE001
        return f"daily_basic backfill failed: {exc}"
    return None


# ----------------------------------------------------------------------------
# 信号回放：折扣启动（复用生产函数 build_discount_relaunch_samples）
# ----------------------------------------------------------------------------
def replay_discount_relaunch(args: argparse.Namespace) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    calendar = load_calendar()
    if len(calendar) <= args.lookback + 1:
        raise SystemExit(f"日历不足：仅 {len(calendar)} 个交易日 < lookback {args.lookback}")

    # 折扣启动需要完整 lookback 天历史 → 可行信号日 = 第 lookback 个交易日及以后。
    feasible = calendar[args.lookback:]
    end = args.end or calendar[-1]
    start = args.start or feasible[0]
    signal_days = [d for d in feasible if start <= d <= end]
    if not signal_days:
        raise SystemExit("可行信号日为空（检查 --start/--end 与数据深度）")

    backfill_err = None
    if not args.skip_backfill:
        backfill_err = backfill_daily_basic(
            signal_days, max_workers=args.fetch_workers, refresh=args.refresh_basic
        )

    basic_names = load_basic_names()
    name_map = dict(zip(basic_names["ts_code"], basic_names["name"].fillna("")))
    market_map = dict(zip(basic_names["ts_code"], basic_names["market"].fillna("")))

    db_sig = load_daily_basic(signal_days)
    if db_sig.empty:
        raise SystemExit("daily_basic 在信号窗口内为空——需要先回补（去掉 --skip-backfill）")
    mv_map = {(r.ts_code, r.trade_date): r.total_mv for r in db_sig.itertuples()}

    # 廉价闸门：在信号日上找候选 (个股, 日)。用 daily 的 pct_chg/amount + daily_basic 的 total_mv。
    daily_sig = load_daily()  # 全市场，随后只在信号日上过闸
    daily_sig = daily_sig[daily_sig["trade_date"].isin(set(signal_days))].copy()
    daily_sig["pct_chg"] = pd.to_numeric(daily_sig["pct_chg"], errors="coerce")
    daily_sig["amount"] = pd.to_numeric(daily_sig["amount"], errors="coerce")
    daily_sig["total_mv"] = [
        mv_map.get((r.ts_code, r.trade_date)) for r in daily_sig.itertuples()
    ]
    daily_sig["total_mv"] = pd.to_numeric(daily_sig["total_mv"], errors="coerce")
    daily_sig["market"] = daily_sig["ts_code"].map(market_map).fillna("")
    daily_sig["name"] = daily_sig["ts_code"].map(name_map).fillna("")

    gate = daily_sig[
        (daily_sig["total_mv"] / 1e4 > args.market_cap)
        & (daily_sig["amount"] / 1e5 > args.amount)
        & (daily_sig["pct_chg"] > args.pct)
        & (~daily_sig["market"].eq("北交所"))
        & (~daily_sig["ts_code"].str.endswith(".BJ"))
        & (~daily_sig["name"].str.upper().str.contains("ST", na=False))
    ].copy()

    meta: Dict[str, Any] = {
        "group_label": "折扣启动",
        "signal_day_window": [signal_days[0], signal_days[-1]],
        "n_signal_days_scanned": len(signal_days),
        "n_gate_candidates": int(len(gate)),
        "daily_basic_backfill_error": backfill_err,
    }
    if gate.empty:
        return pd.DataFrame(), meta

    universe = sorted(gate["ts_code"].unique().tolist())
    meta["n_gate_universe"] = len(universe)

    # 候选股全历史 → 生产口径数值特征。
    daily_u = load_daily(universe)
    feats = add_numeric_features(daily_u)
    feats["trade_date"] = feats["trade_date"].astype(str)

    # 逐信号日复用 build_discount_relaunch_samples（与线上完全一致）。
    db_idx = db_sig.set_index(["ts_code", "trade_date"])
    signals: List[Dict[str, Any]] = []
    for day, cands in gate.groupby("trade_date"):
        cand_codes = set(cands["ts_code"].tolist())
        feat_hist = feats[feats["ts_code"].isin(cand_codes)]
        disc = attach_discount_after_high(feat_hist, day, args.lookback)
        if not disc:
            continue
        panel_day = feats[(feats["trade_date"] == day) & (feats["ts_code"].isin(cand_codes))].copy()
        if panel_day.empty:
            continue
        # 附 daily_basic（信号日）+ 名称/板块 + 折扣证据列。
        for col in ("total_mv", "circ_mv", "turnover_rate", "volume_ratio"):
            panel_day[col] = [
                db_idx[col].get((r.ts_code, day)) if (r.ts_code, day) in db_idx.index else None
                for r in panel_day.itertuples()
            ]
        panel_day["name"] = panel_day["ts_code"].map(name_map).fillna("")
        panel_day["market"] = panel_day["ts_code"].map(market_map).fillna("")
        for dcol in (
            "prev_high_close", "prev_high_date", "post_low", "post_low_date",
            "low_to_target_days", "discount_after_high", "close_vs_prev_high",
            "monthly_ma10", "monthly_above_ma10",
        ):
            panel_day[dcol] = panel_day["ts_code"].map(
                lambda tc: disc.get(str(tc), {}).get(dcol)
            )
        grp = build_discount_relaunch_samples(
            panel_day,
            market_cap_threshold_100m_yuan=args.market_cap,
            amount_threshold_100m_yuan=args.amount,
            pct_chg_threshold=args.pct,
            discount_min=args.discount_min,
            discount_max=args.discount_max,
            pre_contraction_max=args.contraction_max,
            volume_expansion_min=args.expansion_min,
            high_lookback=args.lookback,
            low_recency_days=args.low_recency,
            sample_limit=10_000,
        )
        for c in grp.get("candidates", []):
            c = dict(c)
            c["signal_date"] = day
            signals.append(c)

    sig_df = pd.DataFrame(signals)
    meta["n_signals"] = int(len(sig_df))
    meta["n_unique_stocks"] = int(sig_df["ts_code"].nunique()) if not sig_df.empty else 0
    return sig_df, meta


# ----------------------------------------------------------------------------
# 信号回放：自定义分组（单日特征阈值 filter spec）
# ----------------------------------------------------------------------------
_PRICE_COLS = {"pct_chg", "amount_100m", "close", "open", "ret_5d", "ret_20d"}


def replay_custom(args: argparse.Namespace) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """按用户给的 filter spec（单日特征阈值条件）历史回放任意分组。

    spec JSON 例：
      {"name": "容量上涨", "warmup": 60,
       "conditions": [["total_mv_100m_yuan", ">", 70], ["amount_100m", ">", 5], ["pct_chg", ">", 8]],
       "exclude_st": true, "exclude_bj": true}
    条件列名取自 add_numeric_features + daily_basic 派生（total_mv_100m_yuan / amount_100m /
    turnover_rate / volume_ratio / drawdown_120_high / close_position_120d / pre_ret_5d / ...）。
    含价量条件（pct_chg / amount_100m）时用作廉价预筛，大幅压缩计算面。
    """
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    conds: List[List[Any]] = spec.get("conditions", [])
    if not conds:
        raise SystemExit("spec 缺少 conditions")
    warmup = int(spec.get("warmup", args.warmup))
    label = str(spec.get("name") or "custom")
    exclude_st = bool(spec.get("exclude_st", True))
    exclude_bj = bool(spec.get("exclude_bj", True))

    calendar = load_calendar()
    feasible = calendar[warmup:] if warmup < len(calendar) else []
    if not feasible:
        raise SystemExit(f"warmup={warmup} ≥ 日历长度 {len(calendar)}")
    end = args.end or calendar[-1]
    start = args.start or feasible[0]
    signal_days = [d for d in feasible if start <= d <= end]
    if not signal_days:
        raise SystemExit("可行信号日为空（检查 --start/--end 与 warmup）")

    backfill_err = None
    if not args.skip_backfill:
        backfill_err = backfill_daily_basic(
            signal_days, max_workers=args.fetch_workers, refresh=args.refresh_basic
        )

    basic_names = load_basic_names()
    name_map = dict(zip(basic_names["ts_code"], basic_names["name"].fillna("")))
    market_map = dict(zip(basic_names["ts_code"], basic_names["market"].fillna("")))

    # 廉价预筛：用价量条件压缩个股宇宙（无价量条件则退化为全市场，给出提示）。
    daily_sig = load_daily()
    daily_sig = daily_sig[daily_sig["trade_date"].isin(set(signal_days))].copy()
    daily_sig["amount_100m"] = pd.to_numeric(daily_sig["amount"], errors="coerce") / 1e5
    daily_sig["pct_chg"] = pd.to_numeric(daily_sig["pct_chg"], errors="coerce")
    daily_sig["name"] = daily_sig["ts_code"].map(name_map).fillna("")
    daily_sig["market"] = daily_sig["ts_code"].map(market_map).fillna("")
    price_conds = [c for c in conds if c[0] in _PRICE_COLS]
    mask = pd.Series(True, index=daily_sig.index)
    for col, op, val in price_conds:
        mask &= _apply_cond(daily_sig[col], op, val)
    if exclude_bj:
        mask &= ~daily_sig["ts_code"].str.endswith(".BJ") & ~daily_sig["market"].eq("北交所")
    if exclude_st:
        mask &= ~daily_sig["name"].str.upper().str.contains("ST", na=False)
    gate = daily_sig[mask].copy()

    meta: Dict[str, Any] = {
        "group_label": label,
        "spec": {"conditions": conds, "warmup": warmup,
                 "exclude_st": exclude_st, "exclude_bj": exclude_bj},
        "signal_day_window": [signal_days[0], signal_days[-1]],
        "n_signal_days_scanned": len(signal_days),
        "n_gate_candidates": int(len(gate)),
        "daily_basic_backfill_error": backfill_err,
        "prefilter_note": "无价量预筛条件，全市场计算" if not price_conds else None,
    }
    if gate.empty:
        return pd.DataFrame(), meta

    universe = sorted(gate["ts_code"].unique().tolist())
    meta["n_gate_universe"] = len(universe)
    feats = add_numeric_features(load_daily(universe))
    feats["trade_date"] = feats["trade_date"].astype(str)
    db_sig = load_daily_basic(signal_days)
    db_idx = db_sig.set_index(["ts_code", "trade_date"]) if not db_sig.empty else None

    non_price = [c for c in conds if c[0] not in _PRICE_COLS]
    signals: List[Dict[str, Any]] = []
    for day, cands in gate.groupby("trade_date"):
        cand_codes = set(cands["ts_code"].tolist())
        panel = feats[(feats["trade_date"] == day) & (feats["ts_code"].isin(cand_codes))].copy()
        if panel.empty:
            continue
        for col in ("total_mv", "circ_mv", "turnover_rate", "volume_ratio"):
            panel[col] = [
                (db_idx[col].get((r.ts_code, day)) if (db_idx is not None and (r.ts_code, day) in db_idx.index) else None)
                for r in panel.itertuples()
            ]
        panel["total_mv_100m_yuan"] = pd.to_numeric(panel["total_mv"], errors="coerce") / 1e4
        panel["amount_100m"] = pd.to_numeric(panel["amount"], errors="coerce") / 1e5
        m = pd.Series(True, index=panel.index)
        for col, op, val in non_price:
            if col not in panel.columns:
                raise SystemExit(f"spec 条件列不存在：{col}")
            m &= _apply_cond(panel[col], op, val)
        sel = panel[m]
        for r in sel.itertuples():
            signals.append({
                "ts_code": r.ts_code, "name": name_map.get(r.ts_code, ""), "signal_date": day,
                "pct_chg": _f(getattr(r, "pct_chg", None)),
                "total_mv_100m_yuan": _f(getattr(r, "total_mv_100m_yuan", None)),
                "amount_100m": _f(getattr(r, "amount_100m", None)),
                "turnover_rate": _f(getattr(r, "turnover_rate", None)),
                "volume_ratio": _f(getattr(r, "volume_ratio", None)),
                "close_position_120d": _f(getattr(r, "close_position_120d", None)),
                "drawdown_120_high": _f(getattr(r, "drawdown_120_high", None)),
                "pre_ret_5d": _f(getattr(r, "pre_ret_5d", None)),
                "amount_vs_prev5_ratio": _f(getattr(r, "amount_vs_prev5_ratio", None)),
                "ret_5d": _f(getattr(r, "ret_5d", None)),
                "ret_20d": _f(getattr(r, "ret_20d", None)),
            })

    sig_df = pd.DataFrame(signals)
    meta["n_signals"] = int(len(sig_df))
    meta["n_unique_stocks"] = int(sig_df["ts_code"].nunique()) if not sig_df.empty else 0
    return sig_df, meta


def replay(args: argparse.Namespace) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    if args.group == "custom":
        if not args.spec:
            raise SystemExit("--group custom 需要 --spec FILE")
        return replay_custom(args)
    return replay_discount_relaunch(args)


# HORIZONS 与 compute_forward_returns 已移至 returns_core（见文件顶部 import）。


# ----------------------------------------------------------------------------
# 基础组 6 格 + 因子分层 + 候选叠加条件（含护栏）
# ----------------------------------------------------------------------------
def cell_stats(s: pd.Series, rel: pd.Series) -> Dict[str, Any]:
    v = s.dropna()
    r = rel.dropna()
    if len(v) == 0:
        return {"n": 0}
    return {
        "n": int(len(v)),
        "mean": _r(v.mean()), "median": _r(v.median()),
        "win": _r((v > 0).mean() * 100, 1),
        "rel_mean": _r(r.mean()) if len(r) else None,
        "rel_win": _r((r > 0).mean() * 100, 1) if len(r) else None,
    }


def base_six_cells(df: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for entry, tag in (("open", "ro"), ("close", "rc")):
        rtag = "relo" if entry == "open" else "relc"
        for k in HORIZONS:
            out[f"{entry}_T+{k}"] = cell_stats(df.get(f"{tag}_{k}", pd.Series(dtype=float)),
                                               df.get(f"{rtag}_{k}", pd.Series(dtype=float)))
    return out


FACTOR_BINS = {
    "turnover_rate": ([0, 5, 10, 20, 1e9], ["<5%", "5-10%", "10-20%", ">20%"]),
    "total_mv_100m_yuan": ([0, 150, 300, 1e9], ["80-150亿", "150-300亿", ">300亿"]),
    "pct_chg": ([7, 9.7, 15, 30], ["7-9.7%", "涨停10cm", "20cm板"]),
    "t1_gap": ([-50, 0, 3, 7, 40], ["低开", "高开0-3%", "高开3-7%", "高开>7%"]),
    "volume_ratio": ([0, 1.5, 2.5, 4, 100], ["<1.5", "1.5-2.5", "2.5-4", ">4"]),
    "discount_after_high": ([0.6, 0.7, 0.78, 0.85], ["0.6-0.7", "0.7-0.78", "0.78-0.85"]),
    "close_position_120d": ([0, 0.2, 0.4, 0.6, 1.01], ["<0.2", "0.2-0.4", "0.4-0.6", ">0.6"]),
    "pre_ret_5d": ([-60, -5, 0, 5, 60], ["<-5%", "-5~0%", "0-5%", ">5%"]),
    "amount_vs_prev5_ratio": ([2, 3, 5, 1e9], ["2-3", "3-5", ">5"]),
}


def factor_layers(df: pd.DataFrame, obj_col: str, abs_col: str,
                  extra_bins: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    base = df[obj_col].dropna()
    bins_map = {**FACTOR_BINS, **(extra_bins or {})}
    for fac, (bins, labels) in bins_map.items():
        if fac not in df.columns:
            continue
        sub = df.dropna(subset=[fac, obj_col]).copy()
        if sub.empty:
            continue
        sub["_b"] = pd.cut(pd.to_numeric(sub[fac], errors="coerce"), bins=bins, labels=labels)
        layers = []
        means = []
        for lab in labels:
            cell = sub[sub["_b"] == lab]
            if cell.empty:
                layers.append({"layer": lab, "n": 0})
                means.append(None)
                continue
            m = cell[obj_col].mean()
            means.append(m)
            layers.append({
                "layer": lab, "n": int(len(cell)),
                "obj_mean": _r(m),
                "abs_mean": _r(cell[abs_col].mean()) if abs_col in cell else None,
                "win": _r((cell[abs_col] > 0).mean() * 100, 1) if abs_col in cell else None,
            })
        valid = [m for m in means if m is not None]
        monotonic = len(valid) >= 3 and (
            all(x <= y for x, y in zip(valid, valid[1:])) or all(x >= y for x, y in zip(valid, valid[1:]))
        )
        out[fac] = {"layers": layers, "monotonic": bool(monotonic)}
    return out


HALF_MIN = 8          # 每个时间半区最小样本
BALANCE_MIN = 0.3     # 弱半区 / 强半区 下限（防边际全堆在某一段 = regime 脆弱）


def _combo_stats(sub: pd.DataFrame, label: str, factor_key: str, obj_col: str, abs_col: str,
                 min_n: int, base_obj: Optional[float], split: Optional[str],
                 mask_key: Any = None) -> Optional[Dict[str, Any]]:
    """一个叠加条件（或条件组合）的 G∧c 表现 + 内外样本一致性 + 护栏判定。

    护栏（全部满足才 passes_guardrails）：保留样本≥min_n；前后两个时间半区各≥HALF_MIN；
    确实超过基础组（delta_vs_base>0）；前后半区目标均为正；
    且弱半区/强半区≥BALANCE_MIN（边际不能全靠某一段行情）。
    """
    sub = sub.dropna(subset=[obj_col])
    n = len(sub)
    if n < min_n:
        return None
    obj_mean = sub[obj_col].mean()
    first = sub[sub["signal_date"] <= split][obj_col] if split else pd.Series(dtype=float)
    second = sub[sub["signal_date"] > split][obj_col] if split else pd.Series(dtype=float)
    fm = first.mean() if len(first) else None
    sm = second.mean() if len(second) else None
    delta = (obj_mean - base_obj) if base_obj is not None else None
    both_pos = fm is not None and sm is not None and fm > 0 and sm > 0
    balance = (min(fm, sm) / max(fm, sm)) if (both_pos and max(fm, sm) > 0) else 0.0
    passes = bool(
        n >= min_n and len(first) >= HALF_MIN and len(second) >= HALF_MIN
        and delta is not None and delta > 0 and both_pos and balance >= BALANCE_MIN
    )
    rec = {
        "condition": label, "factor": factor_key, "n_retained": int(n),
        "obj_mean": _r(obj_mean), "delta_vs_base": _r(delta),
        "abs_mean": _r(sub[abs_col].mean()) if abs_col in sub else None,
        "win": _r((sub[abs_col] > 0).mean() * 100, 1) if abs_col in sub else None,
        "oos_first_mean": _r(fm), "oos_second_mean": _r(sm), "oos_balance": _r(balance, 2),
        "n_first": int(len(first)), "n_second": int(len(second)),
        "passes_guardrails": passes,
    }
    if mask_key is not None:
        rec["_mask_key"] = mask_key
    return rec


def _cut_mask(df: pd.DataFrame, fac: str, op: str, edge: float) -> "pd.Series":
    col = pd.to_numeric(df[fac], errors="coerce")
    return (col >= edge) if op == ">=" else (col < edge)


def overlay_singles(df: pd.DataFrame, obj_col: str, abs_col: str,
                    min_n: int, base_obj: Optional[float],
                    extra_bins: Optional[Dict[str, Any]] = None,
                    min_n_extra: Optional[int] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """单因子叠加条件网格。脚本不挑赢家，只标 pass/fail。

    extra_bins 里的 provider 因子用 min_n_extra（更高，压多重检验）；不传时行为与核心 9 因子完全一致。
    """
    dates = sorted(df["signal_date"].dropna().unique().tolist())
    split = dates[len(dates) // 2] if dates else None
    out: List[Dict[str, Any]] = []
    bins_map = {**FACTOR_BINS, **(extra_bins or {})}
    extra_keys = set(extra_bins or {})
    for fac, (bins, _labels) in bins_map.items():
        if fac not in df.columns:
            continue
        mn = min_n_extra if (fac in extra_keys and min_n_extra is not None) else min_n
        for edge in bins[1:-1]:  # 内部切点
            for op in (">=", "<"):
                st = _combo_stats(df[_cut_mask(df, fac, op, edge)], f"{fac} {op} {edge:g}", fac,
                                  obj_col, abs_col, mn, base_obj, split, mask_key=(fac, op, edge))
                if st:
                    out.append(st)
    out.sort(key=lambda c: (c["delta_vs_base"] is not None, c["delta_vs_base"] or -1e9), reverse=True)
    return out, split


def overlay_pairs(df: pd.DataFrame, singles: List[Dict[str, Any]], obj_col: str, abs_col: str,
                  min_n: int, base_obj: Optional[float], split: Optional[str],
                  max_factors: int = 8, provider_factors: Optional[set] = None,
                  min_n_extra: Optional[int] = None) -> List[Dict[str, Any]]:
    """配对叠加（深度≤2）：取每个因子最优的单条件，跨不同因子两两组合。

    任一因子是 provider 时该配对用 min_n_extra（更高门槛）；不传 provider 时与核心行为一致。
    """
    provider_factors = provider_factors or set()
    best: Dict[str, Dict[str, Any]] = {}
    for c in singles:
        if c.get("delta_vs_base") is None:
            continue
        fac = c["factor"]
        if fac not in best or c["delta_vs_base"] > best[fac]["delta_vs_base"]:
            best[fac] = c
    facs = sorted(best.values(), key=lambda c: c["delta_vs_base"], reverse=True)[:max_factors]
    out: List[Dict[str, Any]] = []
    for i in range(len(facs)):
        for j in range(i + 1, len(facs)):
            a, b = facs[i], facs[j]
            fa, opa, ea = a["_mask_key"]
            fb, opb, eb = b["_mask_key"]
            mask = _cut_mask(df, fa, opa, ea) & _cut_mask(df, fb, opb, eb)
            mn = (min_n_extra if (min_n_extra is not None
                  and (a["factor"] in provider_factors or b["factor"] in provider_factors))
                  else min_n)
            st = _combo_stats(df[mask], f"{a['condition']} ∧ {b['condition']}",
                              f"{fa}+{fb}", obj_col, abs_col, mn, base_obj, split)
            if st:
                st["_mask_keys"] = [a["_mask_key"], b["_mask_key"]]
                out.append(st)
    out.sort(key=lambda c: (c["delta_vs_base"] is not None, c["delta_vs_base"] or -1e9), reverse=True)
    return out


# ----------------------------------------------------------------------------
# 证据分片：决策包（模型读）只留结论 + 少量例证，逐条 signals 明细单独落 detail 文件
# （见 references/methodology/factor_mining.md §七；决策包纪律 ≤150KB）。
# ----------------------------------------------------------------------------
_EXAMPLE_FACTOR_COLS = [
    "pct_chg", "total_mv_100m_yuan", "turnover_rate", "volume_ratio",
    "close_position_120d", "discount_after_high", "amount_vs_prev5_ratio",
]


def _signals_summary(sig_df: pd.DataFrame) -> Dict[str, Any]:
    """命中信号的分布摘要（替代整列 dump）：总数、按月、按板块。"""
    if sig_df.empty:
        return {"total": 0}
    months = sig_df["signal_date"].astype(str).str[:6]
    by_month = {str(m): int(c) for m, c in months.value_counts().sort_index().items()}
    by_board: Dict[str, int] = {}
    if "board" in sig_df.columns:
        by_board = {str(b): int(c) for b, c in sig_df["board"].value_counts().items()}
    return {
        "total": int(len(sig_df)),
        "unique_stocks": int(sig_df["ts_code"].nunique()),
        "by_month": by_month,
        "by_board": by_board,
    }


def _example_rows(sub: pd.DataFrame, obj_col: str, abs_col: str, n: int = 3) -> List[Dict[str, Any]]:
    """从命中子集取 ≤n 条例证，按目标格收益取「高/中/低」分布（不只挑赢家，便于诚实引用）。"""
    sub = sub.dropna(subset=[obj_col]).copy()
    if sub.empty:
        return []
    sub = sub.sort_values(obj_col, ascending=False)
    if len(sub) <= n:
        picks = sub
    else:
        picks = sub.iloc[[0, len(sub) // 2, len(sub) - 1]]  # top / median / bottom
    rows: List[Dict[str, Any]] = []
    for r in picks.itertuples():
        rec: Dict[str, Any] = {
            "ts_code": getattr(r, "ts_code", None),
            "name": getattr(r, "name", None),
            "signal_date": getattr(r, "signal_date", None),
            obj_col: _r(getattr(r, obj_col, None)),
            abs_col: _r(getattr(r, abs_col, None)),
        }
        for f in _EXAMPLE_FACTOR_COLS:
            v = getattr(r, f, None)
            if v is not None and pd.notna(v):
                rec[f] = _r(v)
        rows.append(rec)
    return rows


def build_examples(df: pd.DataFrame, singles: List[Dict[str, Any]], pairs: List[Dict[str, Any]],
                   obj_col: str, abs_col: str) -> Dict[str, List[Dict[str, Any]]]:
    """给每条「过闸」叠加条件配 ≤3 条命中例证（非过闸条件不配——不会被引用）。"""
    examples: Dict[str, List[Dict[str, Any]]] = {}
    for c in singles:
        if not c.get("passes_guardrails") or "_mask_key" not in c:
            continue
        fac, op, edge = c["_mask_key"]
        examples[c["condition"]] = _example_rows(df[_cut_mask(df, fac, op, edge)], obj_col, abs_col)
    for c in pairs:
        if not c.get("passes_guardrails") or "_mask_keys" not in c:
            continue
        (fa, opa, ea), (fb, opb, eb) = c["_mask_keys"]
        mask = _cut_mask(df, fa, opa, ea) & _cut_mask(df, fb, opb, eb)
        examples[c["condition"]] = _example_rows(df[mask], obj_col, abs_col)
    return examples


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
SIGNAL_FACTOR_COLS = [
    "turnover_rate", "volume_ratio", "total_mv_100m_yuan", "pct_chg", "discount_after_high",
    "close_position_120d", "pre_ret_5d", "amount_vs_prev5_ratio", "pre_volume_contraction_ratio",
    "ret_5d", "ret_20d", "t1_gap",
]


def run_mining(args: argparse.Namespace) -> Dict[str, Any]:
    """执行一次因子挖掘，返回组装好的 evidence/detail —— 纯取数 + 计算，不做文件 I/O、
    不登记实验、不打印摘要，供 CLI 主流程与测试复用。

    返回 dict：evidence / detail(None if empty) / group_key / asof / obj_col / sig_df / empty。
    """
    if getattr(args, "asof", None) and not getattr(args, "end", None):
        args.end = args.asof

    calendar = load_calendar()
    sig_df, meta = replay(args)
    asof = args.end or calendar[-1]
    group_label = meta.get("group_label", args.group)
    group_key = args.group if args.group != "custom" else (
        re.sub(r"\W+", "_", group_label).strip("_") or "custom")

    obj_entry_tag = "relo" if args.entry == "open" else "relc"
    obj_abs_tag = "ro" if args.entry == "open" else "rc"
    obj_col = f"{obj_entry_tag}_{args.horizon}"      # 目标格相对收益（匹配基准）
    abs_col = f"{obj_abs_tag}_{args.horizon}"        # 目标格绝对收益

    evidence: Dict[str, Any] = {
        "meta": {
            "group": args.group,
            "group_label": group_label,
            "asof": asof,
            "objective_cell": f"T+1{args.entry}->T+{args.horizon} 相对匹配基准",
            "benchmark_scheme": "板块/市值匹配（科创50/创业板指/沪深300/中证500/中证1000），沪深300 宽基对照",
            "min_n": args.min_n,
            "guardrails": (
                f"叠加条件过闸需：保留样本≥{args.min_n}；前后两个时间半区各≥{HALF_MIN}且均为正；"
                f"确实超过基础组（Δ>0）；弱/强半区比≥{BALANCE_MIN}（边际不能全堆在某一段行情）。"
            ),
            "data_coverage": {
                "calendar_days": len(calendar),
                "calendar_span": [calendar[0], calendar[-1]],
            },
            "caveats": [
                "样本窗口与市场环境单一，是证据扫描，不是跨周期统计结论。",
                "ST 用当前名称近似剔除，无法还原历史 ST 状态。",
                "均值易被少数极端赢家抬高，需同看中位数与胜率；叠加条件最优解由模型判断。",
            ],
            **meta,
        }
    }

    if sig_df.empty:
        evidence["base_cells"] = {}
        evidence["factor_layers"] = {}
        evidence["overlay_singles"] = []
        evidence["overlay_pairs"] = []
        evidence["signals_summary"] = {"total": 0}
        evidence["examples"] = {}
        return {"evidence": evidence, "detail": None, "group_key": group_key,
                "asof": asof, "obj_col": obj_col, "sig_df": sig_df, "empty": True}

    sig_df = compute_forward_returns(sig_df, calendar)

    # 跨技能因子（v1）：附 forecast/theme 派生列（as-of 防泄漏），覆盖足够才进叠加网格。
    import factor_providers as fp
    sig_df, factor_coverage = fp.compute_providers(sig_df, calendar)
    overlay_provider_bins = {k: v for k, v in fp.PROVIDER_BINS.items()
                             if factor_coverage.get(k, {}).get("enters_overlay")}
    prov_min_n = max(args.min_n, 25)  # provider 因子叠加门槛更高，压多重检验

    base_cells = base_six_cells(sig_df)
    base_obj = base_cells.get(f"{args.entry}_T+{args.horizon}", {}).get("rel_mean")
    layers = factor_layers(sig_df, obj_col, abs_col, extra_bins=fp.PROVIDER_BINS)
    singles, split = overlay_singles(sig_df, obj_col, abs_col, args.min_n, base_obj,
                                     extra_bins=overlay_provider_bins, min_n_extra=prov_min_n)
    pairs = overlay_pairs(sig_df, singles, obj_col, abs_col, args.min_n, base_obj, split,
                          provider_factors=set(fp.PROVIDER_COLS), min_n_extra=prov_min_n)
    examples = build_examples(sig_df, singles, pairs, obj_col, abs_col)
    singles_out = [{k: v for k, v in c.items() if k != "_mask_key"} for c in singles]
    pairs_out = [{k: v for k, v in c.items() if k != "_mask_keys"} for c in pairs]

    keep_cols = ["ts_code", "name", "signal_date", "board", "benchmark"] + SIGNAL_FACTOR_COLS + \
        [f"{p}_{k}" for p in ("ro", "rc", "relo", "relc") for k in HORIZONS]
    keep_cols = [c for c in keep_cols if c in sig_df.columns]
    signals_out = sig_df[keep_cols].replace({np.nan: None}).to_dict(orient="records")

    evidence["base_cells"] = base_cells
    evidence["factor_layers"] = layers
    evidence["overlay_singles"] = singles_out
    evidence["overlay_pairs"] = pairs_out
    evidence["signals_summary"] = _signals_summary(sig_df)
    evidence["examples"] = examples
    evidence["meta"]["factor_coverage"] = factor_coverage
    detail = {
        "meta": {"group": args.group, "group_label": group_label, "asof": asof,
                 "objective_cell": evidence["meta"]["objective_cell"], "n_signals": len(signals_out)},
        "signals": signals_out,
    }
    return {"evidence": evidence, "detail": detail, "group_key": group_key,
            "asof": asof, "obj_col": obj_col, "sig_df": sig_df, "empty": False}


def main() -> None:
    ap = argparse.ArgumentParser(description="特征分组量化回溯因子挖掘引擎")
    ap.add_argument("--group", default="discount_relaunch", choices=["discount_relaunch", "custom"])
    ap.add_argument("--spec", default=None, help="custom 分组的 filter spec JSON 路径")
    ap.add_argument("--warmup", type=int, default=120, help="custom 分组特征预热交易日数")
    ap.add_argument("--asof", default=None, help="信号窗口结束日 YYYYMMDD（默认最新交易日）")
    ap.add_argument("--start", default=None, help="信号窗口起始日 YYYYMMDD")
    ap.add_argument("--end", default=None, help="同 --asof，优先级更高")
    ap.add_argument("--entry", default="close", choices=["open", "close"], help="默认目标格进场")
    ap.add_argument("--horizon", type=int, default=5, choices=HORIZONS, help="默认目标格持有期")
    ap.add_argument("--min-n", dest="min_n", type=int, default=20, help="叠加条件最小保留样本")
    ap.add_argument("--fetch-workers", dest="fetch_workers", type=int, default=4)
    ap.add_argument("--skip-backfill", dest="skip_backfill", action="store_true",
                    help="跳过 daily_basic 回补（仅用已缓存日，快速冒烟）")
    ap.add_argument("--refresh-basic", dest="refresh_basic", action="store_true",
                    help="整窗重取 daily_basic（修复脏缓存）")
    # 折扣启动阈值（镜像 SKILL.md 默认）
    ap.add_argument("--market-cap", dest="market_cap", type=float, default=80.0)
    ap.add_argument("--amount", type=float, default=5.0)
    ap.add_argument("--pct", type=float, default=7.0)
    ap.add_argument("--discount-min", dest="discount_min", type=float, default=0.6)
    ap.add_argument("--discount-max", dest="discount_max", type=float, default=0.85)
    ap.add_argument("--contraction-max", dest="contraction_max", type=float, default=0.9)
    ap.add_argument("--expansion-min", dest="expansion_min", type=float, default=2.0)
    ap.add_argument("--lookback", type=int, default=200)
    ap.add_argument("--low-recency", dest="low_recency", type=int, default=5)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    result = run_mining(args)

    evidence = result["evidence"]
    group_key, asof, obj_col = result["group_key"], result["asof"], result["obj_col"]
    if result["empty"]:
        ev_path = _write(evidence, args, group_key, asof)
        log_experiment(evidence, args, group_key, asof, ev_path)
        print("[done] 无命中信号——只写出 meta。")
        return

    ev_path = _write(evidence, args, group_key, asof, detail=result["detail"])
    log_experiment(evidence, args, group_key, asof, ev_path)
    _print_summary(evidence, result["sig_df"], obj_col)


def _write(evidence: Dict[str, Any], args: argparse.Namespace, group_key: str, asof: str,
           detail: Optional[Dict[str, Any]] = None) -> str:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else REPORTS_DIR / f"factor_mining_{group_key}_{asof}.json"
    if detail is not None:
        detail_path = out.with_name(out.stem + "_detail.json")
        detail_path.write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
        evidence["meta"]["detail_file"] = detail_path.name
        evidence["meta"]["detail_signals"] = detail.get("meta", {}).get("n_signals")
        print(f"[detail]   {detail_path}  (signals={detail.get('meta', {}).get('n_signals')})")
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    kb = len(json.dumps(evidence, ensure_ascii=False)) / 1024
    print(f"[evidence] {out}  ({kb:.1f} KB)")
    return str(out)


def _print_summary(evidence: Dict[str, Any], sig_df: pd.DataFrame, obj_col: str) -> None:
    m = evidence["meta"]
    print(f"\n=== {m.get('group_label')} 量化回溯 ({m['asof']}) ===")
    print(f"信号窗口 {m.get('signal_day_window')}  扫描 {m.get('n_signal_days_scanned')} 个交易日"
          f"  命中 {m.get('n_signals')} 条 / {m.get('n_unique_stocks')} 只股")
    print(f"目标格：{m['objective_cell']}（基准=板块/市值匹配）\n")
    print("基础组 6 格（绝对 均值/胜率 ｜ 相对匹配基准 均值/胜率）：")
    for cell, st in evidence["base_cells"].items():
        if st.get("n"):
            print(f"  {cell:<12} N={st['n']:>3}  绝对{st['mean']:>6}/{st['win']:>5}%  "
                  f"相对{st.get('rel_mean')}/{st.get('rel_win')}%")

    def _show(title: str, rows: List[Dict[str, Any]]) -> None:
        passed = [c for c in rows if c["passes_guardrails"]]
        print(f"\n{title}（过闸 {len(passed)}/{len(rows)}，脚本不挑最优，留给模型）：")
        for c in passed[:10]:
            print(f"  ✓ {c['condition']:<34} N={c['n_retained']:>3}  目标{c['obj_mean']:>6}  "
                  f"Δ{c['delta_vs_base']:>6}  胜{c['win']}%  内外 {c['oos_first_mean']}/{c['oos_second_mean']}"
                  f"  均衡{c['oos_balance']}")
        if not passed:
            print("  （无候选过闸——多半样本太小或边际偏一段行情，符合预期；见 caveats）")

    _show("单因子叠加条件", evidence["overlay_singles"])
    _show("配对叠加条件（深度2）", evidence["overlay_pairs"])


if __name__ == "__main__":
    main()
