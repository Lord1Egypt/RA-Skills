"""Utilities for code review automation."""

from typing import Any
from datetime import datetime


def format_datetime(dt: Any) -> str:
    """Format datetime for display.

    Args:
        dt: Datetime object

    Returns:
        Formatted datetime string
    """
    if dt is None:
        return "N/A"

    if isinstance(dt, str):
        return dt

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_number(num: int) -> str:
    """Format number with thousands separator.

    Args:
        num: Number to format

    Returns:
        Formatted number string
    """
    return f"{num:,}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length-3] + "..."


def calculate_review_score(info: dict) -> float:
    """Calculate a simple review score based on PR stats.

    Args:
        info: PR information dictionary

    Returns:
        Review score (0-100)
    """
    score = 100.0

    # Deduct points for large changes
    changed_files = info.get("changed_files", 0)
    if changed_files > 50:
        score -= 10
    elif changed_files > 20:
        score -= 5

    # Deduct points for many deletions
    deletions = info.get("deletions", 0)
    if deletions > 500:
        score -= 10
    elif deletions > 200:
        score -= 5

    # Bonus for small changes
    if changed_files < 5 and deletions < 50:
        score += 5

    return max(0, min(100, score))
