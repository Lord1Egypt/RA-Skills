#!/usr/bin/env python3
"""
Financial Astrology v4 — Chiêm Tinh Tài Chính (Day Trading Focus M15/H1)
=========================================================================
Features:
- Moon position, Nakshatra, Pada, House
- Moon-Planet combinations (Chandra-Mangal, Vish Yoga, Grahan Yoga, etc.)
- Moon aspects (tất cả góc chiếu tác động lên Moon)
- Combustion detection + Cazimi
- All major aspects between planets
- Nakshatra trading quality (favorable/unfavorable)
- Gandanta detection
- Sector-specific analysis (Gold, Bitcoin)
- Day trading signal summary
- 🆕 PLANETARY HOURS (Giờ Hora) — Chaldean order, sunrise/sunset based
  Location: Japan (Asia/Tokyo, UTC+9) — default lat/lon for Hekinan

System: Sidereal (Nirayana) - Ayanamsa Lahiri
House System: Whole Sign (Vedic)
"""

import sys
import argparse
import json
import swisseph as swe
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


# ============================================================
# DỮ LIỆU
# ============================================================

# ============================================================
# PLANETARY HOURS (Giờ Hora) — Chaldean Order
# ============================================================
# Thứ tự Chaldean: Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon
# (theo tốc độ biểu kiến chậm → nhanh: Saturn 29n, Jupiter 12n, Mars 2n, Sun 1n, Venus 220n, Mercury 88n, Moon 27n)

CHALDEAN_ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']

# Hành tinh chủ quản mỗi ngày trong tuần
# Python weekday(): Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
DAY_LORDS = {
    0: 'Moon',    # Monday
    1: 'Mars',    # Tuesday
    2: 'Mercury', # Wednesday
    3: 'Jupiter', # Thursday
    4: 'Venus',   # Friday
    5: 'Saturn',  # Saturday
    6: 'Sun',     # Sunday
}

DAY_NAMES_VN = {
    0: 'Thứ Hai', 1: 'Thứ Ba', 2: 'Thứ Tư', 3: 'Thứ Năm',
    4: 'Thứ Sáu', 5: 'Thứ Bảy', 6: 'Chủ Nhật',
}

# Ý nghĩa Giờ Hora cho Trading
HORA_TRADING = {
    'Sun': {
        'emoji': '☀️',
        'name': 'Giờ Mặt Trời',
        'bias': 'BULLISH — Stable uptrend',
        'assets': 'Vàng (XAU), Blue-chip stocks, Government bonds',
        'strategy': 'Buy dips, hold positions, Gold mạnh',
        'warning': 'Tránh overconfidence, không FOMO tại đỉnh',
    },
    'Moon': {
        'emoji': '🌙',
        'name': 'Giờ Mặt Trăng',
        'bias': 'NEUTRAL → Cảm xúc cao',
        'assets': 'Bạc (XAG), Consumer stocks, Real estate, Liquidity cao',
        'strategy': 'Watch sentiment shifts, quick in-out, tight SL',
        'warning': 'Cảm xúc thị trường biến động, dễ false breakout',
    },
    'Mercury': {
        'emoji': '☿️',
        'name': 'Giờ Thủy Tinh',
        'bias': 'HIGH VOLATILITY — Whipsaws',
        'assets': 'Tech stocks, IT, Telecom, Crypto, Brokerage',
        'strategy': 'Scalping, quick trades, range trading',
        'warning': 'Nhiều false signals, không hold qua đêm, tight SL',
    },
    'Venus': {
        'emoji': '♀️',
        'name': 'Giờ Kim Tinh',
        'bias': 'BULLISH — Risk-on',
        'assets': 'Vàng (XAU), Luxury stocks, Consumer, Art, Beauty',
        'strategy': 'Buy dips, trend following, Gold/XAU tốt',
        'warning': 'Tránh over-leverage khi market quá lạc quan',
    },
    'Mars': {
        'emoji': '♂️',
        'name': 'Giờ Hoả Tinh',
        'bias': 'AGGRESSIVE — High volatility',
        'assets': 'Defense, Energy, Metals, Real estate, Oil/Gas',
        'strategy': 'Momentum trading, breakout trades, aggressive entry',
        'warning': '⚠️ Rủi ro CAO — Dễ panic sell, tight SL bắt buộc',
    },
    'Jupiter': {
        'emoji': '♃',
        'name': 'Giờ Mộc Tinh',
        'bias': 'BULLISH — Expansion',
        'assets': 'Banking, Finance, Education, FMCG, Index funds',
        'strategy': 'Position trading, swing trade, buy and hold',
        'warning': 'Tránh over-optimism, luôn có exit plan',
    },
    'Saturn': {
        'emoji': '♄',
        'name': 'Giờ Thổ Tinh',
        'bias': 'BEARISH → Conservative',
        'assets': 'Infrastructure, Mining, Cement, Utilities, Bonds',
        'strategy': 'Sell on rise, reduce position, cash is king, hedge',
        'warning': '⚠️ Market chậm, range-bound — tránh fresh long',
    },
}

# Hành tinh chủ quản mỗi giờ Hora — ý nghĩa cho Vàng (XAU/USD)
HORA_GOLD = {
    'Sun': '☀️ Vàng mạnh — Safe haven demand ổn định, uptrend',
    'Moon': '🌙 Vàng biến động — Theo cảm xúc, watch silver correlation',
    'Mercury': '☿️ Vàng sideways — Whipsaws, range trading',
    'Venus': '♀️ Vàng TỐT — Risk-on, Gold hấp dẫn, buy dips',
    'Mars': '♂️ Vàng biến động MẠNH — Có thể spike lên/xuống bất ngờ',
    'Jupiter': '♃ Vàng tăng — Expansion, banking sector hỗ trợ',
    'Saturn': '♄ Vàng yếu/chậm — Correction, consolidation',
}

# Hành tinh chủ quản mỗi giờ Hora — ý nghĩa cho Bitcoin (BTC/USD)
HORA_BTC = {
    'Sun': '☀️ BTC ổn định — Institutional interest',
    'Moon': '🌙 BTC biến động — Retail sentiment shifts',
    'Mercury': '☿️ BTC HOẠT ĐỘNG MẠNH — Trading volume cao, good for scalping',
    'Venus': '♀️ BTC bullish — Risk appetite cao, altcoin season potential',
    'Mars': '♂️ BTC AGGRESSIVE — Breakout hoặc crash, rất biến động',
    'Jupiter': '♃ BTC tăng — Expansion, adoption news',
    'Saturn': '♄ BTC chậm — Consolidation, accumulation phase',
}

NAKSHATRA_27 = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu",
    "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus",
    "Sun", "Moon", "Mars", "Rahu", "Jupiter",
    "Saturn", "Mercury",
]

NAKSHATRA_SYMBOLS = [
    "🐴", "🔥", "🔪", "🐂", "🦌",
    "🌊", "🏠", "🌸", "🐍", "👑",
    "🛏️", "🛏️", "✋", "🎨", "🌱",
    "🎯", "🌟", "🪖", "🌿", "🌊",
    "👑", "🔥", "🐘", "🐍",
    "🔥", "🐘", "🐟",
]

# Nakshatra trading quality
NAKSHATRA_TRADE = {
    "Ashwini": ("✅ Tốt", "Intraday, quick trades"),
    "Pushya": ("✅✅ Rất tốt", "Investment, wealth building"),
    "Rohini": ("✅ Tốt", "Profit-oriented, growth"),
    "Uttara Phalguni": ("✅ Tốt", "Strategic planning"),
    "Hasta": ("✅ Tốt", "Swing trading, precision"),
    "Ardra": ("❌ Tránh", "Emotional volatility"),
    "Mula": ("❌ Tránh", "Destructive energy"),
    "Ashlesha": ("❌ Tránh", "Hidden motives, confusion"),
}

ZODIAC_SIGNS = [
    "♈ Bạch Dương", "♉ Kim Ngưu", "♊ Song Tử",
    "♋ Cự Giải", "♌ Sư Tử", "♍ Xử Nữ",
    "♎ Thiên Bình", "♏ Thiên Yết", "♐ Nhân Mã",
    "♑ Ma Kết", "♒ Bảo Bình", "♓ Song Ngư",
]

