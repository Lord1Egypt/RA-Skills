#!/usr/bin/env python3
"""
Date filter for airdrop articles.
Filters out articles older than a specified number of days.

Usage:
  python date_filter.py --days 3 --input articles.json --output filtered.json
"""

import json
import argparse
from datetime import datetime, timezone, timedelta


def is_within_days(date_str: str, max_days: int) -> bool:
    """
    Check if a date string is within the last `max_days` days.

    Args:
        date_str: ISO 8601 date string (e.g., "2026-04-13T10:30:00Z")
        max_days: Maximum age in days

    Returns:
        True if the date is within the window, False otherwise
    """
    try:
        # Parse ISO 8601 date
        article_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age = now - article_date
        return age.days <= max_days
    except (ValueError, TypeError):
        # If date cannot be parsed, include the article by default
        # (better to show stale info than miss opportunities)
        return True


def is_future_date(date_str: str) -> bool:
    """
    Check if a date is in the future.

    Note: Future-dated articles are ALLOWED through the filter intentionally.
    Some airdrop announcements have future dates for:
    - Scheduled snapshot dates
    - Upcoming claim windows
    - Future deadline announcements
    These are valid signals that should not be filtered out.

    Args:
        date_str: ISO 8601 date string

    Returns:
        True if the date is in the future, False otherwise
    """
    try:
        article_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return article_date > now
    except (ValueError, TypeError):
        return False


def filter_articles(articles: list, max_days: int) -> list:
    """
    Filter articles by date, keeping only those within max_days.

    Future-dated articles are intentionally kept (see is_future_date docstring).

    Args:
        articles: List of article dicts with 'date' field
        max_days: Maximum age in days

    Returns:
        Filtered list of articles
    """
    filtered = []
    for article in articles:
        date_str = article.get("date", "")
        if is_within_days(date_str, max_days):
            filtered.append(article)

    return filtered


def main():
    parser = argparse.ArgumentParser(description="Filter airdrop articles by date")
    parser.add_argument("--days", type=int, default=3, help="Maximum article age in days (default: 3)")
    parser.add_argument("--input", required=True, help="Input JSON file path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        articles = json.load(f)

    result = filter_articles(articles, args.days)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Filtered: {len(articles)} -> {len(result)} articles (max {args.days} days)")


if __name__ == "__main__":
    main()
