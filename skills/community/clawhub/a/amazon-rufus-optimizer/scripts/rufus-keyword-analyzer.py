#!/usr/bin/env python3
"""
Rufus Keyword Analyzer
Analyzes listing content for Rufus AI search compatibility.
Checks scenario keyword coverage, conversational query readiness,
and generates Rufus-optimized keyword suggestions.

Usage:
    python rufus-keyword-analyzer.py --title "..." --bullets "bullet1|bullet2" --category "Electronics"
"""

import argparse
import json
import sys
from datetime import datetime


RUFUS_SCENARIO_PATTERNS = {
    "use_case": {
        "keywords": ["for outdoor", "for indoor", "for travel", "for home", "for office",
                      "for gym", "for kids", "for seniors", "for camping", "for hiking",
                      "for running", "for cooking", "for cleaning", "for work", "for school",
                      "for pets", "for baby", "for car", "for kitchen", "for bathroom"],
        "weight": 3.0,
        "rufus_queries": ["What's good for camping?", "I need something for my home office",
                          "Looking for a gift for my mom", "Best option for travel"],
    },
    "audience": {
        "keywords": ["for men", "for women", "for beginners", "for professional",
                      "for students", "for elderly", "for athletes", "for gamers"],
        "weight": 2.5,
        "rufus_queries": ["Something for my husband", "Gift for elderly parent",
                          "Beginner-friendly option"],
    },
    "situation": {
        "keywords": ["waterproof", "lightweight", "portable", "compact", "durable",
                      "rechargeable", "wireless", "adjustable", "foldable", "noise-cancelling",
                      "breathable", "stainless", "anti-slip", "shockproof", "heat-resistant"],
        "weight": 2.0,
        "rufus_queries": ["I need something waterproof", "Looking for lightweight option",
                          "Portable and easy to carry"],
    },
    "problem_solving": {
        "keywords": ["easy to use", "no assembly", "quick setup", "hassle-free",
                      "save time", "prevent", "protect", "reduce", "eliminate",
                      "upgrade", "improve", "enhance"],
        "weight": 2.0,
        "rufus_queries": ["Something easy to set up", "No complicated assembly",
                          "Saves me time"],
    },
    "comparison": {
        "keywords": ["alternative to", "upgrade from", "compared to standard",
                      "better than basic", "premium version"],
        "weight": 1.5,
        "rufus_queries": ["Better than the basic model?", "Alternative to [brand]?"],
    },
}


def analyze_rufus_coverage(title: str, bullets: list, category: str) -> dict:
    """Analyze Rufus keyword coverage across listing content."""
    all_text = (title + " " + " ".join(bullets)).lower()

    coverage = {}
    total_score = 0
    max_possible = 0

    for group, data in RUFUS_SCENARIO_PATTERNS.items():
        found = [kw for kw in data["keywords"] if kw in all_text]
        missing = [kw for kw in data["keywords"] if kw not in all_text]
        group_score = len(found) / len(data["keywords"]) * data["weight"]
        max_group = data["weight"]

        coverage[group] = {
            "found": found,
            "found_count": len(found),
            "total_count": len(data["keywords"]),
            "coverage_pct": round(len(found) / len(data["keywords"]) * 100, 1),
            "missing_top5": missing[:5],
            "group_score": round(group_score, 2),
            "max_score": max_group,
            "sample_queries": data["rufus_queries"][:3],
        }

        total_score += group_score
        max_possible += max_group

    overall_pct = round((total_score / max_possible) * 100, 1) if max_possible > 0 else 0
    overall_score = min(100, round(overall_pct * 1.5))  # Boost: 66% coverage = 100 score

    # Category-specific suggestions
    category_suggestions = _generate_category_suggestions(category, coverage)

    return {
        "overall_score": overall_score,
        "overall_coverage_pct": overall_pct,
        "category": category,
        "coverage": coverage,
        "suggestions": category_suggestions,
        "total_keywords_found": sum(c["found_count"] for c in coverage.values()),
        "total_keywords_available": sum(c["total_count"] for c in coverage.values()),
    }


def _generate_category_suggestions(category: str, coverage: dict) -> list:
    """Generate category-specific optimization suggestions."""
    suggestions = []

    # Universal suggestions based on gaps
    if coverage.get("use_case", {}).get("found_count", 0) < 2:
        suggestions.append("Add 2-3 'for [scenario]' patterns in title and first two bullets — this is the #1 Rufus signal")

    if coverage.get("audience", {}).get("found_count", 0) == 0:
        suggestions.append("Add target audience keywords — 'for [audience]' helps Rufus match user profiles")

    if coverage.get("situation", {}).get("found_count", 0) < 2:
        suggestions.append("Add situational descriptors (waterproof, lightweight, portable) — Rufus uses these for conditional queries")

    if coverage.get("problem_solving", {}).get("found_count", 0) == 0:
        suggestions.append("Add problem-solving phrases — 'easy to set up', 'saves time' match Rufus 'how do I...' queries")

    # Category-specific
    cat_lower = category.lower() if category else ""
    if "outdoor" in cat_lower or "sport" in cat_lower or "camping" in cat_lower:
        suggestions.append("For outdoor category: emphasize 'weather-resistant', 'for camping/hiking/running' patterns")
    if "electronic" in cat_lower or "tech" in cat_lower:
        suggestions.append("For electronics: add 'compatible with', 'works with', wireless/rechargeable signals")
    if "home" in cat_lower or "kitchen" in cat_lower:
        suggestions.append("For home/kitchen: add 'for daily use', 'easy to clean', 'space-saving' patterns")

    return suggestions


def format_report(result: dict) -> str:
    lines = []
    lines.append("🎯 Rufus关键词覆盖报告")
    lines.append("━" * 40)
    lines.append(f"品类：{result['category']}")
    lines.append(f"Rufus适配评分：{result['overall_score']}/100")
    lines.append(f"关键词覆盖率：{result['overall_coverage_pct']}%")
    lines.append(f"已覆盖：{result['total_keywords_found']}/{result['total_keywords_available']}个关键词")
    lines.append("")

    for group, data in result["coverage"].items():
        status = "🟢" if data["coverage_pct"] > 50 else ("🟡" if data["coverage_pct"] > 20 else "🔴")
        lines.append(f"  {status} {group}：{data['coverage_pct']}% ({data['found_count']}/{data['total_count']})")
        if data["found"]:
            lines.append(f"     ✅ {', '.join(data['found'][:3])}")
        if data["missing_top5"]:
            lines.append(f"     ❌ 缺失：{', '.join(data['missing_top5'])}")
        lines.append(f"     🔍 示例查询：{data['sample_queries'][0]}")
        lines.append("")

    if result["suggestions"]:
        lines.append("💡 优化建议：")
        for s in result["suggestions"]:
            lines.append(f"  → {s}")

    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Rufus Keyword Analyzer")
    parser.add_argument("--title", required=True)
    parser.add_argument("--bullets", required=True, help="Bullet points separated by |")
    parser.add_argument("--category", default="")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--input", type=str)

    args = parser.parse_args()
    if args.input:
        params = json.loads(args.input)
        title = params.get("title", "")
        bullets = params.get("bullets", [])
        if isinstance(bullets, str):
            bullets = [b.strip() for b in bullets.split("|") if b.strip()]
        category = params.get("category", "")
    else:
        title = args.title
        bullets = [b.strip() for b in args.bullets.split("|") if b.strip()]
        category = args.category

    result = analyze_rufus_coverage(title, bullets, category)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
