#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "pyyaml>=6.0",
#   "rich>=13.0",
# ]
# ///
"""
Service Status Check Script
Checks services running on the server (Nginx/Apache/PHP/Redis/Memcached, etc.)
"""

import argparse
import json
import sys
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
    SOFTWARE_SERVICES,
    load_config,
)


def get_server_services(client: BtClient, services: Optional[list] = None) -> dict:
    """
    Get single server's service status

    Args:
        client: aaPanel client
        services: List of services to query

    Returns:
        Service status info
    """
    # Get all service status
    service_list = client.get_all_services_status(services)

    # Statistics
    total = len(service_list)
    running = sum(1 for s in service_list if s.get("status"))
    stopped = sum(1 for s in service_list if s.get("installed") and not s.get("status"))
    not_installed = sum(1 for s in service_list if not s.get("installed"))

    # Generate alerts
    alerts = []
    for svc in service_list:
        if svc.get("installed") and not svc.get("status"):
            alerts.append({
                "level": "warning",
                "type": "service",
                "message": f"Service {svc.get('title', svc.get('name'))} has stopped",
                "service": svc.get("name"),
            })
        elif svc.get("error"):
            alerts.append({
                "level": "warning",
                "type": "service",
                "message": f"Service {svc.get('name')} status query failed: {svc.get('error')}",
                "service": svc.get("name"),
            })

    return {
        "server": client.name,
        "timestamp": datetime.now().isoformat(),
        "services": service_list,
        "summary": {
            "total": total,
            "running": running,
            "stopped": stopped,
            "not_installed": not_installed,
        },
        "alerts": alerts,
    }


def run_services_check(manager: BtClientManager, server: Optional[str] = None,
                       services: Optional[list] = None) -> dict:
    """
    Execute service status check

    Args:
        manager: Client manager
        server: Specify server name
        services: List of services to query

    Returns:
        Check results
    """
    # Single server
    if server:
        client = manager.get_client(server)
        return get_server_services(client, services)

    # All servers
    all_clients = manager.get_all_clients()
    results = {
        "timestamp": datetime.now().isoformat(),
        "servers": [],
        "summary": {
            "total_servers": 0,
            "total_services": 0,
            "total_running": 0,
            "total_stopped": 0,
        },
        "alerts": [],
    }

    for name, client in all_clients.items():
        try:
            service_result = get_server_services(client, services)
            results["servers"].append(service_result)

            # Summary statistics
            summary = service_result.get("summary", {})
            results["summary"]["total_servers"] += 1
            results["summary"]["total_services"] += summary.get("total", 0)
            results["summary"]["total_running"] += summary.get("running", 0)
            results["summary"]["total_stopped"] += summary.get("stopped", 0)

            # Collect alerts
            for alert in service_result.get("alerts", []):
                results["alerts"].append(alert)

        except Exception as e:
            results["servers"].append({
                "server": name,
                "error": str(e),
                "services": [],
                "alerts": [{"level": "critical", "type": "connection", "message": str(e)}],
            })

    return results


