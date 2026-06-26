"""CLI commands for ClawShorts multi-device management."""
from __future__ import annotations

__all__ = ["main", "create_parser"]

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Any

from clawshorts import config
from clawshorts.device import Device
from clawshorts.device_monitor import check_daemon, poll_screen

# Import the shared DB module (lives under scripts/)
_scripts_dir = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(_scripts_dir))
try:
    import clawshorts_db as db  # noqa: E402
    _HAS_DB = True
except ImportError:
    _HAS_DB = False

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_setup(args: argparse.Namespace) -> int:
    """First-time setup - add first device and initialize config."""
    print("=" * 40)
    print("  ⚡ ClawShorts Setup")
    print("=" * 40)
    print()

    valid, error = config.validate_device_input(args.ip, args.name)
    if not valid:
        print(f"  ❌ {error}")
        return 1

    try:
        device = config.add_device(args.ip, args.name, args.limit)
        print(f"  ✅ Device added: {device.name} ({device.ip})")
        print(f"  📊 Daily limit: {device.limit} shorts")
        print()
        print("  Next steps:")
        print("    1. Enable ADB on Fire TV: Settings → My Fire TV → Developer Options → ADB Debugging")
        print("    2. Run: clawshorts connect")
        print("    3. Run: clawshorts start")
        return 0
    except config.ConfigError as e:
        print(f"  ❌ {e}")
        return 1


def cmd_add(args: argparse.Namespace) -> int:
    """Add a new device."""
    valid, error = config.validate_device_input(args.ip, args.name)
    if not valid:
        print(f"Error: {error}")
        return 1

    try:
        device = config.add_device(args.ip, args.name, args.limit)
        print(f"✅ Added: {device.name} ({device.ip})")
        return 0
    except config.ConfigError as e:
        print(f"Error: {e}")
        return 1


def cmd_remove(args: argparse.Namespace) -> int:
    """Remove a device by IP."""
    removed = config.remove_device(args.ip)
    if removed:
        print(f"✅ Removed device: {args.ip}")
        return 0
    print(f"Device not found: {args.ip}")
    return 1


