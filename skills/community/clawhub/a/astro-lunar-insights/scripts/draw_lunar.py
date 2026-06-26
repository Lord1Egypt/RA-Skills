#!/usr/bin/env python3
"""
astro-lunar-insights: Lunar Chart Renderer
2-panel layout: Left (wide) = 2 wheels stacked, Right (narrow) = text panel
Style matches astro-natal-chart: dark background, element-colored sectors,
planet circles with letter codes, aspect lines, legend.
"""

import json, math, os, subprocess, sys, argparse, shutil

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont

# в”Ђв”Ђ Font + binary setup в”Ђв”Ђ
# ClawHub doesn't allow .ttf/.pyd files, so we ship them as .dat and copy at runtime
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
for _f in os.listdir(_SKILL_DIR):
    if _f.endswith('.dat'):
        _src = os.path.join(_SKILL_DIR, _f)
        _dst = _src[:-4]  # strip .dat
        if not os.path.exists(_dst):
            shutil.copy2(_src, _dst)
        elif os.path.getmtime(_src) > os.path.getmtime(_dst):
            shutil.copy2(_src, _dst)

_TTF_DIR = _SKILL_DIR
_SYM = os.path.join(_TTF_DIR, "seguisym.ttf")
_TXT = os.path.join(_TTF_DIR, "segoeuisl.ttf")

_FC = {}
def fnt(size, sym=False):
    k = (size, sym)
    if k in _FC:
        return _FC[k]
    fp = _SYM if sym else _TXT
    if os.path.exists(fp):
        try:
            _FC[k] = ImageFont.truetype(fp, size)
            return _FC[k]
        except:
            pass
    _FC[k] = ImageFont.load_default()
    return _FC[k]

# Symbols that should be rendered via the symbol font (seguisym.ttf)
# Zodiac signs, aspect glyphs, degree sign, prime/double-prime, retrograde
_SYM_SET = frozenset(
    [chr(c) for c in range(0x2648, 0x2654)]  # zodiac
    + [chr(c) for c in range(0x2609, 0x2648)]  # planet symbols Sun..Pluto
    + [chr(c) for c in range(0x25A1, 0x25B4)]  # square/trine range
    + ['\u2736']  # sextile
    + [chr(c) for c in range(0x26B9, 0x26BB)]  # quincunx/semisextile
    + ['\u2220']  # semisquare/sesquiquadrate
    + ['\u00B0']  # degree
    + ['\u2032', '\u2033']  # prime, double-prime
    + ['\u211E']  # retrograde
)

def is_z(ch):
    """Return True if character should be rendered via the symbol font."""
    return ch in _SYM_SET

def ch_w(ch, f):
    bb = f.getbbox(ch)
    return (bb[2] - bb[0]) if bb else 10

def rtext(draw, x, y, text, size, fill, cy=False):
    sf = fnt(size, sym=True)
    tf = fnt(size, sym=False)
    if cy:
        bb = tf.getbbox(text)
        y -= (bb[3] - bb[1]) // 2
    cx = x
    for ch in text:
        f = sf if is_z(ch) else tf
        draw.text((cx, y), ch, fill=fill, font=f)
        cx += ch_w(ch, f)

def rcent(draw, cx, y, text, size, fill, ox=0):
    sf = fnt(size, sym=True)
    tf = fnt(size, sym=False)
    tw = sum(ch_w(ch, sf if is_z(ch) else tf) for ch in text)
    x = cx - tw // 2 + ox
    for ch in text:
        f = sf if is_z(ch) else tf
        draw.text((x, y), ch, fill=fill, font=f)
        x += ch_w(ch, f)

# в”Ђв”Ђ Constants в”Ђв”Ђ
ZSYM = ['\u2648', '\u2649', '\u264a', '\u264b', '\u264c', '\u264d',
        '\u264e', '\u264f', '\u2650', '\u2651', '\u2652', '\u2653']
ZAB = ['AR', 'TA', 'GE', 'CN', 'LE', 'VI', 'LI', 'SC', 'SG', 'CP', 'AQ', 'PI']
ZEL = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
EL_COL = [(80, 30, 30), (30, 70, 30), (70, 70, 30), (30, 50, 80)]
SIG_COL = [(200, 60, 60), (80, 180, 70), (220, 190, 50), (70, 130, 220),
           (240, 170, 40), (100, 160, 80), (180, 90, 180), (160, 40, 70),
           (90, 110, 210), (100, 100, 100), (70, 170, 210), (60, 140, 140)]
EL_RU = ['Огонь', 'Земля', 'Воздух', 'Вода']
EL_EN = ['Fire', 'Earth', 'Air', 'Water']
SN_RU = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
         'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
SN_EN = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

PM = {
    "Sun": ("SU", (255, 220, 50), "Солнце", "Sun"),
    "Moon": ("MO", (210, 210, 220), "Луна", "Moon"),
    "Mercury": ("ME", (100, 210, 100), "Меркурий", "Mercury"),
    "Venus": ("VE", (80, 230, 170), "Венера", "Venus"),
    "Mars": ("MA", (230, 70, 50), "Марс", "Mars"),
    "Jupiter": ("JU", (210, 150, 60), "Юпитер", "Jupiter"),
    "Saturn": ("SA", (150, 150, 170), "Сатурн", "Saturn"),
    "Uranus": ("UR", (100, 210, 230), "Уран", "Uranus"),
    "Neptune": ("NE", (90, 140, 230), "Нептун", "Neptune"),
    "Pluto": ("PL", (170, 80, 80), "Плутон", "Pluto"),
}


ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']

