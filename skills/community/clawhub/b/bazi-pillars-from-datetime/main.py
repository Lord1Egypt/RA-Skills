#!/usr/bin/env python3
import json
import math
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone, date

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


TG = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DZ = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

YANG_STEMS = {"甲", "丙", "戊", "庚", "壬"}

TERM_LONGITUDE = {
    "春分": 0,
    "清明": 15,
    "谷雨": 30,
    "立夏": 45,
    "小满": 60,
    "芒种": 75,
    "夏至": 90,
    "小暑": 105,
    "大暑": 120,
    "立秋": 135,
    "处暑": 150,
    "白露": 165,
    "秋分": 180,
    "寒露": 195,
    "霜降": 210,
    "立冬": 225,
    "小雪": 240,
    "大雪": 255,
    "冬至": 270,
    "小寒": 285,
    "大寒": 300,
    "立春": 315,
    "雨水": 330,
    "惊蛰": 345,
}

TERM_APPROX_DATE = {
    "小寒": (1, 5),
    "大寒": (1, 20),
    "立春": (2, 4),
    "雨水": (2, 19),
    "惊蛰": (3, 6),
    "春分": (3, 20),
    "清明": (4, 4),
    "谷雨": (4, 20),
    "立夏": (5, 5),
    "小满": (5, 21),
    "芒种": (6, 5),
    "夏至": (6, 21),
    "小暑": (7, 7),
    "大暑": (7, 23),
    "立秋": (8, 7),
    "处暑": (8, 23),
    "白露": (9, 7),
    "秋分": (9, 23),
    "寒露": (10, 8),
    "霜降": (10, 23),
    "立冬": (11, 7),
    "小雪": (11, 22),
    "大雪": (12, 7),
    "冬至": (12, 21),
}

JIE_TERMS = [
    "立春",
    "惊蛰",
    "清明",
    "立夏",
    "芒种",
    "小暑",
    "立秋",
    "白露",
    "寒露",
    "立冬",
    "大雪",
    "小寒",
]

JIE_TO_BRANCH = {
    "立春": "寅",
    "惊蛰": "卯",
    "清明": "辰",
    "立夏": "巳",
    "芒种": "午",
    "小暑": "未",
    "立秋": "申",
    "白露": "酉",
    "寒露": "戌",
    "立冬": "亥",
    "大雪": "子",
    "小寒": "丑",
}

MONTH_BRANCHES = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]

MONTH_STEM_START = {
    "甲": "丙",
    "己": "丙",
    "乙": "戊",
    "庚": "戊",
    "丙": "庚",
    "辛": "庚",
    "丁": "壬",
    "壬": "壬",
    "戊": "甲",
    "癸": "甲",
}

DEFAULT_CITY_MAP_PATH = os.environ.get(
    "BAZI_CITY_MAP_PATH", os.path.join(os.path.dirname(__file__), "cities.json")
)
DEFAULT_CACHE_PATH = os.environ.get(
    "BAZI_CITY_CACHE_PATH", os.path.join(os.path.dirname(__file__), "city_cache.json")
)
DEFAULT_LOOKUP_PROVIDER = os.environ.get("BAZI_GEOCODE_PROVIDER", "nominatim")
DEFAULT_LOOKUP_TIMEOUT = float(os.environ.get("BAZI_GEOCODE_TIMEOUT", "6"))
_CITY_INDEX = None


def parse_datetime(value: str) -> datetime:
    value = value.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError("INVALID_DATETIME")


