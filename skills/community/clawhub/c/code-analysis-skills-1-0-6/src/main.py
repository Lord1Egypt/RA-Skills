"""
Code Analysis Skills - Main Entry Point

A comprehensive Git repository code analysis tool that scans repositories
and analyzes developer commit patterns, work habits, development efficiency,
code style, code quality, and slacking behaviors. Generates honest, direct
evaluations for each developer with scores, grades, and actionable feedback.

Outputs: Markdown, JSON, HTML, PDF
"""

import json
import logging
import os
from typing import Optional

import click
import yaml

from src.scanner import RepoScanner
from src.analyzers.commit_analyzer import CommitAnalyzer
from src.analyzers.work_habit_analyzer import WorkHabitAnalyzer
from src.analyzers.efficiency_analyzer import EfficiencyAnalyzer
from src.analyzers.code_style_analyzer import CodeStyleAnalyzer
from src.analyzers.code_quality_analyzer import CodeQualityAnalyzer
from src.analyzers.slacking_analyzer import SlackingAnalyzer
from src.evaluator.developer_evaluator import DeveloperEvaluator
from src.reporters.markdown_reporter import MarkdownReporter
from src.reporters.json_reporter import JsonReporter
from src.reporters.html_reporter import HtmlReporter
from src.reporters.pdf_reporter import PdfReporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_analysis(
    repo_path: str,
    scan_all_repos: bool = False,
    authors: Optional[list] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    branch: Optional[str] = None,
    output_format: str = "markdown",
    output_path: Optional[str] = None,
) -> dict:
    """
    Main analysis orchestrator.

    Args:
        repo_path: Path to a Git repo or parent directory.
        scan_all_repos: Whether to recursively scan for all .git repos.
        authors: List of author names/emails to filter. None means all.
        since: Start date in ISO format.
        until: End date in ISO format.
        branch: Branch name to analyze.
        output_format: 'json', 'markdown', 'html', or 'pdf'.
        output_path: Output file path (used for PDF generation).

    Returns:
        A dict with 'report' (formatted string) and 'metrics' (raw data).
    """
    # Step 1: Discover repositories
    scanner = RepoScanner()
    if scan_all_repos:
        repos = scanner.scan_directory(repo_path)
    else:
        repos = scanner.scan_single(repo_path)

    if not repos:
        logger.warning("No Git repositories found at: %s", repo_path)
        return {"report": "No Git repositories found.", "metrics": {}}

    logger.info("Found %d repository(ies) to analyze.", len(repos))

    # Step 2: Run all analyzers on each repository
    all_metrics = {}

    for repo_info in repos:
        repo_name = repo_info["name"]
        logger.info("Analyzing repository: %s", repo_name)

        common_kwargs = dict(
            authors=authors, since=since, until=until, branch=branch
        )

        commit_analyzer = CommitAnalyzer(repo_info["path"], **common_kwargs)
        work_habit_analyzer = WorkHabitAnalyzer(repo_info["path"], **common_kwargs)
        efficiency_analyzer = EfficiencyAnalyzer(repo_info["path"], **common_kwargs)
        code_style_analyzer = CodeStyleAnalyzer(repo_info["path"], **common_kwargs)
        code_quality_analyzer = CodeQualityAnalyzer(repo_info["path"], **common_kwargs)
        slacking_analyzer = SlackingAnalyzer(repo_info["path"], **common_kwargs)

        repo_metrics = {
            "commit_patterns": commit_analyzer.analyze(),
            "work_habits": work_habit_analyzer.analyze(),
            "efficiency": efficiency_analyzer.analyze(),
            "code_style": code_style_analyzer.analyze(),
            "code_quality": code_quality_analyzer.analyze(),
            "slacking": slacking_analyzer.analyze(),
        }

        # Step 2.5: Run developer evaluations
        evaluator = DeveloperEvaluator()
        repo_metrics["evaluations"] = evaluator.evaluate(repo_metrics)

        all_metrics[repo_name] = repo_metrics

    # Step 3: Generate report(s)
    # Support generating multiple formats at once
    formats_to_generate = _parse_formats(output_format)
    reports = {}

    for fmt in formats_to_generate:
        reporter = _get_reporter(fmt)

        if fmt == "pdf":
            # PDF needs a file path
            pdf_path = output_path or "report.pdf"
            if not pdf_path.endswith(".pdf"):
                pdf_path = pdf_path.rsplit(".", 1)[0] + ".pdf"
            reporter.generate_to_file(all_metrics, pdf_path)
            reports[fmt] = f"PDF saved to: {pdf_path}"
            logger.info("PDF report generated: %s", pdf_path)
        else:
            reports[fmt] = reporter.generate(all_metrics)

    # Return the primary format's report
    primary_report = reports.get(formats_to_generate[0], "")

    return {"report": primary_report, "metrics": all_metrics, "reports": reports}


