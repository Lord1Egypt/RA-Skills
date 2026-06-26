---
name: byd-remote-control
description: Control and check a BYD vehicle using portable Python helper scripts built on pyBYD. Use when the user wants to check battery state, lock the car, flash lights, start A/C, stop A/C, or build/operate reusable BYD remote-control automation from local scripts and environment variables.
---

# BYD Remote Control

Use the bundled Python scripts in `scripts/` for repeatable BYD actions instead of rewriting the same pyBYD code each time.

## Available scripts

- `scripts/battery_check.py` , fetch battery %, range, charging state, and timestamps as JSON
- `scripts/battery_monitor.py` , fetch battery state and emit an alert payload when battery is below `BATTERY_THRESHOLD`
- `scripts/lock_car.py` , lock the vehicle
- `scripts/flash_lights.py` , flash lights / horn
- `scripts/start_ac.py` , start climate control
- `scripts/stop_ac.py` , stop climate control
- `scripts/byd_common.py` , shared helper module used by the scripts

## How to use

1. Read `references/setup.md` if credentials or dependencies are not already configured.
2. Run the relevant script from the skill directory so `.env` is discovered correctly.
3. Prefer the existing script over ad hoc inline Python when the task matches one of the bundled actions.

## Notes

- The scripts load `.env` from the same directory as the scripts.
- `BYD_PIN` is automatically bridged to `BYD_CONTROL_PIN`.
- Vehicle selection can be controlled with `BYD_VIN` or `BYD_VEHICLE_ALIAS`. If neither is set, the scripts use the first vehicle returned by the account.
- `battery_monitor.py` prints alert JSON when below threshold. Delivery should be handled by the caller or automation layer.
