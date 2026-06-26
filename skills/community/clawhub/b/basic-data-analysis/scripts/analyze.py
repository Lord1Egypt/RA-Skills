#!/usr/bin/env python3
"""
数据分析核心脚本
支持 CSV / Excel / JSON 输入
输出：图表（PNG）+ 统计摘要（JSON）
用法：python3 analyze.py <数据文件路径> [--output-dir <输出目录>]
"""

import sys
import os
import json
import argparse
import warnings
warnings.filterwarnings("ignore")

# ── 依赖检查 ──────────────────────────────────────────────────────────────────
REQUIRED = ["pandas", "matplotlib", "numpy", "openpyxl"]
missing = []
for pkg in REQUIRED:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)
if missing:
    print(f"[ERROR] 缺少依赖，请先运行: pip3 install {' '.join(missing)}")
    sys.exit(1)

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ── 中文字体配置 ──────────────────────────────────────────────────────────────
def setup_chinese_font():
    """尝试加载系统中文字体，失败则使用英文回退"""
    candidates = [
        "PingFang SC", "Heiti SC", "STHeiti", "SimHei",
        "Microsoft YaHei", "WenQuanYi Micro Hei", "Noto Sans CJK SC"
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for font in candidates:
        if font in available:
            plt.rcParams["font.family"] = font
            plt.rcParams["axes.unicode_minus"] = False
            return font
    plt.rcParams["axes.unicode_minus"] = False
    return None

FONT = setup_chinese_font()

# ── 数据加载 ──────────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        for enc in ["utf-8", "utf-8-sig", "gbk", "gb2312"]:
            try:
                return pd.read_csv(path, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError("CSV 编码无法识别")
    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    elif ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            return pd.DataFrame(raw)
        elif isinstance(raw, dict):
            return pd.DataFrame([raw]) if not any(isinstance(v, list) for v in raw.values()) else pd.DataFrame(raw)
        raise ValueError("JSON 格式不支持")
    else:
        raise ValueError(f"不支持的文件格式: {ext}")

# ── EDA ───────────────────────────────────────────────────────────────────────
def eda(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime"]).columns.tolist()

    summary = {
        "shape": list(df.shape),
        "columns": df.columns.tolist(),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "numeric_columns": numeric_cols,
        "categorical_columns": cat_cols,
        "datetime_columns": datetime_cols,
        "missing_values": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().mean() * 100).round(2).to_dict(),
        "duplicates": int(df.duplicated().sum()),
    }

    if numeric_cols:
        desc = df[numeric_cols].describe().round(4)
        summary["numeric_stats"] = desc.to_dict()

    if cat_cols:
        summary["categorical_stats"] = {
            c: {"unique": int(df[c].nunique()), "top5": df[c].value_counts().head(5).to_dict()}
            for c in cat_cols
        }

    return summary

# ── 数据清洗 ──────────────────────────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    log = []
    original_shape = df.shape

    # 删除全空行/列
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # 删除重复行
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates()
        log.append(f"删除重复行: {dup_count} 行")

    # 数值列填充缺失值（中位数）
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        n_missing = df[col].isnull().sum()
        if n_missing > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            log.append(f"列 '{col}' 缺失值 {n_missing} 个，用中位数 {median_val:.4g} 填充")

    # 字符串列填充缺失值
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        n_missing = df[col].isnull().sum()
        if n_missing > 0:
            df[col] = df[col].fillna("未知")
            log.append(f"列 '{col}' 缺失值 {n_missing} 个，用 '未知' 填充")

    log.append(f"清洗完成: {original_shape} → {df.shape}")
    return df, log

# ── 图表生成 ──────────────────────────────────────────────────────────────────
COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2",
          "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]

def _save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path

def plot_bar(df, col, output_dir, top_n=15):
    """柱状图：数值列分布 or 分类列频次"""
    path = os.path.join(output_dir, f"bar_{col}.png")
    fig, ax = plt.subplots(figsize=(10, 5))

    if df[col].dtype in [np.float64, np.int64, float, int]:
        # 数值列 → 直方图风格柱状图
        counts, bins = np.histogram(df[col].dropna(), bins=min(20, df[col].nunique()))
        ax.bar(bins[:-1], counts, width=np.diff(bins), color=COLORS[0], edgecolor="white", align="edge")
        ax.set_xlabel(col)
        ax.set_ylabel("频次")
        ax.set_title(f"{col} 分布（柱状图）")
        for rect in ax.patches:
            h = rect.get_height()
            if h > 0:
                ax.text(rect.get_x() + rect.get_width() / 2, h + 0.3, str(int(h)),
                        ha="center", va="bottom", fontsize=8)
    else:
        vc = df[col].value_counts().head(top_n)
        bars = ax.bar(range(len(vc)), vc.values, color=COLORS[:len(vc)], edgecolor="white")
        ax.set_xticks(range(len(vc)))
        ax.set_xticklabels(vc.index, rotation=30, ha="right")
        ax.set_ylabel("频次")
        ax.set_title(f"{col} Top{top_n} 频次（柱状图）")
        for bar, val in zip(bars, vc.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    str(val), ha="center", va="bottom", fontsize=9)

    return _save(fig, path)

def plot_pie(df, col, output_dir, top_n=8):
    """饼状图：分类列占比"""
    path = os.path.join(output_dir, f"pie_{col}.png")
    vc = df[col].value_counts().head(top_n)
    if len(vc) < 2:
        return None

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        vc.values, labels=vc.index, autopct="%1.1f%%",
        colors=COLORS[:len(vc)], startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5}
    )
    for at in autotexts:
        at.set_fontsize(9)
    ax.set_title(f"{col} 占比（饼状图）")
    return _save(fig, path)

