#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
import zlib
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"zoneinfo unavailable: {exc}")


DEFAULT_CITY = "Shanghai"
DEFAULT_CITY_ZH = "上海"
DEFAULT_TIMEZONE = "Asia/Shanghai"
DEFAULT_LATITUDE = 31.2304
DEFAULT_LONGITUDE = 121.4737
CHINA_COUNTRY_CODES = {"CN", "HK", "MO", "TW"}
SELECTION_MODES = {"standard", "manual", "alternate"}
SELECTION_STATE_VERSION = 1
MAX_SELECTION_STATE_DAYS = 14
USER_AGENT = "daily-morning-greetings/1.0"
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WISDOM_PAIRS_PATH = SKILL_DIR / "references" / "wisdom_pairs.json"
GREETING_ICONS = ["🌅", "🌤️", "☀️", "🌞"]
ENDING_ICONS = ["🍃", "✨", "🌼", "☕"]

WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
MONTH_HINTS = {
    1: "隆冬未退，出门先顾住暖意，做事宜稳，不宜躁。",
    2: "初春乍暖还寒，白天看着松快，早晚仍要护住一层暖。",
    3: "仲春风起，气色渐开，适合把节奏拉顺，不必一早冲太猛。",
    4: "春深渐暖，白天多半舒展，早晚仍留几分凉意。",
    5: "初夏将近，气温抬头，穿衣宜轻一点，行动宜快一点。",
    6: "梅雨和暑气常常交替，心要定，事要一件件收。",
    7: "盛夏火气旺，白天耗神快，安排上宜留出缓冲。",
    8: "暑气未尽，体感仍热，做事要防赶过头，也要防拖过头。",
    9: "初秋渐入场，白天和晚上开始分出层次，节奏适合收一收。",
    10: "秋意渐深，天高气爽，最适合把杂事理顺，把重点拎清。",
    11: "深秋转凉，早晚明显见冷，先把身体顾稳，再谈效率。",
    12: "岁末寒气重，宜收口、宜复盘、宜把力气用在要紧处。",
}
FALLBACK_WISDOM_PAIRS = [
    {
        "role": "哲学家",
        "name": "塞涅卡",
        "quote": "运气是准备与机会的相遇",
        "blessing": "愿你今天心里有数，手上有准备，机会来时也能接得住。",
    },
    {
        "role": "思想家",
        "name": "老子",
        "quote": "千里之行，始于足下",
        "blessing": "愿你今天不急不赶，把眼前这一步先走稳。",
    },
    {
        "role": "教育家",
        "name": "孔子",
        "quote": "欲速则不达",
        "blessing": "愿你今天节奏从容一点，慢一点，反而更顺。",
    },
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build deterministic morning context for daily-morning-greetings."
    )
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    parser.add_argument(
        "--print-message",
        action="store_true",
        help="Emit formatted.message only, preserving blank lines.",
    )
    parser.add_argument(
        "--variant",
        type=int,
        default=0,
        help="Variant index for alternate rerolls. 0 is the standard daily version.",
    )
    parser.add_argument("--city", help="City label for weather lookup, e.g. Shanghai.")
    parser.add_argument("--city-zh", help="Chinese city label used in rendered output.")
    parser.add_argument("--timezone", help="IANA timezone, e.g. Asia/Shanghai.")
    parser.add_argument("--latitude", type=float, help="Latitude for Open-Meteo fallback.")
    parser.add_argument("--longitude", type=float, help="Longitude for Open-Meteo fallback.")
    parser.add_argument(
        "--selection-mode",
        choices=sorted(SELECTION_MODES),
        default="standard",
        help="Selection mode: stable standard, or manual/alternate rerolls with daily non-repeat state.",
    )
    parser.add_argument(
        "--scope-key",
        help="Stable route key for manual/alternate rerolls, e.g. Feishu chat:<chatId>.",
    )
    return parser.parse_args()


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=10) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset))


