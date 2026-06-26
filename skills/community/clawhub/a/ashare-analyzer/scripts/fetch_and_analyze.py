#!/usr/bin/env python3
"""
End-to-end pipeline for A-share stock analysis (v2).

Data sources:
  - 价量 (OHLCV): Tencent Finance (股票 + 沪深300 + 同行业对比股)
  - 同行业/同概念/题材: Eastmoney F10 ssbk + board members
  - 基本面: tushare → akshare → baostock → eastmoney fallback chain
  - 主营业务: Eastmoney RPT_F10_FN_MAINOP

Input: stock code or name
Outputs (in --outdir): kline_<code>.png, compare_<code>.png, data_<code>.json
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "..", "assets"))

from plot_kline import plot_kline, compute_indicator_values  # noqa: E402
from plot_compare import plot_comparison  # noqa: E402
from peer_selector import select_peers  # noqa: E402
from fundamental_chain import resolve_fundamentals  # noqa: E402
from resolve_code import resolve  # noqa: E402
from sources import tencent, eastmoney, tushare_src  # noqa: E402


def _retry(fn, *args, tries=3, delay=0.6, **kwargs):
    last = None
    for i in range(tries):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last = e
            time.sleep(delay * (i + 1))
    raise last


CSI300_TENCENT_CODE = "sh000300"
DISPLAY_DAYS = 252          # days shown in charts / report
WARMUP_DAYS = 120           # extra days for indicator warmup (MA60, MACD etc.)
FETCH_DAYS = DISPLAY_DAYS + WARMUP_DAYS + 48  # 420, with buffer for holidays


def _get_daily_kline(code, days=FETCH_DAYS):
    """tushare pro 优先获取K线，失败后 fallback 到腾讯财经。"""
    try:
        result = tushare_src.get_daily_kline(code, days)
        if result is not None and len(result) > 0:
            return result, "tushare"
    except Exception:
        pass
    return tencent.get_daily_kline(code, days), "tencent"


def fetch_all(raw_input: str, outdir: str, verbose: bool = True) -> dict:
    os.makedirs(outdir, exist_ok=True)
    log = (lambda *a: print("[pipeline]", *a, file=sys.stderr)) if verbose else (lambda *a: None)

    # 1. Resolve
    log("Resolving:", raw_input)
    resolved = resolve(raw_input)
    if "error" in resolved:
        raise RuntimeError(resolved["error"])
    if "matches" in resolved:
        raise RuntimeError(
            f"Ambiguous input — {len(resolved['matches'])} matches: "
            + ", ".join(f"{m['name']}({m['code6']})" for m in resolved["matches"])
        )

    code6 = resolved["code6"]
    tencent_code = resolved["tencent_code"]
    name = resolved["name"]
    ts_code = resolved["ts_code"]
    industry = resolved.get("industry", "")
    log(f"Resolved: {name} ({code6}) industry={industry!r}")

    # 2. Target price (fetch extra for warmup, display only last DISPLAY_DAYS)
    log("Fetching K-line (tushare → tencent fallback)...")
    daily_full, price_source = _retry(_get_daily_kline, tencent_code, FETCH_DAYS)
    last_close = float(daily_full["close"].iloc[-1])
    log(f"K-line source: {price_source}, rows (full): {len(daily_full)}, last close: {last_close}")

    log("Fetching Tencent realtime quote...")
    try:
        rt = tencent.get_realtime_quote(tencent_code)
    except Exception as e:
        log(f"Realtime fetch failed: {e}")
        rt = {}

    # 3. CSI 300
    log("Fetching CSI 300...")
    try:
        csi_full = _retry(_get_daily_kline, CSI300_TENCENT_CODE, FETCH_DAYS)[0]
        csi_full = csi_full[csi_full["trade_date"] >= daily_full["trade_date"].iloc[0]].reset_index(drop=True)
    except Exception as e:
        log(f"CSI 300 fetch failed: {e}")
        csi_full = pd.DataFrame()

    # 4. Peers
    log("Selecting peers...")
    peers = select_peers(code6, max_peers=4, verbose=False)
    log(f"Peers: {[(p['name'], p['source']) for p in peers]}")

    peer_data = []
    for p in peers:
        try:
            pdf, peer_price_src = _retry(_get_daily_kline, p["code6"], FETCH_DAYS)
            pdf = pdf[pdf["trade_date"] >= daily_full["trade_date"].iloc[0]].reset_index(drop=True)
            if len(pdf) == 0:
                log(f"  [{p['name']}] empty kline, skipping")
                continue

            # --- 行情数据：腾讯实时 → 东方财富快照 → K线收盘 ---
            try:
                peer_rt = tencent.get_realtime_quote(p["code6"])
            except Exception:
                peer_rt = {}
            snap = eastmoney.get_stock_snapshot(p["code6"]) or {}

            peer_close = peer_rt.get("price") or snap.get("price") or float(pdf["close"].iloc[-1])
            peer_mv = peer_rt.get("total_mv_亿") or ((snap.get("total_mv") or 0) / 1e8)
            peer_pe = peer_rt.get("pe_ttm") or snap.get("pe_dynamic")

            rt_src = "腾讯财经（实时行情）" if peer_rt.get("price") else (
                "东方财富（push2delay快照）" if snap.get("name") else "K线收盘价")

            # --- 基本面数据：tushare pro → 东方财富数据中心 ---
            try:
                pf_ts = tushare_src.get_fundamental_indicators(p["code6"]) or {}
            except Exception:
                pf_ts = {}
            try:
                pf_em = eastmoney.get_fundamental_indicators(p["code6"]) or {}
            except Exception:
                pf_em = {}

            # 合并：tushare 优先，eastmoney 填充
            pf = {}
            for key in ("roe", "gross_margin", "net_margin", "revenue_yoy", "net_profit_yoy"):
                pf[key] = pf_ts.get(key) if pf_ts.get(key) is not None else pf_em.get(key)

            fund_src = "tushare" if any(pf_ts.get(k) is not None for k in ("roe",)) else "东方财富数据中心"

            if len(pdf) >= 2:
                first_close = float(pdf["close"].iloc[0])
                pct_1y = (float(pdf["close"].iloc[-1]) / first_close - 1) * 100
            else:
                pct_1y = None

            peer_data.append({
                "_source": f"行情:{rt_src}｜基本面:{fund_src}｜价量K线:{peer_price_src}",
                "code6": p["code6"],
                "name": p["name"],
                "source": p["source"],
                "df": pdf,
                "close": peer_close,
                "total_mv_yi": peer_mv,
                "pe_ttm": peer_pe,
                "roe": pf.get("roe"),
                "gross_margin": pf.get("gross_margin"),
                "net_margin": pf.get("net_margin"),
                "revenue_yoy": pf.get("revenue_yoy"),
                "net_profit_yoy": pf.get("net_profit_yoy"),
                "pct_1y": pct_1y,
            })
        except Exception as e:
            log(f"  [{p['name']}] skip: {e}")

    # 5. Fundamental chain
    log("Resolving fundamentals...")
    fundamentals = resolve_fundamentals(code6, verbose=verbose)
    log(f"Fundamentals source: {fundamentals.get('source_used')}")

    # 6. Main business
    log("Fetching main business...")
    try:
        main_biz = eastmoney.get_latest_main_business(code6)
    except Exception as e:
        log(f"Main business failed: {e}")
        main_biz = {}

    # 7. Indicators (computed on full data for warmup, values from tail)
    ind = compute_indicator_values(daily_full)

    # 8. Slice to display window for charts — but pass full data to plot_kline
    #    so that MA60/MACD/etc. have warmup and don't start empty
    daily = daily_full.tail(DISPLAY_DAYS).reset_index(drop=True)
    csi = csi_full.tail(DISPLAY_DAYS + 30).reset_index(drop=True) if len(csi_full) else pd.DataFrame()
    csi = csi[csi["trade_date"] >= daily["trade_date"].iloc[0]].reset_index(drop=True) if len(csi) else csi
    for p in peer_data:
        p["df"] = p["df"][p["df"]["trade_date"] >= daily["trade_date"].iloc[0]].reset_index(drop=True)

    log(f"Display window: {len(daily)} rows")

    # 9. Charts
    log("Rendering K-line chart...")
    kline_path = os.path.join(outdir, f"kline_{code6}.png")
    plot_kline(daily, ts_code, kline_path, last_close=last_close, warmup_df=daily_full)

    log("Rendering comparison chart...")
    compare_path = os.path.join(outdir, f"compare_{code6}.png")
    plot_comparison(
        target_df=daily[["trade_date", "close"]].copy(),
        target_name=name,
        target_code=ts_code,
        index_df=csi if len(csi) else pd.DataFrame(),
        peers=[{"code6": p["code6"], "name": p["name"], "df": p["df"]} for p in peer_data],
        out_path=compare_path,
    )

    # 10. Index movements
    csi_pct_1m = csi_pct_1y = None
    if len(csi) > 20:
        csi_pct_1m = (csi["close"].iloc[-1] / csi["close"].iloc[-21] - 1) * 100
    if len(csi) > 240:
        csi_pct_1y = (csi["close"].iloc[-1] / csi["close"].iloc[0] - 1) * 100

    # 11. Bundle
    fund_data = fundamentals.get("data") or {}

    bundle = {
        "meta": {
            "code6": code6,
            "ts_code": ts_code,
            "tencent_code": tencent_code,
            "name": name,
            "industry": industry,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "data_sources": {
                "price": price_source,
                "peers": "eastmoney_f10",
                "fundamental_used": fundamentals.get("source_used"),
                "fundamental_attempts": fundamentals.get("attempts", []),
                "needs_websearch": fundamentals.get("needs_websearch"),
                "main_business": "eastmoney",
            },
        },
        "price": {
            "_source": f"价量K线：{price_source}（tushare优先→腾讯财经兜底）｜实时行情：腾讯财经（qt.gtimg.cn）",
            "close": rt.get("price") or last_close,
            "prev_close": rt.get("pre_close"),
            "pct_today": rt.get("change_pct"),
            "change_today": rt.get("change"),
            "today_high": rt.get("high"),
            "today_low": rt.get("low"),
            "today_open": rt.get("today_open"),
            "turnover_rate": rt.get("turnover_rate"),
            "total_mv_yi": rt.get("total_mv_亿"),
            "float_mv_yi": rt.get("float_mv_亿"),
            "pe_ttm": rt.get("pe_ttm"),
            "pb": rt.get("pb"),
            "amount_yi": (rt.get("amount_万元") or 0) / 1e4,
        },
        "financials": {
            "_source": f"基本面数据来源：{fund_data.get('source') or '未知'}（fallback chain: tushare → akshare → baostock → eastmoney）",
            "end_date": fund_data.get("end_date"),
            "report_name": fund_data.get("report_name"),
            "revenue_yi": (fund_data.get("revenue") or 0) / 1e8 if fund_data.get("revenue") else None,
            "net_profit_wan": (fund_data.get("net_profit") or 0) / 1e4 if fund_data.get("net_profit") else None,
            "revenue_yoy_pct": fund_data.get("revenue_yoy"),
            "net_profit_yoy_pct": fund_data.get("net_profit_yoy"),
            "roe": fund_data.get("roe"),
            "roa": fund_data.get("roa"),
            "gross_margin": fund_data.get("gross_margin"),
            "net_margin": fund_data.get("net_margin"),
            "debt_to_assets": fund_data.get("debt_to_assets"),
            "eps": fund_data.get("eps"),
            "bps": fund_data.get("bps"),
            "source": fund_data.get("source"),
        },
        "main_business": {**main_biz, "_source": "东方财富（RPT_F10_FN_MAINOP）"},
        "technicals": {**ind, "_source": f"由本地脚本基于{price_source}价量数据计算"},
        "market_compare": {
            "_source": f"{price_source}（沪深300指数）",
            "csi300_pct_1m": csi_pct_1m,
            "csi300_pct_1y": csi_pct_1y,
        },
        "peers": [
            {k: v for k, v in p.items() if k != "df"}
            for p in peer_data
        ],
        "outputs": {
            "kline_path": kline_path,
            "compare_path": compare_path,
        },
    }

    def _clean(obj):
        if isinstance(obj, dict):
            return {k: _clean(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_clean(x) for x in obj]
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        if hasattr(obj, "item"):
            try:
                return obj.item()
            except Exception:
                return str(obj)
        return obj

    bundle = _clean(bundle)

    data_path = os.path.join(outdir, f"data_{code6}.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2, default=str)
    bundle["outputs"]["data_path"] = data_path

    log("Done.")
    return bundle


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stock", help="code or name: 002418, 康盛股份, 002418.SZ, sz002418")
    ap.add_argument("--outdir", default="./output")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    try:
        b = fetch_all(args.stock, args.outdir, verbose=not args.quiet)
        print(json.dumps({
            "ok": True,
            "code6": b["meta"]["code6"],
            "name": b["meta"]["name"],
            "outputs": b["outputs"],
            "fundamental_source": b["meta"]["data_sources"]["fundamental_used"],
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)
