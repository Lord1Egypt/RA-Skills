#!/usr/bin/env python3
"""
Amazon Review Analyzer
Analyzes review patterns: sentiment distribution, common themes, and risk flags.
Generates structured review health report.

Usage:
    python review-analyzer.py --total 150 --negative 12 --avg-rating 4.2 \
        --themes "quality:3,shipping:5,description:2,size:1,packaging:1"
"""

import argparse
import json
import sys
from datetime import datetime


SENTIMENT_THRESHOLDS = {
    "green": (0, 5),     # Healthy
    "yellow": (5, 12),   # Needs attention
    "red": (12, 100),    # Critical
}

RATING_THRESHOLDS = {
    "green": (4.3, 5.0),
    "yellow": (3.8, 4.3),
    "red": (0, 3.8),
}

THEME_RISK_LEVELS = {
    "quality": "high",
    "safety": "critical",
    "description": "medium",
    "shipping": "low",
    "packaging": "low",
    "size": "medium",
    "authenticity": "critical",
    "counterfeit": "critical",
    "warranty": "medium",
    "customer_service": "medium",
}


def analyze_review_health(total: int, negative: int, avg_rating: float,
                           themes: dict, recent_trend: str = "stable") -> dict:
    """Analyze overall review health."""
    negative_rate = round((negative / max(total, 1)) * 100, 1)

    # Sentiment classification
    for level, (low, high) in SENTIMENT_THRESHOLDS.items():
        if low <= negative_rate < high:
            sentiment_level = level
            break
    else:
        sentiment_level = "red"

    # Rating classification
    for level, (low, high) in RATING_THRESHOLDS.items():
        if low <= avg_rating <= high:
            rating_level = level
            break
    else:
        rating_level = "red"

    # Theme risk analysis
    theme_analysis = []
    for theme, count in themes.items():
        risk = THEME_RISK_LEVELS.get(theme, "medium")
        theme_analysis.append({
            "theme": theme,
            "count": count,
            "risk_level": risk,
            "pct_of_negative": round((count / max(negative, 1)) * 100, 1),
        })

    # Sort by risk then count
    risk_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    theme_analysis.sort(key=lambda x: (risk_order.get(x["risk_level"], 2), -x["count"]))

    # Overall score
    score = 60
    if sentiment_level == "green":
        score += 25
    elif sentiment_level == "yellow":
        score += 10
    else:
        score -= 15

    if rating_level == "green":
        score += 15
    elif rating_level == "yellow":
        score += 5
    else:
        score -= 10

    critical_themes = [t for t in theme_analysis if t["risk_level"] == "critical"]
    if critical_themes:
        score -= len(critical_themes) * 5

    score = max(0, min(100, score))
    level = "red" if score < 50 else ("yellow" if score < 75 else "green")

    # Action recommendations
    actions = []
    if negative_rate > 12:
        actions.append("URGENT: Negative rate above 12% — audit recent 1-2 star reviews for patterns")
    if avg_rating < 3.8:
        actions.append("Rating below 3.8 — investigate root cause, consider product improvement")
    if critical_themes:
        for ct in critical_themes:
            actions.append(f"CRITICAL: '{ct['theme']}' theme has {ct['count']} complaints — may need listing correction or product fix")
    if negative_rate > 5 and negative_rate < 12:
        actions.append("Monitor negative trend — set up weekly review tracking")
    if recent_trend == "worsening":
        actions.append("Worsening trend detected — investigate recent negative spike")

    return {
        "score": score,
        "level": level,
        "total_reviews": total,
        "negative_reviews": negative,
        "negative_rate": negative_rate,
        "avg_rating": avg_rating,
        "sentiment_level": sentiment_level,
        "rating_level": rating_level,
        "theme_analysis": theme_analysis,
        "actions": actions,
        "recent_trend": recent_trend,
    }


def format_report(result: dict) -> str:
    level_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
    risk_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}

    lines = []
    lines.append("💬 评论健康报告")
    lines.append("━" * 40)
    lines.append(f"总评论：{result['total_reviews']} | 差评：{result['negative_reviews']} | 差评率：{result['negative_rate']}%")
    lines.append(f"平均评分：{result['avg_rating']} | 趋势：{result['recent_trend']}")
    lines.append(f"综合评分：{level_emoji.get(result['level'], '⚪')} {result['score']}/100")
    lines.append("")

    lines.append("📊 情绪分布：")
    se = level_emoji.get(result['sentiment_level'], '⚪')
    re = level_emoji.get(result['rating_level'], '⚪')
    lines.append(f"  差评率：{se} {result['negative_rate']}%")
    lines.append(f"  评分：{re} {result['avg_rating']}")
    lines.append("")

    if result["theme_analysis"]:
        lines.append("🏷️ 差评主题分布：")
        for t in result["theme_analysis"]:
            re = risk_emoji.get(t["risk_level"], "⚪")
            lines.append(f"  {re} {t['theme']}：{t['count']}条（{t['pct_of_negative']}%）— 风险：{t['risk_level']}")
        lines.append("")

    if result["actions"]:
        lines.append("⚡ 行动建议：")
        for a in result["actions"]:
            lines.append(f"  → {a}")

    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Amazon Review Analyzer")
    parser.add_argument("--total", type=int, required=True)
    parser.add_argument("--negative", type=int, required=True)
    parser.add_argument("--avg-rating", type=float, required=True)
    parser.add_argument("--themes", required=True, help="theme:count pairs, comma-separated")
    parser.add_argument("--trend", default="stable", choices=["improving", "stable", "worsening"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--input", type=str)

    args = parser.parse_args()
    if args.input:
        params = json.loads(args.input)
        themes = params.get("themes", {})
    else:
        themes = {}
        for pair in args.themes.split(","):
            if ":" in pair:
                k, v = pair.split(":", 1)
                themes[k.strip()] = int(v.strip())

    result = analyze_review_health(
        params.get("total", args.total) if args.input else args.total,
        params.get("negative", args.negative) if args.input else args.negative,
        params.get("avg_rating", args.avg_rating) if args.input else args.avg_rating,
        themes,
        params.get("trend", args.trend) if args.input else args.trend,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
