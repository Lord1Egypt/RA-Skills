#!/usr/bin/env python3
"""
基金跨品类关联热力图
计算7只基金的相关系数矩阵，生成热力图

输入：7只基金近60个交易日历史净值
输出：相关性热力图 → assets/correlation_heatmap.png
"""

import json
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 导入东方财富API
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fund_api import fetch_otc_fund_history

# ============ 配置（从 config.json 读取，如无则使用示例）============
TRACKED_FUNDS = {
    "000001": "示例混合型基金A",
    "000002": "示例混合型基金B",
    "000003": "示例债券型基金",
    "000004": "示例黄金ETF联接",
    "000005": "示例养老FOF",
    "000006": "示例白银LOF",
}

HISTORY_DAYS = 60  # 历史数据天数

# ============ 数据获取 ============

def fetch_all_history(days: int = 60, retries: int = 3) -> Dict[str, List]:
    """获取所有基金的历史净值（带重试）"""
    all_data = {}
    for code in TRACKED_FUNDS:
        print(f"  获取 {code} ({TRACKED_FUNDS[code]}) ...", end=" ", flush=True)
        history = None
        for attempt in range(retries):
            try:
                history = fetch_otc_fund_history(code, days=days)
                break
            except Exception as e:
                if attempt < retries - 1:
                    import time
                    time.sleep(2)
                    continue
        if history and len(history) > 0:
            # 按日期升序排列
            history.sort(key=lambda x: x["date"])
            all_data[code] = history
            print(f"✓ {len(history)}条")
        else:
            print(f"✗ 失败（已重试{retries}次）")
            all_data[code] = []
    return all_data


def align_by_date(all_data: Dict[str, List]) -> Dict[str, Dict[str, float]]:
    """
    按日期对齐所有基金数据
    返回: { date: { code: nav } }
    """
    # 合并所有日期
    all_dates = set()
    for code, history in all_data.items():
        for record in history:
            all_dates.add(record["date"])

    # 只保留共同交易日（所有基金都有数据的日期）
    date_presence = {}
    for code, history in all_data.items():
        for record in history:
            d = record["date"]
            if d not in date_presence:
                date_presence[d] = set()
            date_presence[d].add(code)

    common_dates = sorted([d for d in dates if len(date_presence[d]) == len(TRACKED_FUNDS)])
    return common_dates


# ============ 相关性计算 ============

def compute_correlation(history_dict: Dict[str, List[dict]]) -> Optional[List[List[float]]]:
    """计算相关系数矩阵"""
    try:
        import numpy as np
    except ImportError:
        print("[ERROR] numpy 未安装，请运行: pip3 install numpy matplotlib")
        return None

    codes = list(TRACKED_FUNDS.keys())
    n = len(codes)

    # 构建收益率矩阵
    returns_data = {}
    for code in codes:
        hist = history_dict.get(code, [])
        if not hist or len(hist) < 5:
            print(f"[WARN] {code} 数据不足，跳过")
            continue
        # 计算日收益率
        navs = [r["nav"] for r in hist]
        rets = []
        for i in range(1, len(navs)):
            if navs[i-1] > 0:
                rets.append((navs[i] - navs[i-1]) / navs[i-1])
            else:
                rets.append(0)
        returns_data[code] = rets

    if len(returns_data) < 2:
        print("[ERROR] 有效基金数据不足2个")
        return None

    # 对齐长度
    min_len = min(len(v) for v in returns_data.values())
    if min_len < 5:
        print(f"[ERROR] 共同交易日不足5天: {min_len}")
        return None
    matrix = np.array([[returns_data[c][i] for c in codes] for i in range(min_len)])

    # Pearson相关系数矩阵
    corr_matrix = np.corrcoef(matrix, rowvar=False)
    return corr_matrix.tolist()


# ============ 热力图生成 ============

