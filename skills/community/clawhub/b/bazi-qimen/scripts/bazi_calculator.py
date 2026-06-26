#!/usr/bin/env python3
"""Ba Zi (Four Pillars of Destiny) Calculator

Computes a complete Ba Zi chart from solar calendar birth data.
Output: JSON with four pillars, ten gods, five elements, luck periods, and shensha.
"""

import json
import sys
from datetime import datetime

# ============================================================
# CONSTANTS
# ============================================================

TIAN_GAN = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
DI_ZHI = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]

GAN_WUXING = {"Jia":"Wood","Yi":"Wood","Bing":"Fire","Ding":"Fire","Wu":"Earth","Ji":"Earth","Geng":"Metal","Xin":"Metal","Ren":"Water","Gui":"Water"}
ZHI_WUXING = {"Zi":"Water","Chou":"Earth","Yin":"Wood","Mao":"Wood","Chen":"Earth","Si":"Fire","Wu":"Fire","Wei":"Earth","Shen":"Metal","You":"Metal","Xu":"Earth","Hai":"Water"}

GAN_YINYANG = {"Jia":"Yang","Yi":"Yin","Bing":"Yang","Ding":"Yin","Wu":"Yang","Ji":"Yin","Geng":"Yang","Xin":"Yin","Ren":"Yang","Gui":"Yin"}

ZHI_CANGGAN = {
    "Zi":["Gui"],"Chou":["Ji","Gui","Xin"],"Yin":["Jia","Bing","Wu"],"Mao":["Yi"],
    "Chen":["Yi","Wu","Gui"],"Si":["Bing","Wu","Geng"],"Wu":["Ding","Ji"],"Wei":["Ji","Ding","Yi"],
    "Shen":["Geng","Ren","Wu"],"You":["Xin"],"Xu":["Wu","Xin","Ding"],"Hai":["Ren","Jia"]
}

SHENGXIAO = {
    "Zi":"Rat","Chou":"Ox","Yin":"Tiger","Mao":"Rabbit","Chen":"Dragon","Si":"Snake",
    "Wu":"Horse","Wei":"Goat","Shen":"Monkey","You":"Rooster","Xu":"Dog","Hai":"Pig"
}

NAYIN_LIST = [
    "Sea Gold","Furnace Fire","Forest Wood","Road Earth","Sword Metal","Mountain Fire",
    "Stream Water","City Earth","Wax Metal","Willow Wood","Spring Water","Roof Earth",
    "Thunder Fire","Pine Wood","Flowing Water","Sand Metal","Mountain Fire","Plain Wood",
    "Wall Earth","Thin Gold","Lamp Fire","Sky Water","Mansion Earth","Hairpin Metal",
    "Mulberry Wood","Torrent Water","Sand Earth","Heaven Fire","Pomegranate Wood","Ocean Water"
]

# Reference: 1900-01-01 = Jia Xu (index 10 in sexagenary cycle)
REF_DATE = datetime(1900, 1, 1)
REF_INDEX = 10

# Solar term approximate start dates (month, day)
SOLAR_TERM_STARTS = [
    (2, 4),   # Li Chun (Start of Spring) -> Yin month
    (3, 6),   # Jing Zhe (Awakening of Insects) -> Mao month
    (4, 5),   # Qing Ming (Pure Brightness) -> Chen month
    (5, 6),   # Li Xia (Start of Summer) -> Si month
    (6, 6),   # Mang Zhong (Grain in Ear) -> Wu month
    (7, 7),   # Xiao Shu (Minor Heat) -> Wei month
    (8, 8),   # Li Qiu (Start of Autumn) -> Shen month
    (9, 8),   # Bai Lu (White Dew) -> You month
    (10, 8),  # Han Lu (Cold Dew) -> Xu month
    (11, 8),  # Li Dong (Start of Winter) -> Hai month
    (12, 7),  # Da Xue (Major Snow) -> Zi month
    (1, 6),   # Xiao Han (Minor Cold) -> Chou month
]

