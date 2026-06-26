from __future__ import annotations

import json
import urllib.request


class WeatherClient:
    def history_and_forecast(self, latitude: float, longitude: float, timezone: str) -> dict:
        """Fetch rolling 7-day history + 3-day forecast from Open-Meteo in a single call."""
        url = (
            'https://api.open-meteo.com/v1/forecast'
            f'?latitude={latitude}&longitude={longitude}'
            '&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode'
            f'&timezone={timezone}&past_days=7&forecast_days=3'
        )
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read().decode())

        daily = data.get('daily', {})
        # First 7 entries are past days, remaining are forecast
        history_daily = {k: v[:7] for k, v in daily.items()}
        forecast_daily = {k: v[7:] for k, v in daily.items()}

        return {
            'history': {'daily': history_daily},
            'forecast': {'daily': forecast_daily},
        }
