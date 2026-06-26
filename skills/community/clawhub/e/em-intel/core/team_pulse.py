"""Team pulse metrics: quiet engineers, MR trends, and cycle times."""

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple

from adapters.base import MergeRequest


def get_quiet_engineers(
    mrs: List[MergeRequest],
    members: List[str],
    days: int = 10,
) -> List[str]:
    """Find engineers with zero MRs in the last N days.

    Args:
        mrs: All merge requests in the lookback period.
        members: Known team member names/usernames.
        days: How many days of silence counts as "quiet".

    Returns:
        List of engineer names with no MR activity.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    active = {
        mr.author
        for mr in mrs
        if mr.created_at >= cutoff or (mr.merged_at and mr.merged_at >= cutoff)
    }
    return [m for m in members if m not in active]


def get_mr_trends(mrs: List[MergeRequest]) -> Dict[str, Dict[str, int | float]]:
    """Compare current 7-day MR count vs prior 7-day count per author.

    Returns:
        Dict mapping author → {"current": int, "prior": int, "change_pct": float}
    """
    now = datetime.now(timezone.utc)
    current_start = now - timedelta(days=7)
    prior_start = now - timedelta(days=14)

    trends: Dict[str, Dict[str, int | float]] = {}

    for mr in mrs:
        author = mr.author
        if author not in trends:
            trends[author] = {"current": 0, "prior": 0, "change_pct": 0.0}

        if mr.created_at >= current_start:
            trends[author]["current"] += 1
        elif mr.created_at >= prior_start:
            trends[author]["prior"] += 1

    # Calculate percentage change
    for author, data in trends.items():
        prior = data["prior"]
        current = data["current"]
        if prior > 0:
            data["change_pct"] = round(((current - prior) / prior) * 100, 1)
        elif current > 0:
            data["change_pct"] = 100.0
        else:
            data["change_pct"] = 0.0

    return trends


def get_cycle_times(mrs: List[MergeRequest]) -> Dict[str, float]:
    """Calculate average hours from MR open to merge per engineer.

    Only considers merged MRs with valid timestamps.

    Returns:
        Dict mapping author → average cycle time in hours.
    """
    totals: Dict[str, List[float]] = defaultdict(list)

    for mr in mrs:
        if mr.state == "merged" and mr.merged_at:
            hours = (mr.merged_at - mr.created_at).total_seconds() / 3600
            if hours >= 0:
                totals[mr.author].append(hours)

    return {
        author: round(sum(times) / len(times), 1)
        for author, times in totals.items()
        if times
    }


def get_cycle_time_trend(mrs: List[MergeRequest]) -> Tuple[float, float]:
    """Compare average cycle time this week vs last week.

    Returns:
        (this_week_avg_hours, last_week_avg_hours)
    """
    now = datetime.now(timezone.utc)
    this_week_start = now - timedelta(days=7)
    last_week_start = now - timedelta(days=14)

    this_week: List[float] = []
    last_week: List[float] = []

    for mr in mrs:
        if mr.state != "merged" or not mr.merged_at:
            continue
        hours = (mr.merged_at - mr.created_at).total_seconds() / 3600
        if hours < 0:
            continue
        if mr.merged_at >= this_week_start:
            this_week.append(hours)
        elif mr.merged_at >= last_week_start:
            last_week.append(hours)

    tw_avg = round(sum(this_week) / len(this_week), 1) if this_week else 0.0
    lw_avg = round(sum(last_week) / len(last_week), 1) if last_week else 0.0
    return tw_avg, lw_avg
