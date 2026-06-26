#!/usr/bin/env python3
"""
数据分析核心脚本 - OpenClaw data-analysis Skill
输入: CSV/Excel 文件路径 + 分析需求
输出: JSON 格式的完整分析结果（统计数据 + ECharts 图表配置 + 洞察点）
"""
import argparse
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print(json.dumps({
        "error": "缺少依赖包，请运行：pip install pandas numpy openpyxl",
        "details": "pandas 和 numpy 是必需依赖"
    }, ensure_ascii=False))
    sys.exit(1)


# ─────────────────────────────────────────────────────────────
# 列类型检测
# ─────────────────────────────────────────────────────────────

def detect_column_types(df: pd.DataFrame) -> dict:
    """智能检测每列的语义类型"""
    types = {}
    for col in df.columns:
        series = df[col].dropna()
        if len(series) == 0:
            types[col] = "empty"
            continue

        if pd.api.types.is_datetime64_any_dtype(df[col]):
            types[col] = "datetime"
        elif pd.api.types.is_bool_dtype(df[col]):
            types[col] = "boolean"
        elif pd.api.types.is_numeric_dtype(df[col]):
            types[col] = "numeric"
        else:
            # 尝试解析为日期
            try:
                sample = series.head(20).astype(str)
                parsed = pd.to_datetime(sample, infer_datetime_format=True, errors="coerce")
                if parsed.notna().mean() > 0.8:
                    types[col] = "datetime"
                    continue
            except Exception:
                pass

            # 低基数 → 分类
            nunique = series.nunique()
            if nunique <= min(20, max(5, int(len(series) * 0.05))):
                types[col] = "categorical"
            else:
                types[col] = "text"

    return types


# ─────────────────────────────────────────────────────────────
# 数据加载
# ─────────────────────────────────────────────────────────────

def load_data(file_path: str) -> pd.DataFrame:
    """加载 CSV 或 Excel 文件"""
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        # 尝试多种编码
        for enc in ["utf-8-sig", "utf-8", "gbk", "gb2312", "latin1"]:
            try:
                return pd.read_csv(file_path, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"无法识别文件编码：{file_path}")

    elif suffix in (".xlsx", ".xls"):
        try:
            return pd.read_excel(file_path, engine="openpyxl" if suffix == ".xlsx" else "xlrd")
        except ImportError:
            raise ImportError("缺少依赖：pip install openpyxl xlrd")

    else:
        raise ValueError(f"不支持的文件格式：{suffix}，支持 .csv / .xlsx / .xls")


# ─────────────────────────────────────────────────────────────
# 统计分析
# ─────────────────────────────────────────────────────────────

def compute_basic_info(df: pd.DataFrame, col_types: dict) -> dict:
    """计算基础信息"""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    columns_info = []
    for col in df.columns:
        col_type = col_types.get(col, "unknown")
        series = df[col].dropna()
        sample_vals = series.head(3).astype(str).tolist()

        info = {
            "name": col,
            "type": col_type,
            "missing": int(missing[col]),
            "missing_pct": float(missing_pct[col]),
            "unique": int(df[col].nunique()),
            "sample": sample_vals,
        }

        if col_type == "numeric":
            info["min"] = round(float(series.min()), 3) if len(series) > 0 else None
            info["max"] = round(float(series.max()), 3) if len(series) > 0 else None
            info["mean"] = round(float(series.mean()), 3) if len(series) > 0 else None

        columns_info.append(info)

    return {
        "rows": len(df),
        "cols": len(df.columns),
        "duplicates": int(df.duplicated().sum()),
        "total_missing": int(missing.sum()),
        "columns": columns_info,
    }


def compute_stats(df: pd.DataFrame, numeric_cols: list) -> dict:
    """计算数值列描述统计"""
    if not numeric_cols:
        return {}

    desc = df[numeric_cols].describe().round(3)
    result = {}
    for col in numeric_cols:
        series = df[col].dropna()
        result[col] = {
            "count": int(desc.loc["count", col]),
            "mean": round(float(desc.loc["mean", col]), 3),
            "std": round(float(desc.loc["std", col]), 3),
            "min": round(float(desc.loc["min", col]), 3),
            "q25": round(float(desc.loc["25%", col]), 3),
            "median": round(float(desc.loc["50%", col]), 3),
            "q75": round(float(desc.loc["75%", col]), 3),
            "max": round(float(desc.loc["max", col]), 3),
            "skew": round(float(series.skew()), 3),
        }
    return result


