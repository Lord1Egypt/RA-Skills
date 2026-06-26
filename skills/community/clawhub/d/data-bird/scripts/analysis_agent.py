"""
AnalysisAgent: 面向通用业务表生成“趋势/结构/对比/分布/异常/关系”覆盖型图表结果。
"""
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

DEFAULT_MAX_CHARTS = 5
DEFAULT_MIN_CHARTS = 5
TOP_N = 10


def _column_mentioned(cols: List[str], query: str) -> Optional[str]:
    for c in cols:
        s = str(c).strip()
        if s and (s in query or s.lower() in query.lower()):
            return c
    return None


def _detect_intents(query: str) -> List[str]:
    q = (query or "").strip()
    intents: List[str] = []
    if any(k in q for k in ("占比", "比例", "构成", "份额", "饼图", "结构")):
        intents.append("pie")
    if any(k in q.lower() for k in ("top", "rank")) or any(k in q for k in ("排名", "最高", "最低", "排行")):
        intents.append("rank")
    if any(k in q for k in ("分布", "直方", "频次", "波动范围")):
        intents.append("distribution")
    if any(k in q for k in ("相关", "散点", "关系", "相关性")):
        intents.append("scatter")
    if any(k in q for k in ("趋势", "走势", "时间", "按日", "按月", "变化", "增长", "同比", "环比")):
        intents.append("trend")
    if any(k in q for k in ("异常", "缺失", "质量", "风险")):
        intents.append("quality")
    return intents


