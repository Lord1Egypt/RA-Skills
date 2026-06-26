#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "pyyaml>=6.0",
#   "rich>=13.0",
# ]
# ///
"""
SSH Status Check Script
Checks SSH service status and login logs
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
    load_config,
)


def get_ssh_status(client: BtClient) -> dict:
    """
    Get SSH service status

    Args:
        client: aaPanel client

    Returns:
        SSH status info
    """
    result = {
        "server": client.name,
        "timestamp": datetime.now().isoformat(),
        "ssh": {},
        "alerts": [],
    }

    try:
        info = client.get_ssh_info()

        ssh_info = {
            "port": info.get("port", 22),
            "status": info.get("status", False),
            "status_text": info.get("status_text", "Unknown"),
            "ping_enabled": info.get("ping", False),
            "firewall_status": info.get("firewall_status", False),
            "fail2ban": {
                "status": info.get("fail2ban", {}).get("status", 0) == 1,
                "installed": info.get("fail2ban", {}).get("installed", 0) == 1,
            },
            "ban_cron_job": info.get("ban_cron_job", False),
        }

        result["ssh"] = ssh_info

        # Generate alerts
        if not ssh_info["status"]:
            result["alerts"].append({
                "level": "critical",
                "type": "ssh",
                "message": "SSH service has stopped",
            })

        # Check non-standard port
        if ssh_info["port"] != 22:
            result["alerts"].append({
                "level": "info",
                "type": "ssh",
                "message": f"SSH using non-standard port: {ssh_info['port']}",
            })

    except Exception as e:
        result["error"] = str(e)
        result["alerts"].append({
            "level": "critical",
            "type": "connection",
            "message": f"Failed to get SSH status: {e}",
        })

    return result


def get_ssh_logs(client: BtClient, page: int = 1, limit: int = 50,
                 login_filter: str = "ALL", search: str = "") -> dict:
    """
    Get SSH login logs

    Args:
        client: aaPanel client
        page: Page number
        limit: Items per page
        login_filter: Filter type (ALL/success/failed)
        search: Search keyword

    Returns:
        SSH login logs
    """
    result = {
        "server": client.name,
        "timestamp": datetime.now().isoformat(),
        "logs": [],
        "summary": {
            "total": 0,
            "success": 0,
            "failed": 0,
            "unique_ips": set(),
        },
        "alerts": [],
    }

    try:
        response = client.get_ssh_logs(page=page, limit=limit, search=search)
        logs = response.get("data", [])

        # Parse logs
        parsed_logs = []
        for log in logs:
            parsed_log = {
                "time": log.get("time", ""),
                "timestamp": log.get("timestamp", 0),
                "type": log.get("type", "unknown"),  # success/failed
                "status": log.get("status", 0),
                "user": log.get("user", ""),
                "address": log.get("address", ""),
                "port": log.get("port", ""),
                "login_type": log.get("login_type", "password"),
                "area": log.get("area", {}).get("info", "Unknown"),
                "deny_status": log.get("deny_status", 0),
            }

            # Apply filter
            if login_filter != "ALL":
                if login_filter == "success" and parsed_log["type"] != "success":
                    continue
                elif login_filter == "failed" and parsed_log["type"] != "failed":
                    continue

            parsed_logs.append(parsed_log)

            # Statistics
            result["summary"]["total"] += 1
            if parsed_log["type"] == "success":
                result["summary"]["success"] += 1
            else:
                result["summary"]["failed"] += 1
            result["summary"]["unique_ips"].add(parsed_log["address"])

        result["logs"] = parsed_logs
        result["summary"]["unique_ips"] = len(result["summary"]["unique_ips"])

        # Generate alerts - detect abnormal logins
        recent_failed = sum(1 for log in parsed_logs[:10] if log["type"] == "failed")
        if recent_failed >= 5:
            result["alerts"].append({
                "level": "warning",
                "type": "ssh",
                "message": f"{recent_failed} failed login attempts in last 10 logs",
            })

    except Exception as e:
        result["error"] = str(e)
        result["alerts"].append({
            "level": "critical",
            "type": "connection",
            "message": f"Failed to get SSH logs: {e}",
        })

    return result


def run_ssh_check(manager: BtClientManager, server: Optional[str] = None,
                  check_type: str = "status") -> dict:
    """
    Execute SSH check

    Args:
        manager: Client manager
        server: Specify server name
        check_type: Check type (status/logs)

    Returns:
        Check results
    """
    # Single server
    if server:
        client = manager.get_client(server)
        if check_type == "status":
            return get_ssh_status(client)
        else:
            return get_ssh_logs(client)

    # All servers
    all_clients = manager.get_all_clients()
    results = {
        "timestamp": datetime.now().isoformat(),
        "servers": [],
    }

    for name, client in all_clients.items():
        try:
            if check_type == "status":
                result = get_ssh_status(client)
            else:
                result = get_ssh_logs(client)
            results["servers"].append(result)
        except Exception as e:
            results["servers"].append({
                "server": name,
                "error": str(e),
                "alerts": [{"level": "critical", "type": "connection", "message": str(e)}],
            })

    return results


def print_ssh_status(results: dict):
    """Print SSH status output"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        if "servers" in results:
            # Multi-server mode
            for server_data in results["servers"]:
                if "error" in server_data:
                    console.print(f"[red]Server {server_data.get('server', 'Unknown')} error: {server_data['error']}[/red]")
                    continue

                server_name = server_data.get("server", "Unknown")
                ssh_info = server_data.get("ssh", {})

                console.print(f"\n[bold cyan]═══ {server_name} ═══[/bold cyan]")

                # SSH status table
                table = Table(show_header=True, header_style="bold")
                table.add_column("Item", style="cyan", width=20)
                table.add_column("Value", width=30)

                status_str = "[green]Running[/green]" if ssh_info.get("status") else "[red]Stopped[/red]"
                table.add_row("SSH Service", status_str)
                table.add_row("Port", str(ssh_info.get("port", 22)))
                table.add_row("Ping", "Allowed" if ssh_info.get("ping_enabled") else "Denied")
                table.add_row("Firewall", "On" if ssh_info.get("firewall_status") else "Off")

                fail2ban = ssh_info.get("fail2ban", {})
                fb_status = "Installed" if fail2ban.get("installed") else "Not installed"
                if fail2ban.get("status"):
                    fb_status += " [green](Running)[/green]"
                table.add_row("Fail2ban", fb_status)

                console.print(table)

                # Alerts
                alerts = server_data.get("alerts", [])
                if alerts:
                    console.print("\n[yellow]Hints:[/yellow]")
                    for alert in alerts:
                        level = alert.get("level", "info")
                        if level == "critical":
                            color = "red"
                        elif level == "warning":
                            color = "yellow"
                        else:
                            color = "blue"
                        console.print(f"  [{color}]• {alert.get('message', '')}[/{color}]")

        else:
            # Single server mode
            server_name = results.get("server", "Unknown")
            ssh_info = results.get("ssh", {})

            console.print(Panel(f"[bold]{server_name} - SSH Status[/bold]", title="Server"))

            table = Table(show_header=True, header_style="bold")
            table.add_column("Item", style="cyan")
            table.add_column("Value")

            status_str = "[green]Running[/green]" if ssh_info.get("status") else "[red]Stopped[/red]"
            table.add_row("SSH Service", status_str)
            table.add_row("Port", str(ssh_info.get("port", 22)))
            table.add_row("Status Description", ssh_info.get("status_text", "Unknown"))
            table.add_row("Ping", "Allowed" if ssh_info.get("ping_enabled") else "Denied")
            table.add_row("Firewall", "On" if ssh_info.get("firewall_status") else "Off")

            fail2ban = ssh_info.get("fail2ban", {})
            fb_status = "Installed" if fail2ban.get("installed") else "Not installed"
            if fail2ban.get("status"):
                fb_status += " (Running)"
            table.add_row("Fail2ban", fb_status)

            console.print(table)

            # Alerts
            alerts = results.get("alerts", [])
            if alerts:
                console.print(f"\n[bold yellow]Alerts ({len(alerts)}):[/bold yellow]")
                for alert in alerts:
                    level = alert.get("level", "info")
                    if level == "critical":
                        color = "red"
                    elif level == "warning":
                        color = "yellow"
                    else:
                        color = "blue"
                    console.print(f"  [{color}]• {alert.get('message', '')}[/{color}]")

    except ImportError:
        print("Please install rich library for table output: pip install rich")
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


