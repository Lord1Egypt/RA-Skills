#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Transit Chart Renderer — Swiss Ephemeris Edition v4.0.0
Layout: single wheel (natal + transits) | wide forecast panel
- Natal planets: pale/faded on inner orbit
- Transit planets: bright on outer orbit
- Aspect lines between transit and natal planets (color-coded)
- Retrograde: dashed aspect lines
- Wide right panel: full text forecast with word-wrap
"""

import json, math, os, subprocess, sys, argparse, shutil, unicodedata

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont

# ─── Copy .dat → usable ───
_ttf_dir = os.path.dirname(os.path.abspath(__file__))
for _f in os.listdir(_ttf_dir):
    if _f.endswith('.ttf.dat'):
        _s = os.path.join(_ttf_dir, _f)
        _d = _s[:-4]
        if not os.path.exists(_d):
            shutil.copy2(_s, _d)
    if _f.endswith('.pyd.dat'):
        _s = os.path.join(_ttf_dir, _f)
        _d = _s[:-4]
        if not os.path.exists(_d):
            shutil.copy2(_s, _d)
    if _f.endswith('.png.dat'):
        _s = os.path.join(_ttf_dir, _f)
        _d = _s[:-4]
        if not os.path.exists(_d):
            shutil.copy2(_s, _d)

# ─── Import interpretation data ───
_interp_dir = os.path.join(os.path.dirname(_ttf_dir), "..", "astro-natal-chart", "scripts")
if os.path.isdir(_interp_dir):
    sys.path.insert(0, _interp_dir)
    try:
        from interp_data import (HOUSE_TEXTS_RU, HOUSE_TEXTS_EN,
            PLANET_MEANING_RU, PLANET_MEANING_EN,
            SIGN_KEYWORDS_RU, SIGN_KEYWORDS_EN,
            ASPECT_MEANING_RU, ASPECT_MEANING_EN)
    except ImportError:
        HOUSE_TEXTS_RU = HOUSE_TEXTS_EN = []
        PLANET_MEANING_RU = PLANET_MEANING_EN = {}
        SIGN_KEYWORDS_RU = SIGN_KEYWORDS_EN = {}
        ASPECT_MEANING_RU = ASPECT_MEANING_EN = {}
else:
    HOUSE_TEXTS_RU = HOUSE_TEXTS_EN = []
    PLANET_MEANING_RU = PLANET_MEANING_EN = {}
    SIGN_KEYWORDS_RU = SIGN_KEYWORDS_EN = {}
    ASPECT_MEANING_RU = ASPECT_MEANING_EN = {}

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════

ZSYM = ['\u2648','\u2649','\u264a','\u264b','\u264c','\u264d',
        '\u264e','\u264f','\u2650','\u2651','\u2652','\u2653']
ZAB  = ['AR','TA','GE','CN','LE','VI','LI','SC','SG','CP','AQ','PI']
ZEL  = [0,1,2,3,0,1,2,3,0,1,2,3]
EL_COL = [(80,30,30),(30,70,30),(70,70,30),(30,50,80)]
SIG_COL = [(200,60,60),(80,180,70),(220,190,50),(70,130,220),
           (240,170,40),(100,160,80),(180,90,180),(160,40,70),
           (90,110,210),(100,100,100),(70,170,210),(60,140,140)]
EL_RU = ['Огонь','Земля','Воздух','Вода']
EL_EN = ['Fire','Earth','Air','Water']
SN_RU = ['Овен','Телец','Близнецы','Рак','Лев','Дева',
         'Весы','Скорпион','Стрелец','Козерог','Водолей','Рыбы']
SN_EN = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']

PM = {
    "Sun":     ("SU", (255,220,50),  "Солнце", "Sun"),
    "Moon":    ("MO", (210,210,220), "Луна",   "Moon"),
    "Mercury": ("ME", (100,210,100), "Меркурий", "Mercury"),
    "Venus":   ("VE", (80,230,170),  "Венера", "Venus"),
    "Mars":    ("MA", (230,70,50),   "Марс",   "Mars"),
    "Jupiter": ("JU", (210,150,60),  "Юпитер", "Jupiter"),
    "Saturn":  ("SA", (150,150,170), "Сатурн", "Saturn"),
    "Uranus":  ("UR", (100,210,230), "Уран",   "Uranus"),
    "Neptune": ("NE", (90,140,230),  "Нептун", "Neptune"),
    "Pluto":   ("PL", (170,80,80),   "Плутон", "Pluto"),
}
ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']

ASPECT_COLORS = {
    "conjunction": (200,200,200),
    "opposition":  (240,140,40),
    "trine":       (80,220,80),
    "square":      (220,80,80),
    "sextile":     (100,180,240),
    "semisextile": (150,150,100),
    "semisquare":  (150,100,100),
    "quincunx":    (180,160,60),
}
ASPECT_SYM = {
    "conjunction":"\u260c","opposition":"\u260d","square":"\u25a1","trine":"\u25b3",
    "sextile":"\u2736","quincunx":"\u26b9","semisextile":"\u26ba","semisquare":"\u2220"
}
RETRO_COL = (180,60,60)  # dashed line color for retrograde aspects

# Dark theme
BG_MAIN    = (8, 8, 20)
BG_WHEEL   = (16, 16, 36)
BG_LEGEND  = (12, 12, 28)
BORDER_COL = (80, 80, 130)
WHEEL_RING = (180, 180, 210)
HOUSE_COL  = (90, 130, 190)
HOUSE_NUM  = (140, 170, 210)
ASC_COL    = (255, 255, 120)
MC_COL     = (255, 200, 100)
DIVIDER_COL= (80, 80, 120)
TITLE_COL  = (255, 255, 200)
NAME_COL   = (200, 200, 240)
SECTION_COL= (255, 220, 100)
BODY_COL   = (200, 200, 220)
CONCL_COL  = (240, 230, 200)
SEP_COL    = (120, 100, 60)

# ═══════════════════════════════════════════════════════════
# FONTS
# ═══════════════════════════════════════════════════════════

_SYM = os.path.join(_ttf_dir, "seguisym.ttf")
_TXT = os.path.join(_ttf_dir, "segoeuisl.ttf")
_FC = {}

def fnt(size, sym=False):
    k = (size, sym)
    if k in _FC: return _FC[k]
    fp = _SYM if sym else _TXT
    if os.path.exists(fp):
        try: _FC[k] = ImageFont.truetype(fp, size); return _FC[k]
        except: pass
    _FC[k] = ImageFont.load_default(); return _FC[k]

_ASP_CHARS = frozenset(('\u260c','\u260d','\u25a1','\u25b3','\u2736','\u26b9','\u26ba','\u2220'))

def is_astro(ch):
    return ('\u2648' <= ch <= '\u2653') or ch in _ASP_CHARS

def ch_w(ch, f):
    bb = f.getbbox(ch)
    return (bb[2] - bb[0]) if bb else 10

def rtext(draw, x, y, text, size, fill, cy=False):
    """Render text with per-character font selection."""
    sf = fnt(size, sym=True); tf = fnt(size, sym=False)
    if cy:
        bb = tf.getbbox(text); y -= (bb[3] - bb[1]) // 2
    cx = x
    for ch in text:
        f = sf if is_astro(ch) else tf
        draw.text((cx, y), ch, fill=fill, font=f)
        cx += ch_w(ch, f)

def rcent(draw, cx, y, text, size, fill, ox=0):
    sf = fnt(size, sym=True); tf = fnt(size, sym=False)
    tw = sum(ch_w(ch, sf if is_astro(ch) else tf) for ch in text)
    x = cx - tw // 2 + ox
    for ch in text:
        f = sf if is_astro(ch) else tf
        draw.text((x, y), ch, fill=fill, font=f)
        x += ch_w(ch, f)

def wrap_text(text, font, max_w):
    words = text.split(' ')
    lines = []
    cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        bb = font.getbbox(test)
        tw = (bb[2] - bb[0]) if bb else 0
        if tw <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

# ═══════════════════════════════════════════════════════════
# GEOMETRY
# ═══════════════════════════════════════════════════════════

def aof(deg):
    return math.radians(90.0 - float(deg))

def ppos(cx, cy, r, d):
    a = aof(d)
    return cx + r * math.cos(a), cy - r * math.sin(a)

def zod(d):
    d = float(d) % 360
    i = int(d // 30); s = d - i * 30
    return i, ZAB[i], int(s), int((s - int(s)) * 60)

def _fade_color(col, alpha=0.35):
    """Make a color pale/transparent-looking by blending with background."""
    return tuple(int(col[j] * alpha + BG_WHEEL[j] * (1 - alpha)) for j in range(3))

def _draw_dashed_line(draw, p1, p2, fill, width=1, dash_len=8, gap_len=4):
    """Draw a dashed line between two points."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = math.sqrt(dx*dx + dy*dy)
    if dist < 1:
        return
    ux, uy = dx/dist, dy/dist
    drawn = 0
    on = True
    x, y = p1[0], p1[1]
    while drawn < dist:
        seg = dash_len if on else gap_len
        end = min(drawn + seg, dist)
        ex = p1[0] + ux * end
        ey = p1[1] + uy * end
        if on:
            draw.line([(int(x), int(y)), (int(ex), int(ey))], fill=fill, width=width)
        x, y = ex, ey
        drawn = end
        on = not on

