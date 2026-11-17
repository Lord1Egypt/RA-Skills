#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
随机数 time_potential 基线标定
================================

QuantAll 定义 time_potential ∈ [0,1] 为「IC 的时间一致性」：
    越接近 1，因子相关性在时间上越稳定；>0.8 视为高度一致。

本脚本用纯数据模拟三种时间结构，计算
        tp = df.rolling(5).mean().std() / df.std()      (逐列后取均值)
来理解「随机/无结构因子」的 time_potential 基线，作为后续真实因子判读的参照。

直觉：
    - 白噪声：5 日均值把方差稀释为 1/5，std 缩为 1/√5 ≈ 0.447
      → 这是「纯随机因子」的 time_potential 基线
    - 随机游走 / 强自回归：时间惯性大，滚动均值几乎不降方差 → tp 接近 1
结论：真实因子 time_potential 仅 ≈0.45 时，与随机噪声无异，应警惕；
      显著 >0.45（如 0.6~0.8）才表示因子在时间维度上有真实结构。
"""
import os
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(SCRIPT_DIR, "state")


def tp_ratio(df):
    """逐列计算 滚动5日均值std / 原始std，丢弃无效列"""
    num = df.rolling(5).mean().std()
    den = df.std()
    r = num / den
    return r.dropna()


def main():
    np.random.seed(42)
    T, N = 500, 10000  # 500 交易日 × 10000 股票（模拟因子矩阵）

    # 1) 白噪声（无时间结构）—— 随机因子基线
    white = pd.DataFrame(np.random.randn(T, N))
    r_white = tp_ratio(white)

    # 2) 随机游走（强时间惯性）
    rw = pd.DataFrame(np.cumsum(np.random.randn(T, N), axis=0))
    r_rw = tp_ratio(rw)

    # 3) AR(1) ρ=0.8（中等时间结构）
    ar = pd.DataFrame(np.zeros((T, N)))
    for t in range(1, T):
        ar.iloc[t] = 0.8 * ar.iloc[t - 1].values + np.random.randn(N)
    r_ar = tp_ratio(ar)

    theory = 1.0 / np.sqrt(5)
    print(f"白噪声  time_potential: mean={r_white.mean():.4f}  std={r_white.std():.4f}"
          f"   (理论 1/√5={theory:.4f})")
    print(f"随机游走 time_potential: mean={r_rw.mean():.4f}")
    print(f"AR(1)ρ=0.8 time_potential: mean={r_ar.mean():.4f}")

    doc = f"""# 随机数 time_potential 基线标定

模拟公式：`tp = df.rolling(5).mean().std() / df.std()`（逐列后取均值）
数据：500 交易日 × 10000 股票 随机矩阵

| 序列类型 | time_potential(均值) | 时间结构 | 含义 |
|---|---|---|---|
| 白噪声 | {r_white.mean():.4f} | 无 | 理论 1/√5≈{theory:.4f}；**随机因子基线** |
| AR(1) ρ=0.8 | {r_ar.mean():.4f} | 中 | 中等时间惯性 |
| 随机游走 | {r_rw.mean():.4f} | 强 | 滚动均值几乎不降方差，接近 1 |

## 解读（供后续 AI 判读真实因子）
- 白噪声下 5 日均值把方差稀释为 1/5，std 缩为 1/√5≈0.447，这是「纯随机因子」的 time_potential 基线。
- QuantAll 的 time_potential∈[0,1] 衡量「IC 的时间一致性」，越接近 1 越稳定（文档阈值 >0.8 为高度一致）。
- 经验判读：真实因子 time_potential **仅≈0.45** 时，与随机噪声无异，无时间维度价值；
  显著 **>0.45（建议 ≥0.55~0.6）** 才表示因子在时间维度上有真实结构。
- 应用：用 `prune_flow.py init --time-potential-threshold 0.55` 可先把「随机级」因子挡在精选池外。
- 注意：time_potential 与 IR 正交——IR 衡量截面预测稳定性，time_potential 衡量时间序列稳定性，
  二者都应高于各自基线才算「横截面+时间」双稳健。
"""
    out = os.path.join(STATE, "time_potential_baseline.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print("saved", out)


if __name__ == "__main__":
    main()