# ─────────────────────────────────────────────────────────────
# ECharts 图表数据生成
# ─────────────────────────────────────────────────────────────

def build_charts(
    df: pd.DataFrame,
    col_types: dict,
    numeric_cols: list,
    categorical_cols: list,
    datetime_cols: list,
    max_charts: int = 8,
) -> list:
    """生成 ECharts 图表配置数据"""
    charts = []

    # ── 1. 缺失值概览柱状图 ───────────────────────────────────
    missing_data = {
        col: int(df[col].isnull().sum())
        for col in df.columns
        if df[col].isnull().sum() > 0
    }
    if missing_data:
        charts.append({
            "id": "missing_values",
            "type": "bar",
            "title": "缺失值分布",
            "subtitle": "各字段缺失值数量",
            "x": list(missing_data.keys()),
            "y": list(missing_data.values()),
            "color": "#e74c3c",
            "yAxisName": "缺失值数量",
        })

    # ── 2. 数值列分布直方图（最多 4 列）─────────────────────────
    for col in numeric_cols[:4]:
        series = df[col].dropna()
        if len(series) < 5:
            continue
        hist, bin_edges = np.histogram(series, bins=min(25, max(10, int(len(series) ** 0.5))))
        bin_labels = [
            f"{round(bin_edges[i], 2)}~{round(bin_edges[i+1], 2)}"
            for i in range(len(bin_edges) - 1)
        ]
        charts.append({
            "id": f"hist_{col}",
            "type": "histogram",
            "title": f"{col} 数值分布",
            "subtitle": f"均值 {round(float(series.mean()), 2)} | 中位数 {round(float(series.median()), 2)} | 标准差 {round(float(series.std()), 2)}",
            "x": bin_labels,
            "y": hist.tolist(),
            "mean": round(float(series.mean()), 3),
            "median": round(float(series.median()), 3),
            "std": round(float(series.std()), 3),
        })

    # ── 3. 分类列值分布柱状图（最多 3 列）────────────────────────
    for col in categorical_cols[:3]:
        vc = df[col].value_counts().head(12)
        if len(vc) < 2:
            continue
        charts.append({
            "id": f"bar_{col}",
            "type": "bar",
            "title": f"{col} 分布",
            "subtitle": f"Top {len(vc)} 类别",
            "x": [str(v) for v in vc.index.tolist()],
            "y": [int(v) for v in vc.values.tolist()],
            "color": "#3498db",
            "yAxisName": "数量",
        })

    # ── 4. 相关性热力图 ───────────────────────────────────────
    if len(numeric_cols) >= 2:
        corr_cols = numeric_cols[:10]  # 最多 10 列，避免图表过密
        corr_m = df[corr_cols].corr().round(3)
        heatmap_data = []
        for i, row_col in enumerate(corr_m.index):
            for j, col_col in enumerate(corr_m.columns):
                val = float(corr_m.loc[row_col, col_col])
                heatmap_data.append([j, i, round(val, 3)])

        charts.append({
            "id": "correlation_heatmap",
            "type": "heatmap",
            "title": "数值字段相关性热力图",
            "subtitle": "值域 [-1, 1]，绝对值越大相关性越强",
            "x": corr_cols,
            "y": corr_cols,
            "data": heatmap_data,
        })

    # ── 5. 分类 × 数值 分组均值柱状图 ──────────────────────────
    if categorical_cols and numeric_cols and len(charts) < max_charts:
        group_col = categorical_cols[0]
        val_col = numeric_cols[0]
        grouped = df.groupby(group_col)[val_col].mean().round(2)
        if 2 <= len(grouped) <= 15:
            charts.append({
                "id": f"group_{group_col}_{val_col}",
                "type": "grouped_bar",
                "title": f"{val_col} 按 {group_col} 的均值对比",
                "subtitle": f"分组字段：{group_col}",
                "x": [str(v) for v in grouped.index.tolist()],
                "y": [round(float(v), 3) for v in grouped.values.tolist()],
                "xAxisName": group_col,
                "yAxisName": f"{val_col} 均值",
                "color": "#2ecc71",
            })

    # ── 6. 如果有多个数值列 × 同一分类，做多系列柱状图 ───────────
    if categorical_cols and len(numeric_cols) >= 2 and len(charts) < max_charts:
        group_col = categorical_cols[0]
        val_cols = numeric_cols[:3]
        grouped = df.groupby(group_col)[val_cols].mean().round(2)
        if 2 <= len(grouped) <= 12:
            series_data = []
            for vc in val_cols:
                series_data.append({
                    "name": vc,
                    "data": [round(float(v), 3) for v in grouped[vc].values.tolist()],
                })
            charts.append({
                "id": f"multi_bar_{group_col}",
                "type": "multi_bar",
                "title": f"各指标按 {group_col} 分组对比",
                "subtitle": "多指标横向对比",
                "x": [str(v) for v in grouped.index.tolist()],
                "series": series_data,
                "xAxisName": group_col,
            })

    # ── 7. 时间趋势折线图 ─────────────────────────────────────
    if datetime_cols and numeric_cols and len(charts) < max_charts:
        dt_col = datetime_cols[0]
        val_col = numeric_cols[0]
        try:
            df_ts = df[[dt_col, val_col]].copy()
            df_ts[dt_col] = pd.to_datetime(df_ts[dt_col], errors="coerce")
            df_ts = df_ts.dropna().sort_values(dt_col)

            # 按日/周/月聚合，避免点太多
            if len(df_ts) > 200:
                df_ts = df_ts.set_index(dt_col).resample("W")[val_col].mean().reset_index()
                subtitle = "按周聚合"
            elif len(df_ts) > 60:
                df_ts = df_ts.set_index(dt_col).resample("D")[val_col].mean().reset_index()
                subtitle = "按日聚合"
            else:
                subtitle = "原始数据"

            df_ts = df_ts.dropna()
            charts.append({
                "id": f"trend_{dt_col}_{val_col}",
                "type": "line",
                "title": f"{val_col} 时间趋势",
                "subtitle": subtitle,
                "x": df_ts[dt_col].dt.strftime("%Y-%m-%d").tolist(),
                "y": [round(float(v), 3) for v in df_ts[val_col].tolist()],
                "smooth": True,
                "yAxisName": val_col,
            })
        except Exception:
            pass

    # ── 8. 数值占比饼图（分类列 + 数值列 组合）────────────────────
    if categorical_cols and numeric_cols and len(charts) < max_charts:
        group_col = categorical_cols[0]
        val_col = numeric_cols[0]
        grouped = df.groupby(group_col)[val_col].sum()
        if 2 <= len(grouped) <= 10:
            charts.append({
                "id": f"pie_{group_col}_{val_col}",
                "type": "pie",
                "title": f"{val_col} 按 {group_col} 占比",
                "subtitle": f"各 {group_col} 的 {val_col} 总量占比",
                "data": [
                    {"name": str(k), "value": round(float(v), 3)}
                    for k, v in grouped.items()
                ],
            })

    return charts[:max_charts]


