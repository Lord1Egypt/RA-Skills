#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-registry :: 研究布局 vs 疾病负担对标（JCE 2026 方法复用）
本地、零联网（GBD DALYs 由用户自备 CSV 输入）。纯 stdlib 做 OLS；matplotlib 可选出图。

对注册检索到的试验数（按病因）与 GBD 疾病负担（DALYs）做三个指标：
  1) log-log 斜率 β   —— log10(T) 对 log10(D) 的 OLS 斜率（β≈1 资源随负担线性）
  2) 错配比 mismatch  —— 实际试验份额 vs 负担份额的偏离
  3) 零试验病种占比   —— T=0 的病因数及其合计 DALYs 份额

用法：
  python scripts/burden_comparison.py --trials normalized.json --dalys gbd_dalys.csv --out burden_comparison.json
  python scripts/burden_comparison.py --trials normalized.json --dalys gbd_dalys.csv --chart burden_comparison.png
  # trials 也可直接给聚合字典：--trials '{"diarrhea": 0, "breast_cancer": 120, ...}'
"""
import argparse
import csv
import json
import math
import os
import sys


# ---------------------------------------------------------------------------
# 薄 I/O
# ---------------------------------------------------------------------------
def load_trials(path):
    if path.startswith("{") or path.startswith("{"):
        return json.loads(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # 支持 normalized.json（列表）或聚合字典
    if isinstance(data, list):
        agg = {}
        for rec in data:
            key = (rec.get("condition") or rec.get("etiology")
                   or rec.get("disease") or "unknown")
            agg[key] = agg.get(key, 0) + 1
        return agg
    return data


def load_dalys(path):
    dalys = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row.get("etiology") or row.get("cause")
                   or row.get("disease") or list(row.values())[0]).strip()
            try:
                val = float(row.get("dalys") or row.get("DALYs")
                            or row.get("burden") or list(row.values())[1])
            except (TypeError, ValueError):
                continue
            dalys[key] = dalys.get(key, 0.0) + val
    return dalys


# ---------------------------------------------------------------------------
# OLS（log-log），自实现（Gauss-Jordan 解 2x2 正规方程，零依赖）
# ---------------------------------------------------------------------------
def ols_slope(log_x, log_y):
    """返回 (beta, intercept, r2, n)。"""
    n = len(log_x)
    if n < 2:
        return None, None, None, n
    sx = sum(log_x)
    sy = sum(log_y)
    sxx = sum(v * v for v in log_x)
    sxy = sum(a * b for a, b in zip(log_x, log_y))
    syy = sum(v * v for v in log_y)
    # 正规方程: [n, sx; sx, sxx] [b0;b1] = [sy; sxy]
    det = n * sxx - sx * sx
    if abs(det) < 1e-12:
        return None, None, None, n
    b1 = (n * sxy - sx * sy) / det
    b0 = (sy - b1 * sx) / n
    # R^2
    ybar = sy / n
    sst = syy - n * ybar * ybar
    ssr = syy - b0 * sy - b1 * sxy
    r2 = (1 - ssr / sst) if sst != 0 else None
    return b1, b0, r2, n


# ---------------------------------------------------------------------------
# 核心分析
# ---------------------------------------------------------------------------
def analyze(trials, dalys):
    # 交集病因（两边都有的）
    common = [k for k in dalys if k in trials]
    unmatched_trials = {k: v for k, v in trials.items() if k not in dalys}

    rows = []
    for k in common:
        t = max(trials[k], 0)
        d = max(dalys[k], 0)
        rows.append((k, t, d))

    total_t = sum(t for _, t, _ in rows) + sum(unmatched_trials.values())
    total_d = sum(d for _, _, d in rows)

    # log-log 仅用正负担且正试验（log 需 >0）
    lx, ly = [], []
    for k, t, d in rows:
        if d > 0 and t > 0:
            lx.append(math.log10(d))
            ly.append(math.log10(t))
    beta, intercept, r2, n_fit = ols_slope(lx, ly)

    # 错配比：实际试验份额 vs 负担份额
    detail = []
    for k, t, d in rows:
        burden_share = (d / total_d) if total_d else 0.0
        trial_share = (t / total_t) if total_t else 0.0
        mismatch = (trial_share / burden_share) if burden_share > 0 else None
        detail.append({
            "etiology": k, "trials": t, "dalys": d,
            "burden_share": round(burden_share, 6),
            "trial_share": round(trial_share, 6),
            "mismatch_ratio": (round(mismatch, 4) if mismatch is not None else None),
        })
    detail.sort(key=lambda r: r["dalys"], reverse=True)

    # 零试验病种
    zero_trial = [k for k, t, d in rows if t == 0]
    zero_dalys = sum(d for _, t, d in rows if t == 0)
    zero_share = (zero_dalys / total_d) if total_d else 0.0

    # 拟合预测（用于 mismatch vs 预测线）
    if beta is not None and intercept is not None and total_t and total_d:
        pred_total = total_t  # 以实际总试验数为基准，按 β 重分配
        for r in detail:
            if r["dalys"] > 0:
                pred = pred_total * (r["dalys"] ** beta) / sum(
                    dd ** beta for dd in (x["dalys"] for x in detail if x["dalys"] > 0))
                r["predicted_trials_beta"] = round(pred, 2)

    return {
        "n_etiology_common": len(common),
        "n_etiology_unmatched_trials": len(unmatched_trials),
        "unmatched_trials": unmatched_trials,
        "log_log_slope": (round(beta, 4) if beta is not None else None),
        "log_log_intercept": (round(intercept, 4) if intercept is not None else None),
        "log_log_r2": (round(r2, 4) if beta is not None else None),
        "n_points_for_fit": n_fit,
        "total_trials": total_t,
        "total_dalys": total_d,
        "zero_trial_etiology_count": len(zero_trial),
        "zero_trial_dalys_share": round(zero_share, 4),
        "zero_trial_etiology_list": zero_trial,
        "detail": detail,
        "_provenance": "JCE 2026 方法复用（log-log 斜率 / 错配比 / 零试验病种占比）；GBD 数据自备，年份须对齐并在报告中声明；斜率为观察性关联，不证明因果。",
    }


def make_chart(result, out_path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:  # noqa: BLE001
        return f"chart skipped (matplotlib unavailable): {e}"
    pts = [(r["dalys"], r["trials"]) for r in result["detail"]
           if r["dalys"] > 0 and r["trials"] > 0]
    if not pts:
        return "chart skipped (no positive points)"
    xs = [math.log10(d) for d, _ in pts]
    ys = [math.log10(t) for _, t in pts]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(xs, ys, c="steelblue", label="etiology")
    if result["log_log_slope"] is not None:
        b, a = result["log_log_slope"], result["log_log_intercept"]
        xr = [min(xs), max(xs)]
        ax.plot(xr, [a + b * x for x in xr], "r--",
                label=f"fit β={b:.2f}")
        ax.plot(xr, xr, "k:", label="β=1 (burden-linear)")
    ax.set_xlabel("log10(DALYs)")
    ax.set_ylabel("log10(trials)")
    ax.set_title("Trial volume vs disease burden (log-log)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="研究布局 vs 疾病负担对标（JCE 2026）")
    ap.add_argument("--trials", required=True, help="归一化试验 JSON 或聚合字典字符串")
    ap.add_argument("--dalys", required=True, help="GBD DALYs CSV（etiology,dalys）")
    ap.add_argument("--out", help="JSON 输出路径")
    ap.add_argument("--chart", help="PNG 图表输出路径（需 matplotlib）")
    args = ap.parse_args()

    trials = load_trials(args.trials)
    dalys = load_dalys(args.dalys)
    result = analyze(trials, dalys)

    if args.chart:
        msg = make_chart(result, args.chart)
        result["_chart"] = msg

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[burden_comparison] 写出 {args.out}；β={result['log_log_slope']} "
              f"零试验病种={result['zero_trial_etiology_count']} "
              f"(DALYs 份额 {result['zero_trial_dalys_share']})")
    else:
        print(text)


if __name__ == "__main__":
    main()
