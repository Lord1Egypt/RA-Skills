"""CLI commands for ClawShorts multi-device management."""
from __future__ import annotations

__all__ = ["main", "create_parser"]

import argparse
import logging
import re
import subprocess
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

# Config key → display name mapping
_CONFIG_KEY_LABELS = {
    "shorts_width_threshold": "width_threshold",
    "shorts_max_aspect_ratio": "max_aspect_ratio",
    "shorts_fallback_height_ratio": "fallback_height_ratio",
    "shorts_delta_cap": "delta_cap",
    "default_screen_width": "screen_width",
    "default_screen_height": "screen_height",
}

ADB_PORT = 5555
ADB_TIMEOUT = 8

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

        # Auto-detect screen resolution
        if _HAS_DB:
            res = detect_screen_resolution(args.ip)
            if res:
                width, height = res
                print(f"  🖥️  Screen auto-detected: {width}x{height}")
                db.update_device_screen(args.ip, width, height)
            else:
                gbl_w = db.get_config(db.KEY_DEFAULT_SCREEN_WIDTH) or 1920
                gbl_h = db.get_config(db.KEY_DEFAULT_SCREEN_HEIGHT) or 1080
                print(f"  ⚠️  Screen not detected (ADB unavailable). Using global default: {int(gbl_w)}x{int(gbl_h)}")

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

        # Auto-detect screen resolution
        if _HAS_DB:
            res = detect_screen_resolution(args.ip)
            if res:
                width, height = res
                print(f"🖥️  Screen auto-detected: {width}x{height}")
                db.update_device_screen(args.ip, width, height)
            else:
                gbl_w = db.get_config(db.KEY_DEFAULT_SCREEN_WIDTH) or 1920
                gbl_h = db.get_config(db.KEY_DEFAULT_SCREEN_HEIGHT) or 1080
                print(f"⚠️  Screen not detected (ADB unavailable). Using global default: {int(gbl_w)}x{int(gbl_h)}")

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
    """List all configured devices with effective config."""
    devices = config.load_devices()

    print("=" * 50)
    print("  📺 ClawShorts Devices")
    print("=" * 50)

    if not devices:
        print("  No devices configured.")
        print()
        print("  Quick start:")
        print("    clawshorts setup 192.168.1.100 living-room")
        print("=" * 50)
        return 0

    # Load DB config for effective values
    global_cfg = {}
    if _HAS_DB:
        try:
            db.init_db()
            global_cfg = {k: db.get_config(k) for k in db.CONFIG_KEYS}
        except Exception:
            pass

    for device in devices:
        status_icon = "🟢" if device.enabled else "🔴"
        print(f"  {status_icon} {device.name}")
        print(f"     IP: {device.ip} | Limit: {device.limit}/day")

        # Per-device effective config
        dev_full = None
        if _HAS_DB:
            try:
                dev_full = db.get_device(device.ip)
            except Exception:
                pass

        if dev_full and global_cfg:
            sw = dev_full.get("screen_width")
            sh = dev_full.get("screen_height")
            if sw and sh:
                print(f"     Screen: {sw}x{sh}", end="")
            else:
                print(f"     Screen: ?", end="")
        else:
            print(f"     Screen: ?", end="")

        # Show detection thresholds with source
        threshold_keys = [
            ("width_threshold", "shorts_width_threshold", "w"),
            ("max_aspect_ratio", "shorts_max_aspect_ratio", "ar"),
            ("fallback_height_ratio", "shorts_fallback_height_ratio", "h"),
            ("delta_cap", "shorts_delta_cap", "cap"),
        ]
        parts = []
        for col, cfg_key, abbrev in threshold_keys:
            dev_val = (dev_full or {}).get(col)
            gbl_val = global_cfg.get(cfg_key)
            default = db.DEFAULTS.get(cfg_key, 0) if _HAS_DB else 0
            eff_val, source = _effective_value(dev_val, gbl_val, default)
            mark = "*" if source == "per-device" else ""
            parts.append(f"{abbrev}={eff_val:.2f}{mark}")

        if parts:
            print(f" | {' | '.join(parts)}")

        print()

    print("=" * 50)
    print("  (* = per-device override, no mark = global default)")
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
    """Guide user through ADB connection steps and re-detect screen."""
    if not args.ip:
        print("Usage: shorts connect <IP>")
        return 1

    print("📱 ADB Connection Steps:")
    print("")
    print(f"1. Connect to {args.ip}:")
    print(f"   adb connect {args.ip}")
    print("")
    print("   If successful, you should see: 'connected to {args.ip}:5555'")
    print("")
    print("2. Enable ADB Debugging on your Fire TV:")
    print("   Settings → My Fire TV → Developer Options → ADB Debugging = ON")
    print("")
    print("3. Make sure your Fire TV and Mac are on the same WiFi network.")
    print("")

    # Re-detect screen resolution after connecting
    if _HAS_DB:
        print("🔍 Detecting screen resolution...")
        res = detect_screen_resolution(args.ip)
        if res:
            width, height = res
            print(f"   ✅ Detected: {width}x{height}")
            db.update_device_screen(args.ip, width, height)
        else:
            print(f"   ⚠️  Could not detect screen. ADB may not be connected.")
            print(f"      Run 'adb connect {args.ip}' first, then try again.")

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
# Screen detection
# ---------------------------------------------------------------------------

