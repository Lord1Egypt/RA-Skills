#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json

from capital_flow import fetch_market_flow_snapshot
from market_data import fetch_index_snapshot, fetch_sector_movers


def safe_avg(values: list[float | int | None]) -> float | None:
    usable = [float(value) for value in values if value is not None]
    if not usable:
        return None
    return round(sum(usable) / len(usable), 2)


def compute_breadth(indices: list[dict]) -> dict:
    tracked = [item for item in indices if item.get("name") in {"上证指数", "深证成指"}]
    up = sum(int(item.get("up_count") or 0) for item in tracked)
    down = sum(int(item.get("down_count") or 0) for item in tracked)
    total = up + down
    ratio = round(up / total, 4) if total else None
    return {"up": up, "down": down, "ratio": ratio}


def score_breadth(ratio: float | None) -> int:
    if ratio is None:
        return 0
    if ratio >= 0.65:
        return 2
    if ratio >= 0.52:
        return 1
    if ratio <= 0.32:
        return -2
    if ratio <= 0.45:
        return -1
    return 0


def score_main_flow(main_net_yi: float | None) -> int:
    if main_net_yi is None:
        return 0
    if main_net_yi >= 80:
        return 2
    if main_net_yi > 0:
        return 1
    if main_net_yi <= -80:
        return -2
    if main_net_yi < 0:
        return -1
    return 0


def classify_group_tone(group_flow_rows: list[dict]) -> tuple[str, int]:
    tone = "mixed"
    score = 0
    by_name = {row["group"]: row for row in group_flow_rows}
    tech = by_name.get("tech_repair", {})
    defensive = by_name.get("defensive_gauge", {})
    policy = by_name.get("policy_beta", {})

    tech_net = float(tech.get("net_flow_yi") or 0)
    defensive_net = float(defensive.get("net_flow_yi") or 0)
    policy_net = float(policy.get("net_flow_yi") or 0)

    if defensive_net > 0 and tech_net <= 0:
        tone = "defensive"
        score = -1
    elif tech_net > 0 and defensive_net <= 0:
        tone = "growth"
        score = 1
    elif policy_net > 0 and tech_net >= 0:
        tone = "policy-growth"
        score = 1
    return tone, score


def build_sentiment_snapshot(group_flow_rows: list[dict] | None = None) -> dict:
    indices = fetch_index_snapshot()
    top_sectors = fetch_sector_movers(limit=5, rising=True)
    bottom_sectors = fetch_sector_movers(limit=5, rising=False)
    flow_snapshot = fetch_market_flow_snapshot()
    breadth = compute_breadth(indices)
    top_avg = safe_avg([item.get("change_pct") for item in top_sectors])
    bottom_avg = safe_avg([item.get("change_pct") for item in bottom_sectors])

    breadth_score = score_breadth(breadth["ratio"])
    flow_score = score_main_flow(flow_snapshot.get("main_net_yi"))
    dispersion_score = 0
    if top_avg is not None and bottom_avg is not None:
        if top_avg >= 2.5 and bottom_avg <= -2.5:
            dispersion_score = -1
        elif top_avg >= 2.0 and bottom_avg >= -1.0:
            dispersion_score = 1

    group_tone, group_score = classify_group_tone(group_flow_rows or [])
    total_score = breadth_score + flow_score + dispersion_score + group_score

    if group_tone == "defensive" and breadth_score <= 0:
        label = "抱团行情"
        read = "资金更集中在防御和高确定性方向，广度没有同步改善。"
    elif group_tone == "growth" and total_score >= 1:
        label = "科技修复"
        read = "成长方向开始获得资金确认，但仍要看扩散是否持续。"
    elif total_score >= 2:
        label = "修复扩散"
        read = "广度、板块和资金同步改善，情绪修复质量较高。"
    elif total_score <= -2:
        label = "分化偏弱"
        read = "广度和主力资金都偏弱，反弹更像局部脉冲。"
    else:
        label = "分化震荡"
        read = "结构性轮动还在，市场没有给出统一方向。"

    components = [
        {"component": "市场广度", "score": breadth_score, "detail": f"{breadth['up']} / {breadth['down']}"},
        {
            "component": "主力资金",
            "score": flow_score,
            "detail": f"{flow_snapshot.get('main_net_yi')}亿" if flow_snapshot.get("main_net_yi") is not None else "n/a",
        },
        {
            "component": "板块扩散",
            "score": dispersion_score,
            "detail": f"强势板块均值 {top_avg}%，弱势板块均值 {bottom_avg}%",
        },
        {"component": "观察池风格", "score": group_score, "detail": group_tone},
    ]

    return {
        "label": label,
        "read": read,
        "score": total_score,
        "breadth": breadth,
        "market_flow": flow_snapshot,
        "top_sector_avg": top_avg,
        "bottom_sector_avg": bottom_avg,
        "group_tone": group_tone,
        "components": components,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Market sentiment snapshot for A-share Decision Desk.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    snapshot = build_sentiment_snapshot()
    if args.format == "json":
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        return 0
    print("# Market Sentiment")
    print()
    print(f"- state: {snapshot['label']}")
    print(f"- read: {snapshot['read']}")
    print(json.dumps(snapshot["components"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
