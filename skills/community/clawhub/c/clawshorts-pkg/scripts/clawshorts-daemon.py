"""ClawShorts — Fire TV YouTube Shorts time limiter daemon.

Monitors Fire TV devices via ADB. When YouTube Shorts is detected
(video player width < 90pc of screen width), watch time is accumulated.
Once the daily limit (default 120 s = 2 min) is reached, YouTube is
force-stopped. The limit resets automatically at midnight.

Usage:
    python3 clawshorts-daemon.py 192.168.1.100
    python3 clawshorts-daemon.py 192.168.1.100 --debug
    python3 clawshorts-daemon.py 192.168.1.100,192.168.1.101 --daily-limit 120
"""
from __future__ import annotations

import argparse
import logging
import logging.handlers
import re
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

# Add src/ to path for shared modules
_SCRIPTS_DIR = Path(__file__).resolve().parent
_SRC_DIR = _SCRIPTS_DIR.parent / "src"
sys.path.insert(0, str(_SCRIPTS_DIR))  # for clawshorts_db
sys.path.insert(0, str(_SRC_DIR))        # for clawshorts packages

import clawshorts_db as db
from clawshorts.constants import (
    MAX_DELTA_SECONDS,
    SHORTS_FALLBACK_HEIGHT_RATIO,
    SHORTS_WIDTH_THRESHOLD_STRICT,
    SHORTS_MAX_ASPECT_RATIO,
    STATE_DIR,
)
from clawshorts.validators import validate_ipv4

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOG_FILE = STATE_DIR / "daemon.log"
ADB_PORT: Final = 5555
ADB_TIMEOUT: Final = 8
HEARTBEAT_INTERVAL: Final = 30.0  # seconds between heartbeat log lines

YOUTUBE_PACKAGES = (
    "com.google.android.youtube.tv",
    "com.amazon.firetv.youtube",
    "com.amazon.youtube.tv",
    "com.google.android.youtube",
    "com.youtube.tv",
)


# ---------------------------------------------------------------------------
# Config — loaded from DB at startup
# ---------------------------------------------------------------------------

def _load_devices_from_db() -> list[tuple[str, float]]:
    """Load [(ip, limit_val), ...] from SQLite. Migrates from YAML if needed."""
    db.init_db()
    devs = db.get_devices()
    if not devs:
        # Migration: check if old YAML has devices
        _migrate_from_yaml()
        devs = db.get_devices()
    return [(d["ip"], d["limit_val"]) for d in devs if d.get("enabled", True)]


def _migrate_from_yaml() -> None:
    """One-time migration from YAML to SQLite."""
    yaml_path = STATE_DIR / "devices.yaml"
    if not yaml_path.exists():
        return
    try:
        import yaml
        data = yaml.safe_load(yaml_path.read_text())
        if not data or "devices" not in data:
            return
        migrated = 0
        for d in data.get("devices", []):
            db.add_device(
                ip=d.get("ip"),
                name=d.get("name"),
                limit_val=float(d.get("limit", 300)),
            )
            migrated += 1
        log.info("Migrated %d device(s) from YAML to SQLite", migrated)
        yaml_path.unlink()
        log.info("Deleted old devices.yaml")
    except Exception as e:
        log.warning("Migration failed: %s", e)


# ---------------------------------------------------------------------------
# Per-device in-memory state
# ---------------------------------------------------------------------------

@dataclass
class DeviceState:
    """Mutable state for one device within a DaemonContext."""

    last_short_ts: float = 0.0  # monotonic ts of last poll that detected Shorts
    screen_w: int = 0           # cached screen width (pixels)
    screen_h: int = 0           # cached screen height (pixels)
    date: str = ""             # current tracking date (midnight rollover)


# ---------------------------------------------------------------------------
# DaemonContext — wraps all mutable globals
# ---------------------------------------------------------------------------

class DaemonContext:
    """Holds all mutable daemon state. Passed explicitly; no module-level _vars."""

    def __init__(self, devices: list[tuple[str, float]], interval: int) -> None:
        self.devices = devices  # [(ip, limit_val), ...]
        self.interval = interval
        self.states: dict[str, DeviceState] = {ip: DeviceState() for ip, _ in devices}
        self.shutdown: bool = False
        self.last_heartbeat: float = time.time()

    def request_shutdown(self) -> None:
        self.shutdown = True


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def _setup_logging(debug: bool) -> None:
    global log
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-7s %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    fh = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=1_048_576, backupCount=3, encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(fmt)
    log = logging.getLogger("clawshorts")
    log.setLevel(logging.DEBUG)
    log.addHandler(fh)
    log.addHandler(ch)


# ---------------------------------------------------------------------------
# Signal handling
# ---------------------------------------------------------------------------

def _make_signal_handler(ctx: DaemonContext):
    def _handler(signum: int, _frame: object) -> None:
        log.info("Shutdown requested (signal %d)", signum)
        ctx.request_shutdown()
    return _handler


