#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
窗口优化方案 (window optimization) —— 以 top10% / bottom10% 两个分位窗口为优化对象
===================================================================================
与之前"用整体 IC 排序 + 去相关"不同, 本方案把优化对象换成因子的两个分位窗口:
  - top10%    : 因子值最高的 10% 股票窗口
  - bottom10% : 因子值最低的 10% 股票窗口
每个因子在两侧各有一组指标(IC / IR / time_potential / coverage), 来自 QuantAll factor_analysis 输出。

数据有效率(coverage)门限:
  - 若某侧 coverage < 0.07  -> 该侧"放弃", 把该侧的 IC/IR/TP 置 0 来标示;
  - 但"不放弃整个因子": 只置 0 失败的那一侧, 另一侧若 coverage>=0.07 仍然保留;
  - 两侧同时 <0.07 时, 两侧都置 0, 行仍保留(整因子贡献为 0, 但不在数据里删除)。

输出: scripts/factor-window-opt.xlsx  (不覆盖 factor-pure.xlsx)

窗口化演示(--window-ratio):
  去相关时 benchmark 只与 score>=r*score(benchmark) 的候选算相关, 离线估算可省的相关计算量。
  真正的逐对去相关需要 QuantAll(待 tmGmYm 跑完后再接)。
"""
import os
import argparse
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE, "output")
OUT_NAME = "factor-window-opt.xlsx"
COV_FLOOR = 0.07  # 有效率门限


def load_factors():
    recs = []
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if not f.endswith(".xlsx"):
            continue
        # 跳过历史产物, 只读原始因子库
        if f.startswith(("pruned", "factor-pure", "factor-window")):
            continue
        path = os.path.join(OUTPUT_DIR, f)
        df = pd.read_excel(path)
        # 文件名去掉 factor-/facotr- 前缀作为来源标签
        src = f.replace("factor-", "").replace("facotr-", "").replace(".xlsx", "")
        for _, r in df.iterrows():
            recs.append((src, r))
    return recs


def num(v):
    try:
        return float(v)
    except Exception:
        return float("nan")


def gate_and_score(src, r):
    out = {"source": src, "name": r.get("name"), "code": r.get("code")}
    # 整体指标(仅作参考)
    out["IC"] = num(r.get("IC"))
    out["IR"] = num(r.get("IR"))
    out["coverage"] = num(r.get("coverage"))

    # 两侧分窗口处理
    for side in ("top10%", "bottom10%"):
        ic = num(r.get(f"{side}_IC"))
        ir = num(r.get(f"{side}_IR"))
        tp = num(r.get(f"{side}_time_potential"))
        cov = num(r.get(f"{side}_coverage"))
        keep = 1 if cov >= COV_FLOOR else 0
        # 放弃侧: 把有效性指标置 0 标示
        out[f"{side}_IC"] = ic if keep else 0.0
        out[f"{side}_IR"] = ir if keep else 0.0
        out[f"{side}_time_potential"] = tp if keep else 0.0
        out[f"{side}_coverage"] = cov
        out[f"{side}_keep"] = keep

    # 综合得分: 两侧有效 IR 绝对值之和(放弃侧为 0, 自动不贡献)
    out["score"] = abs(out["top10%_IR"]) + abs(out["bottom10%_IR"])
    out["sides_kept"] = out["top10%_keep"] + out["bottom10%_keep"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=50, help="选中因子数(按 score 排序, 至少保留一侧)")
    ap.add_argument("--cov-floor", type=float, default=COV_FLOOR)
    ap.add_argument("--window-ratio", type=float, default=None,
                    help="演示: 去相关时 benchmark 只与 score>=r*score(benchmark) 的候选算相关")
    args = ap.parse_args()

    recs = load_factors()
    rows = [gate_and_score(s, r) for s, r in recs]
    df = pd.DataFrame(rows)

    # 有效率高的因子排前面
    df = df.sort_values("score", ascending=False).reset_index(drop=True)

    # 选中: 至少保留一侧, 取 score 最高的 top N
    df["selected"] = 0
    cnt = 0
    for i in range(len(df)):
        if df.at[i, "sides_kept"] >= 1:
            df.at[i, "selected"] = 1
            cnt += 1
            if cnt >= args.top:
                break

    # 窗口化演示(无需 QuantAll, 仅估算可省的相关计算量)
    win_note = ""
    if args.window_ratio is not None:
        full_pairs = 0
        win_pairs = 0
        for i in range(len(df)):
            bench = df.at[i, "score"]
            cands = df.iloc[i + 1:]
            full_pairs += len(cands)
            win_pairs += int((cands["score"] >= args.window_ratio * bench).sum())
        saved = 1 - (win_pairs / full_pairs) if full_pairs else 0
        win_note = (f"\n[窗口演示 ratio={args.window_ratio}] 全量需算相关对={full_pairs}, "
                    f"窗口内={win_pairs}, 可省约 {saved * 100:.1f}%")

    out_path = os.path.join(BASE, OUT_NAME)
    df.to_excel(out_path, index=False)

    abandoned_top = int((df["top10%_keep"] == 0).sum())
    abandoned_bottom = int((df["bottom10%_keep"] == 0).sum())
    both = int(((df["top10%_keep"] == 0) & (df["bottom10%_keep"] == 0)).sum())
    print(f"因子总数: {len(df)}")
    print(f"top10% 侧因 coverage<{args.cov_floor} 被置0: {abandoned_top}")
    print(f"bottom10% 侧因 coverage<{args.cov_floor} 被置0: {abandoned_bottom}")
    print(f"两侧同时被置0(整因子无贡献, 但行保留): {both}")
    print(f"选中(selected=1, 至少保留一侧, top {args.top}): {int(df['selected'].sum())}")
    print(f"输出 -> {out_path}")
    print(win_note)
    print("\nTop10 预览:")
    cols = ["name", "source", "top10%_IR", "top10%_keep",
            "bottom10%_IR", "bottom10%_keep", "score", "selected"]
    with pd.option_context("display.max_columns", None, "display.width", 220):
        print(df[cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
