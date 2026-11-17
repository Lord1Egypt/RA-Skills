# -*- coding: utf-8 -*-
"""宣传册生成器(通用版): 普卡荧光+高定(钻石边)+高位双面(正反成对,不包边)
   缎带标题+花边边框+渐变底色; 紫光贴合抠图; 封面/信息区/UV演示/二维码
   用法: python make_catalog.py [ROOT] [OUT] [BORDER] [DIA] [COVER] [QR]
   依赖: 同目录 psd_cutout.py / uv_from_cut.py(可缺省,缺省时用整图紫光)"""
import os, re, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
try:
    from uv_from_cut import uv_from_cut
except ImportError:
    uv_from_cut = None
try:
    from uv_effect2 import uv_effect
except ImportError:
    uv_effect = None
import psd_tools

_defaults = {
    "ROOT": r"D:\UserFolders\Desktop\ff卡\新批次\A5尺寸（129张）",
    "OUT": r"D:\UserFolders\Desktop\workspace\A5包边板子\宣传册.png",
    "BORDER": r"D:\UserFolders\Desktop\包边.png",
    "DIA": r"D:\UserFolders\Desktop\钻石包边.png",
    "COVER": r"D:\UserFolders\Desktop\包边\宣传中心图.png",
    "QR": r"D:\UserFolders\Desktop\包边\二维码.png",
    "UVDEMO": r"C:\Users\terri\Doubao\chats\2026-09-11\new-chat\uv_demo.png",
}

def _first(idx, key):
    if len(sys.argv) > idx and sys.argv[idx]:
        return sys.argv[idx]
    return _defaults[key]

ROOT = _first(1, "ROOT")
OUT = _first(2, "OUT")
BORDER = _first(3, "BORDER")
DIA = _first(4, "DIA")
COVER = _first(5, "COVER")
QR = _first(6, "QR")
UVDEMO = _first(7, "UVDEMO")

# 自适应子文件夹名（普卡荧光（196张）/（104张）等）
def _find_sub(root, *keys):
    if not os.path.isdir(root):
        return None
    for k in keys:
        for d in os.listdir(root):
            if k in d and os.path.isdir(os.path.join(root, d)):
                return os.path.join(root, d)
    return None

PUCA = _find_sub(ROOT, "普卡荧光", "普卡") or os.path.join(ROOT, "普卡荧光（104张）")
GAODING = _find_sub(ROOT, "高定") or os.path.join(ROOT, "高定（15张）")
GAOWEI = _find_sub(ROOT, "高位双面", "高位") or os.path.join(ROOT, "高位双面（10张）")
_outdir = os.path.dirname(OUT)
if _outdir:
    os.makedirs(_outdir, exist_ok=True)

W = 1984
BG_TOP = (252, 240, 244)
BG_BOT = (244, 224, 232)
GOLD = (196, 152, 52)
GOLD_L = (218, 184, 120)
DARK = (62, 46, 72)
NAVY = (56, 62, 110)

def font(name, size):
    p = os.path.join(r"C:\Windows\Fonts", name)
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_TITLE = font("georgiab.ttf", 92)
F_SUB   = font("bahnschrift.ttf", 32)
F_H     = font("georgiab.ttf", 22)
F_INFO  = font("bahnschrift.ttf", 19)
F_SEC   = font("georgiab.ttf", 42)
F_SEC_CJK = font("msyhbd.ttc", 42)
F_SECCNT = font("bahnschrift.ttf", 22)
F_NAME  = font("msyhbd.ttc", 20)
F_THX   = font("georgiab.ttf", 54)

def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def tracked(draw, cx, y, text, fnt, fill, tr, anchor="lm"):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tr * (len(text) - 1)
    x = cx - total / 2
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor=anchor)
        x += cw + tr