def cmd_list(args: argparse.Namespace) -> int:
    """List all configured devices."""
    devices = config.load_devices()

    print("=" * 40)
    print("  📺 ClawShorts Devices")
    print("=" * 40)

    if not devices:
        print("  No devices configured.")
        print()
        print("  Quick start:")
        print("    clawshorts setup 192.168.1.100 living-room")
        print("=" * 40)
        return 0

    for device in devices:
        status_icon = "🟢" if device.enabled else "🔴"
        print(f"  {status_icon} {device.name}")
        print(f"     IP: {device.ip} | Limit: {device.limit}/day")
        print()

    print("=" * 40)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Show quota status for device(s) with live verification."""
    devices = config.load_devices()
    if not devices:
        print("No devices configured. Run: clawshorts setup <IP>")
        return 1

    if args.ip:
        device = config.get_device(args.ip)
        if not device:
            print(f"Device not found: {args.ip}")
            return 1
        devices = [device]

    print("=" * 50)
    print("  📊 ClawShorts Status")
    print("=" * 50)

    for device in devices:
        daemon_health = check_daemon(device.ip)
        screen = poll_screen(device.ip)

        print(f"\n  📺 {device.name} ({device.ip})")
        print(f"  ────────────────────────────")
        print(f"  Daemon:  {daemon_health.status}")
        print(f"  Detail:  {daemon_health.detail}")
        print(f"  App:     {screen.app}")
        print(f"  Screen:  {screen.detail}")

        if _HAS_DB:
            usage = db.get_seconds(device.ip, time.strftime("%Y-%m-%d"))
            remaining = max(0.0, device.limit - usage)
            print(f"  Usage:   {usage:.0f}s / {device.limit}s ({remaining:.0f}s remaining)")

        print(f"  Status:  {'Enabled' if device.enabled else 'Disabled'}")

    print("\n" + "=" * 50)
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    """Reset quota for device(s) via SQLite only."""
    if args.ip:
        ips = [args.ip]
    else:
        devices = config.load_devices()
        if not devices:
            print("No devices found to reset.")
            return 1
        ips = [d.ip for d in devices]

    if not ips:
        print("No devices found to reset.")
        return 1

    if _HAS_DB:
        try:
            db.init_db()
            if args.ip:
                db.reset_device(args.ip)
            else:
                db.reset_all()
        except OSError as e:
            logger.warning("DB reset failed: %s", e)

    for ip in ips:
        print(f"  ✅ Reset quota for {ip}")

    print(f"\n  {len(ips)} device(s) reset. Counts will restart from 0.")
    return 0


def cmd_enable(args: argparse.Namespace) -> int:
    """Enable a device."""
    device = config.update_device(args.ip, enabled=True)
    if device:
        print(f"✅ Enabled: {device.name}")
        return 0
    print(f"Device not found: {args.ip}")
    return 1


def cmd_disable(args: argparse.Namespace) -> int:
    """Disable a device."""
    device = config.update_device(args.ip, enabled=False)
    if device:
        print(f"✅ Disabled: {device.name}")
        return 0
    print(f"Device not found: {args.ip}")
    return 1


def cmd_connect(args: argparse.Namespace) -> int:
    """Guide user through ADB connection steps."""
    print("📱 ADB Connection Steps:")
    print("")
    print("1. Enable ADB Debugging on your Fire TV:")
    print("   Settings → My Fire TV → Developer Options → ADB Debugging = ON")
    print("")
    print("2. Make sure your Fire TV and Mac are on the same WiFi network.")
    print("")
    print("3. Test the connection:")
    print(f"   adb connect {args.ip}")
    print("")
    print("   If successful, you should see: 'connected to {args.ip}:5555'")
    print("")
    print("4. Verify YouTube can be accessed:")
    print("   adb -s {args.ip}:5555 shell am start -n com.amazon.firetv.youtube/.MainActivity")
    print("")
    print("Once connected, ClawShorts will automatically detect Shorts viewing.")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    """Show watch history from the DB."""
    if not _HAS_DB:
        print("❌ Database not available")
        return 1

    try:
        import datetime
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=args.days)

        rows = db.get_history(args.ip, start_date.isoformat(), today.isoformat())

        if not rows:
            print(f"No watch history in the last {args.days} days.")
            return 0

        print(f"{'📅 Date':<14} {'Device':<20} {'Seconds':>10} {'Limit':>8} {'Status'}")
        print("─" * 70)

        for row in rows:
            date, ip, seconds, limit_val = row
            remaining = max(0.0, limit_val - seconds)
            if seconds >= limit_val:
                status = "🚫 Limit reached"
            elif remaining < limit_val * 0.2:
                status = "⚠️  Almost out"
            else:
                status = "✅ Under limit"
            print(f"{date:<14} {ip:<20} {seconds:>10.0f} {limit_val:>8} {status}")

        print(f"\n📊 Showing last {args.days} days")
        return 0
    except Exception as e:
        print(f"❌ Error fetching history: {e}")
        return 1


def cmd_logs(args: argparse.Namespace) -> int:
    """Show debug logs."""
    log_path = Path.home() / ".clawshorts" / "daemon.log"
    if not log_path.exists():
        print("No daemon.log found.")
        return 1

    lines = log_path.read_text(errors="replace").splitlines()
    tail = lines[-args.lines:] if len(lines) > args.lines else lines

    for line in tail:
        print(line)
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="clawshorts",
        description="⚡ ClawShorts - YouTube Shorts Blocker for Fire TV",
    )
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging")
    parser.add_argument("--config", "-c", type=Path, help="Path to config file")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # setup
    p = subparsers.add_parser("setup", help="First-time setup")
    p.add_argument("ip", help="Fire TV IP address")
    p.add_argument("name", nargs="?", help="Device name (optional)")
    p.add_argument("--limit", "-l", type=int, default=300, help="Daily shorts limit (default: 300s)")
    p.set_defaults(func=cmd_setup)

    # add
    p = subparsers.add_parser("add", help="Add a new device")
    p.add_argument("ip", help="Fire TV IP address")
    p.add_argument("name", nargs="?", help="Device name (optional)")
    p.add_argument("--limit", "-l", type=int, default=300, help="Daily shorts limit (default: 300s)")
    p.set_defaults(func=cmd_add)

    # remove
    p = subparsers.add_parser("remove", help="Remove a device")
    p.add_argument("ip", help="Fire TV IP address")
    p.set_defaults(func=cmd_remove)

    # list
    subparsers.add_parser("list", help="List all devices").set_defaults(func=cmd_list)

    # status
    p = subparsers.add_parser("status", help="Show quota status")
    p.add_argument("ip", nargs="?", help="Device IP (optional, shows all if omitted)")
    p.set_defaults(func=cmd_status)

    # reset
    p = subparsers.add_parser("reset", help="Reset quota")
    p.add_argument("ip", nargs="?", help="Device IP (optional, resets all if omitted)")
    p.set_defaults(func=cmd_reset)

    # enable
    p = subparsers.add_parser("enable", help="Enable a device")
    p.add_argument("ip", help="Fire TV IP address")
    p.set_defaults(func=cmd_enable)

    # disable
    p = subparsers.add_parser("disable", help="Disable a device")
    p.add_argument("ip", help="Fire TV IP address")
    p.set_defaults(func=cmd_disable)

    # connect
    p = subparsers.add_parser("connect", help="Guide for ADB connection")
    p.add_argument("ip", nargs="?", help="Fire TV IP address (optional)")
    p.set_defaults(func=cmd_connect)

    # history
    p = subparsers.add_parser("history", help="Show watch history")
    p.add_argument("--days", "-d", type=int, default=30, help="Number of days to show (default: 30)")
    p.add_argument("ip", nargs="?", help="Device IP (optional)")
    p.set_defaults(func=cmd_history)

    # logs
    p = subparsers.add_parser("logs", help="Show debug logs")
    p.add_argument("--lines", "-n", type=int, default=50, help="Number of lines to show (default: 50)")
    p.set_defaults(func=cmd_logs)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    log_level = "DEBUG" if args.debug else "INFO"
    config.configure_logging(log_level)

    if not args.command:
        parser.print_help()
        print()
        print("Quick Start:")
        print("  clawshorts setup 192.168.1.100 living-room")
        print("  clawshorts list")
        print("  clawshorts status")
        return 0

    try:
        return args.func(args) or 0
    except config.ConfigError as e:
        logger.error("Config error: %s", e)
        print(f"Error: {e}")
        return 1
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
