"""Morning briefing command: yesterday's merges, aging PRs, quiet engineers, stale epics."""

import os
from datetime import datetime, timedelta, timezone
from typing import List

from rich.console import Console
from rich.table import Table

from adapters.base import CodeAdapter, TicketAdapter
from core.jira_health import get_open_prs_by_age, get_stale_epics, get_unassigned_tickets
from core.team_pulse import get_quiet_engineers

console = Console()


def run(
    code_adapter: CodeAdapter,
    ticket_adapter: TicketAdapter,
    project_keys: List[str],
    team_members: List[str] | None = None,
) -> str:
    """Generate the morning briefing.

    Returns:
        Formatted text report (also printed to console with rich).
    """
    quiet_days = int(os.getenv("EM_QUIET_ENGINEER_DAYS", "7"))
    stale_days = int(os.getenv("EM_STALE_EPIC_DAYS", "14"))

    mrs = code_adapter.get_merge_requests(days=30)
    tickets = ticket_adapter.get_tickets(project_keys)
    epics = ticket_adapter.get_epics(project_keys)

    now = datetime.now(timezone.utc)
    yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0)

    # 1. Merged yesterday
    merged_yesterday = [
        m for m in mrs
        if m.state == "merged" and m.merged_at and m.merged_at >= yesterday_start
    ]

    # 2. Open PRs > 3 days
    pr_buckets = get_open_prs_by_age(mrs)
    old_prs = pr_buckets[">3d"]

    # 3. Quiet engineers
    members = team_members or list(set(m.author for m in mrs))
    quiet = get_quiet_engineers(mrs, members, days=quiet_days)

    # 4. Stale epics
    stale = get_stale_epics(epics, days=stale_days)

    # 5. Unassigned tickets
    unassigned = get_unassigned_tickets(tickets)

    # Build output
    lines = [f"# Morning Brief — {now.strftime('%Y-%m-%d')}\n"]

    lines.append(f"## Merged Yesterday ({len(merged_yesterday)})")
    if merged_yesterday:
        for mr in merged_yesterday:
            lines.append(f"  - [{mr.id}] {mr.title} by {mr.author}")
    else:
        lines.append("  (none)")

    lines.append(f"\n## Open PRs >3 Days ({len(old_prs)})")
    if old_prs:
        for mr in old_prs:
            age = (now - mr.created_at).days
            lines.append(f"  - [{mr.id}] {mr.title} by {mr.author} ({age}d old)")
    else:
        lines.append("  (none)")

    lines.append(f"\n## Quiet Engineers ({len(quiet)})")
    if quiet:
        for name in quiet:
            lines.append(f"  - {name} — no MR in {quiet_days}d")
    else:
        lines.append("  (all active)")

    lines.append(f"\n## Stale Epics ({len(stale)})")
    if stale:
        for epic in stale:
            lines.append(
                f"  - [{epic.key}] {epic.title} — {epic.days_since_update}d since update"
            )
    else:
        lines.append("  (none)")

    lines.append(f"\n## Unassigned Tickets ({len(unassigned)})")
    if unassigned:
        for t in unassigned[:15]:
            lines.append(f"  - [{t.key}] {t.title} ({t.priority})")
        if len(unassigned) > 15:
            lines.append(f"  ... and {len(unassigned) - 15} more")
    else:
        lines.append("  (none)")

    text = "\n".join(lines)

    # Rich console output
    console.print(f"\n[bold cyan]Morning Brief — {now.strftime('%Y-%m-%d')}[/bold cyan]\n")

    if merged_yesterday:
        table = Table(title="Merged Yesterday")
        table.add_column("ID", style="dim")
        table.add_column("Title")
        table.add_column("Author", style="green")
        for mr in merged_yesterday:
            table.add_row(mr.id, mr.title, mr.author)
        console.print(table)

    if old_prs:
        table = Table(title="Open PRs >3 Days", style="red")
        table.add_column("ID", style="dim")
        table.add_column("Title")
        table.add_column("Author")
        table.add_column("Age", justify="right")
        for mr in old_prs:
            age = (now - mr.created_at).days
            table.add_row(mr.id, mr.title, mr.author, f"{age}d")
        console.print(table)

    if quiet:
        console.print(f"\n[yellow]Quiet Engineers ({quiet_days}d):[/yellow] {', '.join(quiet)}")

    if stale:
        console.print(f"\n[red]Stale Epics ({stale_days}d):[/red]")
        for epic in stale:
            console.print(f"  {epic.key}: {epic.title} ({epic.days_since_update}d)")

    return text