def detect_screen_resolution(ip: str) -> tuple[int, int] | None:
    """Query screen size via ADB. Returns (width, height) or None on failure."""
    dev = f"{ip}:{ADB_PORT}"
    try:
        result = subprocess.run(
            ["adb", "-s", dev, "shell", "dumpsys", "display"],
            capture_output=True, text=True, timeout=ADB_TIMEOUT,
        )
        out = result.stdout
        # Parse mDisplayWidth / mDisplayHeight
        w_m = re.search(r"mDisplayWidth=(\d+)", out)
        h_m = re.search(r"mDisplayHeight=(\d+)", out)
        if w_m and h_m:
            return int(w_m.group(1)), int(h_m.group(1))
        # Fallback: wm size
        result2 = subprocess.run(
            ["adb", "-s", dev, "shell", "wm", "size"],
            capture_output=True, text=True, timeout=ADB_TIMEOUT,
        )
        m = re.search(r"(\d+)x(\d+)", result2.stdout)
        if m:
            return int(m.group(1)), int(m.group(2))
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def cmd_detect(args: argparse.Namespace) -> int:
    """Re-detect screen resolution via ADB and update DB."""
    print(f"🔍 Detecting screen resolution for {args.ip}...")
    result = detect_screen_resolution(args.ip)
    if result is None:
        print(f"❌ Could not detect screen for {args.ip}. Is ADB connected?")
        # Fall back to global defaults
        if _HAS_DB:
            w = db.get_config(db.KEY_DEFAULT_SCREEN_WIDTH) or 1920
            h = db.get_config(db.KEY_DEFAULT_SCREEN_HEIGHT) or 1080
            print(f"   Using global defaults: {int(w)}x{int(h)}")
        return 1

    width, height = result
    print(f"✅ Detected: {width}x{height}")
    if _HAS_DB:
        db.update_device_screen(args.ip, width, height)
        print(f"   Updated DB for {args.ip}")
    return 0


# ---------------------------------------------------------------------------
# Config commands
# ---------------------------------------------------------------------------

def _effective_value(device_val, global_val, default):
    """Return human-readable (value, source) for a config value."""
    if device_val is not None:
        return float(device_val), "per-device"
    if global_val is not None:
        return float(global_val), "global"
    return default, "hardcoded"


