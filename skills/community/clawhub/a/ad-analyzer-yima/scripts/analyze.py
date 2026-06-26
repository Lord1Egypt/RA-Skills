"""
广告数据分析脚本 - ad-analyzer-yima
用法: python3 analyze.py --file report.xlsx --out ./charts
"""
import sys
import os
import argparse
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
COLORS = ["#5c3ab7", "#1d9e75", "#ef9f27", "#e24b4a", "#378add",
          "#d4537e", "#639922", "#888780"]


# ── 读取文件 ──────────────────────────────────────────────────────
def load_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        return pd.read_excel(path, engine="openpyxl")
    if ext == ".xls":
        return pd.read_excel(path, engine="xlrd")
    if ext == ".csv":
        for enc in ("utf-8", "utf-8-sig", "gbk", "gb2312"):
            try:
                return pd.read_csv(path, encoding=enc)
            except Exception:
                continue
    raise ValueError(f"不支持的格式: {ext}")


# ── 自动识别列类型 ────────────────────────────────────────────────
def detect_columns(df):
    date_col = None
    dim_cols = []
    metric_cols = []

    for col in df.columns:
        col_str = col if isinstance(col, str) else str(col)
        series = df[col].copy()

        # 尝试识别日期列
        if date_col is None:
            try:
                converted = pd.to_datetime(series, errors="raise")
                if converted.notna().sum() > len(df) * 0.5:
                    date_col = col
                    df[col] = converted
                    continue
            except Exception:
                pass

        # 尝试识别数值列（处理千分位逗号）
        numeric = pd.to_numeric(
            series.astype(str).str.replace(",", "").str.strip(),
            errors="coerce"
        )
        if numeric.notna().sum() >= len(df) * 0.6:
            df[col] = numeric
            metric_cols.append(col)
        else:
            dim_cols.append(col)

    return date_col, dim_cols, metric_cols


# ── 汇总报告 ──────────────────────────────────────────────────────
def print_summary(df, metric_cols, dim_cols, date_col):
    sep = "=" * 60
    print(f"\n{sep}")
    print("  广告数据分析报告")
    print(sep)
    print(f"总行数: {len(df)}    列数: {len(df.columns)}")
    print(f"日期列: {date_col or '未识别'}")
    print(f"维度列: {', '.join(str(c) for c in dim_cols) or '无'}")
    print(f"指标列: {', '.join(str(c) for c in metric_cols)}")

    print("\n--- 全量指标汇总 ---")
    summary = df[metric_cols].agg(["sum", "mean", "max", "min"]).T
    summary.columns = ["合计", "均值", "最大值", "最小值"]
    print(summary.round(2).to_string())

    if dim_cols:
        main_dim = dim_cols[0]
        print(f"\n--- 按【{main_dim}】分组汇总（{metric_cols[0]} 降序）---")
        grouped = df.groupby(main_dim)[metric_cols].sum()
        grouped = grouped.sort_values(metric_cols[0], ascending=False)
        print(grouped.round(2).to_string())


# ── 异常检测 ──────────────────────────────────────────────────────
def detect_anomalies(df, metric_cols):
    print("\n--- 异常检测 ---")
    found = False
    for col in metric_cols:
        mean_v = df[col].mean()
        std_v = df[col].std()
        if std_v == 0 or pd.isna(std_v):
            continue
        high = df[df[col] > mean_v + 2 * std_v]
        low = df[(df[col] < mean_v - 2 * std_v) & (mean_v > 0)]
        if len(high):
            print(f"⚠️  [{col}] 异常高值 {len(high)} 行 | 均值={mean_v:.2f} 阈值={mean_v+2*std_v:.2f}")
            found = True
        if len(low):
            print(f"⚠️  [{col}] 异常低值 {len(low)} 行 | 均值={mean_v:.2f} 阈值={mean_v-2*std_v:.2f}")
            found = True
    if not found:
        print("✅ 未发现明显异常波动")


# ── 图表生成 ──────────────────────────────────────────────────────
def save_fig(fig, path):
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 {path}")
    return path


