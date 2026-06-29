---
name: discord-weather-reporter
version: 1.0.0
description: "Fetch weather forecasts and current conditions, formatted for Discord display. Use when asked about weather, temperature, rain forecasts, or travel planning weather checks. Triggers: 'weather', 'temperature in [city]', 'will it rain', 'forecast for [city]', 'is it going to snow', weather alerts for a location."
---

# Discord Weather Reporter

Fetch current conditions and forecasts, formatted as clean Discord embeds.

## Quick Use

```bash
# Current weather for a city (one-liner)
curl -s "wttr.in/{city}?format=%l:+%c+%t+(feels+like+%f),+%w+wind,+%h+humidity"

# 3-day forecast
curl -s "wttr.in/{city}?format=v2"

# Will it rain?
curl -s "wttr.in/{city}?format=%l:+%c+%p"
```

## Commands

### Current Conditions (one-liner)
```
curl -s "wttr.in/{city}?format=%l:+%c+%t+(feels+like+%f),+%w+wind,+%h+humidity"
```

### 3-Day Forecast
```
curl -s "wttr.in/{city}"
```

### Precipitation Check
```
curl -s "wttr.in/{city}?format=%l:+%c+%p"
```

### Week Forecast
```
curl -s "wttr.in/{city}?format=v2"
```

## Format Codes

- `%c` — Condition emoji
- `%t` — Temperature
- `%f` — "Feels like"
- `%w` — Wind speed
- `%h` — Humidity
- `%p` — Precipitation
- `%l` — Location name

## Examples

**"Weather in London?"**
```
London: ☀️ +18°C (feels like +17°C), 12 km/h wind, 65% humidity
```

**"Will it rain in Tokyo?"**
```
Tokyo: 🌦 Light rain, 4mm expected
```

**"3-day Paris forecast"**
Full 3-day forecast with daily highs/lows

## Notes

- No API key needed (uses wttr.in)
- Rate limited; don't spam requests
- Works for most global cities and airport codes
- Supports airport codes: `curl wttr.in/JFK`
