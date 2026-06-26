---
name: dronemobile
description: Control vehicles via DroneMobile (Firstech/Compustar remote start systems). Use when the user asks to start their car, stop the engine, lock/unlock doors, open the trunk, check battery voltage, or get vehicle status. Triggers on phrases like "start my car", "remote start", "lock my car", "unlock the car", "check battery", "open trunk", "stop the engine", "vehicle status". Requires DRONEMOBILE_EMAIL and DRONEMOBILE_PASSWORD environment variables. Optionally DRONEMOBILE_DEVICE_KEY for multi-vehicle accounts.
---

# DroneMobile Vehicle Control

Control any DroneMobile-connected vehicle via natural language.

## Setup

Set credentials in OpenClaw env (openclaw.json → env):
```json
"DRONEMOBILE_EMAIL": "your@email.com",
"DRONEMOBILE_PASSWORD": "yourpassword",
"DRONEMOBILE_DEVICE_KEY": "40632023374"
```

`DRONEMOBILE_DEVICE_KEY` is optional if you have one vehicle — the script auto-selects the first vehicle on the account.

Install the library if not present:
```bash
pip install drone-mobile --break-system-packages
```

## Commands

Run `scripts/dronemobile.py` with the appropriate command:

| User asks | Command |
|-----------|---------|
| Start / remote start | `python3 scripts/dronemobile.py start` |
| Stop engine | `python3 scripts/dronemobile.py stop` |
| Lock doors | `python3 scripts/dronemobile.py lock` |
| Unlock doors | `python3 scripts/dronemobile.py unlock` |
| Open trunk | `python3 scripts/dronemobile.py trunk` |
| Check battery / status | `python3 scripts/dronemobile.py status` |

## Output

The script prints a one-line status with key telemetry:
```
✅ start | Temp: 6°C | Battery: 12.5V | Engine: off
```

On failure it prints the error and exits with code 1.

## Notes

- Commands are fire-and-forget — the car executes asynchronously. Engine-on status may still show False immediately after start (takes ~30s).
- Battery below 11.8V = low; below 11.0V = critical.
- `drone-mobile` PyPI package has a known bug where `response.success` is always False. The script reads `raw_data['command_success']` directly. PR submitted: https://github.com/bjhiltbrand/drone_mobile_python/pull/18
