#!/usr/bin/env python3
"""
summarizer.py — Weekly spending digest generator
Reads stats from logger, generates human-friendly
summary using Claude Haiku
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Path to logger script
SCRIPT_DIR = Path(__file__).parent
LOGGER = SCRIPT_DIR / "logger.py"


def get_stats() -> dict:
    """Get this week's stats from logger"""
    result = subprocess.run(
        ["python3", str(LOGGER), "stats"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return {"count": 0, "total": 0,
                "by_category": {}, "by_method": {}}
    return json.loads(result.stdout)


def get_week_dates() -> str:
    """Get human-readable week range"""
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return f"{start.strftime('%b %d')} – {end.strftime('%b %d, %Y')}"


def format_method_line(by_method: dict) -> str:
    emoji_map = {
        "bkash":  "🔴 bKash",
        "nagad":  "🟠 Nagad",
        "rocket": "🟣 Rocket",
        "cash":   "💵 Cash",
        "other":  "💰 Other",
    }
    lines = []
    for method, amount in sorted(
        by_method.items(), key=lambda x: x[1], reverse=True
    ):
        label = emoji_map.get(method, method.title())
        lines.append(f"  {label}: {amount:.0f}৳")
    return "\n".join(lines)


def generate_with_claude(stats: dict) -> str:
    """Generate digest using Claude Haiku"""

    top_categories = sorted(
        stats["by_category"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    prompt = f"""Generate a friendly weekly spending digest for a Bangladeshi user.
Data:
- Week: {get_week_dates()}
- Total transactions: {stats['count']}
- Total spent: {stats['total']:.0f}৳
- By category: {json.dumps(dict(top_categories), ensure_ascii=False)}
- By method: {json.dumps(stats['by_method'], ensure_ascii=False)}

Rules:
- Use ৳ symbol for amounts
- Max 15 lines total
- Include one practical insight or tip at the end
- Friendly, warm tone — not corporate
- Use emojis sparingly but meaningfully
- The user is likely Bengali, so you can use a word or
  two of Bengali if it feels natural (optional)

Format:
📊 Weekly Spending Digest
{get_week_dates()}

💰 Total: X৳  (N transactions)

📂 Top Categories:
[categories with amounts and % of total]

📱 Payment Methods:
[method breakdown]

💡 Insight: [one specific observation about their spending]
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def generate_simple(stats: dict) -> str:
    """
    Fallback: generate digest without Claude API call.
    Used when API is unavailable.
    """
    total = stats["total"]
    count = stats["count"]
    week = get_week_dates()

    top = sorted(
        stats["by_category"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:4]

    cat_lines = []
    for cat, amount in top:
        pct = (amount / total * 100) if total > 0 else 0
        cat_lines.append(f"  {cat.title():<14} {amount:>6.0f}৳  ({pct:.0f}%)")

    method_lines = format_method_line(stats["by_method"])

    lines = [
        f"📊 Weekly Spending Digest",
        f"{week}",
        f"",
        f"💰 Total: {total:.0f}৳  ({count} transactions)",
        f"",
        f"📂 By Category:",
    ] + cat_lines + [
        f"",
        f"📱 By Method:",
        method_lines,
    ]

    return "\n".join(lines)


def weekly_digest(use_claude: bool = True) -> str:
    """Main entry point — generate weekly digest"""
    stats = get_stats()

    if stats["count"] == 0:
        return (
            "📊 No transactions logged this week yet.\n"
            "Start tracking by sending your first expense!\n"
            "Example: 'bkash 450 lunch' or '৳১২০০ বিকাশ বিল'"
        )

    if use_claude:
        try:
            return generate_with_claude(stats)
        except Exception:
            pass  # Fall back to simple version

    return generate_simple(stats)


if __name__ == "__main__":
    # Allow --no-claude flag for offline/testing use
    use_claude = "--no-claude" not in sys.argv
    print(weekly_digest(use_claude=use_claude))