# ═══════════════════════════════════════════════════════════
# SINGLE WHEEL: natal (pale, inner) + transit (bright, outer) + aspect lines
# ═══════════════════════════════════════════════════════════

def draw_combined_wheel(draw, cx, cy, RO, RS, RH, RP_NATAL, RP_TRANSIT, RI,
                        natal_pos, transit_pos, houses, asc_deg,
                        title, name="", aspects=None):
    """
    Draw a single wheel with:
    - Natal planets as pale/faded circles on inner orbit (RP_NATAL)
    - Transit planets as bright circles on outer orbit (RP_TRANSIT)
    - Aspect lines between transit and natal planets
    - Dashed lines for retrograde transit planets
    """

    # Background circle
    draw.ellipse((cx-RO, cy-RO, cx+RO, cy+RO), fill=BG_WHEEL, outline=BORDER_COL, width=4)

    # Sign sectors
    asc_si = int(asc_deg // 30) % 12
    sector_start = asc_si * 30
    for i in range(12):
        sd = sector_start + i * 30
        ed = sector_start + (i + 1) * 30
        si = (asc_si + i) % 12
        pts = [(cx, cy)]
        for j in range(41):
            d = sd + (ed - sd) * j / 40
            a = math.radians(90.0 - d)
            pts.append((cx + RO * math.cos(a), cy - RO * math.sin(a)))
        draw.polygon(pts, fill=EL_COL[ZEL[si]])

    draw.ellipse((cx-RO, cy-RO, cx+RO, cy+RO), outline=WHEEL_RING, width=4)

    # Sign division lines
    for i in range(12):
        dc = sector_start + i * 30
        ax, ay = ppos(cx, cy, RO - 6, dc)
        bx, by = ppos(cx, cy, RS - 18, dc)
        draw.line([(int(ax), int(ay)), (int(bx), int(by))], fill=(160,160,190), width=2)

    # Sign symbols
    for i in range(12):
        mid = sector_start + i * 30 + 15
        si = (asc_si + i) % 12
        lx, ly = ppos(cx, cy, RS, mid)
        rcent(draw, int(lx), int(ly), ZSYM[si], 38, SIG_COL[si])

    # House cusps
    for i in range(12):
        dc = float(houses[i])
        ax, ay = ppos(cx, cy, RI + 12, dc)
        bx, by = ppos(cx, cy, RH, dc)
        draw.line([(int(ax), int(ay)), (int(bx), int(by))], fill=HOUSE_COL, width=2)
        nc = float(houses[(i + 1) % 12])
        mid = dc + (nc - dc) / 2 if nc > dc else (dc + (nc + 360 - dc) / 2) % 360
        hnx, hny = ppos(cx, cy, RH + 48, mid)
        rcent(draw, int(hnx), int(hny), ROMAN[i], 20, HOUSE_NUM)

    # ASC / MC lines
    for lbl, dg, col in [("ASC", asc_deg, ASC_COL), ("MC", houses[9] if len(houses) > 9 else 0, MC_COL)]:
        ax, ay = ppos(cx, cy, RI, dg)
        bx, by = ppos(cx, cy, RO - 4, dg)
        draw.line([(int(ax), int(ay)), (int(bx), int(by))], fill=col, width=6)
        lx, ly = ppos(cx, cy, RO + 36, dg)
        rcent(draw, int(lx), int(ly), lbl, 22, col)

    draw.ellipse((cx-RI, cy-RI, cx+RI, cy+RI), outline=(90,90,140), width=2)

    # ── Natal planets (pale, inner orbit) ──
    natal_pp = []
    for key, data in natal_pos.items():
        if key not in PM: continue
        ab, cl, nr, ne = PM[key]
        lon = data["lon"]
        px, py = ppos(cx, cy, RP_NATAL, lon)
        natal_pp.append((key, ab, cl, nr, ne, lon, int(px), int(py)))
        faded = _fade_color(cl, 0.35)
        r = 16
        draw.ellipse((int(px)-r, int(py)-r, int(px)+r, int(py)+r),
                     fill=faded, outline=(80,80,80), width=1)
        rcent(draw, int(px), int(py) - 38, ab + ('(R)' if data.get("retro") else ''), 14, faded)

    # ── Transit planets (bright, outer orbit) ──
    transit_pp = []
    for key, data in transit_pos.items():
        if key not in PM: continue
        ab, cl, nr, ne = PM[key]
        lon = data["lon"]
        px, py = ppos(cx, cy, RP_TRANSIT, lon)
        transit_pp.append((key, ab, cl, nr, ne, lon, int(px), int(py)))
        r = 18
        draw.ellipse((int(px)-r, int(py)-r, int(px)+r, int(py)+r),
                     fill=cl, outline=(255,255,255), width=3)
        rcent(draw, int(px), int(py) - 42, ab + ('(R)' if data.get("retro") else ''), 17, cl)

    # ── Aspect lines between transit and natal ──
    if aspects:
        for a in aspects:
            t_key = a["transit"]
            n_key = a["natal"]
            # Find positions
            t_pos = next(((px, py) for k, ab, cl, nr, ne, lon, px, py in transit_pp if k == t_key), None)
            n_pos = next(((px, py) for k, ab, cl, nr, ne, lon, px, py in natal_pp if k == n_key), None)
            if not t_pos or not n_pos:
                continue
            atype = a["type"]
            col = ASPECT_COLORS.get(atype, (150,150,150))
            # Check if transit planet is retrograde
            t_data = transit_pos.get(t_key, {})
            is_retro = t_data.get("retro", False)
            if is_retro:
                _draw_dashed_line(draw, t_pos, n_pos, RETRO_COL, width=2, dash_len=8, gap_len=4)
            else:
                draw.line([(int(t_pos[0]), int(t_pos[1])), (int(n_pos[0]), int(n_pos[1]))],
                          fill=col, width=2)

    # Title + name
    if title:
        rcent(draw, cx, cy - RO - 50, title, 22, TITLE_COL)
    if name:
        rcent(draw, cx, cy - RO - 24, name, 20, NAME_COL)

    return natal_pp, transit_pp

# ═══════════════════════════════════════════════════════════
# LEGENDS below wheel
# ═══════════════════════════════════════════════════════════

def draw_legends(draw, img, planets_raw, cx, cy, RO, RU, frame_img=None, divider_x=2160):
    FS = 17; FM = 20
    LEG = cy + RO + 15
    plx = 20; ply = LEG; prh = 26; pw = 280

    # Planet legend
    lb = ply + (len(planets_raw) + 1) * prh + 14
    draw.rectangle((plx-10, ply-10, plx+pw, lb), fill=BG_LEGEND, outline=(60,60,100), width=2)
    rtext(draw, plx, ply, "ПЛАНЕТЫ" if RU else "PLANETS", FM-2, (200,200,220))
    for idx, p in enumerate(planets_raw):
        ry = ply + prh + idx * prh
        nm = p['nr'] if RU else p['ne']
        lbl = "%s  %-3s  %s" % (p['sym'], p['abbr'], nm)
        if p['retro']: lbl += ' R'
        rtext(draw, plx, ry, lbl, FS-2, p['col'])

    # Element legend
    elx = plx + pw + 30; ely = LEG; eeh = 30; ew = 230
    elb = ely + 5 * eeh + 14
    draw.rectangle((elx-10, ely-10, elx+ew, elb), fill=BG_LEGEND, outline=(60,60,100), width=2)
    rtext(draw, elx, ely, "Стихии" if RU else "Elements", FM-2, (200,200,220))
    for ei in range(4):
        ry = ely + eeh + ei * eeh
        enm = EL_RU[ei] if RU else EL_EN[ei]
        draw.rectangle((elx, ry+4, elx+22, ry+24), fill=EL_COL[ei])
        rtext(draw, elx+30, ry, enm, FS-2, (200,200,200))

    # Aspect legend
    asx = elx + ew + 30; asy = LEG; ash = 30; asw = 220
    asb = asy + 8 * ash + 14
    draw.rectangle((asx-10, asy-10, asx+asw, asb), fill=BG_LEGEND, outline=(60,60,100), width=2)
    rtext(draw, asx, asy, "АСПЕКТЫ" if RU else "ASPECTS", FM-2, (200,200,220))
    ail = [
        ((200,200,200), "\u260c", "Conj"), ((100,180,240), "\u2736", "Sext"),
        ((220,80,80),   "\u25a1", "Sqr"),  ((80,220,80),   "\u25b3", "Trine"),
        ((180,160,60),  "\u26b9", "Qnc"),  ((240,140,40),  "\u260d", "Opp"),
    ]
    for ai_item, (ac, al, albl) in enumerate(ail):
        ry = asy + ash + ai_item * ash
        draw.rectangle((asx, ry+4, asx+22, ry+24), fill=ac)
        rtext(draw, asx+30, ry, al + " " + albl, FS-2, ac)
    # Retrograde
    ry = asy + ash + len(ail) * ash
    rtext(draw, asx, ry, "--- R  Ретро", FS-2, RETRO_COL)

    # ── QR code (donations) — right of legends, same Y level ──
    # Position: right-aligned to left panel, 50px from divider
    if frame_img is not None:
        qr_w = frame_img.size[0]
        qr_h = frame_img.size[1]
        qr_x = divider_x - 50 - qr_w  # 50px left of divider
        qr_y = asy  # same Y level as legends
        # Use alpha_composite to properly blend RGBA onto RGB canvas
        _region = img.crop((qr_x, qr_y, qr_x + qr_w, qr_y + qr_h)).convert('RGBA')
        _composited = Image.alpha_composite(_region, frame_img)
        img.paste(_composited.convert('RGB'), (qr_x, qr_y))

# ═══════════════════════════════════════════════════════════
# FORECAST PANEL — wide, with colored planet names and word-wrap
# ═══════════════════════════════════════════════════════════

PLANET_TOKENS_RU = {"Солнце","Луна","Меркурий","Венера","Марс","Юпитер","Сатурн","Уран","Нептун","Плутон"}
PLANET_TOKENS_EN = {"Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"}

_PNAMES_RU = sorted([(PM[k][2], k) for k in PM], key=lambda x: -len(x[0]))
_PNAMES_EN = sorted([(PM[k][3], k) for k in PM], key=lambda x: -len(x[0]))

def _split_colorized(line, RU):
    pnames = _PNAMES_RU if RU else _PNAMES_EN
    parts = []
    remaining = line
    while remaining:
        best_idx = len(remaining)
        best_key = None
        best_name = None
        for name, key in pnames:
            idx = remaining.find(name)
            if 0 <= idx < best_idx:
                best_idx = idx
                best_key = key
                best_name = name
        if best_key is not None and best_idx < len(remaining):
            if best_idx > 0:
                parts.append((remaining[:best_idx], None))
            parts.append((best_name, PM[best_key][1]))
            remaining = remaining[best_idx + len(best_name):]
        else:
            parts.append((remaining, None))
            remaining = ''
    return parts

def _parts_width(parts, size):
    sf = fnt(size, sym=True); tf = fnt(size, sym=False)
    w = 0
    for text, _ in parts:
        for ch in text:
            w += ch_w(ch, sf if is_astro(ch) else tf)
    return w

def _draw_parts(draw, x, y, parts, size, default_fill):
    sf = fnt(size, sym=True); tf = fnt(size, sym=False)
    cx = x
    for text, clr in parts:
        fill = clr if clr else default_fill
        for ch in text:
            f = sf if is_astro(ch) else tf
            draw.text((cx, y), ch, fill=fill, font=f)
            cx += ch_w(ch, f)
    return cx

def _wrap_colorized(parts, size, max_w):
    sf = fnt(size, sym=True); tf = fnt(size, sym=False)
    words = []
    for text, clr in parts:
        for wi, w in enumerate(text.split(' ')):
            if wi > 0:
                words.append((' ', clr))
            words.append((w, clr))
    lines = [[]]
    cur_w = 0
    for wtext, wclr in words:
        if not wtext: continue
        ww = sum(ch_w(ch, sf if is_astro(ch) else tf) for ch in wtext)
        sp_w = ch_w(' ', tf)
        if cur_w + ww + (sp_w if cur_w > 0 else 0) <= max_w:
            if cur_w > 0:
                lines[-1].append((' ', None))
                cur_w += sp_w
            lines[-1].append((wtext, wclr))
            cur_w += ww
        else:
            if lines[-1]:
                lines.append([])
            lines[-1].append((wtext, wclr))
            cur_w = ww
    while lines and not lines[-1]:
        lines.pop()
    return lines

def draw_forecast_panel(draw, data, panel_x, panel_w, H, RU, planets_raw):
    FS = 21; FM = 24; FL = 28; LH = 28

    IPP = 35
    IPXL = panel_x + IPP
    IPW = panel_w - IPP * 2
    y = IPP

    def draw_parts_line(x, parts, size, default_fill):
        nonlocal y
        if y > H - 40: return
        _draw_parts(draw, x, y, parts, size, default_fill)
        y += LH

    def draw_parts_cent(parts, size, default_fill):
        tw = _parts_width(parts, size)
        draw_parts_line(IPXL + (IPW - tw) // 2, parts, size, default_fill)

    def draw_colored_wrapped(line, size, default_fill, indent=0):
        nonlocal y
        parts = _split_colorized(line, RU)
        wrapped_lines = _wrap_colorized(parts, size, IPW - indent)
        for wl in wrapped_lines:
            if y > H - 40: return
            draw_parts_line(IPXL + indent, wl, size, default_fill)

    def divider():
        nonlocal y
        draw.line([(panel_x+8, y), (panel_x+panel_w-8, y)], fill=(60,60,100), width=1)
        y += 12

    target = data.get("target_date", "")
    name = data.get("name", "")

    # ── Title ──
    title_line = "ПРОГНОЗ НА %s" % target if RU else "FORECAST FOR %s" % target
    draw_parts_cent(_split_colorized(title_line, RU), FL, TITLE_COL)
    y += FL + 14

    if name:
        draw_parts_cent([(name, NAME_COL)], FM, NAME_COL)
        y += FM + 10

    divider()

    # ── Key aspects ──
    aspects = data.get("aspects", [])

    if aspects:
        hdr = _split_colorized("КЛЮЧЕВЫЕ АСПЕКТЫ ДНЯ" if RU else "KEY ASPECTS OF THE DAY", RU)
        draw_parts_line(IPXL, hdr, FM, SECTION_COL)
        y += FM + 8

        for a in aspects:
            if y > H - 100: break
            t_key = a["transit"]
            n_key = a["natal"]
            atype = a["type"]
            orb = a.get("orb", 0)
            sym = a.get("symbol", ASPECT_SYM.get(atype, ""))
            aname = a.get("name", atype)

            t_name = PM[t_key][2] if RU else PM[t_key][3]
            n_name = PM[n_key][2] if RU else PM[n_key][3]
            t_col = PM[t_key][1]
            n_col = PM[n_key][1]
            asp_col = ASPECT_COLORS.get(atype, (150,150,150))

            # Aspect header line
            aspect_line = "  %s %s → %s  (%s, orb %.1f°)" % (sym, t_name, n_name, aname, orb)
            draw_colored_wrapped(aspect_line, FS, BODY_COL)

            # Description
            meaning = (ASPECT_MEANING_RU if RU else ASPECT_MEANING_EN).get(atype, "")
            if meaning:
                draw_colored_wrapped("    " + meaning, FS - 1, (160,160,180))

            # Planet interaction
            tp = (PLANET_MEANING_RU if RU else PLANET_MEANING_EN).get(t_key, "")
            np_ = (PLANET_MEANING_RU if RU else PLANET_MEANING_EN).get(n_key, "")
            if tp and np_:
                if RU:
                    interaction = "    %s активирует %s: %s встречается с %s." % (t_name, n_name, tp, np_)
                else:
                    interaction = "    %s activates %s: %s meets %s." % (t_name, n_name, tp, np_)
                draw_colored_wrapped(interaction, FS - 1, (150,150,170))

            y += 6

        divider()

    # ═══ HOUSE ACTIVATIONS — format like natal chart ═══
    transit_houses = data.get("transit_houses", {})
    natal_planet_houses = data.get("planet_houses", {})
    HM = HOUSE_TEXTS_RU if RU else HOUSE_TEXTS_EN
    PMean = PLANET_MEANING_RU if RU else PLANET_MEANING_EN
    SN = SN_RU if RU else SN_EN
    ZOD_LON = data.get("transits", {})  # transit positions for sign info

    if transit_houses and HM:
        hdr = _split_colorized("АКТИВАЦИЯ ДОМОВ" if RU else "HOUSE ACTIVATIONS", RU)
        draw_parts_line(IPXL, hdr, FM, SECTION_COL)
        y += FM + 10

        # Group transit planets by house
        house_transits = {}
        for pkey, hnum in transit_houses.items():
            house_transits.setdefault(hnum, []).append(pkey)

        for hnum in sorted(house_transits.keys()):
            if y > H - 120: break
            h_idx = hnum - 1
            h_data = HM[h_idx] if 0 <= h_idx < len(HM) else None
            if not h_data: continue

            # ── House title: "I (ASC) — Личность и самоопределение" ──
            house_title = h_data["title"]
            title_parts = _split_colorized(house_title, RU)
            draw_parts_line(IPXL, title_parts, FS, (180,200,255))
            y += LH + 2

            # ── House description (body) ──
            tf = fnt(FS - 1, sym=False)
            for body_line in h_data["body"]:
                if y > H - 60: break
                wrapped = wrap_text(body_line, tf, IPW - 16)
                for wl in wrapped:
                    if y > H - 60: break
                    parts = _split_colorized("  " + wl, RU)
                    draw_parts_line(IPXL, parts, FS - 1, (170,170,190))
                if y > H - 60: break

            # ── Transit planets in this house ──
            t_keys = house_transits[hnum]
            for t_key in t_keys:
                if y > H - 80: break
                t_name = PM[t_key][2] if RU else PM[t_key][3]
                t_col = PM[t_key][1]
                t_abbr = PM[t_key][0]
                t_data = data.get("transits", {}).get(t_key, {})
                t_lon = t_data.get("lon", 0)
                t_si = int(t_lon // 30)
                t_sign = SN[t_si] if 0 <= t_si < 12 else "?"
                t_sym = ZSYM[t_si] if 0 <= t_si < 12 else "?"
                t_deg = int(t_lon % 30)
                t_min = int((t_lon % 1) * 60)
                t_retro = t_data.get("retro", False)
                retro_s = "\u211e" if t_retro else ""

                # Line: "  ◆ Меркурий (ME ♉ TA 12°30') в I доме"
                if RU:
                    planet_line = "  \u25e6 %s (%s%s %s %s %d\u00b0%d') \u0432 %s \u0434\u043e\u043c\u0435" % (
                        t_name, t_abbr, retro_s, t_sym, t_sign, t_deg, t_min, ROMAN[hnum - 1])
                else:
                    planet_line = "  \u25e6 %s (%s%s %s %s %d\u00b0%d') in House %s" % (
                        t_name, t_abbr, ' R' if t_retro else '', t_sym, t_sign, t_deg, t_min, ROMAN[hnum - 1])
                draw_colored_wrapped(planet_line, FS - 1, t_col, indent=0)

                # ── Find natal planet in same house for context ──
                natal_in_house = [k for k, nh in natal_planet_houses.items() if nh == hnum]

                # ── AI interpretation: transit planet in this house ──
                t_mean = PMean.get(t_key, "")
                h_area = h_data["title"].split("\u2014")[1].strip()[:40] if "\u2014" in h_data["title"] else h_data["title"][:40]

                if RU:
                    if natal_in_house:
                        n_key = natal_in_house[0]
                        n_name = PM[n_key][2]
                        interp_line = "    \u25e6 %s \u0432 %s \u0434\u043e\u043c\u0435: %s. %s \u0430\u043a\u0442\u0438\u0432\u0438\u0440\u0443\u0435\u0442 \u0441\u0444\u0435\u0440\u0443 %s." % (
                            t_name, ROMAN[hnum - 1], t_mean, t_name, h_area)
                    else:
                        interp_line = "    \u25e6 %s \u0432 %s \u0434\u043e\u043c\u0435: %s. \u042d\u043d\u0435\u0440\u0433\u0438\u044f %s \u043f\u0440\u043e\u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0432 \u0441\u0444\u0435\u0440\u0435 %s." % (
                            t_name, ROMAN[hnum - 1], t_mean, t_name, h_area)
                else:
                    if natal_in_house:
                        n_name = PM[natal_in_house[0]][3]
                        interp_line = "    \u25e6 %s in House %s: %s. %s activates the area of %s." % (
                            t_name, ROMAN[hnum - 1], t_mean, t_name, h_area)
                    else:
                        interp_line = "    \u25e6 %s in House %s: %s. The energy of %s expresses in the area of %s." % (
                            t_name, ROMAN[hnum - 1], t_mean, t_name, h_area)
                draw_colored_wrapped(interp_line, FS - 2, (155,155,175), indent=0)

                # ── If there's a natal planet here, add its activation context ──
                if natal_in_house and y < H - 60:
                    n_key = natal_in_house[0]
                    n_name = PM[n_key][2] if RU else PM[n_key][3]
                    n_mean = PMean.get(n_key, "")
                    if RU:
                        act_line = "      \u2192 \u041d\u0430\u0442\u0430\u043b\u044c\u043d\u044b\u0439 %s (%s) \u0430\u043a\u0442\u0438\u0432\u0438\u0440\u043e\u0432\u0430\u043d: %s. %s \u0443\u0441\u0438\u043b\u0438\u0432\u0430\u0435\u0442 %s \u0432 \u044d\u0442\u043e\u0439 \u0441\u0444\u0435\u0440\u0435." % (
                            n_name, n_mean[:50], t_name, n_name, h_area)
                    else:
                        act_line = "      \u2192 Natal %s (%s) is activated: %s strengthens %s in this area." % (
                            n_name, n_mean[:50], t_name, n_name)
                    draw_colored_wrapped(act_line, FS - 2, (140,140,160), indent=0)

            # ── Show if house has no transit planets (but is activated by cusp) ──
            if not t_keys:
                if RU:
                    no_pl = "  \u25e6 \u043d\u0435\u0442 \u0442\u0440\u0430\u043d\u0437\u0438\u0442\u043d\u044b\u0445 \u043f\u043b\u0430\u043d\u0435\u0442"
                else:
                    no_pl = "  \u25e6 no transit planets"
                draw_parts_line(IPXL + 8, [(no_pl, (130,130,150))], FS - 1, (130,130,150))

            y += 8
            # Divider every 3 houses
            if hnum % 3 == 0 and hnum < 12 and y < H - 100:
                draw.line([(panel_x + 10, y), (panel_x + panel_w - 10, y)], fill=(40, 40, 70), width=1)
                y += 10

        divider()

    # ═══ AI CONCLUSION ═══
    conclusion = ""
    # Check for --conclusion file (AI-generated by OpenClaw)
    conclusion_file = data.get("_conclusion_file", "")
    if conclusion_file and os.path.exists(conclusion_file):
        try:
            with open(conclusion_file, "r", encoding="utf-8") as cf:
                conclusion = cf.read().strip()
        except:
            pass
    # Fallback to generated conclusion
    if not conclusion:
        conclusion = _generate_ai_conclusion(data, RU, planets_raw)

    if conclusion and y < H - 120:
        draw.line([(panel_x + 30, y), (panel_x + panel_w - 30, y)], fill=SEP_COL, width=2)
        y += 18

        conc_title = "ЗАКЛЮЧЕНИЕ" if RU else "CONCLUSION"
        draw_parts_cent(_split_colorized(conc_title, RU), FL, SECTION_COL)
        y += FL + 10

        for para in conclusion.split("\n"):
            if not para.strip():
                y += 6; continue
            if y > H - 50: break
            draw_colored_wrapped("  " + para.strip(), FS - 1, CONCL_COL, indent=0)
            y += 4

        if y < H - 80:
            y += 6
            draw.line([(panel_x + 60, y), (panel_x + panel_w - 60, y)], fill=SEP_COL, width=1)
            y += 14

    # ── ClawHub link ──
    if y < H - 50:
        y += 10
        url = "https://clawhub.ai/dynamicsAlex/astro-daily-transits"
        draw_parts_cent([(url, (80,80,120))], FS - 2, (80,80,120))




def _generate_ai_conclusion(data, RU, planets_raw):
    SN = SN_RU if RU else SN_EN
    PMean = PLANET_MEANING_RU if RU else PLANET_MEANING_EN
    HM = HOUSE_TEXTS_RU if RU else HOUSE_TEXTS_EN

    aspects = data.get("aspects", [])
    transit_houses = data.get("transit_houses", {})
    transits = data.get("transits", {})
    natal = data.get("natal", {})

    lines = []

    powerful = [a for a in aspects if a.get("nature") == "powerful"]
    harmonious = [a for a in aspects if a.get("nature") == "harmonious"]
    challenging = [a for a in aspects if a.get("nature") in ("challenging", "tense")]

    if powerful:
        t_key = powerful[0]["transit"]
        n_key = powerful[0]["natal"]
        t_name = PM[t_key][2] if RU else PM[t_key][3]
        n_name = PM[n_key][2] if RU else PM[n_key][3]
        orb = powerful[0].get("orb", 0)
        if RU:
            lines.append("Сегодняшний день отмечен мощным соединением %s с вашим натальным %s (орб %.1f°)." % (t_name, n_name, orb))
            lines.append("Это аспект глубокого слияния энергий, когда транзитная планета буквально зажигает вашу натальную.")
        else:
            lines.append("Today is marked by a powerful conjunction of your natal %s with transiting %s (orb %.1f°)." % (n_name, t_name, orb))
            lines.append("This is a deep fusion of energies where the transiting planet literally ignites your natal one.")

    if harmonious:
        if RU:
            lines.append("Гармоничные аспекты (%d) создают благоприятный фон — энергия течёт легко, открывая возможности для роста и сотрудничества." % len(harmonious))
        else:
            lines.append("Harmonious aspects (%d) create a favorable backdrop — energy flows easily, opening opportunities for growth and cooperation." % len(harmonious))

    if challenging:
        if RU:
            lines.append("Напряжённые аспекты (%d) требуют осознанности: возможны внутренние противоречия или внешние препятствия, которые станут катализаторами развития." % len(challenging))
        else:
            lines.append("Challenging aspects (%d) require awareness: internal contradictions or external obstacles may arise, serving as catalysts for growth." % len(challenging))

    lines.append("")

    # Transit planet in sign context
    if transits and natal and aspects:
        closest = min(aspects, key=lambda a: a.get("orb", 99))
        t_key = closest["transit"]
        t_data = transits.get(t_key, {})
        lon = t_data.get("lon", 0)
        si = int(lon // 30)
        sign_name = SN[si] if 0 <= si < 12 else "?"
        retro = t_data.get("retro", False)
        t_name = PM[t_key][2] if RU else PM[t_key][3]
        t_mean = PMean.get(t_key, "")

        if RU:
            retro_str = " (ретроградный)" if retro else ""
            lines.append("Транзитный %s%s в знаке %s." % (t_name, retro_str, sign_name))
            lines.append("%s в %s — это %s." % (t_name, sign_name, t_mean))
        else:
            retro_str = " (retrograde)" if retro else ""
            lines.append("Transiting %s%s in %s." % (t_name, retro_str, sign_name))
            lines.append("%s in %s — this is %s." % (t_name, sign_name, t_mean))
        lines.append("")

    # House activation summary
    if transit_houses and HM:
        from collections import Counter
        h_counts = Counter(transit_houses.values())
        top_house = h_counts.most_common(1)[0]
        hnum = top_house[0]
        h_idx = hnum - 1
        h_title = HM[h_idx]["title"] if 0 <= h_idx < len(HM) else "House %d" % hnum
        pkeys = [k for k, v in transit_houses.items() if v == hnum]
        pnames = ", ".join(PM[k][2] if RU else PM[k][3] for k in pkeys if k in PM)

        if RU:
            lines.append("Наиболее активен %d-й дом (%s) — здесь сосредоточены %s." % (hnum, h_title, pnames))
            if 0 <= h_idx < len(HM) and HM[h_idx]["body"]:
                lines.append(HM[h_idx]["body"][0])
        else:
            lines.append("The most activated house is House %d (%s) — with %s concentrated here." % (hnum, h_title, pnames))
            if 0 <= h_idx < len(HM) and HM[h_idx]["body"]:
                lines.append(HM[h_idx]["body"][0])
        lines.append("")

    # Practical advice
    if RU:
        if powerful and not challenging:
            lines.append("Рекомендация: используйте энергию дня для решительных действий. Это благоприятное время для начинаний, важных разговоров и проявления инициативы.")
        elif challenging and not powerful:
            lines.append("Рекомендация: не форсируйте события. Лучшая стратегия — наблюдать, анализировать и действовать осознанно. Избегайте конфликтов и импульсивных решений.")
        elif powerful and challenging:
            lines.append("Рекомендация: день сочетает мощную энергию и напряжение. Действуйте, но с осознанностью. Используйте соединения как топливо, а квадраты как компас — они указывают, где нужно работать над собой.")
        else:
            lines.append("Рекомендация: спокойный день для рутины, отдыха и внутренней работы. Хорошее время для медитации, планирования и завершения начатого.")
    else:
        if powerful and not challenging:
            lines.append("Recommendation: use today's energy for decisive action. This is a favorable time for new beginnings, important conversations, and showing initiative.")
        elif challenging and not powerful:
            lines.append("Recommendation: don't force events. The best strategy is to observe, analyze, and act consciously. Avoid conflicts and impulsive decisions.")
        elif powerful and challenging:
            lines.append("Recommendation: the day combines powerful energy with tension. Act, but with awareness. Use conjunctions as fuel and squares as a compass — they show where you need to work on yourself.")
        else:
            lines.append("Recommendation: a calm day for routine, rest, and inner work. Good time for meditation, planning, and finishing what you started.")

    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Daily Transit Chart Renderer v4.0")
    parser.add_argument("date", nargs="?", default="14.12.1991")
    parser.add_argument("time", nargs="?", default="18:30")
    parser.add_argument("city", nargs="?", default="Ижевск")
    parser.add_argument("--target-date", default=None)
    parser.add_argument("--lang", default="ru", choices=["ru", "en"])
    parser.add_argument("--name", default="")
    parser.add_argument("--conclusion", default="", help="Path to AI-generated conclusion file")
    parser.add_argument("--frame", default=None, help="Path to frame image .png.dat (QR code) to embed. Default: bundled frame_small.png.dat")
    args = parser.parse_args()

    RU = (args.lang == "ru")
    _SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))

    # Load frame image (QR code). Default: bundled frame_small.png.dat
    # Keep RGBA to preserve transparency for correct rendering on RGB canvas
    frame_img = None
    frame_path = args.frame
    if frame_path is None:
        frame_path = os.path.join(_SCRIPTDIR, "frame_small.png.dat")
    else:
        if not os.path.isabs(frame_path):
            frame_path = os.path.join(_SCRIPTDIR, frame_path)
    frame_path = os.path.normpath(frame_path)
    if os.path.exists(frame_path):
        try:
            _qr_raw = Image.open(frame_path)
            frame_img = _qr_raw if _qr_raw.mode == 'RGBA' else _qr_raw.convert('RGBA')
            print(f"Frame loaded: {frame_img.size} from {frame_path}")
        except Exception as e:
            print(f"Warning: could not load frame image: {e}")
    else:
        print(f"Warning: frame not found at {frame_path}")

    cmd = [sys.executable, os.path.join(_SCRIPTDIR, "daily_transits.py"),
           args.date, args.time, args.city, "--json"]
    if args.target_date:
        cmd.extend(["--target-date", args.target_date])
    if args.name:
        cmd.extend(["--name", args.name])

    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                         cwd=_SCRIPTDIR, encoding="utf-8")
    if res.returncode != 0:
        print("Error:", res.stderr or res.stdout)
        sys.exit(1)

    data = json.loads(res.stdout)
    # Pass conclusion file path into data for the panel renderer
    if args.conclusion:
        data["_conclusion_file"] = args.conclusion

    # ═══ LAYOUT: wheel (2160) | panel (3600) ═══
    WHEEL = 2160
    PANEL_W = 3600
    TOT_W = WHEEL + PANEL_W
    TOT_H = TOT_W // 2  # 2880

    img = Image.new("RGB", (TOT_W, TOT_H), BG_MAIN)
    draw = ImageDraw.Draw(img)

    # Wheel geometry
    RO = 960; RS = 888; RH = 816
    RP_NATAL = 520    # inner orbit for natal planets (pale)
    RP_TRANSIT = 720  # outer orbit for transit planets (bright)
    RI = 380

    # ── Data ──
    natal_cx = WHEEL // 2
    natal_cy = TOT_H // 2

    natal_pos = {k: {"lon": v["lon"], "speed": v["speed"], "retro": v["retro"]}
                 for k, v in data["natal"].items()}
    transit_pos = {k: {"lon": v["lon"], "speed": v["speed"], "retro": v["retro"]}
                   for k, v in data["transits"].items()}
    natal_houses = data.get("houses", [i * 30.0 for i in range(12)])
    natal_asc = natal_houses[0] if natal_houses else 0
    aspects = data.get("aspects", [])

    # Planets raw for legends
    PO = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]
    planets_raw = []
    for pn, pd in data["natal"].items():
        if pn not in PM: continue
        ab, cl, nr, ne = PM[pn]
        ln = pd["lon"]; si = int(ln // 30); sd = ln - si * 30
        planets_raw.append({
            'key': pn, 'abbr': ab, 'nr': nr, 'ne': ne,
            'lon': ln, 'si': si, 'sab': ZAB[si], 'sym': ZSYM[si],
            'deg': int(sd), 'min': int((sd - int(sd)) * 60),
            'retro': pd["retro"], 'col': cl,
            'house': data.get("planet_houses", {}).get(pn, 1),
        })
    planets_raw.sort(key=lambda p: PO.index(p['key']) if p['key'] in PO else 99)

    # ── Title ──
    wheel_title = "НАТАЛЬНАЯ КАРТА + ТРАНЗИТЫ" if RU else "NATAL + TRANSITS"
    target_str = data.get("target_date", "")
    if target_str:
        wheel_title += "  %s" % target_str

    # ── Draw combined wheel ──
    draw_combined_wheel(draw, natal_cx, natal_cy, RO, RS, RH, RP_NATAL, RP_TRANSIT, RI,
                        natal_pos, transit_pos, natal_houses, natal_asc,
                        wheel_title, name=args.name, aspects=aspects)

    # ── Legends ──
    draw_legends(draw, img, planets_raw, natal_cx, natal_cy, RO, RU, frame_img=frame_img, divider_x=WHEEL)

    # ── Forecast panel ──
    PANEL_X = WHEEL
    draw_forecast_panel(draw, data, PANEL_X, PANEL_W, TOT_H, RU, planets_raw)

    # ── Divider ──
    draw.line([(WHEEL, 0), (WHEEL, TOT_H)], fill=DIVIDER_COL, width=3)

    # ── Save ──
    _name_safe = ""
    if args.name:
        _name_safe = "".join(
            c if c.isascii() and c.isalnum() else "_"
            for c in unicodedata.normalize("NFKD", args.name)
        ).strip("_")
        if _name_safe:
            _name_safe += "_"
    target_part = data.get("target_date", "").replace(".", "-")
    filename = "%sdaily_%s_%s.png" % (_name_safe, target_part, "ru" if RU else "en")
    outdir = os.path.normpath(os.path.join(_ttf_dir, "..", "..", "..", "workspace"))
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, filename)
    img.save(outpath, "PNG")
    print("Saved:", outpath, img.size)

if __name__ == "__main__":
    main()
