#!/usr/bin/env python3
"""
Amazon Listing Analyzer
Analyzes listing quality across 5 dimensions: title, bullets, description, keywords, Rufus-fit.
Generates structured scoring report with optimization recommendations.

Usage:
    python listing-analyze.py --title "Wireless Bluetooth Earbuds" \
        --bullets "1. Premium Sound Quality|2. 30H Battery|3. IPX7 Waterproof|4. Touch Control|5. Fast Charging" \
        --category "Electronics > Headphones" --lang en

    python listing-analyze.py --input '{"title":"...","bullets":["...","..."],"category":"..."}'
"""

import argparse
import json
import sys
from datetime import datetime


# ── Benchmarks ───────────────────────────────────────────────────

TITLE_LENGTH = {"min": 80, "optimal_min": 120, "optimal_max": 200, "max": 250}
BULLET_COUNT = {"min": 3, "optimal": 5, "max": 5}
BULLET_LENGTH = {"min": 80, "optimal_min": 150, "optimal_max": 500}

PROHIBITED_WORDS_EN = [
    "best", "#1", "number one", "guaranteed", "free shipping",
    "100%", "cheap", "discount", "sale", "promotion",
    "top rated", "best seller", "amazon choice", "amazon's choice",
]

RUFUS_KEYWORD_PATTERNS = [
    "for", "with", "without", "compatible", "fits", "suitable",
    "ideal for", "perfect for", "designed for", "made for",
    "outdoor", "indoor", "travel", "home", "office", "gym",
    "kids", "women", "men", "senior", "beginner", "professional",
]


# ── Analysis Functions ───────────────────────────────────────────

def analyze_title(title: str) -> dict:
    """Score listing title quality."""
    issues = []
    score = 50  # Base

    length = len(title)

    # Length scoring
    if length < TITLE_LENGTH["min"]:
        score -= 20
        issues.append(f"Title too short ({length} chars) — minimum {TITLE_LENGTH['min']} chars for index coverage")
    elif TITLE_LENGTH["optimal_min"] <= length <= TITLE_LENGTH["optimal_max"]:
        score += 25
    elif length > TITLE_LENGTH["max"]:
        score -= 15
        issues.append(f"Title may be truncated on mobile ({length} chars) — keep under {TITLE_LENGTH['max']}")
    else:
        score += 10

    # Prohibited word check
    title_lower = title.lower()
    found_prohibited = [w for w in PROHIBITED_WORDS_EN if w in title_lower]
    if found_prohibited:
        score -= 25
        issues.append(f"Contains prohibited/marketing words: {', '.join(found_prohibited)}")

    # Rufus keyword coverage
    rufus_matches = [p for p in RUFUS_KEYWORD_PATTERNS if p in title_lower]
    if rufus_matches:
        score += min(len(rufus_matches) * 5, 20)
    else:
        issues.append("Missing usage-scenario keywords for Rufus/Rufus AI optimization")

    # Capital word count (brand + key terms)
    words = title.split()
    capitalized = sum(1 for w in words if w[0].isupper())
    if capitalized < 2:
        score -= 5
        issues.append("Ensure brand name and key terms are capitalized")

    score = max(0, min(100, score))
    level = "red" if score < 50 else ("yellow" if score < 75 else "green")
    return {"score": score, "level": level, "issues": issues, "length": length}


