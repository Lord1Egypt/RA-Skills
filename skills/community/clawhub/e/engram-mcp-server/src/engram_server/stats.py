from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path

from engram_server.loader import EngramLoader


@dataclass
class EngramStats:
    name: str
    description: str
    knowledge_count: int = 0
    examples_count: int = 0
    memory_entry_count: int = 0
    memory_categories: dict[str, int] = field(default_factory=dict)
    memory_type_distribution: dict[str, int] = field(default_factory=dict)
    recent_entries: list[RecentEntry] = field(default_factory=list)


@dataclass
class GlobalMemoryStats:
    entry_count: int = 0
    categories: dict[str, int] = field(default_factory=dict)
    type_distribution: dict[str, int] = field(default_factory=dict)


@dataclass
class RecentEntry:
    engram_name: str
    category: str
    timestamp: str
    memory_type: str
    summary: str


@dataclass
class StatsReport:
    total_engrams: int = 0
    engram_stats: list[EngramStats] = field(default_factory=list)
    global_memory: GlobalMemoryStats = field(default_factory=GlobalMemoryStats)
    recent_entries: list[RecentEntry] = field(default_factory=list)
    total_memory_entries: int = 0
    total_knowledge_files: int = 0
    total_examples_files: int = 0
    packs_dirs: list[str] = field(default_factory=list)


def _scan_memory_index(
    memory_dir: Path,
    es: EngramStats,
    engram_name: str,
    all_recent: list[RecentEntry],
) -> None:
    index_file = EngramLoader._pick_memory_index_source(memory_dir)
    if index_file is None:
        return
    try:
        lines = index_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return

    for line in lines:
        parsed = EngramLoader._parse_index_entry(line)
        if parsed is None:
            continue
        cat = parsed["category"]
        mtype = parsed["memory_type"]
        es.memory_categories[cat] = es.memory_categories.get(cat, 0) + 1
        es.memory_type_distribution[mtype] = (
            es.memory_type_distribution.get(mtype, 0) + 1
        )
        es.memory_entry_count += 1
        all_recent.append(
            RecentEntry(
                engram_name=engram_name,
                category=cat,
                timestamp=parsed["timestamp"],
                memory_type=mtype,
                summary=parsed["summary"],
            )
        )
        es.recent_entries.append(
            RecentEntry(
                engram_name=engram_name,
                category=cat,
                timestamp=parsed["timestamp"],
                memory_type=mtype,
                summary=parsed["summary"],
            )
        )


def _scan_global_memory(
    loader: EngramLoader,
    report: StatsReport,
    all_recent: list[RecentEntry],
) -> None:
    global_dir = loader._global_memory_dir()
    index_file = EngramLoader._pick_memory_index_source(global_dir)
    if index_file is None:
        return
    try:
        lines = index_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return

    gm = report.global_memory
    for line in lines:
        parsed = EngramLoader._parse_index_entry(line)
        if parsed is None:
            continue
        cat = parsed["category"]
        mtype = parsed["memory_type"]
        gm.categories[cat] = gm.categories.get(cat, 0) + 1
        gm.type_distribution[mtype] = gm.type_distribution.get(mtype, 0) + 1
        gm.entry_count += 1
        all_recent.append(
            RecentEntry(
                engram_name="_global",
                category=cat,
                timestamp=parsed["timestamp"],
                memory_type=mtype,
                summary=parsed["summary"],
            )
        )


def gather_stats(loader: EngramLoader) -> StatsReport:
    report = StatsReport(packs_dirs=[str(d) for d in loader.packs_dirs])
    engrams = loader.list_engrams()
    report.total_engrams = len(engrams)

    all_recent: list[RecentEntry] = []

    for engram_info in engrams:
        name = engram_info["name"]
        es = EngramStats(
            name=name,
            description=engram_info.get("description", ""),
            knowledge_count=engram_info.get("knowledge_count", 0),
            examples_count=engram_info.get("examples_count", 0),
        )

        engram_dir = loader._resolve_engram_dir(name)
        if engram_dir is not None:
            memory_dir = engram_dir / "memory"
            _scan_memory_index(memory_dir, es, name, all_recent)
            es.recent_entries.sort(key=lambda e: e.timestamp, reverse=True)

        report.engram_stats.append(es)
        report.total_knowledge_files += es.knowledge_count
        report.total_examples_files += es.examples_count
        report.total_memory_entries += es.memory_entry_count

    _scan_global_memory(loader, report, all_recent)

    all_recent.sort(key=lambda e: e.timestamp, reverse=True)
    report.recent_entries = all_recent[:10]

    return report


