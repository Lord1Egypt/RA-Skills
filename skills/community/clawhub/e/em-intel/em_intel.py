#!/usr/bin/env python3
"""em-intel: Engineering Manager Intelligence CLI.

Track team performance, engineer contributions, and project health
across GitLab/GitHub + Jira/GitHub Issues.
"""

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent


def _bootstrap_deps() -> None:
    """Install requirements silently on first run if any are missing."""
    req = SKILL_DIR / "requirements.txt"
    if not req.exists():
        return
    try:
        import importlib
        needed = {"requests", "dotenv", "rich", "jinja2", "markdown"}
        missing = [p for p in needed if not importlib.util.find_spec(p)]
        if missing:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req), "-q"],
                check=False,
                capture_output=True,
            )
    except Exception:
        pass  # Don't block startup


_bootstrap_deps()

import requests  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("em-intel")


def _get_code_adapter(dry_run: bool = False):
    """Create the code platform adapter based on EM_CODE_PROVIDER."""
    if dry_run:
        from adapters.mock_adapter import MockCodeAdapter

        return MockCodeAdapter()
    provider = os.getenv("EM_CODE_PROVIDER", "gitlab").lower()
    if provider == "github":
        from adapters.github_adapter import GitHubAdapter

        return GitHubAdapter()
    else:
        from adapters.gitlab_adapter import GitLabAdapter

        return GitLabAdapter()


def _get_ticket_adapter(dry_run: bool = False):
    """Create the ticket system adapter based on EM_TICKET_PROVIDER."""
    if dry_run:
        from adapters.mock_adapter import MockTicketAdapter

        return MockTicketAdapter()
    provider = os.getenv("EM_TICKET_PROVIDER", "jira").lower()
    if provider == "github_issues":
        from adapters.github_issues_adapter import GitHubIssuesAdapter

        return GitHubIssuesAdapter()
    else:
        from adapters.jira_adapter import JiraAdapter

        return JiraAdapter()


def _get_project_keys() -> list[str]:
    """Get project keys from env."""
    keys = os.getenv("JIRA_PROJECTS", "")
    return [k.strip() for k in keys.split(",") if k.strip()]


def _dry_run_banner(enabled: bool) -> None:
    """Print a banner when dry-run mode is active."""
    if enabled:
        from rich.console import Console

        Console().print(
            "\n[bold yellow]⚠ DRY-RUN MODE — using synthetic mock data[/bold yellow]\n"
        )


# ── doctor ────────────────────────────────────────────────────────────


