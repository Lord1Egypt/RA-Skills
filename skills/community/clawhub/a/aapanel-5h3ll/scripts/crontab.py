#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "pyyaml>=6.0",
#   "rich>=13.0",
# ]
# ///
"""
Scheduled Task Check Script
Checks aaPanel scheduled tasks, focusing on backup tasks
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import compatible with dev and release environments
_skill_root = Path(__file__).parent.parent

if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent / "src"))

from bt_common import (
    BtClient,
    BtClientManager,
    load_config,
)


# task type mapping
TASK_TYPE_MAP = {
    "toShell": "Shell Script",
    "site": "Backup Site",
    "database": "Backup Database",
    "path": "Backup Directory",
    "sync_time": "Sync Time",
    "log": "Rotate Log",
    "rememory": "Free Memory",
    "access": "Access URL",
    "backup": "Backup",
}

# task type classification
BACKUP_TYPES = ["site", "database", "path"]


def parse_crontab_task(task: dict) -> dict:
    """
    Parse scheduled task data

    Args:
        task: Raw task data

    Returns:
        Parsed task info
    """
    s_type = task.get("sType", "")
    task_type = TASK_TYPE_MAP.get(s_type, s_type or "Other")

    # Check if backup task
    is_backup = s_type in BACKUP_TYPES or "backup" in task.get("name", "").lower()

    # Parse execution cycle
    cycle = task.get("cycle", "") or task.get("type_zh", "")

    # Parse execution time
    exec_time = ""
    if task.get("type") == "day":
        hour = task.get("where_hour", 0)
        minute = task.get("where_minute", 0)
        exec_time = f"Daily {hour:02d}:{minute:02d}"
    elif task.get("type") == "hour":
        minute = task.get("where_minute", 0)
        exec_time = f"Hourly at minute {minute:02d}"
    elif task.get("type") == "minute-n":
        interval = task.get("where1", "5")
        exec_time = f"Every {interval} minutes"
    elif task.get("type") == "week":
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_idx = int(task.get("where1", 0))
        hour = task.get("where_hour", 0)
        minute = task.get("where_minute", 0)
        exec_time = f"Every {days[day_idx]} at {hour:02d}:{minute:02d}"
    elif task.get("type") == "month":
        day = task.get("where1", 1)
        hour = task.get("where_hour", 0)
        minute = task.get("where_minute", 0)
        exec_time = f"Monthly on day {day} at {hour:02d}:{minute:02d}"

    return {
        "id": task.get("id"),
        "name": task.get("name", "") or task.get("rname", ""),
        "type": task_type,
        "s_type": s_type,
        "is_backup": is_backup,
        "status": task.get("status", 0) == 1,
        "enabled": task.get("status", 0) == 1,
        "cycle": cycle,
        "exec_time": exec_time,
        "backup_target": task.get("sName", "") if is_backup else "",
        "backup_path": task.get("db_backup_path", "/www/backup"),
        "save_count": task.get("save", 0) if is_backup else None,
        "command": task.get("sBody", ""),
        "user": task.get("user", "root"),
        "addtime": task.get("addtime", ""),
        "type_name": task.get("type_name", ""),
        "result": task.get("result", 0),  # 0=not executed/failed, 1=success
    }


def get_crontab_status(client: BtClient, page: int = 1, limit: int = 100) -> dict:
    """
    Get scheduled task status

    Args:
        client: aaPanel client
        page: Page number
        limit: Items per page

    Returns:
        Scheduled task status info
    """
    result = {
        "server": client.name,
        "timestamp": datetime.now().isoformat(),
        "tasks": [],
        "summary": {
            "total": 0,
            "enabled": 0,
            "disabled": 0,
            "backup_tasks": 0,
            "shell_tasks": 0,
            "other_tasks": 0,
        },
        "backup_tasks": [],
        "alerts": [],
    }

    try:
        response = client.get_crontab_list(page=page, limit=limit)
        tasks = response.get("data", [])

        for task in tasks:
            parsed = parse_crontab_task(task)
            result["tasks"].append(parsed)

            # Statistics
            result["summary"]["total"] += 1
            if parsed["enabled"]:
                result["summary"]["enabled"] += 1
            else:
                result["summary"]["disabled"] += 1
                result["alerts"].append({
                    "level": "warning",
                    "type": "crontab",
                    "message": f"Task [{parsed['name']}] is disabled",
                    "task_id": parsed["id"],
                })

            if parsed["is_backup"]:
                result["summary"]["backup_tasks"] += 1
                result["backup_tasks"].append(parsed)
            elif parsed["s_type"] == "toShell":
                result["summary"]["shell_tasks"] += 1
            else:
                result["summary"]["other_tasks"] += 1

    except Exception as e:
        result["error"] = str(e)
        result["alerts"].append({
            "level": "critical",
            "type": "connection",
            "message": f"Failed to get scheduled tasks: {e}",
        })

    return result


def get_backup_task_logs(client: BtClient, task_id: int, days: int = 7) -> dict:
    """
    Get backup task logs

    Args:
        client: aaPanel client
        task_id: Task ID
        days: Query days

    Returns:
        Task log info
    """
    result = {
        "server": client.name,
        "task_id": task_id,
        "timestamp": datetime.now().isoformat(),
        "logs": [],
        "last_status": None,
        "alerts": [],
    }

    try:
        # Calculate time range
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - (days * 24 * 60 * 60)

        response = client.get_crontab_logs(
            task_id=task_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

        if response.get("status"):
            log_content = response.get("msg", "")
            result["logs"] = parse_backup_log(log_content)

            # Analyze last execution status
            if result["logs"]:
                last_log = result["logs"][-1]
                result["last_status"] = last_log.get("status")
                if last_log.get("status") == "failed":
                    result["alerts"].append({
                        "level": "warning",
                        "type": "backup",
                        "message": f"Last backup task execution failed: {last_log.get('message', '')}",
                    })
        else:
            result["error"] = response.get("msg", "Failed to get logs")

    except Exception as e:
        result["error"] = str(e)

    return result


def parse_backup_log(log_content: str) -> list:
    """
    Parse backup log

    Args:
        log_content: Log content

    Returns:
        Parsed log list
    """
    logs = []

    # Split by execution blocks
    blocks = re.split(r"={10,}", log_content)

    for block in blocks:
        if not block.strip():
            continue

        log_entry = {
            "time": "",
            "status": "unknown",
            "message": "",
            "details": [],
        }

        # Extract time
# Pattern to match btpanel backup log start marker (btpanel logs are in Chinese)
        time_match = re.search(r"backup_start_marker\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", block)
        if time_match:
            log_entry["time"] = time_match.group(1)

        # Extract status
        if "Successful" in block:
            log_entry["status"] = "success"
        elif "Failed" in block:
            log_entry["status"] = "failed"

        # Extract details
        lines = block.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("|-"):
                log_entry["details"].append(line[2:])

        # Extract backup file path
# Pattern to match btpanel backup path output (btpanel logs are in Chinese)
        file_match = re.search(r"(?:site backed up to|backup_to_marker)：(.+\.tar\.gz)", block)
        if file_match:
            log_entry["backup_file"] = file_match.group(1)

        if log_entry["time"] or log_entry["status"] != "unknown":
            logs.append(log_entry)

    return logs


def run_crontab_check(manager: BtClientManager, server: Optional[str] = None,
                      backup_only: bool = False) -> dict:
    """
    Execute scheduled task check

    Args:
        manager: Client manager
        server: Specify server name
        backup_only: Only return backup tasks

    Returns:
        Check results
    """
    # Single server
    if server:
        client = manager.get_client(server)
        result = get_crontab_status(client)
        if backup_only:
            result["tasks"] = [t for t in result["tasks"] if t["is_backup"]]
        return result

    # All servers
    all_clients = manager.get_all_clients()
    results = {
        "timestamp": datetime.now().isoformat(),
        "servers": [],
        "summary": {
            "total_servers": 0,
            "total_tasks": 0,
            "total_backup_tasks": 0,
            "total_enabled": 0,
            "total_disabled": 0,
        },
        "alerts": [],
    }

    for name, client in all_clients.items():
        try:
            server_result = get_crontab_status(client)
            if backup_only:
                server_result["tasks"] = [t for t in server_result["tasks"] if t["is_backup"]]

            results["servers"].append(server_result)

            # Summary
            summary = server_result.get("summary", {})
            results["summary"]["total_servers"] += 1
            results["summary"]["total_tasks"] += summary.get("total", 0)
            results["summary"]["total_backup_tasks"] += summary.get("backup_tasks", 0)
            results["summary"]["total_enabled"] += summary.get("enabled", 0)
            results["summary"]["total_disabled"] += summary.get("disabled", 0)

            # Collect alerts
            for alert in server_result.get("alerts", []):
                alert["server"] = name
                results["alerts"].append(alert)

        except Exception as e:
            results["servers"].append({
                "server": name,
                "error": str(e),
                "alerts": [{"level": "critical", "type": "connection", "message": str(e)}],
            })

    return results


def print_crontab_table(results: dict, backup_only: bool = False):
    """Print table-formatted output"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        if "servers" in results and len(results["servers"]) > 1:
            # Multi-server mode
            for server_data in results["servers"]:
                if "error" in server_data:
                    console.print(f"[red]Server {server_data.get('server', 'Unknown')} error: {server_data['error']}[/red]")
                    continue

                server_name = server_data.get("server", "Unknown")
                summary = server_data.get("summary", {})

                console.print(f"\n[bold cyan]═══ {server_name} ═══[/bold cyan]")

                # Task list
                tasks = server_data.get("tasks", [])
                if tasks:
                    table = Table(show_header=True, header_style="bold")
                    table.add_column("Name", style="cyan", width=30)
                    table.add_column("Type", width=12)
                    table.add_column("Status", width=8)
                    table.add_column("Execution Time", width=20)
                    table.add_column("Backup Target", width=15)

                    for task in tasks:
                        # status
                        if task["enabled"]:
                            status_str = "[green]Enabled[/green]"
                        else:
                            status_str = "[red]Disabled[/red]"

                        # Backup target
                        backup_target = task.get("backup_target", "") or ""

                        table.add_row(
                            task.get("name", "-")[:30],
                            task.get("type", "-"),
                            status_str,
                            task.get("exec_time", "-")[:20],
                            backup_target[:15],
                        )

                    console.print(table)
                else:
                    console.print("[yellow]No scheduled tasks[/yellow]")

                # Summary
                console.print(f"\n[dim]Summary: "
                             f"Total {summary.get('total', 0)}, "
                             f"[green]Enabled {summary.get('enabled', 0)}[/green], "
                             f"[red]Disabled {summary.get('disabled', 0)}[/red], "
                             f"Backup tasks {summary.get('backup_tasks', 0)}[/dim]")

                # Alerts
                alerts = server_data.get("alerts", [])
                if alerts:
                    console.print("\n[yellow]Alerts:[/yellow]")
                    for alert in alerts[:5]:
                        level = alert.get("level", "warning")
                        color = "red" if level == "critical" else "yellow"
                        console.print(f"  [{color}]• {alert.get('message', '')}[/{color}]")

            # Total summary
            summary = results.get("summary", {})
            console.print(f"\n[bold]Total Summary:[/bold] "
                         f"Servers: {summary.get('total_servers', 0)}, "
                         f"Total tasks: {summary.get('total_tasks', 0)}, "
                         f"[green]Enabled: {summary.get('total_enabled', 0)}[/green], "
                         f"[red]Disabled: {summary.get('total_disabled', 0)}[/red], "
                         f"Backup tasks: {summary.get('total_backup_tasks', 0)}")

        else:
            # Single server mode
            server_name = results.get("server", "Unknown")
            summary = results.get("summary", {})

            console.print(Panel(f"[bold]{server_name} - Scheduled Tasks[/bold]", title="Server"))

            tasks = results.get("tasks", [])
            if tasks:
                table = Table(show_header=True, header_style="bold")
                table.add_column("ID", width=6)
                table.add_column("Name", style="cyan")
                table.add_column("Type")
                table.add_column("Status")
                table.add_column("Execution Time")
                table.add_column("Backup Target")
                table.add_column("Retention")

                for task in tasks:
                    # status
                    if task["enabled"]:
                        status_str = "[green]Enabled[/green]"
                    else:
                        status_str = "[red]Disabled[/red]"

                    # Retention count
                    save_count = task.get("save_count")
                    save_str = str(save_count) if save_count is not None else "-"

                    table.add_row(
                        str(task.get("id", "-")),
                        task.get("name", "-")[:25],
                        task.get("type", "-"),
                        status_str,
                        task.get("exec_time", "-"),
                        task.get("backup_target", "")[:15] or "-",
                        save_str,
                    )

                console.print(table)
            else:
                console.print("[yellow]No scheduled tasks[/yellow]")

            # Summary
            console.print(f"\n[bold]Summary:[/bold]")
            console.print(f"  Total: {summary.get('total', 0)}")
            console.print(f"  [green]Enabled: {summary.get('enabled', 0)}[/green]")
            console.print(f"  [red]Disabled: {summary.get('disabled', 0)}[/red]")
            console.print(f"  Backup tasks: {summary.get('backup_tasks', 0)}")
            console.print(f"  Shell tasks: {summary.get('shell_tasks', 0)}")
            console.print(f"  Other tasks: {summary.get('other_tasks', 0)}")

            # Alerts
            alerts = results.get("alerts", [])
            if alerts:
                console.print(f"\n[bold yellow]Alerts ({len(alerts)}):[/bold yellow]")
                for alert in alerts:
                    level = alert.get("level", "warning")
                    color = "red" if level == "critical" else "yellow"
                    console.print(f"  [{color}]• {alert.get('message', '')}[/{color}]")

    except ImportError:
        print("Please install rich library for table output: pip install rich")
        print(json.dumps(results, ensure_ascii=False, indent=2))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="aaPanel Scheduled Task Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View all scheduled tasks
  %(prog)s

  # View only backup tasks
  %(prog)s --backup-only

  # View specific server
  %(prog)s --server prod-01

  # View backup task logs
  %(prog)s --logs --task-id 11

  # JSON format output
  %(prog)s --format json
        """,
    )
    parser.add_argument("--server", "-s", help="Specify server name")
    parser.add_argument("--backup-only", action="store_true", help="Show only backup tasks")
    parser.add_argument("--logs", action="store_true", help="View task logs")
    parser.add_argument("--task-id", type=int, help="Task ID (use with --logs)")
    parser.add_argument("--days", type=int, default=7, help="Log query days (default 7)")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="table", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--config", "-c", help="Config file path")

    args = parser.parse_args()

    # Initialize client manager
    manager = BtClientManager()

    try:
        manager.load_config(args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please configure server first: bt-config.py add", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)

    if not manager.get_all_clients():
        print("Error: No servers configured", file=sys.stderr)
        sys.exit(1)

    try:
        if args.logs and args.task_id:
            # View task logs
            if args.server:
                client = manager.get_client(args.server)
            else:
                # Get first server
                client = list(manager.get_all_clients().values())[0]

            results = get_backup_task_logs(client, args.task_id, args.days)
        else:
            # View task list
            results = run_crontab_check(manager, args.server, args.backup_only)

    except KeyError as e:
        print(f"Error: Server not found {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Check failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Output result
    if args.format == "json":
        output = json.dumps(results, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Result saved to: {args.output}")
        else:
            print(output)
    else:
        if args.logs:
            # Log output
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_crontab_table(results, args.backup_only)


if __name__ == "__main__":
    main()