def render_plain(report: StatsReport) -> str:
    lines: list[str] = []
    lines.append("Engram Stats")
    lines.append("=" * 50)
    lines.append(f"Packs dirs: {', '.join(report.packs_dirs)}")
    lines.append(f"Total engrams: {report.total_engrams}")
    lines.append(f"Total knowledge files: {report.total_knowledge_files}")
    lines.append(f"Total examples files: {report.total_examples_files}")
    lines.append(f"Total memory entries: {report.total_memory_entries}")
    lines.append("")

    lines.append("Per-Engram Breakdown:")
    lines.append(f"  {'Name':<25} {'Knowledge':>9} {'Examples':>8} {'Memory':>6}")
    lines.append(f"  {'-' * 25} {'-' * 9} {'-' * 8} {'-' * 6}")
    for es in report.engram_stats:
        lines.append(
            f"  {es.name:<25} {es.knowledge_count:>9} "
            f"{es.examples_count:>8} {es.memory_entry_count:>6}"
        )
    lines.append("")

    all_types: dict[str, int] = {}
    for es in report.engram_stats:
        for t, c in es.memory_type_distribution.items():
            all_types[t] = all_types.get(t, 0) + c
    if all_types:
        lines.append("Memory Type Distribution:")
        for t, c in sorted(all_types.items(), key=lambda x: -x[1]):
            lines.append(f"  {t:<15} {c}")
        lines.append("")

    gm = report.global_memory
    if gm.entry_count > 0:
        lines.append(f"Global Memory: {gm.entry_count} entries")
        for cat, count in sorted(gm.categories.items()):
            lines.append(f"  {cat}: {count}")
        lines.append("")

    if report.recent_entries:
        lines.append("Recent Activity (last 10):")
        for entry in report.recent_entries:
            lines.append(
                f"  [{entry.timestamp}] {entry.engram_name}/{entry.category} "
                f"[{entry.memory_type}] {entry.summary}"
            )

    return "\n".join(lines)


def render_json(report: StatsReport) -> str:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "engrams": [],
        "global_memory": {
            "entry_count": report.global_memory.entry_count,
            "categories": report.global_memory.categories,
            "type_distribution": report.global_memory.type_distribution,
        },
    }

    for es in report.engram_stats:
        payload["engrams"].append(
            {
                "name": es.name,
                "knowledge_count": es.knowledge_count,
                "examples_count": es.examples_count,
                "memory_count": es.memory_entry_count,
                "memory_types": es.memory_type_distribution,
                "recent_entries": [
                    {
                        "category": entry.category,
                        "timestamp": entry.timestamp,
                        "memory_type": entry.memory_type,
                        "summary": entry.summary,
                    }
                    for entry in es.recent_entries[:5]
                ],
            }
        )

    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_csv(report: StatsReport) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "name",
            "knowledge_count",
            "examples_count",
            "memory_count",
            "fact",
            "preference",
            "decision",
            "history",
            "general",
            "inferred",
            "stated",
            "recent_date",
        ]
    )

    for es in report.engram_stats:
        dist = es.memory_type_distribution
        writer.writerow(
            [
                es.name,
                es.knowledge_count,
                es.examples_count,
                es.memory_entry_count,
                dist.get("fact", 0),
                dist.get("preference", 0),
                dist.get("decision", 0),
                dist.get("history", 0),
                dist.get("general", 0),
                dist.get("inferred", 0),
                dist.get("stated", 0),
                es.recent_entries[0].timestamp if es.recent_entries else "",
            ]
        )

    return output.getvalue()


def render_tui(report: StatsReport) -> None:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    console = Console()

    # Summary panel
    summary = Text()
    summary.append("Packs dirs: ", style="dim")
    summary.append(", ".join(report.packs_dirs) + "\n")
    summary.append(f"Engrams: {report.total_engrams}  ", style="cyan")
    summary.append(f"Knowledge: {report.total_knowledge_files}  ", style="green")
    summary.append(f"Examples: {report.total_examples_files}  ", style="green")
    summary.append(f"Memories: {report.total_memory_entries}", style="yellow")
    console.print(Panel(summary, title="Engram Stats", border_style="blue"))

    # Per-engram table
    table = Table(title="Per-Engram Breakdown")
    table.add_column("Name", style="cyan")
    table.add_column("Description", max_width=35)
    table.add_column("Knowledge", justify="right", style="green")
    table.add_column("Examples", justify="right", style="green")
    table.add_column("Memory", justify="right", style="yellow")
    table.add_column("Categories", max_width=40)
    for es in report.engram_stats:
        cats = ", ".join(
            f"{k}({v})" for k, v in sorted(es.memory_categories.items())
        )
        table.add_row(
            es.name,
            es.description[:35],
            str(es.knowledge_count),
            str(es.examples_count),
            str(es.memory_entry_count),
            cats or "-",
        )
    console.print(table)

    # Memory type distribution
    all_types: dict[str, int] = {}
    for es in report.engram_stats:
        for t, c in es.memory_type_distribution.items():
            all_types[t] = all_types.get(t, 0) + c
    if all_types:
        type_table = Table(title="Memory Type Distribution")
        type_table.add_column("Type", style="magenta")
        type_table.add_column("Count", justify="right")
        for t, c in sorted(all_types.items(), key=lambda x: -x[1]):
            type_table.add_row(t, str(c))
        console.print(type_table)

    # Global memory
    gm = report.global_memory
    if gm.entry_count > 0:
        gm_text = Text()
        gm_text.append(f"Total: {gm.entry_count} entries\n", style="bold")
        for cat, count in sorted(gm.categories.items()):
            gm_text.append(f"  {cat}: {count}\n")
        console.print(Panel(gm_text, title="Global Memory", border_style="green"))

    # Recent activity
    if report.recent_entries:
        recent_table = Table(title="Recent Activity")
        recent_table.add_column("Timestamp", style="dim")
        recent_table.add_column("Engram", style="cyan")
        recent_table.add_column("Category")
        recent_table.add_column("Type", style="magenta")
        recent_table.add_column("Summary")
        for entry in report.recent_entries:
            recent_table.add_row(
                entry.timestamp,
                entry.engram_name,
                entry.category,
                entry.memory_type,
                entry.summary,
            )
        console.print(recent_table)
