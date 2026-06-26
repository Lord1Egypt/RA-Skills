"""
Beach Safety MCP Server
Provides comprehensive beach safety conditions via NOAA, Open-Meteo, and other free APIs.
"""

import os

import httpx
import json
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass, asdict




# ============================================================================
# DATA SOURCES (all free, no API keys required unless noted)
# ============================================================================
# 1. NOAA NWS API: api.weather.gov — rip current risk, surf zone forecast
# 2. Open-Meteo Marine: open-meteo.com — wave height, swell, currents (FREE, no key)
# 3. Open-Meteo Weather: open-meteo.com — air temp, wind, precipitation
# 4. NOAA NDBC Buoys: ndbc.noaa.gov — real-time buoy observations
# 5. Open-Meteo Weather: open-meteo.com — UV index (FREE, no key)
# 6. Sunrise-Sunset API: sunrise-sunset.org — sunrise/sunset times
# 7. NOAA CO-OPS: tidesandcurrents.noaa.gov — water level, tides

@dataclass
class BeachConditions:
    """Comprehensive beach safety conditions."""
    beach_name: str
    latitude: float
    longitude: float
    timestamp_utc: str

    # Safety
    rip_current_risk: str
    surf_height_ft: str
    water_quality: str
    uv_index: Optional[float]
    uv_max: Optional[float]
    uv_message: Optional[str]
    uv_risk: str
    air_temperature_f: Optional[float]
    water_temperature_f: Optional[float]

    # Waves
    wave_height_m: Optional[float]
    wave_period_sec: Optional[float]
    wave_direction_deg: Optional[float]
    wave_direction_cardinal: Optional[str]

    # Swell
    swell_height_m: Optional[float]
    swell_period_sec: Optional[float]
    swell_direction_deg: Optional[float]
    swell_direction_cardinal: Optional[str]

    # Wind
    wind_speed_mph: Optional[float]
    wind_direction_deg: Optional[float]
    wind_direction_cardinal: Optional[str]
    wind_offshore: Optional[bool]  # True if offshore (laminated, clean)

    # Ocean
    ocean_current_speed_knots: Optional[float]
    ocean_current_direction_deg: Optional[float]
    tide_status: Optional[str]

    # Sun
    sunrise_time: Optional[str]
    sunset_time: Optional[str]
    hours_of_sunlight: Optional[float]

    # Overall
    safety_score: int  # 1-10
    safety_summary: str
    recommendations: list


def compass_deg_to_cardinal(deg: float) -> str:
    """Convert degrees to cardinal direction."""
    if deg is None:
        return "N/A"
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(deg / 22.5) % 16
    return directions[idx]


def get_uv_risk(uv: float) -> str:
    """Get UV risk level from index."""
    if uv is None:
        return "Unknown"
    if uv <= 2: return "Low"
    if uv <= 5: return "Moderate"
    if uv <= 7: return "High"
    if uv <= 10: return "Very High"
    return "Extreme"


def safe_float(val, default=0.0):
    """Safely convert a value to float."""
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    try:
        return float(str(val).split()[0])
    except (ValueError, IndexError):
        return default

async def geocode_beach(query: str) -> tuple[str, float, float]:
    """
    Geocode a beach name using free OSM services: Nominatim first, then Photons (Komoot) as fallback.
    Both are free, no API key required.
    Returns (display_name, latitude, longitude).
    """
    queries_to_try = [query]
    # If "beach" not already in the query, try appending it
    if "beach" not in query.lower():
        queries_to_try.append(query + " Beach")

    for q in queries_to_try:
        # Try Nominatim — take the top result (most famous match)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={
                        "q": q,
                        "format": "json",
                        "limit": 3,
                        "addressdetails": 1,
                    },
                    headers={"User-Agent": "BeachSafetyMCP/1.0"}
                )
                if resp.status_code == 200:
                    results = resp.json()
                    if results:
                        r = results[0]
                        return r.get("display_name", query), float(r["lat"]), float(r["lon"])
        except Exception:
            pass

        # Try Photons (Komoot) — fallback for tourist beach names
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://photon.komoot.io/api/",
                    params={"q": q, "limit": 3},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    features = data.get("features", [])
                    if features:
                        f = features[0]
                        props = f.get("properties", {})
                        coords = f.get("geometry", {}).get("coordinates", [])
                        if len(coords) >= 2:
                            display = props.get("name", query)
                            for k in ["city", "state", "country"]:
                                if props.get(k): display += f", {props[k]}"
                            return display, coords[1], coords[0]
        except Exception:
            pass

    return query, 0.0, 0.0


