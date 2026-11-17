#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_market.py — L0-L1 全市场缠论结构扫描 (选股漏斗前两层, 纯代码层)
L0: marketdb v_daily_qfq 全A, 剔ST(名称含ST)/上市不足min-bars/近端停牌
L1: 每股 chan_engine.run() 全量计算, 收集"最近 tail-days 根K内出现买卖点"的候选
输出: scan_YYYYMMDD.json {meta, candidates:[{symbol,name,fresh_bsp,pos,ma,invalidations,week_confluence}], stats}
用法:
  python scan_market.py --duckdb data/market.duckdb [--workers 4] [--limit 0] [--out dir]
说明: 结构扫描不做情绪预筛(22ms/股便宜到不需要省), 情绪/资金标签在 L2(fupan_fetch 数据)交叉时再加。
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)


def list_universe(db, min_bars):
    import duckdb
    con = duckdb.connect(db, read_only=True)
    rows = con.execute("""
        SELECT k.thscode, COALESCE(s.name,''), COUNT(*) AS n, MAX(k.date) AS last_d
        FROM v_daily_qfq k LEFT JOIN v_symbol s ON s.thscode = k.thscode
        GROUP BY 1, 2
    """).fetchall()
    latest = max(r[3] for r in rows) if rows else None
    uni = []
    for code, name, n, last_d in rows:
        if n < min_bars:
            continue                       # 上市太短
        if "ST" in (name or "").upper():
            continue                       # 剔ST
        if last_d != latest:
            continue                       # 近端无K=停牌/退市
        uni.append((code, name))
    con.close()
    return uni, str(latest)[:10] if latest else None


def _scan_one(args):
    code, name, db, start, tail_days = args
    try:
        from chan_engine import load_duckdb, run
        rows = load_duckdb(db, code, start)
        if len(rows) < 120:
            return None
        out = run(code, rows, tail_days)
        fresh = out["signals"]["fresh_bsp"]
        if not fresh:
            return None
        return {
            "symbol": code, "name": name, "asof": out["meta"]["asof"],
            "fresh_bsp": fresh,
            "pos_vs_last_zs": out["day"]["pos_vs_last_zs"],
            "last_zs": out["day"]["zs"][-1] if out["day"]["zs"] else None,
            "ma_state": out["ma"]["state"],
            "week_confluence": bool(out["signals"]["week_day_confluence"]),
            "invalidations": out["invalidations"],
        }
    except Exception as e:  # 单股失败不拖垮全扫
        return {"symbol": code, "error": str(e)[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duckdb", required=True)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    ap.add_argument("--min-bars", type=int, default=120)
    ap.add_argument("--start", default=None, help="加速: 只取该日期后的K, 默认全部(建议3年)")
    ap.add_argument("--tail-days", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0, help="调试: 只扫前N只")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    t0 = time.time()
    uni, asof = list_universe(a.duckdb, a.min_bars)
    if a.limit:
        uni = uni[: a.limit]
    tasks = [(c, n, a.duckdb, a.start, a.tail_days) for c, n in uni]

    results, errors = [], []
    if a.workers <= 1:
        it = map(_scan_one, tasks)
    else:
        ex = ProcessPoolExecutor(max_workers=a.workers)
        it = ex.map(_scan_one, tasks, chunksize=64)
    for r in it:
        if r is None:
            continue
        (errors if "error" in r else results).append(r)

    # 排序: 周日共振 > 买点类型(1>2>3) > 有失效价位的
    def rank(c):
        types = "".join(b["type"] for b in c["fresh_bsp"])
        t_rank = 0 if "1" in types else (1 if "2" in types else 2)
        return (not c["week_confluence"], t_rank)
    results.sort(key=rank)

    out = {
        "meta": {"asof": asof, "universe": len(uni), "scanned": len(tasks),
                 "elapsed_s": round(time.time() - t0, 1), "engine": "chan_engine/chanlun_structure_v1",
                 "note": "候选=最近tail_days根K出现bsp, 全部是'当前帧'候选非确认信号"},
        "candidates": results,
        "stats": {
            "n_candidates": len(results),
            "n_errors": len(errors),
            "by_type": _count_types(results),
        },
        "errors": errors[:20],
    }
    tag = (asof or str(date.today())).replace("-", "")
    path = os.path.join(a.out, f"scan_{tag}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print(json.dumps({"written": path, **out["meta"], **out["stats"]}, ensure_ascii=False))


def _count_types(results):
    cnt = {}
    for c in results:
        for b in c["fresh_bsp"]:
            for t in b["type"].split(","):
                key = ("buy_" if b["bs"] == "B" else "sell_") + t.strip()
                cnt[key] = cnt.get(key, 0) + 1
    return cnt


if __name__ == "__main__":
    main()