# ---------------------------------------------------------------------------
# ADB helpers
# ---------------------------------------------------------------------------

def _dev(ip: str) -> str:
    """Return device address with port."""
    return f"{ip}:{ADB_PORT}"


def _shell(ip: str, cmd: str, timeout: int = ADB_TIMEOUT) -> str:
    """Execute an ADB shell command on the device. Returns stdout or empty str."""
    try:
        r = subprocess.run(
            ["adb", "-s", _dev(ip), "shell", cmd],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return r.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def _ensure_connected(ip: str) -> bool:
    """Ensure ADB is connected. Connect if needed. Returns True on success."""
    try:
        r = subprocess.run(
            ["adb", "devices"], capture_output=True, text=True, timeout=ADB_TIMEOUT,
        )
        if f"{_dev(ip)}\tdevice" in r.stdout:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False

    try:
        r = subprocess.run(
            ["adb", "connect", _dev(ip)], capture_output=True, text=True, timeout=15,
        )
        ok = "connected" in r.stdout.lower()
        if ok:
            log.info("Connected to %s", ip)
        else:
            log.warning("Cannot connect to %s: %s", ip, r.stdout.strip())
        return ok
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def _is_youtube_active(ip: str) -> bool:
    """Return True only if a YouTube package is the foreground (resumed) activity."""
    # Check mResumedActivity — this is the actual foreground activity on Fire OS
    out = _shell(
        ip,
        "dumpsys activity activities | grep -m1 'mResumedActivity'",
        timeout=10,
    )
    # Only count if a YouTube package is in the RESUMED activity (foreground)
    # This prevents false positives when YouTube is backgrounded but still in memory
    return any(pkg in out for pkg in YOUTUBE_PACKAGES)


def _get_screen_size(state: DeviceState, ip: str) -> tuple[int, int]:
    """Return (width, height) in pixels, cached after first successful query."""
    if state.screen_w and state.screen_h:
        return state.screen_w, state.screen_h
    out = _shell(ip, "wm size", timeout=6)
    m = re.search(r"(\d+)x(\d+)", out)
    if m:
        state.screen_w, state.screen_h = int(m.group(1)), int(m.group(2))
        log.debug("%s — screen: %dx%d", ip, state.screen_w, state.screen_h)
    return state.screen_w or 1920, state.screen_h or 1080


def _dump_ui(ip: str) -> str:
    """Dump UI hierarchy XML from the device. Returns empty string on failure."""
    slug = ip.replace('.', '-')
    tmp = STATE_DIR / f"ui-{slug}.xml"

    # Security: resolve path and ensure it's within STATE_DIR
    resolved = tmp.resolve()
    if not str(resolved).startswith(str(STATE_DIR.resolve())):
        log.error("Path traversal attempt detected: %s", ip)
        return ""

    try:
        _shell(ip, "uiautomator dump /sdcard/ui.xml", timeout=15)
        r = subprocess.run(
            ["adb", "-s", _dev(ip), "pull", "/sdcard/ui.xml", str(tmp)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return tmp.read_text(errors="replace") if r.returncode == 0 else ""
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def _is_shorts(state: DeviceState, ip: str, xml: str) -> bool:
    """Detect YouTube Shorts using dual criteria:
      1. Width < 45% of screen width (strict threshold)
      2. Aspect ratio < 1.3 (portrait-ish, distinguishes from 16:9 hover previews)

    YouTube home hover previews are 16:9 landscape (~1.78 aspect).
    Actual Shorts are 9:16 portrait (<1.0 aspect).
    Both can appear as ~38% width — aspect ratio differentiates them.

    Strategy:
      1. Focused element (Fire TV YouTube puts focus on the video)
      2. Named player / surface / video elements
      3. Last fallback: centred elements filling significant height
    """
    screen_w, screen_h = _get_screen_size(state, ip)
    strict_threshold = screen_w * SHORTS_WIDTH_THRESHOLD_STRICT

    # Primary: focused element
    for m in re.finditer(
        r'focused="true"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml
    ):
        x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        player_w = x2 - x1
        player_h = y2 - y1
        if player_w < 100:
            continue
        ratio = player_w / screen_w
        aspect = player_w / player_h if player_h > 0 else 999
        log.debug("%s — focused %dx%dpx (%.0f%%, ar=%.2f)", ip, player_w, player_h, ratio * 100, aspect)
        # Must pass BOTH: width strict threshold AND portrait aspect
        return player_w < strict_threshold and aspect < SHORTS_MAX_ASPECT_RATIO

    # Secondary: named player / surface / video elements
    for m in re.finditer(
        r'resource-id="[^"]*(?:player|surface|video)[^"]*"[^>]*'
        r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
        xml, re.I,
    ):
        x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        player_w = x2 - x1
        player_h = y2 - y1
        if player_w < 100:
            continue
        ratio = player_w / screen_w
        aspect = player_w / player_h if player_h > 0 else 999
        log.debug("%s — player %dx%dpx (%.0f%%, ar=%.2f)", ip, player_w, player_h, ratio * 100, aspect)
        return player_w < strict_threshold and aspect < SHORTS_MAX_ASPECT_RATIO

    # Fallback: centred elements that fill significant height
    best_w, best_h = 0, 0
    for m in re.finditer(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml):
        x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        w, h = x2 - x1, y2 - y1
        if h > screen_h * SHORTS_FALLBACK_HEIGHT_RATIO and x1 > 0 and x2 < screen_w and w > best_w:
            best_w, best_h = w, h

    if best_w == 0:
        return False

    ratio = best_w / screen_w
    aspect = best_w / best_h if best_h > 0 else 999
    log.debug("%s — fallback %dx%dpx (%.0f%%, ar=%.2f)", ip, best_w, best_h, ratio * 100, aspect)
    return best_w < strict_threshold and aspect < SHORTS_MAX_ASPECT_RATIO


# ---------------------------------------------------------------------------
# Enforcement
# ---------------------------------------------------------------------------

def _force_stop_youtube(ip: str) -> None:
    """Force-stop whichever YouTube package is installed on the device."""
    installed = _shell(ip, "pm list packages", timeout=10)
    for pkg in YOUTUBE_PACKAGES:
        if f"package:{pkg}" in installed:
            subprocess.run(
                ["adb", "-s", _dev(ip), "shell", "am", "force-stop", pkg],
                capture_output=True,
                timeout=8,
            )
            log.info("%s — Force-stopped %s", ip, pkg)


# ---------------------------------------------------------------------------
# Per-device processing
# ---------------------------------------------------------------------------

def _process_device(ip: str, today: str, daily_limit: float, state: DeviceState) -> None:
    if not _ensure_connected(ip):
        state.last_short_ts = 0.0
        return

    if not _is_youtube_active(ip):
        state.last_short_ts = 0.0
        return

    xml = _dump_ui(ip)
    if not xml:
        state.last_short_ts = 0.0
        return

    now = time.monotonic()

    if not _is_shorts(state, ip, xml):
        state.last_short_ts = 0.0
        return

    # Shorts is actively playing — accumulate elapsed time
    prev_ts = state.last_short_ts
    state.last_short_ts = now  # Set FIRST so first detection counts on next poll
    if prev_ts > 0:
        delta = now - prev_ts
        if delta <= MAX_DELTA_SECONDS:
            db.add_seconds(ip, today, delta)
            log.debug("%s — +%.1fs", ip, delta)

    total = db.get_seconds(ip, today)
    remaining = max(0.0, daily_limit - total)
    log.info(
        "%s — Shorts: %.0fs / %.0fs used  (%.0fs remaining)",
        ip, total, daily_limit, remaining,
    )

    if total >= daily_limit:
        log.info("%s — Daily limit reached (%.0fs). Stopping YouTube.", ip, daily_limit)
        _force_stop_youtube(ip)
        state.last_short_ts = 0.0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(
        description="ClawShorts — Fire TV YouTube Shorts time limiter"
    )
    p.add_argument(
        "--interval", type=int, default=3,
        metavar="SECONDS", help="Poll interval in seconds (default: 3)",
    )
    p.add_argument("--debug", action="store_true", help="Enable verbose debug logging")
    args = p.parse_args()

    _setup_logging(args.debug)

    # Load devices from SQLite — single source of truth
    devices = _load_devices_from_db()
    if not devices:
        log.error("No devices found in database. Run 'shorts setup <IP>' first.")
        sys.exit(1)

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    db.init_db()

    ctx = DaemonContext(devices, args.interval)

    # Wire up signals
    signal.signal(signal.SIGINT, _make_signal_handler(ctx))
    signal.signal(signal.SIGTERM, _make_signal_handler(ctx))

    log.info(
        "ClawShorts started | %d device(s) | poll=%ds | db=%s",
        len(devices), args.interval, db.DB_PATH,
    )

    try:
        while not ctx.shutdown:
            today = time.strftime("%Y-%m-%d")

            for ip, daily_limit in ctx.devices:
                state = ctx.states[ip]

                # Midnight rollover
                if state.date and state.date != today:
                    log.info("%s — New day (%s). Daily limit reset.", ip, today)
                    state.last_short_ts = 0.0
                state.date = today

                try:
                    _process_device(ip, today, daily_limit, state)
                except Exception:
                    log.exception("Unexpected error processing %s", ip)

                if ctx.shutdown:
                    break

            time.sleep(ctx.interval)

            # Heartbeat
            now = time.time()
            if now - ctx.last_heartbeat >= HEARTBEAT_INTERVAL:
                log.info("HEARTBEAT — daemon alive")
                ctx.last_heartbeat = now

    finally:
        log.info("ClawShorts daemon stopped.")


if __name__ == "__main__":
    main()
