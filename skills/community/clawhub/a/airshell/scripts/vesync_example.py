"""AirShell purifier control via pyvesync.

Copy this file to vesync.py in the same directory.
vesync.py is gitignored — it stays local.

Credentials are read from environment variables — never hardcode them in this file.
Set them in your shell profile or a .env file:

    export VESYNC_EMAIL="your@email.com"
    export VESYNC_PASSWORD="yourpassword"

Or store them in a secrets file and source it before running.

Requirements:
    pip install pyvesync

Usage (called by the agent via the airshell skill):
    python3 vesync.py 3    # set purifier to speed 3 (high)
    python3 vesync.py 1    # set purifier to speed 1 (low/quiet)
    python3 vesync.py 0    # turn purifier off
"""

import asyncio
import os
import sys

from pyvesync import VeSync

VESYNC_EMAIL = os.environ["VESYNC_EMAIL"]
VESYNC_PASSWORD = os.environ["VESYNC_PASSWORD"]
DEVICE_NAME = os.environ.get("VESYNC_DEVICE", "")  # device name as shown in the Levoit app
TIMEZONE = os.environ.get("VESYNC_TIMEZONE", "Europe/Rome")

SPEED_HIGH = 3   # speed on PM2.5 alarm raise
SPEED_LOW  = 1   # speed on PM2.5 alarm clear


async def set_speed(level: int) -> bool:
    async with VeSync(VESYNC_EMAIL, VESYNC_PASSWORD, time_zone=TIMEZONE) as manager:
        await manager.login()
        await manager.get_devices()
        for dev in manager.devices:
            if dev.device_name == DEVICE_NAME:
                if level == 0:
                    result = await dev.turn_off()
                else:
                    result = await dev.set_fan_speed(level)
                print(f"{'OK' if result else 'FAILED'}: {dev.device_name} → speed {level}")
                return result
        print(f"Device '{DEVICE_NAME}' not found. Available: {[d.device_name for d in manager.devices]}")
        return False


if __name__ == "__main__":
    level = int(sys.argv[1]) if len(sys.argv) > 1 else SPEED_HIGH
    success = asyncio.run(set_speed(level))
    sys.exit(0 if success else 1)