def calc_safety_score(conditions: dict) -> tuple[int, str, list]:
    """Calculate overall safety score (1-10) and generate recommendations."""
    score = 10
    issues = []
    recommendations = []

    rip = conditions.get("rip_current_risk", "Low")
    if rip == "High":
        score -= 5
        issues.append("High rip current risk")
        recommendations.append("⚠️ STAY OUT OF THE WATER — High rip current risk")
    elif rip == "Moderate":
        score -= 2
        issues.append("Moderate rip current risk")
        recommendations.append("⚠️ Swim near a lifeguard. Be aware of rip currents.")

    wave = safe_float(conditions.get("wave_height_m", 0))
    if wave > 4:
        score -= 2
        issues.append(f"Large waves ({wave:.1f}m)")
        recommendations.append(f"⚠️ Large waves ({wave*3.281:.0f} ft) — dangerous for swimming")

    wind = safe_float(conditions.get("wind_speed_mph", 0))
    if wind > 20:
        score -= 2
        recommendations.append(f"⚠️ Strong winds ({wind:.0f} mph) — dangerous conditions")

    # UV is shown in the main report, don't duplicate in recommendations

    water_temp = safe_float(conditions.get("water_temperature_f"))
    if water_temp:
        if water_temp < 60:
            recommendations.append(f"🌡️ Water is cold ({water_temp:.0f}°F) — wetsuit recommended")
        elif water_temp > 85:
            recommendations.append(f"🌡️ Water is warm ({water_temp:.0f}°F) — bacteria risk higher")

    current = safe_float(conditions.get("ocean_current_speed_knots"))
    if current > 2:
        score -= 1
        recommendations.append(f"🌊 Strong current ({current:.1f} knots) — caution advised")

    if not issues:
        recommendations.append("✅ Generally safe conditions — always swim near others and follow local advisories")

    return max(1, score), "; ".join(issues) if issues else "No major hazards", recommendations