def cmd_config(args: argparse.Namespace) -> int:
    """Show / get / set global or per-device config values."""
    if not _HAS_DB:
        print("❌ Database not available")
        return 1

    try:
        db.init_db()
    except Exception as e:
        print(f"❌ DB error: {e}")
        return 1

    sub = args.config_sub

    # Bare `shorts config` → show global defaults
    if sub is None:
        sub = "show"

    if sub == "show":
        # `shorts config show [IP]` — show all keys with effective values
        ip = getattr(args, "ip", None)
        global_cfg = {k: db.get_config(k) for k in db.CONFIG_KEYS}
        global_cfg = {k: v for k, v in global_cfg.items() if v is not None}

        print("=" * 50)
        print("  ⚙️  ClawShorts Config")
        print("=" * 50)
        print("\n  Global defaults:")
        for key in db.CONFIG_KEYS:
            label = _CONFIG_KEY_LABELS.get(key, key)
            val = global_cfg.get(key)
            default = db.DEFAULTS.get(key)
            display_val = f"{val:.4f}" if val is not None else f"{default:.4f} (hardcoded)"
            print(f"    {label:<28} {display_val}")

        if ip:
            dev = db.get_device(ip)
            if dev:
                print(f"\n  Device: {ip} ({dev.get('name', 'unknown')})")
                for key in db.CONFIG_KEYS:
                    label = _CONFIG_KEY_LABELS.get(key, key)
                    col = db.KEY_TO_DEVICE_COLUMN.get(key)
                    dev_val = dev.get(col) if col else None
                    gbl_val = global_cfg.get(key)
                    default = db.DEFAULTS.get(key, 0)
                    eff_val, source = _effective_value(dev_val, gbl_val, default)
                    override_mark = " *" if source == "per-device" else ""
                    print(f"    {label:<28} {eff_val:.4f}{override_mark}  ({source})")
            else:
                print(f"\n  Device {ip} not found.")
        print()
        print("  (* = per-device override)")
        return 0

    if sub == "get":
        # `shorts config get <key>`
        key = getattr(args, "key", None)
        if not key:
            print("Usage: shorts config get <key>")
            return 1
        # Normalize key
        norm_key = _normalize_key(key)
        if norm_key is None:
            print(f"Unknown config key: {key}")
            print(f"Available: {', '.join(_CONFIG_KEY_LABELS.values())}")
            return 1
        val = db.get_config(norm_key)
        if val is None:
            val = db.DEFAULTS.get(norm_key, 0)
            print(f"{_CONFIG_KEY_LABELS[norm_key]}: {val:.4f} (hardcoded default)")
        else:
            print(f"{_CONFIG_KEY_LABELS[norm_key]}: {val:.4f}")
        return 0

    if sub == "set":
        # `shorts config set <key> <value>` OR `shorts config set <IP> <key> <value>`
        target = getattr(args, "target", None)
        key = getattr(args, "key", None)
        value = getattr(args, "value", None)

        if value is None:
            # 3-arg form: `shorts config set <key> <value>` → global
            value = float(key)
            key = target
            target = None
            norm_key = _normalize_key(key)
            if norm_key is None:
                print(f"Unknown config key: {key}")
                return 1
            db.set_config(norm_key, value)
            print(f"✅ Set global {_CONFIG_KEY_LABELS.get(norm_key, norm_key)} = {value}")
        else:
            # 4-arg form: `shorts config set <IP> <key> <value>` → per-device
            ip = target
            norm_key = _normalize_key(key)
            if norm_key is None:
                print(f"Unknown config key: {key}")
                return 1
            col = db.KEY_TO_DEVICE_COLUMN.get(norm_key)
            if col is None:
                print(f"Key {key} cannot be set per-device (no device column).")
                return 1
            dev = db.get_device(ip)
            if not dev:
                print(f"Device not found: {ip}")
                return 1
            db.update_device(ip, **{col: float(value)})
            print(f"✅ Set {ip} {_CONFIG_KEY_LABELS.get(norm_key, norm_key)} = {value}")
        return 0

    if sub == "reset":
        # `shorts config reset [IP]` — clear per-device overrides
        ip = getattr(args, "ip", None)
        if not ip:
            print("Usage: shorts config reset <IP>")
            return 1
        dev = db.get_device(ip)
        if not dev:
            print(f"Device not found: {ip}")
            return 1
        db.reset_device_config(ip)
        print(f"✅ Reset per-device config for {ip} → using global defaults")
        return 0

    # default: just show help
    print("Usage: shorts config [show|get|set|reset] ...")
    return 0


def _normalize_key(key: str) -> str | None:
    """Normalize a user-facing key name to the internal config key."""
    # Direct mapping of display names
    DISPLAY_TO_KEY = {v: k for k, v in _CONFIG_KEY_LABELS.items()}
    # Also accept the full internal names
    DISPLAY_TO_KEY.update({k: k for k in db.CONFIG_KEYS})
    return DISPLAY_TO_KEY.get(key)


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

    # config
    p = subparsers.add_parser("config", help="Show/get/set global or per-device config")
    sp = p.add_subparsers(dest="config_sub", help="Config sub-commands")

    # config show [IP]
    ps = sp.add_parser("show", help="Show all config keys (global defaults, or per-device effective if IP given)")
    ps.add_argument("ip", nargs="?", help="Device IP (optional)")
    ps.set_defaults(func=cmd_config)

    # config get <key>
    pg = sp.add_parser("get", help="Get a specific global config value")
    pg.add_argument("key", help="Config key (e.g. width_threshold, max_aspect_ratio)")
    pg.set_defaults(func=cmd_config)

    # config set <key> <value>   OR   config set <IP> <key> <value>
    ps_set = sp.add_parser("set", help="Set a global or per-device config value")
    ps_set.add_argument("target", help="IP address (for per-device) or config key (for global)")
    ps_set.add_argument("key", nargs="?", help="Config key (if target is IP)")
    ps_set.add_argument("value", nargs="?", help="Value (if target is IP, otherwise this is the value)")
    ps_set.set_defaults(func=cmd_config)

    # config reset <IP>
    pr = sp.add_parser("reset", help="Clear per-device overrides → use global defaults")
    pr.add_argument("ip", help="Device IP")
    pr.set_defaults(func=cmd_config)

    p.set_defaults(func=cmd_config)

    # detect
    p = subparsers.add_parser("detect", help="Re-detect screen resolution via ADB and update DB")
    p.add_argument("ip", help="Fire TV IP address")
    p.set_defaults(func=cmd_detect)

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
