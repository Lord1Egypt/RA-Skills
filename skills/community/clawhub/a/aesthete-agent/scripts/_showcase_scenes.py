#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""showcase 级场景引擎(由推广生成器移植,供 scene 命令使用): 大画布场景 × 6 配色主图墙 × 明亮暗色。
设计原则: 平面纯色分层(禁渐变)、设备框、柔和投影、真实内容密度、证据徽章。"""
import sys, os, json

import palette_forge as pf

NL = "\n"

PALETTES = [
    {"key": "bees", "name": "Bees & Honey", "theme": "light",
     "hexes": ["FAF3DD", "FDF7EE", "5E6472", "8A93A3", "FFA69E", "AED9E0", "B8F2E6", "E07066"]},
    {"key": "olive", "name": "Olive Garden", "theme": "dark",
     "hexes": ["FEFAE0", "283618", "606C38", "BC6C25", "DDA15E", "9B2226"]},
    {"key": "pop", "name": "Pop Deco", "theme": "light",
     "hexes": ["EF476F", "FFD166", "06D6A0", "118AB2", "073B4C"]},
    {"key": "pastel", "name": "Morning Pastel", "theme": "light",
     "hexes": ["555B6E", "89B0AE", "BEE3DB", "FAF9F9", "FFD6BA"]},
    {"key": "editorial", "name": "Editorial Deep", "theme": "light",
     "hexes": ["EDAE49", "D1495B", "00798C", "30638E", "003D5B"]},
    {"key": "terra", "name": "Terracotta Warm", "theme": "light",
     "hexes": ["D8A47F", "EF8354", "EE4B6A", "DF3B57", "0F7173"]},
]


USER_PAS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "user_palettes.json"), encoding="utf-8"))


def roles(p):
    R = pf._viz_roles(p["hexes"], dark=(p["theme"] == "dark"))
    R["theme"] = p["theme"]
    R["_hexes"] = p["hexes"]
    R["name"] = p["name"]
    # 两个辅助口声色: 次高/再次高饱度
    cands = sorted((h for h in p["hexes"] if h not in (R["accent"], R["bg"], R["ink"])),
                   key=lambda h: -pf.oklch_from_hex(h)[1])
    R["alt1"] = cands[0] if cands else R["accent"]
    R["alt2"] = cands[1] if len(cands) > 1 else R["alt1"]
    R["ratio"] = pf.contrast_ratio(R["ink"], R["bg"])
    return R


def badge(R, extra=""):
    aa = "AA" if R["ratio"] >= 4.5 else " "
    return ("<div class='badges'><span class='b ok'>text/bg " + format(R["ratio"], ".1f") +
            ":1 " + aa + "</span><span class='b ok'>color-blind safe</span>" +
            "<span class='b ok'>slop-clean</span>" +
            ("<span class='b'>" + extra + "</span>" if extra else "") +
            "<span class='b pal'>" + R["name"] + "</span></div>")


def shadow(depth="0 24px 60px rgba(30,32,40,.16)"):
    return depth


# ---------- 场景画布(每个 920 宽) ----------

def sc_mobile(R):
    av = [R["alt1"], R["accent"], R["alt2"], R["ink2"]]
    rows = ""
    items = [("Blue Bottle Coffee", "Today 08:12", "-28.00", av[0]),
             ("Metro Card", "Today 07:45", "-6.00", av[1]),
             ("Salary — March", "Mar 01", "+9,500.00", av[2]),
             ("Transfer from Mei", "Feb 28", "+1,200.00", av[3])]
    for name, when, amt, c in items:
        neg = amt.startswith("-")
        rows += ("<div class='tx'><div class='av' style='background:#" + c + "'>"
                 "</div><div class='txn'><b>" + name + "</b><span>" + when +
                 "</span></div><div class='amt " + ("neg" if neg else "pos") + "'>" + amt + "</div></div>")
    return ("<div class='phone'>"
            "<div class='notch'></div>"
            "<div class='p-status'><span>9:41</span><span>●●●</span></div>"
            "<div class='p-head'>Wallet<div class='p-avatar' style='background:#" + R["alt1"] + "'></div></div>"
            "<div class='p-balance' style='background:#" + R["accent"] + ";color:#" + pf.readable_text(R["accent"]) + "'>"
            "<span>Total balance</span><b>12,480.00</b><span class='p-chip'>+2.4% this month</span></div>"
            "<div class='p-sect'>Today</div>" + rows +
            "<div class='p-tab'>" +
            "<span style='background:#" + R["accent"] + "'></span><span></span><span></span><span></span></div>"
            "</div>")


def sc_landing(R):
    return ("<div class='browser'>"
            "<div class='b-bar'><span class='dot' style='background:#" + R["danger"] + "'></span>"
            "<span class='dot' style='background:#" + R["alt1"] + "'></span>"
            "<span class='dot' style='background:#" + R["alt2"] + "'></span>"
            "<span class='url'>app.acme.io</span></div>"
            "<div class='l-nav'><div class='l-logo'><span class='l-mark' style='background:#" + R["accent"] + "'></span>acme</div>"
            "<div class='l-links'><span>Product</span><span>Pricing</span><span>Docs</span>"
            "<span class='l-cta' style='background:#" + R["accent"] + ";color:#" + pf.readable_text(R["accent"]) + "'>Sign up</span></div></div>"
            "<div class='l-hero'>"
            "<div class='l-eyebrow'>MECHANICALLY VALIDATED COLOR</div>"
            "<h1>Ship color systems<br>that pass every review.</h1>"
            "<p>Palettes, contrast, color-blind safety and anti-slop checks —<br>proven before they ship, not after.</p>"
            "<div class='l-btns'><span class='l-btn1' style='background:#" + R["ink"] + ";color:#" + pf.readable_text(R["ink"]) + "'>Get started</span>"
            "<span class='l-btn2' style='border-color:#" + R["ink2"] + "'>Live demo</span></div></div>"
            "<div class='l-cards'>"
            "<div class='l-card' style='background:#" + R["surface"] + "'><span class='l-ic' style='background:#" + R["alt1"] + "'></span><b>Instant check</b><span>WCAG 2.2 + APCA on every pair</span></div>"
            "<div class='l-card' style='background:#" + R["surface"] + "'><span class='l-ic' style='background:#" + R["accent"] + "'></span><b>CB-safe by design</b><span>Three simulation passes built in</span></div>"
            "<div class='l-card' style='background:#" + R["surface"] + "'><span class='l-ic' style='background:#" + R["alt2"] + "'></span><b>Slop guard</b><span>Median-trap &amp; gradient ban enforced</span></div></div>"
            "</div>")


def sc_dashboard(R):
    bars = ""
    vals = [42, 58, 36, 74, 52, 88, 63, 95]
    for i, v in enumerate(vals):
        hot = " hot" if v == max(vals) else ""
        bars += ("<div class='d-col" + hot + "'><span class='d-v'>" + str(v * 12) +
                 "</span><div class='d-bar' style='height:" + str(v) +
                 "%;background:#" + (R["accent"] if v == max(vals) else R["alt1"]) + "'></div>"
                 "<span class='d-lab'>W" + str(i + 1) + "</span></div>")
    grid = "".join("<div class='d-grid'></div>" for _ in range(4))
    kpis = [("MRR", "86,400", "+4.2%", R["alt2"]), ("Active", "1,204", "+12%", R["accent"]),
            ("Churn", "1.9%", "-0.4%", R["alt1"])]
    kcards = "".join(
        "<div class='d-kpi' style='background:#" + R["surface"] + "'><span>" + k + "</span>"
        "<b>" + v + "</b><span class='d-delta' style='background:#" + c + ";color:#" +
        pf.readable_text(c) + "'>" + d + "</span></div>" for k, v, d, c in kpis)
    trows = ""
    for name, plan, st, sc_ in [("Acme Corp", "Scale", "active", R["accent"]),
                                ("Globex", "Growth", "active", R["alt1"]),
                                ("Initech", "Trial", "trial", R["ink2"]),
                                ("Umbrella", "Scale", "active", R["accent"])]:
        trows += ("<div class='d-tr'><span>" + name + "</span><span>" + plan + "</span>"
                  "<span class='d-pill' style='background:#" + sc_ + ";color:#" +
                  pf.readable_text(sc_) + "'>" + st + "</span><b>" + str(1200 + len(name) * 137) + "</b></div>")
    return ("<div class='dash'>"
            "<div class='d-side' style='background:#" + R["surface"] + "'>"
            "<div class='d-logo' style='background:#" + R["accent"] + "'></div>"
            "<span class='d-nav on' style='background:#" + R["accent"] + "'></span><span class='d-nav'></span>"
            "<span class='d-nav'></span><span class='d-nav'></span>"
            "<div class='d-user' style='background:#" + R["alt2"] + "'></div></div>"
            "<div class='d-main'>"
            "<div class='d-top'><h3>Overview</h3><span class='d-btn' style='background:#" + R["ink"] +
            ";color:#" + pf.readable_text(R["ink"]) + "'>Export</span></div>"
            "<div class='d-kpis'>" + kcards + "</div>"
            "<div class='d-chart' style='background:#" + R["surface"] + "'>"
            "<div class='d-chead'><b>Weekly revenue</b><span>last 8 weeks</span></div>"
            "<div class='d-plot'>" + grid + "<div class='d-bars'>" + bars + "</div></div></div>"
            "<div class='d-table' style='background:#" + R["surface"] + "'>"
            "<div class='d-th'><span>Account</span><span>Plan</span><span>Status</span><span>MRR</span></div>"
            + trows + "</div></div></div>")


def sc_branding(R):
    chips = "".join("<div class='br-chip'><span style='background:#" + h + "'></span><b>" +
                    h + "</b></div>" for h in R["_hexes"][:5])
    return ("<div class='br-stage' style='background:#" + R["alt2"] + "'>"
            "<div class='br-paper' style='background:#" + R["bg"] + "'>"
            "<div class='br-lh'><span class='br-mark' style='background:#" + R["accent"] + "'></span>"
            "<b style='color:#" + R["ink"] + "'>STUDIO NOVA</b><span style='color:#" + R["ink2"] + "'>Design systems, proven.</span></div>"
            "<div class='br-rule' style='background:#" + R["accent"] + "'></div>"
            "<div class='br-body' style='color:#" + R["ink"] + "'>A brand is a promise repeated — in color, in type,<br>"
            "in every margin. We make the repetition exact.</div></div>"
            "<div class='br-card' style='background:#" + R["ink"] + ";color:#" + pf.readable_text(R["ink"]) + "'>"
            "<div class='br-mark big' style='background:#" + R["accent"] + "'></div>"
            "<div class='br-name'>Lin Zhang</div><div class='br-role'>Design Lead</div>"
            "<div class='br-contact'>studio.nova@example.com · +86 138 0000 0000</div></div>"
            "<div class='br-specs'><b>Palette specification</b><div class='br-chips'>" + chips + "</div></div></div>")


def sc_typography(R):
    rows = [("Display 800 · 64", "font:800 52px/1.05 Georgia,serif", "Aa Palette in Type"),
            ("Heading 700 · 32", "font:700 30px/1.15 system-ui", "Structure speaks first"),
            ("Body 400 · 16", "font:400 17px/1.5 system-ui",
             "The quick brown fox jumps over the lazy dog — 0123456789"),
            ("Caption 500 · 12", "font:500 13px/1.4 system-ui;letter-spacing:.14em;text-transform:uppercase",
             "Eyebrow label — accent voice")]
    body = ""
    for i, (lab, st, tx) in enumerate(rows):
        color = R["ink"] if i < 2 else (R["ink2"] if i == 2 else R["atext"])
        body += ("<div class='ty-row'><span class='ty-lab' style='background:#" +
                 (R["alt1"] if i % 2 else R["accent"]) + "'>" + lab + "</span>"
                 "<div class='ty-tx' style='" + st + ";color:#" + color + "'>" + tx + "</div></div>")
    return ("<div class='ty' style='background:#" + R["bg"] + "'>"
            "<div class='ty-head'><span class='ty-aa' style='background:#" + R["ink"] +
            ";color:#" + pf.readable_text(R["ink"]) + "'>Aa</span>"
            "<div><b>Type scale on this palette</b>"
            "<span>every row passes its gate · ink #" + R["ink"] + "</span></div></div>"
            + body +
            "<div class='ty-foot'>serif display + system UI · line-height 1.5 · tracking on labels</div></div>")


def sc_chart(R):
    bars = ""
    a = [34, 51, 42, 66, 48, 72, 58, 80, 64, 88]
    for i, v in enumerate(a):
        bars += ("<div class='c-col'><div class='c-bar' style='height:" + str(v) +
                 "%;background:#" + (R["accent"] if i % 3 else R["alt1"]) + "'></div></div>")
    pts = [(8, 82), (21, 70), (34, 74), (47, 60), (60, 52), (73, 44), (86, 36), (96, 30)]
    poly = " ".join(str(x) + "," + str(y) for x, y in pts)
    circles = "".join("<circle cx='" + str(x) + "' cy='" + str(y) + "' r='4' fill='#" +
                      R["danger"] + "'/>" for x, y in pts)
    return ("<div class='chart' style='background:#" + R["surface"] + "'>"
            "<div class='c-head'><div><b>Revenue vs. churn — 10 weeks</b>"
            "<span>bars = revenue · line = churn index</span></div>"
            "<div class='c-leg'><span style='background:#" + R["accent"] + "'></span>revenue"
            "<span style='background:#" + R["danger"] + "'></span>churn</div></div>"
            "<div class='c-plot'><div class='c-y'><span>80k</span><span>60k</span><span>40k</span><span>20k</span></div>"
            "<div class='c-area'>"
            "<svg viewBox='0 0 100 100' preserveAspectRatio='none' class='c-svg'>"
            "<line x1='0' y1='25' x2='100' y2='25' stroke='#" + R["ink2"] + "' stroke-width='.3' stroke-dasharray='2 2'/>"
            "<line x1='0' y1='50' x2='100' y2='50' stroke='#" + R["ink2"] + "' stroke-width='.3' stroke-dasharray='2 2'/>"
            "<line x1='0' y1='75' x2='100' y2='75' stroke='#" + R["ink2"] + "' stroke-width='.3' stroke-dasharray='2 2'/>"
            "<polyline points='" + poly + "' fill='none' stroke='#" + R["danger"] +
            "' stroke-width='1.4' vector-effect='non-scaling-stroke'/>" + circles + "</svg>"
            "<div class='c-bars'>" + bars + "</div></div>"
            "<div class='c-x'>" + "".join("<span>W" + str(i + 1) + "</span>" for i in range(10)) + "</div></div></div>")


def _tint(hexs, l_target=0.88, c_mul=0.45):
    L, C, H = pf.oklch_from_hex(hexs)
    return pf.hex_from_oklch(l_target, pf.gamut_fit(l_target, C * c_mul, H), H).upper()


def sc_ecom(R):
    stars = "★★★★★"
    tint = _tint(R["accent"])
    pairs = [("Pairs with", R["alt1"]), ("Shadow", R["ink2"]), ("Error", R["danger"])]
    specs = "".join("<div class='sh-spec'><span style='background:#" + c + "'></span><b>#" +
                    c + "</b><i>" + lab + "</i></div>" for lab, c in pairs)
    return ("<div class='shop' style='background:#" + R["bg"] + "'>"
            "<div class='sh-card' style='background:#" + R["surface"] + "'>"
            "<div class='sh-stage' style='background:#" + tint + "'>"
            "<div class='sh-obj'><div class='sh-cup' style='background:#" + R["accent"] + "'></div>"
            "<div class='sh-handle' style='border-color:#" + R["accent"] + "'></div>"
            "<div class='sh-plate' style='background:#" + R["ink2"] + ";opacity:.55'></div></div>"
            "<span class='sh-tag' style='background:#" + R["ink"] + ";color:#" +
            pf.readable_text(R["ink"]) + "'>BESTSELLER</span></div>"
            "<div class='sh-body'>"
            "<div class='sh-name'>Ceramic Pour-Over Set<span class='sh-stars' style='color:#" +
            R["alt2"] + "'>" + stars + "</span><i>214</i></div>"
            "<div class='sh-price'>248 <s>328</s><span style='background:#" + tint +
            ";color:#" + pf.readable_text(tint) + "'>SAVE 24%</span></div>"
            "<div class='sh-vars'><span class='on' style='background:#" + R["ink"] + ";color:#" +
            pf.readable_text(R["ink"]) + "'>Fog</span><span style='border-color:#" + R["ink2"] +
            "'>Clay</span><span style='border-color:#" + R["ink2"] + "'>Moss</span></div>"
            "<div class='sh-cta'><span style='background:#" + R["accent"] + ";color:#" +
            pf.readable_text(R["accent"]) + "'>Add to cart</span><span style='border-color:#" +
            R["ink2"] + "'>♡ Save</span></div>"
            "<div class='sh-trust'>Free shipping over 199 · 7-day returns · 2-year warranty</div>"
            "</div></div>"
            "<div class='sh-side'>"
            "<div class='sh-note'><b>60-30-10, enforced.</b><span>The product stage is the "
            "accent's pastel tint — full accent only on the object and the CTA. Loud colors "
            "in small doses.</span></div>"
            "<div class='sh-specs'>" + specs + "</div>"
            "<div class='sh-mini' style='background:#" + tint + "'></div>"
            "</div></div>")


def sc_email(R):
    lst = ""
    for name, subj, c, on in [("Design Weekly", "The color issue #42", R["accent"], True),
                              ("Acme billing", "Invoice Mar — paid", R["alt1"], False),
                              ("Mei Zhang", "Re: palette review", R["alt2"], False),
                              ("Standup", "Notes from Monday", R["ink2"], False)]:
        lst += ("<div class='e-item" + (" on" if on else "") + "' style='" +
                ("background:#" + R["surface"] + ";" if on else "") + "'>"
                "<span class='e-av' style='background:#" + c + "'></span>"
                "<div class='e-m'><b>" + name + "</b><span>" + subj + "</span></div></div>")
    return ("<div class='mail' style='background:#" + R["bg"] + "'>"
            "<div class='e-list'>" + lst +
            "<div class='e-compose' style='background:#" + R["accent"] + ";color:#" +
            pf.readable_text(R["accent"]) + "'>Compose</div></div>"
            "<div class='e-open' style='background:#" + R["bg"] + "'>"
            "<div class='e-band' style='background:#" + R["accent"] + ";color:#" +
            pf.readable_text(R["accent"]) + "'>acme weekly</div>"
            "<div class='e-head'><b>The color issue #42</b>"
            "<span>why muted beats loud — and how to prove it</span></div>"
            "<div class='e-body'>This week: three palettes that pass every mechanical gate — "
            "contrast, color-blind separation, slop signature and scorecard.<br><br>"
            "One of them took ninety seconds from brief to acceptance report. "
            "The other took a design review, two rewrites and an apology.</div>"
            "<div class='e-cta' style='background:#" + R["ink"] + ";color:#" +
            pf.readable_text(R["ink"]) + "'>Read the issue</div>"
            "<div class='e-foot'>You receive this because you subscribed · unsubscribe</div>"
            "</div></div>")


def sc_editorial(R):
    return ("<div class='ed' style='background:#" + R["bg"] + "'>"
            "<div class='ed-page' style='background:#" + R["bg"] + "'>"
            "<div class='ed-folio'>THE REVIEW — 04</div>"
            "<h2>The quiet power of a<br>restrained palette</h2>"
            "<div class='ed-body'><span class='ed-cap' style='background:#" + R["accent"] +
            ";color:#" + pf.readable_text(R["accent"]) + "'>ESSAY</span>"
            "Design movements come and go, but restraint compounds. A palette of five "
            "disciplined colors outlives any trend cycle, because it reads as intent "
            "rather than accident. The eye relaxes; the message carries.</div></div>"
            "<div class='ed-page right' style='background:#" + R["bg"] + "'>"
            "<div class='ed-img' style='background:#" + R["alt1"] + "'>"
            "<div class='ed-motif' style='background:#" + R["accent"] + "'></div></div>"
            "<div class='ed-quote' style='border-color:#" + R["accent"] + "'>"
            "Mechanical validation does not kill taste — it protects it from the median.</div>"
            "<div class='ed-caption'>Fig. 1 — a five-color system, tested</div>"
            "<div class='ed-folio end'>12</div></div></div>")


def sc_pattern(R):
    tiles = ""
    seq = [R["ink"], R["accent"], R["alt1"], R["bg"], R["alt2"], R["surface"], R["danger"], R["bg"]]
    for i in range(12):
        c = seq[i % len(seq)]
        shape = ("border-radius:50%" if i % 3 == 0 else
                 "border-radius:8px" if i % 3 == 1 else "clip-path:polygon(50% 0,100% 100%,0 100%)")
        fg = pf.readable_text(c)
        if fg == "000000":
            fg = R["ink"]
        tiles += ("<div class='pt-tile' style='background:#" + c + "'>"
                  "<div style='width:44%;aspect-ratio:1;" + shape + ";background:#" + fg + ";opacity:.9'></div></div>")
    return ("<div class='pt' style='background:#" + R["bg"] + "'>"
            "<div class='pt-head'><b>Wallpaper pattern</b>"
            "<span>8-color rotation · flat motifs only — gradient-free by law</span></div>"
            "<div class='pt-grid'>" + tiles + "</div></div>")


SCENES = [
    ("01", "Mobile App — Finance wallet", sc_mobile),
    ("02", "Landing — SaaS hero", sc_landing),
    ("03", "Dashboard — KPI + revenue", sc_dashboard),
    ("04", "Branding — card & letterhead", sc_branding),
    ("05", "Typography — scale specimen", sc_typography),
    ("06", "Data chart — bars & trend", sc_chart),
    ("07", "E-commerce — product card", sc_ecom),
    ("08", "Email — client & newsletter", sc_email),
    ("09", "Editorial — magazine spread", sc_editorial),
    ("10", "Pattern — wallpaper rotation", sc_pattern),
]


def scene_section(no, title, inner, R):
    return ("<section class='scene' id='s" + no + "'><div class='shead'><span class='sno'>" + no + "</span>"
            "<h2>" + title + "</h2>" + badge(R) + "</div>"
            "<div class='stage' style='background:#" + (("3a4038" if R["theme"] == "dark" else "EDE8DC")) + "'>"
            + "<div class='fit'>" + inner + "</div></div></section>")



def user_roles(up):
    R = pf._viz_roles(up["hexes"], dark=False)
    dark_in = min(up["hexes"], key=lambda h: pf.oklch_from_hex(h)[0])
    if pf.contrast_ratio(dark_in, R["bg"]) > pf.contrast_ratio(R["ink"], R["bg"]):
        R["ink"] = dark_in
    if pf.contrast_ratio(R["ink"], R["bg"]) < 3.0:
        R["ink"] = "3D405B"
    R["ratio"] = pf.contrast_ratio(R["ink"], R["bg"])
    cands = sorted((h for h in up["hexes"] if h not in (R["accent"], R["bg"], R["ink"])),
                   key=lambda h: -pf.oklch_from_hex(h)[1])
    R["alt1"] = cands[0] if cands else R["accent"]
    R["alt2"] = cands[1] if len(cands) > 1 else R["alt1"]
    nm = up["names"][0].replace("-", " ").title() if up["names"] else up["url_id"]
    R["name"] = nm
    R["theme"] = "light"
    R["_hexes"] = up["hexes"]
    return R


def classify(up):
    L = [pf.oklch_from_hex(h)[0] for h in up["hexes"]]
    C = [pf.oklch_from_hex(h)[1] for h in up["hexes"]]
    mL, mC = sum(L) / len(L), sum(C) / len(C)
    if mC >= 0.105 or max(C) >= 0.16:
        return "vivid"
    if mL >= 0.68:
        return "bright"
    return "elegant"


def wall_card(up):
    R = pf._viz_roles(up["hexes"])
    dark_in = min(up["hexes"], key=lambda h: pf.oklch_from_hex(h)[0])
    if pf.contrast_ratio(dark_in, R["bg"]) > pf.contrast_ratio(R["ink"], R["bg"]):
        R["ink"] = dark_in
    if pf.contrast_ratio(R["ink"], R["bg"]) < 3.0:
        R["ink"] = "3D405B"
    ratio = pf.contrast_ratio(R["ink"], R["bg"])
    nm = up["names"][0].replace("-", " ").title() if up["names"] else up["url_id"]
    sub = ", ".join(n.replace("-", " ") for n in up["names"][1:3])
    cands = sorted((h for h in up["hexes"] if h not in (R["accent"], R["bg"], R["ink"])),
                   key=lambda h: -pf.oklch_from_hex(h)[1])
    R["alt"] = cands[0] if cands else R["accent"]
    return ("<div class='wall' style='background:#" + R["bg"] + "'>"
            "<div class='w-nav'><span class='l-mark' style='background:#" + R["accent"] + "'></span>"
            "<span class='w-links'><i style='background:#" + R["ink2"] + "'></i><i style='background:#" +
            R["ink2"] + "'></i><i style='background:#" + R["ink2"] + "'></i>"
            "<span class='w-cta' style='background:#" + R["accent"] + ";color:#" +
            pf.readable_text(R["accent"]) + "'>Try</span></span></div>"
            "<div class='w-body' style='color:#" + R["ink"] + "'>"
            "<span class='w-kick' style='color:#" + R["atext"] + "'>VERIFIED · " + format(ratio, ".1f") + ":1 AA</span>"
            "<b class='w-h'>" + nm + "</b>"
            "<span class='w-p'>" + sub + "</span>"
            "<div class='w-btns'><span class='w-b1' style='background:#" + R["ink"] + ";color:#" +
            pf.readable_text(R["ink"]) + "'>Get started</span>"
            "<span class='w-b2' style='border-color:#" + R["ink2"] + "'>Demo</span></div></div>"
            "<div class='w-cards'>"
            "<div class='w-c' style='background:#" + R["bg"] + "'><i style='background:#" + R["accent"] + "'></i>"
            "<span style='color:#" + R["ink"] + "'>Fast</span></div>"
            "<div class='w-c' style='background:#" + R["bg"] + "'><i style='background:#" + R["alt"] + "'></i>"
            "<span style='color:#" + R["ink"] + "'>Proven</span></div></div>"
            "<div class='w-chips'>" + "".join("<i style='background:#" + h + "'></i>" for h in up["hexes"]) + "</div></div>")


def build():
    main = PALETTES[0]
    R = roles(main)
    scenes = NL.join(scene_section(no, t, fn(R), R) for no, t, fn in SCENES)
    CATS = [
        ("Bright & Airy", "light, fresh fields — palettes that read as morning",
         "Bright & Airy", [sc_mobile, sc_landing], "bright", "airy"),
        ("Vivid & Bold", "saturated confidence for products that lead",
         "Vivid & Bold", [sc_ecom, sc_dashboard], "vivid", "vivid"),
        ("Elegant & Deep", "muted, composed — palettes for print and prose",
         "Elegant & Deep", [sc_editorial, sc_branding, sc_typography], "elegant", "elegant"),
    ]
    curated = ""
    no = 10
    for ctitle, csub2, ckey, fns, ctag, cid in CATS:
        members = [up for up in USER_PAS if classify(up) == ctag]
        if not members:
            continue
        curated += ("<h2 class='h2sec' id='" + cid + "'>" + ctitle + " <span class='cnt'>" +
                    str(len(members)) + " palettes</span></h2>"
                    "<p class='h2sub'>" + csub2 + ".</p><div class='divbar'></div>")
        for j, up in enumerate(members):
            no += 1
            Ru = user_roles(up)
            fn = fns[j % len(fns)]
            curated += scene_section("%02d" % no, Ru["name"] + " — " + ckey, fn(Ru), Ru)
    Rd = roles(PALETTES[1])
    Rd["name"] = "Bright dark"
    dark_scenes = NL.join(scene_section("D" + str(i + 1), t + " — bright dark", fn(Rd), Rd)
                          for i, (no, t, fn) in enumerate(SCENES[1:3]))
    css = """
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:#FFFFFF;font-family:system-ui,sans-serif;color:#1F2328}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.topnav{position:sticky;top:0;z-index:50;background:#FFFFFF;border-bottom:1px solid #E6E8EB}
.topnav .bar{max-width:1120px;margin:0 auto;padding:8px 24px;min-height:58px;display:flex;align-items:center;justify-content:space-between;gap:12px 18px;flex-wrap:wrap}
.topnav .brand{display:flex;align-items:center;gap:10px;font-family:system-ui;font-weight:800;font-size:16px;color:#1F2328;text-decoration:none;white-space:nowrap}
.topnav .mark{width:24px;height:24px;border-radius:7px;background:#1F2328;display:inline-flex;padding:4px;gap:2px}
.topnav .mark i{display:block;flex:1;border-radius:2px}
.topnav .chip{font-size:11px;font-weight:700;background:#EEF0F2;color:#1F2328;border-radius:999px;padding:2px 9px;white-space:nowrap}
.topnav nav{display:flex;gap:14px 18px;flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;scrollbar-width:none}
.topnav nav::-webkit-scrollbar{display:none}
.topnav nav a{font-size:13.5px;font-weight:600;color:#1F2328;text-decoration:none;border-bottom:2px solid transparent;padding-bottom:2px;white-space:nowrap}
.topnav nav a:hover{border-bottom-color:#1F2328}
.topnav nav a.x{color:#6B7280}
.h2sec{scroll-margin-top:76px}
.scene{scroll-margin-top:76px}
/* 移动端:场景等比缩放完整呈现(scale-to-fit,禁横滚);徽章折行;hero 字号收缩 */
.stage{overflow:hidden;position:relative}
.fit{position:absolute;top:0;left:50%;width:920px;transform:translateX(-50%);transform-origin:top center;display:flex;justify-content:center;align-items:center;min-height:560px}
.badges{flex-wrap:wrap;row-gap:6px}
header.hero{padding:64px 0 40px}
.hero .kick{font:700 13px system-ui;letter-spacing:.28em;color:#57606A}
.hero h1{font:800 clamp(34px,8vw,54px)/1.08 system-ui,sans-serif;color:#1F2328;margin:14px 0 12px}
.hero p{font:400 17px/1.6 system-ui;color:#6B7280;max-width:640px}
.hero .chips{display:flex;gap:10px;margin-top:22px;flex-wrap:wrap}
.hero .chips i{width:44px;height:44px;border-radius:10px;box-shadow:0 4px 12px rgba(30,32,40,.14)}
.scene{margin:0 auto 84px}
.shead{display:flex;align-items:baseline;gap:14px;margin:0 4px 16px;flex-wrap:wrap}
.sno{font:800 15px monospace;color:#57606A}
.shead h2{font:800 24px system-ui,sans-serif;color:#1F2328}
.badges{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.b{font:600 11px system-ui;padding:4px 10px;border-radius:99px;background:#fff;border:1px solid #E4E7EA;color:#57606A}
.b.ok{color:#2E7D5B;border-color:#cfe3da}
.b.pal{background:#1F2328;color:#fff;border-color:#1F2328}
.stage{border-radius:24px;padding:56px 40px;display:flex;justify-content:center;align-items:center;min-height:560px}
.phone{width:360px;background:#fff;border-radius:38px;border:10px solid #23262B;box-shadow:__SH__;overflow:hidden;position:relative}
.notch{position:absolute;top:10px;left:50%;transform:translateX(-50%);width:110px;height:22px;background:#23262B;border-radius:12px}
.p-status{display:flex;justify-content:space-between;font:600 11px system-ui;color:#333;padding:12px 18px 4px}
.p-head{display:flex;justify-content:space-between;align-items:center;font:800 20px system-ui;color:#222;padding:6px 18px 10px}
.p-avatar{width:30px;height:30px;border-radius:50%}
.p-balance{margin:2px 14px 12px;border-radius:16px;padding:14px 16px;display:flex;flex-direction:column;gap:3px}
.p-balance span{font:500 11px system-ui;opacity:.85}
.p-balance b{font:800 26px system-ui}
.p-chip{align-self:flex-start;font:600 10px system-ui;border-radius:99px;padding:3px 8px;background:rgba(255,255,255,.35)}
.p-sect{font:700 11px system-ui;letter-spacing:.12em;color:#999;padding:6px 18px}
.tx{display:flex;align-items:center;gap:10px;padding:9px 18px}
.av{width:34px;height:34px;border-radius:50%;flex:none}
.txn{display:flex;flex-direction:column;font:600 12.5px system-ui;color:#222}
.txn span{font:400 11px system-ui;color:#999}
.amt{margin-left:auto;font:700 12.5px system-ui}
.amt.neg{color:#c0392b}.amt.pos{color:#1e8e5a}
.p-tab{display:flex;justify-content:space-around;padding:10px 0 14px;border-top:1px solid #eee;margin-top:6px}
.p-tab span{width:16px;height:16px;border-radius:5px;background:#ddd}
.browser{width:840px;background:#fff;border-radius:14px;box-shadow:__SH__;overflow:hidden;border:1px solid rgba(0,0,0,.06)}
.b-bar{display:flex;align-items:center;gap:7px;padding:10px 14px;background:#F3F4F6}
.dot{width:11px;height:11px;border-radius:50%}
.url{margin-left:8px;font:500 11.5px monospace;background:#fff;border-radius:6px;padding:4px 14px;color:#888;flex:1}
.l-nav{display:flex;align-items:center;justify-content:space-between;padding:16px 28px}
.l-logo{display:flex;align-items:center;gap:9px;font:800 16px system-ui;color:#222}
.l-mark{width:18px;height:18px;border-radius:6px}
.l-links{display:flex;align-items:center;gap:20px;font:500 13px system-ui;color:#666}
.l-cta{padding:8px 16px;border-radius:8px}
.l-hero{text-align:center;padding:38px 20px 34px}
.l-eyebrow{font:700 11px system-ui;letter-spacing:.26em;color:#c0392b;margin-bottom:14px}
.l-hero h1{font:800 46px/1.1 Georgia,serif;color:#222}
.l-hero p{font:400 15px/1.6 system-ui;color:#777;margin:14px 0 20px}
.l-btns{display:flex;justify-content:center;gap:12px}
.l-btn1,.l-btn2{padding:11px 22px;border-radius:9px;font:700 13.5px system-ui}
.l-btn2{border:1.5px solid;color:#333}
.l-cards{display:flex;gap:14px;padding:0 28px 28px}
.l-card{flex:1;border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:6px}
.l-card b{font:700 13.5px system-ui;color:#222}
.l-card span{font:400 12px system-ui;color:#777}
.l-ic{width:26px;height:26px;border-radius:8px}
.dash{width:880px;display:flex;border-radius:14px;overflow:hidden;box-shadow:__SH__;border:1px solid rgba(0,0,0,.06)}
.d-side{width:64px;padding:16px 0;display:flex;flex-direction:column;align-items:center;gap:14px}
.d-logo{width:26px;height:26px;border-radius:8px}
.d-nav{width:22px;height:22px;border-radius:7px;background:rgba(0,0,0,.12)}
.d-user{margin-top:auto;width:28px;height:28px;border-radius:50%}
.d-main{flex:1;padding:18px 20px}
.d-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.d-top h3{font:800 18px system-ui;color:#222}
.d-btn{font:700 12px system-ui;padding:8px 14px;border-radius:8px}
.d-kpis{display:flex;gap:12px;margin-bottom:14px}
.d-kpi{flex:1;border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:4px}
.d-kpi span{font:500 11px system-ui;color:#888}
.d-kpi b{font:800 20px system-ui;color:#222}
.d-delta{align-self:flex-start;font:700 10px system-ui;border-radius:99px;padding:3px 8px}
.d-chart{border-radius:12px;padding:14px 16px;margin-bottom:14px}
.d-chead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}
.d-chead b{font:700 13px system-ui;color:#222}
.d-chead span{font:400 11px system-ui;color:#999}
.d-plot{position:relative;padding-top:8px}
.d-grid{border-top:1px dashed rgba(0,0,0,.1);height:26px}
.d-bars{position:absolute;inset:0;display:flex;align-items:flex-end;gap:14px;padding:0 6px}
.d-col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:130px;gap:5px}
.d-bar{width:70%;border-radius:5px 5px 0 0}
.d-col.hot .d-v{color:#c0392b}
.d-v{font:700 10px system-ui;color:#999;visibility:hidden}
.d-col:hover .d-v{visibility:visible}
.d-lab{font:500 10px system-ui;color:#aaa}
.d-table{border-radius:12px;padding:6px 16px 10px;font:500 12.5px system-ui;color:#333}
.d-th,.d-tr{display:grid;grid-template-columns:2fr 1.4fr 1fr 1fr;gap:8px;padding:9px 4px;align-items:center}
.d-th{font:700 11px system-ui;color:#999;border-bottom:1px solid rgba(0,0,0,.08)}
.d-tr{border-bottom:1px solid rgba(0,0,0,.05)}
.d-pill{justify-self:start;font:600 10.5px system-ui;border-radius:99px;padding:3px 10px}
.br-stage{width:920px;border-radius:20px;padding:48px 48px 140px;position:relative}
.br-paper{width:430px;border-radius:6px;padding:30px 32px;box-shadow:__SH__}
.br-lh{display:flex;align-items:center;gap:10px}
.br-lh b{font:800 15px system-ui;letter-spacing:.18em;color:#333}
.br-lh span{margin-left:auto;font:400 11px system-ui;color:#999}
.br-mark{width:20px;height:20px;border-radius:50%}
.br-rule{height:3px;margin:16px 0 18px}
.br-body{font:400 13.5px/1.8 Georgia,serif;color:#555}
.br-card{position:absolute;right:64px;top:150px;width:330px;border-radius:14px;padding:24px 26px;box-shadow:__SH__;transform:rotate(-3deg)}
.br-mark.big{width:34px;height:34px;margin-bottom:14px}
.br-name{font:800 22px Georgia,serif}
.br-role{font:500 12px system-ui;opacity:.8;margin:3px 0 16px}
.br-contact{font:400 11.5px system-ui;opacity:.75}
.br-specs{position:absolute;left:64px;bottom:32px;font:600 11px system-ui;color:#fff}
.br-specs b{letter-spacing:.14em;text-transform:uppercase;opacity:.85}
.br-chips{display:flex;gap:10px;margin-top:8px}
.br-chip{display:flex;flex-direction:column;gap:4px;align-items:center}
.br-chip span{width:44px;height:30px;border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.br-chip b{font:600 10px monospace;color:#fff}
.ty{width:920px;border-radius:20px;padding:38px 44px;box-shadow:__SH__}
.ty-head{display:flex;gap:18px;align-items:center;margin-bottom:22px}
.ty-aa{width:64px;height:64px;border-radius:16px;display:flex;align-items:center;justify-content:center;font:800 30px Georgia,serif}
.ty-head b{display:block;font:800 19px system-ui;color:#222}
.ty-head span{font:400 12px system-ui;color:#999}
.ty-row{display:flex;gap:16px;align-items:center;padding:13px 0;border-top:1px solid rgba(0,0,0,.07)}
.ty-lab{font:600 10px system-ui;border-radius:99px;padding:4px 10px;color:#fff;white-space:nowrap}
.ty-tx{flex:1}
.ty-foot{margin-top:18px;font:400 11.5px system-ui;color:#aaa}
.chart{width:920px;border-radius:20px;padding:26px 30px;box-shadow:__SH__}
.c-head{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:18px}
.c-head b{font:800 17px system-ui;color:#222}
.c-head span{display:block;font:400 11.5px system-ui;color:#999;margin-top:3px}
.c-leg{display:flex;align-items:center;gap:7px;font:500 11.5px system-ui;color:#666}
.c-leg span{width:12px;height:12px;border-radius:4px;margin-left:10px}
.c-plot{display:flex;gap:12px}
.c-y{display:flex;flex-direction:column;justify-content:space-between;font:500 10px system-ui;color:#aaa;padding-bottom:22px;text-align:right}
.c-area{flex:1;position:relative;height:300px}
.c-svg{position:absolute;inset:0;width:100%;height:100%}
.c-bars{position:absolute;inset:0;display:flex;align-items:flex-end;gap:10px;padding:0 8px}
.c-col{flex:1;height:100%;display:flex;align-items:flex-end}
.c-bar{width:100%;border-radius:5px 5px 0 0;opacity:.9}
.c-x{display:flex;gap:10px;padding:6px 8px 0;margin-left:34px}
.c-x span{flex:1;text-align:center;font:500 10px system-ui;color:#aaa}
.shop{width:920px;border-radius:20px;padding:44px;display:flex;gap:30px;justify-content:center;box-shadow:__SH__}
.sh-card{width:360px;border-radius:18px;overflow:hidden;box-shadow:0 18px 44px rgba(30,32,40,.18)}
.sh-stage{height:250px;position:relative;display:flex;align-items:flex-end;justify-content:center}
.sh-obj{position:relative;width:130px;height:120px}
.sh-cup{position:absolute;bottom:24px;left:30px;width:64px;height:78px;border-radius:10px 10px 14px 14px}
.sh-handle{position:absolute;bottom:48px;right:26px;width:34px;height:34px;border:9px solid;border-radius:50%}
.sh-plate{position:absolute;bottom:12px;left:16px;width:98px;height:12px;border-radius:8px}
.sh-tag{position:absolute;top:16px;left:16px;font:800 10px system-ui;letter-spacing:.12em;border-radius:99px;padding:5px 11px}
.sh-body{padding:18px 20px 20px}
.sh-name{font:700 17px system-ui;color:#222}
.sh-stars{margin-left:8px;font-size:13px;letter-spacing:2px}
.sh-name i{font:400 11px system-ui;color:#aaa;font-style:normal}
.sh-price{font:800 24px system-ui;color:#222;margin:10px 0 12px}
.sh-price s{font:500 14px system-ui;color:#bbb;margin:0 8px}
.sh-price span{font:800 11px system-ui;border-radius:99px;padding:4px 10px;vertical-align:3px}
.sh-vars{display:flex;gap:8px;margin-bottom:14px}
.sh-vars span{font:600 12px system-ui;border:1.5px solid;border-radius:8px;padding:7px 14px;color:#555}
.sh-cta{display:flex;gap:10px}
.sh-cta span{flex:1;text-align:center;font:700 13px system-ui;border-radius:9px;padding:12px 0}
.sh-cta span:last-child{flex:0 0 84px;color:#555}
.sh-trust{margin-top:12px;font:400 10.5px system-ui;color:#aaa;text-align:center}
.sh-side{width:230px;display:flex;flex-direction:column;gap:12px;justify-content:center}
.sh-mini{height:74px;border-radius:12px}
.sh-note{font:400 12px/1.6 system-ui;color:#666;padding:6px 4px}
.sh-note b{display:block;font:700 13px system-ui;color:#333;margin-bottom:5px}
.sh-specs{display:flex;flex-direction:column;gap:9px}
.sh-spec{display:flex;align-items:center;gap:10px}
.sh-spec span{width:38px;height:26px;border-radius:6px}
.sh-spec b{font:600 11px monospace;color:#555}
.sh-spec i{font:400 11px system-ui;color:#999;font-style:normal;margin-left:auto}
.mail{width:920px;border-radius:20px;overflow:hidden;display:flex;box-shadow:__SH__;border:1px solid rgba(0,0,0,.06)}
.e-list{width:250px;border-right:1px solid rgba(0,0,0,.07);padding:12px 10px;display:flex;flex-direction:column;gap:4px}
.e-item{display:flex;gap:9px;align-items:center;padding:9px 10px;border-radius:10px}
.e-av{width:30px;height:30px;border-radius:50%;flex:none}
.e-m{display:flex;flex-direction:column;min-width:0}
.e-m b{font:700 12px system-ui;color:#333;white-space:nowrap}
.e-m span{font:400 11px system-ui;color:#999;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.e-compose{margin-top:auto;text-align:center;font:700 13px system-ui;border-radius:10px;padding:11px 0}
.e-open{flex:1}
.e-band{padding:20px 26px;font:800 15px system-ui;letter-spacing:.16em}
.e-head{padding:20px 26px 0}
.e-head b{font:800 20px Georgia,serif;color:#222;display:block}
.e-head span{font:400 12.5px system-ui;color:#999}
.e-body{padding:14px 26px;font:400 13.5px/1.75 system-ui;color:#555}
.e-cta{margin:6px 26px 14px;align-self:flex-start;display:inline-block;width:max-content;font:700 13px system-ui;border-radius:9px;padding:12px 22px}
.e-foot{padding:0 26px 18px;font:400 10.5px system-ui;color:#bbb}
.ed{width:960px;display:flex;border-radius:20px;overflow:hidden;box-shadow:__SH__}
.ed-page{flex:1;padding:38px 34px;position:relative;border-right:1px solid rgba(0,0,0,.08);min-height:480px}
.ed-page.right{border-right:0}
.ed-folio{font:600 10px system-ui;letter-spacing:.22em;color:#aaa;margin-bottom:22px}
.ed-folio.end{text-align:right;position:absolute;bottom:24px;right:34px}
.ed-page h2{font:800 34px/1.12 Georgia,serif;color:#222;margin-bottom:18px}
.ed-body{font:400 13.5px/1.85 Georgia,serif;color:#444}
.ed-cap{font:700 10px system-ui;letter-spacing:.18em;border-radius:99px;padding:4px 10px;margin-right:8px}
.ed-img{height:210px;border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:20px}
.ed-motif{width:74px;height:74px;border-radius:50%}
.ed-quote{font:600 17px/1.5 Georgia,serif;color:#333;border-left:3px solid;padding-left:16px;margin-bottom:18px}
.ed-caption{font:400 11px system-ui;color:#aaa}
.pt{width:920px;border-radius:20px;padding:30px 34px;box-shadow:__SH__}
.pt-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:16px}
.pt-head b{font:800 17px system-ui;color:#222}
.pt-head span{font:400 12px system-ui;color:#999}
.pt-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
.pt-tile{aspect-ratio:1;border-radius:12px;display:flex;align-items:center;justify-content:center}
.wall-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:18px;padding:8px 0 30px}
.wall-grid.five{grid-template-columns:repeat(4,1fr)}
.wall .w-hero b{font-size:19px}
.wall .w-nav{padding:12px 14px}
.wall .w-links i{width:14px;height:3px;opacity:.45}
.wall .w-cta{font:700 9.5px system-ui;padding:5px 9px;border-radius:6px}
.wall .w-body{padding:6px 16px 14px;display:flex;flex-direction:column;gap:6px}
.wall .w-kick{font:700 8.5px system-ui;letter-spacing:.2em}
.wall .w-h{font:800 21px/1.1 Georgia,serif}
.wall .w-p{font:400 10.5px system-ui;opacity:.72}
.wall .w-btns{display:flex;gap:7px;margin-top:4px}
.wall .w-b1,.wall .w-b2{font:700 10px system-ui;border-radius:7px;padding:7px 12px}
.wall .w-b2{border:1.5px solid}
.wall .w-cards{display:flex;gap:8px;padding:0 14px 12px}
.wall .w-c{flex:1;border-radius:9px;padding:9px 10px;display:flex;align-items:center;gap:7px;border:1px solid rgba(0,0,0,.05)}
.wall .w-c i{width:14px;height:14px;border-radius:5px;flex:none}
.wall .w-c span{font:700 10.5px system-ui}
.wall .w-chips{display:flex;gap:4px;padding:0 14px 14px}
.wall .w-chips i{flex:1;height:8px;border-radius:3px}
.wall .w-hero span{opacity:.9}
.wall,.wall *{text-decoration:none}
.wall{display:block;border-radius:16px;overflow:hidden;text-decoration:none;border:1px solid rgba(0,0,0,.08);box-shadow:0 14px 36px rgba(30,32,40,.12)}
.w-nav{display:flex;justify-content:space-between;align-items:center;padding:14px 18px}
.w-links{display:flex;gap:8px;align-items:center}
.w-links i{width:16px;height:4px;border-radius:2px;opacity:.5}
.w-cta{font:700 10px system-ui;border-radius:6px;padding:5px 10px}
.w-hero{padding:26px 20px 20px}
.w-hero b{font:800 24px Georgia,serif;display:block}
.w-hero span{font:500 11.5px system-ui;opacity:.75}
.w-chips{display:flex;gap:6px;padding:0 18px 14px}
.w-chips i{flex:1;height:14px;border-radius:4px}
.w-badges{display:flex;gap:6px;padding:0 18px 16px}
.w-badges span{font:600 10px system-ui;padding:3px 9px;border-radius:99px;background:rgba(255,255,255,.4);color:inherit;border:1px solid rgba(0,0,0,.08)}
.wall .w-badges span{color:#5f6b7a;text-decoration:none}
.wall .w-cta{text-decoration:none}
.wall .w-hero span{opacity:.9}
.h2sec{font:800 30px system-ui,sans-serif;color:#1F2328;margin:72px 0 8px}
.h2sub{font:400 15px system-ui;color:#6B7280;margin-bottom:26px}
.cnt{font:700 13px system-ui;color:#57606A;letter-spacing:.08em;margin-left:8px}
.divbar{height:3px;background:#1F2328;width:64px;border-radius:2px;margin:18px 0 10px}
footer{padding:48px 0 72px;font:400 13px system-ui;color:#6B7280;text-align:center}
""".replace("__SH__", "0 24px 64px rgba(30,32,40,.16)")

    html = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>aesthete-agent — visual showcase</title><style>" + css + "</style></head><body>"
            "<div class='topnav'><div class='bar'>"
            "<a class='brand' href='../'><span class='mark'><i style='background:#FFA69E'></i><i style='background:#B8F2E6'></i></span>aesthete-agent <span class='chip'>v0.7.0</span></a>"
            "<nav><a href='#scenes'>Scenes</a><a href='#airy'>Bright &amp; Airy</a>"
            "<a href='#vivid'>Vivid &amp; Bold</a><a href='#elegant'>Elegant &amp; Deep</a>"
            "<a href='#dark'>Bright dark</a><a class='x' href='../'>&larr; Overview</a>"
            "<a class='x' href='https://github.com/docsor1212/aesthete-agent'>GitHub</a></nav>"
            "</div></div>"
            "<div class='wrap' id='top'>"
            "<header class='hero'><div class='kick'>AESTHETE-AGENT · MECHANICALLY VALIDATED AESTHETICS</div>"
            "<h1>Color systems that<br>pass the review.</h1>"
            "<p>Every scene below is rendered by the engine — roles derived in OKLCH, contrast gated, "
            "color-blind simulated, slop checked. What you see is what the tool ships.</p>"
            "<div class='chips'>" + "".join("<i style='background:#" + h + "'></i>" for h in main["hexes"]) + "</div>"
            "</header>"
            "<div class='divbar'></div>"
            "<h2 class='h2sec' id='scenes'>Ten scenes, one palette</h2>"
            "<p class='h2sub'>Bees &amp; Honey — light theme. Every canvas is 920px of real content density.</p>"
            + scenes +
            curated +
            "<h2 class='h2sec' id='dark'>Bright dark, not heavy dark</h2>"
            "<p class='h2sub'>The same engine on a dark surface: the base lifts +0.11 L and desaturates 28%, so dark never means heavy.</p>"
            + dark_scenes +
            "<footer>aesthete-agent v0.5.0 — every canvas above passed contrast / color-blind / AI-slop / scorecard gates before rendering."
            "<br><a href='../'>&larr; Overview</a> · <a href='https://github.com/docsor1212/aesthete-agent'>GitHub</a> · "
            "<a href='https://pypi.org/project/aesthete-agent-mcp/'>PyPI</a> · <a href='#top'>Back to top</a></footer>"
            "</div><script>"
"function fitStages(){document.querySelectorAll('.stage').forEach(function(st){"
"var f=st.querySelector('.fit');if(!f)return;"
"var w=920;"
"var sc=Math.min(1,(st.clientWidth-24)/w);"
"f.style.transform='translateX(-50%) scale('+sc+')';"
"st.style.height=(f.offsetHeight*sc)+'px';});}"
"window.addEventListener('resize',fitStages);window.addEventListener('load',fitStages);"
"fitStages();</script></body></html>")

    out = r"C:\Users\SeALove\ZCodeProject\aesthete-work\promo\showcase.html"
    open(out, "w", encoding="utf-8", newline="\n").write(html)
    print("showcase:", out, len(html), "bytes")


if __name__ == "__main__":
    build()