NAME_MAP = {
    "2B": "2B", "Kamisato Ayaka": "Kamisato Ayaka", "VIVI": "Vivi",
    "albedo": "Albedo", "asuka": "Asuka", "asuna": "Asuna",
    "boa": "Boa Hancock", "funinna": "Furina", "hinata": "Hinata",
    "kafka": "Kafka", "kurumi": "Kurumi", "makima": "Makima",
    "marin": "Marin Kitagawa", "miku": "Hatsune Miku", "raiden": "Raiden Shogun",
    "rem": "Rem", "rias": "Rias Gremory", "robin": "Robin",
    "shinobu": "Shinobu", "yea miko": "Yae Miko", "yor": "Yor Forger",
    "zreotwo": "Zero Two", "刻晴": "Keqing", "夜一": "Yoruichi",
    "小霞": "Misty", "纲手": "Tsunade", "蒂法": "Tifa",
}

def folder_key(fd):
    return re.sub(r"[（(]\d+张[）)]?", "", fd).strip()

def small_name(png_path):
    fd = os.path.basename(os.path.dirname(png_path))
    return NAME_MAP.get(folder_key(fd), folder_key(fd))

def is_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)

# (no misaligned cards after psd unification; asuna 340 uses cutout per user)
MISALIGN = {}

def cover_resize(img, tw, th):
    sc = max(tw / img.width, th / img.height)
    img = img.resize((max(2, round(img.width * sc)), max(2, round(img.height * sc))), Image.LANCZOS)
    l = (img.width - tw) // 2
    t = (img.height - th) // 2
    return img.crop((l, t, l + tw, t + th))

def card_source(png_path, psd_path):
    """makima/3: extract original from its psd (user request, no mask)"""
    if os.path.basename(png_path).startswith("3") and "makima" in png_path.replace("\\", "/") and psd_path:
        ps = psd_tools.PSDImage.open(psd_path)
        return ps.composite().convert("RGBA")
    return Image.open(png_path).convert("RGBA")

def uv_of(png_path, psd_path, img):
    fd = os.path.basename(os.path.dirname(png_path))
    stem = os.path.splitext(os.path.basename(png_path))[0]
    use_cutout = psd_path and os.path.exists(psd_path) and stem not in MISALIGN.get(folder_key(fd), set())
    if use_cutout:
        try:
            return uv_from_cut(png_path, psd_path).convert("RGBA")
        except Exception:
            pass
    return uv_effect(img.convert("RGB")).convert("RGBA")

def is_land(png_path):
    return Image.open(png_path).size[0] > Image.open(png_path).size[1]

def make_card(png_path, psd_path, card_w, land):
    img = card_source(png_path, psd_path)
    if land:
        CW, CH = card_w, round(card_w * 1052 / 1494)
        frame = Image.open(BORDER).convert("RGBA").rotate(90, expand=True).resize((CW, CH), Image.LANCZOS)
    else:
        CW, CH = card_w, round(card_w * 1494 / 1052)
        frame = Image.open(BORDER).convert("RGBA").resize((CW, CH), Image.LANCZOS)
    img = cover_resize(img, CW, CH)
    normal = img.copy()
    normal.paste(frame, (0, 0), frame)
    uv_img = uv_of(png_path, psd_path, img).resize((CW, CH), Image.LANCZOS)
    uv_img.paste(frame, (0, 0), frame)
    return normal, uv_img, CW, CH

def make_premium_card(png_path, psd_path, card_w, land):
    img = card_source(png_path, psd_path)
    if land:
        CW, CH = card_w, round(card_w * 1052 / 1494)
        frame = Image.open(DIA).convert("RGBA").rotate(90, expand=True).resize((CW, CH), Image.LANCZOS)
    else:
        CW, CH = card_w, round(card_w * 1494 / 1052)
        frame = Image.open(DIA).convert("RGBA").resize((CW, CH), Image.LANCZOS)
    img = cover_resize(img, CW, CH)
    normal = img.copy()
    normal.paste(frame, (0, 0), frame)
    uv_img = uv_of(png_path, psd_path, img).resize((CW, CH), Image.LANCZOS)
    uv_img.paste(frame, (0, 0), frame)
    return normal, uv_img, CW, CH