def print_services_table(results: dict):
    """Print table-formatted output"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        if "servers" in results and len(results["servers"]) > 1:
            # Multi-server mode - show summary
            for server_data in results["servers"]:
                if "error" in server_data:
                    console.print(f"[red]Server {server_data['server']} connection failed: {server_data['error']}[/red]")
                    continue

                server_name = server_data.get("server", "Unknown")
                summary = server_data.get("summary", {})

                # Server title
                console.print(f"\n[bold cyan]═══ {server_name} ═══[/bold cyan]")

                # Service list table
                services = server_data.get("services", [])
                if services:
                    table = Table(show_header=True, header_style="bold")
                    table.add_column("Service", style="cyan", width=20)
                    table.add_column("Version", width=12)
                    table.add_column("Status", width=10)
                    table.add_column("Installed", width=8)
                    table.add_column("PID", width=8)

                    for svc in services:
                        # Status color
                        if not svc.get("installed", False):
                            status_str = "[dim]Not installed[/dim]"
                        elif svc.get("status"):
                            status_str = "[green]Running[/green]"
                        else:
                            status_str = "[red]Stopped[/red]"

                        # Installation status
                        installed_str = "✓" if svc.get("installed") else "-"

                        # PID
                        pid = svc.get("pid", 0) or 0
                        pid_str = str(pid) if pid > 0 else "-"

                        table.add_row(
                            svc.get("title", svc.get("name", "-"))[:20],
                            svc.get("version", "-")[:12],
                            status_str,
                            installed_str,
                            pid_str,
                        )

                    console.print(table)
                else:
                    console.print("[yellow]No service info[/yellow]")

                # Summary
                console.print(f"\n[dim]Summary: "
                             f"Total {summary.get('total', 0)}, "
                             f"[green]Running {summary.get('running', 0)}[/green], "
                             f"[red]Stopped {summary.get('stopped', 0)}[/red], "
                             f"[dim]Not installed {summary.get('not_installed', 0)}[/dim][/dim]")

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
                         f"Total services: {summary.get('total_services', 0)}, "
                         f"[green]Running: {summary.get('total_running', 0)}[/green], "
                         f"[red]Stopped: {summary.get('total_stopped', 0)}[/red]")

        else:
            # Single server mode
            server_name = results.get("server", "Unknown")

            # Basic info
            console.print(Panel(f"[bold]{server_name}[/bold]", title="Server"))

            services = results.get("services", [])
            if services:
                table = Table(show_header=True, header_style="bold")
                table.add_column("Service", style="cyan")
                table.add_column("Version")
                table.add_column("Status")
                table.add_column("Installed")
                table.add_column("PID")

                for svc in services:
                    # Status color
                    if not svc.get("installed", False):
                        status_str = "[dim]Not installed[/dim]"
                    elif svc.get("status"):
                        status_str = "[green]Running[/green]"
                    else:
                        status_str = "[red]Stopped[/red]"

                    # Installation status
                    installed_str = "✓" if svc.get("installed") else "-"

                    # PID
                    pid = svc.get("pid", 0) or 0
                    pid_str = str(pid) if pid > 0 else "-"

                    table.add_row(
                        svc.get("title", svc.get("name", "-")),
                        svc.get("version", "-"),
                        status_str,
                        installed_str,
                        pid_str,
                    )

                console.print(table)
            else:
                console.print("[yellow]No service info[/yellow]")

            # Summary
            summary = results.get("summary", {})
            console.print(f"\n[bold]Summary:[/bold]")
            console.print(f"  Total: {summary.get('total', 0)}")
            console.print(f"  [green]Running: {summary.get('running', 0)}[/green]")
            console.print(f"  [red]Stopped: {summary.get('stopped', 0)}[/red]")
            console.print(f"  [dim]Not installed: {summary.get('not_installed', 0)}[/dim]")

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
        description="aaPanel Service Status Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check all servers' service status
  %(prog)s

  # Check specific server
  %(prog)s --server prod-01

  # Only check specific services
  %(prog)s --service nginx --service redis

  # JSON format output
  %(prog)s --format json

  # Output to file
  %(prog)s --output services.json

Supported services: nginx, apache, mysql, redis, memcached, pure-ftpd
PHP services: Auto-detect installed PHP versions (php-8.2, php-7.4, etc.)
PostgreSQL: Requires pgsql_manager plugin

Field descriptions:
  installed (setup): Whether service is installed
  status: Whether service is running (only meaningful when installed=true)
  version: Installed version number
  pid: Main process ID (when running)
        """,
    )
    parser.add_argument("--server", "-s", help="Specify server name")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="table", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--service", action="append", dest="services",
                        help="Specify services to check (can be used multiple times)")
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

    # Execute check
    try:
        results = run_services_check(manager, args.server, args.services)
    except KeyError as e:
        print(f"Error: Server not found {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Check failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Output result
    if args.format == "table":
        print_services_table(results)
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