ELEMENT_NAMES = ["Lửa", "Đất", "Khí", "Nước"]
QUALITY_NAMES_VN = ["Cơ động", "Bền vững", "Biến đổi"]

HOUSE_MEANINGS = {
    1: "Lagna - Bản thân, khởi đầu",
    2: "Dhana - Tài chính, tích lũy",
    3: "Sahaja - Giao tiếp, nỗ lực",
    4: "Sukha - Nhà cửa, nền tảng",
    5: "Putra - Đầu cơ, may mắn",
    6: "Shatru - Xung đột, dịch vụ",
    7: "Kalatra - Đối tác, kinh doanh",
    8: "Randhara - Biến cố, nghiên cứu",
    9: "Dharma - May mắn, đạo đức",
    10: "Karma - Sự nghiệp, danh tiếng",
    11: "Labha - Lợi nhuận, thu nhập",
    12: "Vyaya - Thất thoát, chi tiêu",
}

BODIES = {
    'Mặt Trăng': swe.MOON,
    'Mặt Trời': swe.SUN,
    'Thủy': swe.MERCURY,
    'Kim': swe.VENUS,
    'Hoả': swe.MARS,
    'Mộc': swe.JUPITER,
    'Thổ': swe.SATURN,
    'Rahu': swe.TRUE_NODE,
}

BODY_NAMES = {
    'Mặt Trăng': '🌙 Mặt Trăng (Chandra)',
    'Mặt Trời': '☀️ Mặt Trời (Surya)',
    'Thủy': '☿️ Thủy Tinh (Budha)',
    'Kim': '♀️ Kim Tinh (Shukra)',
    'Hoả': '♂️ Hoả Tinh (Mangala)',
    'Mộc': '♃ Mộc Tinh (Guru)',
    'Thổ': '♄ Thổ Tinh (Shani)',
    'Rahu': '🐉 Rahu (North Node)',
    'Ketu': '🔻 Ketu (South Node)',
    'Thiên Vương': '⛧ Thiên Vương (Uranus)',
    'Hải Vương': '♆ Hải Vương (Neptune)',
    'Diêm Vương': '♇ Diêm Vương (Pluto)',
}

# SHORT names for display
SHORT_NAMES = {
    'Mặt Trăng': 'Moon', 'Mặt Trời': 'Sun', 'Thủy': 'Mercury',
    'Kim': 'Venus', 'Hoả': 'Mars', 'Mộc': 'Jupiter', 'Thổ': 'Saturn',
    'Rahu': 'Rahu', 'Ketu': 'Ketu',
    'Thiên Vương': 'Uranus', 'Hải Vương': 'Neptune', 'Diêm Vương': 'Pluto',
}

# Aspects
ASPECTS = {
    'Conjunction': {'angle': 0, 'orb': 8, 'symbol': '☌', 'type': 'major'},
    'Sextile': {'angle': 60, 'orb': 6, 'symbol': '⚹', 'type': 'major'},
    'Square': {'angle': 90, 'orb': 7, 'symbol': '□', 'type': 'major'},
    'Trine': {'angle': 120, 'orb': 8, 'symbol': '△', 'type': 'major'},
    'Opposition': {'angle': 180, 'orb': 8, 'symbol': '☍', 'type': 'major'},
    'Quincunx': {'angle': 150, 'orb': 3, 'symbol': '⚻', 'type': 'minor'},
    'Semi-Square': {'angle': 45, 'orb': 2.5, 'symbol': '∠', 'type': 'minor'},
    'Sesquiquadrate': {'angle': 135, 'orb': 2.5, 'symbol': '⚼', 'type': 'minor'},
}

# Combustion orbs — Quy tắc của Anh Minh (nghiêm ngặt hơn Vedic standard)
# Nguồn: COMBUSTION_RULES.md
COMBUST_ORBS = {
    'Thủy': 2, 'Kim': 5, 'Hoả': 10, 'Mộc': 10, 'Thổ': 10,
}
CAZIMI_ORB = 0.2833  # 17 phút = 0.2833°

# Nakshatra span (360° / 27 nakshatras)
NAKSHATRA_SPAN = 360.0 / 27.0  # 13°20'

# ============================================================
# DASHA DATA (Vimshottari Dasha - 120 năm chu kỳ)
# ============================================================

DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
    'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17,
}

DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

DASHA_MEANINGS = {
    'Ketu': "🔻 Tâm linh, nghiên cứu sâu, tách rời vật chất, giải thoát",
    'Venus': "♀️ Tài chính, nghệ thuật, tình yêu, tiện nghi, sắc đẹp",
    'Sun': "☀️ Danh tiếng, sự nghiệp, quyền lực, cha mẹ, lãnh đạo",
    'Moon': "🌙 Cảm xúc, gia đình, nhà cửa, công chúng, trực giác",
    'Mars': "♂️ Năng lượng, xung đột, bất động sản, kỹ thuật, thể thao",
    'Rahu': "🐉 Tham vọng, đột phá, rủi ro, ngoại quốc, công nghệ",
    'Jupiter': "♃ May mắn, học vấn, tài chính, mở rộng, trí tuệ",
    'Saturn': "♄ Kỷ luật, thử thách, chậm nhưng bền, nghiệp quả",
    'Mercury': "☿️ Giao tiếp, kinh doanh, học thuật, nghệ thuật, phân tích",
}


# ============================================================
# HÀM TIỆN ÍCH
# ============================================================

def angle_diff(a, b):
    diff = abs(a - b) % 360
    return min(diff, 360 - diff)

def get_nakshatra(longitude):
    span = 360.0 / 27.0
    pada_span = span / 4.0
    idx = int(longitude / span) % 27
    pos = longitude % span
    pada = int(pos / pada_span) + 1
    return idx, NAKSHATRA_27[idx], pada, NAKSHATRA_LORDS[idx], NAKSHATRA_SYMBOLS[idx]

def get_house(planet_lon, asc_lon):
    asc_sign = int(asc_lon / 30) % 12
    p_sign = int(planet_lon / 30) % 12
    return (p_sign - asc_sign + 12) % 12 + 1

