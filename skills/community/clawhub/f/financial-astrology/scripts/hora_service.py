"""
Hora Service — Tính giờ Hora theo vị trí địa lý.

Hora chia 24h thành các giờ do 7 hành tinh cai quản:
Thứ tự: Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon (lặp lại)

Mỗi ngày có hora đầu tiên (lúc sunrise) do hành tinh của ngày đó cai quản:
- Sunday: Sun, Monday: Moon, Tuesday: Mars, Wednesday: Mercury,
  Thursday: Jupiter, Friday: Venus, Saturday: Saturn
"""

import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import swisseph as swe

logger = logging.getLogger(__name__)

HORA_SEQUENCE = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

DAY_LORDS = {
    6: "Sun",       # Sunday
    0: "Moon",      # Monday
    1: "Mars",      # Tuesday
    2: "Mercury",   # Wednesday
    3: "Jupiter",   # Thursday
    4: "Venus",     # Friday
    5: "Saturn",    # Saturday
}

HORA_MEANINGS = {
    "Sun": {
        "trading": "Authority, government, gold",
        "strategy": "Good for gold, government bonds, stable trades",
        "element": "Fire",
    },
    "Moon": {
        "trading": "Emotions, public sentiment, liquids",
        "strategy": "Watch sentiment shifts, silver, consumer goods",
        "element": "Water",
    },
    "Mars": {
        "trading": "Energy, aggression, metals, real estate",
        "strategy": "Volatile moves, momentum trading, energy stocks",
        "element": "Fire",
    },
    "Mercury": {
        "trading": "Communication, tech, data, short-term",
        "strategy": "Scalping, IT stocks, quick in-out",
        "element": "Earth",
    },
    "Jupiter": {
        "trading": "Expansion, banking, wisdom, growth",
        "strategy": "Banking stocks, position trading, bullish bias",
        "element": "Ether",
    },
    "Venus": {
        "trading": "Luxury, arts, relationships, comfort",
        "strategy": "Consumer goods, luxury stocks, trend following",
        "element": "Earth",
    },
    "Saturn": {
        "trading": "Discipline, restriction, delay, structure",
        "strategy": "Defensive positioning, infrastructure, cautious",
        "element": "Air",
    },
}


def _jd_to_local(jd: float, tz) -> datetime:
    """Convert Julian Day to timezone-aware datetime."""
    y, m, d, h_frac = swe.revjul(jd, swe.GREG_CAL)
    h = int(h_frac)
    m_rem = (h_frac - h) * 60
    mi = int(m_rem)
    s = int((m_rem - mi) * 60)
    dt_utc = datetime(int(y), int(m), int(d), h, mi, s, tzinfo=timezone.utc)
    return dt_utc.astimezone(tz)


def _calc_sun_events(jd_midnight: float, lat: float, lon: float) -> dict:
    """
    Calculate sunrise and sunset for the given day.
    jd_midnight: JD at local midnight of the day.
    Returns dict with sunrise, sunset JDs.
    """
    geopos = (lon, lat, 0.0)
    
    result = {}
    
    # Sunrise
    res, tret = swe.rise_trans(jd_midnight, swe.SUN, swe.CALC_RISE, geopos)
    result["sunrise"] = tret[0]
    
    # Sunset
    res, tret = swe.rise_trans(jd_midnight, swe.SUN, swe.CALC_SET, geopos)
    result["sunset"] = tret[0]
    
    return result