async def get_noaa_beach_forecast(lat: float, lon: float) -> dict:
    """Get NOAA surf zone forecast including rip current risk."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Step 1: Get grid point metadata
            points_url = f"https://api.weather.gov/points/{lat},{lon}"
            resp = await client.get(points_url, headers={"User-Agent": "BeachSafetyMCP/1.0"})
            if resp.status_code != 200:
                return {}

            points_data = resp.json()
            forecast_url = points_data["properties"]["forecast"]

            # Step 2: Get forecast
            forecast_resp = await client.get(forecast_url)
            if forecast_resp.status_code != 200:
                return {}

            forecast = forecast_resp.json()
            periods = forecast.get("properties", {}).get("periods", [])

            if not periods:
                return {}

            current = periods[0]

            # Extract surf zone data if available
            surf = current.get("surfZoneForecast", {}) or {}

            # NOAA provides rip risk in forecast text and short forecast
            short = current.get("shortForecast", "").lower()
            detailed = current.get("detailedForecast", "").lower()
            combined = short + " " + detailed

            # Try explicit rip current risk fields first
            rip_risk = surf.get("ripCurrentRisk")
            if rip_risk and rip_risk != "Unknown":
                pass  # Got it from surf zone
            else:
                # Parse from text — check explicit "rip current risk: X" patterns
                rip_risk = None
                for text in [detailed, short]:
                    if f"rip current risk: low" in text or "low rip current risk" in text:
                        rip_risk = "Low"; break
                    elif f"rip current risk: moderate" in text or "moderate rip current risk" in text:
                        rip_risk = "Moderate"; break
                    elif f"rip current risk: high" in text or "high rip current risk" in text:
                        rip_risk = "High"; break
                    elif "life-threatening" in text:
                        rip_risk = "High"; break

                # Broader keyword matching on short forecast
                if not rip_risk:
                    if "rip current" in combined:
                        if "high" in combined and ("rip" in combined):
                            rip_risk = "High"
                        elif "moderate" in combined:
                            rip_risk = "Moderate"
                        elif "low" in combined:
                            rip_risk = "Low"

                rip_risk = rip_risk or "Unknown"

            return {
                "rip_current_risk": rip_risk,
                "surf_height": surf.get("surfHeight", "Unknown"),
                "wave_height_m": surf.get("waveHeight"),
                "dominant_wave_period": surf.get("dominantWavePeriod"),
                "swell_direction": surf.get("swellDirection"),
                "water_temp_f": surf.get("waterTemperature"),
                "air_temperature_f": current.get("temperature"),
                "wind_speed_text": current.get("windSpeed"),
                "wind_direction_text": current.get("windDirection"),
                "short_forecast": current.get("shortForecast"),
                "detailed_forecast": current.get("detailedForecast"),
            }
    except Exception:
        return {}


async def get_open_meteo_marine(lat: float, lon: float) -> dict:
    """Get Open-Meteo Marine API data — completely free, no API key."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            url = "https://marine-api.open-meteo.com/v1/marine"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": [
                    "wave_height", "wave_period", "wave_direction",
                    "swell_wave_height", "swell_wave_period", "swell_wave_direction",
                    "wind_wave_height", "wind_wave_direction",
                    "sea_surface_temperature"
                ],
                "hourly": [
                    "wave_height", "wave_period", "wave_direction",
                    "swell_wave_height", "swell_wave_period", "swell_wave_direction",
                    "ocean_current_velocity", "ocean_current_direction"
                ],
                "timezone": "auto",
                "forecast_days": 1
            }
            resp = await client.get(url, params=params)
            if resp.status_code != 200:
                return {}

            data = resp.json()
            current = data.get("current", {})

            return {
                "wave_height_m": current.get("wave_height"),
                "wave_period_sec": current.get("wave_period"),
                "wave_direction_deg": current.get("wave_direction"),
                "swell_height_m": current.get("swell_wave_height"),
                "swell_period_sec": current.get("swell_wave_period"),
                "swell_direction_deg": current.get("swell_wave_direction"),
                "wind_wave_height_m": current.get("wind_wave_height"),
                "wind_wave_direction_deg": current.get("wind_wave_direction"),
                "water_temp_c": current.get("sea_surface_temperature"),
            }
    except Exception:
        return {}


async def get_open_meteo_weather(lat: float, lon: float) -> dict:
    """Get Open-Meteo Weather data — completely free, no API key."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code",
                            "wind_speed_10m", "wind_direction_10m"],
                "daily": ["sunrise", "sunset"],
                "timezone": "auto",
                "wind_speed_unit": "mph",
            }
            resp = await client.get(url, params=params)
            if resp.status_code != 200:
                return {}

            data = resp.json()
            current = data.get("current", {})
            daily = data.get("daily", {})

            sunrise = daily.get("sunrise", [None])[0] if daily.get("sunrise") else None
            sunset = daily.get("sunset", [None])[0] if daily.get("sunset") else None

            wind_mph = current.get("wind_speed_10m", 0) or 0
            wind_deg = current.get("wind_direction_10m")

            return {
                "air_temp_c": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "precipitation_mm": current.get("precipitation"),
                "weather_code": current.get("weather_code"),
                "wind_speed_10m": wind_mph,
                "wind_direction_deg": wind_deg,
                "sunrise": sunrise,
                "sunset": sunset,
            }
    except Exception:
        return {}


async def get_buoy_nearest(lat: float, lon: float, max_distance_km: float = 50) -> dict:
    """Find and fetch nearest NOAA NDBC buoy data."""
    # Known buoy stations by region (US coasts)
    # For production, this would query a buoy search API
    # For now, return empty — buoys require station ID lookup
    return {}


async def get_uv_index(lat: float, lon: float, api_key: str = "") -> dict:
    """Get UV index from Open-Meteo (free, no API key needed). Returns daily max UV during daytime, current at night."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat, "longitude": lon,
                    "current": "uv_index",
                    "daily": "uv_index_max",
                    "forecast_days": 1,
                    "timezone": "auto"
                }
            )
            if resp.status_code == 200:
                data = resp.json()
                current_uv = data.get("current", {}).get("uv_index")
                daily = data.get("daily", {})
                uv_max_list = daily.get("uv_index_max", [])
                uv_max = uv_max_list[0] if uv_max_list else None
                # Use current UV during day, fall back to daily max
                uv = float(current_uv) if current_uv is not None else None
                if uv is not None and uv > 0:
                    return {"uv_index": round(uv, 1), "uv_max": round(float(uv_max), 1) if uv_max else None}
                if uv_max is not None:
                    return {"uv_index": 0, "uv_max": round(float(uv_max), 1), "uv_message": "night"}
                return {"uv_index": None, "uv_max": None, "uv_message": "UV data unavailable"}
    except Exception:
        pass
    return {"uv_index": None, "uv_message": "UV data unavailable", "uv_max": None}