def plot_charts(df, metric_cols, dim_cols, date_col, out_dir):
    charts = []
    os.makedirs(out_dir, exist_ok=True)

    # 1. 各指标总量柱状图
    totals = df[metric_cols].sum()
    fig, ax = plt.subplots(figsize=(max(7, len(metric_cols) * 1.4), 5))
    bars = ax.bar(range(len(totals)), totals.values,
                  color=COLORS[:len(metric_cols)], width=0.6)
    ax.set_xticks(range(len(totals)))
    ax.set_xticklabels([str(c) for c in totals.index],
                       rotation=20, ha="right", fontsize=10)
    ax.set_title("各指标总量", fontsize=14, pad=10)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h * 1.01,
                f"{h:,.0f}", ha="center", va="bottom", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    charts.append(save_fig(fig, os.path.join(out_dir, "chart_1_totals.png")))

    # 2. 主维度对比（前3个指标，横向柱状图）
    if dim_cols:
        main_dim = dim_cols[0]
        grouped = (df.groupby(main_dim)[metric_cols].sum()
                     .sort_values(metric_cols[0], ascending=False).head(12))
        show_metrics = metric_cols[:3]
        ncols = len(show_metrics)
        fig, axes = plt.subplots(1, ncols, figsize=(5 * ncols, max(5, len(grouped) * 0.4 + 1)))
        if ncols == 1:
            axes = [axes]
        for i, col in enumerate(show_metrics):
            ax = axes[i]
            vals = grouped[col]
            ax.barh(range(len(vals)), vals.values[::-1] if False else vals.values,
                    color=COLORS[i % len(COLORS)])
            ax.set_yticks(range(len(vals)))
            ax.set_yticklabels([str(x) for x in vals.index], fontsize=9)
            ax.set_title(str(col), fontsize=11)
            ax.grid(axis="x", linestyle="--", alpha=0.3)
        fig.suptitle(f"按【{main_dim}】分组对比", fontsize=13, y=1.02)
        plt.tight_layout()
        charts.append(save_fig(fig, os.path.join(out_dir, "chart_2_dim_compare.png")))

    # 3. 趋势折线图
    if date_col is not None:
        df2 = df.copy()
        df2[date_col] = pd.to_datetime(df2[date_col], errors="coerce")
        df2 = df2.dropna(subset=[date_col])
        daily = df2.groupby(date_col)[metric_cols].sum().sort_index()
        show_metrics = metric_cols[:3]
        nrows = len(show_metrics)
        fig, axes = plt.subplots(nrows, 1, figsize=(12, 3.5 * nrows))
        if nrows == 1:
            axes = [axes]
        for i, col in enumerate(show_metrics):
            ax = axes[i]
            ax.plot(daily.index, daily[col],
                    color=COLORS[i % len(COLORS)], linewidth=2,
                    marker="o", markersize=3)
            ax.fill_between(daily.index, daily[col],
                            alpha=0.08, color=COLORS[i % len(COLORS)])
            ax.set_title(f"{col} 趋势", fontsize=11)
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            plt.setp(ax.get_xticklabels(), rotation=25, ha="right", fontsize=9)
        fig.suptitle("指标趋势分析", fontsize=13, y=1.01)
        plt.tight_layout()
        charts.append(save_fig(fig, os.path.join(out_dir, "chart_3_trend.png")))

    # 4. 相关性热力图
    if len(metric_cols) >= 3:
        corr = df[metric_cols].corr()
        fig, ax = plt.subplots(figsize=(max(6, len(metric_cols)), max(5, len(metric_cols) - 1)))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
                    center=0, ax=ax, linewidths=0.5, annot_kws={"size": 9})
        ax.set_title("指标相关性热力图", fontsize=13)
        plt.tight_layout()
        charts.append(save_fig(fig, os.path.join(out_dir, "chart_4_correlation.png")))

    # 5. 占比饼图
    if dim_cols:
        main_dim = dim_cols[0]
        grouped_pie = df.groupby(main_dim)[metric_cols[0]].sum().sort_values(ascending=False)
        top = grouped_pie.head(8).copy()
        if len(grouped_pie) > 8:
            top["其他"] = grouped_pie.iloc[8:].sum()
        fig, ax = plt.subplots(figsize=(7, 6))
        wedges, texts, autotexts = ax.pie(
            top.values, labels=[str(x) for x in top.index],
            autopct="%1.1f%%",
            colors=(COLORS * 3)[:len(top)],
            startangle=90, pctdistance=0.82
        )
        for t in autotexts:
            t.set_fontsize(9)
        ax.set_title(f"【{main_dim}】{metric_cols[0]} 占比", fontsize=13)
        plt.tight_layout()
        charts.append(save_fig(fig, os.path.join(out_dir, "chart_5_pie.png")))

    return charts


# ── 优化建议 ──────────────────────────────────────────────────────
def print_suggestions(df, metric_cols, dim_cols):
    print("\n--- 优化建议 ---")
    if not dim_cols:
        print("• 建议报表中包含广告计划/广告组等维度列，便于深入分析")
        return
    main_dim = dim_cols[0]
    grouped = df.groupby(main_dim)[metric_cols].sum()
    first = metric_cols[0]
    best = grouped[first].idxmax()
    worst = grouped[first].idxmin()
    best_val = grouped.loc[best, first]
    worst_val = grouped.loc[worst, first]
    print(f"• 【{first}】最高维度: {best}（{best_val:,.2f}）")
    print(f"• 【{first}】最低维度: {worst}（{worst_val:,.2f}）")
    if len(metric_cols) >= 2:
        second = metric_cols[1]
        ratio = grouped[first] / grouped[second].replace(0, float("nan"))
        if ratio.notna().any():
            best_r = ratio.idxmax()
            print(f"• 【{first}/{second}】效率最高: {best_r}（比值={ratio[best_r]:.3f}）")
    print(f"• 建议将预算向【{best}】倾斜，重点优化【{worst}】或考虑暂停")


# ── 主入口 ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="广告数据分析工具")
    parser.add_argument("--file", required=True, help="报表文件路径 (.xlsx/.xls/.csv)")
    parser.add_argument("--out", default="./charts", help="图表输出目录（默认 ./charts）")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    print(f"\n正在读取: {args.file}")
    df = load_file(args.file)
    print(f"读取成功，共 {len(df)} 行 × {len(df.columns)} 列")

    date_col, dim_cols, metric_cols = detect_columns(df)

    if not metric_cols:
        print("❌ 未找到数值列，请确认文件中包含数字数据")
        sys.exit(1)

    print_summary(df, metric_cols, dim_cols, date_col)
    detect_anomalies(df, metric_cols)

    print(f"\n--- 生成图表 → {os.path.abspath(args.out)} ---")
    charts = plot_charts(df, metric_cols, dim_cols, date_col, args.out)

    print_suggestions(df, metric_cols, dim_cols)

    print("\n" + "=" * 60)
    print(f"✅ 分析完成！共生成 {len(charts)} 张图表")
    print(f"   图表目录: {os.path.abspath(args.out)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
