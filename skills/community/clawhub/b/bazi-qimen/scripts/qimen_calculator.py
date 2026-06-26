#!/usr/bin/env python3
"""Qi Men Dun Jia Calculator

Computes a Qi Men Dun Jia chart from a given date/time.
Output: JSON with 9-palace chart arrangement.
"""

import json
from datetime import datetime, timedelta

# ============================================================
# CONSTANTS
# ============================================================

TIAN_GAN = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
DI_ZHI = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]

# Nine Palaces (Jiu Gong) - Luo Shu order
# Palace positions: Kan 1, Kun 2, Zhen 3, Xun 4, Zhong 5, Qian 6, Dui 7, Gen 8, Li 9
PALACES = {
    1: {"name":"Kan","direction":"North","element":"Water","color":"White","trigram":"☵"},
    2: {"name":"Kun","direction":"Southwest","element":"Earth","color":"Black","trigram":"☷"},
    3: {"name":"Zhen","direction":"East","element":"Wood","color":"Azure","trigram":"☳"},
    4: {"name":"Xun","direction":"Southeast","element":"Wood","color":"Green","trigram":"☴"},
    5: {"name":"Zhong","direction":"Center","element":"Earth","color":"Yellow","trigram":""},
    6: {"name":"Qian","direction":"Northwest","element":"Metal","color":"White","trigram":"☰"},
    7: {"name":"Dui","direction":"West","element":"Metal","color":"Red","trigram":"☱"},
    8: {"name":"Gen","direction":"Northeast","element":"Earth","color":"White","trigram":"☶"},
    9: {"name":"Li","direction":"South","element":"Fire","color":"Purple","trigram":"☲"},
}

# Nine Stars (Jiu Xing)
JIU_XING = [
    (1, "Tian Peng"), (2, "Tian Rui"), (3, "Tian Chong"), (4, "Tian Fu"),
    (5, "Tian Qin"), (6, "Tian Xin"), (7, "Tian Zhu"), (8, "Tian Ren"), (9, "Tian Ying")
]
JIU_XING_MAP = {n: name for n, name in JIU_XING}

# Eight Doors (Ba Men) - in order
BA_MEN = ["Xiu (Rest)","Sheng (Life)","Shang (Injury)","Du (Block)","Jing (Scenery)","Si (Death)","Jing (Alarm)","Kai (Open)"]
# Door to palace mapping for Yang Dun: Rest 1, Death 2, Injury 3, Block 4, Center 5, Open 6, Alarm 7, Life 8, Scenery 9
# Door to palace mapping for Yin Dun: Rest 1, Death 2, Injury 3, Block 4, Center 5, Open 6, Alarm 7, Life 8, Scenery 9
# Actually doors rotate based on the Value Door (Zhi Shi)

# Eight Spirits (Ba Shen) - Yang Dun order
BA_SHEN_YANG = ["Zhi Fu (Value Star)","Teng She (Flying Serpent)","Tai Yin (Greater Yin)","Liu He (Six Harmonies)","Bai Hu (White Tiger)","Xuan Wu (Dark Warrior)","Jiu Di (Nine Earths)","Jiu Tian (Nine Heavens)"]
# Yin Dun order
BA_SHEN_YIN = ["Zhi Fu (Value Star)","Teng She (Flying Serpent)","Tai Yin (Greater Yin)","Liu He (Six Harmonies)","Bai Hu (White Tiger)","Xuan Wu (Dark Warrior)","Jiu Tian (Nine Heavens)","Jiu Di (Nine Earths)"]

# 24 Solar Terms with associated Yin/Yang Dun and Bureau numbers
# (term_name, yin_yang, upper/middle/lower bureau)
SOLAR_TERM_JU = [
    # Yang Dun
    ("Winter Solstice", "Yang", 1, 7, 4),
    ("Minor Cold", "Yang", 2, 8, 5),
    ("Major Cold", "Yang", 3, 9, 6),
    ("Start of Spring", "Yang", 8, 5, 2),
    ("Rain Water", "Yang", 9, 6, 3),
    ("Awakening of Insects", "Yang", 1, 7, 4),
    ("Spring Equinox", "Yang", 3, 9, 6),
    ("Pure Brightness", "Yang", 4, 1, 7),
    ("Grain Rain", "Yang", 5, 2, 8),
    ("Start of Summer", "Yang", 4, 1, 7),
    ("Grain Full", "Yang", 5, 2, 8),
    ("Grain in Ear", "Yang", 6, 3, 9),
    # Yin Dun
    ("Summer Solstice", "Yin", 9, 3, 6),
    ("Minor Heat", "Yin", 8, 2, 5),
    ("Major Heat", "Yin", 7, 1, 4),
    ("Start of Autumn", "Yin", 2, 5, 8),
    ("End of Heat", "Yin", 1, 4, 7),
    ("White Dew", "Yin", 9, 3, 6),
    ("Autumn Equinox", "Yin", 7, 1, 4),
    ("Cold Dew", "Yin", 6, 9, 3),
    ("Frost Descent", "Yin", 5, 8, 2),
    ("Start of Winter", "Yin", 6, 9, 3),
    ("Minor Snow", "Yin", 5, 8, 2),
    ("Major Snow", "Yin", 4, 7, 1),
]