def decimal_to_dms(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    s = int(((deg - d) * 60 - m) * 60)
    return d, m, s

def get_sign_info(lon):
    si = int(lon / 30) % 12
    sd = lon % 30
    return si, sd, ELEMENT_NAMES[si % 4], QUALITY_NAMES_VN[si % 3]

def is_gandanta(lon):
    """Kiểm tra Gandanta (last 2° water signs ↔ first 2° fire signs)."""
    si = int(lon / 30) % 12
    sd = lon % 30
    # Water signs: 3 (Cancer), 7 (Scorpio), 11 (Pisces)
    # Fire signs: 0 (Aries), 4 (Leo), 8 (Sagittarius)
    water_last = si in [3, 7, 11] and sd > 28
    fire_first = si in [0, 4, 8] and sd < 2
    return water_last or fire_first


# ============================================================
# PLANETARY HOURS (Giờ Hora) CALCULATION
# ============================================================

def get_sunrise_sunset(jd_start, lat, lon):
    """Tính sunrise, sunset, next_sunrise, prev_sunset bằng Swiss Ephemeris.
    
    Returns: (sunrise_jd, sunset_jd, next_sunrise_jd, prev_sunset_jd)
    Tất cả JD ở UTC.
    - sunrise_jd: sunrise của JST date
    - sunset_jd: sunset SAU sunrise (cùng JST date)
    - next_sunrise_jd: sunrise ngày tiếp theo
    - prev_sunset_jd: sunset TRƯỚC sunrise (đêm trước của JST date)
    """
    geopos = (lon, lat, 0.0)
    
    # Sunrise hôm nay (JST date)
    _, tret = swe.rise_trans(jd_start, swe.SUN, swe.CALC_RISE, geopos)
    sunrise_jd = tret[0]
    
    # Sunset hôm nay (sau sunrise)
    _, tret = swe.rise_trans(sunrise_jd + 0.01, swe.SUN, swe.CALC_SET, geopos)
    sunset_jd = tret[0]
    
    # Sunrise ngày mai
    _, tret = swe.rise_trans(sunset_jd + 0.01, swe.SUN, swe.CALC_RISE, geopos)
    next_sunrise_jd = tret[0]
    
    # Sunset TRƯỚC sunrise (tìm từ trước sunrise)
    _, tret = swe.rise_trans(sunrise_jd - 1.0, swe.SUN, swe.CALC_SET, geopos)
    prev_sunset_jd = tret[0]
    
    return sunrise_jd, sunset_jd, next_sunrise_jd, prev_sunset_jd


def calculate_planetary_hours(dt_utc, lat, lon):
    """Tính Giờ Hora (Planetary Hours) cho ngày hiện tại.
    
    Quy tắc:
    - Ngày bắt đầu từ sunrise → chia 12 giờ ban ngày
    - Đêm từ sunset → sunrise hôm sau → chia 12 giờ ban đêm
    - Giờ đầu tiên của ngày thuộc về hành tinh chủ quản ngày đó
    - Các giờ tiếp theo theo thứ tự Chaldean: Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon
    
    Returns: dict với current_planet, current_hora_num, is_daytime,
             sunrise_jst, sunset_jst, và full 24-hour list
    """
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    
    # Use Asia/Tokyo timezone (JST = UTC+9)
    tz = ZoneInfo('Asia/Tokyo')
    
    # Convert UTC to JST
    dt_utc_naive = dt_utc.replace(tzinfo=None)
    dt_jst = datetime(dt_utc_naive.year, dt_utc_naive.month, dt_utc_naive.day,
                      dt_utc.hour, dt_utc.minute, dt_utc.second, tzinfo=tz)
    # Actually convert properly
    dt_utc_aware = dt_utc.replace(tzinfo=timezone.utc)
    dt_jst = dt_utc_aware.astimezone(tz)
    
    # JD at local midnight (00:00 JST) — NOT 00:00 UTC!
    # This is critical: we need the JD of 00:00 in the LOCAL timezone
    local_midnight = datetime(dt_jst.year, dt_jst.month, dt_jst.day, tzinfo=tz)
    local_midnight_utc = local_midnight.astimezone(timezone.utc)
    jd_midnight = swe.julday(
        local_midnight_utc.year, local_midnight_utc.month, local_midnight_utc.day,
        local_midnight_utc.hour + local_midnight_utc.minute / 60.0 + local_midnight_utc.second / 3600.0,
        cal=swe.GREG_CAL
    )
    
    # Current JD
    now_jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
                        cal=swe.GREG_CAL)
    
    # Sunrise/Sunset for today (local date)
    sunrise_jd, sunset_jd, next_sunrise_jd, prev_sunset_jd = get_sunrise_sunset(jd_midnight, lat, lon)
    
    # Day of week — VEDIC FIX: Day starts at sunrise, not midnight
    # If before sunrise, use previous day's lord
    if now_jd < sunrise_jd:
        # Before sunrise → still yesterday's Vedic day
        effective_date = dt_jst - timedelta(days=1)
    else:
        effective_date = dt_jst
    
    # Python weekday: Mon=0, Sun=6
    # Map to DAY_LORDS: 6=Sun, 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat
    dow = effective_date.weekday()  # Mon=0...Sun=6
    day_lord = DAY_LORDS[dow]
    day_name = DAY_NAMES_VN[dow]
    
    # Determine which sunset to use for night hours
    if now_jd < sunrise_jd:
        night_sunset_jd = prev_sunset_jd
        night_sunrise_jd = sunrise_jd
    else:
        night_sunset_jd = sunset_jd
        night_sunrise_jd = next_sunrise_jd
    
    # Day/night lengths
    day_length_hours = (sunset_jd - sunrise_jd) * 24
    night_length_hours = (night_sunrise_jd - night_sunset_jd) * 24
    day_hour_len = day_length_hours / 12  # mỗi giờ ban ngày
    night_hour_len = night_length_hours / 12  # mỗi giờ ban đêm
    
    # Convert JD to local timezone string
    def jd_to_local_str(jd):
        y, m, d, hour = swe.revjul(jd, swe.GREG_CAL)
        h = int(hour)
        m_rem = (hour - h) * 60
        mi = int(m_rem)
        s = int((m_rem - mi) * 60)
        dt_utc_raw = datetime(int(y), int(m), int(d), h, mi, s, tzinfo=timezone.utc)
        dt_local = dt_utc_raw.astimezone(tz)
        return f"{dt_local.hour:02d}:{dt_local.minute:02d}"
    
    # Build 24 planetary hours list
    hours_list = []
    
    # === 12 Giờ ban ngày (sunrise → sunset) ===
    for i in range(12):
        h_start_jd = sunrise_jd + i * (day_hour_len / 24.0)
        h_end_jd = sunrise_jd + (i + 1) * (day_hour_len / 24.0)
        
        # Planet: start from day_lord, follow Chaldean order
        planet_idx = (CHALDEAN_ORDER.index(day_lord) + i) % 7
        planet = CHALDEAN_ORDER[planet_idx]
        
        hours_list.append({
            'num': i + 1,
            'period': 'day',
            'planet': planet,
            'start_jst': jd_to_local_str(h_start_jd),
            'end_jst': jd_to_local_str(h_end_jd),
            'start_jd': h_start_jd,
            'end_jd': h_end_jd,
        })
    
    # === 12 Giờ ban đêm (sunset → next sunrise) ===
    # Night hours CONTINUE from where day hours ended (not restart)
    night_start_idx = (CHALDEAN_ORDER.index(day_lord) + 12) % 7
    for i in range(12):
        h_start_jd = night_sunset_jd + i * (night_hour_len / 24.0)
        h_end_jd = night_sunset_jd + (i + 1) * (night_hour_len / 24.0)
        
        planet_idx = (night_start_idx + i) % 7
        planet = CHALDEAN_ORDER[planet_idx]
        
        hours_list.append({
            'num': i + 13,
            'period': 'night',
            'planet': planet,
            'start_jst': jd_to_local_str(h_start_jd),
            'end_jst': jd_to_local_str(h_end_jd),
            'start_jd': h_start_jd,
            'end_jd': h_end_jd,
        })
    
    # Find current planetary hour
    current_hora = None
    for h in hours_list:
        if h['start_jd'] <= now_jd < h['end_jd']:
            current_hora = h
            break
    
    # Fallback: if still not found, find closest hour
    if current_hora is None:
        for h in hours_list:
            if h['start_jd'] <= now_jd:
                current_hora = h
        if current_hora is None:
            current_hora = hours_list[0]
    
    result = {
        'day_name': day_name,
        'day_lord': day_lord,
        'dow': dow,
        'sunrise_jst': jd_to_local_str(sunrise_jd),
        'sunset_jst': jd_to_local_str(sunset_jd),
        'day_length_hours': round(day_length_hours, 2),
        'night_length_hours': round(night_length_hours, 2),
        'day_hour_minutes': round(day_hour_len * 60, 0),
        'night_hour_minutes': round(night_hour_len * 60, 0),
        'current_planet': current_hora['planet'] if current_hora else 'Unknown',
        'current_hora_num': current_hora['num'] if current_hora else 0,
        'current_period': current_hora['period'] if current_hora else 'unknown',
        'hours': hours_list,
    }
    
    return result


# ============================================================
# DASHA CALCULATION (Vimshottari Dasha)
# ============================================================

