#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Natal Chart Calculator — Swiss Ephemeris Edition v2.0.0
Uses pyswisseph 2.10.3.2 for high-precision planetary positions and houses.

The swisseph.cp314-win_amd64.pyd file is included alongside this script.
No external dependencies or installation required — works out of the box.
Python 3.10+ required.

Usage: python natal_chart_swe.py <date DD.MM.YYYY> <time HH:MM> <city>
Example: python natal_chart_swe.py 24.04.1983 06:00 Ижевск
"""

import math
import io
import os
import sys

# ─── Load swisseph: bundled library ───
# Tries .dat first (ClawHub-compatible), then .pyd (local dev), then system install
import importlib.util as _ilu
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_swe = None
for _fname in ('swisseph.cp314-win_amd64.pyd.dat', 'swisseph.cp314-win_amd64.pyd'):
    _lib = os.path.join(_SCRIPT_DIR, _fname)
    if os.path.exists(_lib):
        _load_path = _lib
        _tmp_pyd = None
        try:
            # importlib only recognizes .pyd extension; copy .dat -> temp .pyd if needed
            if _load_path.endswith('.dat'):
                _tmp_pyd = _load_path[:-4]  # strip .dat -> .pyd
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
        print("Expected swisseph.cp314-win_amd64.pyd(.dat) in:", _SCRIPT_DIR)
        print("Or install system-wide: pip install pyswisseph")
        sys.exit(1)

swe = _swe

# Fix Windows console encoding
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SIGNS = [
    "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
    "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
]

PLANET_CONFIG = [
    (swe.SUN,      "Sun",     "☀️", "Солнце"),
    (swe.MOON,     "Moon",    "🌙", "Луна"),
    (swe.MERCURY,  "Mercury", "☿",  "Меркурий"),
    (swe.VENUS,    "Venus",   "♀",  "Венера"),
    (swe.MARS,     "Mars",    "♂",  "Марс"),
    (swe.JUPITER,  "Jupiter", "♃",  "Юпитер"),
    (swe.SATURN,   "Saturn",  "♄",  "Сатурн"),
    (swe.URANUS,   "Uranus",  "♅",  "Уран"),
    (swe.NEPTUNE,  "Neptune", "♆",  "Нептун"),
    (swe.PLUTO,    "Pluto",   "♇",  "Плутон"),
]

ASPECTS = {
    "conjunction":  {"symbol": "☌", "name": "Соединение",  "orb": 8},
    "opposition":   {"symbol": "☍", "name": "Оппозиция",   "orb": 8},
    "trine":        {"symbol": "△", "name": "Трин",        "orb": 7},
    "square":       {"symbol": "□", "name": "Квадрат",     "orb": 7},
    "sextile":      {"symbol": "✶", "name": "Секстиль",    "orb": 5},
    "semisextile":  {"symbol": "⚺", "name": "Полусекстиль","orb": 2},
    "semisquare":   {"symbol": "∠", "name": "Полуквадрат","orb": 2},
    "quincunx":     {"symbol": "⚹", "name": "Квинконс",    "orb": 2},
}

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
    "ташкент": {"lat": 41.2995, "lon": 69.2401, "tz": "Asia/Tashkent", "name": "Ташкент, Узбекистан"},
    "можга": {"lat": 56.4527, "lon": 52.2117, "tz": "Europe/Samara", "name": "Можга, Россия"},
    "лондон": {"lat": 51.5074, "lon": -0.1278, "tz": "Europe/London", "name": "Лондон, Великобритания"},
    "нью-йорк": {"lat": 40.7128, "lon": -74.0060, "tz": "America/New_York", "name": "Нью-Йорк, США"},
    "лос-анджелес": {"lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles", "name": "Лос-Анджелес, США"},
    "берлин": {"lat": 52.5200, "lon": 13.4050, "tz": "Europe/Berlin", "name": "Берлин, Германия"},
    "париж": {"lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris", "name": "Париж, Франция"},
    "токио": {"lat": 35.6762, "lon": 139.6503, "tz": "Asia/Tokyo", "name": "Токио, Япония"},
    "пекин": {"lat": 39.9042, "lon": 116.4074, "tz": "Asia/Shanghai", "name": "Пекин, Китай"},
    "дубай": {"lat": 25.2048, "lon": 55.2708, "tz": "Asia/Dubai", "name": "Дубай, ОАЭ"},
    "сингапур": {"lat": 1.3521, "lon": 103.8198, "tz": "Asia/Singapore", "name": "Сингапур"},
    "стамбул": {"lat": 41.0082, "lon": 28.9784, "tz": "Europe/Istanbul", "name": "Стамбул, Турция"},
    "тель-авив": {"lat": 32.0853, "lon": 34.7818, "tz": "Asia/Jerusalem", "name": "Тель-Авив, Израиль"},
    "мумбаи": {"lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata", "name": "Мумбаи, Индия"},
    "дели": {"lat": 28.7041, "lon": 77.1025, "tz": "Asia/Kolkata", "name": "Дели, Индия"},
    "сеул": {"lat": 37.5665, "lon": 126.9780, "tz": "Asia/Seoul", "name": "Сеул, Южная Корея"},
    "сидней": {"lat": -33.8688, "lon": 151.2093, "tz": "Australia/Sydney", "name": "Сидней, Австралия"},
    "торонто": {"lat": 43.6532, "lon": -79.3832, "tz": "America/Toronto", "name": "Торонто, Канада"},
    "чикаго": {"lat": 41.8781, "lon": -87.6298, "tz": "America/Chicago", "name": "Чикаго, США"},
    "мадрид": {"lat": 40.4168, "lon": -3.7038, "tz": "Europe/Madrid", "name": "Мадрид, Испания"},
    "рим": {"lat": 41.9028, "lon": 12.4964, "tz": "Europe/Rome", "name": "Рим, Италия"},
    "амстердам": {"lat": 52.3676, "lon": 4.9041, "tz": "Europe/Amsterdam", "name": "Амстердам, Нидерланды"},
    "стокгольм": {"lat": 59.3293, "lon": 18.0686, "tz": "Europe/Stockholm", "name": "Стокгольм, Швеция"},
    "осло": {"lat": 59.9139, "lon": 10.7522, "tz": "Europe/Oslo", "name": "Осло, Норвегия"},
    "копенгаген": {"lat": 55.6761, "lon": 12.5683, "tz": "Europe/Copenhagen", "name": "Копенгаген, Дания"},
    "хельсинки": {"lat": 60.1699, "lon": 24.9384, "tz": "Europe/Helsinki", "name": "Хельсинки, Финляндия"},
    "варшава": {"lat": 52.2297, "lon": 21.0122, "tz": "Europe/Warsaw", "name": "Варшава, Польша"},
    "прага": {"lat": 50.0755, "lon": 14.4378, "tz": "Europe/Prague", "name": "Прага, Чехия"},
    "бухарест": {"lat": 44.4268, "lon": 26.1025, "tz": "Europe/Bucharest", "name": "Бухарест, Румыния"},
    "будапешт": {"lat": 47.4979, "lon": 19.0402, "tz": "Europe/Budapest", "name": "Будапешт, Венгрия"},
    "афины": {"lat": 37.9838, "lon": 23.7275, "tz": "Europe/Athens", "name": "Афины, Греция"},
    "лиссабон": {"lat": 38.7223, "lon": -9.1393, "tz": "Europe/Lisbon", "name": "Лиссабон, Португалия"},
    "брюссель": {"lat": 50.8503, "lon": 4.3517, "tz": "Europe/Brussels", "name": "Брюссель, Бельгия"},
    "цюрих": {"lat": 47.3769, "lon": 8.5417, "tz": "Europe/Zurich", "name": "Цюрих, Швейцария"},
    "вена": {"lat": 48.2082, "lon": 16.3738, "tz": "Europe/Vienna", "name": "Вена, Австрия"},
    "кишинёв": {"lat": 47.0105, "lon": 28.8638, "tz": "Europe/Chisinau", "name": "Кишинёв, Молдова"},
    "рига": {"lat": 56.9496, "lon": 24.1052, "tz": "Europe/Riga", "name": "Рига, Латвия"},
    "вильнюс": {"lat": 54.6872, "lon": 25.2797, "tz": "Europe/Vilnius", "name": "Вильнюс, Литва"},
    "таллин": {"lat": 59.4370, "lon": 24.7536, "tz": "Europe/Tallinn", "name": "Таллин, Эстония"},
}

TZ_OFFSETS = {
    "Europe/Moscow": 3, "Europe/Samara": 4, "Asia/Yekaterinburg": 5,
    "Asia/Novosibirsk": 7, "Asia/Omsk": 6, "Asia/Barnaul": 7,
    "Asia/Irkutsk": 8, "Asia/Vladivostok": 10, "Europe/Minsk": 3,
    "Europe/Kiev": 2, "Asia/Almaty": 6, "Asia/Tashkent": 5,
    "Asia/Baku": 4, "Asia/Tbilisi": 4, "Asia/Yerevan": 4,
    "Europe/London": 0, "America/New_York": -5, "America/Los_Angeles": -8,
    "Europe/Berlin": 1, "Europe/Paris": 1, "Asia/Tokyo": 9,
    "Asia/Shanghai": 8, "Asia/Dubai": 4, "Asia/Singapore": 8,
    "Europe/Istanbul": 3, "Asia/Jerusalem": 2, "Asia/Kolkata": 5.5,
    "Asia/Seoul": 9, "Australia/Sydney": 11, "America/Toronto": -5,
    "America/Chicago": -6, "Europe/Madrid": 1, "Europe/Rome": 1,
    "Europe/Amsterdam": 1, "Europe/Stockholm": 1, "Europe/Oslo": 1,
    "Europe/Copenhagen": 1, "Europe/Helsinki": 2, "Europe/Warsaw": 1,
    "Europe/Prague": 1, "Europe/Bucharest": 2, "Europe/Budapest": 1,
    "Europe/Athens": 2, "Europe/Lisbon": 0, "Europe/Brussels": 1,
    "Europe/Zurich": 1, "Europe/Vienna": 1, "Europe/Chisinau": 2,
    "Europe/Riga": 2, "Europe/Vilnius": 2, "Europe/Tallinn": 2,
}


def find_city(city_name):
    key = city_name.strip().lower()
    if key in CITY_DB:
        return CITY_DB[key]
    for k, v in CITY_DB.items():
        if key in k or k in key:
            return v
    return None


def normalize_degrees(deg):
    return deg % 360


def deg_to_sign(deg):
    deg = normalize_degrees(deg)
    si = int(deg / 30)
    return si, deg - si * 30


def format_deg(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    return f"{d}°{m:02d}′"


def calc_all_planets(jd):
    planets = {}
    for pid, pname, psym, pname_rus in PLANET_CONFIG:
        xx, rflag = swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SPEED)
        planets[pname] = {"lon": xx[0], "speed": xx[3], "retro": xx[3] < 0}
    return planets


def calc_houses(jd, lat, lon):
    try:
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SWIEPH)
    except Exception:
        cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    return list(cusps[:12]), ascmc[0], ascmc[2]


def calc_aspects(planets):
    aspects = []
    names = list(planets.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1, p2 = names[i], names[j]
            diff = abs(planets[p1]["lon"] - planets[p2]["lon"])
            if diff > 180:
                diff = 360 - diff
            for aname, aangle in [("conjunction",0),("sextile",60),("square",90),
                                   ("trine",120),("opposition",180),("semisextile",30),
                                   ("semisquare",45),("quincunx",150)]:
                orb = ASPECTS[aname]["orb"]
                od = abs(diff - aangle)
                if od <= orb:
                    aspects.append({"p1": p1, "p2": p2, "type": aname, "orb": round(od, 2)})
                    break
    aspects.sort(key=lambda x: x["orb"])
    return aspects


def calc_natal_chart(date_str, time_str, city_name):
    from datetime import datetime, timedelta
    dt_local = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    city = find_city(city_name)
    if not city:
        return {"error": f"Город '{city_name}' не найден в базе данных"}

    lat, lon, tz = city["lat"], city["lon"], city["tz"]
    tz_off = TZ_OFFSETS.get(tz, 0)
    dt_utc = dt_local - timedelta(hours=tz_off)
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                    dt_utc.hour + dt_utc.minute / 60.0)

    planets = calc_all_planets(jd)
    houses, asc, mc = calc_houses(jd, lat, lon)
    aspects = calc_aspects(planets)

    planet_houses = {}
    for pn, pd in planets.items():
        plon = pd["lon"]
        for h in range(12):
            ne = (h + 1) % 12
            hs, he = houses[h], houses[ne]
            if hs < he:
                if hs <= plon < he:
                    planet_houses[pn] = h + 1
                    break
            else:
                if plon >= hs or plon < he:
                    planet_houses[pn] = h + 1
                    break
        else:
            planet_houses[pn] = 1

    ver = swe.__version__
    if isinstance(ver, int):
        vs = f"{ver // 1000000}.{(ver // 10000) % 100}.{ver % 10000}"
    else:
        vs = str(ver)

    return {
        "date": date_str, "time": time_str, "city": city_name,
        "city_full": city["name"], "lat": lat, "lon": lon,
        "tz": tz, "tz_offset": tz_off, "jd": jd,
        "planets": planets, "houses": houses, "asc": asc, "mc": mc,
        "aspects": aspects, "planet_houses": planet_houses,
        "engine": f"Swiss Ephemeris v{vs}",
    }


def format_chart(chart):
    if "error" in chart:
        return f"❌ Ошибка: {chart['error']}"
    L = []
    L.append(f"🌟 НАТАЛЬНАЯ КАРТА  [{chart.get('engine', 'SWE')}]")
    L.append(f"📅 Дата: {chart['date']}  ⏰ Время: {chart['time']}  📍 Место: {chart['city_full']}")
    L.append(f"🌍 {chart['lat']:.4f}°N, {chart['lon']:.4f}°E  🕐 {chart['tz']} (UTC{'+' if chart['tz_offset'] >= 0 else ''}{chart['tz_offset']})")
    L.append(f"📊 JD: {chart['jd']:.6f}")
    L.append("")
    asi, ad = deg_to_sign(chart['asc'])
    mci, mcd = deg_to_sign(chart['mc'])
    L.append(f"⬆️  ASC — {SIGNS[asi]} {format_deg(ad)}")
    L.append(f"🜨  MC  — {SIGNS[mci]} {format_deg(mcd)}")
    L.append("")
    L.append("ПЛАНЕТЫ:")
    L.append("─" * 55)
    for pid, pn, ps, pru in PLANET_CONFIG:
        pd = chart['planets'][pn]
        si, sd = deg_to_sign(pd['lon'])
        retro = " ℞" if pd['retro'] else ""
        L.append(f"  {ps} {pru:<10} — {SIGNS[si]:<10} {format_deg(sd):>8}  [{chart['planet_houses'][pn]} дом]{retro}  ({pd['speed']:+.4f}°/д)")
    L.append("")
    L.append("ДОМА:")
    L.append("─" * 55)
    hn = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
    for i, hlon in enumerate(chart['houses']):
        si, sd = deg_to_sign(hlon)
        L.append(f"  {hn[i]:>4} дом — {SIGNS[si]:<10} {format_deg(sd)}")
    L.append("")
    L.append("КРУПНЫЕ АСПЕКТЫ:")
    L.append("─" * 55)
    if chart['aspects']:
        pmap = {p[1]: p[3] for p in PLANET_CONFIG}
        for a in chart['aspects']:
            ai = ASPECTS[a['type']]
            L.append(f"  {ai['symbol']} {ai['name']}: {pmap.get(a['p1'],a['p1'])} — {pmap.get(a['p2'],a['p2'])}  (орбис: {a['orb']:.1f}°)")
    else:
        L.append("  Крупных аспектов не найдено")
    return "\n".join(L)


if __name__ == "__main__":
    import json as _json
    if len(sys.argv) < 4:
        print("Использование: python natal_chart_swe.py <дата> <время> <город> [--json]")
        print("Пример: python natal_chart_swe.py 24.04.1983 06:00 Ижевск")
        print("Пример (JSON): python natal_chart_swe.py 24.04.1983 06:00 Ижевск --json")
        sys.exit(1)
    args_main = [a for a in sys.argv[1:] if a != "--json"]
    do_json = "--json" in sys.argv[1:]
    if len(args_main) < 3:
        print("Использование: python natal_chart_swe.py <дата> <время> <город> [--json]")
        sys.exit(1)
    chart = calc_natal_chart(args_main[0], args_main[1], args_main[2])
    if do_json:
        out = dict(chart)
        out["planets"] = {k: {"lon": v["lon"], "speed": v["speed"], "retro": v["retro"]} for k, v in chart["planets"].items()}
        out["houses"] = [float(h) for h in chart["houses"]]
        out["asc"] = float(chart["asc"])
        out["mc"] = float(chart["mc"])
        out["aspects"] = [{"p1": a["p1"], "p2": a["p2"], "type": a["type"], "orb": a["orb"]} for a in chart["aspects"]]
        print(_json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(format_chart(chart))