def _profile_map(schema: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    prof = (schema.get("profile") or {}).get("columns") or []
    return {str(p.get("name")): p for p in prof}


def _candidate_dims(schema: Dict[str, Any]) -> List[str]:
    dims = list(schema.get("dimension_columns") or [])
    prof = _profile_map(schema)
    return sorted(
        dims,
        key=lambda c: (
            999 if int(prof.get(c, {}).get("unique_count", 0) or 0) <= 1 else 0,
            abs(int(prof.get(c, {}).get("unique_count", 0) or 0) - 10),
            len(str(c)),
        ),
    )


def _candidate_metrics(schema: Dict[str, Any], query: str) -> List[str]:
    metrics = list(schema.get("metric_columns") or [])
    if not metrics:
        return []
    mentioned = _column_mentioned(metrics, query)
    ordered = [mentioned] if mentioned else []
    ordered.extend([m for m in metrics if m not in ordered])
    return ordered


def _pick_period(series: pd.Series) -> str:
    uniq = int(series.nunique())
    if uniq > 180:
        return "M"
    if uniq > 60:
        return "W"
    return "D"


def _trend_takeaway(series: List[float], label: str) -> str:
    if len(series) < 2:
        return f"{label}样本不足，适合继续观察"
    first, last = float(series[0]), float(series[-1])
    if abs(first) < 1e-9:
        if abs(last) < 1e-9:
            return f"{label}整体平稳，未见明显变化"
        return f"{label}后段明显放量，值得关注成因"
    change = (last - first) / abs(first)
    if change >= 0.15:
        return f"{label}整体上行，末期较初期提升明显"
    if change <= -0.15:
        return f"{label}整体承压，末期水平明显低于初期"
    return f"{label}总体平稳，主要呈阶段性波动"


def _share_takeaway(names: List[str], values: List[float], label: str) -> str:
    if not names or not values:
        return f"{label}暂无足够样本"
    total = sum(float(v or 0) for v in values)
    top_name = str(names[0])
    top_val = float(values[0] or 0)
    share = (top_val / total * 100.0) if total else 0.0
    return f"{top_name}为当前最核心项，贡献约{share:.1f}%"


def _corr_takeaway(values: List[List[float]], x_name: str, y_name: str) -> str:
    if len(values) < 4:
        return f"{x_name}与{y_name}样本不足，暂不判断相关性"
    arr = np.array(values, dtype=float)
    corr = float(np.corrcoef(arr[:, 0], arr[:, 1])[0, 1])
    if corr >= 0.45:
        return f"{x_name}与{y_name}呈较明显正相关"
    if corr <= -0.45:
        return f"{x_name}与{y_name}呈较明显负相关"
    return f"{x_name}与{y_name}相关性偏弱"


def _add_result(results: List[Dict[str, Any]], result: Dict[str, Any], seen: set, key: str, limit: int) -> None:
    if key in seen or len(results) >= limit:
        return
    if result.get("error"):
        return
    seen.add(key)
    results.append(result)


def _add_trend(df: pd.DataFrame, time_col: str, metric: Optional[str], results: List[Dict[str, Any]], seen: set, limit: int) -> None:
    df_t = df.copy()
    df_t[time_col] = pd.to_datetime(df_t[time_col], errors="coerce")
    df_t = df_t.dropna(subset=[time_col])
    if df_t.empty:
        return
    period = _pick_period(df_t[time_col])
    df_t["_period"] = df_t[time_col].dt.to_period(period).astype(str)
    if metric and metric in df_t.columns:
        agg = df_t.groupby("_period")[metric].sum().reset_index()
        values = pd.to_numeric(agg[metric], errors="coerce").fillna(0).tolist()
        result = {
            "type": "trend",
            "chart_type": "line",
            "title_hint": f"{metric}趋势",
            "x_label": "时间",
            "x_data": agg["_period"].tolist(),
            "series": [{"name": metric, "data": values}],
            "takeaway_hint": _trend_takeaway(values, metric),
            "chart_family": "trend",
        }
        _add_result(results, result, seen, f"trend:{metric}", limit)
    else:
        agg = df_t.groupby("_period").size().reset_index(name="记录数")
        values = agg["记录数"].astype(int).tolist()
        result = {
            "type": "trend",
            "chart_type": "line",
            "title_hint": "记录数趋势",
            "x_label": "时间",
            "x_data": agg["_period"].tolist(),
            "series": [{"name": "记录数", "data": values}],
            "takeaway_hint": _trend_takeaway(values, "记录数"),
            "chart_family": "trend",
        }
        _add_result(results, result, seen, "trend:count", limit)


def _group_values(df: pd.DataFrame, dim: str, metric: Optional[str], head: int, ascending: bool = False) -> Tuple[List[str], List[float], str]:
    if metric and metric in df.columns:
        agg = (
            df.groupby(dim)[metric]
            .sum()
            .sort_values(ascending=ascending)
            .head(head)
        )
        return [str(x) for x in agg.index.tolist()], [float(v) for v in agg.tolist()], metric
    agg = df.groupby(dim).size().sort_values(ascending=ascending).head(head)
    return [str(x) for x in agg.index.tolist()], [float(v) for v in agg.tolist()], "记录数"


def _add_compare(df: pd.DataFrame, dim: str, metric: Optional[str], results: List[Dict[str, Any]], seen: set, limit: int, title_hint: str, head: int = TOP_N, ascending: bool = False, result_type: str = "compare") -> None:
    names, values, series_name = _group_values(df, dim, metric, head=head, ascending=ascending)
    if len(names) < 2:
        return
    result = {
        "type": result_type,
        "chart_type": "bar",
        "title_hint": title_hint,
        "x_label": dim,
        "x_data": names,
        "series": [{"name": series_name, "data": values}],
        "takeaway_hint": _share_takeaway(names, values, series_name),
        "chart_family": "comparison" if result_type == "compare" else result_type,
    }
    _add_result(results, result, seen, f"{result_type}:{dim}:{series_name}:{ascending}", limit)


def _add_pie(df: pd.DataFrame, dim: str, metric: Optional[str], results: List[Dict[str, Any]], seen: set, limit: int) -> None:
    names, values, series_name = _group_values(df, dim, metric, head=8, ascending=False)
    if len(names) < 2:
        return
    pie_data = [{"name": n, "value": float(v)} for n, v in zip(names, values)]
    result = {
        "type": "pie",
        "chart_type": "pie",
        "title_hint": f"{dim}占比构成",
        "pie_data": pie_data,
        "takeaway_hint": _share_takeaway(names, values, series_name),
        "chart_family": "composition",
    }
    _add_result(results, result, seen, f"pie:{dim}:{series_name}", limit)


def _add_distribution(df: pd.DataFrame, metric: str, results: List[Dict[str, Any]], seen: set, limit: int) -> None:
    s = pd.to_numeric(df[metric], errors="coerce").dropna()
    if len(s) < 5:
        return
    arr = s.astype(float).values
    nb = min(18, max(6, len(arr) // 20))
    counts, edges = np.histogram(arr, bins=nb)
    labels = [f"{edges[i]:.2g}~{edges[i + 1]:.2g}" for i in range(len(counts))]
    center_idx = int(np.argmax(counts))
    result = {
        "type": "distribution",
        "chart_type": "histogram",
        "title_hint": f"{metric}分布",
        "x_label": metric,
        "x_data": labels,
        "series": [{"name": "频数", "data": counts.astype(int).tolist()}],
        "takeaway_hint": f"{metric}主要集中在 {labels[center_idx]} 区间",
        "chart_family": "distribution",
    }
    _add_result(results, result, seen, f"dist:{metric}", limit)


def _add_scatter(df: pd.DataFrame, m1: str, m2: str, results: List[Dict[str, Any]], seen: set, limit: int) -> None:
    sub = df[[m1, m2]].apply(pd.to_numeric, errors="coerce").dropna().head(800)
    if len(sub) < 4:
        return
    data = [[float(r[m1]), float(r[m2])] for _, r in sub.iterrows()]
    result = {
        "type": "scatter",
        "chart_type": "scatter",
        "title_hint": f"{m1}与{m2}关系",
        "x_metric": m1,
        "y_metric": m2,
        "scatter_data": data,
        "takeaway_hint": _corr_takeaway(data, m1, m2),
        "chart_family": "correlation",
    }
    _add_result(results, result, seen, f"scatter:{m1}:{m2}", limit)


def _add_quality(schema: Dict[str, Any], results: List[Dict[str, Any]], seen: set, limit: int) -> None:
    prof = (schema.get("profile") or {}).get("columns") or []
    rows = [p for p in prof if float(p.get("null_pct", 0) or 0) > 0]
    if not rows:
        return
    rows = sorted(rows, key=lambda p: float(p.get("null_pct", 0) or 0), reverse=True)[:8]
    x_data = [str(r.get("name")) for r in rows]
    values = [float(r.get("null_pct", 0) or 0) for r in rows]
    result = {
        "type": "quality",
        "chart_type": "bar",
        "title_hint": "字段缺失率",
        "x_label": "字段",
        "x_data": x_data,
        "series": [{"name": "缺失率%", "data": values}],
        "takeaway_hint": f"{x_data[0]} 缺失率最高，建议优先核查采集口径",
        "chart_family": "quality",
    }
    _add_result(results, result, seen, "quality:missing", limit)


def _add_metric_totals(df: pd.DataFrame, metrics: List[str], results: List[Dict[str, Any]], seen: set, limit: int) -> None:
    if len(metrics) < 2:
        return
    values: List[float] = []
    names: List[str] = []
    for metric in metrics[:8]:
        s = pd.to_numeric(df[metric], errors="coerce")
        if s.notna().sum() == 0:
            continue
        names.append(metric)
        values.append(float(s.fillna(0).sum()))
    if len(names) < 2:
        return
    result = {
        "type": "metric_compare",
        "chart_type": "bar",
        "title_hint": "核心指标总量对比",
        "x_label": "指标",
        "x_data": names,
        "series": [{"name": "总量", "data": values}],
        "takeaway_hint": _share_takeaway(names, values, "总量"),
        "chart_family": "metric_compare",
    }
    _add_result(results, result, seen, "metric:totals", limit)


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    df: pd.DataFrame = context.get("df")
    schema = context.get("schema") or {}
    query = str(context.get("query") or "").strip()
    opts = context.get("options") if isinstance(context.get("options"), dict) else {}

    time_col = schema.get("detected_time_column")
    metric_cols = _candidate_metrics(schema, query)
    dim_cols = _candidate_dims(schema)
    intents = _detect_intents(query)
    max_charts = min(12, max(1, int(opts.get("max_chart_count") or DEFAULT_MAX_CHARTS)))
    target_charts = min(max_charts, max(1, int(opts.get("min_chart_count") or DEFAULT_MIN_CHARTS)))

    if not metric_cols:
        metric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    results: List[Dict[str, Any]] = []
    seen: set = set()

    def primary_dim(idx: int = 0) -> Optional[str]:
        return dim_cols[idx] if len(dim_cols) > idx else None

    # 用户明确要求时优先满足
    if "trend" in intents and time_col:
        _add_trend(df, time_col, metric_cols[0] if metric_cols else None, results, seen, max_charts)
    if "pie" in intents and primary_dim():
        _add_pie(df, primary_dim(), metric_cols[0] if metric_cols else None, results, seen, max_charts)
    if "rank" in intents and primary_dim():
        _add_compare(df, primary_dim(), metric_cols[0] if metric_cols else None, results, seen, max_charts, "头部排名", result_type="rank")
    if "distribution" in intents and metric_cols:
        _add_distribution(df, metric_cols[0], results, seen, max_charts)
    if "scatter" in intents and len(metric_cols) >= 2:
        _add_scatter(df, metric_cols[0], metric_cols[1], results, seen, max_charts)
    if "quality" in intents:
        _add_quality(schema, results, seen, max_charts)

    # 通用覆盖：趋势、对比、结构、排名、分布、关系、尾部、质量
    if time_col:
        _add_trend(df, time_col, metric_cols[0] if metric_cols else None, results, seen, max_charts)
    if primary_dim():
        _add_compare(df, primary_dim(), metric_cols[0] if metric_cols else None, results, seen, max_charts, "分类对比")
        _add_pie(df, primary_dim(), metric_cols[0] if metric_cols else None, results, seen, max_charts)
        _add_compare(df, primary_dim(), metric_cols[0] if metric_cols else None, results, seen, max_charts, "头部排名", result_type="rank")
        _add_compare(df, primary_dim(), metric_cols[0] if metric_cols else None, results, seen, max_charts, "尾部观察", head=8, ascending=True, result_type="tail")
    if len(dim_cols) >= 2:
        _add_compare(df, dim_cols[1], metric_cols[0] if metric_cols else None, results, seen, max_charts, f"{dim_cols[1]}对比")
        _add_pie(df, dim_cols[1], metric_cols[0] if metric_cols else None, results, seen, max_charts)
    if metric_cols:
        _add_distribution(df, metric_cols[0], results, seen, max_charts)
    if len(metric_cols) >= 2:
        _add_distribution(df, metric_cols[1], results, seen, max_charts)
        _add_scatter(df, metric_cols[0], metric_cols[1], results, seen, max_charts)
        _add_metric_totals(df, metric_cols, results, seen, max_charts)
    _add_quality(schema, results, seen, max_charts)

    # 极端情况下仍无图时，回退到按首个维度计数
    if not results and primary_dim():
        _add_compare(df, primary_dim(), None, results, seen, max_charts, "记录数对比")
        _add_pie(df, primary_dim(), None, results, seen, max_charts)
        _add_quality(schema, results, seen, max_charts)

    context["analysis"] = {
        "intents": intents or ["auto"],
        "scenario": schema.get("scenario"),
        "target_chart_count": target_charts,
        "generated_chart_count": len(results),
        "results": results[:max_charts],
    }
    return context