def generate_heatmap(corr_matrix: List[List[float]], output_path: str):
    """生成并保存热力图"""
    try:
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
    except ImportError:
        print("[ERROR] matplotlib 未安装")
        return False

    # 设置中文字体（多级 fallback）
    import matplotlib.font_manager as fm
    font_prop = None
    zh_font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ]
    for fp in zh_font_paths:
        if os.path.exists(fp):
            try:
                font_prop = fm.FontProperties(fname=fp)
                plt.rcParams["font.family"] = ["sans-serif"]
                plt.rcParams["axes.unicode_minus"] = False
                break
            except Exception:
                continue

    codes = list(TRACKED_FUNDS.keys())
    names = [TRACKED_FUNDS[c] for c in codes]
    n = len(codes)

    # 简化名称（取基金代码）
    short_names = codes

    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    # 自定义颜色映射：深蓝(-1) → 白(0) → 深红(+1)
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "red_white_blue",
        ["#003f88", "#4a90d9", "#f0f0f0", "#f4a460", "#8b0000"]
    )

    # 绘制热力图
    im = ax.imshow(corr_matrix, cmap=cmap, vmin=-1, vmax=1, aspect="equal")

    # 添加数值标注
    for i in range(n):
        for j in range(n):
            val = corr_matrix[i][j]
            color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color=color, fontsize=11, fontweight="bold")

    # 设置坐标轴
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    if font_prop:
        ax.set_xticklabels(short_names, rotation=45, ha="right", fontsize=10, fontproperties=font_prop)
        ax.set_yticklabels(short_names, fontsize=10, fontproperties=font_prop)
        title_font = font_prop
    else:
        ax.set_xticklabels(short_names, rotation=45, ha="right", fontsize=10)
        ax.set_yticklabels(short_names, fontsize=10)
        title_font = None

    title_text = "Correlation Heatmap (60d)\nRed=Pos | Blue=Neg"
    ax.set_title(title_text, fontsize=12, pad=15, color="white", fontproperties=title_font)

    # 颜色条
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Correlation", fontsize=10, color="white")
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax, "yticklabels"), color="white")

    # 白色网格
    ax.set_xticks(np.arange(n) + 0.5, minor=True)
    ax.set_yticks(np.arange(n) + 0.5, minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.5)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(which="major", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[SAVE] 热力图已保存: {output_path}")
    return True


# ============ 分析报告 ============

def generate_insights(corr_matrix: List[List[float]]) -> str:
    """生成文字分析报告"""
    codes = list(TRACKED_FUNDS.keys())
    names = {c: TRACKED_FUNDS[c] for c in codes}
    n = len(codes)

    lines = ["📊 基金关联分析报告", ""]

    # 找出强正相关和负相关对
    strong_pos = []  # >0.7
    strong_neg = []  # <-0.5
    moderate_pos = []  # 0.4-0.7

    for i in range(n):
        for j in range(i + 1, n):
            val = corr_matrix[i][j]
            pair = f"{names[codes[i]]}({codes[i]}) ↔ {names[codes[j]]}({codes[j]})"
            if val > 0.7:
                strong_pos.append((val, pair))
            elif val < -0.5:
                strong_neg.append((val, pair))
            elif val > 0.4:
                moderate_pos.append((val, pair))

    if strong_pos:
        lines.append("🔴 强正相关（同涨同跌，分散效果弱）:")
        for val, pair in sorted(strong_pos, reverse=True):
            lines.append(f"   {val:.2f}  {pair}")
        lines.append("")

    if strong_neg:
        lines.append("🟢 强负相关（可降低组合风险）:")
        for val, pair in sorted(strong_neg):
            lines.append(f"   {val:.2f}  {pair}")
        lines.append("")

    if moderate_pos:
        lines.append("🟡 中度正相关（关联但不高度同步）:")
        for val, pair in sorted(moderate_pos, reverse=True):
            lines.append(f"   {val:.2f}  {pair}")
        lines.append("")

    if not strong_pos and not strong_neg and not moderate_pos:
        lines.append("✅ 各基金间相关性较低，组合分散效果良好")
        lines.append("")

    # 风险提示
    lines.append("💡 小白提示:")
    lines.append("   相关性 >0.7 的基金可以视为\"同一类\"风险")
    lines.append("   如果多只基金高度相关，说明资金可能在集中赌同一类资产")
    lines.append("   真正的分散化：找相关性低的资产搭配")

    return "\n".join(lines)


# ============ 主流程 ============

def main():
    print(f"⏳ 开始获取 {len(TRACKED_FUNDS)} 只基金历史数据 ...")

    all_data = fetch_all_history(days=HISTORY_DAYS)

    # 检查数据完整性
    valid_codes = [code for code, hist in all_data.items() if len(hist) >= 10]
    print(f"\n有效数据基金: {len(valid_codes)}/{len(TRACKED_FUNDS)}")

    if len(valid_codes) < 2:
        print("[WARN] 少于2只基金有足够数据，改为用全部可用数据分析")
        valid_codes = [code for code, hist in all_data.items() if len(hist) >= 5]
        if len(valid_codes) < 2:
            print("[ERROR] 有效基金数量不足，无法计算相关性")
            sys.exit(1)

    # 计算相关性
    print("🔢 计算相关系数矩阵 ...")
    corr_matrix = compute_correlation(all_data)
    if corr_matrix is None:
        sys.exit(1)

    # 生成热力图
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "correlation_heatmap.png")

    print("🎨 生成热力图 ...")
    success = generate_heatmap(corr_matrix, output_path)

    # 生成文字报告
    report = generate_insights(corr_matrix)
    print("\n" + report)

    if success:
        print(f"\n📁 热力图路径: {output_path}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
