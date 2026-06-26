"""
数据自动分析脚本 - data-auto-analyzer 模式 A（通用数据分析）
生成交互式 HTML 报告（浅色主题 · ECharts 图表 · 可分页/可勾选/可筛选/二级树表格 · 悬浮导航）
用法: python3 analyze.py --file report.xlsx [--out data_report.html]
默认输出到当前目录下的 data-auto-analyzer/ 文件夹
"""
import sys
import os
import argparse
import json
import warnings
import html as html_mod

warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import resolve_output_path


# ── 读取文件 ──────────────────────────────────────────────────────
def load_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        df = pd.read_excel(path, engine="openpyxl")
    elif ext == ".xls":
        df = pd.read_excel(path, engine="xlrd")
    elif ext == ".csv":
        df = None
        for enc in ("utf-8", "utf-8-sig", "gbk", "gb2312"):
            try:
                df = pd.read_csv(path, encoding=enc)
                break
            except Exception:
                continue
        if df is None:
            raise ValueError(f"无法读取 CSV: {path}")
    else:
        raise ValueError(f"不支持的格式: {ext}")
    df = _preprocess(df)
    return _split_summary_rows(df)


def _preprocess(df):
    """通用预处理：删除整行/整列全空的脏数据，并去除列名首尾空格。"""
    before_r, before_c = df.shape
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all").reset_index(drop=True)
    df.columns = [str(c).strip() for c in df.columns]
    dr, dc = before_r - df.shape[0], before_c - df.shape[1]
    if dr or dc:
        print(f"  [预处理] 清除 {dr} 个空行 · {dc} 个空列")
    return df


def _split_summary_rows(df):
    summary_markers = {
        "汇总", "合计", "总计", "小计", "平均", "均值", "求和",
        "total", "sum", "subtotal", "summary", "avg", "average", "mean",
        "总合", "总和",
    }

    def is_summary_row(row):
        for v in row.values:
            if pd.isna(v):
                continue
            s = str(v).strip().lower()
            if s in summary_markers:
                return True
            if s.count(",") >= 5 and len(s) > 20 and " " not in s:
                return True
        return False

    mask = df.apply(is_summary_row, axis=1)
    summary_df = df[mask].copy()
    detail_df = df[~mask].reset_index(drop=True)
    if mask.any():
        print(f"  [自动识别] 检测到 {int(mask.sum())} 行汇总/合计，已提取置顶展示")
    return detail_df, summary_df


# ── 自动识别列类型 ────────────────────────────────────────────────
def _looks_like_date_name(col_name):
    s = str(col_name).lower()
    keywords = ["日期", "时间", "date", "time", "day", "month", "year", "周", "月", "年"]
    return any(k in s for k in keywords)


def _looks_like_id_name(col_name):
    s = str(col_name).lower().strip()
    exact = {"排名", "序号", "编号", "id", "rank", "no", "no.", "#"}
    if s in exact:
        return True
    # 任何以 ID / _ID / 编号 / 序号 / 编码 结尾的列，一律按维度处理（不当数值指标）
    for suf in ("id", "_id", "编号", "序号", "编码", "rank no."):
        if s.endswith(suf):
            return True
    return False


def detect_columns(df):
    date_col = None
    dim_cols = []
    metric_cols = []
    pct_cols = set()

    for col in df.columns:
        series = df[col].copy()
        col_name_str = str(col)

        if _looks_like_id_name(col_name_str):
            dim_cols.append(col)
            continue

        is_already_datetime = pd.api.types.is_datetime64_any_dtype(series)
        if date_col is None and (is_already_datetime or _looks_like_date_name(col_name_str)):
            try:
                if not pd.api.types.is_numeric_dtype(series):
                    converted = pd.to_datetime(series, errors="coerce")
                    if converted.notna().sum() > len(df) * 0.5:
                        date_col = col
                        df[col] = converted
                        continue
                elif is_already_datetime:
                    date_col = col
                    continue
            except Exception:
                pass

        raw_str = series.astype(str)
        had_pct = raw_str.str.contains("%", na=False).any()
        cleaned = raw_str.str.replace(",", "").str.replace("%", "").str.strip()
        numeric = pd.to_numeric(cleaned, errors="coerce")
        if numeric.notna().sum() >= len(df) * 0.6 or pd.api.types.is_numeric_dtype(series):
            df[col] = numeric
            metric_cols.append(col)
            if had_pct:
                pct_cols.add(col)
        else:
            dim_cols.append(col)

    # 兜底：列名没带日期关键词但内容其实是日期（表头错位/不规范）时，按内容识别
    if date_col is None:
        for col in list(dim_cols):
            s = df[col]
            if pd.api.types.is_numeric_dtype(s):
                continue
            parsed = pd.to_datetime(s, errors="coerce")
            if parsed.notna().sum() >= len(df) * 0.6 and parsed.nunique() > 1:
                date_col = col
                df[col] = parsed
                dim_cols.remove(col)
                print(f"  [自动识别] 列「{col}」内容为日期，已作为日期轴处理")
                break

    return date_col, dim_cols, metric_cols, pct_cols


# ── 异常检测 ──────────────────────────────────────────────────────
def detect_anomalies(df, metric_cols):
    anomalies = []
    for col in metric_cols:
        mean_v = df[col].mean()
        std_v = df[col].std()
        if std_v == 0 or pd.isna(std_v):
            continue
        high = df[df[col] > mean_v + 2 * std_v]
        low = df[(df[col] < mean_v - 2 * std_v) & (mean_v > 0)]
        if len(high):
            anomalies.append({"type": "high", "col": str(col), "count": int(len(high)),
                              "mean": round(float(mean_v), 2), "threshold": round(float(mean_v + 2 * std_v), 2)})
        if len(low):
            anomalies.append({"type": "low", "col": str(col), "count": int(len(low)),
                              "mean": round(float(mean_v), 2), "threshold": round(float(mean_v - 2 * std_v), 2)})
    return anomalies


# ── 主维度选择 ────────────────────────────────────────────────────
def _pick_main_dim(df, dim_cols):
    if not dim_cols:
        return None
    candidates = []
    for col in dim_cols:
        if _looks_like_id_name(str(col)):
            continue
        unique_count = df[col].nunique()
        if unique_count <= 1:
            continue
        candidates.append((unique_count, col))
    if not candidates:
        return dim_cols[0]
    candidates.sort(key=lambda x: -x[0])
    return candidates[0][1]


# ── 优化建议 ──────────────────────────────────────────────────────
def get_suggestions(df, metric_cols, dim_cols):
    suggestions = []
    if not dim_cols:
        suggestions.append("建议数据中包含分类/分组维度列（如类别、部门、渠道等），便于深入对比分析")
        return suggestions
    main_dim = _pick_main_dim(df, dim_cols)
    if main_dim is None:
        return suggestions
    grouped = df.groupby(main_dim)[metric_cols].sum()
    first = metric_cols[0]
    best = grouped[first].idxmax()
    worst = grouped[first].idxmin()
    suggestions.append(f"【{first}】最高的 {main_dim}: {best}（{grouped.loc[best, first]:,.2f}）")
    suggestions.append(f"【{first}】最低的 {main_dim}: {worst}（{grouped.loc[worst, first]:,.2f}）")
    if len(metric_cols) >= 2:
        second = metric_cols[1]
        ratio = grouped[first] / grouped[second].replace(0, float("nan"))
        if ratio.notna().any():
            best_r = ratio.idxmax()
            suggestions.append(f"【{first}/{second}】比值最高: {best_r}（{ratio[best_r]:.3f}）")
    suggestions.append(f"建议重点关注【{best}】的成功因素，针对【{worst}】进行分析改进")
    return suggestions


# ── 相关性热力图 ──────────────────────────────────────────────────
def prepare_heatmap(df, metric_cols, max_metrics=12):
    usable = [c for c in metric_cols if df[c].notna().sum() > 1 and df[c].std() not in (0, None)]
    if len(usable) < 3:
        return None
    usable = sorted(usable, key=lambda c: -(df[c].std() if not pd.isna(df[c].std()) else 0))[:max_metrics]
    corr = df[usable].corr()
    labels = [str(c) for c in corr.columns]
    data = []
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = corr.iloc[i, j]
            data.append([i, j, None if pd.isna(v) else round(float(v), 2)])
    return {"labels": labels, "data": data}


