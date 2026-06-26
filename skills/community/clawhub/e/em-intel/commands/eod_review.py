"""End-of-day review command: today's activity, cycle time trends, new stale epics."""

import os
from datetime import datetime, timezone
from typing import List

from rich.console import Console
from rich.table import Table

from adapters.base import CodeAdapter, TicketAdapter
from core.jira_health import get_stale_epics
from core.team_pulse import get_cycle_time_trend

console = Console()


def run(
    code_adapter: CodeAdapter,
    ticket_adapter: TicketAdapter,
    project_keys: List[str],
) -> str:
    """Generate the end-of-day review.

    Returns:
        Formatted text report.
    """
    stale_days = int(os.getenv("EM_STALE_EPIC_DAYS", "14"))
    mrs = code_adapter.get_merge_requests(days=14)
    epics = ticket_adapter.get_epics(project_keys)

    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # 1. MRs merged today
    merged_today = [
        m for m in mrs
        if m.state == "merged" and m.merged_at and m.merged_at >= today_start
    ]

    # 2. MRs opened today
    opened_today = [
        m for m in mrs
        if m.created_at >= today_start
    ]

    # 3. Engineers who contributed today
    contributors = sorted(set(
        m.author for m in mrs
        if m.created_at >= today_start
        or (m.merged_at and m.merged_at >= today_start)
    ))

    # 4. Cycle time trend
    tw_avg, lw_avg = get_cycle_time_trend(mrs)

    # 5. Stale epics
    stale = get_stale_epics(epics, days=stale_days)

    # Build output
    lines = [f"# EOD Review — {now.strftime('%Y-%m-%d')}\n"]

    lines.append(f"## Merged Today ({len(merged_today)})")
    for mr in merged_today:
        lines.append(f"  - [{mr.id}] {mr.title} by {mr.author}")
    if not merged_today:
        lines.append("  (none)")

    lines.append(f"\n## Opened Today ({len(opened_today)})")
    for mr in opened_today:
        lines.append(f"  - [{mr.id}] {mr.title} by {mr.author}")
    if not opened_today:
        lines.append("  (none)")

    lines.append(f"\n## Contributors Today ({len(contributors)})")
    if contributors:
        lines.append(f"  {', '.join(contributors)}")
    else:
        lines.append("  (none)")

    lines.append(f"\n## Cycle Time")
    lines.append(f"  This week avg: {tw_avg}h")
    lines.append(f"  Last week avg: {lw_avg}h")
    if lw_avg > 0:
        change = round(((tw_avg - lw_avg) / lw_avg) * 100, 1)
        direction = "faster" if change < 0 else "slower"
        lines.append(f"  Trend: {abs(change)}% {direction}")

    lines.append(f"\n## Stale Epics ({len(stale)})")
    for epic in stale:
        lines.append(
            f"  - [{epic.key}] {epic.title} — {epic.days_since_update}d since update"
        )
    if not stale:
        lines.append("  (none)")

    text = "\n".join(lines)

    # Rich console output
    console.print(f"\n[bold cyan]EOD Review — {now.strftime('%Y-%m-%d')}[/bold cyan]\n")

    if merged_today:
        table = Table(title="Merged Today")
        table.add_column("ID", style="dim")
        table.add_column("Title")
        table.add_column("Author", style="green")
        for mr in merged_today:
            table.add_row(mr.id, mr.title, mr.author)
        console.print(table)

    if opened_today:
        table = Table(title="Opened Today")
        table.add_column("ID", style="dim")
        table.add_column("Title")
        table.add_column("Author", style="cyan")
        for mr in opened_today:
            table.add_row(mr.id, mr.title, mr.author)
        console.print(table)

    if contributors:
        console.print(f"\n[green]Contributors:[/green] {', '.join(contributors)}")

    console.print(f"\n[bold]Cycle Time:[/bold] {tw_avg}h this week vs {lw_avg}h last week")

    return text
