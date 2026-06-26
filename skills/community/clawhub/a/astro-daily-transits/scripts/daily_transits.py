#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astro Daily Transits — Swiss Ephemeris Edition v1.0.0
Calculates daily transits over a natal chart and generates a forecast.

Uses pyswisseph 2.10.3.2 for high-precision planetary positions.

Usage:
  python daily_transits.py <date DD.MM.YYYY> <time HH:MM> <city> [--target-date DD.MM.YYYY] [--json]
  python daily_transits.py 24.04.1983 07:00 Ижевск --target-date 04.06.2026
"""

import math
import io
import os
import sys
import json
import argparse
from datetime import datetime, date

# ─── Load swisseph ───
import importlib.util as _ilu
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_swe = None
for _fname in ('swisseph.cp314-win_amd64.pyd.dat', 'swisseph.cp314-win_amd64.pyd'):
    _lib = os.path.join(_SCRIPT_DIR, _fname)
    if os.path.exists(_lib):
        _load_path = _lib
        _tmp_pyd = None
        try:
            if _load_path.endswith('.dat'):
                _tmp_pyd = _load_path[:-4]
                import shutil
                shutil.copy2(_load_path, _tmp_pyd)
                _load_path = _tmp_pyd
            _spec = _ilu.spec_from_file_location('swisseph', _load_path)
            if _spec is not None and _spec.loader is not None:
                _swe = _ilu.module_from_spec(_spec)
                _spec.loader.exec_module(_swe)
                break
        except Exception:
            pass
        finally:
            if _tmp_pyd is not None:
                try: os.remove(_tmp_pyd)
                except Exception: pass

if _swe is None:
    sys.path.insert(0, _SCRIPT_DIR)
    try:
        import swisseph as _swe
    except ImportError:
        print("ERROR: swisseph not found.")
        sys.exit(1)

swe = _swe

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ─── Constants ───
SIGNS_RU = [
    "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
    "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
]
SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
SIGNS_SYM = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]

PLANET_CONFIG = [
    (swe.SUN,      "Sun",     "☀️", "Солнце",     "Sun"),
    (swe.MOON,     "Moon",    "🌙", "Луна",       "Moon"),
    (swe.MERCURY,  "Mercury", "☿",  "Меркурий",   "Mercury"),
    (swe.VENUS,    "Venus",   "♀",  "Венера",     "Venus"),
    (swe.MARS,     "Mars",    "♂",  "Марс",       "Mars"),
    (swe.JUPITER,  "Jupiter", "♃",  "Юпитер",     "Jupiter"),
    (swe.SATURN,   "Saturn",  "♄",  "Сатурн",     "Saturn"),
    (swe.URANUS,   "Uranus",  "♅",  "Уран",       "Uranus"),
    (swe.NEPTUNE,  "Neptune", "♆",  "Нептун",     "Neptune"),
    (swe.PLUTO,    "Pluto",   "♇",  "Плутон",     "Pluto"),
]

ASPECTS = {
    "conjunction":  {"symbol": "☌", "name_ru": "Соединение",   "name_en": "Conjunction",  "orb": 8, "nature": "powerful"},
    "opposition":   {"symbol": "☍", "name_ru": "Оппозиция",    "name_en": "Opposition",   "orb": 8, "nature": "tense"},
    "trine":        {"symbol": "△", "name_ru": "Трин",         "name_en": "Trine",        "orb": 7, "nature": "harmonious"},
    "square":       {"symbol": "□", "name_ru": "Квадрат",      "name_en": "Square",       "orb": 7, "nature": "challenging"},
    "sextile":      {"symbol": "✶", "name_ru": "Секстиль",     "name_en": "Sextile",      "orb": 5, "nature": "opportunity"},
    "semisextile":  {"symbol": "⚺", "name_ru": "Полусекстиль",  "name_en": "Semisextile",  "orb": 2, "nature": "subtle"},
    "semisquare":   {"symbol": "∠", "name_ru": "Полуквадрат",   "name_en": "Semisquare",   "orb": 2, "nature": "irritation"},
    "quincunx":     {"symbol": "⚹", "name_ru": "Квинконс",      "name_en": "Quincunx",     "orb": 2, "nature": "adjustment"},
}

HOUSES_RU = [
    "I (Личность)", "II (Деньги)", "III (Общение)", "IV (Дом)",
    "V (Творчество)", "VI (Здоровье)", "VII (Партнёрство)", "VIII (Трансформация)",
    "IX (Философия)", "X (Карьера)", "XI (Друзья)", "XII (Подсознание)"
]
HOUSES_EN = [
    "I (Self)", "II (Money)", "III (Communication)", "IV (Home)",
    "V (Creativity)", "VI (Health)", "VII (Partnership)", "VIII (Transformation)",
    "IX (Philosophy)", "X (Career)", "XI (Friends)", "XII (Subconscious)"
]

CITY_DB = {
    "ижевск": {"lat": 56.8519, "lon": 53.2114, "tz": "Europe/Samara", "name": "Ижевск, Россия"},
    "москва": {"lat": 55.7558, "lon": 37.6173, "tz": "Europe/Moscow", "name": "Москва, Россия"},
    "санкт-петербург": {"lat": 59.9343, "lon": 30.3351, "tz": "Europe/Moscow", "name": "Санкт-Петербург, Россия"},
    "петербург": {"lat": 59.9343, "lon": 30.3351, "tz": "Europe/Moscow", "name": "Санкт-Петербург, Россия"},
    "спб": {"lat": 59.9343, "lon": 30.3351, "tz": "Europe/Moscow", "name": "Санкт-Петербург, Россия"},
    "екатеринбург": {"lat": 56.8389, "lon": 60.6057, "tz": "Asia/Yekaterinburg", "name": "Екатеринбург, Россия"},
    "новосибирск": {"lat": 55.0084, "lon": 82.9357, "tz": "Asia/Novosibirsk", "name": "Новосибирск, Россия"},
    "казань": {"lat": 55.7887, "lon": 49.1221, "tz": "Europe/Moscow", "name": "Казань, Россия"},
    "нижний новгород": {"lat": 56.2965, "lon": 43.9361, "tz": "Europe/Moscow", "name": "Нижний Новгород, Россия"},
    "самара": {"lat": 53.2001, "lon": 50.1500, "tz": "Europe/Samara", "name": "Самара, Россия"},
    "ростов-на-дону": {"lat": 47.2357, "lon": 39.7015, "tz": "Europe/Moscow", "name": "Ростов-на-Дону, Россия"},
    "воронеж": {"lat": 51.6720, "lon": 39.1843, "tz": "Europe/Moscow", "name": "Воронеж, Россия"},
    "краснодар": {"lat": 45.0355, "lon": 38.9753, "tz": "Europe/Moscow", "name": "Краснодар, Россия"},
    "уфа": {"lat": 54.7388, "lon": 55.9721, "tz": "Asia/Yekaterinburg", "name": "Уфа, Россия"},
    "волгоград": {"lat": 48.7080, "lon": 44.5133, "tz": "Europe/Moscow", "name": "Волгоград, Россия"},
    "пермь": {"lat": 58.0105, "lon": 56.2502, "tz": "Asia/Yekaterinburg", "name": "Пермь, Россия"},
    "тюмень": {"lat": 57.1522, "lon": 65.5272, "tz": "Asia/Yekaterinburg", "name": "Тюмень, Россия"},
    "омск": {"lat": 54.9885, "lon": 73.3242, "tz": "Asia/Omsk", "name": "Омск, Россия"},
    "барнаул": {"lat": 53.3548, "lon": 83.7698, "tz": "Asia/Barnaul", "name": "Барнаул, Россия"},
    "иркутск": {"lat": 52.2978, "lon": 104.2964, "tz": "Asia/Irkutsk", "name": "Иркутск, Россия"},
    "хабаровск": {"lat": 48.4827, "lon": 135.0839, "tz": "Asia/Vladivostok", "name": "Хабаровск, Россия"},
    "владивосток": {"lat": 43.1332, "lon": 131.9113, "tz": "Asia/Vladivostok", "name": "Владивосток, Россия"},
    "ярославль": {"lat": 57.6261, "lon": 39.8845, "tz": "Europe/Moscow", "name": "Ярославль, Россия"},
    "тольятти": {"lat": 53.5303, "lon": 49.3461, "tz": "Europe/Samara", "name": "Тольятти, Россия"},
    "челябинск": {"lat": 55.1644, "lon": 61.4368, "tz": "Asia/Yekaterinburg", "name": "Челябинск, Россия"},
    "саратов": {"lat": 51.5336, "lon": 46.0343, "tz": "Europe/Samara", "name": "Саратов, Россия"},
    "минск": {"lat": 53.9045, "lon": 27.5615, "tz": "Europe/Minsk", "name": "Минск, Беларусь"},
    "киев": {"lat": 50.4501, "lon": 30.5234, "tz": "Europe/Kiev", "name": "Киев, Украина"},
    "алматы": {"lat": 43.2220, "lon": 76.8512, "tz": "Asia/Almaty", "name": "Алматы, Казахстан"},
    "можга": {"lat": 56.4527, "lon": 52.2117, "tz": "Europe/Samara", "name": "Можга, Россия"},
    "лондон": {"lat": 51.5074, "lon": -0.1278, "tz": "Europe/London", "name": "Лондон, Великобритания"},
    "нью-йорк": {"lat": 40.7128, "lon": -74.0060, "tz": "America/New_York", "name": "Нью-Йорк, США"},
    "лос-анджелес": {"lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles", "name": "Лос-Анджелес, США"},
    "берлин": {"lat": 52.5200, "lon": 13.4050, "tz": "Europe/Berlin", "name": "Берлин, Германия"},
    "париж": {"lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris", "name": "Париж, Франция"},
    "токио": {"lat": 35.6762, "lon": 139.6503, "tz": "Asia/Tokyo", "name": "Токио, Япония"},
    "пекин": {"lat": 39.9042, "lon": 116.4074, "tz": "Asia/Shanghai", "name": "Пекин, Китай"},
    "дубай": {"lat": 25.2048, "lon": 55.2708, "tz": "Asia/Dubai", "name": "Дубай, ОАЭ"},
}

# ─── Helpers ───

def lon_to_sign(lon):
    idx = int(lon // 30) % 12
    deg = lon % 30
    return idx, deg

def format_deg(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    return f"{d}°{m:02d}'"

def get_city(city_name):
    key = city_name.strip().lower()
    if key in CITY_DB:
        return CITY_DB[key]
    for k, v in CITY_DB.items():
        if key in k or k in key:
            return v
    raise ValueError(f"City not found: {city_name}")

def parse_date(s):
    parts = s.strip().split(".")
    return int(parts[2]), int(parts[1]), int(parts[0])

def parse_time(s):
    parts = s.strip().split(":")
    return int(parts[0]), int(parts[1])

def compute_jd(year, month, day, hour, minute, tz_offset):
    return swe.julday(year, month, day, hour + minute / 60.0 - swe.degnorm(tz_offset) / 15.0)

def calc_positions(jd):
    """Returns dict of planet positions with lon, speed, retro."""
    result = {}
    for pid, key, sym, name_ru, name_en in PLANET_CONFIG:
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        xx, rflag = swe.calc_ut(jd, pid, flags)
        lon = xx[0]
        speed = xx[3]
        retro = speed < 0
        result[key] = {"lon": lon, "speed": speed, "retro": retro}
    return result

def calc_houses(jd, lat, lon):
    """Returns houses, asc, mc."""
    flags = swe.FLG_SWIEPH
    data = swe.houses_ex(jd, lat, lon, b'P', flags)
    houses = list(data[0])
    asc = houses[0]
    mc = houses[9]
    return houses, asc, mc

def get_house(lon, houses):
    """Determine which house a longitude falls in."""
    norm_lon = lon % 360
    for i in range(12):
        start = houses[i] % 360
        end = houses[(i + 1) % 12] % 360
        if end > start:
            if start <= norm_lon < end:
                return i + 1
        else:
            if norm_lon >= start or norm_lon < end:
                return i + 1
    return 1

def calc_aspects(transit_pos, natal_pos):
    """Find aspects between transit planets and natal planets."""
    aspects = []
    for t_key, t_data in transit_pos.items():
        for n_key, n_data in natal_pos.items():
            diff = abs(t_data["lon"] - n_data["lon"])
            if diff > 180:
                diff = 360 - diff
            for atype, aconf in ASPECTS.items():
                orb = aconf["orb"]
                if diff <= orb:
                    orb_exact = diff
                    aspects.append({
                        "transit": t_key,
                        "natal": n_key,
                        "type": atype,
                        "symbol": aconf["symbol"],
                        "name": aconf["name_ru"],
                        "nature": aconf["nature"],
                        "orb": round(orb_exact, 1)
                    })
                    break
    return aspects

# ─── Interpretation ───

TRANSIT_INTERP_RU = {
    "Sun": {
        "conjunction": "Транзитное Солнце на вашем натальном — день самовыражения и энергии. Хорошо для начинаний.",
        "opposition": "Оппозиция Солнца — напряжение в отношениях, потребность в балансе между «я» и «другой».",
        "trine": "Гармоничный день! Энергия течёт легко, хорошее время для творчества и общения.",
        "square": "Квадрат Солнца — день испытаний, возможны конфликты эго. Не принимайте решения в спешке.",
        "sextile": "Возможности для роста и самовыражения. Используйте шансы, которые появляются.",
    },
    "Moon": {
        "conjunction": "Транзитная Луна — эмоциональный день, обострение чувств и интуиции.",
        "opposition": "Луна в оппозиции — эмоциональные качели, потребность в заботе и поддержке.",
        "trine": "Гармоничный эмоциональный фон. День для семейных дел и отдыха.",
        "square": "Раздражительность, эмоциональный дискомфорт. Избегайте конфликтов дома.",
        "sextile": "Хороший день для общения с близкими, мягкие эмоции.",
    },
    "Mercury": {
        "conjunction": "Транзитный Меркурий — день важных разговоров и решений ума.",
        "opposition": "Оппозиция Меркурия — споры, недопонимание. Проверяйте информацию.",
        "trine": "Ясное мышление, удачные переговоры и поездки.",
        "square": "Путаница в мыслях, ошибки в документах. Будьте внимательны.",
        "sextile": "Хороший день для обучения и общения.",
    },
    "Venus": {
        "conjunction": "Транзитная Венера — день любви, красоты и финансовых поступлений.",
        "opposition": "Оппозиция Венеры — напряжение в отношениях, возможны финансовые расходы.",
        "trine": "Гармония в любви, приятные встречи, удачные покупки.",
        "square": "Конфликты в отношениях из-за ценностей или денег.",
        "sextile": "Приятные возможности в любви и финансах.",
    },
    "Mars": {
        "conjunction": "Транзитный Марс — всплеск энергии! Действуйте, но избегайте агрессии.",
        "opposition": "Оппозиция Марса — конфликты, столкновения. Контролируйте гнев.",
        "trine": "Энергия течёт легко, хороший день для спорта и работы.",
        "square": "Квадрат Марса — раздражительность, риск травм. Будьте осторожны!",
        "sextile": "Хороший день для активности и инициативы.",
    },
    "Jupiter": {
        "conjunction": "Транзитный Юпитер — день удачи и расширения! Смелые шаги приветствуются.",
        "opposition": "Оппозиция Юпитера — риск переоценки сил, избыточных трат.",
        "trine": "Гармония и рост! Один из лучших дней для любых начинаний.",
        "square": "Квадрат Юпитера — избыточные амбиции, риск ошибок от самонадеянности.",
        "sextile": "Благоприятные возможности, удача в делах.",
    },
    "Saturn": {
        "conjunction": "Транзитный Сатурн — день серьёзности и ответственности. Решайте важные вопросы.",
        "opposition": "Оппозиция Сатурна — давление извне, испытания на прочность.",
        "trine": "Стабильность и дисциплина. Хорошо для долгосрочных планов.",
        "square": "Квадрат Сатурна — ограничения и препятствия. Терпение!",
        "sextile": "Возможности через дисциплину и труд.",
    },
    "Uranus": {
        "conjunction": "Транзитный Уран — день озарений и неожиданностей! Готовьтесь к сюрпризам.",
        "opposition": "Оппозиция Урана — внезапные перемены, потребность в свободе.",
        "trine": "Креативные идеи, позитивные неожиданности.",
        "square": "Квадрат Урана — революционные импульсы, конфликт с авторитетами.",
        "sextile": "Новые идеи и возможности через инновации.",
    },
    "Neptune": {
        "conjunction": "Транзитный Нептун — день интуиции и духовности. Но не теряйте связь с реальностью.",
        "opposition": "Оппозиция Нептуна — иллюзии и заблуждения. Проверяйте факты.",
        "trine": "Вдохновение и творческая интуиция. Прекрасный день для искусства.",
        "square": "Квадрат Нептуна — обманчивые ситуации, путаница.",
        "sextile": "Тонкие инсайты, мягкие творческие влияния.",
    },
    "Pluto": {
        "conjunction": "Транзитный Плутон — глубинная трансформация. Отпускайте старое.",
        "opposition": "Оппозиция Плутона — кризис власти, трансформация через конфликт.",
        "trine": "Глубокая позитивная трансформация и личностный рост.",
        "square": "Квадрат Плутона — мощное давление перемен. Это пройдёт, но изменит вас.",
        "sextile": "Возможности для глубинной работы над собой.",
    },
}

HOUSE_ACTIVATION_RU = [
    "Активируется сфера личности и самовыражения. День для заботы о себе.",
    "Активируются деньги и ценности. Финансовые вопросы на повестке дня.",
    "Активируется общение и обучения. Встречи, поездки, разговоры.",
    "Активируется дом и семья. Вопросы жилища, семьи, корней.",
    "Активируется творчество и дети. Романтика, хобби, дети.",
    "Активируется здоровье и работа. Рутина, самочувствие, обязанности.",
    "Активируются партнёрства. Отношения, брак, значимые встречи.",
    "Активируются трансформации. Чужие ресурсы, интимность, кризисы.",
    "Активируются путешествия и философия. Обучение, духовность, дальние дороги.",
    "Активируется карьера и статус. Профессиональные вопросам, публичность.",
    "Активируются друзья и надежды. Социум, коллективные проекты.",
    "Активируется подсознание. Отдых, уединение, работа с психикой.",
]

def generate_forecast(aspects, transits_in_houses, natal, target_date_str, lang="ru"):
    """Generate human-readable forecast text."""
    lines = []
    natures = {"powerful": [], "tense": [], "harmonious": [], "challenging": [], "opportunity": [], "subtle": [], "irritation": [], "adjustment": []}

    for a in aspects:
        natures[a["nature"]].append(a)

    # Sort harmonious first, then challenging, then others
    priority = ["harmonious", "opportunity", "powerful", "challenging", "tense", "adjustment", "irritation", "subtle"]
    sorted_aspects = []
    for p in priority:
        sorted_aspects.extend(natures[p])

    lines.append(f"ПРОГНОЗ НА {target_date_str}")
    lines.append("=" * 50)
    lines.append("")

    if not sorted_aspects:
        lines.append("  Транзитные аспекты минимальны — спокойный день без ярких событий.")
        lines.append("")
    else:
        lines.append("  КЛЮЧЕВЫЕ ТРАНЗИТЫ ДНЯ:")
        lines.append("")

        seen = set()
        for a in sorted_aspects:
            key = (a["transit"], a["natal"], a["type"])
            if key in seen:
                continue
            seen.add(key)

            interp = TRANSIT_INTERP_RU.get(a["transit"], {}).get(a["type"], f"  {a['symbol']} {a['transit']} {a['name']} {a['natal']} — влияние на сферу {a['natal']}.")
            lines.append(f"  {a['symbol']} {a['transit']} {a['name']} → {a['natal']} (орб {a['orb']}°)")
            lines.append(f"     {interp}")
            lines.append("")

    # House activations
    house_lines = []
    for planet_key, house_num in sorted(transits_in_houses.items(), key=lambda x: x[1]):
        planet_ru = {"Sun": "Солнце", "Moon": "Луна", "Mercury": "Меркурий", "Venus": "Венера",
                     "Mars": "Марс", "Jupiter": "Юпитер", "Saturn": "Сатурн", "Uranus": "Уран",
                     "Neptун": "Нептун", "Pluto": "Плутон"}.get(planet_key, planet_key)
        house_idx = house_num - 1
        if 0 <= house_idx < 12:
            house_lines.append(f"  {planet_ru} в {house_num}-м доме — {HOUSE_ACTIVATION_RU[house_idx]}")

    if house_lines:
        lines.append("  АКТИВАЦИЯ ДОМОВ:")
        lines.extend(house_lines)
        lines.append("")

    # Summary
    good = len(natures["harmonious"]) + len(natures["opportunity"])
    bad = len(natures["challenging"]) + len(natures["tense"])
    powerful = len(natures["powerful"])

    lines.append("  ИТОГО:")
    if good > bad and good > 0:
        lines.append(f"  ✅ Благоприятный день ({good} гармоничных аспектов). Смело действуйте!")
    elif bad > good and bad > 0:
        lines.append(f"  ⚠️ Напряжённый день ({bad} напряжённых аспектов). Будьте осторожны и терпеливы.")
    elif powerful > 0:
        lines.append(f"  🔥 Мощный день ({powerful} соединений). Глубокие изменения возможны.")
    else:
        lines.append(f"  💤 Спокойный день. Хорошее время для рутины и отдыха.")

    return "\n".join(lines)


# ─── Main ───

def main():
    parser = argparse.ArgumentParser(description="Daily Transit Forecast")
    parser.add_argument("date", help="Birth date DD.MM.YYYY")
    parser.add_argument("time", help="Birth time HH:MM")
    parser.add_argument("city", help="Birth city")
    parser.add_argument("--target-date", default=None, help="Forecast date DD.MM.YYYY (default: today)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--lang", default="ru", choices=["ru", "en"])
    parser.add_argument("--name", default="", help="Person's name (for display)")
    args = parser.parse_args()

    # Parse birth data
    by, bm, bd = parse_date(args.date)
    bh, bmin = parse_time(args.time)
    city = get_city(args.city)
    tz_hours = 4.0  # Russia default; for production use city DB tz offset

    # Natal chart JD (UTC)
    jd_natal = swe.julday(by, bm, bd, bh + bmin / 60.0 - tz_hours)

    # Calculate natal positions
    natal_pos = calc_positions(jd_natal)
    natal_houses, natal_asc, natal_mc = calc_houses(jd_natal, city["lat"], city["lon"])

    # Natal planets in houses
    natal_planet_houses = {}
    for key, data in natal_pos.items():
        natal_planet_houses[key] = get_house(data["lon"], natal_houses)

    # Target date
    if args.target_date:
        ty, tm, td = parse_date(args.target_date)
    else:
        today = date.today()
        ty, tm, td = today.year, today.month, today.day

    # Transit JD (noon of target date, UTC)
    jd_transit = swe.julday(ty, tm, td, 12.0 - tz_hours)

    # Calculate transit positions
    transit_pos = calc_positions(jd_transit)

    # Transit planets in natal houses
    transits_in_houses = {}
    for key, data in transit_pos.items():
        transits_in_houses[key] = get_house(data["lon"], natal_houses)

    # Calculate aspects
    aspects = calc_aspects(transit_pos, natal_pos)

    # Target date string
    target_str = f"{td:02d}.{tm:02d}.{ty}"

    if args.json:
        result = {
            "name": args.name,
            "birth_date": args.date,
            "birth_time": args.time,
            "birth_city": city["name"],
            "target_date": target_str,
            "nat.Sun": natal_pos["Sun"]["lon"],
            "natal": {k: {"lon": v["lon"], "speed": round(v["speed"], 3), "retro": v["retro"]} for k, v in natal_pos.items()},
            "transits": {k: {"lon": v["lon"], "speed": round(v["speed"], 3), "retro": v["retro"]} for k, v in transit_pos.items()},
            "transit_houses": transits_in_houses,
            "planet_houses": natal_planet_houses,
            "houses": natal_houses,
            "asc": natal_asc,
            "mc": natal_mc,
            "aspects": aspects,
            "engine": f"Swiss Ephemeris v{swe.__version__}",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        forecast = generate_forecast(aspects, transits_in_houses, natal_pos, target_str, args.lang)
        if args.name:
            forecast = f"👤 {args.name}\n\n{forecast}"
        print(forecast)

if __name__ == "__main__":
    main()