def cmd_doctor(args: argparse.Namespace) -> None:
    """Check env vars and test API connections."""
    from rich.console import Console

    console = Console()
    checks: list[bool] = []

    console.print("\n[bold cyan]em-intel doctor[/bold cyan]\n")

    # ── Code Platform ────────────────────────────────────────────────
    console.print("[bold]Code Platform[/bold]")
    provider = os.getenv("EM_CODE_PROVIDER", "gitlab").lower()
    console.print(f"  Provider: {provider}")

    if provider == "gitlab":
        env_checks = {
            "GITLAB_URL": os.getenv("GITLAB_URL", ""),
            "GITLAB_TOKEN": os.getenv("GITLAB_TOKEN", ""),
            "GITLAB_GROUP": os.getenv("GITLAB_GROUP", ""),
        }
        for var, val in env_checks.items():
            ok = bool(val)
            checks.append(ok)
            symbol = "✅" if ok else "❌"
            console.print(f"  {symbol} {var}: {'set' if ok else 'MISSING'}")

        if all(env_checks.values()):
            # Test API connection
            from urllib.parse import quote_plus

            url = env_checks["GITLAB_URL"].rstrip("/")
            group = quote_plus(env_checks["GITLAB_GROUP"])
            try:
                resp = requests.get(
                    f"{url}/api/v4/groups/{group}/merge_requests",
                    headers={"PRIVATE-TOKEN": env_checks["GITLAB_TOKEN"]},
                    params={"per_page": 1, "state": "merged"},
                    timeout=15,
                )
                resp.raise_for_status()
                checks.append(True)
                console.print("  ✅ GitLab API: connected")
            except requests.RequestException as exc:
                checks.append(False)
                console.print(f"  ❌ GitLab API: {exc}")
    elif provider == "github":
        env_checks = {
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", ""),
            "GITHUB_ORG": os.getenv("GITHUB_ORG", ""),
            "GITHUB_REPO": os.getenv("GITHUB_REPO", ""),
        }
        for var, val in env_checks.items():
            ok = bool(val)
            checks.append(ok)
            symbol = "✅" if ok else "❌"
            console.print(f"  {symbol} {var}: {'set' if ok else 'MISSING'}")

        if all(env_checks.values()):
            org = env_checks["GITHUB_ORG"]
            repo = env_checks["GITHUB_REPO"]
            try:
                resp = requests.get(
                    f"https://api.github.com/repos/{org}/{repo}",
                    headers={
                        "Authorization": f"Bearer {env_checks['GITHUB_TOKEN']}",
                        "Accept": "application/vnd.github+json",
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                checks.append(True)
                console.print("  ✅ GitHub API: connected")
            except requests.RequestException as exc:
                checks.append(False)
                console.print(f"  ❌ GitHub API: {exc}")

    # ── Ticket System ────────────────────────────────────────────────
    console.print("\n[bold]Ticket System[/bold]")
    ticket_provider = os.getenv("EM_TICKET_PROVIDER", "jira").lower()
    console.print(f"  Provider: {ticket_provider}")

    if ticket_provider == "jira":
        env_checks_t = {
            "JIRA_URL": os.getenv("JIRA_URL", ""),
            "JIRA_EMAIL": os.getenv("JIRA_EMAIL", ""),
            "JIRA_TOKEN": os.getenv("JIRA_TOKEN", ""),
            "JIRA_PROJECTS": os.getenv("JIRA_PROJECTS", ""),
        }
        for var, val in env_checks_t.items():
            ok = bool(val)
            checks.append(ok)
            symbol = "✅" if ok else "❌"
            console.print(f"  {symbol} {var}: {'set' if ok else 'MISSING'}")

        if all(env_checks_t.values()):
            from base64 import b64encode

            jira_url = env_checks_t["JIRA_URL"].rstrip("/")
            creds = b64encode(
                f"{env_checks_t['JIRA_EMAIL']}:{env_checks_t['JIRA_TOKEN']}".encode()
            ).decode()
            project = env_checks_t["JIRA_PROJECTS"].split(",")[0].strip()
            try:
                resp = requests.get(
                    f"{jira_url}/rest/api/3/search/jql",
                    headers={
                        "Authorization": f"Basic {creds}",
                        "Accept": "application/json",
                    },
                    params={
                        "jql": f"project = {project} ORDER BY updated DESC",
                        "maxResults": 1,
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                checks.append(True)
                console.print("  ✅ Jira API: connected")
            except requests.RequestException as exc:
                checks.append(False)
                console.print(f"  ❌ Jira API: {exc}")
    elif ticket_provider == "github_issues":
        console.print("  (uses same GitHub credentials as code platform)")

    # ── Delivery Config ──────────────────────────────────────────────
    console.print("\n[bold]Delivery[/bold]")
    delivery = os.getenv("EM_DELIVERY", "print").lower()
    console.print(f"  Channel: {delivery}")

    if delivery == "telegram":
        for var in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
            ok = bool(os.getenv(var, ""))
            checks.append(ok)
            symbol = "✅" if ok else "❌"
            console.print(f"  {symbol} {var}: {'set' if ok else 'MISSING'}")
    elif delivery == "slack":
        ok = bool(os.getenv("SLACK_WEBHOOK_URL", ""))
        checks.append(ok)
        symbol = "✅" if ok else "❌"
        console.print(f"  {symbol} SLACK_WEBHOOK_URL: {'set' if ok else 'MISSING'}")
    elif delivery == "email":
        for var in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "SMTP_TO"):
            ok = bool(os.getenv(var, ""))
            checks.append(ok)
            symbol = "✅" if ok else "❌"
            console.print(f"  {symbol} {var}: {'set' if ok else 'MISSING'}")
    else:
        checks.append(True)
        console.print("  ✅ print (stdout) — no credentials needed")

    # ── Summary ──────────────────────────────────────────────────────
    passed = sum(checks)
    total = len(checks)
    all_ok = all(checks)

    console.print(f"\n[bold]{'✅' if all_ok else '❌'} {passed}/{total} checks passed[/bold]")
    if not all_ok:
        console.print("[yellow]See SETUP.md for token generation instructions.[/yellow]")

    sys.exit(0 if all_ok else 1)


# ── Commands ──────────────────────────────────────────────────────────


def cmd_morning_brief(args: argparse.Namespace) -> None:
    """Run the morning briefing."""
    from commands.morning_brief import run

    dry_run = getattr(args, "dry_run", False)
    _dry_run_banner(dry_run)
    code = _get_code_adapter(dry_run)
    tickets = _get_ticket_adapter(dry_run)
    text = run(code, tickets, _get_project_keys() or ["EEH"])

    if getattr(args, "send", False):
        from core.delivery import send

        send(text, title="Morning Brief")


def cmd_eod_review(args: argparse.Namespace) -> None:
    """Run the end-of-day review."""
    from commands.eod_review import run

    dry_run = getattr(args, "dry_run", False)
    _dry_run_banner(dry_run)
    code = _get_code_adapter(dry_run)
    tickets = _get_ticket_adapter(dry_run)
    text = run(code, tickets, _get_project_keys() or ["EEH"])

    if getattr(args, "send", False):
        from core.delivery import send

        send(text, title="EOD Review")


def cmd_team_report(args: argparse.Namespace) -> None:
    """Run the full team report."""
    from commands.team_report import run

    dry_run = getattr(args, "dry_run", False)
    _dry_run_banner(dry_run)
    code = _get_code_adapter(dry_run)
    tickets = _get_ticket_adapter(dry_run)
    text = run(code, tickets, _get_project_keys() or ["EEH"], days=args.days)

    if getattr(args, "send", False):
        from core.delivery import send

        send(text, title="Team Report")


def cmd_contributions(args: argparse.Namespace) -> None:
    """Show branch → ticket contribution map."""
    from rich.console import Console
    from rich.table import Table

    from core.branch_mapper import get_contributions

    dry_run = getattr(args, "dry_run", False)
    _dry_run_banner(dry_run)
    console = Console()
    code = _get_code_adapter(dry_run)
    tickets = _get_ticket_adapter(dry_run)
    contribs = get_contributions(
        code, tickets, _get_project_keys() or ["EEH"], days=args.days, engineer=args.engineer
    )

    if not contribs:
        console.print("[yellow]No branch → ticket mappings found.[/yellow]")
        return

    for engineer, items in sorted(contribs.items()):
        table = Table(title=f"Contributions: {engineer}")
        table.add_column("Ticket", style="cyan")
        table.add_column("Title")
        table.add_column("Status")
        table.add_column("Branch", style="dim")
        table.add_column("Days Active", justify="right")
        for c in items:
            table.add_row(c.ticket_id, c.ticket_title, c.ticket_status, c.branch_name, str(c.days_active))
        console.print(table)


def cmd_quiet_engineers(args: argparse.Namespace) -> None:
    """List quiet engineers."""
    from rich.console import Console

    from core.team_pulse import get_quiet_engineers

    dry_run = getattr(args, "dry_run", False)
    _dry_run_banner(dry_run)
    console = Console()
    code = _get_code_adapter(dry_run)
    days = int(os.getenv("EM_QUIET_ENGINEER_DAYS", "10"))
    mrs = code.get_merge_requests(days=30)
    members = list(set(m.author for m in mrs))
    quiet = get_quiet_engineers(mrs, members, days=days)

    if quiet:
        console.print(f"\n[yellow]Quiet engineers (no MR in {days}d):[/yellow]")
        for name in quiet:
            console.print(f"  - {name}")
    else:
        console.print("[green]All engineers are active.[/green]")


def cmd_epic_health(args: argparse.Namespace) -> None:
    """List stale and unassigned epics."""
    from rich.console import Console
    from rich.table import Table

    from core.jira_health import get_stale_epics, get_unassigned_tickets

    dry_run = getattr(args, "dry_run", False)
    _dry_run_banner(dry_run)
    console = Console()
    tickets_adapter = _get_ticket_adapter(dry_run)
    keys = _get_project_keys() or ["EEH"]
    epics = tickets_adapter.get_epics(keys)
    tickets = tickets_adapter.get_tickets(keys)

    stale_days = int(os.getenv("EM_STALE_EPIC_DAYS", "14"))
    stale = get_stale_epics(epics, days=stale_days)
    unassigned = get_unassigned_tickets(tickets)

    if stale:
        table = Table(title=f"Stale Epics (>{stale_days}d)")
        table.add_column("Key", style="red")
        table.add_column("Title")
        table.add_column("Days Stale", justify="right")
        table.add_column("Assignee")
        for epic in stale:
            table.add_row(epic.key, epic.title, str(epic.days_since_update), epic.assignee or "-")
        console.print(table)
    else:
        console.print("[green]No stale epics.[/green]")

    if unassigned:
        table = Table(title="Unassigned Open Tickets")
        table.add_column("Key", style="yellow")
        table.add_column("Title")
        table.add_column("Priority")
        for t in unassigned[:20]:
            table.add_row(t.key, t.title, t.priority)
        if len(unassigned) > 20:
            console.print(f"  ... and {len(unassigned) - 20} more")
        console.print(table)
    else:
        console.print("[green]No unassigned tickets.[/green]")


def cmd_setup(args: argparse.Namespace) -> None:
    """Interactive setup wizard."""
    from commands.setup_wizard import run as run_wizard
    run_wizard()


def cmd_newsletter(args: argparse.Namespace) -> None:
    """Generate and send the weekly newsletter."""
    from commands.newsletter import run

    dry_run = getattr(args, "dry_run", False)
    _dry_run_banner(dry_run)
    code = _get_code_adapter(dry_run)
    tickets = _get_ticket_adapter(dry_run)
    # deliver=False when dry-run so output goes to terminal only
    run(code, tickets, _get_project_keys(), days=args.week * 7 if args.week else 7,
        deliver=not dry_run)


# ── CLI Setup ─────────────────────────────────────────────────────────


def _add_dry_run(parser: argparse.ArgumentParser) -> None:
    """Add --dry-run flag to a subparser."""
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Use synthetic mock data instead of real APIs",
    )


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="em-intel",
        description="Engineering Manager Intelligence — team performance & project health",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # setup
    p_setup = subparsers.add_parser("setup", help="Interactive setup wizard — configure API keys and delivery")
    p_setup.set_defaults(func=cmd_setup)

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Check env vars and test API connections")
    p_doctor.set_defaults(func=cmd_doctor)

    # morning-brief
    p_morning = subparsers.add_parser("morning-brief", help="Morning briefing")
    p_morning.add_argument("--send", action="store_true", help="Send via delivery channel")
    _add_dry_run(p_morning)
    p_morning.set_defaults(func=cmd_morning_brief)

    # eod-review
    p_eod = subparsers.add_parser("eod-review", help="End-of-day review")
    p_eod.add_argument("--send", action="store_true", help="Send via delivery channel")
    _add_dry_run(p_eod)
    p_eod.set_defaults(func=cmd_eod_review)

    # team-report
    p_team = subparsers.add_parser("team-report", help="Full team performance report")
    p_team.add_argument("--days", type=int, default=30, help="Lookback days (default: 30)")
    p_team.add_argument("--send", action="store_true", help="Send via delivery channel")
    _add_dry_run(p_team)
    p_team.set_defaults(func=cmd_team_report)

    # contributions
    p_contrib = subparsers.add_parser("contributions", help="Branch → ticket contribution map")
    p_contrib.add_argument("--engineer", type=str, help="Filter by engineer name")
    p_contrib.add_argument("--days", type=int, default=30, help="Lookback days (default: 30)")
    _add_dry_run(p_contrib)
    p_contrib.set_defaults(func=cmd_contributions)

    # quiet-engineers
    p_quiet = subparsers.add_parser("quiet-engineers", help="List quiet engineers")
    _add_dry_run(p_quiet)
    p_quiet.set_defaults(func=cmd_quiet_engineers)

    # epic-health
    p_epic = subparsers.add_parser("epic-health", help="Stale epics and unassigned tickets")
    _add_dry_run(p_epic)
    p_epic.set_defaults(func=cmd_epic_health)

    # newsletter
    p_news = subparsers.add_parser("newsletter", help="Generate and send weekly newsletter")
    p_news.add_argument("--week", type=int, default=1, help="Number of weeks to cover (default: 1)")
    _add_dry_run(p_news)
    p_news.set_defaults(func=cmd_newsletter)

    args = parser.parse_args()

    if not args.command:
        env_path = SKILL_DIR / ".env"
        if not env_path.exists():
            print("\n👋 Welcome to em-intel!")
            print("   Looks like this is your first time. Let's get you set up.\n")
            print("   Option A — guided setup (recommended):")
            print("     ./run.sh setup          # auto-detects Python or Docker")
            print("     python3 em_intel.py setup\n")
            print("   Option B — preview with mock data (no credentials needed):")
            print("     ./run.sh morning-brief --dry-run\n")
            print("   No Python? No problem — Docker works too:")
            print("     docker build -t em-intel . && docker run --rm em-intel setup\n")
        else:
            parser.print_help()
        sys.exit(0)

    try:
        args.func(args)
    except Exception as exc:
        logger.error("Command failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