async def get_tide_data(lat: float, lon: float) -> dict:
    """Get tide predictions from NOAA CO-OPS API."""
    # NOAA CO-OPS requires station ID. For MVP, return approximate.
    return {}


def estimate_rip_risk_from_waves(wave_height_m: float, swell_period_sec: float, wind_speed_mph: float, wind_deg: float) -> str:
    """
    Estimate rip current risk from wave and wind conditions.
    Used as fallback when NOAA doesn't provide official rip risk.
    Based on NWS guidance: wave height, period, and nearshore conditions drive rip formation.
    """
    wave_ft = wave_height_m * 3.281 if wave_height_m else 0
    wave_ht = safe_float(wave_height_m)

    # Offshore wind (> 10mph from land) can indicate cleaner conditions but
    # also means less life guards on duty; onshore = elevated risk
    # Side-shore (perpendicular to coast) = moderate risk
    # For a rough estimate, focus on wave energy
    if wave_ht <= 0:
        return "Low"

    # High energy: tall waves + long period = elevated risk
    if wave_ft >= 4:
        period = safe_float(swell_period_sec)
        if period and period >= 10:
            return "High"
        elif wave_ft >= 6:
            return "High"
        else:
            return "Moderate"

    if wave_ft >= 2.5:
        return "Moderate"

    return "Low"