def calculate_dasha(moon_lon, jd_utc):
    """Tính Vimshottari Dasha sequence từ Moon position."""
    from datetime import datetime, timedelta
    
    # Moon's Nakshatra
    nakshatra_idx = int(moon_lon / NAKSHATRA_SPAN) % 27
    nakshatra_name = NAKSHATRA_27[nakshatra_idx]
    nakshatra_lord = NAKSHATRA_LORDS[nakshatra_idx]
    
    # Position within Nakshatra
    pos_in_nakshatra = moon_lon % NAKSHATRA_SPAN
    remaining_fraction = 1.0 - (pos_in_nakshatra / NAKSHATRA_SPAN)
    
    # Build Dasha sequence
    dasha_sequence = []
    start_idx = DASHA_ORDER.index(nakshatra_lord)
    ordered_planets = DASHA_ORDER[start_idx:] + DASHA_ORDER[:start_idx]
    
    current_jd = jd_utc
    
    for i, lord in enumerate(ordered_planets):
        years = DASHA_YEARS[lord]
        
        # For first Dasha, only remaining portion
        if i == 0:
            effective_years = years * remaining_fraction
        else:
            effective_years = years
        
        # Convert JD to date
        start_date = datetime(1, 1, 1) + timedelta(days=current_jd - 1721425.5)
        end_date = start_date + timedelta(days=effective_years * 365.25)
        
        dasha_sequence.append({
            'lord': lord,
            'years': years,
            'effective_years': round(effective_years, 2),
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'jd_start': current_jd,
            'jd_end': current_jd + effective_years * 365.25,
        })
        
        current_jd += effective_years * 365.25
    
    return {
        'moon_nakshatra': nakshatra_name,
        'nakshatra_lord': nakshatra_lord,
        'remaining_fraction': round(remaining_fraction * 100, 1),
        'sequence': dasha_sequence,
    }


def get_current_dasha(dasha_data, current_jd):
    """Tìm Dasha hiện tại."""
    for d in dasha_data['sequence']:
        if d['jd_start'] <= current_jd <= d['jd_end']:
            return d
    return None


def get_antardasha(dasha_data, current_jd):
    """Tính Antardasha (tiểu vận) trong Dasha hiện tại."""
    from datetime import datetime, timedelta
    
    current_dasha = get_current_dasha(dasha_data, current_jd)
    if not current_dasha:
        return []
    
    lord = current_dasha['lord']
    dasha_start_jd = current_dasha['jd_start']
    
    # Sub-lords follow same order starting from main lord
    start_idx = DASHA_ORDER.index(lord)
    sub_order = DASHA_ORDER[start_idx:] + DASHA_ORDER[:start_idx]
    
    antardashas = []
    sub_jd = dasha_start_jd
    
    for sl in sub_order:
        sub_years = DASHA_YEARS[lord] * DASHA_YEARS[sl] / 120
        sub_end_jd = sub_jd + sub_years * 365.25
        
        sub_start_date = datetime(1, 1, 1) + timedelta(days=sub_jd - 1721425.5)
        sub_end_date = datetime(1, 1, 1) + timedelta(days=sub_end_jd - 1721425.5)
        
        antardashas.append({
            'lord': sl,
            'years': round(sub_years, 2),
            'start': sub_start_date.strftime('%Y-%m-%d'),
            'end': sub_end_date.strftime('%Y-%m-%d'),
            'is_current': sub_jd <= current_jd <= sub_end_jd,
        })
        
        sub_jd = sub_end_jd
    
    return antardashas


# ============================================================
# ASPECTS
# ============================================================

