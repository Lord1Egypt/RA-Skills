"""
ChartAgent: 根据分析结果生成 ECharts option JSON。
支持 line / bar / pie / histogram(bar) / scatter。
"""
from typing import Any, Dict, List


def build_line_option(title: str, x_data: List, series: List[Dict], x_label: str = "") -> Dict[str, Any]:
    opt: Dict[str, Any] = {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": x_data, "name": x_label or ""},
        "yAxis": {"type": "value"},
        "series": [
            {"name": s.get("name", ""), "type": "line", "data": s.get("data", [])}
            for s in series
        ],
    }
    return opt


def build_bar_option(title: str, x_data: List, series: List[Dict], x_label: str = "") -> Dict[str, Any]:
    return {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": x_data, "name": x_label or "", "axisLabel": {"rotate": 30}},
        "yAxis": {"type": "value"},
        "series": [
            {"name": s.get("name", ""), "type": "bar", "data": s.get("data", [])}
            for s in series
        ],
    }


def build_pie_option(title: str, pie_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
        "legend": {"orient": "vertical", "left": "left", "type": "scroll"},
        "series": [
            {
                "name": title,
                "type": "pie",
                "radius": "55%",
                "center": ["50%", "55%"],
                "data": pie_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }


def build_histogram_option(title: str, x_data: List, series: List[Dict], x_label: str = "") -> Dict[str, Any]:
    return {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": x_data, "name": x_label or "", "axisLabel": {"rotate": 45}},
        "yAxis": {"type": "value", "name": "频数"},
        "series": [
            {"name": s.get("name", "频数"), "type": "bar", "data": s.get("data", [])}
            for s in series
        ],
    }


def build_scatter_option(
    title: str, x_name: str, y_name: str, data: List[List[float]]
) -> Dict[str, Any]:
    return {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "value", "name": x_name, "scale": True},
        "yAxis": {"type": "value", "name": y_name, "scale": True},
        "series": [{"type": "scatter", "symbolSize": 8, "data": data}],
    }


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """生成 ECharts 图表数组。"""
    analysis = context.get("analysis") or {}
    results = analysis.get("results") or []
    query = str(context.get("query") or "数据分析").strip()[:40]

    charts: List[Dict[str, Any]] = []
    idx = 0
    for r in results:
        if r.get("error"):
            continue
        ctype = r.get("chart_type", "line")
        title_hint = r.get("title_hint") or ""
        title = f"{query} · {title_hint}" if title_hint else f"{query} · 图{idx + 1}"
        idx += 1

        if ctype == "pie" and r.get("pie_data"):
            opt = build_pie_option(title, r["pie_data"])
        elif ctype == "scatter" and r.get("scatter_data"):
            opt = build_scatter_option(
                title,
                str(r.get("x_metric", "x")),
                str(r.get("y_metric", "y")),
                r["scatter_data"],
            )
        elif ctype == "histogram":
            opt = build_histogram_option(
                title,
                r.get("x_data") or [],
                r.get("series") or [],
                str(r.get("x_label", "")),
            )
        elif ctype == "bar":
            opt = build_bar_option(
                title,
                r.get("x_data") or [],
                r.get("series") or [],
                str(r.get("x_label", "")),
            )
        else:
            opt = build_line_option(
                title,
                r.get("x_data") or [],
                r.get("series") or [],
                str(r.get("x_label", "")),
            )

        charts.append(
            {
                "id": f"chart_{idx}",
                "type": ctype,
                "title": title,
                "family": r.get("chart_family") or r.get("type") or ctype,
                "takeaway": str(r.get("takeaway_hint") or "").strip(),
                "option": opt,
            }
        )

    context["charts"] = charts
    return context