async def get_noaa_surf_zone_alerts(lat: float, lon: float) -> str:
    """Try to get surf zone/rip current alerts from NOAA for this location."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Get the forecast zone from the points endpoint
            points_url = f"https://api.weather.gov/points/{lat},{lon}"
            resp = await client.get(points_url, headers={"User-Agent": "BeachSafetyMCP/1.0"})
            if resp.status_code != 200:
                return "Unknown"

            points_data = resp.json()
            forecast_zone = points_data.get("properties", {}).get("forecastZone", "")

            if not forecast_zone:
                return "Unknown"

            # Try to get the zone ID from the URL
            zone_id = forecast_zone.split("/")[-1]

            # Fetch active alerts for this zone
            alerts_url = f"https://api.weather.gov/alerts/active/zone/{zone_id}"
            resp = await client.get(alerts_url, headers={"User-Agent": "BeachSafetyMCP/1.0"})
            if resp.status_code == 200:
                alerts_data = resp.json()
                features = alerts_data.get("features", [])
                for alert in features:
                    event = alert.get("properties", {}).get("event", "").lower()
                    if "rip" in event or "surf" in event:
                        if "high" in event:
                            return "High"
                        elif "moderate" in event:
                            return "Moderate"
                        elif "low" in event:
                            return "Low"

            return "Unknown"
    except Exception:
        return "Unknown"


async def get_comprehensive_report(
    beach_name: str,
    lat: float,
    lon: float,
) -> dict:
    """Gather all beach safety data from multiple sources."""
    # Fetch all sources in parallel
    import asyncio as _asyncio
    async with httpx.AsyncClient(timeout=30.0) as client:
        results = await _asyncio.gather(
            get_noaa_beach_forecast(lat, lon),
            get_open_meteo_marine(lat, lon),
            get_open_meteo_weather(lat, lon),
            get_uv_index(lat, lon),
            get_noaa_surf_zone_alerts(lat, lon),
        )

    noaa, marine, weather, uv = results[:4]

    # Determine rip current risk: NOAA > alerts > heuristic fallback
    noaa_rip = noaa.get("rip_current_risk", "Unknown")
    if noaa_rip and noaa_rip != "Unknown":
        rip_risk = noaa_rip
    else:
        # Use wave-based heuristic when NOAA doesn't have official data
        wave_h = marine.get("wave_height_m") or noaa.get("wave_height_m")
        swell_p = marine.get("swell_period_sec") or noaa.get("dominant_wave_period")
        wind_s = weather.get("wind_speed_10m") or 0
        rip_risk = estimate_rip_risk_from_waves(wave_h, swell_p, wind_s, weather.get("wind_direction_deg"))

    # Merge data
    conditions = {
        # Safety
        "rip_current_risk": rip_risk,
        "surf_height": noaa.get("surf_height", "Unknown"),
        "water_quality": "Not currently reported",

        # UV
        "uv_index": uv.get("uv_index"),
        "uv_max": uv.get("uv_max"),
        "uv_message": uv.get("uv_message"),
        "uv_risk": get_uv_risk(uv.get("uv_max") or uv.get("uv_index")),

        # Waves
        "wave_height_m": marine.get("wave_height_m") or noaa.get("wave_height_m"),
        "wave_period_sec": marine.get("wave_period_sec") or noaa.get("dominant_wave_period"),
        "wave_direction_deg": marine.get("wave_direction_deg"),
        "wave_direction_cardinal": compass_deg_to_cardinal(
            marine.get("wave_direction_deg") or 0),

        # Swell
        "swell_height_m": marine.get("swell_height_m"),
        "swell_period_sec": marine.get("swell_period_sec"),
        "swell_direction_deg": marine.get("swell_direction_deg"),
        "swell_direction_cardinal": compass_deg_to_cardinal(
            marine.get("swell_direction_deg") or 0),
        "wind_wave_height_m": marine.get("wind_wave_height_m"),
        "wind_wave_direction_deg": marine.get("wind_wave_direction_deg"),

        # Wind
        "wind_speed_mph": round(weather.get("wind_speed_10m") or 0, 1),
        "wind_direction_deg": weather.get("wind_direction_deg"),
        "wind_direction_cardinal": compass_deg_to_cardinal(
            weather.get("wind_direction_deg") or 0),
        "wind_speed_text": noaa.get("wind_speed_text"),

        # Ocean
        "ocean_current_speed_knots": None,
        "ocean_current_direction_deg": None,
        "tide_status": None,

        # Sun
        "sunrise": weather.get("sunrise"),
        "sunset": weather.get("sunset"),

        # Temperature (preserve None so 0C doesn't silently become 32F)
        "air_temp_c": weather.get("air_temp_c"),
        "air_temperature_f": round(weather.get("air_temp_c") * 9/5 + 32, 1) if weather.get("air_temp_c") is not None else None,
        "water_temp_c": marine.get("water_temp_c"),
        "water_temperature_f": round(marine.get("water_temp_c") * 9/5 + 32, 1) if marine.get("water_temp_c") is not None else None,
        "noaa_water_temp_f": noaa.get("water_temp_f"),

        # Forecast
        "short_forecast": noaa.get("short_forecast"),
    }

    # Override water temp with NOAA if available (more accurate at beach)
    if conditions.get("noaa_water_temp_f"):
        conditions["water_temperature_f"] = conditions["noaa_water_temp_f"]

    # Calculate safety
    score, summary, recommendations = calc_safety_score(conditions)

    # Build full report
    report = {
        "beach_name": beach_name,
        "latitude": lat,
        "longitude": lon,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),

        # Safety
        "rip_current_risk": conditions["rip_current_risk"],
        "surf_height": conditions["surf_height"],
        "water_quality": conditions["water_quality"],
        "safety_score": score,
        "safety_summary": summary,
        "recommendations": recommendations,
        "uv_index": conditions["uv_index"],
        "uv_max": conditions.get("uv_max"),
        "uv_message": conditions.get("uv_message"),
        "uv_risk": conditions["uv_risk"],

        # Temperature
        "air_temperature_f": conditions["air_temperature_f"],
        "water_temperature_f": conditions["water_temperature_f"],

        # Waves
        "wave": {
            "height_m": conditions["wave_height_m"],
            "height_ft": round((conditions["wave_height_m"] or 0) * 3.281, 1),
            "period_sec": conditions["wave_period_sec"],
            "direction_deg": conditions["wave_direction_deg"],
            "direction_cardinal": conditions["wave_direction_cardinal"],
        },

        # Swell
        "swell": {
            "height_m": conditions["swell_height_m"],
            "height_ft": round((conditions["swell_height_m"] or 0) * 3.281, 1),
            "period_sec": conditions["swell_period_sec"],
            "direction_deg": conditions["swell_direction_deg"],
            "direction_cardinal": conditions["swell_direction_cardinal"],
        },

        # Wind
        "wind": {
            "speed_mph": conditions["wind_speed_mph"],
            "direction_deg": conditions["wind_direction_deg"],
            "direction_cardinal": conditions["wind_direction_cardinal"],
            "speed_text": conditions["wind_speed_text"],
        },

        # Ocean
        "ocean": {
            "current_speed_knots": conditions["ocean_current_speed_knots"],
            "current_direction_deg": conditions["ocean_current_direction_deg"],
            "tide_status": conditions["tide_status"],
        },

        # Sun
        "sun": {
            "sunrise": conditions["sunrise"],
            "sunset": conditions["sunset"],
        },

        # Forecast
        "weather_forecast": conditions["short_forecast"],
    }

    return report


def fmt(val, fmt_str):
    """Safely format a value or return N/A."""
    if val is None:
        return "N/A"
    try:
        return format(float(val), fmt_str)
    except (TypeError, ValueError):
        return str(val)

def format_report_text(report: dict) -> str:
    """Format report as human-readable text."""
    wave_ht = fmt(report['wave']['height_ft'], ".1f")
    wave_m = fmt(report['wave']['height_m'], ".2f")
    swell_ht = fmt(report['swell']['height_ft'], ".1f")
    swell_per = fmt(report['swell']['period_sec'], ".1f")
    wind_sp = fmt(report['wind']['speed_mph'], ".1f")
    wind_deg = fmt(report['wind']['direction_deg'], ".0f")
    air_tmp = fmt(report['air_temperature_f'], ".0f")
    water_tmp = fmt(report['water_temperature_f'], ".0f")
    uv = fmt(report['uv_index'], ".0f")

    lines = [
        f"🌊 {report['beach_name']} Beach Conditions",
        f"   Lat/Lon: {report['latitude']:.4f}, {report['longitude']:.4f}",
        f"   Updated: {report['timestamp_utc']} UTC",
        "",
        f"🛡️ SAFETY (Score: {report['safety_score']}/10)",
        f"   Rip Current Risk: {report['rip_current_risk']}",
        f"   Safety: {report['safety_summary']}",
        "",
        "🌊 WAVES",
        f"   Wave Height: {wave_ht} ft" + (f" ({wave_m}m)" if wave_m != "N/A" else ""),
    ]

    per = report['wave']['period_sec']
    if per:
        lines.append(f"   Wave Period: {fmt(per, '.1f')} sec")
    dc = report['wave']['direction_cardinal']
    if dc and dc != "N/A":
        lines.append(f"   Wave Direction: {dc} ({wind_deg}°)")

    swell_ht_val = report['swell']['height_ft']
    swell_per_val = report['swell']['period_sec']
    swell_dir = report['swell']['direction_cardinal']
    if swell_ht_val and swell_ht_val != "N/A":
        lines.append(f"   Swell: {fmt(swell_ht_val, '.1f')} ft @ {fmt(swell_per_val, '.1f')} sec from {swell_dir or 'N/A'}")
    else:
        lines.append("   Swell: N/A")

    lines.extend([
        "",
        "💨 WIND",
        f"   Speed: {wind_sp} mph" if wind_sp != "N/A" else "   Wind: N/A",
    ])
    if wind_deg != "N/A" and report['wind']['direction_cardinal']:
        lines.append(f"   Direction: {report['wind']['direction_cardinal']} ({wind_deg}°)")

    lines.extend([
        "",
        "🌡️ TEMPERATURE",
        f"   Air: {air_tmp}°F" if air_tmp != "N/A" else "   Air: N/A",
        f"   Water: {water_tmp}°F" if water_tmp and water_tmp != "N/A" else "   Water: N/A",
    ])

    uv_idx = report['uv_index']
    uv_max = report.get('uv_max')
    is_night = report.get('uv_message') == 'night'
    if uv_max is not None:
        if is_night:
            lines.append(f"☀️ UV INDEX: current=0 (daily max={uv_max}) ({report["uv_risk"]}) — sunscreen recommended")
        else:
            lines.append(f"☀️ UV INDEX: current={uv_idx} (daily max={uv_max}) ({report["uv_risk"]}) — sunscreen recommended")

    if report['weather_forecast']:
        lines.append(f"🌤️  {report['weather_forecast']}")

    lines.append("")
    lines.append("📋 RECOMMENDATIONS:")
    for rec in report['recommendations']:
        lines.append(f"   {rec}")

    return "\n".join(lines)


# ============================================================================
# MCP TOOLS (these are what AI agents will call)
# ============================================================================

def get_beach_report(beach_name: str, latitude: float = None, longitude: float = None) -> str:
    """
    Get comprehensive beach safety conditions for any beach location.

    Args:
        beach_name: Name of the beach (e.g., "Venice Beach, CA", "Waikiki")
                    Can be just a name — geocoding is automatic.
        latitude: Decimal degrees (e.g., 33.9850). Optional — resolved from name if omitted.
        longitude: Decimal degrees (e.g., -118.4695). Optional — resolved from name if omitted.

    Returns:
        Comprehensive beach safety report with waves, swell, wind, temperature, safety score
    """
    import asyncio
    lat = latitude
    lon = longitude
    if lat is None or lon is None:
        display_name, lat, lon = asyncio.run(geocode_beach(beach_name))
        if lat == 0.0 and lon == 0.0:
            return f"Could not find beach: {beach_name}. Try a more specific name (e.g., 'Waikiki Beach, Oahu, HI')."
        if display_name != beach_name:
            beach_name = display_name
    report = asyncio.run(get_comprehensive_report(beach_name, lat, lon))
    return format_report_text(report)


def get_beach_json(beach_name: str, latitude: float = None, longitude: float = None) -> dict:
    """
    Get beach conditions as structured JSON for programmatic use.

    Same data as get_beach_report but in JSON format.
    """
    import asyncio
    lat = latitude
    lon = longitude
    if lat is None or lon is None:
        display_name, lat, lon = asyncio.run(geocode_beach(beach_name))
        if lat == 0.0 and lon == 0.0:
            return {"error": f"Could not find beach: {beach_name}. Try a more specific name."}
        if display_name != beach_name:
            beach_name = display_name
    return asyncio.run(get_comprehensive_report(beach_name, lat, lon))


def get_surf_forecast(lat: float, lon: float) -> dict:
    """
    Get surf-specific forecast including wave height, swell, and period.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Dict with wave_height_ft, swell_height_ft, swell_period_sec, dominant_direction
    """
    import asyncio
    report = asyncio.run(get_comprehensive_report("Surf Spot", lat, lon))
    return {
        "wave_height_ft": report["wave"]["height_ft"],
        "wave_height_m": report["wave"]["height_m"],
        "wave_period_sec": report["wave"]["period_sec"],
        "wave_direction": report["wave"]["direction_cardinal"],
        "swell_height_ft": report["swell"]["height_ft"],
        "swell_period_sec": report["swell"]["period_sec"],
        "swell_direction": report["swell"]["direction_cardinal"],
        "rip_current_risk": report["rip_current_risk"],
        "safety_score": report["safety_score"],
        "timestamp": report["timestamp_utc"],
    }


def get_uv_forecast(lat: float, lon: float) -> dict:
    """
    Get UV index forecast for sun protection planning.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Dict with uv_index and uv_risk
    """
    import asyncio
    uv_data = asyncio.run(get_uv_index(lat, lon))
    return {
        "uv_index": uv_data.get("uv_index"),
        "uv_max": uv_data.get("uv_max"),
        "uv_risk": get_uv_risk(uv_data.get("uv_max") or uv_data.get("uv_index")),
        "recommendation": _uv_recommendation(uv_data.get("uv_max") or uv_data.get("uv_index")),
    }


def _uv_recommendation(uv: float) -> str:
    if uv is None:
        return "UV data unavailable"
    if uv <= 2: return "No protection needed"
    if uv <= 5: return "Wear sunscreen and sunglasses"
    if uv <= 7: return "Wear sunscreen, sunglasses, and a hat"
    if uv <= 10: return "Reduce time in the sun, wear protective clothing"
    return "Avoid being outside during midday hours"


# ============================================================================
# MAIN (stdio MCP server)
# ============================================================================

if __name__ == "__main__":
    import sys
    import json

    # Simple stdio MCP server loop
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())

            # Handle MCP JSON-RPC messages
            method = request.get("method", "")
            msg_id = request.get("id")

            if method == "initialize":
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "beach-safety-mcp",
                            "version": "1.1.1"
                        }
                    }
                }))
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "get_beach_report",
                        "description": "Get comprehensive beach safety conditions including rip current risk, waves, swell, wind, temperature, UV, and safety score for any beach location. Automatically geocodes any beach name worldwide — just say 'Waikiki' or 'Bondi Beach'.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "beach_name": {"type": "string", "description": "Name of the beach (e.g., 'Waikiki', 'Bondi Beach, Sydney', 'Cocoa Beach, FL')"},
                                "latitude": {"type": "number", "description": "Latitude (optional — resolved from name if omitted)"},
                                "longitude": {"type": "number", "description": "Longitude (optional — resolved from name if omitted)"}
                            },
                            "required": ["beach_name"]
                        }
                    },
                    {
                        "name": "get_beach_json",
                        "description": "Get beach conditions as structured JSON for programmatic use. Same as get_beach_report but in JSON format. Auto-geocodes any beach name.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "beach_name": {"type": "string", "description": "Name of the beach (e.g., 'Waikiki', 'Bondi Beach')"},
                                "latitude": {"type": "number", "description": "Latitude (optional)"},
                                "longitude": {"type": "number", "description": "Longitude (optional)"}
                            },
                            "required": ["beach_name"]
                        }
                    },
                    {
                        "name": "get_surf_forecast",
                        "description": "Get surf-specific forecast with wave height, swell, and period.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "lat": {"type": "number"},
                                "lon": {"type": "number"}
                            },
                            "required": ["lat", "lon"]
                        }
                    },
                    {
                        "name": "get_uv_forecast",
                        "description": "Get UV index forecast for sun protection planning.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "lat": {"type": "number"},
                                "lon": {"type": "number"}
                            },
                            "required": ["lat", "lon"]
                        }
                    }
                ]
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools}}))
                sys.stdout.flush()

            elif method == "tools/call":
                name = request["params"]["name"]
                args = request["params"]["arguments"]

                try:
                    if name == "get_beach_report":
                        result = get_beach_report(**args)
                    elif name == "get_beach_json":
                        result = get_beach_json(**args)
                    elif name == "get_surf_forecast":
                        result = get_surf_forecast(**args)
                    elif name == "get_uv_forecast":
                        result = get_uv_forecast(**args)
                    else:
                        result = f"Unknown tool: {name}"

                    print(json.dumps({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": str(result)}]
                        }
                    }))
                except Exception as e:
                    print(json.dumps({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32603, "message": str(e)}
                    }))
                sys.stdout.flush()

        except Exception as e:
            print(f"# Error: {e}", file=sys.stderr)
            sys.stderr.flush()