def flower(draw, cx, cy, r, col, col2=(255, 214, 120)):
    for i in range(5):
        a = i * 72 * math.pi / 180
        ex, ey = cx + math.cos(a) * r * 0.72, cy + math.sin(a) * r * 0.72
        draw.ellipse((ex - r * 0.46, ey - r * 0.46, ex + r * 0.46, ey + r * 0.46), fill=col)
    draw.ellipse((cx - r * 0.26, cy - r * 0.26, cx + r * 0.26, cy + r * 0.26), fill=col2)

def leaf(draw, cx, cy, ang, ln, col):
    a = ang * math.pi / 180
    ex, ey = cx + math.cos(a) * ln, cy + math.sin(a) * ln
    draw.line((cx, cy, ex, ey), fill=col, width=6)
    draw.ellipse((ex - 7, ey - 7, ex + 7, ey + 7), fill=col)

def ribbon_title(cx, y, name, count, w=660, h=118):
    x0, x1 = int(cx - w / 2), int(cx + w / 2)
    y0, y1 = y, y + h
    tb = 26
    sh = Image.new("RGBA", (W, y1 + 26), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0 + 5, y0 + 7, x1 + 5, y1 + 7), radius=tb, fill=(150, 105, 122, 110))
    canvas.paste(sh, (0, 0), sh)
    rb = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rb)
    for yy in range(0, y1 - y0):
        t = yy / (y1 - y0)
        col = (int(254 - 8 * t), int(250 - 10 * t), int(246 - 14 * t), 255)
        rd.line((0, yy, x1 - x0, yy), fill=col)
    rd.polygon([(0, 0), (tb, 0), (0, tb)], fill=(0, 0, 0, 0))
    rd.polygon([(x1 - x0, 0), (x1 - x0 - tb, 0), (x1 - x0, tb)], fill=(0, 0, 0, 0))
    rd.polygon([(0, y1 - y0), (tb, y1 - y0), (0, y1 - y0 - tb)], fill=(0, 0, 0, 0))
    rd.polygon([(x1 - x0, y1 - y0), (x1 - x0 - tb, y1 - y0), (x1 - x0, y1 - y0 - tb)], fill=(0, 0, 0, 0))
    canvas.paste(rb, (x0, y0), rb)
    draw.rectangle((x0 + 12, y0 + 6, x1 - 12, y0 + 8), fill=GOLD_L)
    draw.rectangle((x0 + 12, y1 - 8, x1 - 12, y1 - 6), fill=GOLD_L)
    draw.rectangle((x0 + 6, y0 + 12, x1 - 6, y0 + 14), fill=(250, 232, 210))
    draw.rectangle((x0 + 6, y1 - 14, x1 - 6, y1 - 12), fill=(250, 232, 210))
    fnt = F_SEC_CJK if is_cjk(name) else F_SEC
    tracked(draw, int(cx), y0 + h // 2 - 8, name, fnt, (120, 58, 88), 3)
    tracked(draw, int(cx), y0 + h // 2 + 34, "%d CARDS  |  UV FLUORESCENT" % count, F_SECCNT, (150, 100, 120), 2)

def floral_frame(dr, x, y, w, h, r=30):
    dr.rounded_rectangle((x + 4, y + 4, x + w - 4, y + h - 4), radius=r + 4,
                         fill=None, outline=(222, 190, 160), width=3)
    dr.rounded_rectangle((x + 14, y + 14, x + w - 14, y + h - 14), radius=r,
                         fill=None, outline=GOLD_L, width=2)
    for (fx, fy) in [(x + 34, y + 34), (x + w - 34, y + 34), (x + 34, y + h - 34), (x + w - 34, y + h - 34)]:
        flower(dr, fx, fy, 15, (240, 170, 190), (255, 218, 130))
        leaf(dr, fx + 20, fy - 10, -20, 18, (150, 190, 140))
        leaf(dr, fx - 20, fy + 10, 160, 18, (150, 190, 140))
    flower(dr, x + w // 2, y + 30, 11, (235, 170, 195))

def tinted_bg(src, box_w, box_h, alpha=15, blur=46, collage=False, all_srcs=None):
    if collage and all_srcs:
        cols = 4
        rows = math.ceil(len(all_srcs) / cols)
        cw2, ch2 = box_w // cols, box_h // rows
        bg = Image.new("RGB", (box_w, box_h), (250, 236, 241))
        for i, p in enumerate(all_srcs):
            try:
                im = Image.open(p).convert("RGB")
            except Exception:
                continue
            im = im.resize((cw2, ch2), Image.LANCZOS)
            r, c = divmod(i, cols)
            bg.paste(im, (c * cw2, r * ch2))
        bg = bg.filter(ImageFilter.GaussianBlur(blur))
    else:
        im = Image.open(src).convert("RGB")
        sc = max(box_w / im.width, box_h / im.height)
        im = im.resize((max(2, round(im.width * sc)), max(2, round(im.height * sc))), Image.LANCZOS)
        l, t = (im.width - box_w) // 2, (im.height - box_h) // 2
        im = im.crop((l, t, l + box_w, t + box_h))
        im = im.filter(ImageFilter.GaussianBlur(blur))
        bg = im
    overlay = Image.new("RGBA", (box_w, box_h), (252, 241, 245, 190))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)
    bg.putalpha(alpha)
    return bg

# ============ collect 普卡荧光 ============
folders = []
for f in os.listdir(PUCA):
    d = os.path.join(PUCA, f)
    if not os.path.isdir(d):
        continue
    pngs = sorted([x for x in os.listdir(d) if x.lower().endswith(".png")], key=natkey)
    cards = []
    for p in pngs:
        ps = os.path.join(d, os.path.splitext(p)[0] + ".psd")
        cards.append((os.path.join(d, p), ps if os.path.exists(ps) else None))
    if cards:
        folders.append((f, cards))

big = [(f, c) for f, c in folders if len(c) >= 3]
small = [(f, c) for f, c in folders if len(c) < 3]
big.sort(key=lambda t: (-len(t[1]), folder_key(t[0]).lower()))
puca_sections = big + [("__FEATURED__", [card for _, cards in small for card in cards])]

# ============ collect 高定 (flat, diamond border) ============
gaoding = []
for p in sorted([x for x in os.listdir(GAODING) if x.lower().endswith(".png")], key=natkey):
    ps = os.path.join(GAODING, os.path.splitext(p)[0] + ".psd")
    gaoding.append((os.path.join(GAODING, p), ps if os.path.exists(ps) else None))

# ============ collect 高位双面 (pairs) ============
pair_groups = {}
for p in sorted([x for x in os.listdir(GAOWEI) if x.lower().endswith(".png")], key=natkey):
    base = os.path.splitext(p)[0]
    if "正面" in base:
        name, side = base.split("正面")[0], "正"
    else:
        name, side = base.split("背面")[0], "反"
    ps = os.path.join(GAOWEI, os.path.splitext(p)[0] + ".psd")
    pair_groups.setdefault(name, {})[side] = (os.path.join(GAOWEI, p), ps if os.path.exists(ps) else None)
gaowei = [(n, g.get("正"), g.get("反")) for n, g in sorted(pair_groups.items())]

print("普卡 sections:", len(puca_sections), "cards:", sum(len(c) for _, c in puca_sections))
print("高定 cards:", len(gaoding))
print("高位双面 pairs:", len(gaowei))

# ============ geometry ============
cover_h = 1060
info_h = 300
demo_h = 1000
FX = 50
FW = W - FX * 2
BAN_H = 176
CW_V = 283
CW_L = 430
VGRP_W = CW_V * 2 + 20
GAP = 30
name_h = 56
DS_ROW_H = 402 + 26

def section_layout(cards):
    rows = []
    hs = []
    for i in range(0, len(cards), 3):
        row = cards[i:i + 3]
        lands = [is_land(p) for (p, s) in row]
        if any(lands) and not all(lands):
            # mixed row: split land cards and portrait cards into separate rows
            lrow = [c for c, l in zip(row, lands) if l]
            prow = [c for c, l in zip(row, lands) if not l]
            rows.append(lrow)
            hs.append(666)
            rows.append(prow)
            hs.append(402 + name_h)
        else:
            rows.append(row)
            hs.append(max(666, 402 + name_h) if any(lands) else 402 + name_h)
    return rows, hs

y = cover_h + info_h + demo_h + 10
sec_metrics = []          # (kind, fd, cards|pairs, rows, hs, sec_h)
def add_sec(kind, fd, cards):
    global y
    if kind == "double":
        rows = [cards[i:i + 2] for i in range(0, len(cards), 2)]
        hs = [2 * DS_ROW_H + 22 + 44 for r in rows]
        sec_h = BAN_H + 70 + sum(hs) + 40 + 34
        sec_metrics.append((kind, fd, cards, rows, hs, sec_h))
        y += sec_h + 34
    else:
        rows, hs = section_layout(cards)
        sec_h = BAN_H + 70 + sum(hs) + 40 + 34
        sec_metrics.append((kind, fd, cards, rows, hs, sec_h))
        y += sec_h + 34

for fd, cards in puca_sections:
    add_sec("normal", fd, cards)
add_sec("premium", "__PREMIUM__", gaoding)
for ds_name, ds_f, ds_b in gaowei:
    if ds_f and ds_b:
        add_sec("double", ds_name, [(ds_name, ds_f, ds_b)])
    else:
        add_sec("double", ds_name, [(ds_name, ds_f, ds_b)])

close_h = 420
qr_h = 620
H = y + close_h + qr_h + 40

canvas = Image.new("RGB", (W, H), BG_TOP)
draw = ImageDraw.Draw(canvas)
for yy in range(H):
    t = yy / H
    c = (int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t),
         int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t),
         int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t))
    draw.line((0, yy, W, yy), fill=c)

