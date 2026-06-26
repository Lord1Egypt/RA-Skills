from __future__ import annotations
from datetime import datetime
from typing import Dict, Optional
from ..utils.language import Translator, get_language_from_config

NA = '—'


def build_report(
    results: list[dict],
    weather_data: dict = None,
    config: Optional[Dict] = None,
    query_text: Optional[str] = None
) -> str:
    if config is None:
        config = {}

    language = get_language_from_config(config, query_text)
    t = lambda key: Translator.get_translation(key, language)  # noqa: E731

    lines = [f"# 🌱 {t('daily_report')}", '']
    lines.append(f"*{t('generated_at')}: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*")
    lines.append('')
    lines.append('---')
    lines.append('')

    # --- Weather section (always rendered) ---
    lines.append(f"## 🌤️ {t('weather_summary')}")
    history = (weather_data or {}).get('history', {})
    forecast = (weather_data or {}).get('forecast', {})
    h_daily = history.get('daily', {})
    f_daily = forecast.get('daily', {})

    if h_daily and f_daily:
        recent_rain = sum(h_daily.get('precipitation_sum', [])[-7:])
        today_rain  = f_daily.get('precipitation_sum', [None])[0]
        temp_max    = f_daily.get('temperature_2m_max', [None])[0]
        temp_min    = f_daily.get('temperature_2m_min', [None])[0]
        wx_code     = f_daily.get('weathercode', [None])[0]

        rain_str    = f"**{recent_rain:.1f} mm**"
        today_str   = f"**{today_rain:.1f} mm**" if today_rain is not None else f"**{NA}**"
        temp_str    = f"**{temp_min:.1f}°C – {temp_max:.1f}°C**" if temp_min is not None else f"**{NA}**"
        wx_str      = f"**{Translator.translate_weather_code(wx_code, language)}**" if wx_code is not None else f"**{NA}**"
    else:
        rain_str = today_str = temp_str = wx_str = f"**{NA}**"

    lines.append(f"- {t('recent_7day_rain')}: {rain_str}")
    lines.append(f"- {t('today_forecast_rain')}: {today_str}")
    lines.append(f"- {t('today_temperature')}: {temp_str}")
    lines.append(f"- {t('conditions')}: {wx_str}")
    lines.append('')
    lines.append('---')
    lines.append('')

    # --- Sensor status section (always rendered) ---
    lines.append(f"## 📡 {t('device_status')}")
    all_sensors = [s for item in results for s in item.get('sensors', [])]

    if all_sensors:
        online_count = sum(1 for s in all_sensors if s.get('online', False))
        lines.append(f"{t('online_devices')}: **{online_count}/{len(all_sensors)}**")
        lines.append('')
        for sensor in all_sensors:
            emoji = '🟢' if sensor.get('online', False) else '🔴'
            status_text = t('online') if sensor.get('online', False) else t('offline')
            lines.append(f"### {emoji} {sensor.get('name', 'Unknown')} — {status_text}")

            avg_24h   = sensor.get('moisture_24h_avg')
            avg_count = sensor.get('moisture_24h_count', 0)
            current   = sensor.get('moisture_current')
            avg_str = f"**{avg_24h}%** *({avg_count} readings)*" if avg_24h is not None else f"**{NA}**"
            cur_str = f"**{current}%**" if current is not None else f"**{NA}**"
            lines.append(f"- {t('soil_moisture')} (avg last 50): {avg_str}")
            lines.append(f"- {t('soil_moisture')} (now): {cur_str}")

            temp = sensor.get('temperature')
            lines.append(f"- {t('temperature')}: **{temp}°C**" if temp is not None else f"- {t('temperature')}: **{NA}**")

            battery = sensor.get('battery')
            if battery is not None:
                lines.append(f"- {t('battery')}: **{battery}%** ({Translator.get_battery_status(battery, language)})")
            else:
                lines.append(f"- {t('battery')}: **{NA}**")

            if sensor.get('error'):
                lines.append(f"- {t('error')}: {sensor['error']}")

            lines.append('')
    else:
        lines.append(f"*{t('no_sensor_data')}*")
        lines.append('')

    lines.append('---')
    lines.append('')

    # --- Irrigation decision section (always rendered) ---
    lines.append(f"## 💧 {t('irrigation_decision')}")
    lines.append('')
    for item in results:
        decision = item['decision']
        should   = decision.get('should_irrigate', False)
        minutes  = decision.get('minutes', 0)
        yes_no   = t('yes') if should else t('no')
        dur_str  = f"**{minutes} {t('minutes')}**" if should and minutes > 0 else f"**{NA}**"

        lines.append(f"### {item['zone_name']}")
        lines.append(f"- {t('should_irrigate')}: **{yes_no}**")
        lines.append(f"- {t('watering_duration')}: {dur_str}")
        lines.append(f"- {t('decision_reason')}: {decision.get('reason', NA)}")
        lines.append('')

    return '\n'.join(lines)


def _weathercode_to_description(code: int) -> str:
    """Convert WMO weather code to description."""
    weather_codes = {
        0: "Clear",
        1: "Mostly clear",
        2: "Partly cloudy",
        3: "Cloudy",
        45: "Fog",
        48: "Fog",
        51: "Light rain",
        53: "Moderate rain",
        55: "Heavy rain",
        56: "Freezing drizzle",
        57: "Freezing drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Freezing rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy rain showers",
        85: "Snow showers",
        86: "Snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Heavy thunderstorm with hail"
    }
    return weather_codes.get(code, f"Unknown weather (code {code})")
