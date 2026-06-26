#!/usr/bin/env python3
"""Shared helpers for portable BYD Python scripts."""
from __future__ import annotations

import os
from pathlib import Path

from pybyd import BydClient, BydConfig


SCRIPT_DIR = Path(__file__).resolve().parent
ENV_PATH = SCRIPT_DIR / ".env"
VEHICLE_VIN_ENV = "BYD_VIN"
VEHICLE_ALIAS_ENV = "BYD_VEHICLE_ALIAS"


def load_env_file(path: Path = ENV_PATH) -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ (no overwrite)."""
    if not path.is_file():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def prepare_byd_env() -> None:
    """Load env vars and bridge BYD_PIN to BYD_CONTROL_PIN when needed."""
    load_env_file()
    if "BYD_PIN" in os.environ and "BYD_CONTROL_PIN" not in os.environ:
        os.environ["BYD_CONTROL_PIN"] = os.environ["BYD_PIN"]


def create_config() -> BydConfig:
    """Create pyBYD config from environment."""
    prepare_byd_env()
    return BydConfig.from_env()


async def get_target_vehicle(client: BydClient):
    """Return a selected vehicle using BYD_VIN or BYD_VEHICLE_ALIAS when provided."""
    vehicles = await client.get_vehicles()
    if not vehicles:
        raise RuntimeError("No vehicles tied to this account")

    wanted_vin = os.environ.get(VEHICLE_VIN_ENV, "").strip()
    if wanted_vin:
        for vehicle in vehicles:
            if vehicle.vin == wanted_vin:
                return vehicle
        raise RuntimeError(f"No vehicle found for {VEHICLE_VIN_ENV}={wanted_vin}")

    wanted_alias = os.environ.get(VEHICLE_ALIAS_ENV, "").strip().lower()
    if wanted_alias:
        for vehicle in vehicles:
            alias = (vehicle.auto_alias or "").strip().lower()
            if alias == wanted_alias:
                return vehicle
        raise RuntimeError(f"No vehicle found for {VEHICLE_ALIAS_ENV}={wanted_alias}")

    return vehicles[0]
