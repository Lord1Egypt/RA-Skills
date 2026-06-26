#!/usr/bin/env python3
"""War Room Monitor — live TUI that watches project memory files.

Usage:
    python skills/war-room/monitor.py --project projects/my-idea/
    python skills/war-room/monitor.py --project projects/my-idea/ --refresh 1.0

Spawned automatically by the war-room skill at session start.
Requires: pip install rich
"""
import argparse
import re
import time
from datetime import datetime
from pathlib import Path

try:
    from rich import box
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
except ImportError:
    print("rich is required: pip install rich")
    raise SystemExit(1)

# ── Persona colour map ────────────────────────────────────────────────────────

PERSONA_COLORS = {
    "maya chen":      "cyan",
    "robert ashford": "yellow",
    "priya nair":     "green",
    "james park":     "magenta",
}

def color_for(name: str) -> str:
    key = name.lower()
    for fragment, color in PERSONA_COLORS.items():
        if fragment in key:
            return color
    return "white"

# ── File parsers ──────────────────────────────────────────────────────────────

def parse_turns(log_path: Path) -> list[dict]:
    if not log_path.exists():
        return []
    turns = []
    for block in re.split(r'\n---\n', log_path.read_text()):
        block = block.strip()
        m = re.match(r'\*\*\[Round (\d+)\] (.+?)\*\*\n(.*)', block, re.DOTALL)
        if m:
            turns.append({
                "round":   int(m.group(1)),
                "persona": m.group(2).strip(),
                "text":    m.group(3).strip(),
            })
    return turns

def parse_summary(summary_path: Path) -> dict:
    if not summary_path.exists():
        return {}
    content = summary_path.read_text()
    result = {}
    for key, pattern in [("status", r'\*\*Status\*\*:\s*(.+)'),
                          ("phase",  r'[Pp]hase\s*(\d+)'),
                          ("next",   r'## Resume From\n(.+)')]:
        m = re.search(pattern, content)
        if m:
            result[key] = m.group(1).strip()
    return result

def parse_drift(private_dir: Path) -> dict[int, str]:
    if not private_dir.exists():
        return {}
    flags = {}
    for memo in sorted(private_dir.glob("agent-*-memo.md")):
        m = re.search(r'agent-(\d+)', memo.name)
        if not m:
            continue
        matches = re.findall(r'\*\*Drift flag\*\*:\s*(yes|no)', memo.read_text(), re.I)
        if matches:
            flags[int(m.group(1))] = matches[-1].lower()
    return flags

def tag_style(text: str) -> tuple[str, str]:
    """Return (tag_text, color) for the consensus tag at end of a turn."""
    m = re.search(r'\[(AGREE|PASS|OBJECT[^\]]*)\]\s*$', text)
    if not m:
        return "", "white"
    tag = m.group(1)
    color = "green" if tag == "AGREE" else ("yellow" if tag == "PASS" else "red")
    return f"[{tag}]", color

# ── Layout builder ────────────────────────────────────────────────────────────

def build(project_path: Path) -> Layout:
    mem       = project_path / "memory"
    war_room  = mem / "war-room"
    private   = mem / ".private"

    turns   = parse_turns(war_room / "discussion-log.md")
    summary = parse_summary(mem / "SUMMARY.md")
    drift   = parse_drift(private)

    # ── Header ────────────────────────────────────────────────────────────────
    current_round = max((t["round"] for t in turns), default=0)
    status  = summary.get("status", "waiting")
    phase   = summary.get("phase", "—")
    header  = Panel(
        f"[bold white]War Room[/bold white]  ·  "
        f"[cyan]{project_path.name}[/cyan]  ·  "
        f"phase [yellow]{phase}[/yellow]  ·  "
        f"round [yellow]{current_round}[/yellow]  ·  "
        f"[green]{status}[/green]  ·  "
        f"[dim]{datetime.now().strftime('%H:%M:%S')}[/dim]",
        box=box.HORIZONTALS,
    )

    # ── Transcript (last 8 turns) ─────────────────────────────────────────────
    lines = []
    for t in (turns[-8:] if len(turns) > 8 else turns):
        c = color_for(t["persona"])
        tag, tc = tag_style(t["text"])
        body = t["text"][:280].replace('\n', ' ')
        if tag:
            body = re.sub(r'\[(?:AGREE|PASS|OBJECT[^\]]*)\]\s*$', '', body).strip()
        lines.append(
            f"[{c}][R{t['round']}] {t['persona']}[/{c}]  "
            f"[dim]{body}[/dim]"
            + (f"  [bold {tc}]{tag}[/bold {tc}]" if tag else "")
        )
    transcript = Panel(
        "\n\n".join(lines) if lines else "[dim]Waiting for first turn…[/dim]",
        title="[bold]Discussion[/bold]",
        box=box.ROUNDED,
    )

    # ── Drift table ───────────────────────────────────────────────────────────
    drift_table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    drift_table.add_column("Agent", style="dim")
    drift_table.add_column("Drift")
    for idx in sorted(drift):
        flag  = drift[idx]
        color = "red bold" if flag == "yes" else "green"
        drift_table.add_row(f"agent-{idx}", f"[{color}]{flag}[/{color}]")
    drift_panel = Panel(
        drift_table if drift else "[dim]No memos yet[/dim]",
        title="[bold]Persona Drift[/bold]",
        box=box.ROUNDED,
    )

    # ── Idea snapshot ─────────────────────────────────────────────────────────
    snap_path = war_room / "idea-snapshot.md"
    snap_text = snap_path.read_text()[:600].strip() if snap_path.exists() else "[dim]Not yet written[/dim]"
    snapshot  = Panel(snap_text, title="[bold]Idea Snapshot[/bold]", box=box.ROUNDED)

    # ── Assemble ──────────────────────────────────────────────────────────────
    layout = Layout()
    layout.split_column(
        Layout(header,   size=3),
        Layout(name="body"),
        Layout(snapshot, size=12),
    )
    layout["body"].split_row(
        Layout(transcript, ratio=3),
        Layout(drift_panel, ratio=1),
    )
    return layout

# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="War Room live monitor")
    parser.add_argument("--project", required=True, help="Path to project folder")
    parser.add_argument("--refresh", type=float, default=2.0, help="Refresh interval in seconds")
    args = parser.parse_args()

    project_path = Path(args.project)
    console = Console()

    with Live(build(project_path), refresh_per_second=1, screen=True, console=console) as live:
        while True:
            time.sleep(args.refresh)
            try:
                live.update(build(project_path))
            except KeyboardInterrupt:
                break
            except Exception:
                pass

if __name__ == "__main__":
    main()