def plot_line(df, col, output_dir):
    """带数据标记的折线图：数值列按索引趋势"""
    path = os.path.join(output_dir, f"line_{col}.png")
    series = df[col].dropna().reset_index(drop=True)
    if len(series) < 2:
        return None

    # 采样（超过200点时）
    if len(series) > 200:
        step = len(series) // 100
        series = series.iloc[::step]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(series.index, series.values, color=COLORS[0], linewidth=1.8,
            marker="o", markersize=4, markerfacecolor=COLORS[1])

    # 标注最大/最小值
    idx_max = series.idxmax()
    idx_min = series.idxmin()
    ax.annotate(f"最大: {series[idx_max]:.4g}", xy=(idx_max, series[idx_max]),
                xytext=(idx_max, series[idx_max] * 1.02),
                fontsize=8, color="red", ha="center")
    ax.annotate(f"最小: {series[idx_min]:.4g}", xy=(idx_min, series[idx_min]),
                xytext=(idx_min, series[idx_min] * 0.98),
                fontsize=8, color="blue", ha="center")

    ax.set_xlabel("索引")
    ax.set_ylabel(col)
    ax.set_title(f"{col} 趋势（带标记折线图）")
    ax.grid(True, alpha=0.3)
    return _save(fig, path)

def plot_barh(df, col, output_dir, top_n=15):
    """条形图（水平）：分类列频次排名"""
    path = os.path.join(output_dir, f"barh_{col}.png")
    vc = df[col].value_counts().head(top_n).sort_values()
    if len(vc) < 2:
        return None

    fig, ax = plt.subplots(figsize=(10, max(4, len(vc) * 0.45)))
    bars = ax.barh(range(len(vc)), vc.values, color=COLORS[:len(vc)], edgecolor="white")
    ax.set_yticks(range(len(vc)))
    ax.set_yticklabels(vc.index)
    ax.set_xlabel("频次")
    ax.set_title(f"{col} Top{top_n} 排名（条形图）")
    for bar, val in zip(bars, vc.values):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9)
    return _save(fig, path)

def generate_charts(df: pd.DataFrame, output_dir: str) -> list:
    """自动为合适的列生成四类图表"""
    os.makedirs(output_dir, exist_ok=True)
    charts = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # 柱状图：数值列（最多3列）+ 分类列（最多2列）
    for col in numeric_cols[:3]:
        p = plot_bar(df, col, output_dir)
        if p:
            charts.append({"type": "bar", "column": col, "path": p})

    for col in cat_cols[:2]:
        p = plot_bar(df, col, output_dir)
        if p:
            charts.append({"type": "bar", "column": col, "path": p})

    # 饼状图：分类列（最多2列）
    for col in cat_cols[:2]:
        p = plot_pie(df, col, output_dir)
        if p:
            charts.append({"type": "pie", "column": col, "path": p})

    # 折线图：数值列（最多3列）
    for col in numeric_cols[:3]:
        p = plot_line(df, col, output_dir)
        if p:
            charts.append({"type": "line", "column": col, "path": p})

    # 条形图：分类列（最多2列）
    for col in cat_cols[:2]:
        p = plot_barh(df, col, output_dir)
        if p:
            charts.append({"type": "barh", "column": col, "path": p})

    return charts

# ── 主流程 ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="数据分析脚本")
    parser.add_argument("file", help="数据文件路径（CSV/Excel/JSON）")
    parser.add_argument("--output-dir", default="./analysis_output", help="输出目录")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    print(f"[1/5] 加载数据: {args.file}")
    df = load_data(args.file)
    print(f"      → 形状: {df.shape}")

    print("[2/5] EDA 探索性分析...")
    eda_result = eda(df)

    print("[3/5] 数据清洗...")
    df_clean, clean_log = clean_data(df)
    for msg in clean_log:
        print(f"      → {msg}")

    print("[4/5] 生成图表...")
    charts_dir = os.path.join(args.output_dir, "charts")
    charts = generate_charts(df_clean, charts_dir)
    print(f"      → 生成 {len(charts)} 张图表")

    # 保存摘要 JSON
    result = {
        "file": args.file,
        "eda": eda_result,
        "clean_log": clean_log,
        "charts": charts,
    }
    summary_path = os.path.join(args.output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    print(f"[5/5] 完成！摘要已保存至: {summary_path}")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

if __name__ == "__main__":
    main()
