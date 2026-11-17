#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
因子热力图评估：对 factor-pure.xlsx 的 12 个因子，按 QuantAll「因子视觉化」管道
（标记全交易日 → X=因子, Y=5日收益, 权重=5日收益 → heat_map）收集密度矩阵，
渲染 4x3 热力图网格 + 每因子效果表（rank-IC / 十分位差 / validity）。

本脚本只用 QuantAllClient（纯 urllib），可在任意含 pandas/matplotlib 的 python 运行。
"""
import json
import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prune_flow import QuantAllClient

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(SCRIPT_DIR, "state")
FINAL = os.path.join(SCRIPT_DIR, "factor-pure.xlsx")

RET5 = "out = (d['close']*d['adj_factor']).shift(-5)/(d['close']*d['adj_factor']) - 1"


def text_of(res):
    try:
        return res["content"][0]["text"]
    except Exception:
        return ""


def weighted_corr(x, y, w):
    """加权 Pearson（用于十分位秩相关近似 rank-IC）"""
    w = np.asarray(w, float)
    w = w / w.sum()
    mx = (x * w).sum()
    my = (y * w).sum()
    xc = x - mx
    yc = y - my
    cov = (xc * yc * w).sum()
    sx = ((xc ** 2) * w).sum() ** 0.5
    sy = ((yc ** 2) * w).sum() ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    return float(cov / (sx * sy))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render-only", action="store_true",
                    help="仅用已保存的 state/heatmaps.json 重新渲染，不调用 QuantAll")
    args = ap.parse_args()

    if args.render_only:
        with open(os.path.join(STATE, "heatmaps.json"), "r", encoding="utf-8") as f:
            results = json.load(f)
        render(results)
        return

    df = pd.read_excel(FINAL)
    client = QuantAllClient(timeout=3600)
    client.connect()

    # 标记全部交易日（所有 股票×日期 散点）
    r0 = client.call_tool("new_layer_from_code", {"name": "all", "code": "out = d['close'] > 0"})
    print("[init] new_layer:", text_of(r0).strip()[:80], flush=True)

    # Y 轴 = 5日收益（百分位，稳健）；权重 = 5日收益（实际值，按用户要求）
    client.call_tool("move_by_code",
                     {"code": RET5, "name": "5日收益", "direction": "y", "to_percentile": True})
    client.call_tool("weight_by_code",
                     {"code": RET5, "name": "5日收益", "to_percentile": False})

    results = []
    for i, row in df.iterrows():
        name = str(row["name"])
        code = str(row["code"]).strip()
        src = str(row["source_file"])
        ir0 = float(row["IR"]) if pd.notna(row.get("IR")) else 0.0
        ic0 = float(row["IC"]) if pd.notna(row.get("IC")) else 0.0

        mx = client.call_tool("move_by_code",
                               {"code": code, "name": name, "direction": "x",
                                "to_percentile": True})
        try:
            mxj = json.loads(text_of(mx))["result"]
            if mxj.get("result") == "失败":
                print(f"  [{i}] {name} move_x FAILED: {mxj.get('message')}", flush=True)
                results.append({"name": name, "error": mxj.get("message")})
                continue
        except Exception as e:
            print(f"  [{i}] {name} parse error: {e}", flush=True)
            results.append({"name": name, "error": str(e)})
            continue

        hm = client.call_tool("heat_map", {"mode": "auto"})
        h = json.loads(text_of(hm))["result"]
        cnt = np.array(h["XY热力图数量"], dtype=float)   # 10x10 数量矩阵
        xstat = np.array(h["X轴统计"], dtype=float)       # 各因子十分位均值5日收益
        summary = h.get("summary", {})

        # 从数量矩阵估 rank-IC（十分位秩相关）
        ny, nx = cnt.shape
        X, Y, W = [], [], []
        for yi in range(ny):
            for xi in range(nx):
                c = cnt[yi, xi]
                if c > 0:
                    X.append(xi); Y.append(yi); W.append(c)
        ic_est = weighted_corr(np.array(X, float), np.array(Y, float), np.array(W, float))
        spread = float(xstat[-1] - xstat[0]) * 100  # 顶减底 十分位差(%)

        results.append({
            "name": name, "source_file": src,
            "ir_orig": ir0, "ic_orig": ic0,
            "rank_ic": ic_est, "spread_pct": spread,
            "validity": summary.get("validity"),
            "slope_x": summary.get("slope_x"),
            "count_matrix": cnt.tolist(),
            "x_stat": xstat.tolist(),
        })
        print(f"  [{i}] {name}: rank_IC={ic_est:.3f} spread={spread:.2f}% "
              f"validity={summary.get('validity')}", flush=True)

    # 保存原始矩阵
    with open(os.path.join(STATE, "heatmaps.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    render(results)


def render(results):
    """用已收集的 results 渲染 4x3 热力图网格 + 效果表（英文标签，避免 CJK 字体缺失）"""
    ok = [r for r in results if "count_matrix" in r]
    n = len(ok)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 5 * rows))
    axes = np.array(axes).reshape(-1)
    # 用全部分位值的 P95 做 vmax，避免单个因子的极端单元（如 Alpha#75 的尾部行）压住颜色尺
    all_cells = np.concatenate([np.array(r["count_matrix"]).ravel() for r in ok])
    vmax = float(np.percentile(all_cells, 95))
    for k, r in enumerate(ok):
        ax = axes[k]
        m = np.array(r["count_matrix"])
        im = ax.imshow(m, origin="lower", cmap="viridis", vmin=0, vmax=vmax,
                       aspect="auto")
        ax.set_title(f"{r['name']}\nrank-IC={r['rank_ic']:.3f}  decile-spread={r['spread_pct']:.2f}%",
                     fontsize=9)
        ax.set_xlabel("factor decile", fontsize=8)
        ax.set_ylabel("5d-return decile", fontsize=8)
        ax.set_xticks(range(10)); ax.set_yticks(range(10))
        ax.tick_params(labelsize=6)
    for k in range(n, len(axes)):
        axes[k].axis("off")
    fig.colorbar(im, ax=axes[:n].tolist(), fraction=0.025, pad=0.02,
                 label="count (thousands)")
    fig.suptitle("12 factors x all trading days  |  X=factor decile, Y=5d-return decile, color=density",
                 fontsize=12)
    fig.subplots_adjust(top=0.92, bottom=0.06, hspace=0.35, wspace=0.25)
    png = os.path.join(SCRIPT_DIR, "factor_heatmaps.png")
    fig.savefig(png, dpi=130)
    print("[render] saved", png, flush=True)

    # ---- 效果表 ----
    tbl = pd.DataFrame([{
        "name": r["name"], "source_file": r["source_file"],
        "IR_orig": round(r["ir_orig"], 4), "IC_orig": round(r["ic_orig"], 4),
        "rank_IC_5d": round(r["rank_ic"], 4),
        "decile_spread_%": round(r["spread_pct"], 3),
        "validity": round(r["validity"], 4) if r["validity"] is not None else None,
    } for r in ok])
    tbl = tbl.sort_values("rank_IC_5d", ascending=False).reset_index(drop=True)
    xlsx = os.path.join(SCRIPT_DIR, "factor_heatmap_summary.xlsx")
    tbl.to_excel(xlsx, index=False)
    print("[render] saved", xlsx, flush=True)
    print(tbl.to_string(index=False))


if __name__ == "__main__":
    main()
