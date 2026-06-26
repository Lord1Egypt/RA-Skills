#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "pyyaml>=6.0",
#   "rich>=13.0",
# ]
# ///
"""
System Resource Monitor Script
Monitors CPU, memory, disk, and network usage
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Optional

# Import compatible with dev and release environments
# release environment: bt_common/ (scripts in scripts/)
# dev environment: src/bt_common/ (scripts in src/btpanel/scripts/)
_skill_root = Path(__file__).parent.parent  # skill package root directory

# Prioritize release environment (skill package root), then dev environment
if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent / "src"))

from bt_common import (
    BtClient,
    BtClientManager,
    check_thresholds,
    parse_system_monitor_data,
    load_config,
)


def get_server_system_status(client: BtClient, thresholds: dict) -> dict:
    """
    Get single server's system status

    Args:
        client: aaPanel client
        thresholds: Alert threshold config

    Returns:
        System status info
    """
    # Get system status (GetNetWork API returns complete monitor data)
    status_data = client.get_system_status()

    # Parse data
    formatted = parse_system_monitor_data(status_data, client.name)

    # Check alerts
    alerts = check_thresholds(formatted, thresholds)

    result = formatted
    result["alerts"] = [asdict(a) if hasattr(a, "__dataclass_fields__") else a for a in alerts]
    return result


def run_monitor(manager: BtClientManager, server: Optional[str] = None) -> dict:
    """
    Execute system monitor

    Args:
        manager: Client manager
        server: Specify server name

    Returns:
        Monitor results
    """
    from datetime import datetime

    thresholds = manager.get_global_config().get("thresholds", {"cpu": 80, "memory": 85, "disk": 90})

    # Single server
    if server:
        client = manager.get_client(server)
        return get_server_system_status(client, thresholds)

    # All servers
    all_clients = manager.get_all_clients()
    results = {
        "timestamp": datetime.now().isoformat(),
        "servers": [],
        "summary": {"total": len(all_clients), "healthy": 0, "warning": 0, "critical": 0},
    }

    for name, client in all_clients.items():
        try:
            status = get_server_system_status(client, thresholds)
            results["servers"].append(status)

            # Statistics health status
            alerts = status.get("alerts", [])
            if not alerts:
                results["summary"]["healthy"] += 1
            else:
                has_critical = any(a.get("level") == "critical" for a in alerts)
                if has_critical:
                    results["summary"]["critical"] += 1
                else:
                    results["summary"]["warning"] += 1

        except Exception as e:
            results["servers"].append(
                {
                    "server": name,
                    "error": str(e),
                    "alerts": [{"level": "critical", "type": "connection", "message": str(e)}],
                }
            )
            results["summary"]["critical"] += 1

    return results


def print_table_output(results: dict):
    """Print table-formatted output"""
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()

        if "servers" in results:
            # Multi-server mode
            table = Table(title="System Resource Monitor")
            table.add_column("Server", style="cyan")
            table.add_column("System", style="white")
            table.add_column("CPU", style="green")
            table.add_column("Memory", style="yellow")
            table.add_column("Disk", style="red")
            table.add_column("Status", style="bold")

            for server in results["servers"]:
                if "error" in server:
                    table.add_row(
                        server["server"],
                        "-",
                        "-",
                        "-",
                        "-",
                        "[red]Connection failed[/red]",
                    )
                    continue

                cpu = server.get("cpu", {})
                memory = server.get("memory", {})
                disk = server.get("disk", {})

                # Determine status color
                alerts = server.get("alerts", [])
                if not alerts:
                    status = "[green]Normal[/green]"
                elif any(a.get("level") == "critical" for a in alerts):
                    status = "[red]Error[/red]"
                else:
                    status = "[yellow]Warning[/yellow]"

                table.add_row(
                    server.get("server", "Unknown"),
                    server.get("simple_system", server.get("system", "-")),
                    f"{cpu.get('usage', 0):.1f}%",
                    f"{memory.get('percent', 0):.1f}%",
                    f"{disk.get('percent', 0):.1f}%",
                    status,
                )

            console.print(table)

            # Print summary
            summary = results.get("summary", {})
            console.print(
                f"\nSummary: [green]Normal {summary.get('healthy', 0)}[/green], "
                f"[yellow]Warning {summary.get('warning', 0)}[/yellow], "
                f"[red]Error {summary.get('critical', 0)}[/red]"
            )
        else:
            # Single server mode
            server_name = results.get("server", "Unknown")
            table = Table(title=f"Server: {server_name}")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            cpu = results.get("cpu", {})
            memory = results.get("memory", {})
            disk = results.get("disk", {})
            load = results.get("load", {})
            network = results.get("network", {})

            table.add_row("System", results.get("system", "Unknown"))
            table.add_row("Hostname", results.get("hostname", "Unknown"))
            table.add_row("Uptime", results.get("uptime", "Unknown"))
            table.add_row("Panel Version", results.get("version", "Unknown"))
            table.add_row("", "")
            table.add_row("[bold]CPU[/bold]", "")
            table.add_row("  Usage", f"{cpu.get('usage', 0):.1f}%")
            table.add_row("  Cores", str(cpu.get("cores", 1)))
            table.add_row("  Model", str(cpu.get("model", "Unknown")))
            table.add_row("", "")
            table.add_row("[bold]Memory[/bold]", "")
            table.add_row("  Used", f"{memory.get('used_mb', 0)}/{memory.get('total_mb', 0)} MB")
            table.add_row("  Usage", f"{memory.get('percent', 0):.1f}%")
            table.add_row("  Available", f"{memory.get('available_mb', 0)} MB")
            table.add_row("", "")
            table.add_row("[bold]Disk[/bold]", "")
            table.add_row("  Used", f"{disk.get('used_human', '0')}/{disk.get('total_human', '0')}")
            table.add_row("  Usage", f"{disk.get('percent', 0):.1f}%")
            table.add_row("", "")
            table.add_row("[bold]Load[/bold]", "")
            table.add_row("  1 minute", f"{load.get('one_minute', 0):.2f}")
            table.add_row("  5 minutes", f"{load.get('five_minute', 0):.2f}")
            table.add_row("  15 minutes", f"{load.get('fifteen_minute', 0):.2f}")
            table.add_row("", "")
            table.add_row("[bold]Network[/bold]", "")
            table.add_row("  Upload", f"{network.get('current_up', 0):.2f} KB/s")
            table.add_row("  Download", f"{network.get('current_down', 0):.2f} KB/s")
            table.add_row("  Total Upload", network.get("total_up", "0"))
            table.add_row("  Total Download", network.get("total_down", "0"))
            table.add_row("", "")
            table.add_row("[bold]Resources[/bold]", "")
            table.add_row("  Sites", str(results.get("resources", {}).get("sites", 0)))
            table.add_row("  Databases", str(results.get("resources", {}).get("databases", 0)))

            console.print(table)

            # Print disk partitions
            disks = disk.get("disks", [])
            if disks:
                disk_table = Table(title="Disk Partitions")
                disk_table.add_column("Mount Point", style="cyan")
                disk_table.add_column("File System", style="white")
                disk_table.add_column("Used", style="green")
                disk_table.add_column("Usage", style="yellow")

                for d in disks:
                    disk_table.add_row(
                        d.get("path", "/"),
                        d.get("filesystem", "-"),
                        f"{d.get('used_human', '0')}/{d.get('total_human', '0')}",
                        f"{d.get('percent', 0):.1f}%",
                    )
                console.print(disk_table)

            # Print alerts
            alerts = results.get("alerts", [])
            if alerts:
                console.print("\n[bold yellow]Alerts:[/bold yellow]")
                for alert in alerts:
                    level = alert.get("level", "warning")
                    color = "red" if level == "critical" else "yellow"
                    console.print(f"  [{color}]{alert.get('message', '')}[/{color}]")

    except ImportError:
        # Without rich library, use simple output
        print("Please install rich library for table output: pip install rich")
        print(json.dumps(results, ensure_ascii=False, indent=2))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="aaPanel System Resource Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor all servers
  %(prog)s

  # Monitor specific server
  %(prog)s --server prod-01

  # JSON format output
  %(prog)s --format json

  # Output to file
  %(prog)s --output report.json
        """,
    )
    parser.add_argument("--server", "-s", help="Specify server name")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="json", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--config", "-c", help="Config file path")

    args = parser.parse_args()

    # Initialize client manager
    manager = BtClientManager()

    try:
        manager.load_config(args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please set BT_CONFIG_PATH environment variable or create config file", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)

    if not manager.get_all_clients():
        print("Error: No servers configured", file=sys.stderr)
        sys.exit(1)

    # Execute monitor
    try:
        results = run_monitor(manager, args.server)
    except KeyError as e:
        print(f"Error: Server not found {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Monitor failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Output result
    if args.format == "table":
        print_table_output(results)
    else:
        output = json.dumps(results, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Result saved to: {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()