def analyze_bullets(bullets: list) -> dict:
    """Score bullet points quality."""
    issues = []
    score = 40  # Base

    count = len(bullets)

    # Count scoring
    if count >= BULLET_COUNT["optimal"]:
        score += 20
    elif count >= BULLET_COUNT["min"]:
        score += 10
    else:
        score -= 15
        issues.append(f"Only {count} bullet points — use all {BULLET_COUNT['optimal']} slots")

    # Average length
    avg_len = sum(len(b) for b in bullets) / max(count, 1)
    if avg_len < BULLET_LENGTH["min"]:
        score -= 10
        issues.append(f"Bullet points too short (avg {avg_len:.0f} chars) — expand to {BULLET_LENGTH['optimal_min']}+ chars")
    elif BULLET_LENGTH["optimal_min"] <= avg_len <= BULLET_LENGTH["optimal_max"]:
        score += 15
    elif avg_len > BULLET_LENGTH["optimal_max"]:
        score += 5
        issues.append("Bullet points may be too long for mobile — consider condensing")

    # Check for benefit-driven language
    benefit_words = ["easy", "perfect", "ideal", "ensure", "protect", "enhance", "improve", "save", "enjoy"]
    has_benefits = any(any(bw in b.lower() for bw in benefit_words) for b in bullets)
    if has_benefits:
        score += 10
    else:
        issues.append("Add benefit-driven language — explain what the customer gains, not just features")

    # Check for numbers/stats
    has_numbers = any(any(c.isdigit() for c in b) for b in bullets)
    if has_numbers:
        score += 10
    else:
        issues.append("Include specific numbers/stats in bullet points (e.g., battery hours, dimensions)")

    # Prohibited words in bullets
    for i, b in enumerate(bullets):
        b_lower = b.lower()
        found = [w for w in PROHIBITED_WORDS_EN if w in b_lower]
        if found:
            score -= 15
            issues.append(f"Bullet #{i+1} contains prohibited words: {', '.join(found)}")

    score = max(0, min(100, score))
    level = "red" if score < 50 else ("yellow" if score < 75 else "green")
    return {"score": score, "level": level, "issues": issues, "count": count, "avg_length": round(avg_len)}


def analyze_keywords(title: str, bullets: list, category: str) -> dict:
    """Estimate keyword coverage quality."""
    issues = []
    score = 50

    # Combine all text
    all_text = (title + " " + " ".join(bullets)).lower()
    total_words = len(all_text.split())

    # Unique word ratio (higher = more diverse keywords)
    unique_words = len(set(all_text.split()))
    diversity_ratio = unique_words / max(total_words, 1)

    if diversity_ratio > 0.7:
        score += 15
    elif diversity_ratio > 0.5:
        score += 10
    else:
        issues.append("Low keyword diversity — text may be repetitive")

    # Rufus scenario keywords
    scenario_matches = sum(1 for p in RUFUS_KEYWORD_PATTERNS if p in all_text)
    if scenario_matches >= 3:
        score += 20
    elif scenario_matches >= 1:
        score += 10
    else:
        issues.append("No usage-scenario keywords detected — add 'for [use case]' patterns")

    # Category keyword presence
    if category:
        cat_words = category.lower().split()
        cat_present = sum(1 for w in cat_words if w in all_text)
        if cat_present >= len(cat_words) * 0.5:
            score += 10
        else:
            issues.append("Category-relevant keywords may be missing from listing text")

    score = max(0, min(100, score))
    level = "red" if score < 50 else ("yellow" if score < 75 else "green")
    return {"score": score, "level": level, "issues": issues, "scenario_keyword_count": scenario_matches}


