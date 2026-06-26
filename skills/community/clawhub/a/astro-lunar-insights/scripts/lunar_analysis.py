#!/usr/bin/env python3
"""
astro-lunar-insights: Lunar Phase & Influence Analysis
Uses Swiss Ephemeris (pyswisseph) for astronomical precision.

Calculates 9 lunar metrics:
1. Moon phases (exact dates) — New Moon, First Quarter, Full Moon, Last Quarter
2. Nearest phase dates
3. Lunar day number (tithi) and meaning
4. Transit Moon aspects to natal Moon (personal lunar cycle ~28 days)
5. Personal solar-lunar phase (Transit Moon -> Natal Sun)
6. Transit Moon through natal houses
7. Moon speed analysis
8. Illumination and distance
9. Transit Moon aspects to ALL natal planets

Outputs: text report + JSON data
Optional: --conclusion file.txt for AI-generated interpretation
"""

import swisseph as swe
import math
import json
import sys
import os
from datetime import datetime

# Import interpretations module (same directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import interpretations as interp

# ============================================================
# CONSTANTS
# ============================================================

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
SIGNS_SHORT = ['AR', 'TA', 'GE', 'CN', 'LE', 'VI',
               'LI', 'SC', 'SG', 'CP', 'AQ', 'PI']
SIGN_SYMBOLS = ['\u2648', '\u2649', '\u264A', '\u264B', '\u264C', '\u264D',
                 '\u264E', '\u264F', '\u2650', '\u2653', '\u2651', '\u2652']

SIGNS_RU = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
            'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']

