"""CLI entry point for code-inspector."""

import os
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from code_inspector.detectors import (
    inspect_code,
    inspect_directory,
    CodeSmell,
    InspectResult,
    SEVERITY_WEIGHTS,
)

console = Console()

SEVERITY_ICON = {
    "critical": "🔴",
    "warning": "🟡",
    "info": "🔵",
}

SEVERITY_COLOR = {
    "critical": "red",
    "warning": "yellow",
    "info": "blue",
}


def _print_smells_table(smells: list, title: str):
    """Print a rich table of code smells."""
    if not smells:
        console.print(f"[green]No issues found[/green] — {title}")
        return

    table = Table(title=title, box=box.ROUNDED, expand=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Line", justify="right", width=6)
    table.add_column("Severity", width=10)
    table.add_column("Type", width=22)
    table.add_column("Description", width=48)
    table.add_column("Suggestion", width=40)

    for idx, smell in enumerate(smells, 1):
        icon = SEVERITY_ICON.get(smell.severity, "⚪")
        color = SEVERITY_COLOR.get(smell.severity, "white")
        table.add_row(
            str(idx),
            str(smell.line_number),
            f"{icon} [{color}]{smell.severity}[/{color}]",
            smell.name,
            smell.description[:80],
            smell.fix_suggestion[:60],
        )

    console.print(table)


def _quality_color(score: int) -> str:
    if score >= 90:
        return "green"
    elif score >= 70:
        return "yellow"
    elif score >= 50:
        return "orange1"
    else:
        return "red"


def _print_score_bar(score: int, label: str):
    """Print a visual quality score bar."""
    color = _quality_color(score)
    bar_len = 20
    filled = int(score / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    console.print(f"{label}: [{color}]{bar}[/{color}] [{color}]{score}/100[/{color}]")


@click.group()
def main():
    """code-inspector — detect AI-generated code quality issues."""


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON")
def check(file, json_output):
    """Inspect a single file for AI-generated code smells."""
    result = inspect_code(file)

    if json_output:
        import json
        output = {
            "file_path": result.file_path,
            "language": result.language,
            "quality_score": result.quality_score,
            "smells": [
                {
                    "name": s.name,
                    "severity": s.severity,
                    "line_number": s.line_number,
                    "description": s.description,
                    "snippet": s.snippet,
                    "fix_suggestion": s.fix_suggestion,
                }
                for s in result.smells
            ],
        }
        console.print_json(json.dumps(output, indent=2))
        return

    console.print(Panel.fit(
        f"[bold]{result.file_path}[/bold]  |  Language: {result.language}",
        title="Code Inspector",
        border_style="cyan",
    ))
    _print_score_bar(result.quality_score, "Quality Score")
    _print_smells_table(result.smells, f"Smells Found: {len(result.smells)}")

    if result.smells:
        console.print(f"\n[bold red]{len(result.smells)} issue(s) detected.[/bold red]")
    else:
        console.print("\n[bold green]✓ Clean! No AI code smells detected.[/bold green]")


@main.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--min-score", type=int, default=0, help="Only show files with score below this threshold")
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON")
def scan(directory, min_score, json_output):
    """Scan a directory recursively for AI-generated code smells."""
    results = inspect_directory(directory)

    if not results:
        console.print("[yellow]No supported files found (.py, .js, .ts)[/yellow]")
        return

    if json_output:
        import json
        output = []
        for r in results:
            if r.quality_score >= min_score:
                continue
            output.append({
                "file_path": r.file_path,
                "language": r.language,
                "quality_score": r.quality_score,
                "smells_count": len(r.smells),
                "smells": [
                    {
                        "name": s.name,
                        "severity": s.severity,
                        "line_number": s.line_number,
                        "description": s.description,
                    }
                    for s in r.smells
                ],
            })
        console.print_json(json.dumps(output, indent=2))
        return

    console.print(Panel.fit(
        f"[bold]{directory}[/bold]  |  {len(results)} file(s) scanned",
        title="Code Inspector — Directory Scan",
        border_style="cyan",
    ))

    # Summary table
    table = Table(title="Scan Results", box=box.ROUNDED)
    table.add_column("File", style="cyan", max_width=50)
    table.add_column("Lang", width=6)
    table.add_column("Score", justify="right", width=8)
    table.add_column("Issues", justify="right", width=8)
    table.add_column("Top Smell", max_width=30)

    total_smells = 0
    for r in results:
        if r.quality_score >= min_score and min_score > 0:
            continue
        total_smells += len(r.smells)
        top_smell = ""
        if r.smells:
            smell_counts = {}
            for s in r.smells:
                smell_counts[s.name] = smell_counts.get(s.name, 0) + 1
            top_smell = max(smell_counts, key=smell_counts.get)

        score_color = _quality_color(r.quality_score)
        table.add_row(
            os.path.relpath(r.file_path, directory),
            r.language[:6],
            f"[{score_color}]{r.quality_score}[/{score_color}]",
            str(len(r.smells)),
            top_smell,
        )

    console.print(table)

    # Overall stats
    avg_score = sum(r.quality_score for r in results) / len(results) if results else 0
    console.print(f"\n[bold]Total files:[/bold] {len(results)}  |  "
                  f"[bold]Total issues:[/bold] {total_smells}  |  "
                  f"[bold]Avg score:[/bold] {avg_score:.1f}")

    # Show detailed smells for files with issues
    files_with_issues = [r for r in results if r.smells]
    if files_with_issues:
        console.print(f"\n[bold]Files with issues ({len(files_with_issues)}):[/bold]")
        for r in files_with_issues:
            if r.quality_score >= min_score and min_score > 0:
                continue
            _print_smells_table(r.smells, f"{os.path.relpath(r.file_path, directory)} — Score: {r.quality_score}")


@main.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON")
def stats(directory, json_output):
    """Aggregate statistics: smells by type, quality score distribution."""
    results = inspect_directory(directory)

    if not results:
        console.print("[yellow]No supported files found (.py, .js, .ts)[/yellow]")
        return

    # Aggregate stats
    total_files = len(results)
    total_smells = sum(len(r.smells) for r in results)
    files_with_smells = sum(1 for r in results if r.smells)
    files_clean = total_files - files_with_smells

    # Smells by type
    smell_type_counts = {}
    for r in results:
        for s in r.smells:
            smell_type_counts[s.name] = smell_type_counts.get(s.name, 0) + 1

    # Severity distribution
    severity_counts = {"critical": 0, "warning": 0, "info": 0}
    for r in results:
        for s in r.smells:
            severity_counts[s.severity] = severity_counts.get(s.severity, 0) + 1

    # Quality score distribution
    score_buckets = {"0-49": 0, "50-69": 0, "70-89": 0, "90-100": 0}
    for r in results:
        s = r.quality_score
        if s < 50:
            score_buckets["0-49"] += 1
        elif s < 70:
            score_buckets["50-69"] += 1
        elif s < 90:
            score_buckets["70-89"] += 1
        else:
            score_buckets["90-100"] += 1

    avg_score = sum(r.quality_score for r in results) / total_files if total_files else 0

    if json_output:
        import json
        output = {
            "total_files": total_files,
            "total_smells": total_smells,
            "files_with_smells": files_with_smells,
            "files_clean": files_clean,
            "average_score": round(avg_score, 1),
            "smells_by_type": dict(sorted(smell_type_counts.items(), key=lambda x: -x[1])),
            "severity_distribution": severity_counts,
            "score_distribution": score_buckets,
        }
        console.print_json(json.dumps(output, indent=2))
        return

    console.print(Panel.fit(
        f"[bold]{directory}[/bold]",
        title="Code Inspector — Statistics",
        border_style="cyan",
    ))

    # Overview
    overview = Table(title="Overview", box=box.ROUNDED)
    overview.add_column("Metric", style="cyan")
    overview.add_column("Value", justify="right")
    overview.add_row("Total files scanned", str(total_files))
    overview.add_row("Files with issues", str(files_with_smells))
    overview.add_row("Clean files", str(files_clean))
    overview.add_row("Total smells found", str(total_smells))
    overview.add_row("Average quality score", f"{avg_score:.1f}/100")
    console.print(overview)

    # Smells by type
    if smell_type_counts:
        smell_table = Table(title="Smells by Type", box=box.ROUNDED)
        smell_table.add_column("Type", style="cyan")
        smell_table.add_column("Count", justify="right")
        smell_table.add_column("Severity")
        smell_table.add_column("Deduction/occurrence", justify="right")
        for name, count in sorted(smell_type_counts.items(), key=lambda x: -x[1]):
            weight = SEVERITY_WEIGHTS.get(name, 5)
            if weight >= 20:
                sev = "🔴 critical"
            elif weight >= 10:
                sev = "🟡 warning"
            else:
                sev = "🔵 info"
            smell_table.add_row(name, str(count), sev, f"-{weight}")
        console.print(smell_table)

    # Severity distribution
    sev_table = Table(title="Severity Distribution", box=box.ROUNDED)
    sev_table.add_column("Severity")
    sev_table.add_column("Count", justify="right")
    sev_table.add_column("Bar")
    max_sev = max(severity_counts.values()) if severity_counts else 1
    for sev, cnt in severity_counts.items():
        icon = SEVERITY_ICON.get(sev, "⚪")
        bar_len = int(cnt / max(max_sev, 1) * 20)
        bar = "█" * bar_len
        sev_table.add_row(f"{icon} {sev}", str(cnt), bar)
    console.print(sev_table)

    # Score distribution
    score_table = Table(title="Quality Score Distribution", box=box.ROUNDED)
    score_table.add_column("Score Range")
    score_table.add_column("Files", justify="right")
    score_table.add_column("Bar")
    max_bucket = max(score_buckets.values()) if score_buckets else 1
    for bucket, cnt in score_buckets.items():
        bar_len = int(cnt / max(max_bucket, 1) * 20)
        bar = "█" * bar_len
        score_table.add_row(bucket, str(cnt), bar)
    console.print(score_table)

    # Top offenders
    offenders = sorted(results, key=lambda r: r.quality_score)[:5]
    if offenders:
        top_table = Table(title="Top 5 Lowest-Scoring Files", box=box.ROUNDED)
        top_table.add_column("File", style="cyan", max_width=50)
        top_table.add_column("Score", justify="right")
        top_table.add_column("Issues", justify="right")
        for r in offenders:
            score_color = _quality_color(r.quality_score)
            top_table.add_row(
                os.path.relpath(r.file_path, directory),
                f"[{score_color}]{r.quality_score}[/{score_color}]",
                str(len(r.smells)),
            )
        console.print(top_table)


if __name__ == "__main__":
    main()
