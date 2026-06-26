#!/usr/bin/env python3
"""商机热榜 — 服务层"""

from typing import Any, Dict, List

from _http import api_post
from _errors import ServiceError


def _fmt_detail(title: str, detail: list, max_topics: int = 3) -> List[str]:
    if not detail or not isinstance(detail, list):
        return []
    lines = [f"**{title} Top {max_topics}**"]
    for item in detail[:max_topics]:
        topic = item.get("topic", "-")
        rank = item.get("rank", "-")
        lines.append(f"- {rank}. {topic}")
    return lines


def _build_markdown(biz_data: Dict[str, Any]) -> str:
    if not biz_data:
        return "未返回商机数据。"

    parts: List[str] = ["## 商机热榜"]
    for platform, pdata in biz_data.items():
        parts.append(f"\n### {platform}")
        trend = pdata.get("trend", {})
        hot = pdata.get("hot", {})

        trend_lines = _fmt_detail("趋势", trend.get("detail"))
        hot_lines = _fmt_detail("热度", hot.get("detail"))

        if trend_lines:
            parts.append("\n".join(trend_lines))
        if hot_lines:
            parts.append("\n".join(hot_lines))

    return "\n\n".join(parts)


def fetch_opportunities(timeout: int = 20) -> dict:
    """
    拉取商机热榜（使用 AK 签名）

    Returns:
        {"markdown": str, "data": dict}
    """
    body = {"code": "offer_opportunity"}
    model = api_post("/1688claw/skill/workflow", body, timeout=timeout)

    biz_data = (model or {}).get("bizData")
    if biz_data is None:
        raise ServiceError("商机接口返回为空")

    markdown = _build_markdown(biz_data)
    return {"markdown": markdown, "data": biz_data}