def _parse_formats(output_format: str) -> list:
    """Parse output format string, supporting comma-separated multiple formats."""
    formats = [f.strip().lower() for f in output_format.split(",")]
    valid = {"markdown", "json", "html", "pdf"}
    result = []
    for f in formats:
        if f in valid:
            result.append(f)
        else:
            logger.warning("Unknown format '%s', ignoring.", f)
    return result if result else ["markdown"]


def _get_reporter(output_format: str):
    """Factory method to get the appropriate reporter."""
    reporters = {
        "markdown": MarkdownReporter,
        "json": JsonReporter,
        "html": HtmlReporter,
        "pdf": PdfReporter,
    }
    reporter_cls = reporters.get(output_format.lower())
    if not reporter_cls:
        raise ValueError(
            f"Unsupported output format: {output_format}. "
            f"Choose from: {list(reporters.keys())}"
        )
    return reporter_cls()


# ─── CLI Interface ────────────────────────────────────────────────────────────


@click.command()
@click.option(
    "--repo-path", "-r", required=True, help="Path to Git repo or parent directory."
)
@click.option(
    "--scan-all", is_flag=True, default=False, help="Scan all .git repos recursively."
)
@click.option(
    "--author", "-a", multiple=True, help="Author name/email to analyze (repeatable)."
)
@click.option("--since", "-s", default=None, help="Start date (ISO format).")
@click.option("--until", "-u", default=None, help="End date (ISO format).")
@click.option("--branch", "-b", default=None, help="Branch to analyze.")
@click.option(
    "--format",
    "-f",
    "output_format",
    default="markdown",
    help="Output format(s): markdown, json, html, pdf (comma-separated for multiple).",
)
@click.option("--output", "-o", default=None, help="Output file path (prints to stdout if omitted).")
def cli(repo_path, scan_all, author, since, until, branch, output_format, output):
    """Code Analysis Skills - Analyze Git repositories and developer behaviors."""
    authors_list = list(author) if author else None

    result = run_analysis(
        repo_path=repo_path,
        scan_all_repos=scan_all,
        authors=authors_list,
        since=since,
        until=until,
        branch=branch,
        output_format=output_format,
        output_path=output,
    )

    # Handle multiple output formats
    formats = _parse_formats(output_format)

    if len(formats) == 1 and formats[0] != "pdf":
        report_text = result["report"]
        if output:
            ext_map = {"markdown": ".md", "json": ".json", "html": ".html"}
            out_path = output
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(report_text)
            click.echo(f"Report saved to: {out_path}")
        else:
            click.echo(report_text)
    else:
        # Multiple formats: save each to a file
        base = output or "report"
        if "." in base:
            base = base.rsplit(".", 1)[0]

        ext_map = {"markdown": ".md", "json": ".json", "html": ".html", "pdf": ".pdf"}
        for fmt in formats:
            if fmt == "pdf":
                # Already saved by run_analysis
                click.echo(f"PDF saved to: {base}.pdf")
                continue
            ext = ext_map.get(fmt, f".{fmt}")
            out_path = f"{base}{ext}"
            report_text = result["reports"].get(fmt, "")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(report_text)
            click.echo(f"{fmt.upper()} report saved to: {out_path}")


# ─── Skill Entry Point (for ClawHub) ─────────────────────────────────────────


def main(params: dict) -> dict:
    """
    ClawHub skill entry point.

    Args:
        params: Dict of parameters from skill.yaml.

    Returns:
        Dict with 'report' and 'metrics' outputs.
    """
    return run_analysis(
        repo_path=params.get("repo_path", "."),
        scan_all_repos=params.get("scan_all_repos", False),
        authors=params.get("authors") or None,
        since=params.get("since") or None,
        until=params.get("until") or None,
        branch=params.get("branch") or None,
        output_format=params.get("output_format", "markdown"),
        output_path=params.get("output_path") or None,
    )


if __name__ == "__main__":
    cli()