# ─────────────────────────────────────────────────────────────
# 规则引擎：自动洞察
# ─────────────────────────────────────────────────────────────

def extract_insights(
    df: pd.DataFrame,
    basic_info: dict,
    numeric_cols: list,
    categorical_cols: list,
) -> list:
    """规则引擎提取关键数据洞察"""
    insights = []

    # 缺失值告警
    high_missing = [
        f"{c['name']}（{c['missing_pct']}%）"
        for c in basic_info["columns"]
        if c["missing_pct"] > 10
    ]
    if high_missing:
        insights.append({
            "level": "warning",
            "icon": "⚠️",
            "text": f"以下字段缺失率超过 10%，建议重点关注：{', '.join(high_missing)}",
        })

    # 重复行告警
    if basic_info["duplicates"] > 0:
        pct = round(basic_info["duplicates"] / basic_info["rows"] * 100, 1)
        insights.append({
            "level": "warning",
            "icon": "🔁",
            "text": f"数据集中存在 {basic_info['duplicates']} 条重复记录（占 {pct}%），建议去重处理",
        })

    # 强相关性发现
    if len(numeric_cols) >= 2:
        corr_m = df[numeric_cols].corr()
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                c1, c2 = numeric_cols[i], numeric_cols[j]
                r = float(corr_m.loc[c1, c2])
                if abs(r) > 0.7:
                    direction = "正相关" if r > 0 else "负相关"
                    insights.append({
                        "level": "info",
                        "icon": "📈",
                        "text": f"{c1} 与 {c2} 存在强{direction}（r={r:.2f}），可能存在业务关联",
                    })

    # 异常值检测（IQR 方法）
    for col in numeric_cols[:5]:
        series = df[col].dropna()
        if len(series) < 10:
            continue
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        outliers = ((series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)).sum()
        if outliers > 0:
            pct = round(float(outliers) / len(series) * 100, 1)
            insights.append({
                "level": "info",
                "icon": "🔍",
                "text": f"{col} 字段存在 {int(outliers)} 个异常值（占 {pct}%），建议核查数据质量",
            })

    # 高偏态分布
    for col in numeric_cols[:4]:
        series = df[col].dropna()
        if len(series) < 20:
            continue
        skew = float(series.skew())
        if abs(skew) > 2:
            direction = "右偏（存在极大值）" if skew > 0 else "左偏（存在极小值）"
            insights.append({
                "level": "info",
                "icon": "📊",
                "text": f"{col} 分布呈 {direction}，偏度 = {skew:.2f}，建议使用中位数而非均值描述集中趋势",
            })

    # 分类列高基数告警
    for col in categorical_cols:
        nunique = df[col].nunique()
        if nunique > 50:
            insights.append({
                "level": "info",
                "icon": "🏷️",
                "text": f"{col} 字段有 {nunique} 个唯一值，基数较高，聚合分析时建议分组或取 Top N",
            })

    # 数据集规模提示
    rows = basic_info["rows"]
    if rows < 100:
        insights.append({
            "level": "warning",
            "icon": "📉",
            "text": f"数据集仅有 {rows} 条记录，样本量较小，统计结论可信度有限，建议收集更多数据",
        })
    elif rows > 100000:
        insights.append({
            "level": "info",
            "icon": "🚀",
            "text": f"数据集共 {rows:,} 条记录，为大规模数据集，当前使用抽样分析，结果具有代表性",
        })

    return insights


