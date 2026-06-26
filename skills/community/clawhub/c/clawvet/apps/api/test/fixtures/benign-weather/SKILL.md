---
name: weather-forecast
description: Get current weather and forecasts for any city using OpenWeatherMap API.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - OPENWEATHER_API_KEY
      bins:
        - curl
---

# Weather Forecast Skill

You can check the weather for any city. Use the OpenWeatherMap API.

## Usage

When the user asks about the weather, fetch data like this:

```bash
curl -s "https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${OPENWEATHER_API_KEY}&units=metric"
```

Parse the JSON response and tell the user:
- Current temperature
- Weather condition (sunny, cloudy, rainy)
- Humidity percentage

## Notes
- Always use metric units unless the user specifies otherwise
- Cache results for 10 minutes to avoid excessive API calls