def normalize_city_name(name: str) -> str:
    name = name.strip()
    name = name.replace(" ", "")
    for suffix in ("市", "省", "自治区", "特别行政区"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def load_city_map(path: str) -> dict:
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def build_city_index(data: dict) -> dict:
    index = {}
    for key, value in data.items():
        if isinstance(value, dict):
            lon = value.get("longitude")
            lat = value.get("latitude")
            aliases = value.get("aliases") or []
        elif isinstance(value, (list, tuple)) and len(value) >= 2:
            lon, lat = value[0], value[1]
            aliases = []
        else:
            continue
        if lon is None or lat is None:
            continue
        try:
            lon = float(lon)
            lat = float(lat)
        except Exception:
            continue
        names = [key] + list(aliases)
        for n in names:
            norm = normalize_city_name(str(n))
            if norm:
                index[norm] = (lon, lat, key)
    return index


def load_cache(path: str) -> dict:
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def save_cache(path: str, cache: dict) -> None:
    if not path:
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        return


def geocode_nominatim(name: str, timeout: float):
    query = urllib.parse.quote(name)
    url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={query}"
    headers = {"User-Agent": "opencode-bazi/1.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not data:
        return None
    item = data[0]
    return float(item["lon"]), float(item["lat"])


def geocode_amap(name: str, key: str, timeout: float):
    if not key:
        return None
    query = urllib.parse.quote(name)
    url = f"https://restapi.amap.com/v3/geocode/geo?address={query}&key={key}"
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    geocodes = data.get("geocodes") or []
    if not geocodes:
        return None
    loc = geocodes[0].get("location")
    if not loc or "," not in loc:
        return None
    lon, lat = loc.split(",", 1)
    return float(lon), float(lat)


def geocode_tencent(name: str, key: str, timeout: float):
    if not key:
        return None
    query = urllib.parse.quote(name)
    url = f"https://apis.map.qq.com/ws/geocoder/v1/?address={query}&key={key}"
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("status") != 0:
        return None
    loc = data.get("result", {}).get("location")
    if not loc:
        return None
    return float(loc["lng"]), float(loc["lat"])


def geocode_online(name: str, provider: str, key: str, timeout: float):
    provider = (provider or "nominatim").lower()
    if provider == "amap":
        return geocode_amap(name, key, timeout)
    if provider == "tencent":
        return geocode_tencent(name, key, timeout)
    return geocode_nominatim(name, timeout)


def get_location(location: dict):
    if not location:
        return None
    lon = location.get("longitude")
    lat = location.get("latitude")
    if lon is not None and lat is not None:
        return float(lon), float(lat), location.get("name")

    name = location.get("name")
    if not name:
        return None

    lookup_mode = (location.get("lookup_mode") or "auto").lower()
    lookup_path = location.get("lookup_path") or DEFAULT_CITY_MAP_PATH
    cache_path = location.get("cache_path") or DEFAULT_CACHE_PATH
    provider = location.get("lookup_provider") or DEFAULT_LOOKUP_PROVIDER
    key = location.get("lookup_key") or os.environ.get("BAZI_GEOCODE_KEY", "")
    timeout = location.get("lookup_timeout", DEFAULT_LOOKUP_TIMEOUT)
    try:
        timeout = float(timeout)
    except Exception:
        timeout = DEFAULT_LOOKUP_TIMEOUT

    norm = normalize_city_name(name)

    global _CITY_INDEX
    if _CITY_INDEX is None or lookup_path != DEFAULT_CITY_MAP_PATH:
        _CITY_INDEX = build_city_index(load_city_map(lookup_path))

    if lookup_mode in ("local", "auto"):
        if norm in _CITY_INDEX:
            lon, lat, canonical = _CITY_INDEX[norm]
            return lon, lat, canonical

    cache = load_cache(cache_path)
    if norm in cache:
        try:
            lon, lat = cache[norm]["longitude"], cache[norm]["latitude"]
            return float(lon), float(lat), cache[norm].get("name", norm)
        except Exception:
            pass

    if lookup_mode in ("online", "auto"):
        try:
            coords = geocode_online(name, provider, key, timeout)
        except Exception:
            coords = None
        if coords:
            lon, lat = coords
            cache[norm] = {"longitude": lon, "latitude": lat, "name": name}
            save_cache(cache_path, cache)
            return lon, lat, name

    return None


def equation_of_time_minutes(d: date) -> float:
    n = d.timetuple().tm_yday
    b = math.radians(360 * (n - 81) / 364)
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def julian_day(dt_utc: datetime) -> float:
    y, m = dt_utc.year, dt_utc.month
    d = dt_utc.day
    hour = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600 + dt_utc.microsecond / 3_600_000_000
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5
    jd += hour / 24
    return jd


def sun_apparent_longitude(dt_utc: datetime) -> float:
    jd = julian_day(dt_utc)
    t = (jd - 2451545.0) / 36525.0
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t
    c = (
        (1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(math.radians(m))
        + (0.019993 - 0.000101 * t) * math.sin(math.radians(2 * m))
        + 0.000289 * math.sin(math.radians(3 * m))
    )
    true_long = l0 + c
    omega = 125.04 - 1934.136 * t
    lambd = true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    return (lambd % 360 + 360) % 360


def angle_diff(lon: float, target: float) -> float:
    return (lon - target + 180) % 360 - 180


def find_term_datetime(year: int, term_name: str, tz: ZoneInfo) -> datetime:
    target = TERM_LONGITUDE[term_name]
    month, day = TERM_APPROX_DATE[term_name]
    guess = datetime(year, month, day, 12, 0, 0, tzinfo=tz)
    start = guess - timedelta(days=3)
    end = guess + timedelta(days=3)

    def f(dt_local: datetime) -> float:
        dt_utc = dt_local.astimezone(timezone.utc)
        return angle_diff(sun_apparent_longitude(dt_utc), target)

    f_start = f(start)
    f_end = f(end)
    if f_start == 0:
        return start
    if f_start * f_end > 0:
        start = guess - timedelta(days=6)
        end = guess + timedelta(days=6)
        f_start = f(start)
        f_end = f(end)
        if f_start * f_end > 0:
            return guess

    for _ in range(60):
        mid = start + (end - start) / 2
        f_mid = f(mid)
        if f_start * f_mid <= 0:
            end = mid
            f_end = f_mid
        else:
            start = mid
            f_start = f_mid
    return end


def get_solar_terms(year: int, tz: ZoneInfo) -> dict:
    terms = {}
    for name in TERM_LONGITUDE.keys():
        terms[name] = find_term_datetime(year, name, tz)
    return terms


def get_prev_next_terms(dt_local: datetime, tz: ZoneInfo):
    term_list = []
    for y in (dt_local.year - 1, dt_local.year, dt_local.year + 1):
        terms = get_solar_terms(y, tz)
        for name, tdt in terms.items():
            term_list.append((tdt, name))
    term_list.sort(key=lambda x: x[0])
    prev_term = None
    next_term = None
    for tdt, name in term_list:
        if tdt <= dt_local:
            prev_term = (name, tdt)
        elif tdt > dt_local and next_term is None:
            next_term = (name, tdt)
            break
    return prev_term, next_term


def year_pillar(dt_local: datetime, tz: ZoneInfo):
    terms = get_solar_terms(dt_local.year, tz)
    lichun = terms["立春"]
    year = dt_local.year if dt_local >= lichun else dt_local.year - 1
    idx = (year - 1984) % 60
    tg = TG[idx % 10]
    dz = DZ[idx % 12]
    return year, tg, dz


def month_pillar(dt_local: datetime, year_tg: str, tz: ZoneInfo):
    term_list = []
    for y in (dt_local.year - 1, dt_local.year):
        terms = get_solar_terms(y, tz)
        for name in JIE_TERMS:
            term_list.append((terms[name], name))
    term_list.sort(key=lambda x: x[0])
    prev_term = term_list[0]
    for tdt, name in term_list:
        if tdt <= dt_local:
            prev_term = (tdt, name)
        else:
            break
    branch = JIE_TO_BRANCH[prev_term[1]]
    month_index = MONTH_BRANCHES.index(branch)
    start_stem = MONTH_STEM_START[year_tg]
    stem_index = (TG.index(start_stem) + month_index) % 10
    return TG[stem_index], branch


BASE_DAY = date(1984, 2, 2)  # 丙寅日
BASE_DAY_INDEX = 2  # 丙寅在六十甲子中的序号（甲子=0）


def day_pillar(day_date: date):
    diff = (day_date - BASE_DAY).days
    idx = (diff + BASE_DAY_INDEX) % 60
    tg = TG[idx % 10]
    dz = DZ[idx % 12]
    return tg, dz


def hour_branch(dt_local: datetime) -> int:
    h = dt_local.hour
    if h == 23:
        return 0
    return ((h + 1) // 2) % 12


def hour_pillar(day_tg: str, dt_local: datetime):
    branch_index = hour_branch(dt_local)
    # 子时起干
    day_tg_index = TG.index(day_tg)
    if day_tg_index in (0, 5):
        start = 0
    elif day_tg_index in (1, 6):
        start = 2
    elif day_tg_index in (2, 7):
        start = 4
    elif day_tg_index in (3, 8):
        start = 6
    else:
        start = 8
    tg = TG[(start + branch_index) % 10]
    dz = DZ[branch_index]
    return tg, dz


def add_months(dt: datetime, months: int) -> datetime:
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return dt.replace(year=year, month=month, day=day)


def add_years(dt: datetime, years: int) -> datetime:
    try:
        return dt.replace(year=dt.year + years)
    except ValueError:
        return dt.replace(month=2, day=28, year=dt.year + years)


def compute_dayun(dt_local: datetime, year_tg: str, month_tg: str, month_dz: str, gender: str, tz: ZoneInfo):
    if gender is None:
        return None, "missing_gender"
    gender = gender.lower()
    if gender not in ("male", "female"):
        return None, "invalid_gender"
    forward = (year_tg in YANG_STEMS and gender == "male") or (year_tg not in YANG_STEMS and gender == "female")

    # find next/prev jie term
    terms = []
    for y in (dt_local.year - 1, dt_local.year, dt_local.year + 1):
        term_times = get_solar_terms(y, tz)
        for name in JIE_TERMS:
            terms.append((term_times[name], name))
    terms.sort(key=lambda x: x[0])
    if forward:
        target = next((t for t in terms if t[0] >= dt_local), None)
        if not target:
            target = terms[-1]
        diff = target[0] - dt_local
        direction = "forward"
    else:
        prev = [t for t in terms if t[0] <= dt_local]
        target = prev[-1] if prev else terms[0]
        diff = dt_local - target[0]
        direction = "backward"

    diff_days = diff.total_seconds() / 86400
    start_age_years = diff_days / 3.0
    start_age_months = diff_days * 4.0
    start_datetime = add_months(dt_local, int(round(start_age_months)))

    month_tg_index = TG.index(month_tg)
    month_dz_index = DZ.index(month_dz)
    step = 1 if forward else -1

    cycles = []
    for i in range(1, 9):
        tg = TG[(month_tg_index + step * i) % 10]
        dz = DZ[(month_dz_index + step * i) % 12]
        cycle_start = add_years(start_datetime, (i - 1) * 10)
        cycle_end = add_years(start_datetime, i * 10)
        cycles.append(
            {
                "index": i,
                "tg": tg,
                "dz": dz,
                "gz": tg + dz,
                "start_age_years": round(start_age_years + (i - 1) * 10, 3),
                "start_datetime": cycle_start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end_datetime": cycle_end.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )

    return {
        "direction": direction,
        "start_age_years": round(start_age_years, 3),
        "start_age_months": round(start_age_months, 3),
        "start_datetime": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "cycles": cycles,
    }, None


def compute_flows(flow_dt: datetime, tz: ZoneInfo):
    year, ytg, ydz = year_pillar(flow_dt, tz)
    mtg, mdz = month_pillar(flow_dt, ytg, tz)
    dt_date = flow_dt.date()
    dtg, ddz = day_pillar(dt_date)
    return {
        "datetime": flow_dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "year": {"tg": ytg, "dz": ydz, "gz": ytg + ydz},
        "month": {"tg": mtg, "dz": mdz, "gz": mtg + mdz},
        "day": {"tg": dtg, "dz": ddz, "gz": dtg + ddz},
    }


def calculate_payload(payload: dict) -> dict:
    datetime_str = payload.get("datetime")
    timezone_str = payload.get("timezone")
    if not datetime_str:
        return {"ok": False, "error": {"code": "MISSING_DATE", "missing": ["date"], "message": "Missing datetime"}}
    if not timezone_str:
        return {"ok": False, "error": {"code": "MISSING_TIMEZONE", "missing": ["timezone"], "message": "Missing timezone"}}

    if ZoneInfo is None:
        return {"ok": False, "error": {"code": "INVALID_TIMEZONE", "missing": ["timezone"], "message": "ZoneInfo unavailable"}}

    try:
        local_dt = parse_datetime(datetime_str)
    except ValueError:
        return {"ok": False, "error": {"code": "INVALID_DATETIME", "missing": ["date"], "message": "Invalid datetime"}}

    try:
        tz = ZoneInfo(timezone_str)
    except Exception:
        return {"ok": False, "error": {"code": "INVALID_TIMEZONE", "missing": ["timezone"], "message": "Invalid timezone"}}

    local_dt = local_dt.replace(tzinfo=tz)

    rules = payload.get("rules") or {}
    day_boundary = rules.get("day_boundary", "00:00")
    time_correction = rules.get("time_correction", "mean_solar_time")
    require_dayun = bool(rules.get("require_dayun", False))

    location = payload.get("location")
    location_info = None
    if time_correction in ("true_solar_time", "mean_solar_time"):
        loc = get_location(location)
        if not loc:
            return {"ok": False, "error": {"code": "MISSING_LOCATION", "missing": ["location"], "message": "Missing or invalid location"}}
        location_info = loc
        lon, lat, loc_name = loc
        tz_offset = local_dt.utcoffset().total_seconds() / 3600
        std_meridian = tz_offset * 15
        eot = equation_of_time_minutes(local_dt.date()) if time_correction == "true_solar_time" else 0.0
        lon_correction = 4 * (lon - std_meridian)
        delta_minutes = eot + lon_correction
        true_dt = local_dt + timedelta(minutes=delta_minutes)
    else:
        true_dt = local_dt
        eot = 0.0
        lon_correction = 0.0
        delta_minutes = 0.0

    day_date = true_dt.date()
    if day_boundary == "23:00" and true_dt.hour == 23:
        day_date = (true_dt + timedelta(days=1)).date()

    year_num, year_tg, year_dz = year_pillar(local_dt, tz)
    month_tg, month_dz = month_pillar(local_dt, year_tg, tz)
    day_tg, day_dz = day_pillar(day_date)
    hour_tg, hour_dz = hour_pillar(day_tg, true_dt)

    gender = payload.get("gender")
    dayun = None
    dayun_note = None
    if gender or require_dayun:
        dayun, dayun_note = compute_dayun(local_dt, year_tg, month_tg, month_dz, gender, tz)
        if dayun is None and require_dayun:
            return {"ok": False, "error": {"code": "MISSING_GENDER", "missing": ["gender"], "message": "Missing gender for dayun"}}

    flows = None
    flows_input = payload.get("flows")
    if flows_input and flows_input.get("datetime"):
        flow_tz = tz
        if flows_input.get("timezone"):
            try:
                flow_tz = ZoneInfo(flows_input["timezone"])
            except Exception:
                return {"ok": False, "error": {"code": "INVALID_TIMEZONE", "missing": ["timezone"], "message": "Invalid flow timezone"}}
        flow_dt = parse_datetime(flows_input["datetime"]).replace(tzinfo=flow_tz)
        flows = compute_flows(flow_dt, flow_tz)

    prev_term, next_term = get_prev_next_terms(local_dt, tz)
    notes = []
    if dayun_note == "missing_gender":
        notes.append("dayun_skipped_missing_gender")
    if location_info is None and time_correction in ("true_solar_time", "mean_solar_time"):
        notes.append("location_missing")

    return {
        "ok": True,
        "bazi": {
            "year": {"tg": year_tg, "dz": year_dz},
            "month": {"tg": month_tg, "dz": month_dz},
            "day": {"tg": day_tg, "dz": day_dz},
            "hour": {"tg": hour_tg, "dz": hour_dz},
        },
        "dayun": dayun,
        "flows": flows,
        "solar_terms": {
            "prev": {"name": prev_term[0], "datetime": prev_term[1].strftime("%Y-%m-%dT%H:%M:%S")} if prev_term else None,
            "next": {"name": next_term[0], "datetime": next_term[1].strftime("%Y-%m-%dT%H:%M:%S")} if next_term else None,
        },
        "meta": {
            "timezone": timezone_str,
            "rules_used": {
                "year_boundary": rules.get("year_boundary", "lichun"),
                "month_rule": rules.get("month_rule", "solar_terms"),
                "day_boundary": day_boundary,
                "time_correction": time_correction,
                "require_dayun": require_dayun,
            },
            "true_solar_time": {
                "method": time_correction,
                "datetime": true_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "delta_minutes": round(delta_minutes, 3),
                "equation_of_time_minutes": round(eot, 3),
                "longitude_correction_minutes": round(lon_correction, 3),
            },
            "location": {
                "name": location_info[2] if location_info else None,
                "longitude": location_info[0] if location_info else None,
                "latitude": location_info[1] if location_info else None,
            },
            "confidence": "high",
            "notes": notes,
        },
    }


def calculate_bazi(*args, **kwargs):
    if "datetime" in kwargs:
        datetime_str = kwargs.get("datetime")
        timezone_str = kwargs.get("timezone") or "Asia/Shanghai"
        payload = {
            "datetime": datetime_str,
            "timezone": timezone_str,
            "location": kwargs.get("location"),
            "gender": kwargs.get("gender"),
            "rules": kwargs.get("rules"),
            "flows": kwargs.get("flows"),
        }
        return calculate_payload(payload)

    if len(args) >= 6:
        year, month, day, hour, minute, timezone_str = args[:6]
        datetime_str = f"{int(year):04d}-{int(month):02d}-{int(day):02d}T{int(hour):02d}:{int(minute):02d}:00"
        payload = {
            "datetime": datetime_str,
            "timezone": timezone_str,
            "location": kwargs.get("location"),
            "gender": kwargs.get("gender"),
            "rules": kwargs.get("rules"),
            "flows": kwargs.get("flows"),
        }
        return calculate_payload(payload)

    raise ValueError("calculate_bazi expects datetime/timezone or year,month,day,hour,minute,timezone")


def main():
    payload = json.load(sys.stdin)
    result = calculate_payload(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
