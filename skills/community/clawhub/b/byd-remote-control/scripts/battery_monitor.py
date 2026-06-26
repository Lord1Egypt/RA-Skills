#!/usr/bin/env python3
"""
BYD Battery Monitor - Checks vehicle battery level and reports whether it is below threshold.
"""

import asyncio
import json
import os
from datetime import datetime

from pybyd import BydClient

from byd_common import create_config, get_target_vehicle

BATTERY_THRESHOLD = int(os.environ.get("BATTERY_THRESHOLD", "50"))  # Alert if battery falls below this percentage


async def get_battery_snapshot() -> dict | None:
    """Query BYD API for current battery snapshot via pyBYD."""
    try:
        config = create_config()
        async with BydClient(config) as client:
            vehicle = await get_target_vehicle(client)
            vin = vehicle.vin
            realtime = await client.get_vehicle_realtime(vin)
            if realtime.elec_percent is None:
                return None
            return {
                "battery_level": int(realtime.elec_percent),
                "range_km": realtime.endurance_mileage or realtime.ev_endurance,
                "charging_state": getattr(realtime.effective_charging_state, "name", None),
                "vin": vin,
            }
    except Exception as e:
        print(f"Error querying BYD API via pyBYD: {e}")
        return None

def main():
    """Main monitoring logic."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    snapshot = asyncio.run(get_battery_snapshot())

    if snapshot is None:
        print(f"[{timestamp}] ERROR: Unable to retrieve battery level")
        return

    battery_level = snapshot["battery_level"]
    print(f"[{timestamp}] Battery level: {battery_level}%")
    print(json.dumps(snapshot, ensure_ascii=False))

    if battery_level < BATTERY_THRESHOLD:
        print(
            json.dumps(
                {
                    "alert": True,
                    "battery_level": battery_level,
                    "threshold": BATTERY_THRESHOLD,
                    "range_km": snapshot.get("range_km"),
                    "charging_state": snapshot.get("charging_state"),
                    "vin": snapshot.get("vin"),
                    "timestamp": timestamp,
                },
                ensure_ascii=False,
            )
        )
    else:
        print(f"[{timestamp}] Battery OK ({battery_level}% >= {BATTERY_THRESHOLD}%)")

if __name__ == "__main__":
    main()