def as_int(value):
    try:
        if value in (None, ""):
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def as_float(value):
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def env_or_default(name, default):
    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip()
    return value or default


def env_float(name, default):
    value = os.environ.get(name)
    if value is None:
        return default
    return as_float(value)


def env_int(name, default):
    value = os.environ.get(name)
    if value is None:
        return default
    return as_int(value)


def env_is_set(name):
    value = os.environ.get(name)
    return value is not None and value.strip() != ""


def normalize_location_label(value):
    text = str(value or "").strip()
    return text or None


def normalize_variant(value):
    variant = value if value is not None else 0
    return max(0, int(variant))


def selection_state_path():
    override = os.environ.get("MORNING_GREETING_STATE_PATH")
    if override and override.strip():
        return Path(override.strip()).expanduser()
    return SKILL_DIR / ".state" / "selection_state.json"


def load_selection_state():
    path = selection_state_path()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    days = payload.get("days")
    if not isinstance(days, dict):
        days = {}
    return {
        "version": SELECTION_STATE_VERSION,
        "days": days,
    }


def prune_selection_state(days):
    if len(days) <= MAX_SELECTION_STATE_DAYS:
        return
    for key in sorted(days.keys())[:-MAX_SELECTION_STATE_DAYS]:
        days.pop(key, None)


def save_selection_state(state):
    path = selection_state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    days = state.get("days")
    if isinstance(days, dict):
        prune_selection_state(days)
    temp_path = path.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(temp_path, path)


def normalize_scope_key(value):
    normalized = str(value or "").strip()
    return normalized or "__global__"


def shuffled_indices(base_key, salt, length):
    if length <= 0:
        raise ValueError("shuffle length must be positive")
    ranked = []
    for idx in range(length):
        digest = zlib.crc32(f"{base_key}:{salt}:{idx}".encode("utf-8")) & 0xFFFFFFFF
        ranked.append((digest, idx))
    ranked.sort()
    return [idx for _, idx in ranked]


def reserve_selection_slot(now_local, mode, scope_key):
    if mode == "standard":
        return 0
    state = load_selection_state()
    days = state.setdefault("days", {})
    prune_selection_state(days)
    date_key = now_local.strftime("%Y-%m-%d")
    day_state = days.setdefault(date_key, {})
    scopes = day_state.setdefault("scopes", {})
    normalized_scope = normalize_scope_key(scope_key)
    entry = scopes.setdefault(normalized_scope, {})
    slot = int(entry.get("next_slot") or 0)
    entry["next_slot"] = slot + 1
    entry["last_slot"] = slot
    entry["last_mode"] = mode
    entry["updated_at"] = now_local.isoformat()
    save_selection_state(state)
    return slot


def build_selection_context(now_local, mode, scope_key, variant):
    normalized_mode = str(mode or "standard").strip().lower()
    if normalized_mode not in SELECTION_MODES:
        normalized_mode = "standard"
    date_key = now_local.strftime("%Y-%m-%d")
    if normalized_mode == "standard":
        return {
            "mode": "standard",
            "date_key": date_key,
            "seed_key": date_key,
            "scope_key": None,
            "slot": variant,
            "uses_state": False,
        }

    normalized_scope = normalize_scope_key(scope_key)
    slot = reserve_selection_slot(now_local, normalized_mode, normalized_scope)
    return {
        "mode": normalized_mode,
        "date_key": date_key,
        "seed_key": f"{date_key}:{normalized_scope}",
        "scope_key": normalized_scope,
        "slot": slot,
        "uses_state": True,
    }


