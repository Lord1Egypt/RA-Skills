# -*- coding: utf-8 -*-
"""
工作日报能力实现

接口：queryDailyReportSummary
入参：{date}　出参：data: List<DailyReportSummaryDTO>
每项字段：metricName / metricValue / unit / yesterdayPercentage

sellerUserId 不需要传递，网关会根据 AK 自动注入实际调用方 userId。
"""

import time
from datetime import date as _date
from typing import Any, Dict, List

from _errors import ServiceError
from _http import api_post
from settings import settings


def _normalize_date(date: str) -> str:
    """把 'today' 转成 'YYYY-MM-DD'；其余原样返回（上游 cmd 已做过格式校验）"""
    if date == "today":
        return _date.today().isoformat()
    return date


def get_daily_report(date: str) -> Dict[str, Any]:
    """
    获取接待助手工作日报总结

    Args:
        date: 查询日期，"today" 或 "YYYY-MM-DD"

    Returns:
        {
          "date": "2026-05-14",
          "elapsed_seconds": 0.4,
          "metrics": [
              {"name": "接待人数", "value": "15", "unit": "人", "yoy": "+12.5%"},
              ...
          ]
        }
    """
    start_time = time.time()

    query_date = _normalize_date(date)
    body = {"date": query_date}

    resp = api_post(
        path=settings.DAILY_REPORT_PATH,
        body=body,
        timeout=settings.API_TIMEOUT,
    )

    if not resp.get("success"):
        err = resp.get("errorMsg") or resp.get("message") or resp
        raise ServiceError("获取日报失败：{}".format(err))

    # 网关双层包装：resp.data 是 {"data": [...DTO...]}，需再剥一层
    raw_metrics = (resp.get("data") or {}).get("data") or []

    metrics: List[Dict[str, Any]] = [
        {
            "name": item.get("metricName", ""),
            "value": item.get("metricValue", "--"),
            "unit": item.get("unit") or "",
            "yoy": item.get("yesterdayPercentage") or "",
        }
        for item in raw_metrics
    ]

    return {
        "date": query_date,
        "elapsed_seconds": round(time.time() - start_time, 1),
        "metrics": metrics,
    }


def format_report_markdown(result: Dict[str, Any]) -> str:
    """将日报总结指标列表格式化为 Markdown 表格"""
    date_str = result.get("date", "")
    metrics = result.get("metrics", [])

    lines = ["## 接待助手工作日报（{}）\n".format(date_str)]

    if not metrics:
        lines.append("今天没数据，可能日报还在统计中。")
        return "\n".join(lines)

    lines.append("| 指标 | 数值 | 较昨日 |")
    lines.append("|------|------|--------|")
    for m in metrics:
        value_str = "{}{}".format(m["value"], m["unit"]) if m["unit"] else m["value"]
        lines.append("| {} | **{}** | {} |".format(m["name"], value_str, m["yoy"] or "—"))

    return "\n".join(lines)