# ── 单元格序列化 ──────────────────────────────────────────────────
def _cell(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    try:
        if pd.isna(val):
            return ""
    except (TypeError, ValueError):
        pass
    if isinstance(val, (int, np.integer)):
        return int(val)
    if isinstance(val, (float, np.floating)):
        f = float(val)
        return int(f) if f.is_integer() else round(f, 4)
    return str(val)


def _agg_cells(df, sub, date_col, metric_cols, pct_cols, group_dims=None, date_val=None,
               label_idx=None, label_text=None):
    cells = []
    for c in df.columns:
        if c in metric_cols:
            s = sub[c].dropna()
            if not len(s):
                cells.append("")
            elif c in pct_cols:
                cells.append(_cell(float(s.mean())))
            else:
                cells.append(_cell(float(s.sum())))
        elif c == date_col:
            cells.append(date_val if date_val is not None else "")
        elif group_dims and c in group_dims:
            cells.append(_cell(sub[c].iloc[0]))
        else:
            # 非分组维度：若该组内只有唯一值（如账户ID、客户等恒定字段）则展示，否则留空
            vals = sub[c].dropna().unique()
            cells.append(_cell(vals[0]) if len(vals) == 1 else "")
    if label_idx is not None and label_text is not None:
        cells[label_idx] = label_text
    return cells


def prepare_table_data(df, date_col):
    df_display = df.copy()
    if date_col and date_col in df_display.columns:
        df_display[date_col] = df_display[date_col].astype(str).str[:10]
    columns = [str(c) for c in df_display.columns]
    rows = [[_cell(v) for v in row.values] for _, row in df_display.iterrows()]
    return columns, rows


def build_summary_row(df, columns, date_col, dim_cols, metric_cols, pct_cols, summary_df, main_dim):
    label_idx = columns.index(str(main_dim)) if (main_dim is not None and main_dim in df.columns) else 0
    if summary_df is not None and len(summary_df):
        src = summary_df.iloc[0]
        cells = []
        for c in df.columns:
            cell = _cell(src[c] if c in summary_df.columns else "")
            if isinstance(cell, str) and cell.count(",") >= 5:
                cell = ""
            cells.append(cell)
        cells[label_idx] = "全部数据汇总"
        return cells, True
    if not metric_cols:
        return None, False
    cells = _agg_cells(df, df, date_col, metric_cols, pct_cols, label_idx=label_idx, label_text="全部数据汇总")
    return cells, False


# ── 二级树结构 ────────────────────────────────────────────────────
def build_tree(df, columns, date_col, dim_cols, metric_cols, pct_cols, main_dim):
    if date_col is None or not dim_cols or not metric_cols:
        return {"enabled": False}
    # 分组键：取“会重复出现”的维度（含账户ID 等业务标识），排除每行都唯一的行号类列；
    # 这样每个实体（如每个账户）成一组、其标识列在父行可正常显示，展开即按日期明细。
    group_dims = [c for c in dim_cols if df[c].nunique(dropna=False) < len(df)] or list(dim_cols)

    dim_vals = df[group_dims].astype(str)
    groups, order = {}, []
    for pos in range(len(df)):
        key = tuple(dim_vals.iloc[pos][c] for c in group_dims)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(pos)

    if not groups or max(len(v) for v in groups.values()) <= 1:
        return {"enabled": False}

    date_str = df[date_col].astype(str).str[:10]
    parents = []
    for key in order:
        idxs = groups[key]
        sub = df.iloc[idxs]
        cells = _agg_cells(df, sub, date_col, metric_cols, pct_cols, group_dims=group_dims)
        child_idx = sorted(idxs, key=lambda p: date_str.iloc[p])
        parents.append({"cells": cells, "child_idx": [int(p) for p in child_idx]})

    label_idx = columns.index(str(main_dim)) if (main_dim is not None and main_dim in df.columns) else 0
    grand_cells = _agg_cells(df, df, date_col, metric_cols, pct_cols, label_idx=label_idx, label_text="全部数据汇总")
    grand_children = []
    for d in sorted(date_str.unique()):
        sub = df[date_str == d]
        grand_children.append(_agg_cells(df, sub, date_col, metric_cols, pct_cols, date_val=d))

    return {
        "enabled": True,
        "parents": parents,
        "grand": {"cells": grand_cells, "children": grand_children},
        "group_dim_idx": [columns.index(str(c)) for c in group_dims],
    }


# ── 汇总指标卡片 ──────────────────────────────────────────────────
def get_summary_stats(df, metric_cols, pct_cols):
    stats = []
    for col in metric_cols:
        s = df[col].dropna()
        if not len(s):
            continue
        stats.append({"name": str(col), "is_pct": col in pct_cols,
                      "sum": round(float(s.sum()), 2), "mean": round(float(s.mean()), 2),
                      "max": round(float(s.max()), 2), "min": round(float(s.min()), 2)})
    return stats


# ── 生成 HTML 报告 ────────────────────────────────────────────────
def generate_html():
    return HTML_TEMPLATE


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>数据分析报告</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.5.0/echarts.min.js"></script>
<style>
  :root {
    --bg-page:#f3f5f9; --bg-card:#ffffff; --bg-soft:#f7f9fc; --bg-hover:#eef3ff;
    --border:#e9ecf2; --border-soft:#f0f2f6;
    --text-primary:#1d2433; --text-secondary:#5a6478; --text-dim:#9aa3b2;
    --accent-blue:#3b6cff; --accent-green:#10b981; --accent-orange:#f59e0b;
    --accent-red:#ef4444; --accent-purple:#7c5cff; --accent-cyan:#0ea5b7;
    --shadow:0 1px 2px rgba(20,28,48,.04), 0 8px 24px rgba(20,28,48,.06);
    --shadow-sm:0 1px 2px rgba(20,28,48,.05);
    --gradient-1:linear-gradient(135deg,#3b6cff 0%,#7c5cff 100%);
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
    background:var(--bg-page); color:var(--text-primary); line-height:1.6; min-height:100vh; -webkit-font-smoothing:antialiased; }
  a { color:inherit; }
  .container { max-width:1320px; margin:0 auto; padding:24px 28px 60px; }

  .header { text-align:center; padding:46px 24px 36px; }
  .header h1 { font-size:2rem; font-weight:800; background:var(--gradient-1); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:8px; letter-spacing:-0.02em; }
  .header .subtitle { color:var(--text-secondary); font-size:0.92rem; }

  /* 悬浮导航 */
  .sidenav { position:fixed; left:18px; top:50%; transform:translateY(-50%); z-index:80; display:flex; flex-direction:column; gap:4px;
    background:var(--bg-card); border:1px solid var(--border); border-radius:14px; padding:10px 8px; box-shadow:var(--shadow); }
  .sidenav a { display:flex; align-items:center; gap:8px; font-size:0.82rem; color:var(--text-secondary); text-decoration:none; padding:7px 14px; border-radius:9px; white-space:nowrap; cursor:pointer; transition:.18s; }
  .sidenav a .dot { width:6px; height:6px; border-radius:50%; background:var(--border); transition:.18s; }
  .sidenav a:hover { background:var(--bg-soft); color:var(--text-primary); }
  .sidenav a.active { background:var(--bg-hover); color:var(--accent-blue); font-weight:600; }
  .sidenav a.active .dot { background:var(--accent-blue); }
  @media (max-width:1180px){ .sidenav { display:none; } }

  /* 折叠区块 */
  .sec { margin-bottom:26px; scroll-margin-top:20px; }
  .sec-head { display:flex; align-items:center; gap:10px; margin-bottom:16px; user-select:none; }
  .sec-head .bar { width:4px; height:18px; border-radius:3px; background:var(--gradient-1); }
  .sec-head .sec-title { font-size:1.15rem; font-weight:700; }
  .sec-head .chev { margin-left:auto; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; width:42px; height:42px; border-radius:10px; border:1px solid var(--border); background:var(--bg-card); box-shadow:var(--shadow-sm); transition:transform .3s, background .2s, color .2s; color:var(--text-secondary); font-size:1.5rem; line-height:1; }
  .sec-head .chev:hover { background:var(--bg-hover); color:var(--accent-blue); border-color:var(--accent-blue); }
  .sec.sec-collapsed .chev { transform:rotate(-90deg); }
  .sec-body { display:grid; grid-template-rows:1fr; transition:grid-template-rows .35s ease; }
  .sec.sec-collapsed .sec-body { grid-template-rows:0fr; }
  .sec-inner { overflow:hidden; min-height:0; }

  .card { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; box-shadow:var(--shadow); }

  .overview-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; }
  .ov-card { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; padding:20px; box-shadow:var(--shadow); transition:.2s; }
  .ov-card:hover { transform:translateY(-2px); box-shadow:0 10px 28px rgba(20,28,48,.10); }
  .ov-card .label { font-size:0.78rem; color:var(--text-dim); letter-spacing:.04em; margin-bottom:6px; }
  .ov-card .value { font-size:1.5rem; font-weight:800; word-break:break-all; }
  .ov-card .sub { font-size:0.78rem; color:var(--text-dim); margin-top:4px; }

  .stats-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:14px; }
  .stat-card { background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:18px; box-shadow:var(--shadow-sm); }
  .stat-card.hidden { display:none; }
  .stat-card .stat-name { font-size:0.85rem; font-weight:700; color:var(--accent-blue); margin-bottom:12px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .stat-card .stat-row { display:flex; justify-content:space-between; padding:4px 0; font-size:0.82rem; }
  .stat-card .stat-row .lbl { color:var(--text-secondary); }
  .stat-card .stat-row .val { color:var(--text-primary); font-weight:600; font-variant-numeric:tabular-nums; }

  .info-box { background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:15px 18px; margin-bottom:12px; font-size:0.88rem; box-shadow:var(--shadow-sm); }
  .info-box.hidden { display:none; }
  .info-box.warn { border-left:4px solid var(--accent-orange); }
  .info-box.ok { border-left:4px solid var(--accent-green); }
  .info-box.tip { border-left:4px solid var(--accent-purple); }
  .more-btn { background:var(--bg-card); border:1px dashed var(--border); color:var(--accent-blue); padding:8px 16px; border-radius:10px; cursor:pointer; font-size:0.82rem; margin-top:6px; }
  .more-btn:hover { background:var(--bg-hover); border-color:var(--accent-blue); }

  /* 表格 */
  .table-wrap { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; box-shadow:var(--shadow); }
  .table-toolbar { display:flex; justify-content:space-between; align-items:center; padding:14px 18px; border-bottom:1px solid var(--border); flex-wrap:wrap; gap:10px; }
  .toolbar-left { display:flex; align-items:center; gap:10px; flex-wrap:wrap; position:relative; }
  .search-box { background:var(--bg-soft); border:1px solid var(--border); border-radius:9px; padding:8px 14px; color:var(--text-primary); font-size:0.85rem; width:230px; outline:none; transition:.2s; }
  .search-box:focus { border-color:var(--accent-blue); background:#fff; }
  .btn { background:var(--bg-card); border:1px solid var(--border); color:var(--text-secondary); padding:8px 14px; border-radius:9px; cursor:pointer; font-size:0.82rem; transition:.2s; white-space:nowrap; }
  .btn:hover { border-color:var(--accent-blue); color:var(--accent-blue); }
  .btn.primary { background:var(--accent-blue); border-color:var(--accent-blue); color:#fff; }
  .btn.on { border-color:var(--accent-blue); color:var(--accent-blue); background:var(--bg-hover); }
  .page-info { color:var(--text-secondary); font-size:0.82rem; }
  .sel-info { color:var(--accent-cyan); font-size:0.82rem; font-weight:600; }

  .filter-pop { position:absolute; top:46px; left:0; z-index:60; width:440px; max-height:82vh; background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:16px; box-shadow:0 16px 48px rgba(20,28,48,.18); display:none; }
  .filter-pop.open { display:flex; flex-direction:column; }
  .filter-pop h4 { font-size:0.85rem; margin-bottom:10px; flex:0 0 auto; }
  #filter-rows { flex:1 1 auto; overflow-y:auto; max-height:46vh; padding-right:2px; }
  .filter-row { display:flex; gap:8px; margin-bottom:8px; align-items:center; }
  .filter-row .op, .filter-row .num { background:var(--bg-soft); border:1px solid var(--border); color:var(--text-primary); border-radius:8px; padding:7px 8px; font-size:0.8rem; outline:none; }
  .filter-row .op { width:74px; } .filter-row .num { width:96px; }
  .filter-row .del { color:var(--accent-red); cursor:pointer; padding:0 6px; font-size:1.1rem; }
  .filter-actions { display:flex; gap:8px; margin-top:10px; flex:0 0 auto; }

  .table-container { overflow-x:auto; }
  .data-table { width:100%; border-collapse:collapse; font-size:0.82rem; }
  .data-table th { background:var(--bg-soft); color:var(--text-secondary); font-weight:700; font-size:0.74rem; padding:11px 14px; text-align:left; white-space:nowrap; cursor:pointer; user-select:none; border-bottom:1px solid var(--border); position:sticky; top:0; z-index:2; }
  .data-table th.nosort { cursor:default; }
  .data-table th:hover:not(.nosort) { color:var(--accent-blue); }
  .data-table th .sort-icon { margin-left:4px; opacity:.4; }
  .data-table th.sorted .sort-icon { opacity:1; color:var(--accent-blue); }
  .data-table td { padding:9px 14px; border-bottom:1px solid var(--border-soft); white-space:nowrap; max-width:240px; overflow:hidden; text-overflow:ellipsis; color:var(--text-primary); }
  .data-table tbody tr.parent-row:hover td { background:var(--bg-hover); }
  .data-table td.num, .data-table th.num { text-align:right; font-variant-numeric:tabular-nums; }
  .data-table .chk-col { width:42px; text-align:center; }
  .data-table input[type=checkbox] { cursor:pointer; width:15px; height:15px; accent-color:var(--accent-blue); }
  tr.summary-row td { background:#fff7e8 !important; color:#92660a; font-weight:700; border-bottom:2px solid var(--accent-orange); }
  tr.child-row td { background:var(--bg-soft); color:var(--text-secondary); font-size:0.78rem; }
  tr.child-row td.child-first { padding-left:30px; color:var(--accent-cyan); font-weight:600; }
  .tchev { display:inline-block; width:16px; cursor:pointer; color:var(--text-dim); transition:transform .2s; margin-right:4px; }
  .tchev.open { transform:rotate(90deg); color:var(--accent-blue); }

  .pagination { display:flex; justify-content:center; align-items:center; gap:6px; padding:16px; border-top:1px solid var(--border); }
  .pagination button { background:var(--bg-card); border:1px solid var(--border); color:var(--text-secondary); padding:6px 12px; border-radius:8px; cursor:pointer; font-size:0.82rem; transition:.2s; }
  .pagination button:hover { border-color:var(--accent-blue); color:var(--accent-blue); }
  .pagination button.active { background:var(--accent-blue); border-color:var(--accent-blue); color:#fff; }
  .pagination button:disabled { opacity:.4; cursor:not-allowed; }

  .chart-card { background:var(--bg-card); border:1px solid var(--border); border-radius:14px; padding:18px 20px; margin-bottom:20px; box-shadow:var(--shadow); }
  .chart-head { display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:10px; }
  .chart-head .ctitle { font-size:1rem; font-weight:700; margin-right:auto; }
  .chart-head .clabel { color:var(--text-dim); font-size:0.78rem; }
  .seg { display:inline-flex; border:1px solid var(--border); border-radius:9px; overflow:hidden; }
  .seg button { background:var(--bg-card); border:none; color:var(--text-secondary); padding:6px 13px; font-size:0.78rem; cursor:pointer; }
  .seg button.on { background:var(--accent-blue); color:#fff; }
  .chart-box { width:100%; height:470px; }
  .chart-empty { display:flex; align-items:center; justify-content:center; height:470px; color:var(--text-dim); font-size:0.9rem; }

  /* 自定义下拉（带搜索）*/
  .ms { position:relative; display:inline-block; }
  .ms-btn { background:var(--bg-card); border:1px solid var(--border); color:var(--text-primary); border-radius:9px; padding:6px 12px; font-size:0.78rem; cursor:pointer; max-width:300px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .ms-btn:hover { border-color:var(--accent-blue); }
  .ms-pop { display:none; position:absolute; top:38px; left:0; z-index:70; min-width:220px; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:8px; box-shadow:0 16px 48px rgba(20,28,48,.18); }
  .ms-pop.open { display:block; }
  .ms-search { width:100%; box-sizing:border-box; background:var(--bg-soft); border:1px solid var(--border); border-radius:7px; padding:6px 10px; font-size:0.78rem; outline:none; margin-bottom:6px; }
  .ms-list { max-height:260px; overflow:auto; }
  .ms-item { display:flex; align-items:center; gap:8px; padding:6px 8px; border-radius:7px; font-size:0.8rem; cursor:pointer; }
  .ms-item:hover { background:var(--bg-hover); }
  .ms-item.sel { color:var(--accent-blue); font-weight:600; background:var(--bg-soft); }
  .ms-item.dis { opacity:.35; cursor:not-allowed; }
  .ms-item input { accent-color:var(--accent-blue); }
  .ms-empty { color:var(--text-dim); font-size:0.78rem; padding:8px; text-align:center; }

  .footer { text-align:center; padding:30px; color:var(--text-dim); font-size:0.78rem; }
  @media (max-width:768px){ .container{padding:16px 14px 50px;} .header h1{font-size:1.5rem;} .overview-grid{grid-template-columns:repeat(2,1fr);} .filter-pop{width:92vw;} }
</style>
</head>
<body>

<nav class="sidenav" id="sidenav"></nav>

<div class="header">
  <h1>数据分析报告</h1>
  <p class="subtitle">{{FILE_NAME}} · 共 {{TOTAL_ROWS}} 行 × {{TOTAL_COLS}} 列</p>
</div>

<div class="container">

  <div class="sec" id="sec-overview"><div class="sec-head"><span class="bar"></span><span class="sec-title">数据概览</span><span class="chev" onclick="toggleSec(this)" title="展开/收起">▾</span></div>
    <div class="sec-body"><div class="sec-inner"><div class="overview-grid" id="overview-grid"></div></div></div></div>

  <div class="sec" id="sec-stats"><div class="sec-head"><span class="bar"></span><span class="sec-title">核心指标汇总</span><span class="chev" onclick="toggleSec(this)" title="展开/收起">▾</span></div>
    <div class="sec-body"><div class="sec-inner"><div class="stats-grid" id="stats-grid"></div><button class="more-btn" id="stats-more" style="display:none"></button></div></div></div>

  <div class="sec" id="sec-anomaly"><div class="sec-head"><span class="bar"></span><span class="sec-title">异常检测</span><span class="chev" onclick="toggleSec(this)" title="展开/收起">▾</span></div>
    <div class="sec-body"><div class="sec-inner"><div id="anomaly-box"></div><button class="more-btn" id="anomaly-more" style="display:none"></button></div></div></div>

  <div class="sec" id="sec-suggest"><div class="sec-head"><span class="bar"></span><span class="sec-title">优化建议</span><span class="chev" onclick="toggleSec(this)" title="展开/收起">▾</span></div>
    <div class="sec-body"><div class="sec-inner"><div id="suggestion-box"></div></div></div></div>

  <div class="sec" id="sec-table"><div class="sec-head"><span class="bar"></span><span class="sec-title">明细数据</span><span class="chev" onclick="toggleSec(this)" title="展开/收起">▾</span></div>
    <div class="sec-body"><div class="sec-inner">
      <div class="table-wrap">
        <div class="table-toolbar">
          <div class="toolbar-left">
            <input class="search-box" id="search-input" placeholder="搜索维度列..." oninput="onSearch()">
            <button class="btn" id="filter-btn" onclick="toggleFilterPop(event)">更多筛选 ▾</button>
            <button class="btn" id="cols-btn" onclick="toggleColsPop(event)">显示列 ▾</button>
            <span class="sel-info" id="sel-info"></span>
            <div class="filter-pop" id="filter-pop">
              <h4>指标筛选（多组之间为“且”关系）</h4>
              <div id="filter-rows"></div>
              <div class="filter-actions">
                <button class="btn" onclick="addFilterRow()">+ 添加条件</button>
                <button class="btn primary" onclick="applyFilters()">应用</button>
                <button class="btn" onclick="resetFilters()">重置</button>
              </div>
            </div>
            <div class="filter-pop" id="cols-pop"><h4>选择要显示的维度列</h4><div id="cols-list" style="max-height:50vh;overflow:auto"></div></div>
          </div>
          <span class="page-info" id="page-info"></span>
        </div>
        <div class="table-container">
          <table class="data-table" id="data-table"><thead id="table-head"></thead><tbody id="table-body"></tbody></table>
        </div>
        <div class="pagination" id="pagination"></div>
      </div>
    </div></div></div>

  <div class="sec" id="sec-charts"><div class="sec-head"><span class="bar"></span><span class="sec-title">数据可视化</span><span class="chev" onclick="toggleSec(this)" title="展开/收起">▾</span></div>
    <div class="sec-body"><div class="sec-inner">
      <p style="color:var(--text-dim);font-size:0.82rem;margin:0 0 16px;">默认展示「全部数据汇总」的全量聚合；勾选某些行可聚焦对比（按日期勾选多组时每组单独成线/柱）；勾选「汇总」行则仅展示汇总数据。</p>
      <div id="chart-area"></div>
    </div></div></div>

</div>

<div class="footer">Generated by data-auto-analyzer · 数据本地处理</div>

<script>
const REPORT = {{REPORT_JSON}};

const COLS = REPORT.columns;
const META = REPORT.col_meta;
const METRICS = REPORT.metric_cols;
const DIM_IDX = REPORT.dim_idx;
const METRIC_IDX = REPORT.metric_idx;
const DATE_IDX = REPORT.date_col_index;
const MAIN_DIM_IDX = REPORT.main_dim_index;
const HAS_DATE = DATE_IDX >= 0;
const TREE = REPORT.tree || { enabled:false };
const TREE_ON = TREE.enabled;
const PIE_DIMS = REPORT.pie_dim_options || [];
const COLORS = ['#3b6cff','#10b981','#f59e0b','#ef4444','#7c5cff','#0ea5b7','#ec4899','#06b6d4','#84cc16','#f97316','#6366f1','#14b8a6'];
const EC = { text:'#5a6478', sub:'#9aa3b2', axis:'#e3e7ef', split:'#eef1f6', tipBg:'#ffffff', tipText:'#1d2433', tipBorder:'#e9ecf2' };

const PAGE_SIZE = 10;
let currentPage = 1, sortCol = -1, sortAsc = true;
let searchQ = '';
let metricFilters = [], filterRows = [];
const selected = new Set();

const allRows = REPORT.rows.map((cells,i)=>({ rid:i, cells }));
const parents = TREE_ON ? TREE.parents.map((p,i)=>({ gid:i, cells:p.cells, childIdx:p.child_idx, expanded:false })) : null;
const HAS_GRAND = METRICS.length > 0;          // 顶部“汇总”行（指标随筛选实时聚合）
const PCT_SET = new Set(REPORT.pct_idx || []); // 百分比指标：聚合用均值
let grandExpanded = false;
let hiddenCols = new Set(REPORT.constant_dim_idx || []);  // 默认隐藏“全表恒定”的重复维度列
function visCols(){ const r=[]; for(let i=0;i<COLS.length;i++) if(!hiddenCols.has(i)) r.push(i); return r; }
const ALL_DATES = HAS_DATE ? [...new Set(allRows.map(r=>r.cells[DATE_IDX]).filter(x=>x!==''&&x!=null))].sort() : [];
// 系列标签：把该组的全部分组维度用 _ 拼接（保证唯一可区分）；图例截断+tooltip 换行避免过长遮挡
const baseRows = () => TREE_ON ? parents : allRows;
const gidOf = r => TREE_ON ? r.gid : r.rid;
let viewRows = baseRows().slice();

function colIndex(name){ return COLS.indexOf(name); }
function toNum(v){ if(typeof v==='number')return v; if(v==null||v==='')return 0; const n=parseFloat(String(v).replace(/[,%\s]/g,'')); return isNaN(n)?0:n; }
function isNumericCell(v){ if(typeof v==='number')return true; if(v==null||v==='')return false; return /^-?[\d.,%\s]+$/.test(String(v)); }
function round2(v){ return Math.round(v*100)/100; }
function fmt(n){ if(n===''||n==null)return '-'; if(typeof n==='string')return n;
  if(Math.abs(n)>=1e8)return (n/1e8).toFixed(2)+'亿'; if(Math.abs(n)>=1e4)return (n/1e4).toFixed(2)+'万';
  if(Number.isInteger(n))return n.toLocaleString(); return n.toLocaleString(undefined,{maximumFractionDigits:2}); }
function esc(v){ return String(v).replace(/"/g,'&quot;'); }

/* ===== 悬浮导航 ===== */
const NAV=[['sec-overview','概览'],['sec-stats','指标'],['sec-anomaly','异常'],['sec-suggest','建议'],['sec-table','明细'],['sec-charts','图表']];
function setActiveNav(id){ document.querySelectorAll('.sidenav a').forEach(a=>a.classList.toggle('active',a.dataset.target===id)); }
function updateActiveNav(){ const off=140; let cur=NAV[0][0];
  for(const [id] of NAV){ const el=document.getElementById(id); if(el && el.getBoundingClientRect().top<=off) cur=id; }
  if(window.innerHeight+window.scrollY >= document.documentElement.scrollHeight-4) cur=NAV[NAV.length-1][0];
  setActiveNav(cur); }
function buildNav(){
  document.getElementById('sidenav').innerHTML = NAV.map(([id,t])=>`<a data-target="${id}"><span class="dot"></span>${t}</a>`).join('');
  document.querySelectorAll('.sidenav a').forEach(a=>a.onclick=()=>{ const el=document.getElementById(a.dataset.target);
    el.classList.remove('sec-collapsed'); setActiveNav(a.dataset.target); el.scrollIntoView({behavior:'smooth',block:'start'}); });
  window.addEventListener('scroll', updateActiveNav, {passive:true}); updateActiveNav();
}
function toggleSec(head){ const sec=head.closest('.sec'); sec.classList.toggle('sec-collapsed');
  if(sec.querySelector('#chart-area') && !sec.classList.contains('sec-collapsed')) setTimeout(resizeAllCharts,360); }

/* ===== 概览 / 汇总 / 异常 / 建议 ===== */
function renderOverview(){
  const cards=[
    { label:'数据行数', value:REPORT.total_rows.toLocaleString(), sub:'条明细记录' },
    { label:'数据列数', value:REPORT.total_cols, sub:`维度 ${REPORT.dim_cols.length} · 指标 ${REPORT.metric_cols.length}` },
    { label:'日期列', value:REPORT.date_col||'未识别', sub:REPORT.date_range||'截面数据' },
    { label:'主维度', value:(MAIN_DIM_IDX>=0?COLS[MAIN_DIM_IDX]:'无'), sub:TREE_ON?'二级树分组':'图表分组维度' },
  ];
  document.getElementById('overview-grid').innerHTML = cards.map(c=>
    `<div class="ov-card"><div class="label">${c.label}</div><div class="value">${c.value}</div><div class="sub">${c.sub}</div></div>`).join('');
}
function setupMore(gridId, btnId, total, sel){
  const btn=document.getElementById(btnId);
  if(total<=4){ btn.style.display='none'; return; }
  btn.style.display='inline-block'; btn.dataset.open='0'; btn.textContent=`展开更多 (${total-4}) ▾`;
  btn.onclick=()=>{ const open=btn.dataset.open==='1';
    document.querySelectorAll(`#${gridId} ${sel}`).forEach((e,i)=>{ if(i>=4) e.classList.toggle('hidden',open); });
    btn.dataset.open=open?'0':'1'; btn.textContent=open?`展开更多 (${total-4}) ▾`:'收起 ▴'; };
}
function renderStats(){
  document.getElementById('stats-grid').innerHTML = REPORT.summary_stats.map((s,i)=>`
    <div class="stat-card ${i>=4?'hidden':''}"><div class="stat-name">${s.name}${s.is_pct?' <span style="color:var(--text-dim)">(%)</span>':''}</div>
      <div class="stat-row"><span class="lbl">${s.is_pct?'均值':'合计'}</span><span class="val">${fmt(s.is_pct?s.mean:s.sum)}</span></div>
      <div class="stat-row"><span class="lbl">均值</span><span class="val">${fmt(s.mean)}</span></div>
      <div class="stat-row"><span class="lbl">最大值</span><span class="val">${fmt(s.max)}</span></div>
      <div class="stat-row"><span class="lbl">最小值</span><span class="val">${fmt(s.min)}</span></div></div>`).join('');
  setupMore('stats-grid','stats-more',REPORT.summary_stats.length,'.stat-card');
}
function renderAnomalies(){
  const box=document.getElementById('anomaly-box');
  if(!REPORT.anomalies.length){ box.innerHTML='<div class="info-box ok">✅ 未发现明显异常波动，各指标在正常范围内</div>'; document.getElementById('anomaly-more').style.display='none'; return; }
  box.innerHTML = REPORT.anomalies.map((a,i)=>{ const icon=a.type==='high'?'📈':'📉', label=a.type==='high'?'异常高值':'异常低值';
    return `<div class="info-box warn ${i>=4?'hidden':''}">${icon} 【${a.col}】${label} ${a.count} 行 · 均值 ${fmt(a.mean)} · 阈值 ${fmt(a.threshold)}</div>`; }).join('');
  setupMore('anomaly-box','anomaly-more',REPORT.anomalies.length,'.info-box');
}
function renderSuggestions(){ document.getElementById('suggestion-box').innerHTML = REPORT.suggestions.map(s=>`<div class="info-box tip">💡 ${s}</div>`).join(''); }

/* ===== 表格 ===== */
function renderTableHead(){
  let th='<tr><th class="chk-col nosort"><input type="checkbox" id="chk-all" onclick="toggleAll(this)"></th>';
  th += visCols().map(i=>`<th class="${META[i].type==='metric'?'num':''}" onclick="sortTable(${i})" data-col="${i}"><span>${COLS[i]}</span><span class="sort-icon">↕</span></th>`).join('')+'</tr>';
  document.getElementById('table-head').innerHTML=th;
}
function topRowHtml(r){
  const gid=gidOf(r), sel=selected.has(gid), expanded=!!r.expanded;
  const hasCh = TREE_ON && r.childIdx && r.childIdx.length>0;
  const vis=visCols();
  const chevIdx=(DATE_IDX>=0 && !hiddenCols.has(DATE_IDX)) ? DATE_IDX : (vis.length?vis[0]:0);
  let tds=vis.map(i=>{ const v=r.cells[i], numeric=META[i].type==='metric'; let inner=(numeric&&typeof v==='number')?fmt(v):v;
    if(i===chevIdx && hasCh) inner=`<span class="tchev ${expanded?'open':''}" onclick="event.stopPropagation();toggleExpand(${gid})">▸</span>`+inner;
    return `<td class="${numeric?'num':''}" title="${esc(v)}">${inner}</td>`; }).join('');
  let h=`<tr class="parent-row"><td class="chk-col"><input type="checkbox" ${sel?'checked':''} onclick="toggleSel(${gid},this)"></td>${tds}</tr>`;
  if(hasCh && expanded) h+=r.childIdx.map(ix=>childRowHtml(REPORT.rows[ix])).join('');
  return h;
}
// ——— 顶部“汇总”行：维度列合并为一个“汇总”，指标随当前筛选结果实时聚合 ———
function aggMetricCells(rows){
  return COLS.map((c,i)=>{ if(META[i].type!=='metric') return '';
    let sum=0,cnt=0; for(const r of rows){ const v=r.cells[i]; if(v===''||v==null)continue; sum+=toNum(v); cnt++; }
    if(!cnt) return ''; return PCT_SET.has(i) ? round2(sum/cnt) : round2(sum); });
}
function grandChildrenCells(){   // 仅二级树：把已筛选各组的每日明细按日期再聚合
  const map=new Map();
  viewRows.forEach(p=> (p.childIdx||[]).forEach(ix=>{ const c=REPORT.rows[ix], d=c[DATE_IDX];
    if(d===''||d==null)return; if(!map.has(d))map.set(d,[]); map.get(d).push({cells:c}); }));
  return [...map.keys()].sort().map(d=>{ const cells=aggMetricCells(map.get(d)); cells[DATE_IDX]=d; return cells; });
}
function grandRowHtml(){
  const cells=aggMetricCells(viewRows), vis=visCols();
  let lead=0; for(const i of vis){ if(META[i].type==='metric')break; lead++; } if(lead<1)lead=1;
  const chev = TREE_ON ? `<span class="tchev ${grandExpanded?'open':''}" onclick="event.stopPropagation();toggleExpand('ALL')">▸</span>` : '';
  let tds=`<td colspan="${lead}" class="sum-merge">${chev}汇总</td>`;
  for(const i of vis.slice(lead)){ const numeric=META[i].type==='metric', v=cells[i];
    tds+=`<td class="${numeric?'num':''}">${numeric&&typeof v==='number'?fmt(v):''}</td>`; }
  let h=`<tr class="summary-row"><td class="chk-col"><input type="checkbox" ${selected.has('ALL')?'checked':''} onclick="toggleSel('ALL',this)"></td>${tds}</tr>`;
  if(TREE_ON && grandExpanded) h+=grandChildrenCells().map(childRowHtml).join('');
  return h;
}
function childRowHtml(cells){ const vis=visCols(); const firstIdx=(DATE_IDX>=0 && !hiddenCols.has(DATE_IDX))?DATE_IDX:vis[0];
  const tds=vis.map(i=>{ const v=cells[i], numeric=META[i].type==='metric';
    return `<td class="${numeric?'num':''} ${i===firstIdx?'child-first':''}" title="${esc(v)}">${(numeric&&typeof v==='number')?fmt(v):v}</td>`; }).join('');
  return `<tr class="child-row"><td class="chk-col"></td>${tds}</tr>`; }
function renderTableBody(){
  const start=(currentPage-1)*PAGE_SIZE, pageRows=viewRows.slice(start,start+PAGE_SIZE);
  let html='';
  if(HAS_GRAND && currentPage===1 && viewRows.length) html+=grandRowHtml();
  html += pageRows.map(r=>topRowHtml(r)).join('');
  document.getElementById('table-body').innerHTML = html || `<tr><td colspan="${visCols().length+1}" style="text-align:center;color:var(--text-dim);padding:24px">无匹配数据</td></tr>`;
  document.getElementById('page-info').textContent = `显示 ${viewRows.length?start+1:0}-${Math.min(start+PAGE_SIZE,viewRows.length)} / 共 ${viewRows.length} ${TREE_ON?'组':'条'}`;
  syncSelInfo(); syncAllChk(); renderPagination();
}
function renderPagination(){
  const box=document.getElementById('pagination'), totalPages=Math.ceil(viewRows.length/PAGE_SIZE);
  if(totalPages<=1){ box.innerHTML=''; return; }
  let btns=[`<button onclick="goPage(${currentPage-1})" ${currentPage===1?'disabled':''}>‹</button>`], pages=[];
  if(totalPages<=7){ for(let i=1;i<=totalPages;i++)pages.push(i); }
  else { pages=[1]; if(currentPage>3)pages.push('...'); for(let i=Math.max(2,currentPage-1);i<=Math.min(totalPages-1,currentPage+1);i++)pages.push(i); if(currentPage<totalPages-2)pages.push('...'); pages.push(totalPages); }
  pages.forEach(p=> p==='...'?btns.push('<span style="color:var(--text-dim);padding:0 4px">…</span>'):btns.push(`<button class="${p===currentPage?'active':''}" onclick="goPage(${p})">${p}</button>`));
  btns.push(`<button onclick="goPage(${currentPage+1})" ${currentPage===totalPages?'disabled':''}>›</button>`);
  box.innerHTML=btns.join('');
}
function goPage(p){ const tp=Math.ceil(viewRows.length/PAGE_SIZE); if(p<1||p>tp)return; currentPage=p; renderTableBody(); }
function sortTable(idx){
  if(sortCol===idx) sortAsc=!sortAsc; else { sortCol=idx; sortAsc=true; }
  const type=META[idx].type;
  viewRows.sort((a,b)=>{ let va=a.cells[idx],vb=b.cells[idx]; const ea=(va===''||va==null),eb=(vb===''||vb==null);
    if(ea&&eb)return 0; if(ea)return 1; if(eb)return -1;
    if(type==='metric'||(isNumericCell(va)&&isNumericCell(vb))){ const d=toNum(va)-toNum(vb); return sortAsc?d:-d; }
    if(type==='date')return sortAsc?String(va).localeCompare(String(vb)):String(vb).localeCompare(String(va));
    return sortAsc?String(va).localeCompare(String(vb),'zh'):String(vb).localeCompare(String(va),'zh'); });
  document.querySelectorAll('.data-table th[data-col]').forEach(th=>{ const i=+th.dataset.col; th.classList.toggle('sorted',i===idx); th.querySelector('.sort-icon').textContent=i===idx?(sortAsc?'↑':'↓'):'↕'; });
  currentPage=1; renderTableBody();
}

/* ===== 搜索 + 指标筛选 ===== */
function applyView(){
  const searchIdx = TREE_ON ? TREE.group_dim_idx : DIM_IDX;
  viewRows = baseRows().filter(r=>{
    if(searchQ && !searchIdx.some(i=>String(r.cells[i]).toLowerCase().includes(searchQ))) return false;
    for(const f of metricFilters){ const v=toNum(r.cells[f.idx]);
      if(f.op==='>'&&!(v>f.val))return false; if(f.op==='>='&&!(v>=f.val))return false; if(f.op==='='&&!(v===f.val))return false;
      if(f.op==='<='&&!(v<=f.val))return false; if(f.op==='<'&&!(v<f.val))return false; }
    return true;
  });
  if(sortCol>=0){ const sc=sortCol; sortCol=-1; sortTable(sc); return; }
  currentPage=1; renderTableBody();
}
function onSearch(){ searchQ=document.getElementById('search-input').value.trim().toLowerCase(); applyView(); }
function toggleFilterPop(e){ e.stopPropagation(); const pop=document.getElementById('filter-pop'); pop.classList.toggle('open');
  if(pop.classList.contains('open') && !filterRows.some(r=>r.alive)) addFilterRow(); }
function addFilterRow(){
  const wrap=document.getElementById('filter-rows'), row=document.createElement('div'); row.className='filter-row';
  const colHost=document.createElement('span'); colHost.style.flex='1';
  const opSel=document.createElement('select'); opSel.className='op'; opSel.innerHTML=['>','>=','=','<=','<'].map(o=>`<option>${o}</option>`).join('');
  const num=document.createElement('input'); num.className='num'; num.type='number'; num.placeholder='数值';
  const del=document.createElement('span'); del.className='del'; del.title='删除'; del.textContent='×';
  row.append(colHost,opSel,num,del); wrap.appendChild(row);
  const opts=METRIC_IDX.map(i=>({label:COLS[i],value:i}));
  const w=createSingleSelect(colHost, opts, opts[0].value, ()=>{}, '指标');
  const entry={getCol:()=>w.get(),getOp:()=>opSel.value,getNum:()=>num.value,alive:true};
  filterRows.push(entry); del.onclick=()=>{ entry.alive=false; row.remove(); };
}
function applyFilters(){
  metricFilters=[];
  filterRows.filter(r=>r.alive).forEach(r=>{ const idx=+r.getCol(), op=r.getOp(), raw=r.getNum();
    if(raw!==''&&!isNaN(parseFloat(raw))) metricFilters.push({idx,op,val:parseFloat(raw)}); });
  document.getElementById('filter-pop').classList.remove('open');
  const btn=document.getElementById('filter-btn'); btn.classList.toggle('on',metricFilters.length>0);
  btn.textContent=(metricFilters.length?`更多筛选(${metricFilters.length}) `:'更多筛选 ')+'▾';
  applyView();
}
function resetFilters(){ metricFilters=[]; filterRows=[]; document.getElementById('filter-rows').innerHTML=''; addFilterRow();
  const btn=document.getElementById('filter-btn'); btn.classList.remove('on'); btn.textContent='更多筛选 ▾'; applyView(); }
document.addEventListener('click',e=>{ const pop=document.getElementById('filter-pop'), btn=document.getElementById('filter-btn');
  if(pop.classList.contains('open') && !pop.contains(e.target) && e.target!==btn) pop.classList.remove('open'); });

/* ===== 维度列显隐配置 ===== */
function renderColsConfig(){
  const dims=COLS.map((c,i)=>({c,i})).filter(o=>META[o.i].type==='dim');
  document.getElementById('cols-list').innerHTML = dims.length ? dims.map(o=>
    `<label class="ms-item"><input type="checkbox" ${hiddenCols.has(o.i)?'':'checked'} onchange="toggleCol(${o.i},this.checked)"><span>${o.c}</span></label>`).join('')
    : '<div class="ms-empty">无维度列</div>';
}
function toggleColsPop(e){ e.stopPropagation(); document.getElementById('cols-pop').classList.toggle('open'); }
function toggleCol(i,show){ if(show)hiddenCols.delete(i); else hiddenCols.add(i); renderTableHead(); renderTableBody(); refreshAxisCharts(); }
document.addEventListener('click',e=>{ const pop=document.getElementById('cols-pop'), btn=document.getElementById('cols-btn');
  if(pop && pop.classList.contains('open') && !pop.contains(e.target) && e.target!==btn) pop.classList.remove('open'); });

/* ===== 勾选 / 展开 ===== */
function toggleSel(gid, el){ if(el.checked) selected.add(gid); else selected.delete(gid); syncSelInfo(); syncAllChk(); refreshSelCharts(); }
function toggleExpand(gid){ if(gid==='ALL') grandExpanded=!grandExpanded; else { const p=parents[gid]; if(p)p.expanded=!p.expanded; } renderTableBody(); }
function toggleAll(el){ viewRows.forEach(r=> el.checked?selected.add(gidOf(r)):selected.delete(gidOf(r))); renderTableBody(); refreshSelCharts(); }
function clearSel(){ selected.clear(); renderTableBody(); refreshSelCharts(); }
function syncAllChk(){ const all=document.getElementById('chk-all'); if(!all)return;
  all.checked = viewRows.length>0 && viewRows.every(r=>selected.has(gidOf(r))); all.indeterminate=!all.checked && viewRows.some(r=>selected.has(gidOf(r))); }
function syncSelInfo(){ const el=document.getElementById('sel-info'); el.innerHTML = selected.size ? `已选 ${selected.size} 项 <a href="#" onclick="clearSel();return false" style="color:var(--text-dim)">清除</a>` : ''; }

/* ===== 图表数据源 ===== */
function selectedParents(){ if(!TREE_ON)return []; const out=[]; selected.forEach(g=>{ if(g!=='ALL'&&parents[g]) out.push(parents[g]); }); return out; }
function chartDetailRows(){
  if(selected.size===0 || selected.has('ALL')) return allRows;
  if(TREE_ON){ const out=[]; selectedParents().forEach(p=>p.childIdx.forEach(ix=>out.push(allRows[ix]))); return out.length?out:allRows; }
  const out=allRows.filter(r=>selected.has(r.rid)); return out.length?out:allRows;
}
function groupLabel(p){ let idx=TREE.group_dim_idx.filter(i=>!hiddenCols.has(i)); if(!idx.length) idx=TREE.group_dim_idx; return idx.map(i=>p.cells[i]).join('_'); }
function groupDateMap(p, metrics){ const m={}; p.childIdx.forEach(ix=>{ const c=REPORT.rows[ix], d=c[DATE_IDX]; if(!m[d])m[d]={}; metrics.forEach(k=>m[d][k]=(m[d][k]||0)+toNum(c[colIndex(k)])); }); return m; }

/* ===== 自定义下拉（多选 / 单选，均带搜索）===== */
function closeAllPops(except){ document.querySelectorAll('.ms-pop.open').forEach(p=>{ if(p!==except)p.classList.remove('open'); }); }
function placePop(btn, pop){ const r=btn.getBoundingClientRect();
  pop.style.position='fixed'; pop.style.top=(r.bottom+4)+'px'; pop.style.left=r.left+'px'; pop.style.minWidth=Math.max(200,r.width)+'px'; }
window.addEventListener('scroll', ()=>closeAllPops(null), true);
function createMultiSelect(host, opts, getSel, setSel, getDisabled, onChange, placeholder){
  host.classList.add('ms');
  const btn=document.createElement('button'); btn.className='ms-btn';
  const pop=document.createElement('div'); pop.className='ms-pop';
  const search=document.createElement('input'); search.className='ms-search'; search.placeholder='搜索...';
  const list=document.createElement('div'); list.className='ms-list';
  pop.append(search,list); host.append(btn,pop);
  const label=()=>{ const s=getSel(); return `${placeholder}：${s.length?s.join('、'):'无'}`; };
  function renderList(){ const q=search.value.toLowerCase(), fl=opts.filter(o=>o.toLowerCase().includes(q));
    list.innerHTML = fl.length?'':'<div class="ms-empty">无匹配</div>';
    fl.forEach(o=>{ const dis=getDisabled(o), s=getSel().includes(o);
      const it=document.createElement('label'); it.className='ms-item'+(dis?' dis':'');
      it.innerHTML=`<input type="checkbox" ${s?'checked':''} ${dis?'disabled':''}><span>${o}</span>`;
      it.querySelector('input').addEventListener('change',ev=>{ let v=getSel().slice(); if(ev.target.checked)v.push(o); else v=v.filter(x=>x!==o); setSel(v); btn.textContent=label(); renderList(); onChange(); });
      list.appendChild(it); }); }
  btn.textContent=label();
  btn.onclick=e=>{ e.stopPropagation(); closeAllPops(pop); pop.classList.toggle('open'); if(pop.classList.contains('open')){ placePop(btn,pop); search.value=''; renderList(); search.focus(); } };
  search.oninput=renderList; search.onclick=e=>e.stopPropagation();
  document.addEventListener('click',e=>{ if(!host.contains(e.target) && e.target!==pop && !pop.contains(e.target)) pop.classList.remove('open'); });
  return { refresh(){ btn.textContent=label(); if(pop.classList.contains('open'))renderList(); } };
}
function createSingleSelect(host, opts, initVal, onChange, placeholder){
  let val=initVal; host.classList.add('ms');
  const btn=document.createElement('button'); btn.className='ms-btn';
  const pop=document.createElement('div'); pop.className='ms-pop';
  const search=document.createElement('input'); search.className='ms-search'; search.placeholder='搜索...';
  const list=document.createElement('div'); list.className='ms-list';
  pop.append(search,list); host.append(btn,pop);
  const cur=()=>{ const o=opts.find(o=>o.value==val); return (placeholder?placeholder+'：':'')+(o?o.label:''); };
  function renderList(){ const q=search.value.toLowerCase(), fl=opts.filter(o=>o.label.toLowerCase().includes(q));
    list.innerHTML = fl.length?'':'<div class="ms-empty">无匹配</div>';
    fl.forEach(o=>{ const it=document.createElement('div'); it.className='ms-item'+(o.value==val?' sel':''); it.textContent=o.label;
      it.onclick=()=>{ val=o.value; btn.textContent=cur(); pop.classList.remove('open'); onChange(val); }; list.appendChild(it); }); }
  btn.textContent=cur();
  btn.onclick=e=>{ e.stopPropagation(); closeAllPops(pop); pop.classList.toggle('open'); if(pop.classList.contains('open')){ placePop(btn,pop); search.value=''; renderList(); search.focus(); } };
  search.oninput=renderList; search.onclick=e=>e.stopPropagation();
  document.addEventListener('click',e=>{ if(!host.contains(e.target) && e.target!==pop && !pop.contains(e.target)) pop.classList.remove('open'); });
  return { get:()=>val, set:v=>{ val=v; btn.textContent=cur(); } };
}

/* ===== 折线 / 柱形 ===== */
const axisState = {
  line: { xmode:HAS_DATE?'date':'dim', left:METRICS.slice(0,1), right:METRICS.slice(1,2), chart:null },
  bar:  { xmode:HAS_DATE?'date':'dim', left:METRICS.slice(0,1), right:METRICS.slice(1,2), chart:null },
};
function aggregate(rows, xIdx, metrics){
  const map=new Map();
  rows.forEach(r=>{ const x=r.cells[xIdx]; if(x===''||x==null)return; let o=map.get(x); if(!o){o={};metrics.forEach(m=>o[m]=0);map.set(x,o);} metrics.forEach(m=>o[m]+=toNum(r.cells[colIndex(m)])); });
  let cats=[...map.keys()];
  if(xIdx===DATE_IDX) cats.sort();
  else if(metrics.length){ const pm=metrics[0]; cats.sort((a,b)=>(map.get(b)[pm]||0)-(map.get(a)[pm]||0)); cats=cats.slice(0,30); }
  return { cats, map };
}
function mkSeries(kind,name,onR,data,color){
  return kind==='line'
    ? { name,type:'line',yAxisIndex:onR?1:0,data,smooth:true,symbol:'circle',symbolSize:5,lineStyle:{width:2.5},itemStyle:{color} }
    : { name,type:'bar',yAxisIndex:onR?1:0,data,barMaxWidth:24,itemStyle:{color,borderRadius:[3,3,0,0]} };
}
function ecBase(o){ return Object.assign({ backgroundColor:'transparent', textStyle:{color:EC.text},
  tooltip:{backgroundColor:EC.tipBg,borderColor:EC.tipBorder,textStyle:{color:EC.tipText,fontSize:12},confine:true,extraCssText:'box-shadow:0 8px 28px rgba(20,28,48,.14);border-radius:8px;max-width:360px;white-space:normal;word-break:break-all;'} }, o); }
function shortName(s){ return s.length>20 ? s.slice(0,20)+'…' : s; }
function axisLabelCfg(rotate){ return {color:EC.text,fontSize:10,rotate,hideOverlap:true,margin:12}; }
function renderAxisChart(kind){
  const st=axisState[kind], el=document.getElementById('chart-'+kind); if(!el)return;
  const metrics=[...st.left,...st.right], xIdx=st.xmode==='date'?DATE_IDX:MAIN_DIM_IDX;
  if(xIdx<0||!metrics.length){ el.innerHTML='<div class="chart-empty">请至少选择一个左/右轴指标</div>'; st.chart=null; return; }
  if(el.querySelector('.chart-empty')) el.innerHTML='';
  const rightSet=new Set(st.right);
  let cats, series=[], ci=0;
  const selP=(TREE_ON && st.xmode==='date' && !selected.has('ALL')) ? selectedParents() : [];
  if(st.xmode==='date' && selP.length){
    // 按日期 + 已勾选分组：无论勾 1 条还是多条，每组都用「维度拼接_指标」命名
    cats=ALL_DATES.slice();
    selP.forEach(p=>{ const lab=groupLabel(p), bd=groupDateMap(p,metrics);
      metrics.forEach(m=>{ const onR=rightSet.has(m); const data=cats.map(d=> (bd[d]&&bd[d][m]!=null)?round2(bd[d][m]):null);
        series.push(mkSeries(kind, lab+'_'+m+(onR?' (右)':''), onR, data, COLORS[ci++%COLORS.length])); }); });
  } else if(st.xmode==='date'){
    // 按日期 + 未勾选(或勾选了“汇总”)：全量聚合，系列名以「汇总」开头
    const agg=aggregate(allRows,DATE_IDX,metrics); cats=agg.cats;
    metrics.forEach(m=>{ const onR=rightSet.has(m); const data=cats.map(c=>{const v=agg.map.get(c)[m];return v==null?null:round2(v);});
      series.push(mkSeries(kind, '汇总_'+m+(onR?' (右)':''), onR, data, COLORS[ci++%COLORS.length])); });
  } else {
    // 按维度：X 轴即为维度，系列就用指标名
    const rows=chartDetailRows(); const agg=aggregate(rows,xIdx,metrics); cats=agg.cats;
    metrics.forEach(m=>{ const onR=rightSet.has(m); const data=cats.map(c=>{const v=agg.map.get(c)[m];return v==null?null:round2(v);});
      series.push(mkSeries(kind, m+(onR?' (右)':''), onR, data, COLORS[ci++%COLORS.length])); });
  }
  if(!cats.length){ el.innerHTML='<div class="chart-empty">无可用数据</div>'; st.chart=null; return; }
  const hasRight=st.right.length>0;
  const yAxis=[{ type:'value', name:st.left.join('/'), nameTextStyle:{color:EC.sub}, axisLabel:{color:EC.text,fontSize:10,formatter:v=>fmt(v)}, splitLine:{lineStyle:{color:EC.split}} }];
  if(hasRight) yAxis.push({ type:'value', name:st.right.join('/'), position:'right', nameTextStyle:{color:EC.sub}, axisLabel:{color:EC.text,fontSize:10,formatter:v=>fmt(v)}, splitLine:{show:false} });
  if(!st.chart) st.chart=echarts.init(el);
  st.chart.setOption(ecBase({
    legend:{ data:series.map(s=>s.name), top:0, type:'scroll', textStyle:{color:EC.text,fontSize:11}, formatter:shortName, tooltip:{show:true} },
    tooltip:{ trigger:'axis', axisPointer:{type:kind==='bar'?'shadow':'line'} },
    xAxis:{ type:'category', data:cats, boundaryGap:kind==='bar', axisLabel:axisLabelCfg(cats.length>6?32:0), axisLine:{lineStyle:{color:EC.axis}}, axisTick:{show:false} },
    yAxis,
    series,
    grid:{ top:46, bottom:88, left:64, right:hasRight?68:28 },
    dataZoom:[ {type:'inside'}, {type:'slider',bottom:10,height:18,borderColor:EC.axis,fillerColor:'rgba(59,108,255,0.12)',handleStyle:{color:'#3b6cff'},textStyle:{color:EC.sub,fontSize:9}} ],
  }), true);
  st.chart.resize();
}
function refreshAxisCharts(){ renderAxisChart('line'); renderAxisChart('bar'); }

/* ===== 饼图（跟随勾选 · 可选分组维度 · 不合并其他）===== */
let pieChart=null, pieMetricW=null, pieDimW=null;
function renderPie(){
  const el=document.getElementById('chart-pie'); if(!el)return;
  if(!PIE_DIMS.length || !METRICS.length){ el.innerHTML='<div class="chart-empty">缺少维度或指标，无法生成占比图</div>'; return; }
  if(el.querySelector('.chart-empty')) el.innerHTML='';
  const metric=pieMetricW.get(), dimIdxs=PIE_DIMS[+pieDimW.get()].idx, map=new Map();
  chartDetailRows().forEach(r=>{ const key=dimIdxs.map(i=>r.cells[i]).join('_'); if(key===''||key==null)return; map.set(key,(map.get(key)||0)+toNum(r.cells[colIndex(metric)])); });
  const arr=[...map.entries()].map(([k,v])=>({name:String(k),value:round2(v)})).sort((a,b)=>b.value-a.value);
  if(!pieChart) pieChart=echarts.init(el);
  pieChart.setOption(ecBase({
    tooltip:{trigger:'item',formatter:'{b}: {c} ({d}%)'},
    legend:{type:'scroll',orient:'vertical',right:8,top:'middle',textStyle:{color:EC.text,fontSize:11}}, color:COLORS,
    series:[{ type:'pie', radius:['40%','68%'], center:['42%','50%'], data:arr, label:{color:EC.text,fontSize:11},
      itemStyle:{borderRadius:5,borderColor:'#fff',borderWidth:2}, emphasis:{label:{fontSize:14,fontWeight:'bold'}} }],
  }), true);
  pieChart.resize();
}

/* ===== 热力图（全量）===== */
let heatmapChart=null;
function renderHeatmap(){
  const el=document.getElementById('chart-heatmap'); if(!el||!REPORT.heatmap)return;
  const d=REPORT.heatmap; if(!heatmapChart) heatmapChart=echarts.init(el);
  heatmapChart.setOption(ecBase({
    tooltip:{formatter:p=>`${d.labels[p.data[0]]} ↔ ${d.labels[p.data[1]]}<br/>相关系数: ${p.data[2]}`},
    grid:{top:54,bottom:96,left:120,right:40},
    xAxis:{type:'category',data:d.labels,axisLabel:axisLabelCfg(38),axisLine:{lineStyle:{color:EC.axis}},axisTick:{show:false},splitArea:{show:true}},
    yAxis:{type:'category',data:d.labels,axisLabel:{color:EC.text,fontSize:10},axisLine:{lineStyle:{color:EC.axis}},axisTick:{show:false},splitArea:{show:true}},
    visualMap:{min:-1,max:1,calculable:true,orient:'horizontal',left:'center',top:6,itemWidth:14,itemHeight:120,inRange:{color:['#ef4444','#f4f6f9','#10b981']},textStyle:{color:EC.sub}},
    series:[{type:'heatmap',data:d.data,label:{show:true,color:'#1d2433',fontSize:10},emphasis:{itemStyle:{shadowBlur:10,shadowColor:'rgba(0,0,0,0.2)'}}}],
  }));
  heatmapChart.resize();
}

function refreshSelCharts(){ refreshAxisCharts(); renderPie(); }
function resizeAllCharts(){ ['line','bar'].forEach(k=>axisState[k].chart&&axisState[k].chart.resize()); pieChart&&pieChart.resize(); heatmapChart&&heatmapChart.resize(); }

/* ===== 构建图表区 ===== */
function buildChartArea(){
  let html='';
  ['line','bar'].forEach(kind=>{
    const title=kind==='line'?'平滑折线图':'柱形图';
    const seg=HAS_DATE
      ? `<div class="seg"><button class="${axisState[kind].xmode==='date'?'on':''}" onclick="setXMode('${kind}','date')">按日期</button><button class="${axisState[kind].xmode==='dim'?'on':''}" onclick="setXMode('${kind}','dim')">按维度</button></div>`
      : `<span class="clabel">X轴：${MAIN_DIM_IDX>=0?COLS[MAIN_DIM_IDX]:'维度'}</span>`;
    html+=`<div class="chart-card"><div class="chart-head"><span class="ctitle">${title}</span>${seg}<span class="clabel">左轴</span><span id="ms-left-${kind}"></span><span class="clabel">右轴</span><span id="ms-right-${kind}"></span></div><div class="chart-box" id="chart-${kind}"></div></div>`;
  });
  html+=`<div class="chart-card"><div class="chart-head"><span class="ctitle">占比分布</span><span class="clabel">维度</span><span id="pie-dim"></span><span class="clabel">指标</span><span id="pie-metric"></span></div><div class="chart-box" id="chart-pie"></div></div>`;
  if(REPORT.heatmap) html+=`<div class="chart-card"><div class="chart-head"><span class="ctitle">指标相关性热力图（全量）</span></div><div class="chart-box" id="chart-heatmap"></div></div>`;
  document.getElementById('chart-area').innerHTML=html;

  ['line','bar'].forEach(kind=>{ const st=axisState[kind], refs={};
    refs.left=createMultiSelect(document.getElementById('ms-left-'+kind), METRICS, ()=>st.left, v=>{st.left=v;}, o=>st.right.includes(o), ()=>{ refs.right.refresh(); renderAxisChart(kind); }, '左轴');
    refs.right=createMultiSelect(document.getElementById('ms-right-'+kind), METRICS, ()=>st.right, v=>{st.right=v;}, o=>st.left.includes(o), ()=>{ refs.left.refresh(); renderAxisChart(kind); }, '右轴');
  });
  let pieDefault=0; PIE_DIMS.forEach((o,i)=>{ if(o.idx.length===1 && o.idx[0]===MAIN_DIM_IDX) pieDefault=i; });
  pieDimW=createSingleSelect(document.getElementById('pie-dim'), PIE_DIMS.map((d,i)=>({label:d.label,value:i})), pieDefault, ()=>renderPie(), '');
  pieMetricW=createSingleSelect(document.getElementById('pie-metric'), METRICS.map(m=>({label:m,value:m})), METRICS[0], ()=>renderPie(), '');
  refreshAxisCharts(); renderPie(); renderHeatmap();
}
function setXMode(kind,mode){ axisState[kind].xmode=mode;
  const head=document.getElementById('chart-'+kind).parentNode.querySelector('.seg');
  if(head){ const b=head.querySelectorAll('button'); b[0].classList.toggle('on',mode==='date'); b[1].classList.toggle('on',mode==='dim'); }
  renderAxisChart(kind);
}
window.addEventListener('resize', resizeAllCharts);

/* ===== 初始化 ===== */
buildNav();
renderOverview(); renderStats(); renderAnomalies(); renderSuggestions();
renderTableHead(); renderColsConfig(); renderTableBody(); buildChartArea();
</script>
</body>
</html>"""


# ── 主入口 ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="通用数据分析工具（模式 A）")
    parser.add_argument("--file", required=True, help="报表文件路径 (.xlsx/.xls/.csv)")
    parser.add_argument("--out", default="data_report.html",
                        help="输出 HTML 文件名/路径（纯文件名时放入 data-auto-analyzer 目录）")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    print(f"\n正在读取: {args.file}")
    df, summary_df = load_file(args.file)
    print(f"读取成功，共 {len(df)} 行 × {len(df.columns)} 列")

    date_col, dim_cols, metric_cols, pct_cols = detect_columns(df)
    if not metric_cols:
        print("❌ 未找到数值列，请确认文件中包含数字数据")
        sys.exit(1)

    print(f"日期列: {date_col or '未识别'}")
    print(f"维度列: {', '.join(str(c) for c in dim_cols) or '无'}")
    print(f"指标列: {', '.join(str(c) for c in metric_cols)}")

    main_dim = _pick_main_dim(df, dim_cols)
    columns, rows = prepare_table_data(df, date_col)
    summary_row, sum_is_orig = build_summary_row(
        df, columns, date_col, dim_cols, metric_cols, pct_cols, summary_df, main_dim)
    tree = build_tree(df, columns, date_col, dim_cols, metric_cols, pct_cols, main_dim)
    if tree.get("enabled"):
        print(f"二级树: 已启用（{len(tree['parents'])} 个维度组，可展开按日期明细）")

    col_meta = []
    for c in df.columns:
        t = "date" if c == date_col else ("metric" if c in metric_cols else "dim")
        col_meta.append({"name": str(c), "type": t})

    col_list = list(df.columns)
    date_col_index = col_list.index(date_col) if date_col is not None else -1
    main_dim_index = col_list.index(main_dim) if main_dim is not None else -1
    dim_idx = [col_list.index(c) for c in dim_cols]
    metric_idx = [col_list.index(c) for c in metric_cols]
    pct_idx = [col_list.index(c) for c in pct_cols]
    # 全表只有唯一值的维度列（内容重复无信息量）→ 默认在表格中隐藏，可在“显示列”里勾回
    constant_dim_idx = [col_list.index(c) for c in dim_cols if df[c].nunique(dropna=False) <= 1]

    # 饼图分组维度：包含账户ID 等业务标识列，仅排除“每行都唯一”的行号类列；并提供全维度组合
    pie_cols = [c for c in dim_cols if df[c].nunique(dropna=False) < len(df)] or list(dim_cols)
    pie_dim_options = [{"label": str(c), "idx": [col_list.index(c)]} for c in pie_cols]
    if len(pie_cols) > 1:
        pie_dim_options.append({"label": "+".join(str(c) for c in pie_cols),
                                "idx": [col_list.index(c) for c in pie_cols]})

    date_range = ""
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
        if len(dates):
            date_range = f"{dates.min().strftime('%Y-%m-%d')} ~ {dates.max().strftime('%Y-%m-%d')}"

    report = {
        "file_name": os.path.basename(args.file),
        "total_rows": len(df), "total_cols": len(df.columns),
        "date_col": str(date_col) if date_col else None,
        "date_col_index": date_col_index, "main_dim_index": main_dim_index,
        "date_range": date_range,
        "dim_cols": [str(c) for c in dim_cols], "metric_cols": [str(c) for c in metric_cols],
        "dim_idx": dim_idx, "metric_idx": metric_idx, "pct_idx": pct_idx,
        "constant_dim_idx": constant_dim_idx, "col_meta": col_meta,
        "summary_stats": get_summary_stats(df, metric_cols, pct_cols),
        "anomalies": detect_anomalies(df, metric_cols),
        "suggestions": get_suggestions(df, metric_cols, dim_cols),
        "heatmap": prepare_heatmap(df, metric_cols),
        "columns": columns, "rows": rows,
        "summary_row": summary_row, "summary_is_original": sum_is_orig,
        "tree": tree, "pie_dim_options": pie_dim_options,
    }

    html_content = generate_html()
    report_json = json.dumps(report, ensure_ascii=False, default=str)
    html_content = html_content.replace("{{REPORT_JSON}}", report_json)
    html_content = html_content.replace("{{FILE_NAME}}", html_mod.escape(report["file_name"]))
    html_content = html_content.replace("{{TOTAL_ROWS}}", str(report["total_rows"]))
    html_content = html_content.replace("{{TOTAL_COLS}}", str(report["total_cols"]))

    out_path = resolve_output_path(args.out)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    n_charts = 3 + (1 if report["heatmap"] else 0)
    print(f"\n{'=' * 60}")
    print(f"✅ 分析完成！交互式 HTML 报告已生成（浅色主题）")
    print(f"   报告路径: {out_path}")
    print(f"   表格: {'二级树（父=维度汇总/子=按日期）' if tree.get('enabled') else '平铺'} · 每页 10 条")
    print(f"   汇总行: {'原报表提取' if sum_is_orig else ('自动计算' if summary_row else '无')}")
    print(f"   图表: {n_charts} 个（折线/柱形双轴·按组成线 · 饼图可选维度 · 热力图全量）· 含悬浮导航")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