# Wu Hu Dun (Five Tiger Escape): Year Stem -> Month Stem for Yin month
WU_HU_DUN = {
    "Jia":"Bing","Ji":"Bing","Yi":"Wu","Geng":"Wu","Bing":"Geng","Xin":"Geng","Ding":"Ren","Ren":"Ren","Wu":"Jia","Gui":"Jia"
}

# Wu Shu Dun (Five Rat Escape): Day Stem -> Hour Stem for Zi hour
WU_SHU_DUN = {
    "Jia":"Jia","Ji":"Jia","Yi":"Bing","Geng":"Bing","Bing":"Wu","Xin":"Wu","Ding":"Geng","Ren":"Geng","Wu":"Ren","Gui":"Ren"
}

# ============================================================
# HELPERS
# ============================================================

def sexagenary(gan_idx, zhi_idx):
    return TIAN_GAN[gan_idx % 10] + DI_ZHI[zhi_idx % 12]

def pillar_index(gan, zhi):
    """Compute sexagenary index 0-59 from stem and branch."""
    g = TIAN_GAN.index(gan)
    z = DI_ZHI.index(zhi)
    # 60 = lcm(10, 12), 10 * 6 = 60, 12 * 5 = 60
    # pillar index = gan * 6 + offset
    offset = (z - g) % 12
    return g * 6 + offset // 2 if offset % 2 == 0 else g * 6 + offset

# ============================================================
# PILLAR CALCULATION
# ============================================================

def calc_day_pillar_idx(date):
    days = (date - REF_DATE).days
    return (REF_INDEX + days) % 60

def calc_year_pillar_idx(year):
    # 1984 = Jia Zi = index 0 (actually 1864)
    base = 1864
    return (year - base) % 60

def get_month_zhi_idx(date):
    m, d = date.month, date.day
    for i in range(12):
        st_m, st_d = SOLAR_TERM_STARTS[i]
        next_i = (i + 1) % 12
        next_m, next_d = SOLAR_TERM_STARTS[next_i]
        # Is date in this solar term period?
        if st_m < next_m or (st_m == next_m and st_d <= next_d):
            in_period = (m > st_m or (m == st_m and d >= st_d)) and \
                        (m < next_m or (m == next_m and d < next_d))
        else:
            # Wraps year end
            in_period = (m > st_m or (m == st_m and d >= st_d)) or \
                        (m < next_m or (m == next_m and d < next_d))
        if in_period:
            return (i + 2) % 12
    return 2  # Default Yin

def calc_month_gan(year_gan, month_zhi_idx):
    start_gan = WU_HU_DUN[year_gan]
    start_i = TIAN_GAN.index(start_gan)
    offset = (month_zhi_idx - 2) % 12
    return TIAN_GAN[(start_i + offset) % 10]

def calc_hour_gan(day_gan, hour_zhi_idx):
    start_gan = WU_SHU_DUN[day_gan]
    start_i = TIAN_GAN.index(start_gan)
    return TIAN_GAN[(start_i + hour_zhi_idx) % 10]