def print_ssh_logs(results: dict):
    """Print SSH logs output"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        if "servers" in results:
            # Multi-server mode
            for server_data in results["servers"]:
                if "error" in server_data:
                    console.print(f"[red]Server {server_data.get('server', 'Unknown')} error: {server_data['error']}[/red]")
                    continue

                server_name = server_data.get("server", "Unknown")
                logs = server_data.get("logs", [])
                summary = server_data.get("summary", {})

                console.print(f"\n[bold cyan]═══ {server_name} ═══[/bold cyan]")

                # Summary
                console.print(f"[dim]Total: {summary.get('total', 0)}, "
                             f"[green]Success: {summary.get('success', 0)}[/green], "
                             f"[red]Failed: {summary.get('failed', 0)}[/red], "
                             f"Unique IPs: {summary.get('unique_ips', 0)}[/dim]")

                if logs:
                    table = Table(show_header=True, header_style="bold")
                    table.add_column("Time", width=20)
                    table.add_column("Type", width=8)
                    table.add_column("User", width=10)
                    table.add_column("IP Address", width=18)
                    table.add_column("Region", width=15)

                    for log in logs[:30]:
                        type_str = "[green]Success[/green]" if log["type"] == "success" else "[red]Failed[/red]"
                        table.add_row(
                            log.get("time", "")[:19],
                            type_str,
                            log.get("user", "-"),
                            log.get("address", "-"),
                            log.get("area", "Unknown")[:15],
                        )

                    console.print(table)
                else:
                    console.print("[yellow]No login logs[/yellow]")

                # Alerts
                alerts = server_data.get("alerts", [])
                if alerts:
                    console.print("\n[yellow]Alerts:[/yellow]")
                    for alert in alerts:
                        level = alert.get("level", "warning")
                        color = "red" if level == "critical" else "yellow"
                        console.print(f"  [{color}]• {alert.get('message', '')}[/{color}]")

        else:
            # Single server mode
            server_name = results.get("server", "Unknown")
            logs = results.get("logs", [])
            summary = results.get("summary", {})

            console.print(Panel(f"[bold]{server_name} - SSH Login Logs[/bold]", title="Server"))

            # Summary
            console.print(f"[dim]Total: {summary.get('total', 0)}, "
                         f"[green]Success: {summary.get('success', 0)}[/green], "
                         f"[red]Failed: {summary.get('failed', 0)}[/red], "
                         f"Unique IPs: {summary.get('unique_ips', 0)}[/dim]")

            if logs:
                table = Table(show_header=True, header_style="bold")
                table.add_column("Time")
                table.add_column("Type")
                table.add_column("User")
                table.add_column("IP Address")
                table.add_column("Port")
                table.add_column("Region")

                for log in logs[:50]:
                    type_str = "[green]Success[/green]" if log["type"] == "success" else "[red]Failed[/red]"
                    table.add_row(
                        log.get("time", "")[:19],
                        type_str,
                        log.get("user", "-"),
                        log.get("address", "-"),
                        log.get("port", "-"),
                        log.get("area", "Unknown"),
                    )

                console.print(table)
            else:
                console.print("[yellow]No login logs[/yellow]")

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
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="aaPanel SSH Status and Log Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View SSH service status
  %(prog)s --status

  # View SSH login logs
  %(prog)s --logs

  # Only view failed login logs
  %(prog)s --logs --filter failed

  # Only view successful login logs
  %(prog)s --logs --filter success

  # Search for specific IP login records
  %(prog)s --logs --search 192.168.1.1

  # Specify server
  %(prog)s --status --server prod-01

  # JSON format output
  %(prog)s --logs --format json
        """,
    )
    parser.add_argument("--server", "-s", help="Specify server name")
    parser.add_argument("--status", action="store_true", help="View SSH service status")
    parser.add_argument("--logs", action="store_true", help="View SSH login logs")
    parser.add_argument("--filter", choices=["ALL", "success", "failed"], default="ALL",
                        help="Log filter: ALL (all), success (success), failed (failed)")
    parser.add_argument("--search", help="Search keyword (IP address or username)")
    parser.add_argument("--limit", "-n", type=int, default=50,
                        help="Number of logs to return (default: 50)")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="table",
                        help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--config", "-c", help="Config file path")

    args = parser.parse_args()

    # Default to show status
    if not args.status and not args.logs:
        args.status = True

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
        if args.status:
            results = run_ssh_check(manager, args.server, "status")
            if args.format == "json":
                output = json.dumps(results, ensure_ascii=False, indent=2, default=str)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(output)
                    print(f"Result saved to: {args.output}")
                else:
                    print(output)
            else:
                print_ssh_status(results)

        if args.logs:
            results = run_ssh_check(manager, args.server, "logs")
            # Apply filter
            if args.filter != "ALL" or args.search:
                if "servers" in results:
                    for server_data in results["servers"]:
                        if "logs" in server_data:
                            filtered_logs = []
                            for log in server_data["logs"]:
                                if args.filter != "ALL":
                                    if args.filter == "success" and log["type"] != "success":
                                        continue
                                    elif args.filter == "failed" and log["type"] != "failed":
                                        continue
                                if args.search:
                                    if args.search not in log.get("address", "") and args.search not in log.get("user", ""):
                                        continue
                                filtered_logs.append(log)
                            server_data["logs"] = filtered_logs
                            # Update statistics
                            server_data["summary"]["total"] = len(filtered_logs)
                            server_data["summary"]["success"] = sum(1 for l in filtered_logs if l["type"] == "success")
                            server_data["summary"]["failed"] = sum(1 for l in filtered_logs if l["type"] == "failed")
                            server_data["summary"]["unique_ips"] = len(set(l["address"] for l in filtered_logs))
                elif "logs" in results:
                    filtered_logs = []
                    for log in results["logs"]:
                        if args.filter != "ALL":
                            if args.filter == "success" and log["type"] != "success":
                                continue
                            elif args.filter == "failed" and log["type"] != "failed":
                                continue
                        if args.search:
                            if args.search not in log.get("address", "") and args.search not in log.get("user", ""):
                                continue
                        filtered_logs.append(log)
                    results["logs"] = filtered_logs
                    results["summary"]["total"] = len(filtered_logs)
                    results["summary"]["success"] = sum(1 for l in filtered_logs if l["type"] == "success")
                    results["summary"]["failed"] = sum(1 for l in filtered_logs if l["type"] == "failed")
                    results["summary"]["unique_ips"] = len(set(l["address"] for l in filtered_logs))

            if args.format == "json":
                output = json.dumps(results, ensure_ascii=False, indent=2, default=str)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(output)
                    print(f"Result saved to: {args.output}")
                else:
                    print(output)
            else:
                print_ssh_logs(results)

    except KeyError as e:
        print(f"Error: Server not found {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Check failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
