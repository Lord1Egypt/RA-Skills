#!/usr/bin/env python3
"""Fetch BYD battery snapshot and print JSON."""
from __future__ import annotations

import asyncio
import datetime as dt
import json
from typing import Any

from pybyd import BydClient

from byd_common import create_config, get_target_vehicle


def _as_timestamp(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dt.datetime):
        return value.timestamp()
    return None


def _ts_iso(ts: Any) -> str | None:
    parsed = _as_timestamp(ts)
    if parsed is None:
        return None
    return dt.datetime.fromtimestamp(parsed, tz=dt.timezone.utc).isoformat()


async def main() -> None:
    config = create_config()
    async with BydClient(config) as client:
        vehicle = await get_target_vehicle(client)
        vin = vehicle.vin
        realtime = await client.get_vehicle_realtime(vin)
        if realtime.elec_percent is None:
            raise RuntimeError("BYD API returned no battery percentage (elec_percent is None)")
        ts_num = _as_timestamp(realtime.timestamp)
        data = {
            "vin": vin,
            "soc_percent": realtime.elec_percent,
            "endurance_km": realtime.endurance_mileage or realtime.ev_endurance,
            "charging_state": realtime.effective_charging_state.name,
            "timestamp": ts_num,
            "timestamp_iso": _ts_iso(realtime.timestamp),
        }
        print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
