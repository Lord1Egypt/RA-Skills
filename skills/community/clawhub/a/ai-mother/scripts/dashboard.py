#!/usr/bin/env python3
"""
AI Mother TUI Dashboard
Real-time monitoring of all AI agents with rich terminal UI
"""
import subprocess
import json
import time
import sys
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.layout import Layout
except ImportError:
    print("❌ Missing 'rich' library. Install with: pip3 install rich")
    sys.exit(1)

SKILL_DIR = Path.home() / ".openclaw/skills/ai-mother"
STATE_FILE = SKILL_DIR / "ai-state.txt"
PATROL_SCRIPT = SKILL_DIR / "scripts/patrol.sh"

console = Console()

def run_patrol():
    """Run patrol script and return output"""
    try:
        result = subprocess.run(
            [str(PATROL_SCRIPT), "--quiet"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def parse_state_file():
    """Parse ai-state.txt and return list of agents"""
    if not STATE_FILE.exists():
        return []
    
    agents = []
    with open(STATE_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) >= 7:
                agents.append({
                    'pid': parts[0],
                    'type': parts[1],
                    'workdir': parts[2],
                    'task': parts[3],
                    'status': parts[4],
                    'last_check': int(parts[5]),
                    'notes': parts[6]
                })
    return agents

def get_status_emoji(status):
    """Return emoji for status"""
    emoji_map = {
        'active': '✅',
        'idle': '💤',
        'waiting_input': '💬',
        'waiting_api': '🚫',
        'error': '❌',
        'stopped': '⚠️',
        'zombie': '💀',
        'completed': '🎉'
    }
    return emoji_map.get(status, '❓')

def format_time_ago(timestamp):
    """Format timestamp as 'X minutes ago'"""
    now = int(time.time())
    diff = now - timestamp
    if diff < 60:
        return f"{diff}s ago"
    elif diff < 3600:
        return f"{diff // 60}m ago"
    elif diff < 86400:
        return f"{diff // 3600}h ago"
    else:
        return f"{diff // 86400}d ago"

def generate_dashboard():
    """Generate dashboard layout"""
    agents = parse_state_file()
    
    # Header
    header = Panel(
        "[bold cyan]👩‍👧‍👦 AI Mother Dashboard[/bold cyan]\n"
        f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]",
        style="cyan"
    )
    
    # Agents table
    table = Table(title=f"Active AI Agents ({len(agents)})", show_header=True, header_style="bold magenta")
    table.add_column("PID", style="cyan", width=8)
    table.add_column("Type", style="green", width=10)
    table.add_column("Status", width=12)
    table.add_column("Project", style="blue", width=40)
    table.add_column("Last Check", style="yellow", width=12)
    table.add_column("Notes", style="dim", width=30)
    
    if not agents:
        table.add_row("—", "—", "—", "—", "—", "No AI agents running")
    else:
        for agent in agents:
            status_emoji = get_status_emoji(agent['status'])
            status_text = f"{status_emoji} {agent['status']}"
            workdir_short = agent['workdir'].replace(str(Path.home()), '~')
            if len(workdir_short) > 40:
                workdir_short = '...' + workdir_short[-37:]
            
            table.add_row(
                agent['pid'],
                agent['type'],
                status_text,
                workdir_short,
                format_time_ago(agent['last_check']),
                agent['notes'][:30]
            )
    
    # Summary
    status_counts = {}
    for agent in agents:
        status_counts[agent['status']] = status_counts.get(agent['status'], 0) + 1
    
    summary_text = " | ".join([f"{get_status_emoji(s)} {s}: {c}" for s, c in status_counts.items()])
    if not summary_text:
        summary_text = "No agents"
    
    summary = Panel(summary_text, title="Summary", style="green")
    
    # Layout
    layout = Layout()
    layout.split_column(
        Layout(header, size=3),
        Layout(table),
        Layout(summary, size=3)
    )
    
    return layout

def main():
    """Main dashboard loop"""
    console.clear()
    console.print("[bold cyan]👩‍👧‍👦 AI Mother Dashboard[/bold cyan]")
    console.print("[dim]Loading...[/dim]\n")
    
    # Run initial patrol
    console.print("Running patrol scan...")
    run_patrol()
    
    try:
        with Live(generate_dashboard(), refresh_per_second=0.5, console=console) as live:
            while True:
                time.sleep(5)  # Refresh every 5 seconds
                live.update(generate_dashboard())
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard closed.[/yellow]")

if __name__ == "__main__":
    main()