ASPECT_DATA = [
    (0,   8, 'Conjunction',     True),
    (30,  6, 'Semisextile',     False),
    (45,  6, 'Semisquare',      True),
    (60,  8, 'Sextile',         False),
    (90,  8, 'Square',          True),
    (120, 8, 'Trine',           False),
    (135, 6, 'Sesquiquadrate',  True),
    (150, 8, 'Quincunx',        False),
    (180, 8, 'Opposition',      True),
]

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def format_deg(lon, lang='en'):
    """Format longitude as sign + degrees."""
    sign_idx = int(lon // 30)
    deg = lon % 30
    signs = SIGNS_RU if lang == 'ru' else SIGNS
    return f"{signs[sign_idx]} {deg:.2f}\u00b0"


def find_aspect(angle):
    """Find closest aspect to given angle."""
    best = None
    best_orb = 360
    for tgt, orb, name, maj in ASPECT_DATA:
        d = abs(angle - tgt)
        if d <= orb and d < best_orb:
            best_orb = d
            best = (tgt, orb, name, maj)
    return best


def get_house(longitude, cusps):
    """Find house number for a longitude in Placidus cusps."""
    for i in range(12):
        h_start = cusps[i]
        h_end = cusps[(i + 1) % 12]
        if h_start < h_end:
            if h_start <= longitude < h_end:
                return i + 1
        else:
            if longitude >= h_start or longitude < h_end:
                return i + 1
    return 1


def find_phase_date(start_jd, target_elongation):
    """Find Julian date when Moon elongation = target."""
    jd = start_jd
    for _ in range(50):
        sun, _ = swe.calc_ut(jd, swe.SUN)
        moon, _ = swe.calc_ut(jd, swe.MOON)
        elong = (moon[0] - sun[0]) % 360
        diff = (target_elongation - elong + 180) % 360 - 180
        if abs(diff) < 0.001:
            return jd
        jd += diff / 12.2
    return jd


def compute_natal(birth_jd, geolat, geolon):
    """Compute natal positions and house cusps."""
    positions = {}
    for pname, planet in [('Sun', swe.SUN), ('Moon', swe.MOON),
                          ('Mercury', swe.MERCURY), ('Venus', swe.VENUS),
                          ('Mars', swe.MARS), ('Jupiter', swe.JUPITER),
                          ('Saturn', swe.SATURN), ('Uranus', swe.URANUS),
                          ('Neptune', swe.NEPTUNE), ('Pluto', swe.PLUTO)]:
        lon, flags = swe.calc_ut(birth_jd, planet)
        positions[pname] = {'lon': lon[0], 'speed': lon[1], 'retro': lon[3] < 0}
    cusps, ascmc = swe.houses_ex(birth_jd, geolat, geolon, b'P')
    positions['ASC'] = {'lon': ascmc[0]}
    positions['MC'] = {'lon': ascmc[1]}
    positions['houses'] = list(cusps)
    return positions


def get_personal_phase(personal_elong):
    """Determine personal solar-lunar phase."""
    if personal_elong < 22.5 or personal_elong >= 337.5:
        return 'new_moon'
    elif personal_elong < 67.5:
        return 'crescent'
    elif personal_elong < 112.5:
        return 'first_quarter'
    elif personal_elong < 157.5:
        return 'gibbous'
    elif personal_elong < 202.5:
        return 'full_moon'
    elif personal_elong < 247.5:
        return 'disseminating'
    elif personal_elong < 292.5:
        return 'last_quarter'
    else:
        return 'balsamic'


def get_phase_name(elongation, lang='en'):
    """Get 8-phase name."""
    if lang == 'ru':
        phases = {
            (0, 22.5): 'Новолуние', (22.5, 67.5): 'Растущий серп',
            (67.5, 112.5): 'Первая четверть', (112.5, 157.5): 'Растущая выпуклая',
            (157.5, 202.5): 'Полнолуние', (202.5, 247.5): 'Убывающая выпуклая',
            (247.5, 292.5): 'Последняя четверть', (292.5, 337.5): 'Убывающий серп',
            (337.5, 360): 'Бальзамическая Луна',
        }
    else:
        phases = {
            (0, 22.5): 'New Moon', (22.5, 67.5): 'Waxing Crescent',
            (67.5, 112.5): 'First Quarter', (112.5, 157.5): 'Waxing Gibbous',
            (157.5, 202.5): 'Full Moon', (202.5, 247.5): 'Waning Gibbous',
            (247.5, 292.5): 'Last Quarter', (292.5, 337.5): 'Waning Crescent',
            (337.5, 360): 'Balsamic Moon',
        }
    for (lo, hi), name in phases.items():
        if lo <= elongation < hi:
            return name
    return 'Unknown'


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze(birth_date_str, birth_time_str, city, target_date_str=None,
            name="", lang="en", output_json=False, conclusion_file=None,
            output_file=None):
    """Full lunar analysis for a person."""

    # Parse birth date
    parts = birth_date_str.split('.')
    bday, bmonth, byear = int(parts[0]), int(parts[1]), int(parts[2])
    tparts = birth_time_str.split(':')
    bhour, bmin = int(tparts[0]), int(tparts[1])

    # City coordinates
    city_coords = {
        'izhevsk': (56.85, 53.21),
        '\u043c\u043e\u0436\u0433\u0430': (56.47, 52.21),
        'moscow': (55.75, 37.62),
        'saint petersburg': (59.93, 30.32),
        '\u043c\u043e\u0441\u043a\u0432\u0430': (55.75, 37.62),
        '\u0441\u0430\u043d\u043a\u0442-\u043f\u0435\u0442\u0435\u0440\u0431\u0443\u0440\u0433': (59.93, 30.32),
    }
    geolat, geolon = 56.85, 53.21
    for cname, coords in city_coords.items():
        if cname in city.lower():
            geolat, geolon = coords
            break

    # Julian dates
    birth_jd = swe.julday(byear, bmonth, bday, bhour + bmin / 60.0)
    if target_date_str:
        # Support both DD.MM.YYYY and YYYY-MM-DD formats
        if '.' in target_date_str:
            tparts = target_date_str.split('.')
            target_jd = swe.julday(int(tparts[2]), int(tparts[1]), int(tparts[0]), 12.0)
        elif '-' in target_date_str:
            tparts = target_date_str.split('-')
            target_jd = swe.julday(int(tparts[0]), int(tparts[1]), int(tparts[2]), 12.0)
        else:
            raise ValueError('target-date format must be DD.MM.YYYY or YYYY-MM-DD')
    else:
        import time
        now = time.gmtime()
        target_jd = swe.julday(now[0], now[1], now[2], now[3] + now[4] / 60.0)

    # Natal chart
    natal = compute_natal(birth_jd, geolat, geolon)
    house_cusps = natal['houses']

    # Transit positions
    sun, _ = swe.calc_ut(target_jd, swe.SUN)
    moon, _ = swe.calc_ut(target_jd, swe.MOON)
    transit_sun_lon = sun[0]
    transit_moon_lon = moon[0]
    moon_dist_au = moon[2]

    # Moon speed (centered difference)
    moon_prev, _ = swe.calc_ut(target_jd - 0.5, swe.MOON)
    moon_next, _ = swe.calc_ut(target_jd + 0.5, swe.MOON)
    transit_moon_speed = (moon_next[0] - moon_prev[0]) % 360
    if transit_moon_speed > 180:
        transit_moon_speed -= 360
    transit_moon_speed = abs(transit_moon_speed)

    elongation = (transit_moon_lon - transit_sun_lon) % 360
    illumination = (1 - math.cos(math.radians(elongation))) / 2 * 100
    current_phase_name = get_phase_name(elongation, lang)

    # Lunar day
    lunar_day = int(elongation / 12.19) + 1
    if lunar_day > 30:
        lunar_day = 30

    # Transit Moon -> Natal Moon
    natal_moon = natal['Moon']['lon']
    diff_nm = abs(transit_moon_lon - natal_moon)
    if diff_nm > 180:
        diff_nm = 360 - diff_nm
    asp_nm = find_aspect(diff_nm)

    # Personal phase
    natal_sun = natal['Sun']['lon']
    personal_elong = (transit_moon_lon - natal_sun + 360) % 360
    personal_phase_key = get_personal_phase(personal_elong)

    # Transit Moon house
    moon_house = get_house(transit_moon_lon, house_cusps)

    # Perigee/Apogee
    moon_next_d, _ = swe.calc_ut(target_jd + 1, swe.MOON)
    approaching = "perigee" if moon_dist_au < moon_next_d[2] else "apogee"

    # Transit Moon aspects to all natal planets
    all_aspects = []
    for pname in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
                  'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']:
        plon = natal[pname]['lon']
        diff = abs(transit_moon_lon - plon)
        if diff > 180:
            diff = 360 - diff
        asp = find_aspect(diff)
        if asp:
            angle, orb, aname, major = asp
            orb_val = abs(diff - angle)
            all_aspects.append({
                'transit': 'Moon', 'natal': pname,
                'aspect': aname, 'major': major,
                'orb': round(orb_val, 2),
                'natal_lon': round(plon, 4),
                'natal_retro': natal[pname]['retro'],
            })

    # Nearest phases
    nearest_phases = {}
    phase_names_list = ['New Moon', 'First Quarter', 'Full Moon', 'Last Quarter']
    if lang == 'ru':
        phase_names_list = ['Новолуние', 'Первая четверть', 'Полнолуние', 'Последняя четверть']
    for ptarget, pname in zip([0, 90, 180, 270], phase_names_list):
        jd = find_phase_date(target_jd, ptarget)
        y, m, d, h = swe.revjul(jd)
        days_diff = jd - target_jd
        nearest_phases[pname] = {
            'date': f"{d:02d}.{m:02d}.{y}",
            'hours_utc': round(h, 3),
            'days_diff': round(days_diff, 1),
        }

    # Planets in Moon's house
    planets_in_house = []
    for pname in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
                  'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']:
        plon = natal[pname]['lon']
        if get_house(plon, house_cusps) == moon_house:
            planets_in_house.append({
                'name': pname, 'lon': round(plon, 4),
                'retro': natal[pname]['retro'],
            })

    # Moon speed description
    if transit_moon_speed > 15:
        speed_desc = "Very fast (near perigee) \u2014 events move quickly, less depth" if lang != 'ru' else "\u041e\u0447\u0435\u043d\u044c \u0431\u044b\u0441\u0442\u0440\u0430\u044f (\u0440\u044f\u0434\u043e\u043c \u0441 \u043f\u0435\u0440\u0438\u0433\u0435\u0435\u043c) \u2014 \u0441\u043e\u0431\u044b\u0442\u0438\u044f \u0431\u044b\u0441\u0442\u0440\u043e, \u043c\u0435\u043d\u044c\u0448\u0435 \u0433\u043b\u0443\u0431\u0438\u043d\u044b"
    elif transit_moon_speed > 13.5:
        speed_desc = "Fast \u2014 rapid emotional shifts, matters progress" if lang != 'ru' else "\u0411\u044b\u0441\u0442\u0440\u0430\u044f \u2014 \u0431\u044b\u0441\u0442\u0440\u044b\u0435 \u044d\u043c\u043e\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u044b"
    elif transit_moon_speed > 11.5:
        speed_desc = "Normal \u2014 balanced emotional processing" if lang != 'ru' else "\u041d\u043e\u0440\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u2014 \u0441\u0431\u0430\u043b\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u044d\u043c\u043e\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430"
    elif transit_moon_speed > 10:
        speed_desc = "Slow \u2014 lingering feelings, deeper impact" if lang != 'ru' else "\u041c\u0435\u0434\u043b\u0435\u043d\u043d\u0430\u044f \u2014 \u0437\u0430\u0442\u044f\u0436\u043d\u044b\u0435 \u0447\u0443\u0432\u0441\u0442\u0432\u0430, \u0433\u043b\u0443\u0431\u0436\u0435 \u0432\u043b\u0438\u044f\u043d\u0438\u0435"
    else:
        speed_desc = "Very slow (near apogee) \u2014 prolonged emotional intensity" if lang != 'ru' else "\u041e\u0447\u0435\u043d\u044c \u043c\u0435\u0434\u043b\u0435\u043d\u043d\u0430\u044f (\u0440\u044f\u0434\u043e\u043c \u0441 \u0430\u043f\u043e\u0433\u0435\u0435\u043c) \u2014 \u0437\u0430\u0442\u044f\u0436\u043d\u0430\u044f \u044d\u043c\u043e\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c"

    # Approaching text
    if lang == 'ru':
        approaching_text = "\u043f\u0440\u0438\u0431\u043b\u0438\u0436\u0430\u0435\u0442\u0441\u044f \u043a " + ("\u043f\u0435\u0440\u0438\u0433\u0435\u044e" if approaching == "perigee" else "\u0430\u043f\u043e\u0433\u0435\u044e")
    else:
        approaching_text = f"approaching {approaching}"

    # ============================================================
    # BUILD JSON DATA
    # ============================================================

    result = {
        'name': name,
        'birth_date': birth_date_str,
        'birth_time': birth_time_str,
        'birth_city': city,
        'target_date': target_date_str or datetime.now().strftime('%d.%m.%Y'),
        'lang': lang,
        '_natal': natal,
        'moon_phase': {
            'name': current_phase_name,
            'elongation': round(elongation, 4),
            'illumination': round(illumination, 2),
            'distance_au': round(moon_dist_au, 6),
            'distance_km': round(moon_dist_au * 149597870.7),
        },
        'nearest_phases': nearest_phases,
        'lunar_day': {
            'number': lunar_day,
        },
        'transit_moon': {
            'lon': round(transit_moon_lon, 4),
            'sign': SIGNS[int(transit_moon_lon // 30)],
            'sign_ru': SIGNS_RU[int(transit_moon_lon // 30)],
            'speed': round(transit_moon_speed, 4),
            'approaching': approaching,
        },
        'transit_moon_to_natal_moon': {
            'natal_moon_lon': round(natal_moon, 4),
            'natal_moon_sign': SIGNS[int(natal_moon // 30)],
            'natal_moon_sign_ru': SIGNS_RU[int(natal_moon // 30)],
            'transit_moon_sign': SIGNS[int(transit_moon_lon // 30)],
            'transit_moon_sign_ru': SIGNS_RU[int(transit_moon_lon // 30)],
            'aspect': asp_nm[2] if asp_nm else None,
            'orb': round(abs(diff_nm - asp_nm[0]), 2) if asp_nm else None,
        },
        'personal_phase': {
            'key': personal_phase_key,
            'elongation': round(personal_elong, 2),
        },
        'transit_moon_house': {
            'house': moon_house,
            'natal_planets_in_house': planets_in_house,
        },
        'moon_speed': {
            'speed': round(transit_moon_speed, 4),
            'description': speed_desc,
            'approaching': approaching_text,
        },
        'transit_moon_aspects': all_aspects,
        'engine': 'Swiss Ephemeris v20230604',
    }

    # ============================================================
    # LOAD CONCLUSION (AI or autonomous)
    # ============================================================

    conclusion = None
    if conclusion_file and os.path.exists(conclusion_file):
        with open(conclusion_file, 'r', encoding='utf-8') as f:
            conclusion = json.load(f)
    else:
        # Generate autonomous interpretations
        conclusion = interp.generate_metric_summaries(result, lang)
        conclusion['_autonomous'] = True

    result['conclusion'] = conclusion

    # ---- JSON OUTPUT ----
    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    if output_json:
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as _f:
                _f.write(json_str)
                _f.write('\n')
        else:
            print(json_str)
        return result

    # ---- TEXT OUTPUT ----
    R = lang == 'ru'
    def h1(s): print(f"\n{'=' * 60}\n  {s}\n{'=' * 60}\n")
    def h2(s): print(f"\n{s}\n{'-' * 40}")
    def line(s): print(f"   {s}")
    def h2(s): print(f"\n{s}\n{'-' * 40}")
    def line(s): print(f"   {s}")

    title = "\u041b\u0423\u041d\u041d\u042b\u0419 \u0410\u041d\u0410\u041b\u0418\u0417" if R else "LUNAR ANALYSIS"
    h1(f"{title}: {name}")
    line(f"{birth_date_str} {birth_time_str} {city}")
    line(f"{target_date_str or ('\u0441\u0435\u0433\u043e\u0434\u043d\u044f' if R else 'today')}")
    if conclusion_file:
        line(f"AI conclusion: {conclusion_file}")
    elif conclusion.get('_autonomous'):
        line("\u0410\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u0430\u044f \u0438\u043d\u0442\u0435\u0440\u043f\u0440\u0435\u0442\u0430\u0446\u0438\u044f" if R else "Autonomous interpretation")

    # 1. Moon phase
    h2("1. " + ("\u0422\u0415\u041a\u0423\u0429\u0410\u042f \u0424\u0410\u0417\u0410 \u041b\u0423\u041d\u042b" if R else "CURRENT MOON PHASE"))
    line(f"{current_phase_name} | {elongation:.1f}\u00b0 | {illumination:.1f}%")
    line(f"{moon_dist_au * 149597870.7:.0f} km")
    if conclusion and 'moon_phase' in conclusion:
        line("")
        line(conclusion['moon_phase']['interpretation']['description'][:200])

    # 2. Nearest phases
    h2("2. " + ("\u0411\u041b\u0418\u0416\u0410\u0419\u0428\u0418\u0415 \u0424\u0410\u0417\u042b" if R else "NEAREST PHASES"))
    for pn, pd in nearest_phases.items():
        direction = ("\u0447\u0435\u0440\u0435\u0437" if R else "in") if pd['days_diff'] > 0 else ("\u043d\u0430\u0437\u0430\u0434" if R else "ago")
        line(f"{pn}: {pd['date']} ({abs(pd['days_diff']):.1f}d {direction})")

    # 3. Lunar day
    h2("3. " + ("\u041b\u0423\u041d\u041d\u042b\u0419 \u0414\u0415\u041d\u042c (\u0422\u0418\u0422\u0425\u0418)" if R else "LUNAR DAY (TITHI)"))
    ld_interp = interp.interpret_lunar_day(lunar_day, lang)
    line(f"{lunar_day}/30")
    line(ld_interp)

    # 4. Transit Moon -> Natal Moon
    h2("4. " + ("\u0422\u0420\u0410\u041d\u0417\u0418\u0422\u041d\u0410\u042f \u041b\u0423\u041d\u0410 \u041a \u041d\u0410\u0422\u0410\u041b\u042c\u041d\u041e\u0419" if R else "TRANSIT MOON TO NATAL MOON"))
    line(f"Natal: {format_deg(natal_moon, lang)} | Transit: {format_deg(transit_moon_lon, lang)}")
    if asp_nm:
        angle, orb, aname, major = asp_nm
        orb_val = abs(diff_nm - angle)
        line(f"{aname} (orb {orb_val:.1f}\u00b0)")
        if conclusion and 'transit_moon_to_natal_moon' in conclusion and conclusion['transit_moon_to_natal_moon']['interpretation']:
            interp_text = conclusion['transit_moon_to_natal_moon']['interpretation']
            # Word wrap
            words = interp_text.split()
            l = ""
            for w in words:
                if len(l) + len(w) > 70:
                    line(l)
                    l = w + " "
                else:
                    l += w + " "
            if l.strip():
                line(l)

    # 5. Personal phase
    h2("5. " + ("\u041f\u0415\u0420\u0421\u041e\u041d\u0410\u041b\u042c\u041d\u0410\u042f \u0421\u041e\u041b\u041d\u0415\u0427\u041d\u041e-\u041b\u0423\u041d\u041d\u0410\u042f \u0424\u0410\u0417\u0410" if R else "PERSONAL SOLAR-LUNAR PHASE"))
    line(f"Natal Sun: {format_deg(natal_sun, lang)} | Transit Moon: {format_deg(transit_moon_lon, lang)}")
    line(f"{personal_elong:.1f}\u00b0")
    if conclusion and 'personal_phase' in conclusion:
        pp = conclusion['personal_phase']['interpretation']
        line(f"{pp[0]}: {pp[1][:200]}")

    # 6. Transit Moon house
    h2("6. " + ("\u0422\u0420\u0410\u041d\u0417\u0418\u0422\u041d\u0410\u042f \u041b\u0423\u041d\u0410 \u0412 \u041d\u0410\u0422\u0410\u041b\u042c\u041d\u041e\u041c \u0414\u041e\u041c\u0415" if R else "TRANSIT MOON IN NATAL HOUSE"))
    line(f"House {moon_house}")
    if conclusion and 'transit_moon_house' in conclusion:
        line(conclusion['transit_moon_house']['interpretation'][:200])
    if planets_in_house:
        pnames = ", ".join([p['name'] for p in planets_in_house])
        line(("\u041d\u0430\u0442\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u043b\u0430\u043d\u0435\u0442\u044b: " if R else "Natal planets: ") + pnames)

    # 7. Moon speed
    h2("7. " + ("\u0421\u041a\u041e\u0420\u041e\u0421\u0422\u042c \u041b\u0423\u041d\u042b" if R else "MOON SPEED"))
    line(f"{transit_moon_speed:.2f}\u00b0/" + ("\u0434\u0435\u043d\u044c" if R else "day"))
    line(speed_desc)
    line(approaching_text)

    # 8. All aspects
    h2("8. " + ("\u0410\u0421\u041f\u0415\u041a\u0422\u042b \u041a\u041e \u0412\u0421\u0415\u041c \u041f\u041b\u0410\u041d\u0415\u0422\u0410\u041c" if R else "ASPECTS TO ALL PLANETS"))
    for a in all_aspects:
        marker = "*" if a['major'] else " "
        retro = " R" if a['natal_retro'] else ""
        line(f"  {marker} Moon {a['aspect']:15s} {a['natal']:8s} {format_deg(a['natal_lon'], lang)}{retro} (orb {a['orb']:.1f}\u00b0)")

    # 9. Conclusion
    if conclusion:
        h2("9. " + ("\u0417\u0410\u041a\u041b\u042e\u0427\u0415\u041d\u0418\u0415" if R else "CONCLUSION"))
        if conclusion.get('_autonomous'):
            # Print autonomous summary
            summary = conclusion.get('summary', {})
            line(("\u042d\u043d\u0435\u0440\u0433\u0438\u044f \u0446\u0438\u043a\u043b\u0430: " if R else "Cycle energy: ") + summary.get('cycle_energy', ''))
            line(("\u0418\u043d\u0442\u0435\u043d\u0441\u0438\u0432\u043d\u043e\u0441\u044c: " if R else "Intensity: ") + summary.get('intensity', ''))
            line("")
            # Print each metric's interpretation
            for key in ['moon_phase', 'transit_moon_to_natal_moon', 'personal_phase', 'transit_moon_house', 'moon_speed']:
                if key in conclusion and conclusion[key] and conclusion[key].get('interpretation'):
                    ci = conclusion[key]['interpretation']
                    if isinstance(ci, dict):
                        desc = ci.get('description', '')
                    elif isinstance(ci, tuple):
                        desc = ci[1] if len(ci) > 1 else ci[0]
                    else:
                        desc = str(ci)
                    if desc:
                        # Word wrap
                        words = desc.split()
                        l = ""
                        for w in words:
                            if len(l) + len(w) > 70:
                                line(l)
                                l = w + " "
                            else:
                                l += w + " "
                        if l.strip():
                            line(l)
                        line("")
        elif isinstance(conclusion, dict) and 'overall' in conclusion:
            # AI conclusion
            overall = conclusion['overall']
            words = overall.split()
            l = ""
            for w in words:
                if len(l) + len(w) > 70:
                    line(l)
                    l = w + " "
                else:
                    l += w + " "
            if l.strip():
                line(l)

            # Per-metric conclusions
            if 'metrics' in conclusion:
                line("")
                for mkey, mtext in conclusion['metrics'].items():
                    line(f"  {mkey}: {mtext[:150]}")

    print(f"\n{'=' * 60}")
    print(f"  * = " + ("\u043c\u0430\u0436\u043e\u0440\u043d\u044b\u0439 \u0430\u0441\u043f\u0435\u043a\u0442" if R else "major aspect"))
    print(f"  R = " + ("\u0440\u0435\u0442\u0440\u043e\u0433\u0440\u0430\u0434" if R else "retrograde"))
    print(f"{'=' * 60}")

    return result


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python lunar_analysis.py DD.MM.YYYY HH:MM City [target-date] [--lang ru/en] [--name Name] [--json] [--output file.json] [--conclusion file.json]")
        sys.exit(1)

    target = None
    name = ""
    lang = "en"
    as_json = False
    conclusion_file = None
    output_file = None

    args = sys.argv[1:]
    positional = []
    i = 0
    while i < len(args):
        if args[i] == '--lang' and i + 1 < len(args):
            lang = args[i + 1]
            i += 2
        elif args[i] == '--name' and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] == '--json':
            as_json = True
            i += 1
        elif args[i] == '--conclusion' and i + 1 < len(args):
            conclusion_file = args[i + 1]
            i += 2
        elif args[i] == '--output' and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == '--target-date' and i + 1 < len(args):
            target = args[i + 1]
            i += 2
        else:
            positional.append(args[i])
            i += 1

    # Positional target date (4th arg) still supported for backward compat
    if target is None and len(positional) >= 4:
        target = positional[3]

    analyze(positional[0], positional[1], positional[2], target, name, lang, as_json, conclusion_file, output_file)
