---
name: weather-lookup
description: >
  Get current weather conditions for any city using the Open-Meteo API.
  Use when the user asks about weather, temperature, or forecast.
user-invocable: true
metadata:
  openclaw:
    requires:
      env: ["HOME"]
---

# Weather Lookup

Fetches current weather for a given city using the free Open-Meteo API.
No API key required.

## When to use
- User asks "what's the weather in X?"
- User asks about temperature, rain, or forecast for a location

## Input
city: string — city name (e.g. "London", "Tokyo")

## Output
JSON with temp (°C), condition, humidity, wind speed

## How it works
1. Geocode the city name to lat/lon via Open-Meteo geocoding API
2. Fetch current weather from Open-Meteo forecast API
3. Return formatted result

## Example
User: "What's the weather in Paris?"
→ Calls weather API for Paris coordinates
→ Returns: { city: "Paris, France", temp: "18°C", condition: "Partly cloudy" }

## Notes
- Uses only public, free APIs — no authentication needed
- Read-only — does not write any files
- No shell commands used