def get_hour_zhi_idx(hour):
    return ((hour + 1) // 2) % 12

# ============================================================
# TEN GODS (Shi Shen)
# ============================================================

SHISHEN_MAP = {}

def wuxing_relation(my, other):
    sheng = {"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
    ke = {"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
    if my == other: return "Same"
    if sheng.get(other) == my: return "Generates me"
    if sheng.get(my) == other: return "I generate"
    if ke.get(other) == my: return "Controls me"
    if ke.get(my) == other: return "I control"
    return "?"

def calc_shishen(day_gan, other_gan):
    rel = wuxing_relation(GAN_WUXING[day_gan], GAN_WUXING[other_gan])
    same_yy = GAN_YINYANG[day_gan] == GAN_YINYANG[other_gan]
    is_self = other_gan == day_gan

    table = {
        ("Same", True): "Bi Jian (Sibling)",
        ("Same", False): "Jie Cai (Wealth Drain)",
        ("Generates me", True): "Pian Yin (Indirect Seal)",
        ("Generates me", False): "Zheng Yin (Direct Seal)",
        ("I generate", True): "Shi Shen (Eating God)",
        ("I generate", False): "Shang Guan (Hurt Officer)",
        ("Controls me", True): "Qi Sha (Seven Killings)",
        ("Controls me", False): "Zheng Guan (Direct Officer)",
        ("I control", True): "Pian Cai (Indirect Wealth)",
        ("I control", False): "Zheng Cai (Direct Wealth)",
    }
    return table.get((rel, same_yy), "?")

# ============================================================
# SHENSHA (Divine Spirits)
# ============================================================

def calc_shensha(day_gan, day_zhi, year_zhi, month_zhi, hour_zhi):
    branches = [year_zhi, month_zhi, day_zhi, hour_zhi]
    result = []

    tianyi = {"Jia":"Chou/Wei","Wu":"Chou/Wei","Geng":"Chou/Wei","Yi":"Zi/Shen","Ji":"Zi/Shen",
               "Bing":"Hai/You","Ding":"Hai/You","Xin":"Wu/Yin","Ren":"Si/Mao","Gui":"Si/Mao"}
    for b in tianyi.get(day_gan, "").split("/"):
        if b in branches:
            result.append("Tian Yi Gui Ren (Heavenly Help Star)"); break

    wen = {"Jia":"Si","Yi":"Wu","Bing":"Shen","Ding":"You","Wu":"Shen","Ji":"You","Geng":"Hai","Xin":"Zi","Ren":"Yin","Gui":"Mao"}
    for b in wen.get(day_gan, ""):
        if b in branches:
            result.append("Wen Chang (Star of Wisdom)"); break

    taohua = {"Zi":"You","Chou":"Wu","Yin":"Mao","Mao":"Zi","Chen":"You","Si":"Wu","Wu":"Mao","Wei":"Zi","Shen":"You","You":"Wu","Xu":"Mao","Hai":"Zi"}
    for b in taohua.get(day_zhi, ""):
        if b in branches:
            result.append("Tao Hua (Peach Blossom)"); break

    yima = {"Zi":"Yin","Chou":"Hai","Yin":"Shen","Mao":"Si","Chen":"Yin","Si":"Hai","Wu":"Shen","Wei":"Si","Shen":"Yin","You":"Hai","Xu":"Shen","Hai":"Si"}
    for b in yima.get(day_zhi, ""):
        if b in branches:
            result.append("Yi Ma (Horse)"); break

    huagai = {"Zi":"Chen","Chou":"Chou","Yin":"Xu","Mao":"Wei","Chen":"Chen","Si":"Chou","Wu":"Xu","Wei":"Wei","Shen":"Chen","You":"Chou","Xu":"Xu","Hai":"Wei"}
    for b in huagai.get(day_zhi, ""):
        if b in branches:
            result.append("Hua Gai (Canopy)"); break

    yangren = {"Jia":"Mao","Yi":"Yin","Bing":"Wu","Ding":"Si","Wu":"Wu","Ji":"Si","Geng":"You","Xin":"Shen","Ren":"Zi","Gui":"Hai"}
    for b in yangren.get(day_gan, ""):
        if b in branches:
            result.append("Yang Ren (Blade)"); break

    return result

# ============================================================
# DAYUN (Major Luck)
# ============================================================

def calc_dayun(gender, year_gan, month_zhi_idx, month_gan):
    is_yang = GAN_YINYANG[year_gan] == "Yang"
    forward = is_yang if gender == "male" else not is_yang

    dayun = []
    for i in range(10):
        age = 1 + i * 10
        if forward:
            z = DI_ZHI[(month_zhi_idx + 1 + i) % 12]
            g = TIAN_GAN[(TIAN_GAN.index(WU_HU_DUN[year_gan]) + ((month_zhi_idx - 2 + 1 + i) % 12)) % 10]
        else:
            z = DI_ZHI[(month_zhi_idx - 1 - i) % 12]
            g = TIAN_GAN[(TIAN_GAN.index(WU_HU_DUN[year_gan]) + ((month_zhi_idx - 2 - 1 - i) % 12)) % 10]
        dayun.append({"age": age, "pillar": g + z, "gan": g, "zhi": z, "wuxing": GAN_WUXING[g]})
    return dayun

# ============================================================
# MAIN
# ============================================================

def calculate_bazi(year, month, day, hour, gender="male"):
    birth = datetime(year, month, day, hour)

    # Effective year: before Li Chun (Feb 4), use previous year
    eff_year = year
    if month < 2 or (month == 2 and day < 4):
        eff_year = year - 1

    year_gan = TIAN_GAN[calc_year_pillar_idx(eff_year) % 10]
    year_zhi = DI_ZHI[calc_year_pillar_idx(eff_year) % 12]
    year_pillar = year_gan + year_zhi

    day_idx = calc_day_pillar_idx(birth)
    day_gan = TIAN_GAN[day_idx % 10]
    day_zhi = DI_ZHI[day_idx % 12]
    day_pillar = day_gan + day_zhi

    month_zhi_i = get_month_zhi_idx(birth)
    month_zhi = DI_ZHI[month_zhi_i]
    month_gan = calc_month_gan(year_gan, month_zhi_i)
    month_pillar = month_gan + month_zhi

    hour_zhi_i = get_hour_zhi_idx(hour)
    hour_zhi = DI_ZHI[hour_zhi_i]
    hour_gan = calc_hour_gan(day_gan, hour_zhi_i)
    hour_pillar = hour_gan + hour_zhi

    # Hidden stems
    def canggan(z):
        return ZHI_CANGGAN.get(z, [])

    # Ten gods for each pillar (relative to day master)
    pillars_data = [
        ("Year", year_gan, year_zhi),
        ("Month", month_gan, month_zhi),
        ("Day", day_gan, day_zhi),
        ("Hour", hour_gan, hour_zhi),
    ]

    pillars_out = {}
    for label, g, z in pillars_data:
        g_wx = GAN_WUXING[g]
        z_wx = ZHI_WUXING[z]
        cg = canggan(z)
        # Shi Shen (Ten God)
        ss = calc_shishen(day_gan, g)
        pillars_out[label] = {
            "pillar": g + z,
            "gan": g, "zhi": z,
            "gan_wuxing": g_wx, "zhi_wuxing": z_wx,
            "gan_yinyang": GAN_YINYANG[g], "zhi_yinyang": "Yang" if DI_ZHI.index(z) % 2 == 0 else "Yin",
            "shishen": ss,
            "canggan": cg,
            "nayin": NAYIN_LIST[pillar_index(g, z) // 2],
            "shengxiao": SHENGXIAO.get(z, "?"),
        }

    # Five elements count
    wx = {"Wood":0,"Fire":0,"Earth":0,"Metal":0,"Water":0}
    for p in pillars_out.values():
        wx[p["gan_wuxing"]] += 1
        wx[p["zhi_wuxing"]] += 1

    # Dayun
    dayun = calc_dayun(gender, year_gan, month_zhi_i, month_gan)

    # Shensha
    shensha = calc_shensha(day_gan, day_zhi, year_zhi, month_zhi, hour_zhi)

    return {
        "birth": {"year":year,"month":month,"day":day,"hour":hour,"gender":gender,"lunar_date":None},
        "day_master": {
            "gan": day_gan, "zhi": day_zhi,
            "wuxing": GAN_WUXING[day_gan],
            "yinyang": GAN_YINYANG[day_gan],
            "shengxiao": SHENGXIAO.get(year_zhi, "?"),
        },
        "pillars": pillars_out,
        "wuxing_count": wx,
        "dayun": dayun,
        "shensha": shensha,
        "_note": "Major Luck calculation uses simplified rules. For detailed analysis, combine with precise solar term positioning."
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Ba Zi Calculator")
    parser.add_argument("--year", type=int, default=1990)
    parser.add_argument("--month", type=int, default=1)
    parser.add_argument("--day", type=int, default=1)
    parser.add_argument("--hour", type=int, default=12)
    parser.add_argument("--gender", default="male")
    args = parser.parse_args()

    result = calculate_bazi(args.year, args.month, args.day, args.hour, args.gender)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()