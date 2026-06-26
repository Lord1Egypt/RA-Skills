"""Map feature branches to ticket IDs and engineer contributions.

The key insight: feature branches often contain ticket IDs (e.g., feature/EEH-123-add-widget).
By parsing branch names with regex, we can automatically map engineer activity to tickets
without requiring manual time tracking.
"""

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional

from adapters.base import Branch, CodeAdapter, Ticket, TicketAdapter

TICKET_PATTERN = re.compile(r"([A-Z]+-\d+)")


@dataclass
class Contribution:
    ticket_id: str
    ticket_title: str
    ticket_status: str
    branch_name: str
    days_active: int
    engineer: str
    status: str  # "active" or "merged"


def extract_ticket_id(branch_name: str) -> Optional[str]:
    """Extract a Jira-style ticket ID from a branch name.

    Matches patterns like EEH-123, PROJ-456, ABC-1.
    Returns the first match or None.
    """
    match = TICKET_PATTERN.search(branch_name.upper().replace("/", "-").replace("_", "-"))
    if match:
        return match.group(1)
    # Also try the original name (branches like feature/EEH-123-description)
    match = TICKET_PATTERN.search(branch_name)
    return match.group(1) if match else None


def map_branches_to_tickets(
    branches: List[Branch],
    tickets: List[Ticket],
) -> Dict[str, List[Contribution]]:
    """Map branches to tickets, grouped by engineer.

    Returns a dict: engineer_name → list of Contribution objects.
    """
    ticket_lookup = {t.key: t for t in tickets}
    now = datetime.now(timezone.utc)
    contributions: Dict[str, List[Contribution]] = {}

    for branch in branches:
        ticket_id = extract_ticket_id(branch.name)
        if not ticket_id:
            continue

        ticket = ticket_lookup.get(ticket_id)
        start = branch.created_at or branch.last_commit_at
        days_active = (now - start).days

        contribution = Contribution(
            ticket_id=ticket_id,
            ticket_title=ticket.title if ticket else "(unknown ticket)",
            ticket_status=ticket.status if ticket else "Unknown",
            branch_name=branch.name,
            days_active=days_active,
            engineer=branch.author,
            status="active",
        )

        contributions.setdefault(branch.author, []).append(contribution)

    return contributions


def get_contributions(
    code_adapter: CodeAdapter,
    ticket_adapter: TicketAdapter,
    project_keys: List[str],
    days: int = 30,
    engineer: Optional[str] = None,
) -> Dict[str, List[Contribution]]:
    """High-level: fetch branches + tickets, map them, optionally filter by engineer."""
    branches = code_adapter.get_branches(days=days)
    tickets = ticket_adapter.get_tickets(project_keys)
    all_contributions = map_branches_to_tickets(branches, tickets)

    if engineer:
        # Case-insensitive match
        filtered = {
            k: v
            for k, v in all_contributions.items()
            if engineer.lower() in k.lower()
        }
        return filtered
    return all_contributions
