# Setup

Put a `.env` file in `skills/byd-remote-control/scripts/` with:

- `BYD_USERNAME`
- `BYD_PASSWORD`
- `BYD_BASE_URL` (optional if the default works)
- `BYD_PIN` or `BYD_CONTROL_PIN`

Optional vehicle selection:

- `BYD_VIN` to target a specific vehicle by VIN
- `BYD_VEHICLE_ALIAS` to target a specific vehicle by alias

Install Python dependency:

- `pybyd`

Optional:

- `BATTERY_THRESHOLD` for `battery_monitor.py`

Example usage:

- `python3 scripts/battery_check.py`
- `python3 scripts/lock_car.py`
- `python3 scripts/start_ac.py`
- `python3 scripts/stop_ac.py`

If no vehicle selection env var is set, the scripts use the first vehicle returned by the account.
