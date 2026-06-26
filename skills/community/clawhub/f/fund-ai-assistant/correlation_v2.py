#!/usr/bin/env python3
"""
基金关联热力图 v2 - 小白友好版

计算配置基金的两两相关性，生成热力图，辅助判断组合分散化效果

使用方式：
  python3 correlation_v2.py              # 生成热力图 + 报告
  python3 correlation_v2.py --codes 000001 000003  # 指定基金
  python3 correlation_v2.py --days 90     # 指定历史天数（默认60）

输出：相关性矩阵 + 热力图 → assets/correlation_heatmap_v2.png
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fund_api import fetch_otc_fund_history

TRACKED_FUNDS = {
    "000001": "示例混合型基金A",
    "000002": "示例混合型基金B",
    "000003": "示例债券型基金",
    "000004": "示例黄金ETF联接",
    "000005": "示例养老FOF",
    "000006": "示例白银LOF",
}

def fetch_all_history(days=60):
    """获取所有基金历史数据"""
    all_data = {}
    for code in TRACKED_FUNDS:
        print(f"  {code} ...", end=" ", flush=True)
        hist = fetch_otc_fund_history(code, days=days)
        if hist and len(hist) >= 5:
            hist.sort(key=lambda x: x["date"])
            all_data[code] = hist
            print(f"✓ {len(hist)}条")
        else:
            print(f"✗ 数据不足")
    return all_data

def compute_correlation(all_data):
    """计算相关系数矩阵"""
    import numpy as np
    codes = list(TRACKED_FUNDS.keys())
    names = [TRACKED_FUNDS[c] for c in codes]

    # 计算收益率
    returns = {}
    for code, hist in all_data.items():
        navs = [r["nav"] for r in hist]
        rets = [(navs[i] - navs[i-1]) / navs[i-1] for i in range(1, len(navs))]
        returns[code] = rets

    min_len = min(len(v) for v in returns.values())
    matrix = np.array([[returns[c][i] for c in codes] for i in range(min_len)])
    corr = np.corrcoef(matrix, rowvar=False)
    return corr.tolist(), codes, names

def generate_chart(corr_matrix, codes, names, output_path):
    """生成小白友好版热力图"""
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import matplotlib.patches as mpatches

    # 加载中文字体（多级 fallback）
    zh_font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ]
    zh_font = None
    for fp in zh_font_paths:
        if os.path.exists(fp):
            try:
                zh_font = fm.FontProperties(fname=fp)
                break
            except Exception:
                continue

    plt.rcParams["axes.unicode_minus"] = False
    n = len(codes)

    # 创建图形：深色背景 + 大尺寸
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("#f8f9fa")
    ax.set_facecolor("#f8f9fa")

    # 颜色映射：深绿(-1) → 浅灰(0) → 深红(+1)
    # 改为：小白视角：红色=危险集中，绿色=安全分散
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "risk_map", ["#2d6a4f", "#74c69d", "#f0f0f0", "#f4a460", "#8b0000"]
    )

    im = ax.imshow(corr_matrix, cmap=cmap, vmin=-1, vmax=1, aspect="equal")

    # 标注数值
    for i in range(n):
        for j in range(n):
            val = corr_matrix[i][j]
            # 字体颜色：小相关用深色，大相关用白色
            text_color = "white" if abs(val) > 0.5 else "#333333"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color=text_color, fontsize=12, fontweight="bold",
                    fontproperties=zh_font)

    # X轴标签（上方）
    ax.set_xticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=10.5,
                       fontproperties=zh_font)
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', top=True, labeltop=True, labelbottom=False)

    # Y轴标签（左侧）
    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=10.5, fontproperties=zh_font)

    # 网格线
    ax.set_xticks(np.arange(n) + 0.5, minor=True)
    ax.set_yticks(np.arange(n) + 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)

    # 去除边框
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ===== 图例说明 =====
    legend_y = -0.08
    fig.text(0.5, legend_y, "相关性强弱说明", ha="center", fontsize=12,
             fontweight="bold", fontproperties=zh_font)

    legend_items = [
        ("#8b0000", "🔴 0.8~1.0  高度相关 → 同涨同跌，分散效果弱，风险集中"),
        ("#f4a460", "🟠 0.5~0.8  中度相关 → 走势较同步，注意集中风险"),
        ("#f0f0f0", "⚪ 0.0~0.5  低相关   → 分散效果较好"),
        ("#74c69d", "🟢 -0.5~0  负相关   → 通常此情况较少，可降低组合风险"),
    ]
    for k, (color, text) in enumerate(legend_items):
        fig.text(0.12 + k * 0.22, legend_y - 0.05, f"■ {text}",
                 ha="left", fontsize=8, color=color, fontproperties=zh_font,
                 va="top")

    # 标题
    title = "📊 配置的N只基金关联热力图"
    fig.text(0.5, 1.02, title, ha="center", fontsize=16,
             fontweight="bold", fontproperties=zh_font)
    fig.text(0.5, 0.985, "近60交易日收益率相关性  |  红色越多=资金在集中赌一件事",
              ha="center", fontsize=10, color="#666666", fontproperties=zh_font)

    # ===== 关键发现标注 =====
    # 找出风险最集中的对
    risk_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            val = corr_matrix[i][j]
            if val > 0.7:
                risk_pairs.append((val, names[i], names[j]))

    risk_pairs.sort(reverse=True)

    finding_y = 0.01
    if risk_pairs:
        fig.text(0.5, finding_y,
                 f"⚠️ 风险集中警告：{' / '.join([f'{a}↔{b}({v:.2f})' for v,a,b in risk_pairs[:3]])}",
                 ha="center", fontsize=9, color="#8b0000",
                 fontproperties=zh_font, style="italic")

    plt.tight_layout(rect=[0, 0.08, 1, 0.97])
    plt.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVE] {output_path}")

def main():
    print("⏳ 获取基金历史数据 ...")
    all_data = fetch_all_history(days=60)

    if len(all_data) < 2:
        print("[ERROR] 数据不足")
        sys.exit(1)

    print("🔢 计算相关性 ...")
    corr, codes, names = compute_correlation(all_data)

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "correlation_heatmap_v2.png")

    print("🎨 生成图表 ...")
    generate_chart(corr, codes, names, output_path)

    # 输出文字摘要
    print("\n📋 关键发现：")
    import numpy as np
    corr_arr = np.array(corr)
    n = len(codes)
    high_risk = []
    for i in range(n):
        for j in range(i + 1, n):
            if corr_arr[i, j] > 0.8:
                high_risk.append((corr_arr[i, j], names[i], names[j]))

    high_risk.sort(reverse=True)
    for val, a, b in high_risk:
        print(f"  🔴 {a} ↔ {b}: {val:.2f}")

    print(f"\n图表: {output_path}")

if __name__ == "__main__":
    main()