# ---- cover ----
cover = Image.open(COVER).convert("RGB")
scale = W / cover.width
cover = cover.resize((W, round(cover.height * scale)), Image.LANCZOS)
top = (cover.height - cover_h) // 2
cover = cover.crop((0, top, W, top + cover_h))
grad = Image.new("L", (1, cover_h), 0)
for yy in range(cover_h):
    a = 0
    if yy > cover_h - 260:
        a = int(230 * (yy - (cover_h - 260)) / 260)
    grad.putpixel((0, yy), a)
grad = grad.resize((W, cover_h))
dark_layer = Image.new("RGB", (W, cover_h), (20, 12, 32))
cover.paste(dark_layer, (0, 0), grad)
canvas.paste(cover, (0, 0))
tracked(draw, W // 2, cover_h - 150, "Moewaifushop", F_TITLE, (255, 246, 225), 8)
tracked(draw, W // 2, cover_h - 40, "A5 ACRYLIC CARD COLLECTION", F_SUB, (235, 218, 190), 6)

# ---- info ----
iy = cover_h + 60
draw.rectangle((80, iy - 10, 83, iy + 118), fill=GOLD)
draw.text((110, iy), "COLLECTION UPDATE", font=F_H, fill=DARK, anchor="lm")
for i, t in enumerate(["new items in stock!", "updated weekly", "follow our social media", "for updates and exclusive content"]):
    draw.text((110, iy + 40 + i * 27), t, font=F_INFO, fill=(120, 102, 124), anchor="lm")
rx = W - 110
draw.rectangle((rx - 3, iy - 10, rx, iy + 118), fill=GOLD)
draw.text((rx - 30, iy), "CATALOG GUIDE", font=F_H, fill=DARK, anchor="rm")
for i, t in enumerate(["1. Product Categories", "2. Packaging Details", "3. Shipping Information", "4. Return Policy"]):
    draw.text((rx - 30, iy + 40 + i * 27), t, font=F_INFO, fill=(120, 102, 124), anchor="rm")

# ---- UV demo ----
dy = cover_h + info_h
demo = Image.new("RGB", (W, demo_h), (30, 20, 45))
if os.path.exists(UVDEMO):
    demo = Image.open(UVDEMO).convert("RGB").resize((W, demo_h), Image.LANCZOS)
canvas.paste(demo, (0, dy))
dt = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
dd = ImageDraw.Draw(dt)
dd.rectangle((0, 0, W, 200), fill=(25, 15, 40))
alpha = Image.new("L", (W, 200), 0)
for yy in range(200):
    alpha.putpixel((0, yy), int(150 * (1 - abs(yy - 100) / 100)))
alpha = alpha.resize((W, 200))
canvas.paste(dt, (0, dy), alpha)
tracked(draw, W // 2, dy + 78, "UV-REACTIVE FLUORESCENT EFFECT", font("georgiab.ttf", 40), (235, 210, 150), 3)
tracked(draw, W // 2, dy + 140, "Glow under UV blacklight  |  A5 UV-Reactive Fluorescent Board", F_INFO, (225, 215, 235), 2)

# ---- sections ----
y = dy + demo_h + 10
for kind, fd, cards, rows, hs, sec_h in sec_metrics:
    box_x, box_y = FX, y
    if kind == "normal":
        if fd == "__FEATURED__":
            all_png = [p for (p, s) in cards]
            bgimg = tinted_bg(None, FW, sec_h, alpha=16, collage=True, all_srcs=all_png)
        else:
            bgimg = tinted_bg(cards[0][0], FW, sec_h, alpha=15)
    elif kind == "premium":
        bgimg = tinted_bg(cards[0][0], FW, sec_h, alpha=15, blur=40)
    else:
        bgimg = tinted_bg(cards[0][1][0], FW, sec_h, alpha=15, blur=40)
    canvas.paste(bgimg, (box_x, box_y), bgimg)
    panel = Image.new("RGBA", (FW - 28, sec_h - 28), (255, 250, 251, 128))
    canvas.paste(panel, (box_x + 14, box_y + 14), panel)
    floral_frame(draw, box_x, box_y, FW, sec_h)
    if kind == "normal":
        nm = "FEATURED CHARACTERS" if fd == "__FEATURED__" else NAME_MAP.get(folder_key(fd), folder_key(fd))
        ribbon_title(W // 2, box_y + 34, nm, len(cards))
    elif kind == "premium":
        ribbon_title(W // 2, box_y + 34, "PREMIUM COLLECTION", len(cards), w=900)
    else:
        ribbon_title(W // 2, box_y + 34, fd.upper() + "  ·  DOUBLE-SIDED", len(cards) * 2, w=760)

    cy = box_y + 34 + BAN_H + 30
    if kind == "double":
        # each card = front+back pair, two rows (front normal+uv / back normal+uv)
        for row in rows:
            n_grp = len(row)
            grp_w = CW_V * 2 + 20
            gap = (FW - n_grp * grp_w - (n_grp - 1) * GAP) / 2
            x = FX + gap
            for (name_, front, back) in row:
                f_img = Image.open(front[0]).convert("RGBA")
                f_w, f_h = f_img.size
                cw = round(DS_ROW_H * f_w / f_h)
                ch = DS_ROW_H
                def pair_card(png, psd):
                    im = Image.open(png).convert("RGBA")
                    cw2 = round(ch * im.width / im.height)
                    im = cover_resize(im, cw2, ch)
                    uv = uv_of(png, psd, im).resize((cw2, ch), Image.LANCZOS)
                    return im, uv, cw2
                fn, fu, fcw = pair_card(front[0], front[1])
                bn, bu, bcw = pair_card(back[0], back[1]) if back else (None, None, 0)
                canvas.paste(fn, (int(x), cy))
                canvas.paste(fu, (int(x) + fcw + 18, cy))
                if back:
                    canvas.paste(bn, (int(x), cy + ch + 22))
                    canvas.paste(bu, (int(x) + bcw + 18, cy + ch + 22))
                tracked(draw, int(x) + fcw // 2, cy + ch + 12, name_ + "  /  FRONT", F_NAME, (140, 80, 105), 1)
                if back:
                    tracked(draw, int(x) + fcw // 2, cy + ch + 22 + ch + 12, "BACK", F_NAME, (150, 100, 120), 1)
                x += grp_w + GAP
            cy += 2 * DS_ROW_H + 22 + 44
    else:
        for row, rh in zip(rows, hs):
            n_grp = len(row)
            lands = [is_land(p) for (p, s) in row]
            if any(lands):
                grp_w = CW_L
                gap = (FW - n_grp * grp_w - (n_grp - 1) * GAP) / 2
                x = FX + gap
                for (png, psd) in row:
                    maker = make_premium_card if kind == "premium" else make_card
                    normal, uv, cw, ch = maker(png, psd, CW_L, True)
                    canvas.paste(normal, (int(x), cy))
                    canvas.paste(uv, (int(x), cy + ch + 18))
                    nm2 = small_name(png) if kind == "normal" and fd == "__FEATURED__" else (
                        NAME_MAP.get(folder_key(fd), folder_key(fd)) if kind == "normal" else "")
                    if nm2:
                        tracked(draw, int(x) + cw // 2, cy + ch + 18 + uv.height + 24, nm2, F_NAME, (140, 80, 105), 1)
                    x += grp_w + GAP
            else:
                grp_w = VGRP_W
                gap = (FW - n_grp * grp_w - (n_grp - 1) * GAP) / 2
                x = FX + gap
                for (png, psd) in row:
                    maker = make_premium_card if kind == "premium" else make_card
                    normal, uv, cw, ch = maker(png, psd, CW_V, False)
                    canvas.paste(normal, (int(x), cy))
                    canvas.paste(uv, (int(x) + cw + 20, cy))
                    nm2 = small_name(png) if kind == "normal" and fd == "__FEATURED__" else (
                        NAME_MAP.get(folder_key(fd), folder_key(fd)) if kind == "normal" else "")
                    if nm2:
                        tracked(draw, int(x) + cw + 10, cy + ch + 32, nm2, F_NAME, (140, 80, 105), 1)
                    x += grp_w + GAP
            cy += rh
    y += sec_h + 34

# ---- closing ----
ty = y + 8
close_bg = Image.new("RGB", (W, close_h), (240, 205, 218))
for yy in range(close_h):
    v = int(200 + 55 * yy / close_h)
    close_bg.paste((v, 175, 195), (0, yy, W, yy + 1))
canvas.paste(close_bg, (0, ty))
tracked(draw, W // 2, ty + close_h // 2 - 20, "THANK YOU", F_THX, (120, 70, 95), 6)
tracked(draw, W // 2, ty + close_h // 2 + 55, "Every card is made with care — follow us for new drops", F_INFO, (150, 110, 125), 2)

# ---- QR ----
yqr = ty + close_h + 20
qr = Image.open(QR).convert("RGB")
qw = W - 160
qh = round(qr.height * qw / qr.width)
qr = qr.resize((qw, qh), Image.LANCZOS)
canvas.paste(qr, ((W - qw) // 2, yqr))

canvas.save(OUT)
print("saved:", OUT, canvas.size)
