#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
双因子热力图评估：对 factor-pure.xlsx 的 N 个因子，生成所有无序因子对 (i<j)。
每对按 QuantAll「因子视觉化」管道：
    标记全交易日 → X=factor_i(十分位), Y=factor_j(十分位), 权重=5日收益 → heat_map
收集：
    - 密度矩阵 (XY热力图数量, 10x10)  —— 两因子的联合分布
    - 权重矩阵 (XY热力图权重, 10x10)  —— 每格的「平均5日收益」
渲染：
    1) 权重图：颜色 = 平均5日收益(%)，发散色，看两因子如何共同预测收益
    2) 密度图：颜色 = 散点数量，看两因子联合覆盖是否均匀（避免空格误读）
    3) 每对指标表：因子相关性(冗余度) / 对角收益差(互补强度) / 极值格

本脚本只用 QuantAllClient（纯 urllib），可在任意含 pandas/matplotlib 的 python 运行。
"""
import json
import os
import sys
import time
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


def call_retry(client, tool, args, tries=6, sleep=8):
    """带退避重试（应对 QuantAll 并发锁 '有其它任务在执行'）"""
    last = None
    for i in range(tries):
        r = client.call_tool(tool, args)
        t = text_of(r)
        try:
            j = json.loads(t)
        except Exception:
            last = t[:80]
            time.sleep(sleep)
            continue
        res = j.get("result")
        # 失败判定：result 是 dict 且 result.result == '失败'
        # （成功时 result 可能是字符串如 '完成,数量:...' 或含矩阵的 dict）
        if isinstance(res, dict) and res.get("result") == "失败":
            last = res.get("message", "失败")
            print(f"    [{tool}] busy/失败 retry {i+1}: {last}", flush=True)
            time.sleep(sleep)
            continue
        return j
    raise RuntimeError(f"{tool} 重试{tries}次仍失败: {last}")


def weighted_corr(x, y, w):
    """加权 Pearson（由密度矩阵估两因子十分位的相关性 = 冗余度）"""
    w = np.asarray(w, float)
    s = w.sum()
    if s <= 0:
        return 0.0
    w = w / s
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


def collect():
    df = pd.read_excel(FINAL)
    df = df.reset_index(drop=True)
    n = len(df)
    names = [str(r["name"]) for _, r in df.iterrows()]
    codes = [str(r["code"]).strip() for _, r in df.iterrows()]
    ics = [float(r["IC"]) if pd.notna(r.get("IC")) else 0.0 for _, r in df.iterrows()]
    srcs = [str(r["source_file"]) for _, r in df.iterrows()]

    client = QuantAllClient(timeout=3600)
    client.connect()

    # 标记全部交易日（所有 股票×日期 散点）
    call_retry(client, "new_layer_from_code",
               {"name": "all", "code": "out = d['close'] > 0"})
    print("[init] layer created", flush=True)
    # 权重 = 5日收益（实际值）
    call_retry(client, "weight_by_code",
               {"code": RET5, "name": "5d_ret", "to_percentile": False})

    pairs = []
    total = n * (n - 1) // 2
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            k += 1
            ni, nj = names[i], names[j]
            ci, cj = codes[i], codes[j]
            # 设置 X / Y 轴为两个不同因子（均十分位）
            call_retry(client, "move_by_code",
                       {"code": ci, "name": ni, "direction": "x", "to_percentile": True})
            call_retry(client, "move_by_code",
                       {"code": cj, "name": nj, "direction": "y", "to_percentile": True})
            hm = call_retry(client, "heat_map", {"mode": "auto"})["result"]
            cnt = np.array(hm["XY热力图数量"], dtype=float)      # 10x10 密度
            wmat = np.array(hm["XY热力图权重"], dtype=float)     # 10x10 平均5日收益
            pairs.append({
                "i": i, "j": j, "name_i": ni, "name_j": nj,
                "src_i": srcs[i], "src_j": srcs[j],
                "ic_i": ics[i], "ic_j": ics[j],
                "count_matrix": cnt.tolist(),
                "weight_matrix": wmat.tolist(),
            })
            print(f"  [{k}/{total}] {ni} x {nj}  "
                  f"done (cnt_sum={cnt.sum()/1000:.0f}k)", flush=True)

    with open(os.path.join(STATE, "pairs.json"), "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    print("[collect] saved state/pairs.json", flush=True)
    return pairs


def analyze(pairs):
    """每对：因子相关性(冗余度) + 对角收益差(互补强度) + 极值格"""
    rows = []
    for p in pairs:
        cnt = np.array(p["count_matrix"], dtype=float)
        w = np.array(p["weight_matrix"], dtype=float)
        ny, nx = cnt.shape
        # 因子相关性：由密度矩阵估两因子十分位加权 Pearson
        X, Y, W = [], [], []
        for yi in range(ny):
            for xi in range(nx):
                c = cnt[yi, xi]
                if c > 0:
                    X.append(xi); Y.append(yi); W.append(c)
        fc = weighted_corr(np.array(X, float), np.array(Y, float), np.array(W, float))

        # 按各自 IC 符号对齐方向：IC>0 高分=好，IC<0 翻转
        ww = w.copy()
        if p["ic_i"] < 0:
            ww = ww[::-1, :]
        if p["ic_j"] < 0:
            ww = ww[:, ::-1]
        good = np.nanmean(ww[8:10, 8:10])   # 右上角(高-高)
        bad = np.nanmean(ww[0:2, 0:2])      # 左下角(低-低)
        spread = float((good - bad) * 100)  # %

        # 极值格
        amax = np.nanargmax(ww)
        imax, jmax = np.unravel_index(amax, ww.shape)
        amaxv = float(ww[imax, jmax] * 100)
        amin = np.nanargmin(ww)
        imin, jmin = np.unravel_index(amin, ww.shape)
        aminv = float(ww[imin, jmin] * 100)

        rows.append({
            "factor_i": p["name_i"], "factor_j": p["name_j"],
            "src_i": p["src_i"].replace("factor-", "").replace(".xlsx", ""),
            "src_j": p["src_j"].replace("factor-", "").replace(".xlsx", ""),
            "factor_corr": round(fc, 4),
            "corner_spread_%": round(spread, 3),
            "best_cell_%": round(amaxv, 3),
            "best_cell_decile": f"({imax},{jmax})",
            "worst_cell_%": round(aminv, 3),
            "worst_cell_decile": f"({imin},{jmin})",
            "ic_i": round(p["ic_i"], 4), "ic_j": round(p["ic_j"], 4),
        })
    return rows


def render(pairs):
    ok = [p for p in pairs if "weight_matrix" in p and np.array(p["weight_matrix"]).sum() > 0]
    n = len(ok)
    cols = 8
    rows = (n + cols - 1) // cols

    # ---- 图1：权重 = 平均5日收益(%) ----
    wmats = [np.array(p["weight_matrix"], dtype=float) * 100 for p in ok]
    vmax = float(np.nanpercentile(np.concatenate([m.ravel() for m in wmats]), 97))
    vmax = max(vmax, 0.05)
    fig1, axes1 = plt.subplots(rows, cols, figsize=(2.0 * cols, 1.95 * rows))
    axes1 = np.array(axes1).reshape(-1)
    for k, p in enumerate(ok):
        ax = axes1[k]
        m = wmats[k]
        im = ax.imshow(m, origin="lower", cmap="RdBu_r", vmin=-vmax, vmax=vmax,
                       aspect="auto")
        ax.set_title(f"{p['name_i']}\n× {p['name_j']}", fontsize=7)
        ax.set_xticks([]); ax.set_yticks([])
    for k in range(n, len(axes1)):
        axes1[k].axis("off")
    fig1.colorbar(im, ax=axes1[:n].tolist(), fraction=0.02, pad=0.02,
                  label="mean 5d return (%)")
    fig1.suptitle("Pairwise factor heatmap  |  X & Y = two different factor deciles, "
                  "color = mean 5d return (%)  |  red=up, blue=down", fontsize=11)
    fig1.subplots_adjust(top=0.90, bottom=0.04, hspace=0.35, wspace=0.15)
    png1 = os.path.join(SCRIPT_DIR, "factor_pairs_weight.png")
    fig1.savefig(png1, dpi=130)
    print("[render] saved", png1, flush=True)

    # ---- 图2：密度 = 散点数量 ----
    cmats = [np.array(p["count_matrix"], dtype=float) for p in ok]
    cvmax = float(np.percentile(np.concatenate([m.ravel() for m in cmats]), 95))
    fig2, axes2 = plt.subplots(rows, cols, figsize=(2.0 * cols, 1.95 * rows))
    axes2 = np.array(axes2).reshape(-1)
    for k, p in enumerate(ok):
        ax = axes2[k]
        m = cmats[k]
        im = ax.imshow(m, origin="lower", cmap="viridis", vmin=0, vmax=cvmax,
                       aspect="auto")
        ax.set_title(f"{p['name_i']} × {p['name_j']}", fontsize=7)
        ax.set_xticks([]); ax.set_yticks([])
    for k in range(n, len(axes2)):
        axes2[k].axis("off")
    fig2.colorbar(im, ax=axes2[:n].tolist(), fraction=0.02, pad=0.02,
                  label="count (thousands)")
    fig2.suptitle("Pairwise factor density  |  X & Y = two different factor deciles, "
                  "color = number of (stock x day) points", fontsize=11)
    fig2.subplots_adjust(top=0.90, bottom=0.04, hspace=0.35, wspace=0.15)
    png2 = os.path.join(SCRIPT_DIR, "factor_pairs_count.png")
    fig2.savefig(png2, dpi=130)
    print("[render] saved", png2, flush=True)

    # ---- 指标表 ----
    rows_tbl = analyze(ok)
    tbl = pd.DataFrame(rows_tbl)
    tbl = tbl.sort_values("corner_spread_%", ascending=False).reset_index(drop=True)
    xlsx = os.path.join(SCRIPT_DIR, "factor_pairs_summary.xlsx")
    tbl.to_excel(xlsx, index=False)
    print("[render] saved", xlsx, flush=True)
    print(tbl.to_string(index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render-only", action="store_true",
                    help="仅用已保存的 state/pairs.json 重新渲染，不调用 QuantAll")
    args = ap.parse_args()
    if args.render_only:
        pairs = json.load(open(os.path.join(STATE, "pairs.json"), encoding="utf-8"))
        render(pairs)
        return
    pairs = collect()
    render(pairs)


if __name__ == "__main__":
    main()
