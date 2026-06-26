# Deployment Context — Example

*This is an example of a filled-in deployment.md for a nursery setup.*
*Copy to `deployment.md` and customize, or let your agent fill it in via the setup interview.*

---

## Installation

- **Device ID:** `airshell-01`
- **Device URL:** `http://<PI_TAILSCALE_IP>:5000`
- **Room:** Nursery
- **Occupants:** Infant, 3 months old

## Location

- **City / description:** Milan, Italy — humid winters, hot dry summers
- **Latitude:** 45.4654
- **Longitude:** 9.1859

## Alarm Thresholds

*(Infant-grade — most conservative)*

| Alarm | Raise | Clear | Smoothing |
|-------|-------|-------|-----------|
| CO₂ high | 800 ppm | 700 ppm | 5 min |
| PM2.5 high | 25 µg/m³ | 15 µg/m³ | 3 min |
| Temp high | 20°C | 18°C | 10 min |
| Temp low | 16°C | 18°C | 10 min |
| Humidity high | 60% | 55% | 10 min |
| Humidity low | 35% | 40% | 10 min |

## Notification Preferences

- Alert on raise: yes
- Alert on clear: only if raised >30 min
- Repeat alerts: yes — escalating intervals: 30, 20, 10 min

## Purifier Control *(optional)*

If you have a smart air purifier, the agent can control it automatically when PM2.5 alarms fire.

- **Script:** path to your local vesync.py (copy from `scripts/vesync_example.py` and fill in credentials)
- **Speed high:** fan speed when PM2.5 alarm raises (e.g. 3)
- **Speed low:** fan speed when PM2.5 alarm clears (e.g. 1)
- **Python:** path to the Python interpreter with pyvesync installed

Credentials are read from environment variables — never put passwords in the script itself:

```bash
export VESYNC_EMAIL="your@email.com"
export VESYNC_PASSWORD="yourpassword"
export VESYNC_DEVICE="Your Device Name"   # exactly as shown in the Levoit app
export VESYNC_TIMEZONE="Europe/Rome"
```

Example deployment config:
```
script: /path/to/skills/airshell/scripts/vesync.py
python: /path/to/skills/airshell/scripts/venv/bin/python
speed_high: 3
speed_low: 1
```

Leave this section out if you don't have a compatible purifier.

## Special Notes

- Sensor self-heats ~1–2°C — actual room temp is ~1–2°C lower than reading
- CO₂ in a closed crib can be 4× room level — keep room well below 800 ppm
- Overheating is a SIDS risk factor — temp alerts are high priority