def resolve_location(args):
    city_explicit = bool(args.city or env_is_set("MORNING_WEATHER_CITY"))
    city_zh_explicit = bool(args.city_zh or env_is_set("MORNING_WEATHER_CITY_ZH"))
    timezone_explicit = bool(args.timezone or env_is_set("MORNING_WEATHER_TIMEZONE"))
    latitude_explicit = bool(args.latitude is not None or env_is_set("MORNING_WEATHER_LATITUDE"))
    longitude_explicit = bool(args.longitude is not None or env_is_set("MORNING_WEATHER_LONGITUDE"))
    city = (args.city or env_or_default("MORNING_WEATHER_CITY", DEFAULT_CITY)).strip()
    if city_zh_explicit:
        city_zh = (
            args.city_zh or env_or_default("MORNING_WEATHER_CITY_ZH", DEFAULT_CITY_ZH)
        ).strip()
    elif city_explicit:
        city_zh = city
    else:
        city_zh = env_or_default("MORNING_WEATHER_CITY_ZH", DEFAULT_CITY_ZH).strip()
    timezone = (args.timezone or env_or_default("MORNING_WEATHER_TIMEZONE", DEFAULT_TIMEZONE)).strip()
    latitude = args.latitude if args.latitude is not None else env_float("MORNING_WEATHER_LATITUDE", DEFAULT_LATITUDE)
    longitude = args.longitude if args.longitude is not None else env_float("MORNING_WEATHER_LONGITUDE", DEFAULT_LONGITUDE)
    if not city:
        city = DEFAULT_CITY
    if not city_zh:
        city_zh = city
    if not timezone:
        timezone = DEFAULT_TIMEZONE
    return {
        "city_en": city,
        "city_zh": city_zh,
        "timezone": timezone,
        "latitude": latitude,
        "longitude": longitude,
        "city_explicit": city_explicit,
        "city_zh_explicit": city_zh_explicit,
        "timezone_explicit": timezone_explicit,
        "coordinates_explicit": latitude_explicit and longitude_explicit,
        "is_default_location": city == DEFAULT_CITY and city_zh == DEFAULT_CITY_ZH,
    }


def condition_to_chinese(text):
    raw = (text or "").strip()
    lower = raw.lower()
    if not raw:
        return "天气情况未明"
    if "thunder" in lower:
        return "雷雨"
    if "hail" in lower:
        return "冰雹"
    if "sleet" in lower or "ice pellet" in lower:
        return "雨夹雪"
    if "snow" in lower:
        return "下雪"
    if "freezing rain" in lower:
        return "冻雨"
    if "drizzle" in lower:
        return "毛毛雨"
    if "shower" in lower:
        return "阵雨"
    if "rain" in lower:
        return "下雨"
    if "fog" in lower or "mist" in lower:
        return "有雾"
    if "overcast" in lower:
        return "阴天"
    if "cloud" in lower and "partly" in lower:
        return "多云间晴"
    if "cloud" in lower:
        return "多云"
    if "sun" in lower or "clear" in lower:
        return "晴"
    return raw


def open_meteo_code_to_chinese(code):
    mapping = {
        0: "晴",
        1: "基本晴",
        2: "晴间多云",
        3: "阴天",
        45: "有雾",
        48: "冻雾",
        51: "毛毛雨",
        53: "毛毛雨",
        55: "毛毛雨",
        56: "冻毛毛雨",
        57: "冻毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        66: "冻雨",
        67: "冻雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "阵雨",
        81: "阵雨",
        82: "强阵雨",
        85: "阵雪",
        86: "强阵雪",
        95: "雷雨",
        96: "雷雨夹冰雹",
        99: "强雷雨夹冰雹",
    }
    return mapping.get(code, "天气情况未明")


def weather_notes(weather):
    notes = []
    temp = weather.get("temperature_c")
    feels_like = weather.get("feels_like_c")
    min_temp = weather.get("min_c")
    max_temp = weather.get("max_c")
    wind_kph = weather.get("wind_kph")
    humidity = weather.get("humidity_pct")
    precip = weather.get("precip_mm")
    rain = weather.get("chance_of_rain_pct")

    if min_temp is not None and max_temp is not None and max_temp - min_temp >= 7:
        notes.append("昼夜温差较大")
    if ((rain is not None and rain >= 50) or (precip is not None and precip >= 1.0)):
        notes.append("今天有明显雨意，带伞更稳妥")
    if wind_kph is not None and wind_kph >= 20:
        notes.append("风感比较明显")
    if humidity is not None and humidity >= 80:
        notes.append("湿度偏高，体感容易发闷")
    if temp is not None and feels_like is not None and feels_like <= temp - 3:
        notes.append("体感比温度更凉")
    return notes


