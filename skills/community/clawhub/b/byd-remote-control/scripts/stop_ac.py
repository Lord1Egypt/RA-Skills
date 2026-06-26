#!/usr/bin/env python3
"""Stop BYD A/C remotely using pyBYD."""

import asyncio

from pybyd.client import BydClient

from byd_common import create_config, get_target_vehicle


async def main():
    config = create_config()
    async with BydClient(config) as client:
        print("🔐 Logging in...")
        await client.login()

        print("🚗 Fetching vehicles...")
        try:
            vehicle = await get_target_vehicle(client)
        except RuntimeError:
            print("❌ No vehicles found!")
            return

        vin = vehicle.vin
        print(f"✅ Found: {vehicle.auto_alias or 'BYD M6'} (VIN: {vin})")

        try:
            await client.verify_command_access(vin)
            print("✅ Command access verified")
        except Exception as e:
            print(f"⚠️ Could not verify command access: {e}")

        print("🛑 Stopping A/C...")
        result = await client.stop_climate(vin=vin)

        message = getattr(result, "message", None)
        success = getattr(result, "success", None)
        control_state = getattr(result, "control_state", None)
        res = getattr(result, "res", None)

        print("📦 Raw response:", result)

        if success is True or control_state == 1:
            print("✅ A/C stopped successfully!")
            if message:
                print(f"   Status: {message}")
            return

        print("⚠️ A/C stop command did not report success.")
        if message:
            print(f"   Message: {message}")
        if res is not None:
            print(f"   Result code: {res}")
        if control_state is not None:
            print(f"   Control state: {control_state}")


if __name__ == "__main__":
    asyncio.run(main())
