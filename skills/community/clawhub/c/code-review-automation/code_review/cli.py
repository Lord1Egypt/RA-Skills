"""CLI interface for Code Review Automation."""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from .github_client import GitHubConfig
from .claude_client import ClaudeConfig
from .repo_ops import GitHubRepo
from .pr_analyzer import PRAnalyzer
from .security_scanner import SecurityScanner
from .style_checker import StyleChecker
from .config import ConfigManager

app = typer.Typer(
    name="code-review",
    help="Automated code review for GitHub pull requests",
    add_completion=False
)

console = Console()


@app.command()
def list_prs(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    state: str = typer.Option("open", help="PR state (open, closed, all)"),
    limit: int = typer.Option(10, "--limit", help="Maximum PRs to show")
):
    """List pull requests for a repository."""
    config = GitHubConfig()

    if not config.is_configured():
        console.print("[red]✗ Not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    try:
        client = config.get_client()
        repo_ops = GitHubRepo(client, repo)
        prs = repo_ops.get_prs(state=state, limit=limit)

        if not prs:
            console.print(f"[yellow]No PRs found for {repo}[/yellow]")
            return

        table = Table(title=f"Pull Requests ({repo})")
        table.add_column("Number", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Author", style="green")
        table.add_column("State", style="yellow")
        table.add_column("Files", style="white")
        table.add_column("+/-", style="white")

        for pr in prs:
            table.add_row(
                str(pr.number),
                pr.title[:50],
                pr.user.login,
                pr.state.upper(),
                str(pr.changed_files),
                f"+{pr.additions}/-{pr.deletions}"
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def pr_info(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    pr_number: int = typer.Argument(..., help="Pull request number")
):
    """Show detailed information about a pull request."""
    config = GitHubConfig()

    if not config.is_configured():
        console.print("[red]✗ Not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    try:
        client = config.get_client()
        repo_ops = GitHubRepo(client, repo)
        info = repo_ops.get_pr_info(pr_number)

        console.print(Panel(
            f"[bold]PR #{info['number']}[/bold]\n\n"
            f"[cyan]Title:[/cyan] {info['title']}\n"
            f"[cyan]Author:[/cyan] {info['author']}\n"
            f"[cyan]State:[/cyan] {info['state'].upper()}\n"
            f"[cyan]Created:[/cyan] {info['created_at']}\n"
            f"[cyan]Updated:[/cyan] {info['updated_at']}\n\n"
            f"[yellow]Stats:[/yellow]\n"
            f"  Files changed: {info['changed_files']}\n"
            f"  Additions: +{info['additions']}\n"
            f"  Deletions: -{info['deletions']}\n\n"
            f"[green]Mergeable:[/green] {info['mergeable']}\n"
            f"[green]Labels:[/green] {', '.join(info['labels']) or 'None'}\n\n"
            f"[cyan]Description:[/cyan]\n{info['description']}",
            title="Pull Request Details"
        ))

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def pr_files(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    pr_number: int = typer.Argument(..., help="Pull request number")
):
    """Show files changed in a pull request."""
    config = GitHubConfig()

    if not config.is_configured():
        console.print("[red]✗ Not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    try:
        client = config.get_client()
        repo_ops = GitHubRepo(client, repo)
        files = repo_ops.get_pr_diff(pr_number)

        if not files:
            console.print("[yellow]No files changed[/yellow]")
            return

        table = Table(title=f"Files Changed in PR #{pr_number}")
        table.add_column("Filename", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Additions", style="yellow")
        table.add_column("Deletions", style="yellow")

        for file in files:
            table.add_row(
                file.filename,
                file.status.upper(),
                str(file.additions),
                str(file.deletions)
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def search_prs(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    query: str = typer.Option(..., "--query", "-q", help="Search query (searches title)"),
    state: str = typer.Option("open", help="PR state (open, closed, all)"),
    limit: int = typer.Option(10, "--limit", help="Maximum PRs to show")
):
    """Search pull requests by keyword."""
    config = GitHubConfig()

    if not config.is_configured():
        console.print("[red]✗ Not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    try:
        from .utils import truncate_text

        client = config.get_client()
        repo_ops = GitHubRepo(client, repo)
        prs = repo_ops.get_prs(state=state, limit=100)  # Get more for filtering

        # Filter by query
        query_lower = query.lower()
        filtered_prs = [
            pr for pr in prs
            if query_lower in pr.title.lower()
        ][:limit]

        if not filtered_prs:
            console.print(f"[yellow]No PRs found matching '{query}'[/yellow]")
            return

        table = Table(title=f"PRs Matching '{query}' ({repo})")
        table.add_column("Number", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Author", style="green")
        table.add_column("State", style="yellow")
        table.add_column("Updated", style="white")

        for pr in filtered_prs:
            table.add_row(
                str(pr.number),
                truncate_text(pr.title, 50),
                pr.user.login,
                pr.state.upper(),
                pr.updated_at.strftime("%Y-%m-%d %H:%M")
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def repo_info(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)")
):
    """Show general repository information."""
    config = GitHubConfig()

    if not config.is_configured():
        console.print("[red]✗ Not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    try:
        client = config.get_client()
        repository = client.get_repo(repo)

        console.print(Panel(
            f"[bold]{repo}[/bold]\n\n"
            f"[cyan]Name:[/cyan] {repository.full_name}\n"
            f"[cyan]Description:[/cyan] {repository.description or 'No description'}\n"
            f"[cyan]Language:[/cyan] {repository.language or 'N/A'}\n"
            f"[cyan]Stars:[/cyan] {repository.stargazers_count:,}\n"
            f"[cyan]Forks:[/cyan] {repository.forks_count:,}\n"
            f"[cyan]Open Issues:[/cyan] {repository.open_issues_count:,}\n"
            f"[cyan]Open PRs:[/cyan] {repository.get_pulls().totalCount if repository.get_pulls() else 0}\n"
            f"[cyan]Created:[/cyan] {repository.created_at.strftime('%Y-%m-%d')}\n"
            f"[cyan]Updated:[/cyan] {repository.updated_at.strftime('%Y-%m-%d')}",
            title="Repository Information"
        ))

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def review_pr(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    pr_number: int = typer.Argument(..., help="Pull request number")
):
    """Analyze a pull request using Claude AI."""
    github_config = GitHubConfig()
    claude_config = ClaudeConfig()

    if not github_config.is_configured():
        console.print("[red]✗ GitHub not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    if not claude_config.is_configured():
        console.print("[red]✗ Claude not configured. Set ANTHROPIC_API_KEY in .env file.[/red]")
        raise typer.Exit(1)

    try:
        with console.status("[bold green]Analyzing pull request...[/bold green]"):
            # Get GitHub client and repo
            github_client = github_config.get_client()
            repo_ops = GitHubRepo(github_client, repo)

            # Get PR info
            pr = repo_ops.get_pr(pr_number)
            diff_content = repo_ops.get_pr_diff_content(pr_number)

            # Analyze with Claude
            analyzer = PRAnalyzer()
            analysis = analyzer.analyze_pr(pr, diff_content)

            # Get quality score
            quality_score = analyzer.get_code_quality_score(analysis["analysis"])

        # Display results
        console.print()

        # PR Header
        header_color = "green" if quality_score >= 70 else "yellow" if quality_score >= 50 else "red"
        console.print(Panel(
            f"[bold]PR #{pr.number}[/bold]\n\n"
            f"[cyan]Title:[/cyan] {pr.title}\n"
            f"[cyan]Author:[/cyan] {pr.user.login}\n"
            f"[cyan]Files:[/cyan] {pr.changed_files}\n"
            f"[cyan]Additions:[/cyan] +{pr.additions}\n"
            f"[cyan]Deletions:[/cyan] -{pr.deletions}\n\n"
            f"[{header_color}]Code Quality Score: {quality_score}/100[/bold]",
            title="Pull Request Analysis",
            border_style=header_color
        ))

        console.print()

        # Display analysis as markdown
        md = Markdown(analysis["analysis"])
        console.print(md)

        console.print()
        console.print(f"[dim]Analysis generated with {analysis['model']}[/dim]")

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def security_scan(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    pr_number: int = typer.Argument(..., help="Pull request number"),
    config_file: str = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Scan a pull request for security vulnerabilities."""
    github_config = GitHubConfig()

    if not github_config.is_configured():
        console.print("[red]✗ GitHub not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    # Load configuration
    config_mgr = ConfigManager(config_file)
    security_config = config_mgr.get_security_config()

    if not security_config.enabled:
        console.print("[yellow]Security scanning is disabled in configuration.[/yellow]")
        return

    try:
        with console.status("[bold green]Scanning for security vulnerabilities...[/bold green]"):
            # Get GitHub client and repo
            github_client = github_config.get_client()
            repo_ops = GitHubRepo(github_client, repo)

            # Get PR info
            pr = repo_ops.get_pr(pr_number)
            diff_content = repo_ops.get_pr_diff_content(pr_number)

            # Run security scan
            scanner = SecurityScanner()
            issues = scanner.scan_diff(diff_content, repo)
            summary = scanner.get_summary()

        # Display results
        console.print()

        # Summary
        critical_color = "red" if summary['critical'] > 0 else "green"
        high_color = "yellow" if summary['high'] > 0 else "green"
        medium_color = "yellow" if summary['medium'] > 0 else "green"
        low_color = "blue" if summary['low'] > 0 else "green"

        console.print(Panel(
            f"[{critical_color}]Critical: {summary['critical']}[/{critical_color}]  "
            f"[{high_color}]High: {summary['high']}[/{high_color}]  "
            f"[{medium_color}]Medium: {summary['medium']}[/{medium_color}]  "
            f"[{low_color}]Low: {summary['low']}[/{low_color}]  "
            f"\n[dim]Total: {summary['total']} issues found[/dim]",
            title="Security Scan Results",
            border_style=critical_color if summary['critical'] > 0 else high_color if summary['high'] > 0 else "green"
        ))

        console.print()

        # Display issues
        if issues:
            for issue in issues:
                severity_color = {
                    'critical': 'red',
                    'high': 'yellow',
                    'medium': 'yellow',
                    'low': 'blue'
                }[issue.severity]

                console.print(Panel(
                    f"[bold]{severity_color}[{issue.severity.upper()}][/{severity_color}] "
                    f"{issue.category}[/bold]\n\n"
                    f"[cyan]Description:[/cyan] {issue.description}\n"
                    f"[cyan]Recommendation:[/cyan] {issue.recommendation}",
                    title=f"Security Issue (Line {issue.line_number})",
                    border_style=severity_color
                ))

                if config_mgr.config.show_code_snippets and issue.code_snippet:
                    console.print(f"[dim]Code:[/dim] {issue.code_snippet}")
                    console.print()
        else:
            console.print("[green]✓ No security vulnerabilities found[/green]")

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def style_check(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    pr_number: int = typer.Argument(..., help="Pull request number"),
    config_file: str = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Check a pull request for style and linting issues."""
    github_config = GitHubConfig()

    if not github_config.is_configured():
        console.print("[red]✗ GitHub not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    # Load configuration
    config_mgr = ConfigManager(config_file)
    style_config = config_mgr.get_style_config()

    if not style_config.enabled:
        console.print("[yellow]Style checking is disabled in configuration.[/yellow]")
        return

    try:
        with console.status("[bold green]Checking code style...[/bold green]"):
            # Get GitHub client and repo
            github_client = github_config.get_client()
            repo_ops = GitHubRepo(github_client, repo)

            # Get PR info
            pr = repo_ops.get_pr(pr_number)
            diff_content = repo_ops.get_pr_diff_content(pr_number)

            # Run style check
            checker = StyleChecker()
            issues = checker.check_diff(diff_content, repo)
            summary = checker.get_summary()

        # Display results
        console.print()

        # Summary
        error_color = "red" if summary['error'] > 0 else "green"
        warning_color = "yellow" if summary['warning'] > 0 else "green"
        info_color = "blue"

        console.print(Panel(
            f"[{error_color}]Error: {summary['error']}[/{error_color}]  "
            f"[{warning_color}]Warning: {summary['warning']}[/{warning_color}]  "
            f"[{info_color}]Info: {summary['info']}[/{info_color}]  "
            f"\n[dim]Total: {summary['total']} issues found[/dim]",
            title="Style Check Results",
            border_style=error_color if summary['error'] > 0 else "green"
        ))

        console.print()

        # Display issues
        if issues:
            for issue in issues[:20]:  # Limit to first 20 issues
                severity_color = {
                    'error': 'red',
                    'warning': 'yellow',
                    'info': 'blue'
                }[issue.severity]

                console.print(Panel(
                    f"[bold]{severity_color}[{issue.severity.upper()}][/{severity_color}] "
                    f"{issue.category}[/bold]\n\n"
                    f"[cyan]Description:[/cyan] {issue.description}\n"
                    f"[cyan]Suggestion:[/cyan] {issue.suggestion}",
                    title=f"Style Issue (Line {issue.line_number})",
                    border_style=severity_color
                ))

                if config_mgr.config.show_code_snippets and issue.code_snippet:
                    console.print(f"[dim]Code:[/dim] {issue.code_snippet}")
                    console.print()

            if len(issues) > 20:
                console.print(f"[dim]... and {len(issues) - 20} more issues[/dim]")
        else:
            console.print("[green]✓ No style issues found[/green]")

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def full_review(
    repo: str = typer.Argument(..., help="Repository (e.g., owner/repo)"),
    pr_number: int = typer.Argument(..., help="Pull request number"),
    config_file: str = typer.Option(None, "--config", "-c", help="Configuration file path"),
    skip_llm: bool = typer.Option(False, "--skip-llm", help="Skip LLM analysis"),
    skip_security: bool = typer.Option(False, "--skip-security", help="Skip security scan"),
    skip_style: bool = typer.Option(False, "--skip-style", help="Skip style check")
):
    """Run full code review (LLM + Security + Style) on a pull request."""
    github_config = GitHubConfig()
    claude_config = ClaudeConfig()

    if not github_config.is_configured():
        console.print("[red]✗ GitHub not configured. Set GITHUB_TOKEN in .env file.[/red]")
        raise typer.Exit(1)

    # Load configuration
    config_mgr = ConfigManager(config_file)

    try:
        # Get GitHub client and repo
        github_client = github_config.get_client()
        repo_ops = GitHubRepo(github_client, repo)

        # Get PR info
        pr = repo_ops.get_pr(pr_number)
        diff_content = repo_ops.get_pr_diff_content(pr_number)

        console.print()
        console.print(f"[bold cyan]Running full code review for PR #{pr_number}...[/bold cyan]")
        console.print(f"[dim]Repository: {repo}[/dim]")
        console.print(f"[dim]Title: {pr.title}[/dim]")
        console.print()

        # LLM Analysis
        quality_score = None
        if not skip_llm and claude_config.is_configured() and config_mgr.get_llm_config().enabled:
            with console.status("[bold green]Running LLM analysis...[/bold green]"):
                analyzer = PRAnalyzer()
                analysis = analyzer.analyze_pr(pr, diff_content)
                quality_score = analyzer.get_code_quality_score(analysis["analysis"])

            header_color = "green" if quality_score >= 70 else "yellow" if quality_score >= 50 else "red"
            console.print(f"[{header_color}]✓ LLM Analysis: {quality_score}/100[/{header_color}]")

        # Security Scan
        security_summary = None
        if not skip_security and config_mgr.get_security_config().enabled:
            with console.status("[bold green]Running security scan...[/bold green]"):
                scanner = SecurityScanner()
                security_issues = scanner.scan_diff(diff_content, repo)
                security_summary = scanner.get_summary()

            sec_color = "red" if security_summary['critical'] > 0 or security_summary['high'] > 0 else "green"
            console.print(f"[{sec_color}]✓ Security Scan: {security_summary['total']} issues found[/{sec_color}]")

        # Style Check
        style_summary = None
        if not skip_style and config_mgr.get_style_config().enabled:
            with console.status("[bold green]Running style check...[/bold green]"):
                checker = StyleChecker()
                style_issues = checker.check_diff(diff_content, repo)
                style_summary = checker.get_summary()

            style_color = "yellow" if style_summary['error'] > 0 else "green"
            console.print(f"[{style_color}]✓ Style Check: {style_summary['total']} issues found[/{style_color}]")

        console.print()

        # Summary
        console.print(Panel(
            f"[bold]PR #{pr.number}[/bold]\n\n"
            f"[cyan]Title:[/cyan] {pr.title}\n"
            f"[cyan]Author:[/cyan] {pr.user.login}\n"
            f"[cyan]Files:[/cyan] {pr.changed_files}\n"
            f"[cyan]Additions:[/cyan] +{pr.additions}\n"
            f"[cyan]Deletions:[/cyan] -{pr.deletions}\n"
            + (f"\n[{header_color}]Code Quality Score: {quality_score}/100[/{header_color}]" if quality_score else "")
            + (f"\n[red]Security Issues: {security_summary['total']}[/red]" if security_summary and security_summary['total'] > 0 else "")
            + (f"\n[yellow]Style Issues: {style_summary['total']}[/yellow]" if style_summary and style_summary['total'] > 0 else ""),
            title="Full Review Summary",
            border_style="green"
        ))

        # Recommendations
        recommendations = []
        if quality_score and quality_score < config_mgr.get_llm_config().quality_threshold:
            recommendations.append(f"Code quality score ({quality_score}) below threshold ({config_mgr.get_llm_config().quality_threshold})")
        if security_summary and (security_summary['critical'] > 0 or security_summary['high'] > 0):
            recommendations.append(f"Critical/High security issues detected: {security_summary['critical'] + security_summary['high']}")
        if style_summary and style_summary['error'] > 0:
            recommendations.append(f"Style errors detected: {style_summary['error']}")

        if recommendations:
            console.print()
            console.print("[bold yellow]Recommendations:[/bold yellow]")
            for rec in recommendations:
                console.print(f"  • {rec}")

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def config_init(
    output: str = typer.Option(".reviewrc", "--output", "-o", help="Output configuration file path")
):
    """Initialize a default configuration file."""
    try:
        config_mgr = ConfigManager()
        config_path = config_mgr.create_default_config(output)

        console.print(f"[green]✓ Configuration file created: {config_path}[/green]")
        console.print("[dim]Edit the file to customize your code review settings.[/dim]")
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