def build_summary(city_label, weather):
    if not weather.get("ok"):
        return f"{city_label}实时天气暂未获取到。"

    parts = []
    condition = weather.get("condition_zh")
    temp = weather.get("temperature_c")
    feels_like = weather.get("feels_like_c")
    min_temp = weather.get("min_c")
    max_temp = weather.get("max_c")
    rain = weather.get("chance_of_rain_pct")
    wind = weather.get("wind_kph")
    humidity = weather.get("humidity_pct")

    if condition:
        parts.append(condition)
    if temp is not None:
        parts.append(f"{temp}°C")
    if feels_like is not None:
        parts.append(f"体感{feels_like}°C")
    if min_temp is not None and max_temp is not None:
        parts.append(f"今日约{min_temp}°C到{max_temp}°C")
    if rain is not None:
        parts.append(f"降雨概率约{rain}%")
    if wind is not None:
        parts.append(f"风速约{wind}km/h")
    if humidity is not None:
        parts.append(f"湿度约{humidity}%")
    return f"{city_label}当前" + "，".join(parts) + "。"


def weather_icon(condition_zh):
    text = condition_zh or ""
    if "雷" in text:
        return "⛈️"
    if "雪" in text:
        return "🌨️"
    if "雨" in text:
        return "🌧️"
    if "雾" in text:
        return "🌫️"
    if "阴" in text:
        return "☁️"
    if "多云" in text or "晴间" in text or "基本晴" in text:
        return "🌥️"
    if "晴" in text:
        return "☀️"
    return "☁️"


def temperature_text(weather):
    current = weather.get("temperature_c")
    min_temp = weather.get("min_c")
    max_temp = weather.get("max_c")
    if min_temp is not None and max_temp is not None:
        return f"{min_temp}°C到{max_temp}°C"
    if min_temp is not None:
        return f"最低{min_temp}°C"
    if max_temp is not None:
        return f"最高{max_temp}°C"
    if current is not None:
        return f"当前约{current}°C"
    return "气温暂未获取到"


def outfit_lead(weather):
    temp = weather.get("temperature_c")
    feels_like = weather.get("feels_like_c")
    baseline = feels_like if feels_like is not None else temp
    if baseline is None:
        return "带件薄外套会更稳妥"
    if baseline <= 5:
        return "厚外套或呢大衣穿上会更稳妥"
    if baseline <= 10:
        return "外套加长袖会更合适"
    if baseline <= 16:
        return "薄外套配长袖会更合适"
    if baseline <= 22:
        return "长袖或薄外套基本够用"
    if baseline <= 28:
        return "轻薄一点穿会更舒服"
    return "短袖为主会更轻快"


def outfit_tail(weather):
    notes = []
    min_temp = weather.get("min_c")
    max_temp = weather.get("max_c")
    rain = weather.get("chance_of_rain_pct")
    precip = weather.get("precip_mm")
    wind_kph = weather.get("wind_kph")
    humidity = weather.get("humidity_pct")

    if min_temp is not None and max_temp is not None and max_temp - min_temp >= 7:
        notes.append("早晚温差大")
    if ((rain is not None and rain >= 50) or (precip is not None and precip >= 1.0)):
        notes.append("出门带把伞更稳妥")
    if wind_kph is not None and wind_kph >= 20:
        notes.append("风有点大，衣服最好能挡风")
    if humidity is not None and humidity >= 85 and not any("伞" in note for note in notes):
        notes.append("空气偏潮，穿得利落一点更舒服")

    if not notes:
        return "正常轻便出门就可以"
    return "，".join(notes)


