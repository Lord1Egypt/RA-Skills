"""Output rendering for /depradar.

Modes: compact (default), json, md (full markdown), context (for skills), path.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from schema import (
    DepRadarReport, BreakingChange, GithubIssueItem, HackerNewsItem,
    ImpactLocation, PackageUpdate, RedditItem, StackOverflowItem, TwitterItem,
)
from dates import format_relative
from score import _title_is_probably_relevant


# ── Public API ────────────────────────────────────────────────────────────────

def render(report: DepRadarReport, emit_mode: str = "compact", min_score: int = 0) -> str:
    """Dispatch to the correct renderer."""
    modes = {
        "compact": render_compact,
        "json":    render_json,
        "md":      render_markdown,
        "context": render_context,
    }
    fn = modes.get(emit_mode, render_compact)
    if emit_mode == "compact":
        return render_compact(report, min_score=min_score)
    return fn(report)


def render_compact(report: DepRadarReport, min_score: int = 0) -> str:
    """Concise report for in-terminal reading. ~200-400 lines."""
    lines: List[str] = []
    _header(lines, report)

    breaking = report.packages_with_breaking_changes
    minor    = report.packages_with_minor_updates

    if not breaking and not minor:
        lines.append("  ✅ All dependencies are up to date. Nothing to do.")
        _footer(lines, report)
        return "\n".join(lines)

    if breaking:
        lines.append(_divider("⚠️  BREAKING CHANGES — action required"))
        visible   = [p for p in breaking if min_score == 0 or p.score >= min_score]
        suppressed = [p for p in breaking if min_score > 0 and p.score < min_score]
        for pkg in visible:
            _render_breaking_package(lines, pkg, report)
        if suppressed:
            lines.append(
                f"  ℹ {len(suppressed)} low-priority item(s) below score {min_score} "
                "(use --min-score=0 to see all)"
            )

    if minor:
        lines.append(_divider("🟡  MINOR UPDATES (no breaking changes)"))
        for pkg in minor[:10]:   # cap at 10
            lines.append(
                f"  {pkg.package:<30} {pkg.current_version} → {pkg.latest_version}"
                f"  ({pkg.semver_type})"
                + (" — SEMVER VIOLATION: breaking change in minor release" if pkg.semver_violation else "")
                + (f"  — security fix included" if _has_security(pkg) else "")
            )
        if len(minor) > 10:
            lines.append(f"  … and {len(minor) - 10} more minor updates")

    if report.packages_current:
        lines.append("")
        lines.append(f"  ✅ Up to date ({len(report.packages_current)} packages)")

    if report.packages_not_found:
        lines.append("")
        lines.append(f"  ○ Not found in registry: {', '.join(report.packages_not_found)}")

    _footer(lines, report)
    return "\n".join(lines)


def render_json(report: DepRadarReport) -> str:
    """Full JSON output — the entire report as machine-readable JSON."""
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)


def render_markdown(report: DepRadarReport) -> str:
    """Full markdown report — suitable for saving to file."""
    lines: List[str] = []
    project = Path(report.project_path).name or "project"
    date    = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines.append(f"# /depradar Report — {project}")
    lines.append(f"*Generated: {date}  |  Window: last {report.days_window} days  |  Depth: {report.depth}*")
    lines.append("")

    breaking = report.packages_with_breaking_changes
    if breaking:
        lines.append("## ⚠️ Breaking Changes")
        lines.append("")
        for pkg in breaking:
            lines.append(f"### `{pkg.package}` — {pkg.current_version} → {pkg.latest_version}")
            lines.append(f"**Released:** {format_relative(pkg.release_date or '')}  |  "
                         f"**Score:** {pkg.score}/100")
            lines.append("")
            if pkg.breaking_changes:
                lines.append("#### What changed")
                for bc in pkg.breaking_changes:
                    lines.append(f"- **[{bc.change_type.upper()}]** `{bc.symbol}` — {bc.description}")
                    if bc.old_signature:
                        lines.append(f"  - Before: `{bc.old_signature}`")
                    if bc.new_signature:
                        lines.append(f"  - After:  `{bc.new_signature}`")
                    if bc.migration_note:
                        lines.append(f"  - 💡 {bc.migration_note}")
            elif pkg.semver_type == "major":
                lines.append(
                    "> ⚠️ **Major version bump** — specific breaking changes could not be "
                    "automatically extracted. Review the changelog before upgrading."
                )
            if pkg.impact_locations:
                lines.append("")
                lines.append("#### Impact in your codebase")
                for loc in pkg.impact_locations[:8]:
                    lines.append(f"- `{loc.file_path}:{loc.line_number}` — `{loc.usage_text[:80]}`")
                if len(pkg.impact_locations) > 8:
                    lines.append(f"- … and {len(pkg.impact_locations) - 8} more locations")
            if pkg.changelog_url:
                lines.append("")
                lines.append(f"📋 [Release notes / Changelog]({pkg.changelog_url})")
            lines.append("")
            _md_community_signals(lines, pkg.package, report)
            lines.append("---")
            lines.append("")

    minor = report.packages_with_minor_updates
    if minor:
        lines.append("## 🟡 Minor Updates")
        lines.append("")
        lines.append("| Package | Current | Latest | Type |")
        lines.append("|---------|---------|--------|------|")
        for pkg in minor[:20]:
            lines.append(f"| `{pkg.package}` | {pkg.current_version} | {pkg.latest_version} | {pkg.semver_type} |")
        if len(minor) > 20:
            lines.append(f"\n*…and {len(minor) - 20} more.*")
        lines.append("")

    if report.packages_current:
        lines.append(f"## ✅ Up to Date ({len(report.packages_current)} packages)")
        lines.append("")
        lines.append(", ".join(f"`{p}`" for p in sorted(report.packages_current)))
        lines.append("")

    _md_errors(lines, report)
    return "\n".join(lines)


def render_context(report: DepRadarReport) -> str:
    """Compact context snippet suitable for passing to other Claude Code skills."""
    lines: List[str] = []
    breaking = report.packages_with_breaking_changes
    if not breaking:
        return f"No breaking dependency changes detected in last {report.days_window} days."
    lines.append(f"[/depradar context — {len(breaking)} breaking change(s) detected]")
    for pkg in breaking[:5]:
        lines.append(f"\n• {pkg.package} {pkg.current_version}→{pkg.latest_version} ({pkg.semver_type})")
        for bc in pkg.breaking_changes[:2]:
            lines.append(f"  - {bc.change_type}: {bc.symbol} — {bc.description[:80]}")
        if pkg.impact_locations:
            lines.append(f"  - Impact: {len(pkg.impact_locations)} file(s) in your codebase")
    if len(breaking) > 5:
        lines.append(f"\n… and {len(breaking) - 5} more. Run /depradar for full report.")
    return "\n".join(lines)


def auto_save(report: DepRadarReport, save_dir: Optional[str] = None) -> Optional[str]:
    """Save full markdown to disk. Returns the path, or None on failure."""
    if save_dir:
        directory = Path(save_dir)
    else:
        directory = Path.home() / "Documents" / "DepRadar"
    try:
        directory.mkdir(parents=True, exist_ok=True)
        project = re.sub(r"[^\w\-]", "_", Path(report.project_path).name or "project")
        date    = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"{project}-{date}.md"
        path = directory / filename
        path.write_text(render_markdown(report), encoding="utf-8")
        return str(path)
    except OSError:
        return None


# ── Internal rendering helpers ────────────────────────────────────────────────

def _header(lines: List[str], report: DepRadarReport) -> None:
    project = Path(report.project_path).name or "project"
    n_breaking = len(report.packages_with_breaking_changes)
    n_minor    = len(report.packages_with_minor_updates)
    n_current  = len(report.packages_current)

    lines.append(f"\n  /depradar  — {project}")
    # Prominent partial-results banner — shown BEFORE the count line so it can't be missed
    if report.partial_results:
        lines.append("  ⚠️  PARTIAL RESULTS — some packages could not be checked (see footer for details)")
    lines.append(
        f"  📦 {report.packages_scanned} packages scanned  "
        f"| ⚠️  {n_breaking} breaking  "
        f"| 🟡 {n_minor} minor  "
        f"| ✅ {n_current} current"
    )
    if report.from_cache and report.cache_age_hours is not None:
        lines.append(f"  (cached {report.cache_age_hours:.1f}h ago — use --refresh to update)")
    lines.append("")


def _footer(lines: List[str], report: DepRadarReport) -> None:
    if report.registry_errors:
        lines.append("")
        lines.append("  ⚠️  Registry errors:")
        for pkg, err in report.registry_errors.items():
            lines.append(f"     {pkg}: {err}")
    # Registry fetch errors (transient: network/timeout) — distinct from not-found
    if report.registry_fetch_errors:
        lines.append("")
        lines.append(
            f"  ⚠️  {len(report.registry_fetch_errors)} package(s) had fetch errors "
            "(network/timeout — may be transient):"
        )
        for pkg, err in list(report.registry_fetch_errors.items())[:5]:
            lines.append(f"     • {pkg}: {err}")
        lines.append("     (Retry with --refresh to force a fresh attempt)")
    if report.dep_parse_errors:
        lines.append("")
        lines.append(f"  ⚠️  {len(report.dep_parse_errors)} dependency file(s) had parse errors:")
        for err in report.dep_parse_errors[:3]:
            lines.append(f"     • {err}")
    if report.scan_skipped:
        lines.append("")
        lines.append(f"  ℹ  {len(report.scan_skipped)} file(s) skipped during scan (run --verbose for details)")
    if report.rate_limit_hits:
        lines.append("")
        for src, cnt in report.rate_limit_hits.items():
            lines.append(
                f"  ⚠️  GitHub rate limit: {cnt} package(s) could not be checked. "
                "Add GITHUB_TOKEN to ~/.config/depradar/.env for 5000 req/hr."
            )
        # List the actual package names that were skipped
        if report.rate_limited_packages:
            pkgs = ", ".join(report.rate_limited_packages[:10])
            suffix = (
                f" (+{len(report.rate_limited_packages) - 10} more)"
                if len(report.rate_limited_packages) > 10 else ""
            )
            lines.append(f"     Packages skipped: {pkgs}{suffix}")
    lines.append("")
    lines.append(f"  💾 Tip: /depradar --emit=md  saves full report to ~/Documents/DepRadar/")
    lines.append("")


def _divider(label: str) -> str:
    return f"\n  {'─' * 55}\n  {label}\n  {'─' * 55}"


def _render_breaking_package(
    lines: List[str], pkg: PackageUpdate, report: DepRadarReport
) -> None:
    rel = format_relative(pkg.release_date or "")

    # Build badges
    badges = ["BREAKING"]
    if pkg.semver_violation:
        badges.append("⚠ SEMVER VIOLATION")
    if pkg.score >= 70:
        stale_badge = _staleness_badge(pkg.release_date or "")
        if stale_badge:
            badges.append(stale_badge)

    badge_str = "  ".join(badges)
    lines.append(f"\n  ### {pkg.package}  {pkg.current_version} → {pkg.latest_version}  "
                 f"[{badge_str}]  Released: {rel}  (score: {pkg.score}/100)")

    # Per-workspace table (Fix 22)
    ws = pkg.workspace_versions
    if len(ws) > 1:
        lines.append("\n  Affected workspaces:")
        for ws_path, ws_ver in sorted(ws.items()):
            try:
                rel_path = os.path.relpath(ws_path)
            except ValueError:
                rel_path = ws_path
            lines.append(f"    • {rel_path} ({ws_ver} → breaking)")

    # Impact
    if pkg.impact_locations:
        conf_badge = {"high": "HIGH", "med": "MED", "low": "LOW"}.get(pkg.impact_confidence, "")
        lines.append(
            f"\n  **Impact: {len(pkg.impact_locations)} file(s) in YOUR codebase** "
            f"[{conf_badge} confidence]"
        )
        for loc in pkg.impact_locations[:6]:
            method_badge = {"ast": " [AST]", "grep": " [pattern]"}.get(loc.detection_method, "")
            lines.append(f"    - {loc.file_path}:{loc.line_number}{method_badge} — {loc.usage_text[:70]}")
        if len(pkg.impact_locations) > 6:
            lines.append(f"    … +{len(pkg.impact_locations) - 6} more")
    elif pkg.impact_confidence != "not_scanned":
        lines.append("  **Impact: Not detected in your codebase** (may be indirect usage)")

    # Breaking changes list
    if pkg.breaking_changes:
        lines.append("\n  **Breaking changes:**")
        for i, bc in enumerate(pkg.breaking_changes, 1):
            lines.append(f"    {i}. `{bc.symbol}` [{bc.change_type.upper()}]")
            lines.append(f"       {bc.description}")
            if bc.source_excerpt and bc.source_excerpt != bc.description:
                excerpt = bc.source_excerpt[:120].replace("\n", " ")
                lines.append(f"       Source: \"{excerpt}\"")
            if bc.migration_note:
                lines.append(f"       💡 {bc.migration_note}")
    elif pkg.semver_type == "major":
        # Major bump but specific breaking changes could not be extracted from release notes.
        # Give the developer explicit guidance rather than silently showing nothing.
        lines.append(
            "\n  ⚠️  Major version bump — specific breaking changes could not be"
            " automatically extracted from the release notes."
        )
        if pkg.changelog_url:
            lines.append(f"  📋 Review the changelog before upgrading: {pkg.changelog_url}")
        else:
            lines.append(
                "  Search for the package migration guide before upgrading."
            )

    # Release notes snippet
    if pkg.release_notes_snippet:
        snippet = pkg.release_notes_snippet[:300].replace("\n", " ").strip()
        lines.append(f"\n  **Release notes:** {snippet}…")

    if pkg.changelog_url:
        lines.append(f"\n  📋 Full notes: {pkg.changelog_url}")

    # Community signals for this package
    issues  = [x for x in report.github_issues if x.package == pkg.package]
    so_q    = [x for x in report.stackoverflow  if x.package == pkg.package]
    reddit  = [x for x in report.reddit         if x.package == pkg.package]
    hn      = [x for x in report.hackernews     if x.package == pkg.package]

    def _best_relevant(items, title_fn):
        """Return the highest-scored item whose title passes relevance filter, or None.

        Returns None when all titles are noise (e.g. Flutter checklists for commander.js).
        The caller still shows the count — only the example title is suppressed.
        """
        rel = [x for x in items if _title_is_probably_relevant(title_fn(x), pkg.package)]
        return max(rel, key=lambda x: x.score) if rel else None

    total_signals = len(issues) + len(so_q) + len(reddit) + len(hn)
    if total_signals:
        lines.append("\n  **Community signals:**")
        if issues:
            top = _best_relevant(issues, lambda x: x.title)
            if top:
                lines.append(f"    - {len(issues)} GitHub issue(s) — e.g. \"{top.title[:60]}\"")
            else:
                lines.append(f"    - {len(issues)} GitHub issue(s)")
        if so_q:
            top = _best_relevant(so_q, lambda x: x.question_title)
            if top:
                lines.append(
                    f"    - StackOverflow: \"{top.question_title[:60]}\" "
                    f"({top.answer_count} answer(s)"
                    + (", SOLVED" if top.is_answered else "")
                    + ")"
                )
            else:
                lines.append(f"    - {len(so_q)} StackOverflow question(s)")
        if reddit:
            top = _best_relevant(reddit, lambda x: x.title)
            if top:
                lines.append(f"    - Reddit r/{top.subreddit}: \"{top.title[:55]}\"")
            else:
                lines.append(f"    - {len(reddit)} Reddit post(s)")
        if hn:
            top = _best_relevant(hn, lambda x: x.title)
            if top:
                lines.append(f"    - HN: \"{top.title[:60]}\" ({top.points} pts)")
            else:
                lines.append(f"    - {len(hn)} HN item(s)")
    lines.append("")


def _md_community_signals(
    lines: List[str], package: str, report: DepRadarReport
) -> None:
    issues  = [x for x in report.github_issues if x.package == package]
    so_q    = [x for x in report.stackoverflow  if x.package == package]
    reddit  = [x for x in report.reddit         if x.package == package]
    hn      = [x for x in report.hackernews     if x.package == package]

    if not any([issues, so_q, reddit, hn]):
        return

    def _relevant(items, title_fn):
        rel = [x for x in items if _title_is_probably_relevant(title_fn(x), package)]
        return rel if rel else []

    lines.append("#### Community signals")
    lines.append("")
    for item in sorted(_relevant(issues, lambda x: x.title), key=lambda x: x.score, reverse=True)[:3]:
        state = "🔴 open" if item.state == "open" else "✅ closed"
        lines.append(f"- **GitHub Issue** [{state}] [{item.title}]({item.url}) — {item.comments} comments")
    for item in sorted(_relevant(so_q, lambda x: x.question_title), key=lambda x: x.score, reverse=True)[:3]:
        answered = "✅ answered" if item.is_answered else "❓ unanswered"
        lines.append(f"- **StackOverflow** [{answered}] [{item.question_title}]({item.question_url})")
    for item in sorted(_relevant(reddit, lambda x: x.title), key=lambda x: x.score, reverse=True)[:2]:
        lines.append(f"- **Reddit** r/{item.subreddit}: [{item.title}]({item.url})")
    for item in sorted(_relevant(hn, lambda x: x.title), key=lambda x: x.score, reverse=True)[:2]:
        lines.append(f"- **HN:** [{item.title}]({item.hn_url}) — {item.points} pts")
    lines.append("")


def _md_errors(lines: List[str], report: DepRadarReport) -> None:
    errors = {**report.registry_errors, **report.community_errors, **report.scan_errors}
    if not errors:
        return
    lines.append("## ⚠️ Errors")
    lines.append("")
    for source, msg in errors.items():
        lines.append(f"- `{source}`: {msg}")
    lines.append("")


def _has_security(pkg: PackageUpdate) -> bool:
    notes = (pkg.release_notes_snippet or "").lower()
    return any(kw in notes for kw in ("cve", "security", "vulnerability", "vuln"))


def _staleness_badge(release_date: str) -> str:
    """Return a staleness badge string if the package is overdue for upgrade."""
    if not release_date:
        return ""
    try:
        from dates import days_since
        days = days_since(release_date)
    except Exception:
        return ""
    if days >= 365:
        return "⚡ STALE (1y+)"
    elif days >= 180:
        return "⚡ STALE (6m+)"
    elif days >= 90:
        return "⚡ STALE (3m+)"
    return ""