# Planet name mapping: English -> Russian
PN_RU = {
    "Sun": "Солнце",
    "Moon": "Луна",
    "Mercury": "Меркурий",
    "Venus": "Венера",
    "Mars": "Марс",
    "Jupiter": "Юпитер",
    "Saturn": "Сатурн",
    "Uranus": "Уран",
    "Neptune": "Нептун",
    "Pluto": "Плутон",
}


# Aspect colors matching natal chart style
ASP_COLORS = {
    'Conjunction': (200, 200, 200),
    'Sextile':     (100, 180, 240),
    'Square':      (220, 80, 80),
    'Trine':       (80, 220, 80),
    'Quincunx':    (180, 160, 60),
    'Opposition':  (240, 140, 40),
    'Semisextile': (150, 150, 100),
    'Semisquare':  (150, 100, 100),
    'Sesquiquadrate': (150, 100, 100),
}

# в”Ђв”Ђ Geometry helpers в”Ђв”Ђ
def aof(d):
    return math.radians(90.0 - float(d))

def ppos(cx, cy, r, d):
    a = aof(d)
    return cx + r * math.cos(a), cy - r * math.sin(a)

# в”Ђв”Ђ Draw natal-style wheel в”Ђв”Ђ
def draw_wheel(img, dw, cx, cy, RO, RS, RH, RP, RI, natal_data, transit_moon_lon,
               transit_moon_speed, all_aspects, lang, title, is_moon_wheel=False):
    """Draw a natal-style wheel with planets, houses, aspects, legend."""
    R = (lang == 'ru')
    SN = SN_RU if R else SN_EN
    EL = EL_RU if R else EL_EN

    houses = natal_data['houses']
    asc_deg = natal_data['ASC']['lon']
    mc_deg = natal_data['MC']['lon']

    # Outer circle background
    dw.ellipse((cx - RO, cy - RO, cx + RO, cy + RO), fill=(16, 16, 36), outline=(80, 80, 130), width=4)

    # Sign sectors (element-colored)
    asc_sign_idx = int(asc_deg // 30) % 12
    sector_start = asc_sign_idx * 30
    for i in range(12):
        sd = sector_start + i * 30
        ed = sector_start + (i + 1) * 30
        sign_idx = (asc_sign_idx + i) % 12
        col = EL_COL[ZEL[sign_idx]]
        pts = [(cx, cy)]
        for j in range(41):
            d = sd + (ed - sd) * j / 40
            a = math.radians(90.0 - d)
            pts.append((cx + RO * math.cos(a), cy - RO * math.sin(a)))
        dw.polygon(pts, fill=col)
    dw.ellipse((cx - RO, cy - RO, cx + RO, cy + RO), outline=(180, 180, 210), width=4)

    # Sign boundary lines + zodiac symbols
    for i in range(12):
        dc = sector_start + i * 30
        ax, ay = ppos(cx, cy, RO - 6, dc)
        bx, by = ppos(cx, cy, RS - 18, dc)
        dw.line([(int(ax), int(ay)), (int(bx), int(by))], fill=(160, 160, 190), width=2)
        mid_dc = sector_start + i * 30 + 15
        si = (asc_sign_idx + i) % 12
        lx, ly = ppos(cx, cy, RS, mid_dc)
        rcent(dw, int(lx), int(ly), ZSYM[si], 38, SIG_COL[si])

    # House cusp lines + Roman numerals
    for i in range(12):
        dc = float(houses[i])
        ax, ay = ppos(cx, cy, RI + 12, dc)
        bx, by = ppos(cx, cy, RH, dc)
        dw.line([(int(ax), int(ay)), (int(bx), int(by))], fill=(90, 130, 190), width=2)
        nc = float(houses[(i + 1) % 12])
        mid = dc + (nc - dc) / 2 if nc > dc else (dc + (nc + 360 - dc) / 2) % 360
        hnx, hny = ppos(cx, cy, RH + 48, mid)
        rcent(dw, int(hnx), int(hny), ROMAN[i], 20, (140, 170, 210))

    # ASC/MC lines
    asc_label = "АСЦ" if R else "ASC"
    mc_label = "МС" if R else "MC"
    for lbl, dg, col in [(asc_label, asc_deg, (255, 255, 120)), (mc_label, mc_deg, (255, 200, 100))]:
        ax, ay = ppos(cx, cy, RI, dg)
        bx, by = ppos(cx, cy, RO - 4, dg)
        dw.line([(int(ax), int(ay)), (int(bx), int(by))], fill=col, width=6)
        lx, ly = ppos(cx, cy, RO + 36, dg)
        rcent(dw, int(lx), int(ly), lbl, 22, col)

    # Inner circle
    dw.ellipse((cx - RI, cy - RI, cx + RI, cy + RI), outline=(90, 90, 140), width=2)

    # в”Ђв”Ђ Planets в”Ђв”Ђ
    pp_main = []
    for pn, pd in natal_data.items():
        if pn in ('houses', 'ASC', 'MC'):
            continue
        if pn not in PM:
            continue
        ab, cl, nr, ne = PM[pn]
        ln = pd['lon']
        rt = pd['retro']
        px, py = ppos(cx, cy, RP, ln)
        pp_main.append((pn, ab, cl, nr, ne, ln, rt, int(px), int(py)))

    # Draw aspect lines first (behind planets)
    for a in all_aspects:
        if not a['major']:
            continue
        d1 = next(((pl, px, py) for pl, ab, cl, nr, ne, ln, rt, px, py in pp_main if pl == a['natal']), None)
        if d1:
            # Transit Moon is always the other planet
            tm_px, tm_py = ppos(cx, cy, RP, transit_moon_lon)
            col = ASP_COLORS.get(a['aspect'], (150, 150, 150))
            dw.line([(d1[1], d1[2]), (tm_px, tm_py)], fill=col, width=2)

    # Draw planet circles with letter codes
    for pn, ab, cl, nr, ne, ln, rt, px, py in pp_main:
        r = 18
        dw.ellipse((int(px) - r, int(py) - r, int(px) + r, int(py) + r),
                   fill=cl, outline=(255, 255, 255), width=3)
        nm = nr if R else ne
        rcent(dw, int(px), int(py) - 42, ab + ('(R)' if rt else ''), 17, cl)

    # в”Ђв”Ђ Transit Moon (highlighted, outer orbit) в”Ђв”Ђ
    if is_moon_wheel:
        tm_r = RP + 80
        tm_px, tm_py = ppos(cx, cy, tm_r, transit_moon_lon)
        # Glow
        for gr in range(28, 8, -3):
            alpha = max(20, 80 - gr * 2)
            glow_col = (200, 200, 255)
            dw.ellipse((int(tm_px) - gr, int(tm_py) - gr, int(tm_px) + gr, int(tm_py) + gr),
                       fill=glow_col)
        # Circle
        r = 22
        dw.ellipse((int(tm_px) - r, int(tm_py) - r, int(tm_px) + r, int(tm_py) + r),
                   fill=(255, 255, 220), outline=(255, 255, 255), width=3)
        rcent(dw, int(tm_px), int(tm_py) - 46, "MO", 17, (255, 220, 100))
        tm_label = "ТРАНЗИТ" if R else "TRANSIT"
        rcent(dw, int(tm_px), int(tm_py) + 28, tm_label, 15, (255, 255, 220))

    # в”Ђв”Ђ Title above wheel в”Ђв”Ђ
    title_y = cy - RO - 80
    rcent(dw, cx, title_y, title, 22, (255, 220, 100))

    # в”Ђв”Ђ Legend below wheel: 3 groups side by side в”Ђв”Ђ
    LEG_TOP = cy + RO + 12
    grp_w = (RO * 2) // 3  # each group gets 1/3 of total width
    SN = SN_RU if R else SN_EN
    EL = EL_RU if R else EL_EN
    gh = 22  # row height
    # All groups same height = tallest group (aspects: 6 items + title + padding)
    UNIFORM_H = gh * 7 + 10  # 154px, fits all groups

    # в”Ђв”Ђ Group 1: Planets (vertical list, 2 columns if needed) в”Ђв”Ђ
    gx = cx - RO
    gy = LEG_TOP
    n_planets = len(pp_main)
    n_cols = 2 if n_planets > 6 else 1
    n_rows = (n_planets + n_cols - 1) // n_cols
    col_w = (grp_w - 4) // n_cols
    dw.rectangle((gx, gy, gx + grp_w - 4, gy + UNIFORM_H),
                 fill=(12, 12, 28), outline=(60, 60, 100), width=2)
    pl_title = "ПЛАНЕТЫ" if R else "PLANETS"
    rtext(dw, gx + 6, gy + 3, pl_title, 15, (200, 200, 220))
    for idx, (pn, ab, cl, nr, ne, ln, rt, px, py) in enumerate(pp_main):
        col = idx // n_rows
        row = idx % n_rows
        rx = gx + 6 + col * col_w
        ry = gy + gh + row * gh + 3
        si = int(ln // 30)
        nm = nr if R else ne
        lbl = f"{ZSYM[si]} {ab} {nm}"
        if rt:
            lbl += " R"
        dw.ellipse((rx, ry, rx + 12, ry + 12), fill=cl, outline=(255, 255, 255), width=1)
        rtext(dw, rx + 16, ry, lbl, 12, cl)

    # в”Ђв”Ђ Group 2: Aspects (vertical list) в”Ђв”Ђ
    gx2 = cx - RO + grp_w
    gy2 = LEG_TOP
    dw.rectangle((gx2, gy2, gx2 + grp_w - 4, gy2 + UNIFORM_H),
                 fill=(12, 12, 28), outline=(60, 60, 100), width=2)
    asp_title = "АСПЕКТЫ" if R else "ASPECTS"
    rtext(dw, gx2 + 6, gy2 + 3, asp_title, 15, (200, 200, 220))
    ail = [
        ((200, 200, 200), "\u260c", "Conj"),
        ((100, 180, 240), "\u2736", "Sext"),
        ((220, 80, 80), "\u25a1", "Sqr"),
        ((80, 220, 80), "\u25b3", "Trine"),
        ((180, 160, 60), "\u26b9", "Qnc"),
        ((240, 140, 40), "\u260d", "Opp"),
    ]
    for ai, (ac, al, albl) in enumerate(ail):
        ry = gy2 + gh + ai * gh + 3
        dw.rectangle((gx2 + 6, ry + 1, gx2 + 18, ry + 13), fill=ac)
        rtext(dw, gx2 + 22, ry, f"{al} {albl}", 13, ac)

    # в”Ђв”Ђ Group 3: Elements (vertical list) в”Ђв”Ђ
    gx3 = cx - RO + grp_w * 2
    gy3 = LEG_TOP
    dw.rectangle((gx3, gy3, gx3 + grp_w - 4, gy3 + UNIFORM_H),
                 fill=(12, 12, 28), outline=(60, 60, 100), width=2)
    el_title = "СТИХИИ" if R else "ELEMENTS"
    rtext(dw, gx3 + 6, gy3 + 3, el_title, 15, (200, 200, 220))
    for ei in range(4):
        ry = gy3 + gh + ei * gh + 3
        enm = EL[ei]
        dw.rectangle((gx3 + 6, ry + 1, gx3 + 18, ry + 13), fill=EL_COL[ei])
        rtext(dw, gx3 + 22, ry, enm, 13, (200, 200, 200))


# в”Ђв”Ђ Text panel в”Ђв”Ђ
def draw_text_panel(img, dw, x0, y0, w, h, data, lang, frame_img=None):
    """Draw the right-side text interpretation panel with colored planet names and aspect types."""
    R = (lang == 'ru')

    # Background
    dw.rectangle((x0, y0, x0 + w, y0 + h), fill=(10, 10, 22), outline=(60, 60, 100), width=2)

    x = x0 + 20
    _y = [y0 + 15]
    max_w = w // 2 - 20  # half width for faster wrapping

    # Font sizes matching natal chart: FS=19, FM=22, FL=26, LH=22
    FS = 19  # body text
    FM = 22  # medium (subheads)
    FL = 26  # large (main header)
    LH = 22  # line height

    # Thin divider color
    DIVIDER_COL = (50, 50, 80)

    # Planet color mapping (Russian/English names -> RGB)
    PLANET_COLORS = {}
    for _pn, (_ab, _cl, _nr, _ne) in PM.items():
        PLANET_COLORS[_nr] = _cl
        PLANET_COLORS[_ne] = _cl

    # Aspect color mapping (lowercase name -> RGB)
    ASP_COLORS_LOCAL = {}
    for _an, _ac in ASP_COLORS.items():
        ASP_COLORS_LOCAL[_an.lower()] = _ac
        ASP_COLORS_LOCAL[_an] = _ac
    # Aspect symbol -> color map (for rendering aspect glyphs in text)
    ASP_SYMBOL_COLORS = {
        '\u260c': (200, 200, 200),  # Conjunction
        '\u260d': (240, 140, 40),   # Opposition
        '\u25a1': (220, 80, 80),    # Square
        '\u25b3': (80, 220, 80),    # Trine
        '\u2736': (100, 180, 240),  # Sextile
        '\u26b9': (180, 160, 60),   # Quincunx
        '\u26ba': (150, 150, 100),  # Semisextile
        '\u2220': (150, 100, 100),  # Semisquare / Sesquiquadrate
    }

    def _get_word_color(word):
        c = PLANET_COLORS.get(word)
        if c:
            return c
        c = ASP_COLORS_LOCAL.get(word.lower())
        if c:
            return c
        return ASP_SYMBOL_COLORS.get(word)

    def _adv(n=1):
        _y[0] += n

    def _draw_colored_line(text, size, default_color):
        """Draw a single line with per-word color coding."""
        sf = fnt(size, sym=True)
        tf = fnt(size, sym=False)
        words = text.split()
        cx = x
        space_w = ch_w(' ', tf)
        for i, wd in enumerate(words):
            wc = _get_word_color(wd) or default_color
            stripped = wd.strip('.,;:!?')
            if stripped != wd:
                wc2 = _get_word_color(stripped) or default_color
            else:
                wc2 = wc
            for ch in wd:
                f = sf if is_z(ch) else tf
                dw.text((cx, _y[0]), ch, fill=wc2, font=f)
                cx += ch_w(ch, f)
            if i < len(words) - 1:
                dw.text((cx, _y[0]), ' ', fill=default_color, font=tf)
                cx += space_w
        _adv(LH)

    def _wrap_multiline(line_text, size, max_width, default_color):
        """Word-wrap a long line, then draw each wrapped line."""
        tf = fnt(size, sym=False)
        words = line_text.split()
        cur = ""
        for wd in words:
            if cur:
                test_bb = tf.getbbox(cur + " " + wd)
                tw = (test_bb[2] - test_bb[0]) if test_bb else 0
                if tw <= max_width:
                    cur = cur + " " + wd
                    continue
                _draw_colored_line(cur, size, default_color)
                cur = wd
            else:
                cur = wd
        if cur:
            _draw_colored_line(cur, size, default_color)

    def text(line, sz=FS, color=(220, 220, 240)):
        _wrap_multiline(line, sz, max_w, color)

    def small(line, color=(180, 180, 200)):
        _wrap_multiline(line, FS - 5, max_w, color)

    def header(line, color=(255, 220, 100)):
        _wrap_multiline(line, FL, max_w, color)
        _adv(6)

    def subhead(line, color=(180, 200, 255)):
        _wrap_multiline(line, FM, max_w, color)
        _adv(3)

    def wrapped(line, sz=FS, color=(200, 200, 220)):
        _wrap_multiline(line, sz, max_w, color)

    def spacer(s=8):
        _adv(s)

    def check(needed):
        return _y[0] + needed < y0 + h - 20

    def metric_divider():
        """Draw a thin horizontal line across 2/3 of text block width, from left edge."""
        div_w = int(max_w * 2 / 3)
        _adv(4)
        dw.line([(x, _y[0]), (x + div_w, _y[0])], fill=DIVIDER_COL, width=1)
        _adv(8)

    # в”Ђв”Ђ Helper: extract interpretation text from conclusion[mkey] в”Ђв”Ђ
    conclusion_data = data.get('conclusion', {})
    is_ai = 'overall' in conclusion_data

    def interp_text(mkey):
        val = conclusion_data.get(mkey)
        if isinstance(val, str):
            return val
        if isinstance(val, list):
            # For transit_moon_aspects list: build readable summary
            if mkey == 'transit_moon_aspects' and len(val) > 0 and isinstance(val[0], dict):
                # Aspect name -> Unicode symbol mapping
                ASP_TO_SYM = {
                    'Conjunction': '\u260c', 'Opposition': '\u260d',
                    'Square': '\u25a1', 'Trine': '\u25b3',
                    'Sextile': '\u2736', 'Quincunx': '\u26b9',
                    'Semisextile': '\u26ba', 'Semisquare': '\u2220',
                    'Sesquiquadrate': '\u2220',
                }
                parts = []
                for a in val:
                    asp = a.get('aspect', '?')
                    nat = a.get('natal', '?')
                    orb = a.get('orb', 0)
                    retro = ' R' if a.get('natal_retro') else ''
                    sym = ASP_TO_SYM.get(asp, asp)
                    nat_name = PN_RU.get(nat, nat) if R else nat
                    transit_name = '\u041b\u0443\u043d\u0430' if R else 'Moon'
                    if R:
                        parts.append('{transit} {sym} {nat} (\u043e\u0440\u0431 {orb:.1f}\u00b0){retro}'.format(
                            transit=transit_name, sym=sym, nat=nat_name, orb=orb, retro=retro))
                    else:
                        parts.append('Moon {sym} {nat} (orb {orb:.1f}\u00b0){retro}'.format(
                            sym=sym, nat=nat, orb=orb, retro=retro))
                return ', '.join(parts)
            return ' '.join(str(x) for x in val)
        if not isinstance(val, dict):
            return ''
        raw = val.get('interpretation', '')
        if not raw:
            return ''
        if isinstance(raw, dict):
            if 'interpretation' in raw:
                return str(raw['interpretation'])
            return raw.get('description', str(raw))
        elif isinstance(raw, (tuple, list)):
            if len(raw) >= 2 and all(isinstance(x, str) for x in raw[:2]):
                return f"{raw[0]}: {raw[1]}"
            return ' '.join(str(x) for x in raw)
        return str(raw)

    def show_interp(mkey, limit=None):
        txt = interp_text(mkey)
        if not txt:
            return
        if is_ai:
            wrapped(txt)
        else:
            wrapped(txt[:limit] if limit else txt)

    # в”Ђв”Ђ Titles / Labels
    if R:
        T1 = '\u0424\u0410\u0417\u0410 \u041b\u0423\u041d\u042b'
        T2 = '\u0411\u041b\u0418\u0416\u0410\u0419\u0428\u0418\u0415 \u0424\u0410\u0417\u042b'
        T3 = '\u041b\u0423\u041d\u041d\u042b\u0419 \u0414\u0415\u041d\u042c'
        T4 = '\u041b\u0423\u041d\u0410 \u041a \u041d\u0410\u0422\u0410\u041b\u042c\u041d\u041e\u0419'
        T5 = '\u041f\u0415\u0420\u0421\u041e\u041d\u0410\u041b\u042c\u041d\u0410\u042f \u0424\u0410\u0417\u0410'
        T6 = '\u041b\u0423\u041d\u0410 \u0412 \u0414\u041e\u041c\u0415'
        T7 = '\u0421\u041a\u041e\u0420\u041e\u0421\u0422\u042c \u041b\u0423\u041d\u042b'
        T8 = '\u0410\u0421\u041f\u0415\u041a\u0422\u042b'
        T9 = '\u0417\u0410\u041a\u041b\u042e\u0427\u0415\u041d\u0418\u0415'
        TP = '\u041f\u043b\u0430\u043d\u0435\u0442\u044b'
        TE = '\u042d\u043d\u0435\u0440\u0433\u0438\u044f'
        TI = '\u0418\u043d\u0442\u0435\u043d\u0441\u0438\u0432\u043d\u043e\u0441\u0442\u044c'
        TD = '\u0434\u0435\u043d\u044c'
        dir_in = '\u0447\u0435\u0440\u0435\u0437'
        dir_ago = '\u043d\u0430\u0437\u0430\u0434'
    else:
        T1 = 'MOON PHASE'
        T2 = 'NEAREST PHASES'
        T3 = 'LUNAR DAY'
        T4 = 'MOON TO NATAL MOON'
        T5 = 'PERSONAL PHASE'
        T6 = 'MOON IN HOUSE'
        T7 = 'MOON SPEED'
        T8 = 'ASPECTS'
        T9 = 'CONCLUSION'
        TP = 'Planets'
        TE = 'Energy'
        TI = 'Intensity'
        TD = 'day'
        dir_in = 'in'
        dir_ago = 'ago'

    # Title
    name = data.get('name', '')
    title = ('\u041b\u0423\u041d\u041d\u042b\u0419 \u0410\u041d\u0410\u041b\u0418\u0417: ' + name) if R else ('LUNAR ANALYSIS: ' + name)
    header(title)
    small(data.get('birth_date', '') + ' ' + data.get('birth_time', '') + ' | ' + data.get('target_date', ''))
    if conclusion_data.get('_autonomous'):
        small('\u0410\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u0430\u044f \u0438\u043d\u0442\u0435\u0440\u043f\u0440\u0435\u0442\u0430\u0446\u0438\u044f' if R else 'Autonomous interpretation')
    elif is_ai:
        small('AI \u0438\u043d\u0442\u0435\u0440\u043f\u0440\u0435\u0442\u0430\u0446\u0438\u044f' if R else 'AI interpretation')
    spacer()

    # 1. Moon phase
    mp = data['moon_phase']
    subhead('1. ' + T1)
    text('{nm} | {el}\u00b0 | {il}%'.format(nm=mp['name'], el=format(mp['elongation'], '.1f'), il=format(mp['illumination'], '.1f')))
    show_interp('moon_phase', limit=400)
    metric_divider()

    # 2. Nearest phases
    subhead('2. ' + T2)
    for pn, pd in data['nearest_phases'].items():
        dd = pd['days_diff']
        direction = dir_in if dd > 0 else dir_ago
        small(pn + ': ' + pd['date'] + ' (' + format(abs(dd), '.1f') + 'd ' + direction + ')')
    show_interp('nearest_phases', limit=200)
    metric_divider()

    # 3. Lunar day
    ld = data['lunar_day']
    subhead('3. ' + T3 + ' ' + str(ld['number']) + '/30')
    show_interp('lunar_day', limit=200)
    metric_divider()

    # 4. Transit Moon -> Natal Moon
    tm = data['transit_moon_to_natal_moon']
    subhead('4. ' + T4)
    if tm['aspect']:
        text(tm['aspect'] + ' (orb ' + str(tm['orb']) + '\u00b0)')
    show_interp('transit_moon_to_natal_moon', limit=400)
    metric_divider()

    # 5. Personal phase
    pp = data['personal_phase']
    subhead('5. ' + T5)
    text(format(pp['elongation'], '.1f') + '\u00b0')
    show_interp('personal_phase', limit=400)
    metric_divider()

    # 6. Transit Moon house
    mh = data['transit_moon_house']
    subhead('6. ' + T6 + ' ' + str(mh['house']))
    show_interp('transit_moon_house', limit=400)
    if mh['natal_planets_in_house']:
        # Use Russian planet names if lang=ru
        if R:
            pnames_ru = ', '.join([PN_RU.get(p['name'], p['name']) for p in mh['natal_planets_in_house']])
            small(TP + ': ' + pnames_ru)
        else:
            pnames = ', '.join([p['name'] for p in mh['natal_planets_in_house']])
            small(TP + ': ' + pnames)
    metric_divider()

    # 7. Moon speed
    ms = data['moon_speed']
    subhead('7. ' + T7)
    text(format(ms['speed'], '.2f') + '\u00b0/' + TD)
    show_interp('moon_speed', limit=200)
    metric_divider()

    # 8. Aspects
    # Symbol map: aspect name -> symbol char (rendered via seguisym.ttf)
    ASP_SYM = {
        'Conjunction':    '\u260c',
        'Opposition':     '\u260d',
        'Square':         '\u25a1',
        'Trine':          '\u25b3',
        'Sextile':        '\u2736',
        'Quincunx':       '\u26b9',
        'Semisextile':    '\u26ba',
        'Semisquare':     '\u2220',
        'Sesquiquadrate': '\u2220',
    }
    subhead('8. ' + T8)
    for a in data['transit_moon_aspects'][:12]:
        if not check(20):
            break
        marker = '*' if a['major'] else ' '
        retro_s = ' R' if a['natal_retro'] else ''
        sym = ASP_SYM.get(a['aspect'], '?')
        # Use Russian planet names if lang=ru
        nat_name = PN_RU.get(a['natal'], a['natal']) if R else a['natal']
        transit_moon_name = '\u041b\u0443\u043d\u0430' if R else 'Moon'
        # Build line: marker + transit_moon + aspect_sym + natal_planet + orb
        orb_text = '(orb ' + format(a['orb'], '.1f') + '\u00b0)' + retro_s
        aspect_line_text = '  ' + marker + ' ' + transit_moon_name + ' ' + sym + ' ' + nat_name.ljust(10) + ' ' + orb_text
        _draw_colored_line(aspect_line_text, FS - 5, (180, 180, 200))
    show_interp('transit_moon_aspects', limit=400)
    metric_divider()

    # 9. Conclusion вЂ” ALWAYS show, styled like natal chart
    if 'conclusion' in data:
        spacer(12)
        # Top decorative line removed (kept conc_line_x for bottom line)
        conc_line_w = int(max_w * 0.85)
        conc_line_x = x + (max_w - conc_line_w) // 2
        _adv(LH + 10)
        # Title
        conc_title_color = (255, 215, 0)
        _wrap_multiline('9. ' + T9, FL, max_w, conc_title_color)
        _adv(10)
        # Body text
        conclusion = data['conclusion']
        if conclusion.get('_autonomous'):
            summary = conclusion.get('summary', {})
            wrapped(TE + ': ' + summary.get('cycle_energy', ''))
            wrapped(TI + ': ' + summary.get('intensity', ''))
        elif is_ai:
            # Render AI conclusion with plain text font only (no sym font mixing)
            tf = fnt(FS - 1, sym=False)
            ai_text = conclusion['overall']
            words = ai_text.split()
            cur = ""
            for wd in words:
                if cur:
                    test_bb = tf.getbbox(cur + " " + wd)
                    tw = (test_bb[2] - test_bb[0]) if test_bb else 0
                    if tw <= max_w:
                        cur = cur + " " + wd
                        continue
                    dw.text((x, _y[0]), cur, fill=(240, 230, 200), font=tf)
                    _adv(LH)
                    cur = wd
                else:
                    cur = wd
            if cur:
                dw.text((x, _y[0]), cur, fill=(240, 230, 200), font=tf)
                _adv(LH)
        # Bottom decorative line
        _adv(8)
        if _y[0] < y0 + h - 40:
            dw.line([(conc_line_x + 30, _y[0]), (conc_line_x + conc_line_w - 30, _y[0])], fill=(120, 100, 60), width=1)
            _adv(14)

        # ClawHub link
        if _y[0] < y0 + h - 50:
            _adv(10)
            clawhub_url = "https://clawhub.ai/dynamicsalex/astro-lunar-insights"
            tf_url = fnt(FS - 2, sym=False)
            url_bb = tf_url.getbbox(clawhub_url)
            url_tw = (url_bb[2] - url_bb[0]) if url_bb else 0
            url_x = x + (max_w - url_tw) // 2
            dw.text((url_x, _y[0]), clawhub_url, fill=(80, 80, 120), font=tf_url)

        # Frame image (QR code for donations) — placed after conclusion, right-aligned to text block edge
        if frame_img is not None:
            _adv(14)
            frame_w = frame_img.size[0]
            frame_h = frame_img.size[1]
            # Right-align to the text block right edge (x + max_w)
            frame_x = x + max_w - frame_w
            frame_y = _y[0]
            qr_rgb = frame_img.convert('RGB')
            img.paste(qr_rgb, (frame_x, frame_y))
            _y[0] += frame_h + 10




# в”Ђв”Ђ Draw simple moon phase wheel (original style) в”Ђв”Ђ
def draw_phase_wheel(img, dw, cx, cy, RO, elongation, illumination, fonts, lang):
    """Draw the original-style moon phase wheel вЂ” simple circle with illuminated portion."""
    R = (lang == 'ru')

    # Background circle
    dw.ellipse((cx - RO, cy - RO, cx + RO, cy + RO),
               fill=(15, 15, 35), outline=(80, 80, 120), width=3)

    # Draw illuminated portion (line-based fill)
    for i in range(360):
        angle = math.radians(i)
        phase_angle = math.radians(elongation)
        cos_angle = math.cos(angle - phase_angle)
        if elongation <= 180:
            if cos_angle > 0:
                x1 = cx + RO * math.cos(angle)
                y1 = cy - RO * math.sin(angle)
                x2 = cx + RO * 0.85 * math.cos(angle)
                y2 = cy - RO * 0.85 * math.sin(angle)
                dw.line([(x1, y1), (x2, y2)], fill=(200, 200, 180), width=2)
        else:
            if cos_angle < 0:
                x1 = cx + RO * math.cos(angle)
                y1 = cy - RO * math.sin(angle)
                x2 = cx + RO * 0.85 * math.cos(angle)
                y2 = cy - RO * 0.85 * math.sin(angle)
                dw.line([(x1, y1), (x2, y2)], fill=(200, 200, 180), width=2)

    # Outer ring with sign divisions
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        x1 = cx + (RO + 10) * math.cos(angle)
        y1 = cy + (RO + 10) * math.sin(angle)
        x2 = cx + (RO + 25) * math.cos(angle)
        y2 = cy + (RO + 25) * math.sin(angle)
        dw.line([(x1, y1), (x2, y2)], fill=(100, 100, 150), width=2)

    # Phase labels
    label_r = RO + 55
    if R:
        phase_labels = [(0, "0°", "Новолуние"), (90, "90°", "1-я четверть"),
                        (180, "180°", "Полнолуние"), (270, "270°", "3-я четверть")]
    else:
        phase_labels = [(0, "0°", "New Moon"), (90, "90°", "1st Quarter"),
                        (180, "180°", "Full Moon"), (270, "270°", "3rd Quarter")]
    for deg, deg_label, name in phase_labels:
        angle = math.radians(deg - 90)
        lx = cx + label_r * math.cos(angle)
        ly = cy + label_r * math.sin(angle)
        rcent(dw, int(lx), int(ly), f"{deg_label}\n{name}", 16, (150, 150, 180))

    # Current phase indicator
    phase_angle = math.radians(elongation - 90)
    px = cx + (RO - 30) * math.cos(phase_angle)
    py = cy + (RO - 30) * math.sin(phase_angle)
    dw.ellipse([int(px) - 15, int(py) - 15, int(px) + 15, int(py) + 15],
               fill=(255, 220, 100), outline=(255, 255, 200), width=2)

    # Center illumination
    rcent(dw, cx, cy, f"{illumination:.0f}%", 32, (255, 255, 220))

    # Title above wheel вЂ” raised higher
    title = "ФАЗА ЛУНЫ" if R else "MOON PHASE"
    rcent(dw, cx, cy - RO - 80, title, 22, (255, 220, 100))

    # No legend for phase wheel вЂ” it's self-explanatory
    # (phase circle with illumination % in center)


# в”Ђв”Ђ Main render в”Ђв”Ђ
def render_chart(data, output_path, lang="en", frame_img=None):
    """Render 5760x2880 chart: left = 2 wheels side by side, right = text panel."""
    R = (lang == 'ru')

    TOT_W = 5760
    TOT_H = 2880

    # Layout:
    # Left panel: 2 wheels side by side (each ~2160px wide)
    # Right panel: text interpretation (remaining width)
    WHEEL_SIZE = 1700  # each wheel gets this much width
    LEFT_W = WHEEL_SIZE * 2  # 3400
    RIGHT_W = TOT_W - LEFT_W  # 2360

    WHEEL_R = 640  # radius for natal wheel
    PHASE_R = 640  # radius for phase wheel

    # Wheel Y center: circles centered vertically in image
    # R=640, so bottom = 1440+640=2080, legend fits below (2880-2080=800px)
    WHEEL_CY = TOT_H // 2  # vertical center

    img = Image.new('RGB', (TOT_W, TOT_H), (8, 8, 20))
    dw = ImageDraw.Draw(img)

    # в”Ђв”Ђ LEFT PANEL: 2 wheels side by side в”Ђв”Ђ
    wheel1_cx = WHEEL_SIZE // 2  # phase wheel center
    wheel1_cy = WHEEL_CY
    wheel2_cx = WHEEL_SIZE + WHEEL_SIZE // 2  # natal wheel center
    wheel2_cy = WHEEL_CY

    # Prepare natal data
    natal_for_draw = {}
    for pn in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
               'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']:
        natal_for_draw[pn] = {
            'lon': data['_natal'][pn]['lon'],
            'retro': data['_natal'][pn]['retro'],
        }
    natal_for_draw['ASC'] = {'lon': data['_natal']['ASC']['lon']}
    natal_for_draw['MC'] = {'lon': data['_natal']['MC']['lon']}
    natal_for_draw['houses'] = data['_natal']['houses']

    transit_moon_lon = data['transit_moon']['lon']
    transit_moon_speed = data['transit_moon']['speed']
    all_aspects = data['transit_moon_aspects']

    # Wheel 1: Moon phase wheel (original simple style)
    phase_elong = data['moon_phase']['elongation']
    phase_illum = data['moon_phase']['illumination']
    draw_phase_wheel(img, dw, wheel1_cx, wheel1_cy, PHASE_R,
                     phase_elong, phase_illum, None, lang)

    # Wheel 2: Natal wheel with transit Moon
    natal_title = "НАТАЛЬНОЕ КОЛЕСО" if R else "NATAL CHART"
    RO = WHEEL_R
    RS = RO - 62
    RH = RO - 124
    RP = RO - 270
    RI = RO - 460
    draw_wheel(img, dw, wheel2_cx, wheel2_cy, RO, RS, RH, RP, RI,
               natal_for_draw, transit_moon_lon, transit_moon_speed,
               all_aspects, lang, natal_title, is_moon_wheel=True)

    # RIGHT PANEL: Text interpretation
    draw_text_panel(img, dw, LEFT_W, 0, RIGHT_W, TOT_H, data, lang, frame_img)

    # Divider
    dw.line([(LEFT_W, 0), (LEFT_W, TOT_H)], fill=(80, 80, 120), width=3)

    # Save
    img.save(output_path, 'PNG')
    print(f"Saved: {output_path} ({TOT_W}x{TOT_H})")


# в”Ђв”Ђ CLI в”Ђв”Ђ
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["en", "ru"], default="en")
    parser.add_argument("--name", default="")
    parser.add_argument("--conclusion", default="", help="Path to JSON file with AI conclusion")
    parser.add_argument("--target-date", default="", help="Target date DD.MM.YYYY (default: today)")
    parser.add_argument("date", nargs="?", default="24.04.1983")
    parser.add_argument("time", nargs="?", default="07:00")
    parser.add_argument("city", nargs="?", default="РР¶РµРІСЃРє")
    parser.add_argument("--frame", default=None, help="Path to frame image .png.dat (QR code) to embed after conclusion. Default: bundled frame_small.png.dat")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load frame image (QR code). Default: bundled frame_small.png.dat
    frame_img = None
    frame_path = args.frame
    if frame_path is None:
        # Use bundled QR code
        frame_path = os.path.join(script_dir, "frame_small.png.dat")
    else:
        # Resolve user-provided path: if relative, look relative to skill directory
        if not os.path.isabs(frame_path):
            frame_path = os.path.join(script_dir, frame_path)
    frame_path = os.path.normpath(frame_path)
    if os.path.exists(frame_path):
        try:
            frame_img = Image.open(frame_path)
            print(f"Frame loaded: {frame_img.size} from {frame_path}")
        except Exception as e:
            print(f"Warning: could not load frame image: {e}")
    else:
        print(f"Warning: frame not found at {frame_path}")

    # Build analysis args
    analysis_args = [args.date, args.time, args.city, "--lang", args.lang, "--json"]
    if args.name:
        analysis_args += ["--name", args.name]
    if args.conclusion:
        analysis_args += ["--conclusion", args.conclusion]
    if args.target_date:
        analysis_args += ["--target-date", args.target_date]

    # Get JSON data вЂ” write to temp file to avoid console encoding issues
    import tempfile
    tmp_json = os.path.join(tempfile.gettempdir(), "lunar_analysis_tmp.json")
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    res = subprocess.run(
        [sys.executable, os.path.join(script_dir, "lunar_analysis.py")] + analysis_args + ["--output", tmp_json],
        capture_output=True, text=True, timeout=30, cwd=script_dir, encoding="utf-8", env=env
    )
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
        sys.exit(1)
    with open(tmp_json, 'r', encoding='utf-8') as _jf:
        data = json.load(_jf)
    os.unlink(tmp_json)

    # Output path вЂ” include name and target date
    target_date = data.get('target_date', '')
    safe_name = args.name.replace(' ', '_') if args.name else 'lunar'
    output_name = f"lunar_{safe_name}_{target_date.replace('.', '-')}_{args.lang}.png"
    output_path = os.path.join(os.path.expanduser('~'), '.openclaw', 'workspace', output_name)

    render_chart(data, output_path, args.lang, frame_img)


if __name__ == '__main__':
    main()
