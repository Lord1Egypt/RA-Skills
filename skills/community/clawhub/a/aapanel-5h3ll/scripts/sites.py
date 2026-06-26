#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "pyyaml>=6.0",
#   "rich>=13.0",
# ]
# ///
"""
Site Status Check Script
Checks running status and SSL certificates of all sites and projects
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
    parse_all_sites,
    load_config,
)


def get_server_sites(client: BtClient) -> dict:
    """
    Get single server's site status

    Args:
        client: aaPanel client

    Returns:
        Site status info
    """
    # Get all sites and projects
    sites_data = client.get_all_sites()

    # Parse data
    return parse_all_sites(sites_data, client.name)


def run_sites_check(manager: BtClientManager, server: Optional[str] = None) -> dict:
    """
    Execute site status check

    Args:
        manager: Client manager
        server: Specify server name

    Returns:
        Check results
    """
    # Single server
    if server:
        client = manager.get_client(server)
        return get_server_sites(client)

    # All servers
    all_clients = manager.get_all_clients()
    results = {
        "timestamp": datetime.now().isoformat(),
        "servers": [],
        "summary": {
            "total": 0,
            "running": 0,
            "stopped": 0,
            "ssl_expired": 0,
            "ssl_expiring": 0,
        },
        "alerts": [],
    }

    for name, client in all_clients.items():
        try:
            site_result = get_server_sites(client)
            results["servers"].append(site_result)

            # Summary statistics
            summary = site_result.get("summary", {})
            results["summary"]["total"] += summary.get("total", 0)
            results["summary"]["running"] += summary.get("by_status", {}).get("running", 0)
            results["summary"]["stopped"] += summary.get("by_status", {}).get("stopped", 0)
            results["summary"]["ssl_expired"] += summary.get("ssl_expired", 0)
            results["summary"]["ssl_expiring"] += summary.get("ssl_expiring", 0)

            # Collect alerts
            for alert in site_result.get("alerts", []):
                results["alerts"].append(alert)

        except Exception as e:
            results["servers"].append({
                "server": name,
                "error": str(e),
                "sites": [],
                "alerts": [{"level": "critical", "type": "connection", "message": str(e)}],
            })

    return results


def print_sites_table(results: dict):
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

                # Site list table
                sites = server_data.get("sites", [])
                if sites:
                    table = Table(show_header=True, header_style="bold")
                    table.add_column("Name", style="cyan", width=25)
                    table.add_column("Type", width=8)
                    table.add_column("Status", width=8)
                    table.add_column("SSL", width=10)
                    table.add_column("PHP/Port", width=10)
                    table.add_column("Note", width=20)

                    for site in sites:
                        # Status color
                        status = site.get("status", "unknown")
                        if status == "running":
                            status_str = "[green]Running[/green]"
                        elif status == "starting":
                            status_str = "[yellow]Starting[/yellow]"
                        else:
                            status_str = "[red]Stopped[/red]"

                        # SSL status
                        ssl = site.get("ssl", {})
                        ssl_status = ssl.get("status", "none")
                        if ssl_status == "valid":
                            ssl_str = f"[green]{ssl.get('days_remaining', 0)}d[/green]"
                        elif ssl_status == "warning":
                            ssl_str = f"[yellow]{ssl.get('days_remaining', 0)}d[/yellow]"
                        elif ssl_status == "critical":
                            ssl_str = f"[red]{ssl.get('days_remaining', 0)}d[/red]"
                        elif ssl_status == "expired":
                            ssl_str = "[red]Expired[/red]"
                        else:
                            ssl_str = "-"

                        # PHP version or port
                        php_or_port = site.get("php_version") or str(site.get("port", "")) or "-"

                        table.add_row(
                            site.get("name", "-")[:25],
                            site.get("type", "-"),
                            status_str,
                            ssl_str,
                            php_or_port[:10],
                            (site.get("ps", "") or "")[:20],
                        )

                    console.print(table)
                else:
                    console.print("[yellow]No sites[/yellow]")

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
                         f"Total sites: {summary.get('total', 0)}, "
                         f"[green]Running: {summary.get('running', 0)}[/green], "
                         f"[red]Stopped: {summary.get('stopped', 0)}[/red], "
                         f"[red]SSL expired: {summary.get('ssl_expired', 0)}[/red], "
                         f"[yellow]SSL expiring: {summary.get('ssl_expiring', 0)}[/yellow]")

        else:
            # Single server mode
            server_name = results.get("server", "Unknown")

            # Basic info
            console.print(Panel(f"[bold]{server_name}[/bold]", title="Server"))

            sites = results.get("sites", [])
            if sites:
                table = Table(show_header=True, header_style="bold")
                table.add_column("Name", style="cyan")
                table.add_column("Type")
                table.add_column("Status")
                table.add_column("SSL")
                table.add_column("Path")
                table.add_column("Note")

                for site in sites:
                    status = site.get("status", "unknown")
                    if status == "running":
                        status_str = "[green]Running[/green]"
                    elif status == "starting":
                        status_str = "[yellow]Starting[/yellow]"
                    else:
                        status_str = "[red]Stopped[/red]"

                    ssl = site.get("ssl", {})
                    ssl_status = ssl.get("status", "none")
                    if ssl_status == "valid":
                        ssl_str = f"[green]Valid ({ssl.get('days_remaining', 0)}d)[/green]"
                    elif ssl_status == "expired":
                        ssl_str = "[red]Expired[/red]"
                    elif ssl_status in ["warning", "critical"]:
                        ssl_str = f"[yellow]Expires in {ssl.get('days_remaining', 0)}d[/yellow]"
                    else:
                        ssl_str = "-"

                    table.add_row(
                        site.get("name", "-"),
                        site.get("type", "-"),
                        status_str,
                        ssl_str,
                        site.get("path", "-")[:40],
                        site.get("ps", "")[:20],
                    )

                console.print(table)
            else:
                console.print("[yellow]No sites[/yellow]")

            # Summary
            summary = results.get("summary", {})
            console.print(f"\n[bold]Summary:[/bold]")
            console.print(f"  Total: {summary.get('total', 0)}")
            console.print(f"  By type: {summary.get('by_type', {})}")
            console.print(f"  By status: {summary.get('by_status', {})}")

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
        description="aaPanel Site Status Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check all servers' site status
  %(prog)s

  # Check specific server
  %(prog)s --server prod-01

  # Only show stopped sites
  %(prog)s --filter stopped

  # Only show SSL expiring sites
  %(prog)s --filter ssl-warning

  # Output to file
  %(prog)s --output sites.json
        """,
    )
    parser.add_argument("--server", "-s", help="Specify server name")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="table", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--filter", choices=["stopped", "ssl-warning", "ssl-expired"],
                        help="Filter: stopped (stopped sites), ssl-warning (SSL expiring), ssl-expired (SSL expired)")
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
        results = run_sites_check(manager, args.server)
    except KeyError as e:
        print(f"Error: Server not found {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Check failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Apply filter
    if args.filter:
        results = apply_filter(results, args.filter)

    # Output result
    if args.format == "table":
        print_sites_table(results)
    else:
        output = json.dumps(results, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Result saved to: {args.output}")
        else:
            print(output)


def apply_filter(results: dict, filter_type: str) -> dict:
    """Apply filter"""
    if "servers" in results:
        # Multi-server mode
        for server_data in results.get("servers", []):
            if "sites" in server_data:
                server_data["sites"] = filter_sites(server_data["sites"], filter_type)
    elif "sites" in results:
        # Single server mode
        results["sites"] = filter_sites(results["sites"], filter_type)

    return results


def filter_sites(sites: list, filter_type: str) -> list:
    """Filter site list"""
    filtered = []
    for site in sites:
        if filter_type == "stopped":
            if site.get("status") == "stopped":
                filtered.append(site)
        elif filter_type == "ssl-warning":
            ssl = site.get("ssl", {})
            if ssl.get("status") == "warning":
                filtered.append(site)
        elif filter_type == "ssl-expired":
            ssl = site.get("ssl", {})
            if ssl.get("status") == "expired":
                filtered.append(site)
    return filtered


if __name__ == "__main__":
    main()