def calculate_aspects(bodies_data, outer_data=None):
    aspects_list = []
    all_b = dict(bodies_data)
    if outer_data:
        all_b.update(outer_data)
    
    names = list(all_b.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            diff = angle_diff(all_b[n1]['lon'], all_b[n2]['lon'])
            
            for aname, ainfo in ASPECTS.items():
                angle = ainfo['angle']
                orb = ainfo['orb']
                target = abs(diff - angle)
                if target <= orb:
                    tight = target <= orb * 0.5
                    aspects_list.append({
                        'p1': n1, 'p2': n2,
                        'aspect': aname, 'symbol': ainfo['symbol'],
                        'diff': diff, 'orb': round(target, 2),
                        'tight': tight, 'type': ainfo['type'],
                    })
                    break
    return aspects_list


# ============================================================
# COMBUSTION
# ============================================================

def check_combustion(bodies_data):
    results = []
    sun_lon = bodies_data['Mặt Trời']['lon']
    
    for name, limit in COMBUST_ORBS.items():
        if name not in bodies_data:
            continue
        diff = angle_diff(sun_lon, bodies_data[name]['lon'])
        
        if diff <= CAZIMI_ORB:
            results.append({'planet': name, 'diff': round(diff, 2),
                          'status': 'CAZIMI ⚡',
                          'desc': f'{name} Cazimi — Năng lượng cực mạnh, tập trung'})
        elif diff <= limit:
            results.append({'planet': name, 'diff': round(diff, 2),
                          'status': 'COMBUST 🔥',
                          'desc': f'{name} combust — cách Mặt Trời {diff:.1f}°'})
    return results


# ============================================================
# MOON-PLANET COMBINATIONS (Vedic Yoga)
# ============================================================

def get_moon_combinations(moon_lon, bodies_data):
    """Tìm Moon kết hợp với hành tinh nào (same sign hoặc tight aspect)."""
    combos = []
    moon_sign = int(moon_lon / 30) % 12
    
    for name in ['Mặt Trời', 'Thủy', 'Kim', 'Hoả', 'Mộc', 'Thổ', 'Rahu', 'Ketu']:
        if name not in bodies_data or name == 'Mặt Trăng':
            continue
        p_lon = bodies_data[name]['lon']
        p_sign = int(p_lon / 30) % 12
        
        # Same sign = conjunction
        if moon_sign == p_sign:
            diff = angle_diff(moon_lon, p_lon)
            combos.append({
                'planet': name,
                'type': 'Conjunction (cùng cung)',
                'diff': round(diff, 1),
            })
    
    # Check Nakshatra lord
    _, nak_name, _, nak_lord, _ = get_nakshatra(moon_lon)
    
    return combos, nak_lord


def interpret_moon_combination(planet_name, nakshatra_lord):
    """Diễn giải Moon + Planet combination."""
    interpretations = {
        'Mặt Trời': ("🌙☀️ Moon-Sun (Surya Yoga)", "Stable Uptrend — Tăng ổn định, confidence, low volatility",
                     "Buy dips, Gold mạnh, government bonds"),
        'Thủy': ("🌙☿️ Moon-Mercury", "High Volatility — Whipsaws, lên xuống liên tục",
                 "Scalping, quick in-out, tight SL"),
        'Kim': ("🌙♀️ Moon-Venus", "Risk Appetite — Risk-on, consumer/luxury mạnh",
                "Growth stocks, consumer sector, trend following"),
        'Hoả': ("🌙♂️ Chandra-Mangal Yoga 🐂", "Bull Run — Tăng nhanh, volume cao, aggressive bullish",
                "Buy on dips, momentum trading, defense/energy"),
        'Mộc': ("🌙♃ Moon-Jupiter", "Expansion — Tăng trưởng ổn định, banking rally, optimism",
                "Position trading, banking/finance, swing trade"),
        'Thổ': ("🌙♄ Vish Yoga 🐻", "Slow Bleed — Range-bound đến negative, struggle tại resistance",
                "Sell on rise, tránh fresh long, cash"),
        'Rahu': ("🌙🐉 Grahan Yoga 🕳️", "The Trap — High volatility, fake breakout, sudden spikes",
                 "Option buying (gamma), KHÔNG hold qua đêm, tight SL"),
        'Ketu': ("🌙🔻 Ketu Panic 💥", "Panic Button — Drop đột ngột không news, 'bottom falls out'",
                 "Hedge, shorting, defensive positioning"),
    }
    
    return interpretations.get(planet_name, (f"🌙 {planet_name}", "", ""))


# ============================================================
# MOON ASPECTS INTERPRETATION
# ============================================================

def interpret_moon_aspect(aspect_name, other_planet):
    """Diễn giải Moon aspect cho trading."""
    key = (aspect_name, other_planet)
    
    # Specific interpretations
    specific = {
        ('Square', 'Hoả'): "PANIC SELL / FOMO BUY — Rất biến động ⚠️⚠️",
        ('Opposition', 'Hoả'): "Bulls vs Bears — Chiến trường, dễ đảo chiều ⚠️",
        ('Square', 'Thủy'): "False signals — Thông tin trái ngược, confusion ⚠️",
        ('Opposition', 'Thủy'): "Market phân hóa — Whipsaws, sideways ⚠️",
        ('Square', 'Rahu'): "BLACK SWAN potential — Biến động cực mạnh ⚠️⚠️⚠️",
        ('Opposition', 'Rahu'): "DISRUPTION lớn — Fake moves, sudden spikes ⚠️⚠️⚠️",
        ('Trine', 'Mộc'): "Bullish mạnh — Expansion, steady growth ✅",
        ('Conjunction', 'Mộc'): "Optimism — Steady growth, banking rally ✅",
        ('Sextile', 'Mộc'): "Cơ hội — Growth, good entry ✅",
        ('Square', 'Thổ'): "Fear + Greed — Phân cực, correction ⚠️",
        ('Opposition', 'Thổ'): "Turning point — Fear vs Greed cực đoan ⚠️",
        ('Trine', 'Kim'): "Risk-on ổn định — Bullish trend ✅",
        ('Conjunction', 'Kim'): "Risk appetite cao — Bullish sentiment ✅",
        ('Square', 'Kim'): "Choppy — Risk on/off liên tục ⚠️",
        ('Opposition', 'Kim'): "Bull/Bear phân cực — Dễ đảo chiều ⚠️",
        ('Trine', 'Mặt Trời'): "Momentum bullish ổn định ✅",
        ('Conjunction', 'Mặt Trời'): "New Moon energy — Bắt đầu chu kỳ mới",
        ('Opposition', 'Mặt Trời'): "Full Moon — Đỉnh cảm xúc, reversal ⚠️",
        ('Trine', 'Hoả'): "Động lực mua mạnh — Momentum bullish ✅",
        ('Sextile', 'Hoả'): "Bullish nhẹ — Động lực tăng ✅",
        ('Sextile', 'Thủy'): "Thông tin tốt — Setup rõ ràng ✅",
        ('Trine', 'Thủy'): "Phân tích chính xác — Trade smooth ✅",
        ('Sextile', 'Thổ'): "Cân bằng rủi ro — Trade có tính toán",
        ('Trine', 'Thổ'): "Correction có trật tự — Structured ✅",
        ('Sextile', 'Rahu'): "Volatility có lợi — Opportunity ✅",
        ('Trine', 'Rahu'): "Disruption tích cực — Trend mới ✅",
        ('Sextile', 'Ketu'): "Breakout tiềm năng — Opportunity ✅",
        ('Trine', 'Ketu'): "Chuyển đổi thuận lợi — Smooth ✅",
    }
    
    if key in specific:
        return specific[key]
    
    # Generic
    generic = {
        'Conjunction': f"Năng lượng hợp nhất — {other_planet} ảnh hưởng mạnh đến Moon",
        'Sextile': f"Hài hòa — Cơ hội từ {other_planet}",
        'Square': f"Căng thẳng — Thử thách từ {other_planet} ⚠️",
        'Trine': f"Thuận lợi — Dòng chảy tốt từ {other_planet} ✅",
        'Opposition': f"Đối cực — Turning point từ {other_planet} ⚠️",
        'Quincunx': f"Điều chỉnh — Bất ổn nhẹ từ {other_planet}",
        'Semi-Square': f"Nhẹ căng thẳng — Watch {other_planet}",
        'Sesquiquadrate': f"Friction — Watch {other_planet}",
    }
    return generic.get(aspect_name, f"{aspect_name} {other_planet}")


# ============================================================
# MOON PHASE
# ============================================================

def get_moon_phase(elongation):
    if elongation < 7:
        return "New Moon", "🌑 Bắt đầu chu kỳ mới, ít biến động — Chờ breakout"
    elif elongation < 83:
        return "Waxing Crescent", "🌒 Lạc quan dần, Bullish — Buy dips"
    elif 83 <= elongation <= 97:
        return "First Quarter", "🌓 Xung đột, decision point — Watch reversal"
    elif elongation < 173:
        return "Waxing Gibbous", "🌔 Lạc quan cao, Bullish — Trend following"
    elif 173 <= elongation <= 187:
        return "Full Moon", "🌕 Đỉnh cảm xúc, BIẾN ĐỘNG CAO — Tránh overtrading"
    elif elongation < 263:
        return "Waning Gibbous", "🌖 Lạc quan giảm, thận trọng — Take profit"
    elif 263 <= elongation <= 277:
        return "Last Quarter", "🌗 Đánh giá lại, biến động — Hedge"
    elif elongation < 353:
        return "Waning Crescent", "🌘 Bi quan, Bearish — Cash, short"
    else:
        return "New Moon", "🌑 Bắt đầu chu kỳ mới, ít biến động — Chờ breakout"


# ============================================================
# CALCULATE ALL
# ============================================================

def calculate_all(dt_utc, lat, lon, is_natal=False):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                       dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
                       cal=swe.GREG_CAL)
    
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    
    # Ascendant (sidereal)
    tropical_cusps, asmc = swe.houses(jd_ut, lat, lon, b'P')
    asc_sidereal = (tropical_cusps[0] - ayanamsa) % 360
    mc_sidereal = (tropical_cusps[10] - ayanamsa) % 360
    
    asc_si = int(asc_sidereal / 30) % 12
    asc_sd = asc_sidereal % 30
    asc_d, asc_m, asc_s = decimal_to_dms(asc_sd)
    mc_si = int(mc_sidereal / 30) % 12
    mc_sd = mc_sidereal % 30
    mc_d, mc_m, mc_s = decimal_to_dms(mc_sd)
    
    # Navagraha
    bodies = {}
    for name, bid in BODIES.items():
        r, _ = swe.calc_ut(jd_ut, bid, swe.FLG_SIDEREAL)
        p_lon, p_lat, dist, spd = r[0], r[1], r[2], r[3]
        si, sd, elem, qual = get_sign_info(p_lon)
        d, m, s = decimal_to_dms(sd)
        ni, nn, pa, nl, ns = get_nakshatra(p_lon)
        h = get_house(p_lon, asc_sidereal)
        
        bodies[name] = {
            'lon': p_lon, 'lat': p_lat, 'dist': dist, 'spd': spd,
            'si': si, 'sd': sd, 'd': d, 'm': m, 's': s,
            'sign': ZODIAC_SIGNS[si], 'elem': elem, 'qual': qual,
            'ni': ni, 'nak': nn, 'ns': ns, 'pada': pa, 'nl': nl, 'house': h,
        }
    
    # Ketu
    rahu_lon = bodies['Rahu']['lon']
    ketu_lon = (rahu_lon + 180) % 360
    si, sd, elem, qual = get_sign_info(ketu_lon)
    d, m, s = decimal_to_dms(sd)
    ni, nn, pa, nl, ns = get_nakshatra(ketu_lon)
    h = get_house(ketu_lon, asc_sidereal)
    bodies['Ketu'] = {
        'lon': ketu_lon, 'lat': 0, 'dist': 0, 'spd': 0,
        'si': si, 'sd': sd, 'd': d, 'm': m, 's': s,
        'sign': ZODIAC_SIGNS[si], 'elem': elem, 'qual': qual,
        'ni': ni, 'nak': nn, 'ns': ns, 'pada': pa, 'nl': nl, 'house': h,
    }
    
    # Outer planets
    outer_names = {'Thiên Vương': swe.URANUS, 'Hải Vương': swe.NEPTUNE, 'Diêm Vương': swe.PLUTO}
    outer = {}
    for name, bid in outer_names.items():
        r, _ = swe.calc_ut(jd_ut, bid, swe.FLG_SIDEREAL)
        p_lon, p_lat, dist, spd = r[0], r[1], r[2], r[3]
        si, sd, elem, qual = get_sign_info(p_lon)
        d, m, s = decimal_to_dms(sd)
        ni, nn, pa, nl, ns = get_nakshatra(p_lon)
        h = get_house(p_lon, asc_sidereal)
        
        outer[name] = {
            'lon': p_lon, 'lat': p_lat, 'dist': dist, 'spd': spd,
            'si': si, 'sd': sd, 'd': d, 'm': m, 's': s,
            'sign': ZODIAC_SIGNS[si], 'elem': elem, 'qual': qual,
            'ni': ni, 'nak': nn, 'ns': ns, 'pada': pa, 'nl': nl, 'house': h,
        }
    
    # Moon phase
    elongation = (bodies['Mặt Trăng']['lon'] - bodies['Mặt Trời']['lon']) % 360
    phase_name, phase_desc = get_moon_phase(elongation)
    
    # Aspects
    aspects = calculate_aspects(bodies, outer)
    
    # Combustion
    combustions = check_combustion(bodies)
    
    # Moon combinations
    moon_combos, nakshatra_lord = get_moon_combinations(bodies['Mặt Trăng']['lon'], bodies)
    
    # Gandanta
    moon_gandanta = is_gandanta(bodies['Mặt Trăng']['lon'])
    
    # Dasha (Vimshottari) - only for natal charts
    dasha = None
    current_dasha = None
    antardashas = []
    
    if is_natal:
        dasha = calculate_dasha(bodies['Mặt Trăng']['lon'], jd_ut)
        # Use current date to find active Dasha, not birth date
        from datetime import datetime
        current_jd = swe.julday(datetime.now(timezone.utc).year, datetime.now(timezone.utc).month, 
                                datetime.now(timezone.utc).day, 
                                datetime.now(timezone.utc).hour + datetime.now(timezone.utc).minute / 60.0,
                                cal=swe.GREG_CAL)
        current_dasha = get_current_dasha(dasha, current_jd)
        antardashas = get_antardasha(dasha, current_jd)
    
    # Planetary Hours (Giờ Hora) — Sử dụng hora_service.py chính xác
    try:
        from hora_service import get_current_hora
        tz = ZoneInfo('Asia/Tokyo')
        from datetime import datetime
        now_tz = datetime.now(tz)
        hora_data = get_current_hora(lat=lat, lon=lon, tz_name='Asia/Tokyo')
        planetary_hours = {
            'day_name': hora_data['day_of_week'],
            'day_lord': hora_data['first_hora_lord'],
            'sunrise_jst': hora_data['sunrise'],
            'sunset_jst': hora_data['sunset'],
            'day_length_hours': hora_data['day_length_hours'],
            'night_length_hours': hora_data['night_length_hours'],
            'day_hour_minutes': hora_data['day_length_hours'] * 60 / 12,
            'night_hour_minutes': hora_data['night_length_hours'] * 60 / 12,
            'current_planet': hora_data['current_hora']['lord'],
            'current_hora_num': hora_data['current_hora']['hour_num'],
            'current_period': 'day' if hora_data['is_daytime'] else 'night',
            'current_trading': hora_data['current_hora']['trading'],
            'current_strategy': hora_data['current_hora']['strategy'],
            'current_element': hora_data['current_hora']['element'],
            'hours': [{
                'num': h['hour_num'],
                'period': h['period'],
                'planet': h['lord'],
                'start_jst': h['start'],
                'end_jst': h['end'],
                'trading': h.get('trading', ''),
                'strategy': h.get('strategy', ''),
            } for h in hora_data['full_sequence']],
        }
    except ImportError:
        # Fallback to old method if hora_service.py not available
        planetary_hours = calculate_planetary_hours(dt_utc, lat, lon)
    
    return {
        'ayanamsa': ayanamsa, 'jd': jd_ut,
        'asc_si': asc_si, 'asc_sd': asc_sd, 'asc_d': asc_d, 'asc_m': asc_m, 'asc_s': asc_s,
        'mc_si': mc_si, 'mc_sd': mc_sd, 'mc_d': mc_d, 'mc_m': mc_m, 'mc_s': mc_s,
        'bodies': bodies, 'outer': outer,
        'phase_name': phase_name, 'phase_desc': phase_desc, 'elongation': elongation,
        'aspects': aspects, 'combustions': combustions,
        'moon_combos': moon_combos, 'nakshatra_lord': nakshatra_lord,
        'moon_gandanta': moon_gandanta,
        'dasha': dasha, 'current_dasha': current_dasha, 'antardashas': antardashas,
        'planetary_hours': planetary_hours,
    }