# ─────────────────────────────────────────────────────────────
# 主分析流程
# ─────────────────────────────────────────────────────────────

def analyze(file_path: str, requirements: str, max_charts: int = 8) -> dict:
    """完整分析流程，返回供 JS 渲染 HTML 报告的 JSON 数据"""

    # 1. 加载数据
    df = load_data(file_path)

    # 大数据集采样（保留原始行数信息）
    original_rows = len(df)
    if len(df) > 50000:
        df = df.sample(n=50000, random_state=42)

    # 2. 检测列类型
    col_types = detect_column_types(df)
    numeric_cols = [c for c, t in col_types.items() if t == "numeric"]
    categorical_cols = [c for c, t in col_types.items() if t == "categorical"]
    datetime_cols = [c for c, t in col_types.items() if t == "datetime"]

    # 3. 基础信息
    basic_info = compute_basic_info(df, col_types)
    basic_info["original_rows"] = original_rows
    basic_info["sampled"] = original_rows > 50000

    # 4. 描述统计
    stats = compute_stats(df, numeric_cols)

    # 5. 生成图表数据
    charts = build_charts(df, col_types, numeric_cols, categorical_cols, datetime_cols, max_charts)

    # 6. 自动洞察
    insights = extract_insights(df, basic_info, numeric_cols, categorical_cols)

    # 7. 构建摘要（供 AI 理解并补充结论）
    summary = {
        "rows": basic_info["rows"],
        "original_rows": original_rows,
        "cols": basic_info["cols"],
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "datetime_cols": datetime_cols,
        "missing_fields": [
            c["name"] for c in basic_info["columns"] if c["missing_pct"] > 0
        ],
        "key_insights": [item["text"] for item in insights],
        "charts_generated": len(charts),
    }

    return {
        "basic_info": basic_info,
        "stats": stats,
        "charts": charts,
        "insights": insights,
        "summary": summary,
        "requirements": requirements,
        "file_name": Path(file_path).name,
        "col_types": col_types,
    }


# ─────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="数据分析核心脚本")
    parser.add_argument("--file", required=True, help="数据文件路径")
    parser.add_argument("--requirements", required=True, help="分析需求")
    parser.add_argument("--max-charts", type=int, default=8, help="最大图表数量")
    args = parser.parse_args()

    try:
        result = analyze(args.file, args.requirements, args.max_charts)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except Exception as e:
        import traceback
        print(json.dumps({
            "error": str(e),
            "traceback": traceback.format_exc()
        }, ensure_ascii=False))
        sys.exit(1)
