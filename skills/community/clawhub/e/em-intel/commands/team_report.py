"""Full team performance report command."""

import os
from typing import List

from rich.console import Console
from rich.table import Table

from adapters.base import CodeAdapter, TicketAdapter
from core.branch_mapper import get_contributions
from core.jira_health import get_open_prs_by_age, get_stale_epics, get_unassigned_tickets
from core.team_pulse import get_cycle_times, get_mr_trends, get_quiet_engineers

console = Console()


def run(
    code_adapter: CodeAdapter,
    ticket_adapter: TicketAdapter,
    project_keys: List[str],
    days: int = 30,
    team_members: List[str] | None = None,
) -> str:
    """Generate a comprehensive team performance report.

    Returns:
        Formatted text report.
    """
    quiet_days = int(os.getenv("EM_QUIET_ENGINEER_DAYS", "10"))
    stale_days = int(os.getenv("EM_STALE_EPIC_DAYS", "14"))

    mrs = code_adapter.get_merge_requests(days=days)
    tickets = ticket_adapter.get_tickets(project_keys)
    epics = ticket_adapter.get_epics(project_keys)

    members = team_members or list(set(m.author for m in mrs))
    merged = [m for m in mrs if m.state == "merged"]
    opened = [m for m in mrs if m.state in ("opened", "open")]

    # Metrics
    trends = get_mr_trends(mrs)
    cycle_times = get_cycle_times(mrs)
    quiet = get_quiet_engineers(mrs, members, days=quiet_days)
    pr_buckets = get_open_prs_by_age(mrs)
    stale = get_stale_epics(epics, days=stale_days)
    unassigned = get_unassigned_tickets(tickets)
    contributions = get_contributions(code_adapter, ticket_adapter, project_keys, days=days)

    # Build output
    lines = [f"# Team Report — Last {days} Days\n"]

    lines.append("## Summary")
    lines.append(f"  - {len(merged)} MRs merged, {len(opened)} open")
    lines.append(f"  - {len(members)} engineers tracked")
    lines.append(f"  - {len(quiet)} quiet engineers (>{quiet_days}d)")
    lines.append(f"  - {len(stale)} stale epics (>{stale_days}d)")
    lines.append(f"  - {len(unassigned)} unassigned tickets")

    lines.append("\n## MR Trends (this week vs last week)")
    for author, trend in sorted(trends.items()):
        sign = "+" if trend["change_pct"] >= 0 else ""
        lines.append(
            f"  - {author}: {trend['current']} current, {trend['prior']} prior "
            f"({sign}{trend['change_pct']}%)"
        )

    lines.append("\n## Cycle Times (avg hours to merge)")
    for author, hours in sorted(cycle_times.items(), key=lambda x: x[1]):
        lines.append(f"  - {author}: {hours}h")

    if quiet:
        lines.append(f"\n## Quiet Engineers (no MR in {quiet_days}d)")
        for name in quiet:
            lines.append(f"  - {name}")

    lines.append(f"\n## Open PR Age Distribution")
    for bucket, bucket_mrs in pr_buckets.items():
        lines.append(f"  - {bucket}: {len(bucket_mrs)} MRs")

    if stale:
        lines.append(f"\n## Stale Epics ({len(stale)})")
        for epic in stale:
            lines.append(
                f"  - [{epic.key}] {epic.title} — {epic.days_since_update}d"
            )

    if contributions:
        lines.append("\n## Branch → Ticket Contributions")
        for engineer, contribs in sorted(contributions.items()):
            lines.append(f"  {engineer}:")
            for c in contribs:
                lines.append(
                    f"    - {c.ticket_id}: {c.ticket_title} "
                    f"({c.days_active}d, {c.ticket_status})"
                )

    text = "\n".join(lines)

    # Rich console output
    console.print(f"\n[bold cyan]Team Report — Last {days} Days[/bold cyan]\n")

    summary_table = Table(title="Summary")
    summary_table.add_column("Metric")
    summary_table.add_column("Value", justify="right")
    summary_table.add_row("MRs Merged", str(len(merged)))
    summary_table.add_row("MRs Open", str(len(opened)))
    summary_table.add_row("Engineers", str(len(members)))
    summary_table.add_row("Quiet Engineers", str(len(quiet)))
    summary_table.add_row("Stale Epics", str(len(stale)))
    summary_table.add_row("Unassigned Tickets", str(len(unassigned)))
    console.print(summary_table)

    if trends:
        trend_table = Table(title="MR Trends")
        trend_table.add_column("Engineer")
        trend_table.add_column("This Week", justify="right")
        trend_table.add_column("Last Week", justify="right")
        trend_table.add_column("Change", justify="right")
        for author, trend in sorted(trends.items()):
            sign = "+" if trend["change_pct"] >= 0 else ""
            trend_table.add_row(
                author,
                str(trend["current"]),
                str(trend["prior"]),
                f"{sign}{trend['change_pct']}%",
            )
        console.print(trend_table)

    if cycle_times:
        ct_table = Table(title="Cycle Times (hours)")
        ct_table.add_column("Engineer")
        ct_table.add_column("Avg Hours", justify="right")
        for author, hours in sorted(cycle_times.items(), key=lambda x: x[1]):
            ct_table.add_row(author, str(hours))
        console.print(ct_table)

    return text
