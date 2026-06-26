"""Jira/ticket health checks: stale epics, unassigned tickets, PR age buckets."""

from datetime import datetime, timedelta, timezone
from typing import Dict, List

from adapters.base import Epic, MergeRequest, Ticket


def get_stale_epics(epics: List[Epic], days: int = 14) -> List[Epic]:
    """Find epics not updated in the last N days that aren't Done/Closed.

    Args:
        epics: List of epics (already filtered to non-closed by adapter).
        days: Threshold for staleness.

    Returns:
        Epics where days_since_update >= days.
    """
    return [e for e in epics if e.days_since_update >= days]


def get_unassigned_tickets(tickets: List[Ticket]) -> List[Ticket]:
    """Find open tickets with no assignee.

    Returns:
        Tickets where assignee is None and status suggests they're open.
    """
    closed_statuses = {"done", "closed", "resolved", "cancelled"}
    return [
        t
        for t in tickets
        if t.assignee is None and t.status.lower() not in closed_statuses
    ]


def get_open_prs_by_age(mrs: List[MergeRequest]) -> Dict[str, List[MergeRequest]]:
    """Group open MRs into age buckets: <1d, 1-3d, >3d.

    Returns:
        Dict with keys "<1d", "1-3d", ">3d" mapping to MR lists.
    """
    now = datetime.now(timezone.utc)
    buckets: Dict[str, List[MergeRequest]] = {"<1d": [], "1-3d": [], ">3d": []}

    for mr in mrs:
        if mr.state not in ("opened", "open"):
            continue
        age = now - mr.created_at
        if age < timedelta(days=1):
            buckets["<1d"].append(mr)
        elif age < timedelta(days=3):
            buckets["1-3d"].append(mr)
        else:
            buckets[">3d"].append(mr)

    return buckets