def calculate_hora(dt: datetime, lat: float, lon: float) -> dict:
    """
    Tính giờ Hora hiện tại cho vị trí địa lý.
    
    Input: timezone-aware datetime
    """
    tz = dt.tzinfo
    tz_name = dt.tzname() or "Local"
    
    # Current time in UTC as JD
    dt_utc = dt.astimezone(timezone.utc)
    jd_now = swe.julday(
        dt_utc.year, dt_utc.month, dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
        cal=swe.GREG_CAL
    )
    
    # Local midnight (start of today) as JD
    # Convert local date to UTC midnight
    local_midnight = datetime(dt.year, dt.month, dt.day, tzinfo=tz)
    local_midnight_utc = local_midnight.astimezone(timezone.utc)
    jd_midnight = swe.julday(
        local_midnight_utc.year, local_midnight_utc.month, local_midnight_utc.day,
        local_midnight_utc.hour + local_midnight_utc.minute / 60.0 + local_midnight_utc.second / 3600.0,
        cal=swe.GREG_CAL
    )
    
    # Sunrise/sunset for today
    sun_events = _calc_sun_events(jd_midnight, lat, lon)
    sunrise_jd = sun_events["sunrise"]
    sunset_jd = sun_events["sunset"]
    
    # Tomorrow's sunrise
    jd_tomorrow_midnight = jd_midnight + 1.0
    tomorrow_events = _calc_sun_events(jd_tomorrow_midnight, lat, lon)
    next_sunrise_jd = tomorrow_events["sunrise"]
    
    # Day of week (Python: Mon=0..Sun=6) → day lord
    # VEDIC FIX: Day starts at sunrise, not midnight.
    # If before sunrise, use previous day's lord.
    if jd_now < sunrise_jd:
        # Before sunrise → still yesterday's Vedic day
        yesterday = dt.replace(day=dt.day) - __import__('datetime').timedelta(days=1)
        day_of_week_idx = yesterday.weekday()
    else:
        day_of_week_idx = dt.weekday()
    first_hora_lord = DAY_LORDS.get(day_of_week_idx, "Sun")
    
    # Build hora sequence starting from day lord
    start_idx = HORA_SEQUENCE.index(first_hora_lord)
    hora_order = HORA_SEQUENCE[start_idx:] + HORA_SEQUENCE[:start_idx]
    
    # Calculate hora lengths
    day_length = sunset_jd - sunrise_jd
    night_length = next_sunrise_jd - sunset_jd
    hora_day_len = day_length / 12.0
    hora_night_len = night_length / 12.0
    
    # Determine current hora
    is_daytime = sunrise_jd <= jd_now <= sunset_jd
    
    if is_daytime:
        elapsed = jd_now - sunrise_jd
        hora_num = min(int(elapsed / hora_day_len), 11)  # 0-11 for daytime
        hora_start = sunrise_jd + hora_num * hora_day_len
        hora_end = hora_start + hora_day_len
        hora_idx = hora_num  # 0-11
    else:
        if jd_now > sunset_jd:
            # Night after sunset
            elapsed = jd_now - sunset_jd
            hora_num_night = min(int(elapsed / hora_night_len), 11)  # 0-11
            hora_start = sunset_jd + hora_num_night * hora_night_len
            hora_end = hora_start + hora_night_len
            hora_idx = 12 + hora_num_night  # 12-23
        else:
            # Before sunrise (night before today)
            # Need yesterday's sunset
            yesterday_midnight = jd_midnight - 1.0
            yest_events = _calc_sun_events(yesterday_midnight, lat, lon)
            yest_sunset = yest_events["sunset"]
            
            elapsed = jd_now - yest_sunset
            hora_num_night = min(int(elapsed / hora_night_len), 11)
            hora_start = yest_sunset + hora_num_night * hora_night_len
            hora_end = hora_start + hora_night_len
            hora_idx = 12 + hora_num_night
    
    # Current hora lord
    current_lord = hora_order[hora_idx % 7]
    meaning = HORA_MEANINGS.get(current_lord, {})
    
    # Build full 24-hora sequence
    full_sequence = []
    for i in range(24):
        lord = hora_order[i % 7]
        period = "day" if i < 12 else "night"
        
        if i < 12:
            h_start = _jd_to_local(sunrise_jd + i * hora_day_len, tz)
            h_end = _jd_to_local(sunrise_jd + (i + 1) * hora_day_len, tz)
        else:
            ni = i - 12
            h_start = _jd_to_local(sunset_jd + ni * hora_night_len, tz)
            h_end = _jd_to_local(sunset_jd + (ni + 1) * hora_night_len, tz)
        
        full_sequence.append({
            "hour_num": i + 1,
            "lord": lord,
            "period": period,
            "start": h_start.strftime("%H:%M"),
            "end": h_end.strftime("%H:%M"),
            "trading": HORA_MEANINGS.get(lord, {}).get("trading", ""),
            "strategy": HORA_MEANINGS.get(lord, {}).get("strategy", ""),
        })
    
    return {
        "timestamp": dt.isoformat(),
        "timezone": tz_name,
        "sunrise": _jd_to_local(sunrise_jd, tz).strftime("%H:%M:%S"),
        "sunset": _jd_to_local(sunset_jd, tz).strftime("%H:%M:%S"),
        "next_sunrise": _jd_to_local(next_sunrise_jd, tz).strftime("%H:%M:%S"),
        "day_length_hours": round(day_length * 24, 2),
        "night_length_hours": round(night_length * 24, 2),
        "is_daytime": is_daytime,
        "current_hora": {
            "lord": current_lord,
            "start": _jd_to_local(hora_start, tz).strftime("%H:%M:%S"),
            "end": _jd_to_local(hora_end, tz).strftime("%H:%M:%S"),
            "hour_num": hora_idx + 1,
            "trading": meaning.get("trading", ""),
            "strategy": meaning.get("strategy", ""),
            "element": meaning.get("element", ""),
        },
        "first_hora_lord": first_hora_lord,
        "day_of_week": dt.strftime("%A"),
        "full_sequence": full_sequence,
    }


def get_current_hora(lat: float = 34.9333, lon: float = 136.9667, tz_name: str = "Asia/Tokyo") -> dict:
    """Get current hora for Hekinan, Japan."""
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    logger.info(f"Calculating hora for {now.isoformat()}")
    return calculate_hora(now, lat, lon)
