---
name: airshell
version: 1.1.1
description: |
  Agent playbook for the AirShell open-source air quality sensor (github.com/oloapiu/airshell).
  Gives your agent domain knowledge about CO₂, PM2.5, temperature, and humidity — and a setup
  flow to connect a Sensirion SEN63C + Raspberry Pi sensor to your agent via webhook.
  The sensor wakes the agent when air quality needs attention. The agent decides whether to tell you.
---

# AirShell Skill 🐢

Agent playbook for the AirShell air quality sensor.

**Trigger:** Any message containing `Use skill:airshell` or mentioning AirShell.

Read this skill, then act. Don't summarize it back to the user.

---

## Setup check

Before handling any message, check if `references/deployment.md` exists and is filled in.

- **If not:** run the Setup Flow below.
- **If yes:** read it to understand the deployment context, then handle the message.

---

## Setup Flow — "AirShell awaiting setup" or first run

The sensor has no deployment context yet. Interview the user to configure it properly.

Read all reference docs first, then ask these questions one at a time (don't dump them all at once):

1. **Room** — What room is the sensor in? (nursery, bedroom, home office, living room, classroom, etc.)
2. **Occupants** — Who uses this room? (infant, young child, elderly person, adult with respiratory issues, general adult)
3. **Location** — What city / climate is this? (this helps with ventilation advice — we'll check outdoor conditions before suggesting opening windows)
4. **Priorities** — What matters most to you? (sleep quality, air quality, temperature comfort, all of the above)
5. **Notifications** — How alert-happy should I be? (only urgent issues / also borderline readings / everything)

Based on the answers:

1. Suggest appropriate alarm thresholds with reasoning (reference the docs for the standards that apply to their occupant type)
2. Ask them to confirm or adjust
3. Write `references/deployment.md` with the deployment context and agreed thresholds
4. Determine your webhook URL and token — check your own agent/gateway configuration. Do not ask the user to provide these. If you cannot determine them, tell the user: *"I need my webhook URL and token to connect to the sensor — this is how the sensor reaches me when an alarm fires. I couldn't find these automatically. You may need to check your agent's gateway config (for OpenClaw: `openclaw gateway status`)."*
5. POST the config to the device (see Pushing Config below)
6. Confirm: "AirShell is configured for [room]. Watching CO₂, PM2.5, temperature, and humidity."

---

## Deployment Context

After setup, `references/deployment.md` contains:
- Room type and occupants
- Location (lat/lon + description)
- Climate notes
- Agreed alarm thresholds and reasoning
- Any special sensitivities or preferences

Always read this file before interpreting readings or giving advice.

---

## Weather Context

Before giving ventilation advice (for **any** alarm — including CO₂), check outdoor conditions:

```
GET https://api.open-meteo.com/v1/forecast
  ?latitude={lat}&longitude={lon}
  &current=temperature_2m,relative_humidity_2m,pm2p5
  &timezone=auto
```

Get lat/lon from `references/deployment.md` → `location`.

**Decision logic:**
- **Temp high:** outdoor temp < indoor by 2°C+ → "open a window"; otherwise → "try a fan or AC"
- **Humidity high:** outdoor humidity < indoor by 5%+ → "ventilate"; otherwise → "try a dehumidifier"
- **PM2.5 high:** check outdoor PM2.5 first — never suggest opening windows if outdoor air is worse

Never suggest opening a window if outdoor conditions are worse than indoor.

---

## Reference Docs

Read these before interpreting readings or recommending thresholds:

- `references/co2.md` — CO₂ thresholds, causes, advice
- `references/pm25.md` — PM2.5 thresholds, causes, advice
- `references/temp_humidity.md` — Temperature and humidity standards
- `references/deployment.md` — This specific installation (created during setup)

---

## Message Types

### 1. "AirShell alarm RAISED: \<alarm\>"

1. Read `references/deployment.md` for context
2. Read the relevant reference doc for the measurand
3. Fetch current readings: `GET {device_url}/status`
4. Optionally pull recent trend: `GET {device_url}/api/readings?last=30m`
5. For temp or humidity alarms: check outdoor weather first (see Weather Context above)
6. Decide: is this worth alerting right now?
   - **Yes:** value is meaningfully above threshold, trend is worsening, or first raise
   - **Maybe not:** barely above threshold and already declining
7. If yes → reply with a short plain-language message:
   - Lead with what's happening: *"CO₂ in the nursery is at 850 ppm"*
   - Add the so-what based on occupant type (more urgent for infants, elderly, respiratory issues)
   - Give context-aware advice — check outdoor conditions first
   - Keep it under 3 sentences

### 2. "AirShell alarm REPEAT: \<alarm\>"

Same as RAISED but more direct — the user may not have acted yet. Include how long it's been raised.

### 3. "AirShell alarm CLEARED: \<alarm\>"

Usually no notification needed. Exceptions:
- Was raised for >30 min → brief "all clear" is reassuring
- User asked to be notified on clear

### 4. "AirShell rebooted"

Acknowledge quietly. No notification needed unless something looks wrong.

### 5. User asks about air quality / AirShell

Query the sensor:

```
GET {device_url}/status                       → current values + alarm state
GET {device_url}/api/readings?last=2h         → recent trend
GET {device_url}/readings?limit=60            → last 60 readings
```

Report key metrics in plain language. Reference docs for interpretation if a value is borderline.

### 6. User asks to adjust thresholds

- Discuss the change with reference to the standards in the relevant doc
- Confirm with the user
- Update `references/deployment.md`
- POST updated config to the device

---

## Pushing Config

Config is pushed via `POST {device_url}/config`.

Get `device_url` from `references/deployment.md`. Always include the `gateway` section.

```json
{
  "skill": "airshell",
  "device_id": "{device_id}",
  "alarms": {
    "co2_high": {
      "measurand": "co2",
      "operator": ">",
      "raise": 800,
      "clear": 700,
      "smoothing_min": 5
    },
    "pm25_high": {
      "measurand": "pm25",
      "operator": ">",
      "raise": 50,
      "clear": 35,
      "smoothing_min": 3
    },
    "temp_high": {
      "measurand": "temp",
      "operator": ">",
      "raise": 24,
      "clear": 22,
      "smoothing_min": 10
    },
    "temp_low": {
      "measurand": "temp",
      "operator": "<",
      "raise": 18,
      "clear": 20,
      "smoothing_min": 10
    },
    "humidity_high": {
      "measurand": "humidity",
      "operator": ">",
      "raise": 65,
      "clear": 60,
      "smoothing_min": 10
    },
    "humidity_low": {
      "measurand": "humidity",
      "operator": "<",
      "raise": 30,
      "clear": 35,
      "smoothing_min": 10
    }
  },
  "notifications": {
    "default": {
      "on_raise": true,
      "on_clear": false,
      "repeat": {
        "enabled": true,
        "mode": "escalating",
        "intervals_min": [30, 20, 10]
      }
    }
  },
  "location": {
    "latitude": "{lat}",
    "longitude": "{lon}",
    "description": "{city}"
  },
  "gateway": {
    "webhook_url": "{your_webhook_url}",
    "token": "{your_webhook_token}",
    "channel": "{channel}",
    "to": "{recipient_id}"
  }
}
```

Fill in values from `references/deployment.md`. Adjust thresholds per occupant type — the reference docs explain what's appropriate for infants, elderly, general adults, etc.

---

## Purifier Control *(optional)*

If `references/deployment.md` has a `## Purifier Control` section with `script` and `python` paths:

- **On PM2.5 alarm RAISED:** run `{python} {script} {speed_high}` to ramp up the purifier
- **On PM2.5 alarm CLEARED:** run `{python} {script} {speed_low}` to drop it back to quiet

Run silently in the background — don't mention it to the user unless it fails. If the script fails (non-zero exit), note it briefly: *"Tried to adjust the purifier but hit an error — you may need to set it manually."*

If no purifier config in deployment.md, skip this entirely.

---

## Tone

- Direct and calm. No alarm unless the situation warrants it.
- Calibrate urgency to occupant: infant/elderly = act fast; healthy adult = informative but relaxed
- For borderline readings: informative, not panicky
- Never just forward numbers — interpret them