def build_weather_line(weather, city_label):
    if not weather.get("ok"):
        return f"{city_label}今天天气暂未获取到，带件薄外套，出门前看一眼实时天气会更稳妥。"
    icon = weather.get("icon") or weather_icon(weather.get("condition_zh"))
    return (
        f"{city_label}今天{icon} {weather.get('condition_zh')}，{temperature_text(weather)}，"
        f"{outfit_lead(weather)}，{outfit_tail(weather)}。"
    )


def parse_wttr(location):
    city_query = urllib.parse.quote(location["city_en"])
    payload = fetch_json(f"https://wttr.in/{city_query}?format=j1")
    current = (payload.get("current_condition") or [{}])[0]
    today = (payload.get("weather") or [{}])[0]
    hourly = today.get("hourly") or []
    raw_desc = ""
    desc_list = current.get("weatherDesc") or []
    if desc_list:
        raw_desc = (desc_list[0] or {}).get("value") or ""
    weather = {
        "ok": True,
        "source": "wttr.in",
        "condition_raw": raw_desc,
        "condition_zh": condition_to_chinese(raw_desc),
        "temperature_c": as_int(current.get("temp_C")),
        "feels_like_c": as_int(current.get("FeelsLikeC")),
        "min_c": as_int(today.get("mintempC")),
        "max_c": as_int(today.get("maxtempC")),
        "humidity_pct": as_int(current.get("humidity")),
        "wind_kph": as_int(current.get("windspeedKmph")),
        "precip_mm": as_float(current.get("precipMM")),
        "chance_of_rain_pct": max(
            [as_int(item.get("chanceofrain")) or 0 for item in hourly] or [0]
        ),
        "errors": [],
    }
    weather["notes"] = weather_notes(weather)
    weather["summary"] = build_summary(location["city_zh"], weather)
    return weather


def parse_open_meteo(location):
    resolved = resolve_open_meteo_target(location)
    timezone = resolved["timezone"]
    query = urllib.parse.urlencode(
        {
            "latitude": resolved["latitude"],
            "longitude": resolved["longitude"],
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                ]
            ),
            "daily": ",".join(
                [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                    "weather_code",
                ]
            ),
            "timezone": timezone,
            "forecast_days": 1,
        }
    )
    payload = fetch_json(f"https://api.open-meteo.com/v1/forecast?{query}")
    current = payload.get("current") or {}
    daily = payload.get("daily") or {}
    code = as_int(current.get("weather_code"))
    weather = {
        "ok": True,
        "source": "open-meteo",
        "condition_raw": str(code) if code is not None else "",
        "condition_zh": open_meteo_code_to_chinese(code),
        "temperature_c": as_int(current.get("temperature_2m")),
        "feels_like_c": as_int(current.get("apparent_temperature")),
        "min_c": as_int((daily.get("temperature_2m_min") or [None])[0]),
        "max_c": as_int((daily.get("temperature_2m_max") or [None])[0]),
        "humidity_pct": as_int(current.get("relative_humidity_2m")),
        "wind_kph": as_int(current.get("wind_speed_10m")),
        "precip_mm": as_float(current.get("precipitation")),
        "chance_of_rain_pct": as_int(
            (daily.get("precipitation_probability_max") or [None])[0]
        ),
        "errors": [],
    }
    weather["notes"] = weather_notes(weather)
    weather["summary"] = build_summary(location["city_zh"], weather)
    return weather


