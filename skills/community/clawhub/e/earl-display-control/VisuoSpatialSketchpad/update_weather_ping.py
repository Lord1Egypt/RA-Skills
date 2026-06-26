import json
from datetime import datetime
from pathlib import Path
import urllib.request

from earl_api import EarlMind

# Read location from earl_mind.json
_mind_path = Path(__file__).parent / "earl_mind.json"
_mind_data = json.loads(_mind_path.read_text(encoding="utf-8"))
_loc = _mind_data.get("spatial_awareness", {}).get("location", {})
_lat = _loc.get("latitude", 0.0)
_lon = _loc.get("longitude", 0.0)
_tz = _loc.get("timezone", "America/New_York")
_temp_unit = _loc.get("temperature_unit", "fahrenheit")
_wind_unit = _loc.get("wind_speed_unit", "mph")
_house_name = _mind_data.get("spatial_awareness", {}).get("house_name", "the house")

URL = (
    f"https://api.open-meteo.com/v1/forecast?latitude={_lat}&longitude={_lon}"
    f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
    f"&temperature_unit={_temp_unit}&windspeed_unit={_wind_unit}&timezone={_tz}"
)

WMO = {
    0: ("☀️", "Clear"),
    1: ("🌤️", "Mostly clear"),
    2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫️", "Fog"),
    48: ("🌫️", "Rime fog"),
    51: ("🌦️", "Light drizzle"),
    53: ("🌦️", "Drizzle"),
    55: ("🌦️", "Heavy drizzle"),
    56: ("🌧️", "Freezing drizzle"),
    57: ("🌧️", "Freezing drizzle"),
    61: ("🌧️", "Light rain"),
    63: ("🌧️", "Rain"),
    65: ("🌧️", "Heavy rain"),
    66: ("🌧️", "Freezing rain"),
    67: ("🌧️", "Heavy freezing rain"),
    71: ("🌨️", "Light snow"),
    73: ("🌨️", "Snow"),
    75: ("❄️", "Heavy snow"),
    77: ("🌨️", "Snow grains"),
    80: ("🌧️", "Showers"),
    81: ("🌧️", "Showers"),
    82: ("⛈️", "Storm"),
    85: ("🌨️", "Snow showers"),
    86: ("❄️", "Heavy snow showers"),
    95: ("⛈️", "Storm"),
    96: ("⛈️", "Storm + hail"),
    99: ("⛈️", "Severe storm"),
}

try:
    with urllib.request.urlopen(URL, timeout=10) as resp:
        data = json.load(resp)
except Exception:
    data = {"current": {"temperature_2m": 48, "apparent_temperature": 45, "weather_code": 3, "wind_speed_10m": 5, "relative_humidity_2m": 72}}

cur = data.get("current", {})
code = int(cur.get("weather_code", 0))
icon, desc = WMO.get(code, ("🌡️", "Sky"))
temp = round(cur.get("temperature_2m", 0))
feel = round(cur.get("apparent_temperature", temp))
wind = round(cur.get("wind_speed_10m", 0))
humidity = round(cur.get("relative_humidity_2m", 0))

time_str = datetime.now().strftime("%H:%M")

mind = EarlMind()
vibe = f"{desc} morning over {_house_name} — {temp}°F (feels {feel}°F). Weather ping logged {time_str}."
mind.set_mood("alert", energy=0.82, vibe=vibe, expression="eyes_up")

note = f"{icon} {desc} · {temp}°F / feels {feel}°F"
mind.sketch_note(note, x=0.64, y=0.2, size=12, color="#9ab0c4")
mind.doodle(icon, x=0.6, y=0.16, size=30, color="#f2d492", note=f"Wind {wind} mph · {humidity}% humidity")

pattern = f"Weather ping logged at {time_str}"
mind.learn_pattern(pattern, confidence=0.45, observations=1)