def analyze_rufus_fit(title: str, bullets: list) -> dict:
    """Score Rufus AI search compatibility."""
    issues = []
    score = 30  # Lower base — Rufus requires intentional optimization

    all_text = (title + " " + " ".join(bullets)).lower()

    # Usage scenario patterns
    scenario_patterns = [
        ("for outdoor", "outdoor use"),
        ("for travel", "travel-friendly"),
        ("for home", "home use"),
        ("for gym", "gym/workout"),
        ("for kids", "children-friendly"),
        ("for office", "office/professional"),
        ("compatible with", "compatibility info"),
        ("fits", "fit/size info"),
    ]

    matched_scenarios = []
    for pattern, label in scenario_patterns:
        if pattern in all_text:
            matched_scenarios.append(label)

    if len(matched_scenarios) >= 2:
        score += 30
    elif len(matched_scenarios) >= 1:
        score += 15
    else:
        issues.append("No usage scenarios detected — Rufus AI relies on 'for [scenario]' patterns")

    # Question-answer format readiness
    qa_indicators = ["how to", "what is", "why", "when to", "where to"]
    has_qa = any(q in all_text for q in qa_indicators)
    if has_qa:
        score += 10
    else:
        issues.append("Consider adding Q&A-style content for Rufus conversational queries")

    # Feature-specific descriptors
    spec_indicators = ["waterproof", "lightweight", "durable", "portable", "rechargeable", "wireless", "adjustable"]
    specs_found = [s for s in spec_indicators if s in all_text]
    score += min(len(specs_found) * 5, 20)

    if not specs_found:
        issues.append("Add specific feature descriptors (waterproof, lightweight, etc.) for Rufus matching")

    score = max(0, min(100, score))
    level = "red" if score < 50 else ("yellow" if score < 75 else "green")
    return {
        "score": score,
        "level": level,
        "issues": issues,
        "matched_scenarios": matched_scenarios,
        "specs_found": specs_found,
    }


def analyze(params: dict) -> dict:
    """Run full 5-dimension listing analysis."""
    title = params.get("title", "")
    bullets_raw = params.get("bullets", [])
    if isinstance(bullets_raw, str):
        bullets = [b.strip() for b in bullets_raw.split("|") if b.strip()]
    else:
        bullets = bullets_raw
    category = params.get("category", "")
    lang = params.get("lang", "en")

    scores = {
        "title": analyze_title(title),
        "bullets": analyze_bullets(bullets),
        "keywords": analyze_keywords(title, bullets, category),
        "rufus_fit": analyze_rufus_fit(title, bullets),
    }

    # Overall score
    total = sum(s["score"] for s in scores.values()) / len(scores)
    total = round(total)

    # Fix priority
    sorted_dims = sorted(scores.items(), key=lambda x: x[1]["score"])
    fix_priority = [{"dimension": dim, **data} for dim, data in sorted_dims]

    return {
        "title": title[:80] + "..." if len(title) > 80 else title,
        "category": category,
        "overall_score": total,
        "scores": scores,
        "fix_priority": fix_priority,
        "timestamp": datetime.now().isoformat(),
    }


def format_report(result: dict) -> str:
    """Format analysis result as readable report."""
    level_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
    dim_cn = {"title": "标题", "bullets": "五点描述", "keywords": "关键词", "rufus_fit": "Rufus适配"}

    lines = []
    lines.append("🩺 Listing诊断报告")
    lines.append("━" * 40)
    lines.append(f"产品：{result['title']}")
    lines.append(f"品类：{result['category']}")
    lines.append(f"综合评分：{result['overall_score']}/100")
    lines.append("")

    lines.append("📊 分项评分：")
    for dim, data in result["scores"].items():
        emoji = level_emoji.get(data["level"], "⚪")
        name = dim_cn.get(dim, dim)
        lines.append(f"  {name}：{emoji} {data['score']}/100")

    lines.append("")
    lines.append("🎯 修复优先级：")
    for i, item in enumerate(result["fix_priority"], 1):
        emoji = level_emoji.get(item["level"], "⚪")
        name = dim_cn.get(item["dimension"], item["dimension"])
        lines.append(f"  {i}. {name}{emoji} ({item['score']}/100)")
        for issue in item.get("issues", [])[:2]:
            lines.append(f"     → {issue}")

    lines.append("")
    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Amazon Listing Analyzer")
    parser.add_argument("--title", required=True, help="Listing title")
    parser.add_argument("--bullets", required=True, help="Bullet points separated by |")
    parser.add_argument("--category", default="", help="Product category path")
    parser.add_argument("--lang", default="en", help="Listing language")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--input", type=str, help="JSON string with all parameters")

    args = parser.parse_args()

    if args.input:
        params = json.loads(args.input)
    else:
        params = {
            "title": args.title,
            "bullets": args.bullets,
            "category": args.category,
            "lang": args.lang,
        }

    result = analyze(params)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