def resolve_open_meteo_target(location):
    cached = location.get("_open_meteo_target")
    if cached is not None:
        return cached

    if location["coordinates_explicit"] or location["is_default_location"]:
        timezone = location["timezone"]
        if not timezone:
            timezone = DEFAULT_TIMEZONE
        target = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "timezone": timezone,
            "country_code": "CN" if location["is_default_location"] else None,
        }
        location["_open_meteo_target"] = target
        return target

    queries = []
    if location["city_en"]:
        queries.append(location["city_en"])
    if location["city_zh"] and location["city_zh"] not in queries:
        queries.append(location["city_zh"])

    for query_name in queries:
        query = urllib.parse.urlencode(
            {
                "name": query_name,
                "count": 5,
                "language": "zh",
                "format": "json",
            }
        )
        payload = fetch_json(f"https://geocoding-api.open-meteo.com/v1/search?{query}")
        results = payload.get("results") or []
        if not results:
            continue

        preferred = None
        if location["timezone"] == DEFAULT_TIMEZONE:
            preferred = next(
                (item for item in results if item.get("country_code") in CHINA_COUNTRY_CODES),
                None,
            )
        if preferred is None and location["timezone_explicit"]:
            preferred = next(
                (item for item in results if item.get("timezone") == location["timezone"]),
                None,
            )
        if preferred is None:
            preferred = results[0]

        if not location["city_zh_explicit"]:
            preferred_name = normalize_location_label(preferred.get("name"))
            if preferred_name:
                location["city_zh"] = preferred_name
        timezone = location["timezone"]
        if not location["timezone_explicit"]:
            timezone = preferred.get("timezone") or timezone or DEFAULT_TIMEZONE
        target = {
            "latitude": preferred.get("latitude"),
            "longitude": preferred.get("longitude"),
            "timezone": timezone or DEFAULT_TIMEZONE,
            "country_code": preferred.get("country_code"),
        }
        if target["latitude"] is not None and target["longitude"] is not None:
            location["_open_meteo_target"] = target
            return target

    raise ValueError("missing coordinates for Open-Meteo lookup")


def prefer_open_meteo(location):
    if location["is_default_location"]:
        return True
    if location["coordinates_explicit"] and location["timezone"] == DEFAULT_TIMEZONE:
        return True
    try:
        target = resolve_open_meteo_target(location)
    except Exception:
        return False
    return target.get("country_code") in CHINA_COUNTRY_CODES


def build_weather(location):
    errors = []
    loaders = (parse_open_meteo, parse_wttr) if prefer_open_meteo(location) else (parse_wttr, parse_open_meteo)
    for loader in loaders:
        try:
            weather = loader(location)
            return weather
        except Exception as exc:  # pragma: no cover
            errors.append(f"{loader.__name__}: {exc}")
    return {
        "ok": False,
        "source": None,
        "condition_raw": "",
        "condition_zh": "",
        "temperature_c": None,
        "feels_like_c": None,
        "min_c": None,
        "max_c": None,
        "humidity_pct": None,
        "wind_kph": None,
        "precip_mm": None,
        "chance_of_rain_pct": None,
        "notes": [],
        "errors": errors,
        "summary": build_summary(location["city_zh"], {"ok": False}),
    }


def load_wisdom_pairs():
    try:
        payload = json.loads(WISDOM_PAIRS_PATH.read_text(encoding="utf-8"))
        pairs = payload.get("pairs") or []
    except Exception:
        pairs = []
    cleaned = []
    for item in pairs:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "").strip()
        name = str(item.get("name") or "").strip()
        quote = str(item.get("quote") or "").strip().rstrip("。")
        blessing = str(item.get("blessing") or "").strip()
        if role and name and quote and blessing:
            cleaned.append(
                {
                    "role": role,
                    "name": name,
                    "quote": quote,
                    "blessing": blessing,
                }
            )
    return cleaned or FALLBACK_WISDOM_PAIRS


def rotate_index(base_key, salt, length, variant):
    if length <= 0:
        raise ValueError("rotation length must be positive")
    base_index = zlib.crc32(f"{base_key}:{salt}".encode("utf-8")) % length
    return (base_index + variant) % length


def select_rotation_index(length, salt, selection):
    if selection["mode"] == "standard":
        return rotate_index(selection["date_key"], salt, length, selection["slot"])
    order = shuffled_indices(selection["seed_key"], salt, length)
    return order[selection["slot"] % length]


