"""Device configuration management — backed by SQLite.

Delegates all device CRUD to clawshorts_db (scripts/).
Preserves the same public API for backward compatibility with cli.py.
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

import yaml

# Import db from scripts/ directory
_scripts_dir = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(_scripts_dir))
try:
    import clawshorts_db as db
except ImportError:
    raise ImportError("clawshorts_db not found — ensure scripts/ is accessible")

from .constants import STATE_DIR
from .device import Device
from .validators import validate_ipv4

__all__ = [
    "ConfigError",
    "add_device",
    "configure_logging",
    "get_config_path",
    "get_device",
    "load_devices",
    "remove_device",
    "save_devices",
    "set_config_path",
    "update_device",
    "validate_device_input",
]

log = logging.getLogger(__name__)

_CONFIG_FILE = STATE_DIR / "devices.yaml"  # kept for compat, not used


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
        datefmt="%H:%M:%S",
    )


# ---------------------------------------------------------------------------
# Config paths (kept for compat)
# ---------------------------------------------------------------------------

def get_config_path() -> Path:
    return _CONFIG_FILE


def set_config_path(path: Path) -> None:
    global _CONFIG_FILE
    _CONFIG_FILE = Path(path)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ConfigError(Exception):
    pass


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_device_input(ip: str, name: str | None = None) -> tuple[bool, str]:
    """Validate device input. Returns (ok, error_message)."""
    if not validate_ipv4(ip):
        return False, f"Invalid IP format: {ip}"
    if name:
        import re
        if not re.match(r"^[a-zA-Z0-9\-_]+$", name):
            return False, "Name can only contain alphanumeric, hyphen, underscore"
        if len(name) > 50:
            return False, "Name must be 50 characters or less"
    return True, ""


# ---------------------------------------------------------------------------
# Public API — delegates to clawshorts_db
# ---------------------------------------------------------------------------

def load_devices() -> list[Device]:
    """Load all enabled devices from SQLite. Migrates from YAML if needed."""
    # Migration: if YAML exists but DB is empty, migrate
    _migrate_yaml_to_db()
    db_devices = db.get_devices()
    return [_row_to_device(d) for d in db_devices]


def get_device(ip: str) -> Device | None:
    """Get a single device by IP."""
    d = db.get_device(ip)
    return _row_to_device(d) if d else None


def add_device(ip: str, name: str | None = None, limit: int = 300) -> Device:
    """Add or replace a device in SQLite."""
    db.add_device(ip, name, float(limit))
    return Device(ip=ip, name=name, limit=limit)


def remove_device(ip: str) -> bool:
    """Remove a device (soft-disable)."""
    return db.remove_device(ip)


def update_device(ip: str, **kwargs: Any) -> Device | None:
    """Update device fields."""
    result = db.update_device(ip, **kwargs)
    if result:
        return _row_to_device(result)
    return None


def save_devices(devices: list[Device]) -> None:
    """Replace all devices. For compat only — prefer direct DB calls."""
    for d in devices:
        db.add_device(d.ip, d.name, float(d.limit))


# ---------------------------------------------------------------------------
# Migration
# ---------------------------------------------------------------------------

def _migrate_yaml_to_db() -> None:
    """One-time migration: read devices from YAML, insert into SQLite, delete YAML."""
    yaml_path = STATE_DIR / "devices.yaml"
    if not yaml_path.exists():
        return

    db.init_db()
    existing = db.get_devices()
    if existing:
        # DB already has devices — migration was already done, clean up old YAML
        log.info("DB already has %d device(s). Removing old YAML.", len(existing))
        yaml_path.unlink()
        return

    try:
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
# Helpers
# ---------------------------------------------------------------------------

def _row_to_device(row: dict) -> Device:
    """Convert a DB row dict to a Device model."""
    return Device(
        ip=row["ip"],
        name=row.get("name"),
        limit=int(row["limit_val"]),
        enabled=bool(row.get("enabled", True)),
    )