# ============================================================
# FORMAT OUTPUT
# ============================================================

def format_output(data, dt, tz, lat, lon):
    b = data['bodies']
    o = data['outer']
    a = data['aspects']
    c = data['combustions']
    mc = data['moon_combos']
    nl = data['nakshatra_lord']
    moon = b['Mặt Trăng']
    
    lines = []
    def W(s=""): lines.append(s)
    
    W("=" * 75)
    W("📊 FINANCIAL ASTROLOGY — DAY TRADING FOCUS (M15/H1)")
    W("   (SIDEREAL - AYANAMSA LAHIRI | WHOLE SIGN HOUSES)")
    W("=" * 75)
    W(f"⏰ {dt.strftime('%Y-%m-%d %H:%M:%S')} {tz} | 📍 {lat}°N, {lon}°E")
    W(f"🌐 Ayanamsa: {data['ayanamsa']:.4f}° | JD: {data['jd']:.6f}")
    W("=" * 75)
    W()
    
    # Chart info
    W(f"⬆️ Lagna: {ZODIAC_SIGNS[data['asc_si']]} {data['asc_d']}°{data['asc_m']}'{data['asc_s']}\"")
    W(f"☀️ MC:    {ZODIAC_SIGNS[data['mc_si']]} {data['mc_d']}°{data['mc_m']}'{data['mc_s']}\"")
    W()
    
    # =============================================
    # 0. PLANETARY HOURS (Giờ Hora)
    # =============================================
    ph = data.get('planetary_hours', {})
    if ph:
        current_planet = ph['current_planet']
        hora_info = HORA_TRADING.get(current_planet, {})
        
        W("=" * 75)
        W("⏰ GIỜ HORA (PLANETARY HOURS) — Chaldean Order")
        W("=" * 75)
        W(f"📅 {ph['day_name']} — Hành tinh chủ quản ngày: {current_planet}")
        W(f"🌅 Sunrise: {ph['sunrise_jst']} JST | 🌇 Sunset: {ph['sunset_jst']} JST")
        W(f"☀️ Ban ngày: {ph['day_length_hours']}h ({ph['day_hour_minutes']:.0f}min/giờ) | 🌙 Ban đêm: {ph['night_length_hours']}h ({ph['night_hour_minutes']:.0f}min/giờ)")
        W()
        
        emoji = hora_info.get('emoji', '❓')
        name = hora_info.get('name', f'Giờ {current_planet}')
        bias = hora_info.get('bias', '')
        assets = hora_info.get('assets', '')
        strategy = hora_info.get('strategy', '')
        warning = hora_info.get('warning', '')
        
        period_emoji = '☀️ BAN NGÀY' if ph['current_period'] == 'day' else '🌙 BAN ĐÊM'
        
        W(f"{emoji} GIỜ HIỆN TẠI: {name} (Hora {ph['current_hora_num']}/24) — {period_emoji}")
        W(f"   📊 Bias: {bias}")
        W(f"   💰 Assets phù hợp: {assets}")
        W(f"   🎯 Chiến lược: {strategy}")
        if warning:
            W(f"   ⚠️ Cảnh báo: {warning}")
        W()
        
        # Vàng (XAU/USD) specific
        gold_meaning = HORA_GOLD.get(current_planet, '')
        W(f"🥇 VÀNG (XAU/USD): {gold_meaning}")
        
        # Bitcoin specific
        btc_meaning = HORA_BTC.get(current_planet, '')
        W(f"₿ BITCOIN (BTC/USD): {btc_meaning}")
        W()
        
        # Show today's full 24-hour schedule
        W("--- LỊCH 24 GIỜ HORA HÔM NAY ---")
        W(f"{'Hora':<6} {'Period':<5} {'Giờ JST':<12} {'Hành tinh':<10} {'Trading':<30}")
        W("-" * 70)
        
        for h in ph['hours']:
            period_icon = '☀️' if h['period'] == 'day' else '🌙'
            h_planet = h['planet']
            h_info = HORA_TRADING.get(h_planet, {})
            h_bias = h_info.get('bias', '')[:28]
            
            marker = ' ◀' if h['num'] == ph['current_hora_num'] else ''
            W(f"  {h['num']:2d}  {period_icon:<4} {h['start_jst']}-{h['end_jst']:<7} {h_planet:<10} {h_bias}{marker}")
        W()
        W("=" * 75)
        W()
    
    # =============================================
    # 1. MOON ANALYSIS
    # =============================================
    W("=" * 75)
    W("🌙 PHÂN TÍCH MOON — SHORT-TERM SENTIMENT (M15/H1)")
    W("=" * 75)
    
    W(f"🌙 Phase: {data['phase_name']}")
    W(f"   {data['phase_desc']}")
    W(f"   Elongation: {data['elongation']:.1f}°")
    W()
    
    W(f"🌙 Moon ở {moon['sign']} {moon['d']}°{moon['m']}'{moon['s']}\"")
    W(f"   Nguyên tố: {moon['elem']} | Chất lượng: {moon['qual']}")
    
    # Element mood
    if moon['elem'] == "Lửa":
        W("   🔥 MOOD: RISK-ON → Tự tin, bullish, thích mạo hiểm")
        W("   → Xu hướng: BUY dips, momentum plays")
    elif moon['elem'] == "Đất":
        W("   🌍 MOOD: THỰC TẾ → Safe haven, value play")
        W("   → Xu hướng: Vàng mạnh, crypto ổn định")
    elif moon['elem'] == "Khí":
        W("   💨 MOOD: LÝ TRÍ → Phân tích, phân vân, sideways")
        W("   → Xu hướng: Range trading, false breakouts")
    elif moon['elem'] == "Nước":
        W("   💧 MOOD: CẢM XÚC → Nhạy cảm, dễ biến động mạnh")
        W("   → Xu hướng: Watch sudden moves, tight SL")
    
    W()
    W(f"   {moon['ns']} Nakshatra: {moon['nak']} (thứ {moon['ni']+1}/27) | Pada: {moon['pada']}/4")
    W(f"   Lord: {moon['nl']}")
    
    # Nakshatra trade quality
    if moon['nak'] in NAKSHATRA_TRADE:
        quality, desc = NAKSHATRA_TRADE[moon['nak']]
        W(f"   {quality} cho trading — {desc}")
    
    # Gandanta
    if data['moon_gandanta']:
        W("   ⚠️🌊 MOON Ở GANDANTA POINT — Biến động cực đoan, reversal bất ngờ!")
        W("   ⚠️ Khuyến nghị: Tránh trade hoặc dùng VERY TIGHT SL")
    
    W()
    
    # Moon speed (Moon luôn di chuyển thuận, không bao giờ retrograde)
    if moon['spd'] > 13:
        W(f"   🚀 Moon nhanh ({moon['spd']:.1f}°/ngày) → Biến động CAO, nhiều cơ hội M15/H1")
    elif moon['spd'] > 0:
        W(f"   🐢 Moon bình thường ({moon['spd']:.1f}°/ngày) → Biến động trung bình")
    else:
        W(f"   ⚠️ Moon đứng (stationary) → Xu hướng tạm dừng, watch breakout")
    
    # =============================================
    # 2. MOON-PLANET COMBINATIONS
    # =============================================
    W()
    W("-" * 50)
    W("🔗 MOON COMBINATIONS (Moon kết hợp với hành tinh)")
    W("-" * 50)
    
    if mc:
        for combo in mc:
            title, trend, strategy = interpret_moon_combination(combo['planet'], nl)
            W(f"   {title} (cách {combo['diff']}°)")
            W(f"   → {trend}")
            W(f"   → Chiến lược: {strategy}")
    else:
        W(f"   Moon không conjunction hành tinh nào trong cùng cung")
    
    # Nakshatra lord influence
    W(f"   🌙 Moon Nakshatra Lord: {nl} → {nl} sẽ ảnh hưởng mạnh đến trend hôm nay")
    
    # =============================================
    # 3. MOON ASPECTS
    # =============================================
    W()
    W("-" * 50)
    W("🔗 MOON ASPECTS — Góc chiếu tác động lên Moon")
    W("   ⚡ Quan trọng nhất cho M15/H1 ⚡")
    W("-" * 50)
    
    moon_asps = [x for x in a if x['p1'] == 'Mặt Trăng' or x['p2'] == 'Mặt Trăng']
    
    if not moon_asps:
        W("   ⚪ Moon không có aspect chính → Market lặng, ít biến động")
    else:
        for asp in sorted(moon_asps, key=lambda x: x['orb']):
            other = asp['p2'] if asp['p1'] == 'Mặt Trăng' else asp['p1']
            tight = "🔴 TIGHT" if asp['tight'] else ""
            interp = interpret_moon_aspect(asp['aspect'], other)
            W(f"   🌙 {asp['symbol']} {asp['aspect']} {SHORT_NAMES.get(other, other)} (orb: {asp['orb']}°) {tight}")
            W(f"      → {interp}")
    
    # =============================================
    # 4. COMBUSTION
    # =============================================
    W()
    W("=" * 75)
    W("🔥 COMBUSTION — Hành tinh bị bốc cháy")
    W("=" * 75)
    
    if c:
        for comb in c:
            W(f"   {comb['desc']}")
            if comb['planet'] == 'Thủy':
                W("   → Thông tin market có thể sai lệch, false signals nhiều")
            elif comb['planet'] == 'Kim':
                W("   → Risk appetite bị ảnh hưởng, valuation sai lệch")
            elif comb['planet'] == 'Hoả':
                W("   → Aggression giảm, nhưng bất ngờ tăng")
    else:
        W("   ✅ Không có hành tinh nào combust → Tâm lý ổn định")
    
    # =============================================
    # 5. MERCURY STATUS
    # =============================================
    W()
    W("=" * 75)
    W("☿️ THỦY TINH — THÔNG TIN & TÍN HIỆU")
    W("=" * 75)
    
    merc = b['Thủy']
    if merc['spd'] < 0:
        W("   ☿️ THỦY NGHỊCH HÀNH (Mercury Retrograde)")
        W("   ⚠️ False breakout/breakdown — không vào lệnh ngay tại breakout")
        W("   ⚠️ Technical glitch, execution error")
        W("   ⚠️ Thông tin nhầm lẫn, news gây sốc")
        W("   → Khuyến nghị: Chờ confirmation, giảm position size, tight SL")
    else:
        W("   ☿️ Thủy thuận → Thông tin rõ ràng, setup đáng tin cậy")
    
    merc_combust = any(x['planet'] == 'Thủy' for x in c)
    if merc_combust:
        W("   🔥 THỦY BỐC CHÁY → False signals cao, trade ít lệnh hơn")
    
    # =============================================
    # 6. ALL MAJOR ASPECTS
    # =============================================
    W()
    W("=" * 75)
    W("🔗 TẤT CẢ GÓC CHIẾU CHÍNH (Major Aspects)")
    W("=" * 75)
    
    sorted_asps = sorted(a, key=lambda x: x['orb'])
    for asp in sorted_asps:
        tight = "🔴" if asp['tight'] else " "
        W(f"  {tight} {SHORT_NAMES.get(asp['p1'], asp['p1'])} {asp['symbol']} {asp['aspect']} {SHORT_NAMES.get(asp['p2'], asp['p2'])} (orb: {asp['orb']}°)")
    
    # =============================================
    # 7. DAY TRADING SIGNAL
    # =============================================
    W()
    W("=" * 75)
    W("📊 TÍN HIỆU DAY TRADING (M15/H1)")
    W("=" * 75)
    
    signals = []
    
    # Moon phase bias
    if "Waxing" in data['phase_name']:
        signals.append("📈 Moon Phase: BULLISH BIAS")
    elif "Waning" in data['phase_name']:
        signals.append("📉 Moon Phase: BEARISH BIAS")
    elif data['phase_name'] == "Full Moon":
        signals.append("🌕 Full Moon: BIẾN ĐỘNG CAO — Watch for reversal")
    elif data['phase_name'] == "New Moon":
        signals.append("🌑 New Moon: ÍT BIẾN ĐỘNG — Wait for breakout")
    
    # Moon aspects sentiment
    if moon_asps:
        neg = ['Square', 'Opposition', 'Quincunx']
        pos = ['Trine', 'Sextile', 'Conjunction']
        neg_c = sum(1 for x in moon_asps if x['aspect'] in neg)
        pos_c = sum(1 for x in moon_asps if x['aspect'] in pos)
        
        if neg_c >= 2:
            signals.append(f"⚠️ Moon có {neg_c} aspect tiêu cực → BIẾN ĐỘNG CAO, cẩn trọng")
        elif pos_c >= 2:
            signals.append(f"✅ Moon có {pos_c} aspect tích cực → Trend thuận lợi")
        elif neg_c >= 1:
            signals.append("⚡ Moon có aspect căng thẳng → Watch for volatility spikes")
    
    # Mercury
    if merc['spd'] < 0:
        signals.append("☿️ Mercury Rx → Cẩn trọng, không trade news, chờ confirmation")
    if merc_combust:
        signals.append("🔥 Mercury combust → False signals cao")
    
    # Gandanta
    if data['moon_gandanta']:
        signals.append("🌊 Moon ở Gandanta → BIẾN ĐỘNG CỰC ĐOAN, tránh trade hoặc tight SL")
    
    # Moon combos
    for combo in mc:
        title, trend, _ = interpret_moon_combination(combo['planet'], nl)
        signals.append(f"🔗 {title} → {trend}")
    
    for s in signals:
        W(f"  {s}")
    
    # =============================================
    # 8. NAVAGRAHA SUMMARY
    # =============================================
    W()
    W("=" * 75)
    W("📋 NAVAGRAHA SUMMARY")
    W("=" * 75)
    
    order = ['Mặt Trăng', 'Mặt Trời', 'Thủy', 'Kim', 'Hoả', 'Mộc', 'Thổ', 'Rahu', 'Ketu']
    for name in order:
        if name not in b:
            continue
        d = b[name]
        pos = f"{d['d']}°{d['m']}'{d['s']}\""
        rx = " Rx" if d['spd'] < 0 else ""
        cb = " 🔥COMBUST" if any(x['planet'] == name and x['status'] == 'COMBUST 🔥' for x in c) else ""
        cz = " ⚡CAZIMI" if any(x['planet'] == name and x['status'] == 'CAZIMI ⚡' for x in c) else ""
        W(f"  {BODY_NAMES[name]}: {d['sign']} {pos} | Nhà {d['house']} | {d['ns']} {d['nak']} P{d['pada']}{rx}{cb}{cz}")
    
    # =============================================
    # 9. OUTER PLANETS
    # =============================================
    W()
    W("=" * 75)
    W("🪐 OUTER PLANETS")
    W("=" * 75)
    
    for name in ['Thiên Vương', 'Hải Vương', 'Diêm Vương']:
        if name not in o:
            continue
        d = o[name]
        pos = f"{d['d']}°{d['m']}'{d['s']}\""
        rx = " Rx" if d['spd'] < 0 else ""
        W(f"  {BODY_NAMES[name]}: {d['sign']} {pos} | Nhà {d['house']} | {d['nak']} P{d['pada']}{rx}")
    
    # =============================================
    # 10. DASHA (VIMSHOTTARI)
    # =============================================
    W()
    W("=" * 75)
    W("📊 DASHA — ĐẠI VẬN & TIỂU VẬN (Vimshottari 120 năm)")
    W("=" * 75)
    
    dasha = data.get('dasha', {})
    current_dasha = data.get('current_dasha')
    antardashas = data.get('antardashas', [])
    
    if dasha:
        W(f"🌙 Moon Nakshatra: {dasha['moon_nakshatra']}")
        W(f"👑 Nakshatra Lord: {dasha['nakshatra_lord']}")
        W(f"📐 Remaining in Nakshatra: {dasha['remaining_fraction']}%")
        W()
        
        if current_dasha:
            W(f"🔴 ĐẠI VẬN HIỆN TẠI: {current_dasha['lord']}")
            W(f"   {DASHA_MEANINGS.get(current_dasha['lord'], '')}")
            W(f"   Từ {current_dasha['start']} đến {current_dasha['end']}")
            W()
        
        W("--- ĐẠI VẬN (120 năm) ---")
        W(f"{'Đại vận':<12} {'Năm':<8} {'Từ':<12} {'Đến':<12} {'Hiện tại':<10}")
        W("-" * 60)
        
        for d in dasha['sequence']:
            marker = "🔴 HIỆN TẠI" if (current_dasha and d['lord'] == current_dasha['lord']) else ""
            W(f"{d['lord']:<12} {d['effective_years']:<8.2f} {d['start']:<12} {d['end']:<12} {marker}")
        
        W()
        
        if antardashas:
            W("--- TIỂU VẬN (Antardasha) ---")
            W(f"{'Tiểu vận':<12} {'Từ':<12} {'Đến':<12} {'Ý nghĩa':<30}")
            W("-" * 70)
            
            for ad in antardashas:
                marker = "🔴" if ad['is_current'] else " "
                meaning = DASHA_MEANINGS.get(ad['lord'], '')[:30]
                W(f"{ad['lord']:<12} {ad['start']:<12} {ad['end']:<12} {marker} {meaning}")
    else:
        W("ℹ️ Dasha chỉ tính cho Natal Chart (thêm --natal để tính Dasha)")
    
    # =============================================
    # 11. ASSET-SPECIFIC
    # =============================================
    W()
    W("=" * 75)
    W("📊 PHÂN TÍCH THEO ASSET")
    W("=" * 75)
    
    # Gold
    W()
    W("🥇 VÀNG (XAU/USD)")
    W("-" * 40)
    sun = b['Mặt Trời']
    venus = b['Kim']
    W(f"  ☀️ Mặt Trời ở {sun['sign']} | ♀️ Kim ở {venus['sign']}")
    
    if moon['elem'] in ["Đất", "Nước"]:
        W("  🌙 Moon trong cung Đất/Nước → Safe haven demand CAO, hỗ trợ Vàng")
    elif moon['elem'] == "Lửa":
        W("  🔥 Moon trong cung Lửa → Risk-on, Vàng có thể giảm hấp dẫn")
    elif moon['elem'] == "Khí":
        W("  💨 Moon trong cung Khí → Phân vân, Vàng sideways")
    
    # Bitcoin
    W()
    W("₿ BITCOIN (BTC/USD)")
    W("-" * 40)
    rahu = b['Rahu']
    uranus = o.get('Thiên Vương', {})
    W(f"  🐉 Rahu ở {rahu['sign']} | ⛧ Thiên Vương ở {uranus.get('sign', '?')}")
    
    if merc['spd'] < 0 or merc_combust:
        W("  ☿️ Mercury Rx/combust → Crypto biến động mạnh, false signals")
    else:
        W("  ☿️ Thủy thuận → Tín hiệu Crypto rõ ràng hơn")
    
    if uranus.get('si') == 10:  # Aquarius
        W("  ♇ Diêm Vương trong Bảo Bình → Era mới cho Crypto, AI, Decentralization")
    
    # =============================================
    # DISCLAIMER
    # =============================================
    W()
    W("=" * 75)
    W("⚠️ LƯU Ý:")
    W("  • Financial astrology là công cụ BỔ TRỢ, KHÔNG thay thế phân tích kỹ thuật")
    W("  • Correlation ≠ causation — hành tinh không 'gây ra' biến động")
    W("  • Luôn dùng stop loss, không risk quá 1-2% per trade")
    W("  • Đầu tư có rủi ro, tự chịu trách nhiệm")
    W("=" * 75)
    
    return "\n".join(lines)


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Financial Astrology — Day Trading Focus (M15/H1)')
    parser.add_argument('--tz', type=str, default='Asia/Tokyo')
    parser.add_argument('--date', type=str, default=None)
    parser.add_argument('--lat', type=float, default=34.9333)
    parser.add_argument('--lon', type=float, default=136.9667)
    parser.add_argument('--asset', type=str, default='all')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--natal', action='store_true', help='Calculate Dasha for natal chart')
    
    args = parser.parse_args()
    
    tz = ZoneInfo(args.tz)
    
    if args.date:
        dt_naive = datetime.strptime(args.date, '%Y-%m-%d %H:%M:%S')
        dt_display = dt_naive.replace(tzinfo=tz)
        dt_utc = dt_display.astimezone(timezone.utc)
    else:
        dt_display = datetime.now(tz)
        dt_utc = dt_display.astimezone(timezone.utc)
    
    data = calculate_all(dt_utc, args.lat, args.lon, is_natal=args.natal)
    
    if args.json:
        print(json.dumps(data, default=str, ensure_ascii=False))
    else:
        print(format_output(data, dt_display, args.tz, args.lat, args.lon))

if __name__ == '__main__':
    main()