def choose_wisdom_pair(selection):
    pairs = load_wisdom_pairs()
    rotation_key = selection["seed_key"]
    index = select_rotation_index(len(pairs), "wisdom", selection)
    pair = dict(pairs[index])
    pair.update(
        {
            "source": "local_wisdom_pairs",
            "rotation_key": rotation_key,
            "variant": selection["slot"],
            "selection_mode": selection["mode"],
            "index": index,
            "count": len(pairs),
        }
    )
    return pair


def pick_icon(pool, selection, salt):
    rotation_key = selection["seed_key"]
    index = select_rotation_index(len(pool), salt, selection)
    return {
        "text": pool[index],
        "rotation_key": rotation_key,
        "variant": selection["slot"],
        "selection_mode": selection["mode"],
        "index": index,
        "count": len(pool),
    }


def build_wisdom_line(wisdom, ending_icon_text):
    return (
        f"{wisdom['role']}{wisdom['name']}说：“{wisdom['quote']}。”"
        f"{wisdom['blessing']}{ending_icon_text}"
    )


def build_message(greeting_line, weather_line, wisdom_line):
    return "\n\n".join([greeting_line, weather_line, wisdom_line])


def part_of_day(now_local):
    hour = now_local.hour
    if 5 <= hour < 11:
        return "早上"
    if 11 <= hour < 14:
        return "中午"
    if 14 <= hour < 18:
        return "下午"
    return "晚上"


def main():
    args = parse_args()
    location = resolve_location(args)
    variant = normalize_variant(args.variant if args.variant is not None else env_int("MORNING_WEATHER_VARIANT", 0))
    now_local = dt.datetime.now(ZoneInfo(location["timezone"]))
    selection = build_selection_context(now_local, args.selection_mode, args.scope_key, variant)
    weather = build_weather(location)
    weather["icon"] = weather_icon(weather.get("condition_zh"))
    wisdom = choose_wisdom_pair(selection)
    greeting_icon = pick_icon(GREETING_ICONS, selection, "greeting")
    ending_icon = pick_icon(ENDING_ICONS, selection, "ending")
    greeting_line = f"{greeting_icon['text']} 早安！"
    weather_line = build_weather_line(weather, location["city_zh"])
    wisdom_line = build_wisdom_line(wisdom, ending_icon["text"])
    variant_label = "standard" if selection["mode"] == "standard" and selection["slot"] == 0 else f"{selection['mode']}-{selection['slot']}"
    payload = {
        "schema_version": 1,
        "generated_at": now_local.isoformat(),
        "variant": {
            "index": selection["slot"],
            "label": variant_label,
            "is_default": selection["mode"] == "standard" and selection["slot"] == 0,
            "mode": selection["mode"],
        },
        "selection": {
            "mode": selection["mode"],
            "slot": selection["slot"],
            "scope_key": selection["scope_key"],
            "uses_state": selection["uses_state"],
        },
        "location": {
            "city_en": location["city_en"],
            "city_zh": location["city_zh"],
            "timezone": location["timezone"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        },
        "date_context": {
            "iso_date": now_local.strftime("%Y-%m-%d"),
            "weekday_cn": WEEKDAY_CN[now_local.weekday()],
            "local_time": now_local.strftime("%H:%M"),
            "part_of_day": part_of_day(now_local),
        },
        "season_hint": MONTH_HINTS[now_local.month],
        "weather": weather,
        "greeting": {
            "icon": greeting_icon["text"],
            "text": greeting_line,
            "rotation_key": greeting_icon["rotation_key"],
            "index": greeting_icon["index"],
            "count": greeting_icon["count"],
        },
        "wisdom": {
            **wisdom,
            "ending_icon": ending_icon["text"],
            "line": wisdom_line,
        },
        "formatted": {
            "greeting": greeting_line,
            "weather": weather_line,
            "wisdom": wisdom_line,
            "message": build_message(greeting_line, weather_line, wisdom_line),
        },
    }
    if args.print_message:
        print(payload["formatted"]["message"])
    elif args.compact:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
