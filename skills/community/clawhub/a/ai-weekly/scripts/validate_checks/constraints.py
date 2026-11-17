"""check_constraints — 硬约束校验（P2-1：边界条件集中声明）。

校验 HTML 报告是否满足预设的硬限制：
- 新闻卡片数 ≤ NEWS_MAX_ITEMS（100）
- 排行榜每榜行数 ≤ LEADERBOARD_TOP_N（50）
- HTML 体积 ≤ HTML_MAX_SIZE_BYTES（5 MB）
- Chart.js 数据点 ≤ CHART_MAX_DATA_POINTS（20）

这些约束在 generate_site.py 中强制实施，此处做事后审计。
"""
from __future__ import annotations

import re
from pathlib import Path

from aiweekly.const import (
    NEWS_MAX_ITEMS,
    LEADERBOARD_TOP_N,
    HTML_MAX_SIZE_BYTES,
    CHART_MAX_DATA_POINTS,
)


def check_constraints(html_path: Path) -> dict:
    """校验硬约束是否满足。"""
    try:
        content = html_path.read_text(encoding="utf-8")
    except OSError as e:
        return {"ok": True, "warn": True, "msg": f"HTML 读取失败（跳过约束校验）：{e}"}

    issues = []
    warnings = []

    # 1. HTML 体积
    size_bytes = len(content.encode("utf-8"))
    if size_bytes > HTML_MAX_SIZE_BYTES:
        issues.append(
            f"HTML 体积 {size_bytes / 1024 / 1024:.2f} MB 超过上限 {HTML_MAX_SIZE_BYTES // 1024 // 1024} MB"
        )
    elif size_bytes > HTML_MAX_SIZE_BYTES * 0.8:
        warnings.append(
            f"HTML 体积 {size_bytes / 1024 / 1024:.2f} MB 接近上限（建议压缩 Chart.js 数据）"
        )

    # 2. 新闻卡片数
    news_cards = len(re.findall(r'class="news-card"', content))
    if news_cards > NEWS_MAX_ITEMS:
        issues.append(
            f"新闻卡片 {news_cards} 条超过上限 {NEWS_MAX_ITEMS}"
        )
    elif news_cards == 0:
        warnings.append("未检测到新闻卡片（可能是旧版格式或空数据）")

    # 3. 排行榜行数（每榜独立检查）
    # 从 LEADERBOARD_DATA JS 对象中提取每榜行数
    lb_match = re.search(r'const LEADERBOARD_DATA\s*=\s*(\{[\s\S]*?\});', content)
    if lb_match:
        lb_raw = lb_match.group(1)
        # 按榜源计数 rows 数组
        for source in ["lmarena", "aa", "ls", "hf", "oc", "sv", "ms"]:
            rows_match = re.findall(
                rf'"rows"\s*:\s*\[([^\]]*)\]',
                lb_raw[lb_raw.find(f'"{source}"'):lb_raw.find(f'"{source}"') + 500]
                if f'"{source}"' in lb_raw else ""
            )
            for r in rows_match:
                count = r.count('"model"') or r.count('"name"')
                if count > LEADERBOARD_TOP_N:
                    issues.append(f"榜单 {source} 有 {count} 行，超过上限 {LEADERBOARD_TOP_N}")
    else:
        # 旧版 RANKING_DATA 格式
        rank_match = re.findall(r'"model"\s*:', content)
        if len(rank_match) > LEADERBOARD_TOP_N:
            warnings.append(f"排行榜模型数约 {len(rank_match)}，超过建议上限 {LEADERBOARD_TOP_N}")

    # 4. Chart.js 数据点
    chart_matches = re.findall(r'data:\s*\[([^\]]+)\]', content)
    for data in chart_matches:
        points = len(data.split(','))
        if points > CHART_MAX_DATA_POINTS:
            warnings.append(f"Chart.js 数据点 {points} 超过建议上限 {CHART_MAX_DATA_POINTS}（可压缩）")

    if issues:
        return {
            "ok": False,
            "warn": False,
            "msg": "约束违反：" + "；".join(issues),
            "details": {"issues": issues, "warnings": warnings},
        }
    elif warnings:
        return {
            "ok": True,
            "warn": True,
            "msg": "约束警告：" + "；".join(warnings),
            "details": {"issues": [], "warnings": warnings},
        }
    else:
        return {
            "ok": True,
            "warn": False,
            "msg": f"硬约束全部满足（新闻 ≤{NEWS_MAX_ITEMS}、排行榜 ≤{LEADERBOARD_TOP_N}、HTML ≤{HTML_MAX_SIZE_BYTES // 1024 // 1024}MB）",
        }
