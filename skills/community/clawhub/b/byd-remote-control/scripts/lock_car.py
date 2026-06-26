#!/usr/bin/env python3
"""Lock the vehicle via pybyd."""
from __future__ import annotations

import asyncio

from pybyd import BydClient

from byd_common import create_config, get_target_vehicle


async def main() -> None:
    config = create_config()
    async with BydClient(config) as client:
        vehicle = await get_target_vehicle(client)
        vin = vehicle.vin
        await client.verify_command_access(vin)
        result = await client.lock(vin)
        print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
