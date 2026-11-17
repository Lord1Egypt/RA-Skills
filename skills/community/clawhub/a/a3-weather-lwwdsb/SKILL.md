---
name: a3-weather
description: "Daily weather forecast for any city or coordinates with a practical day plan (umbrella/sunscreen/layers tips and the best dry, comfortable outdoor window). Uses the free Open-Meteo API; no API key."
homepage: https://open-meteo.com
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["node"] } } }
---

# a3-weather

Use when the user asks about the weather, whether to bring an umbrella, what to wear,
or when to go outside — for today, tomorrow, or a specific date up to 7 days ahead.

## Run

If `a3-weather` is on PATH, call it directly; otherwise run the bundled script:

```
a3-weather --city "Los Angeles"
node {baseDir}/scripts/a3-weather.mjs --city "Los Angeles"
```

Options:

- `--city NAME` — place name (geocoded by Open-Meteo), or `--lat N --lon N [--name LABEL]`.
- `--date today|tomorrow|YYYY-MM-DD` — default `today` (in the location's own timezone).
- `--units imperial|metric` — default `imperial` (°F, mph, in). Use the user's stated preference.
- `--json` — machine-readable output (conditions, high/low, precipitation, wind, UV, plan, source).

Use the user's home location from USER.md when they don't name a place.

## Reading the result

- Exit 0: a forecast. Relay the summary line; keep units as returned.
- Exit 2: invalid input — fix the arguments (the JSON `reason` says what is wrong).
- Exit 3: data unavailable (no such place, date outside the 7-day range, or the
  weather service failed). Tell the user the forecast is unavailable and why.
  **Never invent or estimate weather values.**

Always mention that data comes from Open-Meteo (CC BY 4.0) when giving a forecast.
