"""disk-sweeper: Report formatter.

Renders scan/analysis results into Markdown, JSON, or plain text reports.
"""
import json
from typing import Dict, List, Optional


def format_report(
    analysis: Dict,
    output_format: str = "markdown",
    summary_only: bool = False,
) -> str:
    """Format analysis results into the desired output format."""
    if output_format == "json":
        return json.dumps(analysis, ensure_ascii=False, indent=2)

    if output_format == "text":
        return _format_text(analysis)

    return _format_markdown(analysis, summary_only)


def _format_markdown(analysis: Dict, summary_only: bool) -> str:
    """Render as Markdown report."""
    lines = []
    lines.append("# 📊 Disk Analysis Report\n")
    lines.append(f"**Total**: {analysis.get('total_size_human', 'N/A')} "
                 f"| **Files**: {analysis.get('total_files', 0):,}")
    lines.append("")

    if summary_only:
        lines.append(f"**Estimated Cleanable**: {analysis.get('potential_free_human', 'N/A')}")
        return "\n".join(lines)

    # By type
    lines.append("## 📁 By File Type\n")
    lines.append("| Type | Size | Files | % |")
    lines.append("|------|------|-------|---|")
    for t in analysis.get("by_type", []):
        bars = "█" * max(1, int(t["percentage"] / 2))
        lines.append(f"| {t['type']} | {t['size_human']} | {t['file_count']:,} | {t['percentage']}% {bars} |")
    lines.append("")

    # Top files
    lines.append("## 🔍 Largest Files\n")
    lines.append("| # | Name | Size | Type |")
    lines.append("|---|------|------|------|")
    for i, f in enumerate(analysis.get("top_files", [])[:10], 1):
        lines.append(f"| {i} | {f.get('name', 'N/A')} | {f.get('size_human', 'N/A')} | {f.get('type', 'N/A')} |")
    lines.append("")

    # Largest dirs
    lines.append("## 📂 Largest Directories\n")
    lines.append("| Directory | Size | Files |")
    lines.append("|-----------|------|-------|")
    for d in analysis.get("largest_dirs", [])[:10]:
        lines.append(f"| {d.get('path', 'N/A')} | {d.get('size_human', 'N/A')} | {d.get('file_count', 0):,} |")
    lines.append("")

    # Duplicates
    dupes = analysis.get("duplicates", {})
    if dupes.get("groups_found", 0) > 0:
        lines.append("## 🔁 Duplicate Files\n")
        lines.append(f"Found {dupes['groups_found']} duplicate groups, wasting **{dupes.get('total_wasted_human', 'N/A')}**\n")
        for g in dupes.get("groups", [])[:5]:
            lines.append(f"- {g.get('size_human', 'N/A')} × {g.get('count', 0)} copies: {g.get('paths', ['N/A'])[0]}")
        lines.append("")

    # Caches
    caches = analysis.get("caches", [])
    if caches:
        lines.append("## 🗑️ Application Caches\n")
        lines.append("| App | Size | Safety |")
        lines.append("|-----|------|--------|")
        for c in caches[:10]:
            icon = {"SAFE": "🟢", "CLEANABLE": "🟡", "CAUTION": "🟠"}
            lines.append(f"| {c.get('app', 'N/A')} | {c.get('size_human', 'N/A')} | {icon.get(c.get('safety', ''), '⚪')} {c.get('safety', 'N/A')} |")
        lines.append("")

    # Recommendations
    recs = analysis.get("recommendations", [])
    if recs:
        lines.append("## 🧹 Cleanup Recommendations\n")
        for r in recs:
            lines.append(f"- [{r.get('safety', 'N/A')}] {r.get('category', 'N/A')}: {r.get('action', 'N/A')} (~{r.get('potential_savings_human', 'N/A')})")

    return "\n".join(lines)


def _format_text(analysis: Dict) -> str:
    """Render as plain text."""
    lines = []
    lines.append("Disk Analysis Report")
    lines.append("=" * 40)
    lines.append(f"Total: {analysis.get('total_size_human', 'N/A')}")
    lines.append(f"Files: {analysis.get('total_files', 0):,}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    test = {
        "total_size_human": "156.4 GB",
        "total_files": 50234,
        "by_type": [
            {"type": "video", "size_human": "48.2 GB", "file_count": 124, "percentage": 30.8},
            {"type": "image", "size_human": "32.1 GB", "file_count": 12045, "percentage": 20.5},
        ],
        "top_files": [
            {"name": "4k-demo.mov", "size_human": "4.2 GB", "type": "video"},
            {"name": "backup.zip", "size_human": "2.8 GB", "type": "archive"},
        ],
        "largest_dirs": [
            {"path": "/Users/test/Movies", "size_human": "48.2 GB", "file_count": 124},
        ],
    }
    print(_format_markdown(test, summary_only=False))