# Approximate solar term dates (month, day)
SOLAR_TERM_DATES = [
    ("Winter Solstice", 12, 22), ("Minor Cold", 1, 6), ("Major Cold", 1, 20), ("Start of Spring", 2, 4),
    ("Rain Water", 2, 19), ("Awakening of Insects", 3, 6), ("Spring Equinox", 3, 21), ("Pure Brightness", 4, 5),
    ("Grain Rain", 4, 20), ("Start of Summer", 5, 6), ("Grain Full", 5, 21), ("Grain in Ear", 6, 6),
    ("Summer Solstice", 6, 22), ("Minor Heat", 7, 7), ("Major Heat", 7, 23), ("Start of Autumn", 8, 8),
    ("End of Heat", 8, 23), ("White Dew", 9, 8), ("Autumn Equinox", 9, 23), ("Cold Dew", 10, 8),
    ("Frost Descent", 10, 24), ("Start of Winter", 11, 8), ("Minor Snow", 11, 22), ("Major Snow", 12, 7),
]

# ============================================================
# HELPERS
# ============================================================

def get_hour_zhi(hour):
    idx = ((hour + 1) // 2) % 12
    return DI_ZHI[idx]

def get_day_zhi(date):
    """Calculate day branch (simplified)."""
    ref = datetime(1900, 1, 1)
    days = (date - ref).days
    return DI_ZHI[(days + 10) % 12]

def get_day_gan(date):
    ref = datetime(1900, 1, 1)
    days = (date - ref).days
    return TIAN_GAN[(days + 10) % 10]

def get_hour_gan(day_gan, hour_zhi):
    """Five Rat Escape for hour stem."""
    start_idx = {
        "Jia":0,"Ji":0,"Yi":2,"Geng":2,"Bing":4,"Xin":4,"Ding":6,"Ren":6,"Wu":8,"Gui":8
    }
    hz_idx = DI_ZHI.index(hour_zhi)
    return TIAN_GAN[(start_idx[day_gan] + hz_idx) % 10]

def get_current_solar_term(date):
    m, d = date.month, date.day
    # Find which solar term period we're in
    for i, (name, sm, sd) in enumerate(SOLAR_TERM_DATES):
        if m == sm and d >= sd:
            # Check if past any later term in same month
            found = i
            for j in range(i+1, len(SOLAR_TERM_DATES)):
                nm, nsd = SOLAR_TERM_DATES[j][1], SOLAR_TERM_DATES[j][2]
                if m == nm and d >= nsd:
                    found = j
            return SOLAR_TERM_DATES[found][0]
        elif (m == sm and d < sd):
            # Before this term, use previous
            prev = (i - 1) % 24
            return SOLAR_TERM_DATES[prev][0]
    # Winter period
    return "Winter Solstice"

def get_ju_number(solar_term_name, date):
    """Determine the bureau number based on solar term and San Yuan (Three Ternaries)."""
    # Find the solar term config
    for name, yin_yang, upper, middle, lower in SOLAR_TERM_JU:
        if name == solar_term_name:
            # Simplified San Yuan detection based on day of term period
            # A solar term is ~15 days: 1-5 upper, 6-10 middle, 11-15 lower
            # Simplified: use day of month mod 5
            day_of_term = (date.day % 15) or 15
            if day_of_term <= 5:
                return yin_yang, upper
            elif day_of_term <= 10:
                return yin_yang, middle
            else:
                return yin_yang, lower
    return "Yang", 1

# ============================================================
# MAIN CALCULATION
# ============================================================

def calculate_qimen(year, month, day, hour, minute=0):
    """Calculate complete Qi Men Dun Jia chart."""
    date = datetime(year, month, day, hour, minute)

    # 1. Determine solar term and bureau
    solar_term = get_current_solar_term(date)
    dun_type, ju_number = get_ju_number(solar_term, date)

    # 2. Sexagenary for current hour
    day_gan = get_day_gan(date)
    hour_zhi = get_hour_zhi(hour)
    hour_gan = get_hour_gan(day_gan, hour_zhi)
    shi_chen = hour_gan + hour_zhi  # Hour Stem + Hour Branch

    # 3. Build Earth Plate (Di Pan) - the base layout
    # Yang Dun: start Jia Zi Wu at palace Ju number, clockwise increasing
    # Yin Dun: start Jia Zi Wu at palace Ju number, counterclockwise decreasing
    di_pan = {}
    gan_seq = ["Wu","Ji","Geng","Xin","Ren","Gui","Ding","Bing","Yi"]
    for i, g in enumerate(gan_seq):
        if dun_type == "Yang":
            pal = ((ju_number - 1 + i) % 9) + 1
        else:
            pal = ((ju_number - 1 - i) % 9) + 1
        di_pan[pal] = g

    # 4. Determine Value Star (Zhi Fu) and Value Door (Zhi Shi)
    # Value Star = star whose original palace contains the Hour Stem's hidden stem
    # For simplicity, use the star in the palace where Hour Stem sits on earth plate
    zhi_fu_pal = None
    for pal, g in di_pan.items():
        if g == hour_gan:
            zhi_fu_pal = pal
            break
    if zhi_fu_pal is None:
        zhi_fu_pal = 1
    zhi_fu_star = JIU_XING_MAP.get(zhi_fu_pal, "Tian Peng")

    # Value Door: door originally in Value Star's palace
    zhi_shi_door = BA_MEN[(zhi_fu_pal - 1) % 8]
    zhi_shi_pal = zhi_fu_pal

    # 5. Arrange Heaven Plate (Tian Pan) - stars follow Value Star
    tian_pan = {}
    for i in range(9):
        from_pal = ((zhi_fu_pal - 1 + i) % 9) + 1
        star = JIU_XING_MAP.get(from_pal, "?")
        tian_pan[from_pal] = star

    # Stars rotate so Value Star is at the Hour Stem palace
    tian_pan_rotated = {}
    offset = zhi_fu_pal - 1  # simplified
    for pal in range(1, 10):
        src = ((pal - 1 - offset) % 9) + 1 if dun_type == "Yang" else ((pal - 1 + offset) % 9) + 1
        tian_pan_rotated[pal] = JIU_XING_MAP.get(src, "?")

    # 6. Arrange Eight Doors
    men_pan = {}
    zhi_shi_start = zhi_fu_pal
    for i, door in enumerate(BA_MEN):
        pal = ((zhi_shi_start - 1 + i) % 9) + 1
        if pal == 5:
            pal = 2  # Zhong 5 attaches to Kun 2
        men_pan[pal] = door

    # 7. Arrange Eight Spirits (Ba Shen)
    shen_pan = {}
    shen_order = BA_SHEN_YANG if dun_type == "Yang" else BA_SHEN_YIN
    for i, shen in enumerate(shen_order):
        pal = ((zhi_fu_pal - 1 + i) % 9) + 1
        shen_pan[pal] = shen

    # 8. Heaven stems in each palace (Tian Pan Gan)
    # Rotate earth plate to follow Value Star
    tian_gan = {}
    for pal in range(1, 10):
        if pal == 5:
            tian_gan[pal] = di_pan.get(5, "")
            continue
        src_pal = ((pal - zhi_fu_pal) % 9) + 1
        tian_gan[pal] = di_pan.get(src_pal, "")

    # Build result
    chart = {}
    for pal in range(1, 10):
        name = PALACES[pal]["name"]
        chart[f"Palace{pal}({name})"] = {
            "palace": pal,
            "name": name,
            "direction": PALACES[pal]["direction"],
            "element": PALACES[pal]["element"],
            "di_pan_gan": di_pan.get(pal, ""),
            "tian_pan_xing": tian_pan_rotated.get(pal, ""),
            "tian_pan_gan": tian_gan.get(pal, ""),
            "men": men_pan.get(pal, ""),
            "shen": shen_pan.get(pal, ""),
        }

    return {
        "datetime": f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}",
        "solar_term": solar_term,
        "dun_type": f"{'Yang' if dun_type == 'Yang' else 'Yin'} Dun",
        "ju_number": ju_number,
        "shi_chen": shi_chen,
        "zhi_fu": zhi_fu_star,
        "zhi_shi": zhi_shi_door,
        "chart": chart,
        "_note": "Qi Men Dun Jia chart uses a simplified algorithm. For detailed chart creation, please combine with precise solar term times and accurate San Yuan calculations."
    }

# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Qi Men Dun Jia Calculator")
    parser.add_argument("--year", type=int, default=datetime.now().year)
    parser.add_argument("--month", type=int, default=datetime.now().month)
    parser.add_argument("--day", type=int, default=datetime.now().day)
    parser.add_argument("--hour", type=int, default=datetime.now().hour)
    parser.add_argument("--minute", type=int, default=0)
    args = parser.parse_args()

    result = calculate_qimen(args.year, args.month, args.day, args.hour, args.minute)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()