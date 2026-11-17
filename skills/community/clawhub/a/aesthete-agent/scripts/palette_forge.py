#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""palette_forge.py — offline palette engine distilled from public palette community mechanics.

Commands:
  harmony   generate a palette from a seed color using a harmony rule (OKLCH)
  mutate    classic adjust transforms (shade/saturation/hue/temperature/luminance)
  contrast  WCAG contrast ratio + AA/AAA verdict for fg/bg pair
  roles     assign 60-30-10 role architecture + emit CSS variables
  blind     color-blindness simulation (protanopia/deuteranopia/tritanopia)
  slop      AI-slop lint (Tailwind-default family, flat lightness, purple gradient, all-vivid)
  extract   pull dominant colors from an image (needs Pillow)
  search    search the curated harvested library (palettes/palettes.json)
  card      render a self-contained HTML palette card + UI mockup for self-review
  export    emit tokens (css / tailwind / json / svg)

Core is stdlib-only. `extract` needs Pillow; everything else runs anywhere.

Color math: OKLab (Bjorn Ottosson, public domain) for perceptual operations;
WCAG 2.x relative-luminance formula for contrast; Machado et al. 2009 matrices
for color-blindness simulation (approximate, severity 1.0).
"""
import argparse
import colorsys
import hashlib
import json
import math
import os
import re
NL = chr(10)
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LIBRARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "palettes", "palettes.json")
PROFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "profile.json")


def load_profile():
    """用户偏好档案——机制化消费;不存在则返回空档(不猜)。"""
    try:
        with open(PROFILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

# ---------------------------------------------------------------- color core

def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x


def parse_hex(s):
    s = str(s).strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"bad hex: {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "%02X%02X%02X" % tuple(int(round(clamp(c) * 255)) for c in rgb)


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklab_from_srgb(rgb):
    r, g, b = (srgb_to_linear(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def srgb_from_oklab(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        clamp(linear_to_srgb(4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s)),
        clamp(linear_to_srgb(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s)),
        clamp(linear_to_srgb(-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)),
    )


def oklch_from_hex(h):
    L, a, b = oklab_from_srgb(tuple(c / 255 for c in parse_hex(h)))
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return L, C, H


def hex_from_oklch(L, C, H):
    rad = math.radians(H)
    rgb = srgb_from_oklab(L, C * math.cos(rad), C * math.sin(rad))
    return to_hex(rgb)


def gamut_fit(L, C, H):
    """Reduce chroma until (L,C,H) fits sRGB. Returns fitted C."""
    rad = math.radians(H)
    for step in range(33):
        c = C * (1 - step / 32)
        a, b = c * math.cos(rad), c * math.sin(rad)
        l_ = L + 0.3963377774 * a + 0.2158037573 * b
        m_ = L - 0.1055613458 * a - 0.0638541728 * b
        s_ = L - 0.0894841775 * a - 1.2914855480 * b
        l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
        vals = (
            4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
        )
        if all(-0.002 <= v <= 1.002 for v in vals):
            return c
    return 0.0


def hsl(h):
    r, g, b = (c / 255 for c in parse_hex(h))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ll, ss


# ------------------------------------------------------------ WCAG contrast

def rel_luminance(h):
    r, g, b = (srgb_to_linear(c / 255) for c in parse_hex(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    l1, l2 = sorted((rel_luminance(fg), rel_luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def wcag_verdict(ratio, large=False):
    aa = 3.0 if large else 4.5
    aaa = 4.5 if large else 7.0
    verdicts = []
    verdicts.append("AA PASS" if ratio >= aa else "AA FAIL")
    verdicts.append("AAA PASS" if ratio >= aaa else "AAA FAIL")
    return verdicts


def readable_text(bg):
    """palette-site is-light equivalent: pick black or white text per WCAG."""
    if contrast_ratio("000000", bg) >= contrast_ratio("FFFFFF", bg):
        return "000000"
    return "FFFFFF"


# --------------------------------------------------- color-blind simulation
# Machado, Oliveira & Fernandes 2009, severity 1.0 (RGB-space matrices)

CB_MATRICES = {
    "protanopia": (
        0.152286, 1.052583, -0.204868,
        0.114503, 0.786281, 0.099216,
        -0.003882, -0.048116, 1.051998,
    ),
    "deuteranopia": (
        0.367322, 0.860646, -0.227968,
        0.280085, 0.672501, 0.047413,
        -0.011820, 0.042940, 0.968881,
    ),
    "tritanopia": (
        1.255528, -0.076749, -0.178779,
        -0.078411, 0.930809, 0.147602,
        0.004733, 0.691367, 0.303900,
    ),
}


def simulate_cb(h, kind):
    r, g, b = (c / 255 for c in parse_hex(h))
    m = CB_MATRICES[kind]
    out = (
        m[0] * r + m[1] * g + m[2] * b,
        m[3] * r + m[4] * g + m[5] * b,
        m[6] * r + m[7] * g + m[8] * b,
    )
    return to_hex(tuple(clamp(c) for c in out))


# ------------------------------------------------------------- AI-slop lint

TAILWIND_DEFAULTS = {
    "3B82F6": "blue-500", "6366F1": "indigo-500", "8B5CF6": "violet-500",
    "A855F7": "purple-500", "EC4899": "pink-500", "6D28D9": "violet-700",
    "4F46E5": "indigo-600", "0EA5E9": "sky-500", "22D3EE": "cyan-400",
}


def slop_lint(hexes):
    findings = []
    upper = [h.upper() for h in hexes]
    hits = [(h, TAILWIND_DEFAULTS[h]) for h in upper if h in TAILWIND_DEFAULTS]
    if hits:
        findings.append(f"MEDIAN-TRAP: Tailwind tutorial defaults present: "
                        f"{', '.join(f'#{h} ({n})' for h, n in hits)} — this is the "
                        f"'median of training data' look; pick another route")
    Ls = [oklch_from_hex(h)[0] for h in upper]
    if max(Ls) - min(Ls) < 0.25:
        findings.append(f"FLAT-LIGHTNESS: L range {max(Ls)-min(Ls):.2f} < 0.25 — no light/dark "
                        f"architecture; text/bg roles will fail contrast")
    purpleish = [oklch_from_hex(h) for h in upper
                 if 275 <= oklch_from_hex(h)[2] <= 330 and oklch_from_hex(h)[1] > 0.12]
    if len(purpleish) >= 2 and abs(purpleish[0][0] - purpleish[1][0]) < 0.2:
        findings.append("PURPLE-GRADIENT: two mid-light chromatic purples — the #1 AI-slop signature")
    if Ls and all(oklch_from_hex(h)[1] > 0.16 and oklch_from_hex(h)[0] > 0.45 for h in upper):
        findings.append("ALL-VIVID: every color loud — no quiet surface for content to rest on")
    if not findings:
        findings.append("CLEAN: no known slop signature detected (taste is still yours)")
    return findings


# ------------------------------------------------------------ subcommands



def apca(txt, bg):
    """APCA 0.1.9 感知对比度(WCAG 3 草案方向):返回 Lc 值(0-108+,越大越清晰)。
    指南:正文 Lc>=75(理想 90)/大字 >=60/粗大字 >=45/非文字 >=30/低于 15 不可见。"""
    def ychan(h):
        c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
        return tuple((x/12.92 if x <= 0.04045 else ((x+0.055)/1.055)**2.4) for x in c)
    def devY(c):
        y = 0.2126729*c[0]**2.4 + 0.7151522*c[1]**2.4 + 0.0721750*c[2]**2.4
        return y + (0.022 - y)**1.414 if y < 0.022 else y
    yt, yb = devY(ychan(txt)), devY(ychan(bg))
    if yb > yt:
        sapc = (yb**0.56 - yt**0.57) * 1.14
    else:
        sapc = (yb**0.65 - yt**0.62) * 1.14
    lc = abs(sapc) * 100
    return round(lc, 1) if abs(sapc) > 0.1 else 0.0


def apca_verdict(lc):
    if lc >= 90: return "正文理想"
    if lc >= 75: return "正文最低"
    if lc >= 60: return "大字/流畅"
    if lc >= 45: return "粗大字>=24px"
    if lc >= 30: return "非文字最低"
    if lc >= 15: return "不可见边缘"
    return "不可见"


def _export_w3c(hexes):
    toks = {"color": {}, "guideline": {"$type": "content",
            "$value": "WCAG 2.2 AA: body>=4.5:1, large/UI>=3:1; APCA Lc>=75 body"}}
    for i, h in enumerate(hexes):
        toks["color"][f"palette-{i+1}"] = {"$type": "color", "$value": f"#{h}"}
    return json.dumps(toks, ensure_ascii=False, indent=2)


def _export_context(hexes):
    rs = sorted(((oklch_from_hex(h), h) for h in hexes), key=lambda t: -t[0][0])
    bg, ink = rs[0][1], rs[-1][1]
    cands = [(oklch_from_hex(h)[1], h) for h in hexes if h not in (bg, ink)]
    accent = max(cands)[1] if cands else bg
    body_pair = contrast_ratio(ink, bg)
    best = max(((contrast_ratio(a, b), a, b) for i, a in enumerate(hexes) for b in hexes[i+1:]))
    ctx = []
    ctx.append("# Color System Context(可直接粘贴给任何 LLM 的配色上下文)")
    ctx.append("")
    ctx.append("## Tokens")
    for i, h in enumerate(hexes, 1):
        L, C, H = oklch_from_hex(h)
        ctx.append(f"- palette-{i}: #{h} (OKLCH {L:.2f} {C:.3f} {H:.0f}deg)")
    ctx.append("")
    ctx.append("## Roles(60-30-10)")
    ctx.append(f"- background: #{bg} (60%)")
    ctx.append(f"- text: #{ink} (contrast vs bg {body_pair:.2f}:1)")
    ctx.append(f"- accent: #{accent} (<=10%, 稀缺即力量)")
    ctx.append("")
    ctx.append("## Guardrails(硬规则)")
    ctx.append("- 正文对比 >=4.5:1,大字/非文字 >=3:1(APCA Lc>=75/60 为感知口径)")
    ctx.append("- accent 不超过全页 10%;最强色拥有一块完整区域")
    ctx.append("- 禁:Tailwind 默认族(#3B82F6/#6366F1/#8B5CF6)/紫渐变/全高饱和/平坦明度")
    ctx.append("- 红绿永不作唯一区分;图表用明度阶梯+冗余编码")
    ctx.append(f"- 已验证最优对: #{best[1]} on #{best[2]} = {best[0]:.2f}:1")
    return chr(10).join(ctx)


def _viz_weak_voices(bg, surface, ink, ink2, muted_target=4.5, disabled_target=3.05):
    """弱声部两档(A2 新增): 沿 bg->ink 的 OKLCH 明度梯二分取色, 保 ink 色相。
    落底背景 land = bg/surface 中更暗的那面(同一弱色铺在更暗的面上比值更小, 按最坏面钉线)。
      muted    = 正文次级声部(段落/表体/引用/控件标签与 currentColor 描边): 目标 >=4.5:1
      disabled = 最低声部(禁用态/作废价/坐标轴/脚注)+ 非文字占位图元: 目标 >=3:1(WCAG 1.4.11)
    disabled 钉线不超过 ink2 实际比值, 以免"最低声部"比 ink2 更黑(梯序倒挂);
    两档的 3:1 硬底线达不到就直接 raise —— 绝不静默回落。"""
    land = min((bg, surface), key=lambda h: rel_luminance(h))
    bL, bC, bH = oklch_from_hex(bg)
    iL, iC, iH = oklch_from_hex(ink)
    cL, cC, cH = oklch_from_hex(ink2)
    C = min(0.045, max(bC, 0.012))

    def ramp(frac):
        L = bL + (iL - bL) * frac
        return hex_from_oklch(L, gamut_fit(L, C, iH), iH).upper()

    def pin(target):
        lo, hi = 0.0, 1.0
        if contrast_ratio(ramp(hi), land) < target:      # 整条梯都够不到 -> 交给调用方报错
            return ramp(hi)
        for _ in range(24):
            mid = (lo + hi) / 2.0
            if contrast_ratio(ramp(mid), land) >= target:
                hi = mid
            else:
                lo = mid
        return ramp(hi)

    r2 = contrast_ratio(ink2, land)
    muted = pin(min(muted_target, max(3.0, contrast_ratio(ink, land))))
    disabled = pin(min(disabled_target, max(3.0, r2 - 0.05)))
    for k, v in (("muted", muted), ("disabled", disabled)):
        r = contrast_ratio(v, land)
        if r < 3.0:
            raise ValueError("assert_weak_voice_floor: 角色 %s=#%s 对落底背景 #%s 只有 %.2f:1"
                             " (<3:1), 拒绝产出" % (k, v, land, r))
    return muted, disabled


def _viz_roles(hexes, dark=None):
    """角色自动映射: bg/surface/ink/ink2/accent(+danger 若存在红系)。dark 缺省按明度均值自判。"""
    info = sorted(((oklch_from_hex(h)[0], h) for h in hexes), key=lambda t: -t[0])
    mL = sum(t[0] for t in info) / len(info)
    if dark is None:
        dark = mL < 0.5
    ordered = info if not dark else list(reversed(info))
    bg = ordered[0][1]
    ink = ordered[-1][1]
    if dark:
        # 明亮暗色: 大底抬亮+降饱和, 暗色不压抑(审美铁律: 暗色不是黑压压)
        bL0, bC0, bH0 = oklch_from_hex(bg)
        bL1 = min(0.42, bL0 + 0.11)
        bg = hex_from_oklch(bL1, gamut_fit(bL1, bC0 * 0.72, bH0), bH0).upper()
    rest = [t for t in ordered[1:-1]] or ordered[:1]
    accent = max(rest, key=lambda t: oklch_from_hex(t[1])[1])[1] if rest else bg
    # surface/ink2 派生而非挑选: 从 bg/ink 沿 OKLCH 插值, 保色相降饱和,
    # 避免把高饱和色(如暗红)当成中性面、或弱对比色当次级文字
    bL, bC, bH = oklch_from_hex(bg)
    iL, iC, iH = oklch_from_hex(ink)
    # 浅色主题 surface 近纸白(微降), 深色主题明显抬升 — 非对称
    sFrac = 0.06 if not dark else 0.16
    sL = bL + (iL - bL) * sFrac
    surface = hex_from_oklch(sL, gamut_fit(sL, bC * 0.9, bH), bH).upper()
    mL2 = bL + (iL - bL) * 0.52
    c2 = min(0.05, iC * 0.6 + 0.01)
    ink2 = hex_from_oklch(mL2, gamut_fit(mL2, c2, iH), iH).upper()
    _k = 0
    while contrast_ratio(ink2, bg) < 3.0 and _k < 10:
        _k += 1
        cL2 = mL2 + (iL - mL2) * _k / 10
        ink2 = hex_from_oklch(cL2, gamut_fit(cL2, c2, iH), iH).upper()
    reds = []
    for _, h in ordered:
        _, C, H = oklch_from_hex(h)
        if 8 <= H <= 35 and C > 0.08 and h not in (bg, ink, accent):
            reds.append(h)
    danger = None
    if reds:
        reds.sort(key=lambda h: -contrast_ratio(h, bg))
        if contrast_ratio(reds[0], bg) >= 3.0:
            danger = reds[0]
    if danger is None:
        danger = accent if contrast_ratio(accent, bg) >= 3.0 else ink
    # accent_text: accent 当文字用不达标时, 沿 OKLCH 向 ink 爬坡亮度直到 3:1
    atext = accent
    if contrast_ratio(accent, bg) < 3.0:
        aL, aC, aH = oklch_from_hex(accent)
        for k in range(1, 11):
            cL = aL + (iL - aL) * k / 10
            cand = hex_from_oklch(cL, gamut_fit(cL, aC, aH), aH).upper()
            atext = cand
            if contrast_ratio(cand, bg) >= 3.0:
                break
    muted, disabled = _viz_weak_voices(bg, surface, ink, ink2)
    return {"bg": bg, "surface": surface, "ink": ink, "ink2": ink2, "accent": accent,
            "danger": danger, "atext": atext, "dark": dark,
            "muted": muted, "disabled": disabled}


def _viz_text_levels(R):
    """多级文字阶梯(弱声部系统): ink/ink2 之外的弱声部。
    t3=弱小字(脚注/图注), t4=最弱(占位/划线价), 从 bg→ink 沿 OKLCH 派生并保底 1.5:1。"""
    bL, bC, bH = oklch_from_hex(R["bg"])
    iL, iC, iH = oklch_from_hex(R["ink"])
    lv = {}
    for key, frac in (("t3", 0.34), ("t4", 0.18)):
        L = bL + (iL - bL) * frac
        C = min(0.045, max(bC, 0.012))
        h6 = hex_from_oklch(L, gamut_fit(L, C, iH), iH).upper()
        k = 0
        while contrast_ratio(h6, R["bg"]) < 1.5 and k < 10:
            k += 1
            L2 = L + (iL - L) * k / 10
            h6 = hex_from_oklch(L2, gamut_fit(L2, C, iH), iH).upper()
        lv[key] = h6
    return lv


def _viz_render(ord_hexes, theme, label):
    """同场景换色渲染一个 variant(吸收 visualizer 空格洗牌循环:设计固定,色板变化)。"""
    hexes = ord_hexes
    R = _viz_roles(hexes, dark=theme)
    t_on = {k: readable_text(v) for k, v in R.items() if k != "dark"}
    # 辅助口声色(sage/honey 类): 文字用途须对 surface>=3:1, 从次高饱度色里挑, 兜底 ink2
    _cands = sorted((h for h in hexes if h not in (R["accent"], R["bg"], R["ink"])),
                    key=lambda h: -oklch_from_hex(h)[1])
    sage = next((h for h in _cands if contrast_ratio(h, R["surface"]) >= 3.0), R["ink2"])
    honey = (_cands[0] if _cands and contrast_ratio(_cands[0], R["surface"]) >= 1.6
             else R["ink2"])
    tl = _viz_text_levels(R)
    legend = NL.join(
        "<span class='chip' style='background:#" + R[k] + ";color:#" + t_on[k] + "'>" + k + ":#" + R[k] + "</span>"
        for k in ("bg", "surface", "ink", "ink2", "accent", "atext", "danger"))
    css = (NL.join([
        "body{margin:0;background:#23272E;font-family:system-ui,sans-serif;color:#E8EEF6}",
        "header{padding:16px 22px;border-bottom:1px solid rgba(255,255,255,.12)}",
        "header h1{font-size:16px;margin:0 0 10px}",
        "header h1 b{color:#F2CC8F}",
        ".chips{display:flex;gap:8px;flex-wrap:wrap}",
        ".chip{padding:4px 10px;border-radius:99px;font:600 11px monospace}",
        ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:16px;padding:16px}",
        ".scene{background:#fff;border-radius:10px;overflow:hidden}",
        ".scene h2{font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.85;",
        "  margin:0;padding:8px 14px;background:#F2F2F0;color:#444}",
        ".badge{float:right;font:700 10px monospace;color:#7CD992}",
        ".vsec{padding:6px 0 2px}",
        ".vhead{padding:10px 22px 0;font:700 13px system-ui;color:#F2CC8F;display:flex;gap:12px;align-items:center}",
        ".vhead .badge{float:none}",
        ".vhead .chips{padding:0}"
    ]))
    scenes = []

    # S1 Mobile App
    tpl = NL.join([
      "<div style='width:230px;margin:14px auto;border:1px solid #ddd;border-radius:18px;overflow:hidden;background:%(bg)s'>",
      "  <div style='padding:5px 12px;font:600 9px system-ui;color:%(tbg)s;display:flex;justify-content:space-between'><span>9:41</span><span>●●●</span></div>",
      "  <div style='padding:12px 14px 8px;color:%(ink)s;font:700 15px system-ui'>Wallet</div>",
      "  <div style='margin:0 12px;padding:14px;border-radius:12px;background:%(accent)s;color:%(tac)s'>",
      "    <div style='font:600 10px system-ui;opacity:.8'>Balance</div>",
      "    <div style='font:800 22px system-ui'>12,480</div></div>",
      "  <div style='margin:10px 12px;padding:10px 12px;border-radius:10px;background:%(surface)s;color:%(ink)s;display:flex;gap:10px;align-items:center'>",
      "    <div style='width:30px;height:30px;border-radius:8px;background:%(ink2)s'></div>",
      "    <div style='font:600 12px system-ui'>Coffee run<div style='font:400 10px;color:%(ink2)s'>Today 08:12</div></div>",
      "    <div style='margin-left:auto;font:700 12px;color:%(danger)s'>-28</div></div>",
      "  <div style='margin:10px 12px 14px;padding:10px 12px;border-radius:10px;background:%(surface)s;color:%(ink)s;display:flex;gap:10px;align-items:center'>",
      "    <div style='width:30px;height:30px;border-radius:8px;background:%(honey)s'></div>",
      "    <div style='font:600 12px system-ui'>Salary<div style='font:400 10px;color:%(ink2)s'>Mar 01</div></div>",
      "    <div style='margin-left:auto;font:700 12px;color:%(sage)s'>+9,500</div></div>",
      "  <div style='display:flex;justify-content:space-around;padding:8px 0 12px;border-top:1px solid rgba(0,0,0,.06)'>",
      "    <div style='width:18px;height:18px;border-radius:5px;background:%(accent)s'></div>",
      "    <div style='width:18px;height:18px;border-radius:5px;background:%(ink2)s;opacity:.4'></div>",
      "    <div style='width:18px;height:18px;border-radius:5px;background:%(ink2)s;opacity:.4'></div></div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(surface)s": R["surface"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"],
         "%(accent)s": R["accent"], "%(danger)s": R["danger"], "%(honey)s": hexes[2 % len(hexes)],
         "%(sage)s": sage, "%(tbg)s": t_on["bg"], "%(tac)s": t_on["accent"]}
    scenes.append(("Mobile App · 金融卡", _fill(tpl, m)))

    # S2 Landing
    tpl = NL.join([
      "<div style='background:%(bg)s;color:%(ink)s'>",
      "  <div style='display:flex;align-items:center;gap:10px;padding:12px 16px'>",
      "    <div style='width:22px;height:22px;border-radius:6px;background:%(accent)s'></div>",
      "    <b style='font:700 13px system-ui'>acme</b>",
      "    <span style='margin-left:auto;font:500 11px system-ui;color:%(ink2)s'>Docs&nbsp;&nbsp;Pricing</span>",
      "    <span style='padding:6px 12px;border-radius:6px;background:%(accent)s;color:%(tac)s;font:600 11px system-ui'>Sign up</span></div>",
      "  <div style='text-align:center;padding:26px 18px 20px'>",
      "    <div style='font:800 22px/1.25 system-ui'>Ship color systems<br>that pass review</div>",
      "    <div style='font:400 12px system-ui;color:%(ink2)s;margin:8px 0 14px'>Mechanically validated palettes for your product.</div>",
      "    <span style='padding:8px 16px;border-radius:7px;background:%(ink)s;color:%(tink)s;font:600 12px system-ui'>Get started</span>",
      "    <span style='padding:8px 16px;border-radius:7px;border:1px solid %(ink2)s;color:%(ink)s;font:600 12px system-ui;margin-left:6px'>Live demo</span></div>",
      "  <div style='display:flex;gap:8px;padding:0 16px 18px'>",
      "    <div style='flex:1;border:1px solid %(cardline)s;border-radius:8px;padding:10px;background:%(surface)s'>",
      "      <div style='width:20px;height:20px;border-radius:5px;background:%(honey)s'></div>",
      "      <div style='font:700 11px system-ui;margin-top:6px'>Fast</div>",
      "      <div style='font:400 10px system-ui;color:%(csub)s'>Instant checks</div></div>",
      "    <div style='flex:1;border:1px solid %(cardline)s;border-radius:8px;padding:10px;background:%(surface)s'>",
      "      <div style='width:20px;height:20px;border-radius:5px;background:%(sage)s'></div>",
      "      <div style='font:700 11px system-ui;margin-top:6px'>Proven</div>",
      "      <div style='font:400 10px system-ui;color:%(csub)s'>WCAG + APCA</div></div></div></div>",
    ])
    # 0.7.0 修复:暗色下卡片边框换浅线,弱文字(ink2 对 surface <3:1)升级为 ink——暗绿卡片文字不可读旧账
    csub = R["ink2"] if contrast_ratio(R["ink2"], R["surface"]) >= 3.0 else R["ink"]
    m = {"%(bg)s": R["bg"], "%(surface)s": R["surface"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"],
         "%(accent)s": R["accent"], "%(honey)s": hexes[2 % len(hexes)], "%(sage)s": sage,
         "%(tink)s": t_on["ink"], "%(tac)s": t_on["accent"],
         "%(cardline)s": "rgba(255,255,255,.16)" if theme else "rgba(0,0,0,.08)",
         "%(csub)s": csub}
    scenes.append(("Landing · 落地页", _fill(tpl, m)))

    # S3 Dashboard
    bars = "".join(
        "<div style='flex:1;height:" + str(30 + ((i * 23) % 60)) + "%;background:#" +
        (R["accent"] if i == 3 else hexes[(i + 1) % len(hexes)]) +
        ";border-radius:3px 3px 0 0'></div>" for i in range(7))
    tpl = NL.join([
      "<div style='display:flex;min-height:210px;background:%(bg)s'>",
      "  <div style='width:52px;background:%(surface)s;padding:10px 0;display:flex;flex-direction:column;gap:10px;align-items:center'>",
      "    <div style='width:20px;height:20px;border-radius:6px;background:%(accent)s'></div>",
      "    <div style='width:16px;height:16px;border-radius:4px;background:%(ink2)s;opacity:.5'></div>",
      "    <div style='width:16px;height:16px;border-radius:4px;background:%(ink2)s;opacity:.5'></div>",
      "    <div style='width:16px;height:16px;border-radius:4px;background:%(ink2)s;opacity:.5'></div></div>",
      "  <div style='flex:1;padding:12px;color:%(ink)s'>",
      "    <div style='display:flex;gap:8px'>",
      "      <div style='flex:1;background:%(surface)s;border-radius:8px;padding:10px'><div style='font:500 9px system-ui;color:%(ink2)s'>MRR</div><div style='font:800 16px system-ui'>86k</div></div>",
      "      <div style='flex:1;background:%(surface)s;border-radius:8px;padding:10px'><div style='font:500 9px system-ui;color:%(ink2)s'>Active</div><div style='font:800 16px system-ui'>1,204</div></div>",
      "      <div style='flex:1;background:%(surface)s;border-radius:8px;padding:10px'><div style='font:500 9px system-ui;color:%(ink2)s'>Churn</div><div style='font:800 16px system-ui;color:%(danger)s'>1.9%</div></div></div>",
      "    <div style='display:flex;align-items:flex-end;gap:6px;height:70px;margin-top:10px;background:%(surface)s;border-radius:8px;padding:10px'>%(bars)s</div>",
      "    <div style='margin-top:8px;background:%(surface)s;border-radius:8px;overflow:hidden;font:500 10px system-ui'>",
      "      <div style='display:flex;justify-content:space-between;padding:6px 10px;border-bottom:1px solid rgba(0,0,0,.05)'><span>Acme Corp</span><b>12,400</b></div>",
      "      <div style='display:flex;justify-content:space-between;padding:6px 10px'><span>Globex</span><b>8,150</b></div></div></div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(surface)s": R["surface"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"],
         "%(accent)s": R["accent"], "%(danger)s": R["danger"], "%(bars)s": bars}
    scenes.append(("Dashboard · 仪表盘", _fill(tpl, m)))

    # S4 Branding
    tpl = NL.join([
      "<div style='padding:16px;background:%(bg)s'>",
      "  <div style='max-width:250px;margin:0 auto;background:%(surface)s;border-radius:8px;padding:16px;box-shadow:0 4px 14px rgba(0,0,0,.10)'>",
      "    <div style='display:flex;align-items:center;gap:8px'>",
      "      <div style='width:26px;height:26px;border-radius:50%;background:%(accent)s'></div>",
      "      <b style='font:800 13px system-ui;letter-spacing:.06em;color:%(ink)s'>STUDIO NOVA</b></div>",
      "    <div style='height:1px;background:rgba(0,0,0,.08);margin:10px 0'></div>",
      "    <div style='font:400 10px/1.7 system-ui;color:%(ink2)s'>Lin Zhang · Design Lead<br>studio.nova@example.com<br>+86 138 0000 0000</div>",
      "    <div style='margin-top:10px;display:flex;gap:5px'>",
      "      <div style='width:14px;height:14px;border-radius:3px;background:%(honey)s'></div>",
      "      <div style='width:14px;height:14px;border-radius:3px;background:%(sage)s'></div>",
      "      <div style='width:14px;height:14px;border-radius:3px;background:%(ink)s'></div></div></div>",
      "  <div style='max-width:250px;margin:10px auto 4px;border-radius:8px;overflow:hidden;display:flex;height:54px'>",
      "    <div style='flex:2;background:%(ink)s;color:%(tink)s;display:flex;align-items:center;justify-content:center;font:800 13px system-ui;letter-spacing:.2em'>NOVA</div>",
      "    <div style='flex:1;background:%(accent)s'></div>",
      "    <div style='flex:1;background:%(honey)s'></div>",
      "    <div style='flex:1;background:%(sage)s'></div></div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(surface)s": R["surface"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"],
         "%(accent)s": R["accent"], "%(honey)s": hexes[2 % len(hexes)], "%(sage)s": sage,
         "%(tink)s": t_on["ink"]}
    scenes.append(("Branding · 名片与色带", _fill(tpl, m)))

    # S5 Typography
    tpl = NL.join([
      "<div style='padding:16px 18px;background:%(bg)s;color:%(ink)s'>",
      "  <div style='font:800 30px/1.1 Georgia,serif'>Aa Palette in Type</div>",
      "  <div style='font:700 15px system-ui;margin-top:8px'>Heading 2 — structure speaks in the darkest ink</div>",
      "  <div style='font:400 12px/1.7 system-ui;color:%(ink2)s;margin-top:6px'>Body 12px — secondary ink at 1.7 line height. The quick brown fox jumps over the lazy dog 0123456789.</div>",
      "  <div style='font:600 10px system-ui;letter-spacing:.18em;color:%(atext)s;margin-top:8px'>EYEBROW LABEL — ACCENT VOICE</div>",
      "  <div style='font:400 10px monospace;color:%(ink2)s;margin-top:6px'>mono 10px — data: 1,204 · 86.4% · +3.2</div>",
      "  <div style='font:400 10px system-ui;color:%(t3)s;margin-top:4px'>Caption — faint voice for footnotes and axis labels</div>",
      "  <div style='font:400 11px system-ui;color:%(t4)s;margin-top:3px'>Placeholder — weakest voice, decorative only</div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"], "%(atext)s": R["atext"],
         "%(t3)s": tl["t3"], "%(t4)s": tl["t4"]}
    scenes.append(("Typography · 字阶标本", _fill(tpl, m)))

    # S6 Pattern
    tiles = ""
    for i in range(6):
        h = hexes[i % len(hexes)]
        tiles += ("<div style='aspect-ratio:1;border-radius:6px;display:flex;align-items:center;"
                  "justify-content:center;background:#" + h + "'>"
                  "<div style='width:55%;height:55%;border-radius:50%;background:#" +
                  readable_text(h) + ";opacity:.16'></div></div>")
    sc = ("<div style='padding:14px;background:#" + R["bg"] + "'>"
          "<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:8px'>" + tiles + "</div></div>")
    scenes.append(("Pattern · 图案节奏", sc))


    # S7 Data Chart
    cbars = ""
    for i in range(7):
        h1 = 30 + ((i * 37) % 65)
        h2 = 22 + ((i * 23) % 45)
        cbars += ("<div style='flex:1;display:flex;align-items:flex-end;gap:3px;align-self:stretch'>"
                  "<div style='flex:1;height:" + str(h1) + "%;background:#" + R["accent"] + ";border-radius:2px 2px 0 0'></div>"
                  "<div style='flex:1;height:" + str(h2) + "%;background:#" + R["ink2"] + ";opacity:.45;border-radius:2px 2px 0 0'></div></div>")
    tpl = NL.join([
      "<div style='padding:14px 16px;background:%(bg)s;color:%(ink)s'>",
      "  <div style='display:flex;justify-content:space-between;align-items:baseline'>",
      "    <b style='font:700 13px system-ui'>Weekly active users</b>",
      "    <span style='font:500 9px system-ui;color:%(t3)s'>Mar 1–7</span></div>",
      "  <div style='display:flex;align-items:flex-end;gap:10px;height:110px;margin-top:10px;border-bottom:2px solid %(ink2)s;padding:0 4px'>%(cbars)s</div>",
      "  <div style='display:flex;gap:14px;margin-top:8px;font:500 9px system-ui;color:%(t3)s'>",
      "    <span><span style='display:inline-block;width:8px;height:8px;background:%(accent)s;border-radius:2px'></span> 2026</span>",
      "    <span><span style='display:inline-block;width:8px;height:8px;background:%(ink2)s;border-radius:2px'></span> 2025</span></div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"], "%(accent)s": R["accent"],
         "%(t3)s": tl["t3"], "%(cbars)s": cbars}
    scenes.append(("Data Chart · 数据图表", _fill(tpl, m)))

    # S8 E-commerce Product Card
    tpl = NL.join([
      "<div style='padding:14px;background:%(bg)s'>",
      "  <div style='width:200px;margin:0 auto;background:%(surface)s;border-radius:10px;overflow:hidden;border:1px solid rgba(0,0,0,.06)'>",
      "    <div style='height:100px;background:%(accent)s;display:flex;align-items:center;justify-content:center'>",
      "      <div style='width:52px;height:68px;border-radius:6px;background:%(honey)s'></div></div>",
      "    <div style='padding:10px 12px'>",
      "      <div style='font:700 12px system-ui;color:%(ink)s'>Ceramic Pour-Over Set</div>",
      "      <div style='font:500 9px system-ui;color:%(t3)s;margin-top:2px'>★★★★★ <span style='color:%(t4)s'>(214)</span></div>",
      "      <div style='margin-top:6px'><b style='font:800 15px system-ui;color:%(ink)s'>248</b> <span style='font:400 10px system-ui;color:%(t4)s;text-decoration:line-through'>328</span></div>",
      "      <div style='margin-top:8px;padding:7px 0;text-align:center;border-radius:6px;background:%(accent)s;color:%(tac)s;font:700 11px system-ui'>Add to cart</div>",
      "      <div style='font:400 9px system-ui;color:%(t3)s;margin-top:6px'>Free shipping over 199 · 7-day returns</div></div></div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(surface)s": R["surface"], "%(ink)s": R["ink"], "%(accent)s": R["accent"],
         "%(honey)s": honey, "%(tac)s": t_on["accent"], "%(t3)s": tl["t3"], "%(t4)s": tl["t4"]}
    scenes.append(("E-commerce · 商品卡", _fill(tpl, m)))

    # S9 Email Template
    tpl = NL.join([
      "<div style='background:%(surface)s;padding:14px'>",
      "  <div style='max-width:260px;margin:0 auto;background:%(bg)s;border-radius:8px;overflow:hidden;border:1px solid rgba(0,0,0,.07)'>",
      "    <div style='padding:10px 14px;background:%(accent)s;color:%(tac)s;font:800 12px system-ui'>acme weekly</div>",
      "    <div style='padding:14px'>",
      "      <div style='font:800 15px/1.3 system-ui;color:%(ink)s'>The color issue #42</div>",
      "      <div style='height:3px;width:36px;background:%(honey)s;margin:8px 0'></div>",
      "      <div style='font:400 11px/1.6 system-ui;color:%(ink2)s'>This week: three palettes that pass every mechanical gate, and why muted beats loud.</div>",
      "      <div style='margin-top:10px;display:inline-block;padding:8px 14px;border-radius:6px;background:%(ink)s;color:%(tink)s;font:700 11px system-ui'>Read the issue</div></div>",
      "    <div style='padding:8px 14px;border-top:1px solid rgba(0,0,0,.06);font:400 9px system-ui;color:%(t3)s'>You receive this because you subscribed · unsubscribe</div></div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(surface)s": R["surface"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"], "%(accent)s": R["accent"],
         "%(honey)s": honey, "%(tac)s": t_on["accent"], "%(tink)s": t_on["ink"], "%(t3)s": tl["t3"]}
    scenes.append(("Email · 邮件模板", _fill(tpl, m)))

    # S10 Editorial
    tpl = NL.join([
      "<div style='padding:14px 16px;background:%(bg)s;color:%(ink)s'>",
      "  <div style='font:800 11px system-ui;letter-spacing:.3em;color:%(atext)s'>THE REVIEW</div>",
      "  <div style='font:800 19px/1.2 Georgia,serif;margin-top:6px'>The quiet power of a restrained palette</div>",
      "  <div style='display:flex;gap:10px;margin-top:8px'>",
      "    <div style='flex:1;font:400 10px/1.65 Georgia,serif;color:%(ink2)s'>Design movements come and go, but restraint compounds. A palette of five disciplined colors outlives any trend cycle and reads as intent.</div>",
      "    <div style='flex:1;font:400 10px/1.65 Georgia,serif;color:%(ink2)s;border-left:2px solid %(accent)s;padding-left:10px'>Mechanical validation does not kill taste — it protects it from the median.</div></div></div>",
    ])
    m = {"%(bg)s": R["bg"], "%(ink)s": R["ink"], "%(ink2)s": R["ink2"], "%(accent)s": R["accent"], "%(atext)s": R["atext"]}
    scenes.append(("Editorial · 杂志编辑页", _fill(tpl, m)))


    body = ""
    for title, inner in scenes:
        body += "<div class='scene'><h2>" + title + "</h2>" + inner + "</div>"
    badge_r = contrast_ratio(R["ink"], R["bg"])
    badge = "text/bg %.2f:1" % badge_r + (" AA" if badge_r >= 4.5 else "")
    head = ("<div class='vsec'><div class='vhead'><b>" + label + "</b>" +
            "<span class='badge'>" + badge + "</span></div>"
            "<div class='chips'>" + legend + "</div></div>")
    sec = head + "<div class='grid'>" + body + "</div>"
    return css, sec


def cmd_visualize(args):
    """Palette Visualizer: 色板套进 10 类真实 UI 场景自审;
    --svg 槽位清单重着色(纯黑白保留), --shuffle N 出多排列对比网格。"""
    hexes = [h.upper() for h in palette_list(args.palette)]
    if len(hexes) < 3:
        print("至少 3 色", file=sys.stderr); sys.exit(2)
    n_var = max(1, min(int(getattr(args, "variants", 1) or 1), 6))
    orders = [hexes[i:] + hexes[:i] for i in range(n_var)]
    if n_var >= 2:
        orders[1] = list(reversed(orders[1]))
    if args.svg:
        if not os.path.exists(args.svg):
            print(f"文件不存在: {args.svg}", file=sys.stderr); sys.exit(2)
        raw = open(args.svg, encoding="utf-8", errors="ignore").read()
        # 槽位清单模型: 提取 SVG 自身颜色清单,
        # 按明度秩映射色板, 纯黑白保留, 设计的明暗结构不被破坏
        found = re.findall(r"(?:fill|stroke)[:=][\"']?\s*(#[0-9a-fA-F]{3,6})", raw)
        inv = []
        for c in found:
            c = c[1:].upper()
            if len(c) == 3:
                c = "".join(x * 2 for x in c)
            if len(c) != 6 or c in ("000000", "FFFFFF") or c not in inv:
                if len(c) == 6 and c not in ("000000", "FFFFFF"):
                    inv.append(c)
        inv.sort(key=lambda h: oklch_from_hex(h)[0])
        n_sh = max(1, min(int(getattr(args, "shuffle", 1) or 1), 6))
        def _rank_map(svg_txt, order):
            # order 即映射序列: k=0 传明度排序(保设计明暗结构), k>=1 传排列(变体)
            pal = list(order)
            def _tgt(c):
                i = inv.index(c)
                if len(pal) == 1 or len(inv) == 1:
                    return pal[0]
                return pal[round(i * (len(pal) - 1) / (len(inv) - 1))]
            def _t(m):
                c = m.group(2).strip("#").upper()
                if len(c) == 3:
                    c = "".join(x * 2 for x in c)
                if len(c) != 6 or c in ("000000", "FFFFFF") or c not in inv:
                    return m.group(0)
                return m.group(1) + ":" + "#" + _tgt(c)
            out = re.sub(r"(fill|stroke):\s*(#[0-9a-fA-F]{3,6})", _t, svg_txt)
            def _t2(m):
                c = m.group(2).strip("#").upper()
                if len(c) == 3:
                    c = "".join(x * 2 for x in c)
                if len(c) != 6 or c in ("000000", "FFFFFF") or c not in inv:
                    return m.group(0)
                return m.group(1) + "=\"#" + _tgt(c) + "\""
            out = re.sub(r"(fill|stroke)=\"(#[0-9a-fA-F]{3,6})\"", _t2, out)
            return out
        base = os.path.splitext(args.svg)[0]
        outs = []
        for k in range(n_sh):
            order = list(hexes)
            if k == 1:
                order = list(reversed(order))
            elif k > 1:
                order = hexes[k:] + hexes[:k]
            if k == 0:
                order = sorted(order, key=lambda h: oklch_from_hex(h)[0])
            p = base + (".recolored.svg" if k == 0 else ".recolor-%d.svg" % (k + 1))
            open(p, "w", encoding="utf-8").write(_rank_map(raw, order))
            outs.append((p, order))
        if n_sh > 1:
            grid = ["<!doctype html><meta charset='utf-8'><body style='background:#23272E;font-family:system-ui;padding:10px'>"]
            for p, order in outs:
                grid.append("<div style='color:#E8EEF6;padding:8px 6px 4px;font:600 12px monospace'>" +
                            " ".join("#" + h for h in order) + "</div>"
                            "<img src='" + os.path.basename(p) + "' style='max-width:96%;border-radius:8px;margin:0 6px 16px'>")
            grid.append("</body>")
            gp = base + ".recolor-grid.html"
            open(gp, "w", encoding="utf-8").write("".join(grid))
            outs.append((gp, []))
        print("SVG 槽位清单重着色: " + ", ".join(p for p, _ in outs) +
              " (清单=%d 色; 纯黑白保留; %d 排列)" % (len(inv), n_sh))
        if not inv:
            print("提示: SVG 未发现可映射颜色(fill/stroke 的 hex)")
    vcss = ""
    sections = []
    for vi, oh in enumerate(orders):
        label = ("Variant %d · %s" % (vi + 1, " ".join("#" + h for h in oh))) if n_var > 1 else ""
        css_v, sec = _viz_render(oh, (args.theme == "dark"), label)
        if not vcss:
            vcss = css_v
        sections.append(sec)
    html = ("<!doctype html><html><head><meta charset='utf-8'><title>Visualizer - " + args.name + "</title>"
            "<style>" + vcss + "</style></head><body><header>"
            "<h1>Visualizer · <b>" + args.name + "</b></h1></header>"
            + "".join(sections) + "</body></html>")
    out = args.out or "visualizer.html"
    open(out, "w", encoding="utf-8").write(html)
    R = _viz_roles(hexes, dark=(args.theme == "dark"))
    print("visualizer: " + out + " (10 场景; 角色 bg=#" + R["bg"] + " ink=#" + R["ink"] + " accent=#" + R["accent"] + ")")
    print("自审: 截图/emitImage 本文件, 按五镜判色在真实版式里是否成立")


def _write_visualize_html(hexes, name, dark, out):
    """单方向整页渲染(directions 用;variant 循环逻辑留在 cmd_visualize)。"""
    css, sec = _viz_render(list(hexes), dark, "")
    html = ("<!doctype html><html><head><meta charset='utf-8'><title>Visualizer - " + name + "</title>"
            "<style>" + css + "</style></head><body><header>"
            "<h1>Visualizer · <b>" + name + "</b></h1></header>"
            + sec + "</body></html>")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)


def _fill(tpl, m):
    for k, v in m.items():
        if len(v) == 6 and all(c in "0123456789abcdefABCDEF" for c in v):
            v = "#" + v
        tpl = tpl.replace(k, v)
    return tpl


def _export_prompt(hexes):
    """色板 → 图像生成提示词块: 角色化+占比+反 AI 味风格约束(封面/插画管线直接可用)。"""
    lines = []
    if len(hexes) >= 3:
        R = _viz_roles(hexes)
        share = {"bg": "large background fields (about 60%)",
                 "surface": "panels and cards (about 25%)",
                 "ink": "subject and text blocks",
                 "ink2": "secondary details and shadows",
                 "accent": "accents and highlights (about 10-15%)"}
        lines.append("PALETTE — use exactly these hex values, 60-30-10 dominance:")
        seen = []
        for k in ("bg", "surface", "ink", "ink2", "accent"):
            if R[k] not in seen:
                seen.append(R[k])
                _, C, H = oklch_from_hex(R[k])
                tone = "warm" if (H >= 310 or H < 70) else "cool"
                lines.append("- #" + R[k] + " (" + tone + ", lightness " +
                             format(oklch_from_hex(R[k])[0], ".2f") + ") — " + share[k])
        for h in hexes:
            if h not in seen:
                lines.append("- #" + h + " — supporting color, small doses only")
        warm = sum(1 for h in seen
                   if oklch_from_hex(h)[2] >= 310 or oklch_from_hex(h)[2] < 70) >= len(seen) / 2
        lines.append("STYLE: matte surfaces, soft directional light, film-like grain — " +
                     ("warm cozy mood." if warm else "cool calm mood."))
    else:
        lines.append("PALETTE — use exactly these hex values:")
        lines.extend("- #" + h for h in hexes)
    lines.append("AVOID: neon glow, gradients of any kind (flat color layering only), "
                 "saturated AI-look median "
                 "palette, pure black shadows.")
    return NL.join(lines)


def cmd_direct(args):
    """色彩导演(0.19):整页配色机械度量——温度旅程/饱和曲线/张力/主色戏剧(渲染实证规则集)。
    --zones "hex:share,..." 单页快判;--manifest lab_zones.json 批量;--bold 标品牌页(大域准入)。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import color_director
    except ImportError as e:
        print(f"缺 color_director: {e}", file=sys.stderr)
        sys.exit(2)
    if args.manifest:
        cases = json.load(open(args.manifest, encoding="utf-8"))
        n_pass = 0
        for c in cases:
            res = color_director.analyze(c["page"], [tuple(z) for z in c["zones"]],
                                         acts=[list(map(tuple, a)) for a in c["acts"]] if c.get("acts") else None,
                                         focal=tuple(c["focal"]) if c.get("focal") else None,
                                         bold=c.get("bold", False), last_act_loud=c.get("last_act_loud"),
                                         accent_share=c.get("accent_share"), palette=c.get("palette"),
                                         cap=c.get("cap"), only=c.get("only"))
            print(f"{res['page']} → {res['verdict']}")
            for f in res["findings"]:
                if f["verdict"] == "FAIL":
                    print(f"  [FAIL] {f['rule']}: {f['evidence']}")
            n_pass += res["verdict"] == "PASS"
        print(f"合计: {n_pass}/{len(cases)} PASS")
        sys.exit(0)
    if not args.zones:
        print("--zones 或 --manifest 必给其一", file=sys.stderr)
        sys.exit(2)
    zones = color_director._parse_zones(args.zones)
    res = color_director.analyze(args.page or "cli", zones, bold=args.bold)
    print(f"裁决: {res['verdict']}")
    for f in res["findings"]:
        mark = "PASS" if f["verdict"] == "PASS" else "FAIL"
        print(f"  [{mark}] {f['rule']}: {f['evidence']}")
        if f["verdict"] == "FAIL" and f.get("fix"):
            print(f"         ↳ {f['fix']}")
    sys.exit(0 if res["verdict"] == "PASS" else 1)


def cmd_report(args):
    """一键验收工件: 四道机械闸(对比度/色盲/AI-slop/评分)聚合成单一 PASS/FAIL JSON。
    退出码=裁决(0=PASS, 1=FAIL)。"""
    hexes = [h.upper() for h in palette_list(args.palette)]
    if len(hexes) < 3:
        print("至少 3 色", file=sys.stderr); sys.exit(2)
    engine = os.path.abspath(__file__)

    def _run(*a):
        r = subprocess.run([sys.executable, engine] + list(a), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=180)
        return r.returncode, (r.stdout or r.stderr or "").strip()

    gates = {}
    best = None
    for i, a in enumerate(hexes):
        for b in hexes[i + 1:]:
            r = contrast_ratio(a, b)
            if best is None or r > best[0]:
                best = (r, a, b)
    gates["contrast"] = {"pass": best[0] >= 4.5,
                         "best": format(best[0], ".2f") + ":1 (#" + best[1] + " on #" + best[2] + ")",
                         "threshold": "4.5:1",
                         "detail": ("判据=板内存在≥4.5:1可用文字对(非全对全查);实测最优对 #"
                                    + best[1] + " on #" + best[2] + " = " + format(best[0], ".2f") + ":1"
                                    + ("" if best[0] >= 4.5 else "——板内无可读文字对,换板或调墨"))}
    rc, out = _run("blind", "--palette", ",".join(hexes))
    # AE3: COLLISION RISK 不再 pass=True;纸面豁免=碰撞色为近中性(pale/card 层次设计意图,
    # 靠边框/阴影区分,色板层判"撞色"属语义错配);有色碰撞如实翻红
    _cb_pairs = re.findall(r"([0-9A-Fa-f]{6})\s*\(min-separation[^)]*\)\s*<-\s*COLLISION RISK", out)

    def _near_neutral(h):
        L, C, _ = oklch_from_hex(h.upper().lstrip("#"))
        return C < 0.10
    # 纸面豁免无条件适用:碰撞对为近中性(C<0.10)=pale/card 层次设计意图,
    # 全灰板同理(其假安心由 contrast/slop/score 三门兜住,总裁决不放松)
    _cb_hard = [h for h in _cb_pairs if not _near_neutral(h)]
    gates["color_blind"] = {"pass": rc == 0 and not _cb_hard, "detail": out[-160:]}
    rc, out = _run("slop", "--palette", ",".join(hexes))
    gates["ai_slop"] = {"pass": rc == 0, "detail": out[-160:]}
    rc, out = _run("score", "--palette", ",".join(hexes))
    # AE3: score 门不再忽略 detail 里的发现。分级裁决:[P0] 或总分 <15 翻红(P1 提醒+Good 分
    # 不翻——纸面对层次属设计意图);紫渐变类签名由 ai_slop 门专责,不在此重复计票
    _m = re.search(r"TOTAL\s+(\d+)/20", out)
    _total = int(_m.group(1)) if _m else 20
    _hard = re.search(r"\[P0\]", out) is not None
    gates["score"] = {"pass": rc == 0 and not _hard and _total >= 15, "detail": out[-160:]}
    if getattr(args, "zones", None):
        # 第五闸(0.19):主色戏剧——主色档位与占面 cap(渲染实证规则,--zones 给页面占比)
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import color_director as _cd
            zl = _cd._parse_zones(args.zones)
            share_map = dict(zl)
            acc = max(hexes, key=lambda h: _cd.oklch_from_hex(h)[1])
            accent_share = share_map.get(acc, max((sh for _, sh in zl), default=0.0))
            ok, ev = _cd.rule_drama(hexes, accent_share, bold=bool(getattr(args, "bold", False)))
            gates["drama"] = {"pass": bool(ok), "detail": ev}
        except Exception as e:
            gates["drama"] = {"pass": True, "detail": f"drama 闸跳过: {e}"}
    verdict = "PASS" if all(g["pass"] for g in gates.values()) else "FAIL"
    # 0.8.0 量化叙事:几闸过/拦下几项发现——检查的收益给数字,不只给结论
    n_pass = sum(1 for g in gates.values() if g["pass"])
    n_findings = 0 if verdict == "PASS" else sum(
        1 for g in gates.values() if not g["pass"]) + len(re.findall(r"\[P[0-3]\]", gates["score"]["detail"]))
    summary = {"gates_passed": f"{n_pass}/{len(gates)}", "issues_caught": n_findings}
    # 零模型信任闸:指纹绑定——裁决与输入摘要互锁,验收记录可对账防篡改
    fp = hashlib.sha256(("aesthete-report/v1|" + ",".join(hexes) + "|" + verdict)
                        .encode("utf-8")).hexdigest()
    print(json.dumps({"palette": hexes, "gates": gates, "verdict": verdict,
                      "summary": summary, "fingerprint": fp},
                     ensure_ascii=False, indent=2))
    sys.exit(0 if verdict == "PASS" else 1)


def palette_list(s):
    return [h for h in (x.strip() for x in s.replace("#", ",").split(",")) if h]


def _theme_hexes(name):
    """主题名 → hex 列表;不存在 exit 2(带可选清单)。tokens/scene/scaffold 同源。"""
    tpath = os.path.join(os.path.dirname(os.path.abspath(LIBRARY)), "themes.json")
    with open(tpath, encoding="utf-8") as f:
        td = json.load(f)
    ts = td["themes"] if isinstance(td, dict) else td
    rec = next((t for t in ts if t.get("name_en") == name or t["name"] == name), None)
    if rec is None:
        print(f"主题不存在: {name}——可选: " +
              ", ".join(t.get("name_en", t["name"]) for t in ts), file=sys.stderr)
        sys.exit(2)
    return [v.lstrip("#").upper() for v in rec["colors"].values()]


def cmd_harmony(args):
    L, C, H = oklch_from_hex(args.base)
    modes = {
        "monochromatic": [0], "analogous": [-30, 0, 30],
        "complementary": [0, 180], "split-complementary": [0, 150, 210],
        "triadic": [0, 120, 240], "tetradic": [0, 90, 180, 270],
        "square": [0, 90, 180, 270],
    }
    hues = [(H + d) % 360 for d in modes[args.mode]]
    dark = args.theme == "dark"
    # role scaffold: quiet bg, dark text, chromatic body from harmony hues
    bg_L, text_L = (0.97, 0.22) if not dark else (0.23, 0.95)
    surf_C = 0.012
    palette = [
        hex_from_oklch(bg_L, surf_C, H),                       # background
        hex_from_oklch((bg_L - 0.06) if not dark else (bg_L + 0.05), surf_C, (H + 20) % 360),  # surface
    ]
    for h in hues:
        c = gamut_fit(0.55 if not dark else 0.68, min(0.19, max(C, 0.11)), h)
        palette.append(hex_from_oklch(0.55 if not dark else 0.68, c, h))
    palette.append(hex_from_oklch(text_L, 0.008, H))          # text
    if args.count:
        palette = palette[:args.count]
    print(" ".join(palette))
    print("roles: bg surface primary... text (assign with `roles`)")
    print("contrast bg/text: %.2f:1 (%s)" % (
        (lambda r: r)(contrast_ratio(palette[0], palette[-1])),
        wcag_verdict(contrast_ratio(palette[0], palette[-1]))[0]))
    for f in slop_lint(palette):
        print("lint:", f)


def cmd_mutate(args):
    hexes = palette_list(args.palette)
    out = []
    for h in hexes:
        L, C, H = oklch_from_hex(h)
        L += args.lum / 100
        C = max(0.0, C + args.sat / 100)
        H = (H + args.hue) % 360
        C = gamut_fit(L, C, H)
        # temperature: rotate toward warm (+) or cool (-) without wrecking hue identity
        if args.temp:
            target = 60 if args.temp > 0 else 260
            delta = args.temp / 100 * 15
            dist = (target - H) % 360
            H = (H + delta * (1 if dist < 180 else -1)) % 360
        if args.shade:
            L += args.shade / 100 * 0.5
            C = gamut_fit(L, C, H)
        out.append(hex_from_oklch(clamp(L), C, H))
    print(" ".join(out))


def cmd_contrast(args):
    # AE5: 统一清洗入参——带 # 输入时 f"#{fg.upper()}" 曾拼出 ##XXX(复制即失效)
    args.fg = str(args.fg).strip().lstrip("#")
    args.bg = str(args.bg).strip().lstrip("#")
    if getattr(args, "method", "wcag") == "apca":
        lc = apca(args.fg, args.bg)
        print(f"APCA Lc={lc} ({apca_verdict(lc)})  #{args.fg.upper()} on #{args.bg.upper()}")
        print("指南: 正文>=75(理想90) / 大字>=60 / 粗大字>=45 / 非文字>=30 — WCAG 3 草案方向")
        return
    ratio = contrast_ratio(args.fg, args.bg)
    verdicts = wcag_verdict(ratio, args.large)
    best = readable_text(args.bg)
    print(f"#{args.fg.upper()} on #{args.bg.upper()} = {ratio:.2f}:1  {' '.join(verdicts)}")
    if ratio < (3.0 if args.large else 4.5):
        # suggest fix: nudge fg lightness away from bg
        L, C, H = oklch_from_hex(args.fg)
        bg_L = oklch_from_hex(args.bg)[0]
        step = 0.05 if bg_L > L else -0.05
        for _ in range(16):
            L += step
            c = gamut_fit(L, C, H)
            cand = hex_from_oklch(clamp(L), c, H)
            if contrast_ratio(cand, args.bg) >= (3.0 if args.large else 4.5):
                print(f"suggestion: #{cand} ({contrast_ratio(cand, args.bg):.2f}:1)")
                break
    print(f"auto text for bg: #{best}")


def cmd_roles(args):
    hexes = palette_list(args.palette)
    info = sorted(((oklch_from_hex(h), h) for h in hexes), reverse=True)
    light_theme = args.theme != "dark"
    bg = max(info, key=lambda t: t[0][0]) if light_theme else min(info, key=lambda t: t[0][0])
    text = min(info, key=lambda t: t[0][0]) if light_theme else max(info, key=lambda t: t[0][0])
    rest = [t for t in info if t[1] not in (bg[1], text[1])]
    accent = max(rest, key=lambda t: t[0][1]) if rest else bg
    primary = max([t for t in rest if t[1] != accent[1]],
                  key=lambda t: abs(t[0][0] - 0.55)) if len(rest) > 1 else (accent if accent is not bg else bg)
    surface = min([t for t in rest if t[1] not in (accent[1], primary[1])],
                  key=lambda t: abs(t[0][0] - bg[0][0]), default=None) if rest else None
    roles = {"bg": bg[1], "text": text[1], "accent": accent[1], "primary": primary[1]}
    if surface:
        roles["surface"] = surface[1]
    if args.semantic:
        # semantic states derived from the accent hue (角色,不是色块袋):
        # success/warning/error/info keep the accent's lightness & chroma character
        L, C, H = oklch_from_hex(accent[1])
        C = max(C, 0.10)
        for name, hue in (("success", 145), ("warning", 85), ("error", 25), ("info", 250)):
            roles[name] = hex_from_oklch(clamp(L), gamut_fit(L, C, hue), hue)
    checks = [
        ("text/bg", contrast_ratio(roles["text"], roles["bg"]), False),
        ("primary/bg", contrast_ratio(roles["primary"], roles["bg"]), True),
        ("accent/bg", contrast_ratio(roles["accent"], roles["bg"]), True),
    ]
    if args.css:
        print(":root {")
        for k, v in roles.items():
            print(f"  --color-{k}: #{v};")
        print("}")
    else:
        for k, v in roles.items():
            t = readable_text(v)
            print(f"{k:8s} #{v}  (text: #{t})")
    ok = True
    for name, r, large in checks:
        v = wcag_verdict(r, large)[0]
        if "FAIL" in v:
            ok = False
        print(f"check {name}: {r:.2f}:1 {v}")
    usage = ("60-30-10 mapping: %s dominates ~60%% (bg), %s+%s ~30%% (structure), "
             "%s ~10%% (accent)" % (roles["bg"], roles.get("surface", roles["primary"]),
                                    roles["primary"], roles["accent"]))
    print(usage)
    sys.exit(0 if ok else 1)


def cmd_ramp(args):
    """OKLCH lightness ramp from a base hue — chroma falls off near white/black
    (端点降饱和法则:不为数学均匀在极端明度硬保高 chroma)。"""
    L, C, H = oklch_from_hex(args.base)
    C = max(C, 0.08)
    out = []
    lo, hi = (0.25, 0.97) if args.direction != "dark" else (0.97, 0.25)
    for i in range(args.steps):
        t = i / max(1, args.steps - 1)
        L_i = lo + (hi - lo) * t
        # chroma falloff near the extremes
        c_scale = clamp(min((L_i - 0.02) / 0.30, (0.98 - L_i) / 0.30, 1.0))
        c = gamut_fit(L_i, C * c_scale, H)
        out.append(hex_from_oklch(L_i, c, H))
    print(" ".join(out))


def cmd_score(args):
    """Audit-style palette scorecard: deterministic checks only, 0-4 anchors,
    P0-P3 findings. Mechanical gate for step 4; taste stays with the model/user."""
    hexes = palette_list(args.palette)
    findings = []

    def dim(name, score, note):
        print(f"{name:12s} {'#'*score}{'.'*(4-score)} {score}/4  {note}")
        return score

    # 1 architecture: lightness span + quiet surface presence
    Ls = [oklch_from_hex(h)[0] for h in hexes]
    span = max(Ls) - min(Ls)
    a = 4 if span >= 0.45 else 3 if span >= 0.30 else 2 if span >= 0.20 else 1 if span >= 0.12 else 0
    dim("ARCHITECTURE", a, f"L span {span:.2f} (need >=0.25 for role architecture)")
    if span < 0.25:
        findings.append(("P1", f"flat lightness (span {span:.2f} < 0.25): no quiet surface for content"))

    # 2 readability: best text/bg pair + accent visibility
    best = max(((contrast_ratio(x, y), x, y) for i, x in enumerate(hexes) for y in hexes[i+1:]), default=(0, None, None))
    r, x, y = best
    b = 4 if r >= 7 else 3 if r >= 4.5 else 2 if r >= 3 else 1 if r >= 2 else 0
    dim("READABILITY", b, f"best pair {x}/{y} = {r:.2f}:1")
    if r < 4.5:
        findings.append(("P0" if r < 3 else "P1", f"no AA-readable text/bg pair (best {r:.2f}:1)"))

    # 3 CB safety: min pairwise separation under deuteranopia
    def lab_orig(h):
        return oklab_from_srgb(tuple(c / 255 for c in parse_hex(h)))
    def d_cb(h):
        rgbs = [c / 255 for c in parse_hex(h)]
        m = CB_MATRICES["deuteranopia"]
        o = tuple(clamp(m[i]*rgbs[0] + m[i+1]*rgbs[1] + m[i+2]*rgbs[2]) for i in (0, 3, 6))
        return oklab_from_srgb(o)
    pairs = [(i, j) for i in range(len(hexes)) for j in range(i+1, len(hexes))]
    cb = min(min(math.dist(lab_orig(hexes[i]), lab_orig(hexes[j])),
                 math.dist(d_cb(hexes[i]), d_cb(hexes[j]))) for i, j in pairs)
    c = 4 if cb >= 0.12 else 3 if cb >= 0.08 else 2 if cb >= 0.05 else 1 if cb >= 0.03 else 0
    dim("CB-SAFETY", c, f"min pair separation under deuteranopia {cb:.3f} (>=0.08 good)")
    if cb < 0.05:
        findings.append(("P1", "two colors collide under red-green blindness; rely on lightness or add labels"))

    # 4 saturation discipline
    Cs = [oklch_from_hex(h)[1] for h in hexes]
    mean_c = sum(Cs) / len(Cs)
    loud = sum(1 for c_, l_ in zip(Cs, Ls) if c_ > 0.16 and l_ > 0.45)
    d = 4 if loud == 0 and mean_c <= 0.14 else 3 if loud <= 1 else 2 if loud <= 2 else 1 if loud < len(hexes) else 0
    dim("SAT-DISCIPLINE", d, f"mean C {mean_c:.3f}, {loud}/{len(hexes)} loud colors (quiet surfaces needed)")
    if loud == len(hexes):
        findings.append(("P2", "every color is loud; add a quiet neutral surface"))

    # 5 uniqueness vs the median (anti-slop)
    slop_f = [f for f in slop_lint(hexes) if not f.startswith("CLEAN")]
    e = 4 if not slop_f else 2 if len(slop_f) == 1 else 0
    dim("UNIQUENESS", e, "; ".join(slop_f) if slop_f else "no median-trap signature")
    for f in slop_f:
        findings.append(("P1" if "MEDIAN-TRAP" in f else "P2", f))

    total = a + b + c + d + e
    band = ("Excellent" if total >= 18 else "Good" if total >= 14 else
            "Acceptable" if total >= 10 else "Poor" if total >= 6 else "Critical")
    print("-" * 56)
    print(f"TOTAL {total}/20  {band}")
    # 档案机制:偏好违例=机械发现(不是建议)
    prof = load_profile()
    reg = prof.get("registers", {}).get(prof.get("default_register", ""), {})
    dark_share = sum(1 for l_ in Ls if l_ < 0.35) / len(Ls) if Ls else 0
    if reg.get("theme") == "light" and dark_share >= 0.4:
        findings.append(("P1", f"PROFILE: 档案默认语域要求浅底,当前 {int(dark_share*100)}% 色为深底(dark_penalty={prof.get('theme_bias', {}).get('dark_penalty', 0)})——除非 brief 明示深色,否则换板"))
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    for sev, msg in sorted(findings, key=lambda t: order[t[0]]):
        print(f"[{sev}] {msg}")
    if not findings:
        print("[OK] no mechanical findings; taste judgment happens in context (card step)")
    sys.exit(1 if any(s == "P0" for s, _ in findings) or total < 10 else 0)


def cmd_showcase(args):
    """Contact sheet of library candidates for user selection (样张点名)."""
    with open(LIBRARY, encoding="utf-8") as f:
        lib = json.load(f)
    pals = lib["palettes"]
    if args.style:
        want = set(args.style.split(","))
        pals = [p for p in pals if want & set(p["computed_styles"])]
    if args.min_likes:
        pals = [p for p in pals if p["likes"] >= args.min_likes]
    pals = pals[: args.limit]
    cards = []
    for p in pals:
        stars = "*" * p["tier"] or "new"
        flags = " ".join(p["flags"])
        sw = "".join(f'<div style="background:#{h};flex:1;padding:26px 0 6px;text-align:center">'
                     f'<span style="font:600 11px monospace;color:#{readable_text(h)};opacity:.75">{h}</span></div>'
                     for h in p["hexes"])
        cards.append(f"""
      <div style="border:1px solid #e5e5e5;border-radius:10px;overflow:hidden">
        <div style="display:flex">{sw}</div>
        <div style="padding:8px 12px;font:500 13px system-ui;display:flex;justify-content:space-between;gap:8px">
          <span>{p['name']} <span style="color:#999">{stars} {p['likes']:,}</span></span>
          <span style="color:#b33">{flags}</span>
        </div>
      </div>""")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Palette showcase</title></head>
<body style="margin:0;background:#fafafa;font-family:system-ui">
  <div style="max-width:960px;margin:0 auto;padding:28px">
    <h1 style="font:700 20px system-ui">Palette showcase — pick one by name</h1>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">{''.join(cards)}</div>
  </div>
</body></html>"""
    out = args.out or "palette_showcase.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"showcase written: {out} ({len(pals)} palettes)")
    print("present to user for explicit selection, then build with the chosen palette")


def cmd_blind(args):
    hexes = palette_list(args.palette)
    kinds = ["protanopia", "deuteranopia", "tritanopia"] if not args.kind else [args.kind]
    row = " ".join(h.upper() for h in hexes)
    print("original : " + row)
    for k in kinds:
        sim = [simulate_cb(h, k) for h in hexes]
        # distinctness loss: min pairwise delta-E (oklab) original vs simulated
        def mindiff(cols):
            labs = [oklab_from_srgb(tuple(c / 255 for c in parse_hex(x))) for x in cols]
            m = 9e9
            for i in range(len(labs)):
                for j in range(i + 1, len(labs)):
                    d = math.dist(labs[i], labs[j])
                    m = min(m, d)
            return m
        loss = mindiff(hexes) - mindiff(sim)
        warn = "  <- COLLISION RISK" if mindiff(sim) < 0.07 else ""
        print(f"{k:12s}: " + " ".join(s.upper() for s in sim) + f"  (min-separation drop {loss:+.3f}){warn}")


def cmd_slop(args):
    findings = slop_lint(palette_list(args.palette))
    for f in findings:
        print(f)
    sys.exit(0 if all(f.startswith("CLEAN") for f in findings) else 1)


def cmd_extract(args):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow required: pip install pillow", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.image):
        print(f"文件不存在: {args.image}", file=sys.stderr)
        sys.exit(2)
    try:
        img = Image.open(args.image).convert("RGB")
    except Exception as e:
        print(f"无法打开图像({e}): 仅支持常见位图格式", file=sys.stderr)
        sys.exit(2)
    img.thumbnail((200, 200))
    q = img.quantize(colors=args.n, method=Image.Quantize.MEDIANCUT).convert("RGB")
    counts = sorted(q.getcolors(img.width * img.height) or [], reverse=True)
    total = img.width * img.height
    picked = []
    for cnt, rgb in counts:
        h = to_hex(tuple(c / 255 for c in rgb))
        L, C, _ = oklch_from_hex(h)
        if C < 0.008 and picked:  # collapse near-gray duplicates, keep one
            continue
        picked.append((h, cnt / total, L, C))
        if len(picked) >= args.n:
            break
    for h, share, L, C in picked:
        print(f"#{h}  {share*100:5.1f}%  L={L:.2f} C={C:.3f}  text:#{readable_text(h)}")


def cmd_search(args):
    with open(LIBRARY, encoding="utf-8") as f:
        lib = json.load(f)
    pals = lib["palettes"]
    if args.style:
        want = set(args.style.split(","))
        pals = [p for p in pals if want & set(p["computed_styles"])]
    if args.min_likes:
        pals = [p for p in pals if p["likes"] >= args.min_likes]
    if args.no_flags:
        pals = [p for p in pals if not p["flags"]]
    pals = pals[: args.limit]
    for p in pals:
        stars = "*" * p["tier"] if p["tier"] else "new"
        flags = " !" + "!".join(p["flags"]) if p["flags"] else ""
        print(f"{stars:4s}{p['likes']:>7,}  {p['name']}  [{' '.join(p['computed_styles'])}]{flags}")
        print(f"           {' '.join(p['hexes'])}")


def cmd_house(args):
    """已验收设计入库(origin=house):用户的接受裁决=最强味信号,直接进库参与 match。"""
    hexes = [h.upper() for h in palette_list(args.hexes)]
    assert 3 <= len(hexes) <= 10, "3-10 色"
    with open(LIBRARY, encoding="utf-8") as f:
        lib = json.load(f)
    key = "#".join(sorted(hexes))
    if any("#".join(sorted(p["hexes"])) == key for p in lib["palettes"]):
        print("已存在同色组合,跳过")
        return
    hues, lights, sats = [], [], []
    for h in hexes:
        hh, ll, ss = hsl(h)
        hues.append(hh); lights.append(ll); sats.append(ss)
    mean_l = sum(lights) / len(lights)
    mean_s = sum(sats) / len(sats)
    tags = ["warm" if sum(1 for x in hues if x >= 310 or x < 70) >= len(hues) / 2 else "cool"]
    tags.append("dark" if mean_l < 0.35 else "light" if mean_l > 0.65 else "mid")
    if mean_s < 0.40 and mean_l > 0.60: tags.append("pastel")
    if mean_s > 0.55: tags.append("vivid")
    best = max(contrast_ratio(a, b) for i, a in enumerate(hexes) for b in hexes[i+1:])
    lib["palettes"].insert(0, {
        "name": args.name, "hexes": hexes, "text_hint": [], "likes": 0, "tier": 3,
        "origin": "house", "computed_styles": sorted(set(tags)),
        "occurrences": 1, "flags": [],
        "metrics": {"lightness_span": round(max(lights) - min(lights), 3),
                    "max_contrast": round(best, 2), "cb_min_separation": None},
        "sources": [f"house:{args.from_proj or 'user_accepted'}"],
    })
    lib["_meta"]["counts"]["kept"] = len(lib["palettes"])
    json.dump(lib, open(LIBRARY, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    prof = load_profile()
    prof.setdefault("loved_palette_ids", [])
    if args.name not in prof["loved_palette_ids"]:
        prof["loved_palette_ids"].append(args.name)
        json.dump(prof, open(PROFILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("提醒: profile.json(用户裁决档案)有变更——若在 git 管理的安装内,记得提交,避免偏好只有工作区一份(AE7)")
    print(f"house 入库: {args.name} [{' '.join(sorted(set(tags)))}] (loved+1, match 自动加权)")


def cmd_selftest(args):
    """机器金标:WCAG 边界/OKLCH 往返/slop 签名/对比函数。非零退出 = 引擎不可信。"""
    ok, fail = [], []
    def check(name, cond):
        (ok if cond else fail).append(name)
        print(("PASS  " if cond else "FAIL  ") + name)
    check("wcag边界-过(#767676/FFF=4.54)", 4.53 < contrast_ratio("767676", "FFFFFF") < 4.55)
    check("wcag边界-不过(#777777/FFF=4.48)", 4.47 < contrast_ratio("777777", "FFFFFF") < 4.49)
    check("wcag阈值方向", contrast_ratio("767676", "FFFFFF") > contrast_ratio("777777", "FFFFFF"))
    h = "2A9D8F"
    L1, C1, H1 = oklch_from_hex(h)
    check("oklch往返(L误差<0.003)", abs(oklch_from_hex(hex_from_oklch(L1, C1, H1))[0] - L1) < 0.003)
    check("oklch往返(色相误差<0.5deg)", abs((oklch_from_hex(hex_from_oklch(L1, C1, H1))[2] - H1 + 180) % 360 - 180) < 0.5)
    check("slop签名-tailwind", any("MEDIAN-TRAP" in f for f in slop_lint(["3B82F6", "8B5CF6", "EC4899", "6366F1", "A855F7"])))
    check("slop签名-干净板", all(f.startswith("CLEAN") for f in slop_lint(["264653", "2A9D8F", "E9C46A", "F4A261", "E76F51"])))
    check("自动文字-深底选白", readable_text("000814") == "FFFFFF")
    check("自动文字-浅底选黑", readable_text("FEFAE0") == "000000")
    check("色盲矩阵-有输出", len(simulate_cb("FF0000", "deuteranopia")) == 6)
    print(f"\n{len(ok)} PASS / {len(fail)} FAIL")
    sys.exit(0 if not fail else 1)


THEMES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "palettes", "themes.json")

def load_themes():
    try:
        with open(THEMES_FILE, encoding="utf-8") as f:
            return json.load(f)["themes"]
    except Exception:
        return []


def cmd_themes(args):
    """列出命名主题包(配色+字体+语气+适用域)。"""
    themes = load_themes()
    if args.json:
        print(json.dumps(themes, ensure_ascii=False, indent=1))
        return
    for t in themes:
        print(f"{t['name']} ({t['name_en']})  —  {t['use_when']}")
        print(f"  色: {' '.join(t['colors'].values())}")
        print(f"  语气: {t['voice']}")
    print(f"\
共 {len(themes)} 包;theme apply <名> --format css 输出完整 token")


def cmd_theme(args):
    themes = load_themes()
    t = next((x for x in themes if x["name"] == args.name or x["name_en"] == args.name), None)
    if not t:
        print(f"主题不存在: {args.name};可用: " + ", ".join(x["name"] for x in themes))
        sys.exit(2)
    if args.format == "json":
        print(json.dumps(t, ensure_ascii=False, indent=1))
        return
    c = t["colors"]
    print(f"/* {t['name']} — {t['use_when']} */")
    print(":root {")
    for k, v in c.items():
        print(f"  --c-{k.replace('_','-')}: {v};")
    for k, v in t["fonts"].items():
        print(f"  --font-{k}: {v};")
    print("  --radius: 6px;")
    print("}")
    print(f"/* 语气: {t['voice']} */")


def cmd_matrix(args):
    """全对对比度矩阵 + 最优文字/背景配对推荐。"""
    hexes = [h.upper() for h in palette_list(args.palette)]
    n = len(hexes)
    print("| | " + " | ".join(f"#{h}" for h in hexes) + " |")
    print("|---|" + "---|" * n)
    best = []
    for i, a in enumerate(hexes):
        row = [f"#{a}"]
        for j, b in enumerate(hexes):
            if i == j:
                row.append("—")
                continue
            r = contrast_ratio(a, b)
            row.append(f"{r:.2f}")
            if i < j:
                best.append((r, a, b))
        print("| " + " | ".join(row) + " |")
    best.sort(reverse=True)
    pairs = ", ".join(f"#{a}/#{b}={r:.2f}:1" for r, a, b in best[:3])
    print("")
    print(f"最优文字对: {pairs}")
    print(f"过 AA 正文对(>=4.5): {sum(1 for r,_,_ in best if r >= 4.5)} 组;过 AAA 大字(>=3): {sum(1 for r,_,_ in best if r >= 3)} 组")
    if args.recommend:
        r, a, b = best[0]
        print(f"推荐: 文字 #{a} 于底 #{b}({r:.2f}:1)")


def cmd_semantic(args):
    """色盲安全分类色:明度阶梯交错+色相均布,内置去盲分离度验证(图表/数据可视化)。"""
    n = max(3, min(12, args.count))
    base_hue = oklch_from_hex(args.base)[2] if args.base else args.hue
    out, worst = [], 0
    for tries in range(60):
        cols = []
        for i in range(n):
            hue = (base_hue + i * (360 / max(3, n)) + (15 if i % 2 else 0)) % 360
            L = 0.82 if i % 2 == 0 else 0.52
            if i == n - 1 and n % 2:
                L = 0.30
            C = 0.13 if i % 2 == 0 else 0.15
            c = gamut_fit(L, C, hue)
            cols.append(hex_from_oklch(L, c, hue))
        def lab(h):
            return oklab_from_srgb(tuple(cc / 255 for cc in parse_hex(h)))
        def labd(h):
            m = CB_MATRICES["deuteranopia"]
            rgbs = [cc / 255 for cc in parse_hex(h)]
            o = tuple(clamp(m[i]*rgbs[0] + m[i+1]*rgbs[1] + m[i+2]*rgbs[2]) for i in (0, 3, 6))
            return oklab_from_srgb(o)
        labs = [lab(h) for h in cols]
        labd_ = [labd(h) for h in cols]
        worst = 9e9
        for i in range(n):
            for j in range(i+1, n):
                worst = min(worst, math.dist(labs[i], labs[j]), math.dist(labd_[i], labd_[j]))
        if worst >= 0.08:
            out = cols
            break
        base_hue = (base_hue + 7) % 360
    if not out:
        print("无法在 60 次内找到色盲安全组合——减少 --count 或放宽", file=sys.stderr)
        sys.exit(1)
    print(" ".join(out))
    for h in out:
        L, C, H = oklch_from_hex(h)
        print(f"  #{h}  L={L:.2f} C={C:.3f} H={H:.0f}  文字:#{readable_text(h)}")
    print(f"色盲安全: 最小分离度 {worst:.3f}(>=0.08)")


def cmd_critique(args):
    """五镜报告生成器:机械发现预填,guided 表单待补 taste 裁决,附 finding ledger。"""
    lines = ["# 五镜自审报告(机械部分预填)", ""]
    pal = palette_list(args.palette) if args.palette else []
    here = os.path.abspath(__file__)
    if pal:
        sc = subprocess.run([sys.executable, here, "score", "--palette", ",".join(pal)],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        lines += ["## 镜3 色彩(机械)", "", "```", sc.stdout or "", "```", ""]
        sl = subprocess.run([sys.executable, here, "slop", "--palette", ",".join(pal)],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        lines += ["slop: " + (sl.stdout or "").strip(), ""]
    if args.evidence and os.path.exists(args.evidence):
        ev = json.load(open(args.evidence, encoding="utf-8"))
        lines += ["## 镜4 渲染实测(机械)", "",
                  f"- 主题: {ev.get('theme')} / bodyBg {ev.get('bodyBg')}",
                  f"- 实测最小字号: {ev.get('minFont')}px(样本: {ev.get('fontSample','')})",
                  "- 最差对比对: " + ", ".join(f"#{p['fg']}/#{p['bg']}={p['ratio']}" for p in ev.get("worstPairs", [])[:4]),
                  "- 色彩面积占比: " + ", ".join(f"#{c['hex']} {c['areaRatio']*100:.0f}%" for c in ev.get("colors", [])[:6]), ""]
    lines += ["## 镜0 意图(待裁决)", "- 给谁看/场景/3秒带走: ____", "- 语域匹配: ____", "",
              "## 镜1 构成(待裁决)", "- 视线落点顺序: ____", "- 签名元素唯一: ____", "",
              "## 镜2 信息(待裁决)", "- 数据是否成对出现: ____", "- 删减候选: ____", "",
              "## 镜4 文字(待裁决)", "- 字体声音匹配: ____", "",
              "## 减法 pass(只删不加)", "- 删了什么: ____", "- 保留红线(对象/依据/状态/主动作)核对: ____", "",
              "## finding ledger", "",
              "```",
              "ledger: <问题1> answered | <问题2> partially(剩X) | <问题3> unresolved(原因)",
              "预算: 已用 N 轮 | 剩余: 最多 1 轮修复",
              "```"]
    out = args.out or "critique_report.md"
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"报告: {out}(机械发现已预填;taste 裁决按镜填空)")


def cmd_doctor(args):
    """环境体检:部署健康一键诊断。"""
    ok, bad = [], []
    def check(name, cond, detail=""):
        (ok if cond else bad).append(name)
        print(("PASS  " if cond else "FAIL  ") + name + (f"  {detail}" if detail else ""))
    check("python>=3.8", sys.version_info >= (3, 8))
    try:
        import PIL
        check("Pillow(extract 可用)", True)
    except ImportError:
        check("Pillow(extract 可用)", False, "pip install pillow")
    try:
        lib = json.load(open(LIBRARY, encoding="utf-8"))
        check(f"调色板库({lib['_meta']['counts']['kept']} 板)", lib["_meta"]["counts"]["kept"] >= 50)
    except Exception as e:
        check("调色板库", False, str(e)[:60])
    th = load_themes()
    check(f"主题包({len(th)} 个)", len(th) >= 5)
    pr = load_profile()
    check("profile.json(偏好档案)", "registers" in pr)
    sdir = os.path.dirname(THEMES_FILE)
    for f in ("lint_page.py", "make_variants.py", "render_probe.js", "build_library.py"):
        check(f"工具 {f}", os.path.exists(os.path.join(sdir, "..", "scripts", f)))
    st = subprocess.run([sys.executable, os.path.abspath(__file__), "selftest"],
                        capture_output=True, text=True)
    check("引擎 selftest", st.returncode == 0)
    print("")
    print(f"{len(ok)} PASS / {len(bad)} FAIL")
    sys.exit(0 if not bad else 1)


BRIEF_KEYWORDS = {
    # 词 → 语域。机械映射,不靠临场发挥;新领域=加词条,不是加散文。
    "medical_teaching": ["教学", "临床", "查房", "医学", "医疗", "指南", "解读", "儿科", "病例", "文献", "患教",
                         # 0.20.0 英文词条
                         "teaching", "clinical", "medical", "guideline", "journal club", "grand rounds",
                         "case report", "slide deck", "journal"],
    "pediatric_cover": ["封面", "儿童", "母婴",
                        # 0.20.0 英文词条
                        "children", "kids", "child", "vaccine", "poster", "cover", "baby", "infant"],
    # 前端语域(0.7.0):中文审美口语词 → 板族。"鲜艳"只指向有品位的鲜活——
    # 无品位的刺眼板带 gate 旗/踩禁词族,排序里 -4 自然沉底,不是这里豁免。
    "frontend_soft": ["素雅", "清新", "柔和", "温柔", "淡雅", "耐看", "干净", "极简", "简洁", "轻盈",
                      "奶油", "莫兰迪", "奶油风", "治愈", "轻盈感", "温柔风",
                      # 0.12.0 扩容
                      "素净", "温润", "细腻", "柔美", "淡色", "舒适", "棉麻", "日式", "侘寂", "奶咖",
                      "软糯", "松弛",
                      # 0.20.0 英文词条
                      "soft", "calm", "pastel", "minimal", "gentle", "clean"],
    "frontend_deep": ["大气", "稳重", "高级", "高级感", "质感", "商务", "沉稳", "典雅", "正式", "深沉",
                      "轻奢", "厚重", "硬朗", "工业风", "办公",
                      # 0.12.0 扩容
                      "老钱风", "深邃", "暗色调", "墨色", "咖啡", "皮革", "胡桃木", "绅士", "压得住",
                      # 0.20.0 英文词条
                      "dark", "premium", "luxury", "elegant", "serious", "moody",
                      "杂志", "幻灯片", "俱乐部"],
    "frontend_bold": ["鲜艳", "活力", "年轻", "大胆", "撞色", "吸睛", "潮流", "醒目",
                      "明快", "清爽", "活泼", "元气", "有劲",
                      # 0.12.0 扩容
                      "多巴胺", "节庆", "欢快", "张扬", "热烈", "能量感"],
    "frontend_tech": ["科技", "科技感", "现代", "未来", "理性", "开发者", "程序员", "数据",
                      "极客", "赛博", "科幻", "智能",
                      # 0.12.0 扩容
                      "赛博朋克", "像素", "终端", "代码", "太空", "宇宙", "机甲", "霓虹",
                      # 0.20.0 英文词条(AE2):SKILL.md 示例即英文 brief,表必须双语
                      "fintech", "dashboard", "saas", "developer", "terminal", "tech",
                      "engineering", "tool", "devtool", "api"],
    # 东方语域(0.12.0):国风/传统色审美 → 暖陶/深墨/青绿系板
    "frontend_heritage": ["国风", "国潮", "水墨", "青绿", "敦煌", "宋韵", "禅意", "茶",
                          "古朴", "陶土", "宣纸", "东方", "汉风", "唐风", "古风", "年画",
                          "瓷器", "漆器"],
}
REGISTER_TAGS = {
    "medical_teaching": ["light", "mid", "warm", "cool", "pastel"],
    "pediatric_cover": ["warm", "vivid", "mid", "pastel"],
    "frontend_soft": ["light", "pastel", "mid", "cool"],
    "frontend_deep": ["dark", "mid", "cool", "monochromatic"],
    "frontend_bold": ["vivid", "warm", "multihue", "mid"],
    "frontend_tech": ["cool", "monochromatic", "mid", "light"],
    "frontend_heritage": ["warm", "mid", "dark", "pastel"],
}


def _load_lib():
    with open(LIBRARY, encoding="utf-8") as f:
        return json.load(f)


def _ranked_for_register(pals, reg, prof):
    """语域 → 库内排序(共享于 match/directions;标签命中+loved 加权+暗底惩罚+禁词族沉底)。"""
    want_tags = set(REGISTER_TAGS.get(reg, []))
    pen = prof.get("theme_bias", {}).get("dark_penalty", 0)
    banned = set(prof.get("banned_hex_families", {}).get("tailwind_defaults", []))
    loved = prof.get("loved_palette_ids", [])

    def rank(p):
        tag_hits = len(want_tags & set(p["computed_styles"]))
        dark = 1 if ({'dark', 'deep'} & set(p["computed_styles"])) else 0
        slop = 1 if set(p["hexes"]) & banned else 0
        return (tag_hits + (2 if p["name"] in loved else 0) - dark * pen - slop * 4,
                p["tier"], p["likes"])

    return sorted(pals, key=rank, reverse=True)


def _brief_registers(brief):
    """brief → 命中语域列表(按命中数降序;无命中=空表,由调用方决定回退)。"""
    hits = {r: sum(1 for k in kws if k in brief) for r, kws in BRIEF_KEYWORDS.items()}
    return [r for r, n in sorted(hits.items(), key=lambda kv: -kv[1]) if n > 0]


def cmd_match(args):
    """brief → 语域 → 库内排序。机制:关键词映射 + 档案惩罚;候选 ≥2 才许往下走。"""
    prof = load_profile()
    pals = _load_lib()["palettes"]
    reg = args.register
    if not reg:
        regs = _brief_registers(args.brief)
        reg = regs[0] if regs else prof.get("default_register", "medical_teaching")
    pen = prof.get("theme_bias", {}).get("dark_penalty", 0)
    pals = _ranked_for_register(pals, reg, prof)
    if args.no_flags:
        pals = [p for p in pals if not p["flags"]]
    want_tags = set(REGISTER_TAGS.get(reg, []))
    loved = prof.get("loved_palette_ids", [])
    banned = set(prof.get("banned_hex_families", {}).get("tailwind_defaults", []))

    def _score(p):
        # 与 _ranked_for_register 的排序主键同源(单一事实源):显示什么就按什么排
        hits = len(want_tags & set(p["computed_styles"]))
        dark = 1 if ({'dark', 'deep'} & set(p["computed_styles"])) else 0
        slop = 1 if set(p["hexes"]) & banned else 0
        return hits + (2 if p["name"] in loved else 0) - dark * pen - slop * 4

    print(f"register={reg}  theme_penalty_dark={pen}  candidates={len(pals)}")
    print("排序: score=语域标签命中+loved-暗底惩罚-禁词族(主键,降序), 次键 tier/likes; 首列即 score")
    try:
        _tp = os.path.join(os.path.dirname(os.path.abspath(LIBRARY)), "themes.json")
        _td = json.load(open(_tp, encoding="utf-8")) if os.path.exists(_tp) else {}
        for _rr in (_td.get("register_recipes") or {}).values():
            if _rr.get("register") == reg:
                print(f"配方: {_rr.get('name')}——{_rr.get('strategy')}")
    except Exception:
        pass
    for p in pals[: args.limit]:
        stars = "*" * p["tier"] if p["tier"] else "new"
        fl = " !" + "!".join(p["flags"]) if p["flags"] else ""
        print(f"{stars:4s}{_score(p):>4d} {p['likes']:>7,}  {p['name']}  [{' '.join(p['computed_styles'])}]{fl}")
        print(f"           {' '.join(p['hexes'])}")
    print("纪律:取 ≥2 候选走 card/showcase 对比后定;被否决的裁决写回 profile.json(机制,不是记忆)。")


def cmd_directions(args):
    """跨语域方向对比:不同语域族各取头牌,整页渲染并排 + 元数据栏 + 选择回传句。
    差异铁律:方向间色板必须不同、标签差 ≥2——同板换排列不算方向。"""
    prof = load_profile()
    pals = _load_lib()["palettes"]
    regs = [r.strip() for r in args.registers.split(",")] if args.registers else _brief_registers(args.brief)
    if args.registers:
        bad = [r for r in regs if r not in BRIEF_KEYWORDS]
        if bad:
            print(f"未知语域: {','.join(bad)}——可选: {','.join(BRIEF_KEYWORDS)}", file=sys.stderr)
            sys.exit(2)
    if not regs:
        regs = [prof.get("default_register", "medical_teaching")]
    n = max(2, min(args.n, 4))
    if len(regs) < n:
        for r in ("frontend_soft", "frontend_deep", "frontend_bold", "frontend_tech",
                  "medical_teaching", "pediatric_cover"):
            if r not in regs:
                regs.append(r)
            if len(regs) >= n:
                break
    regs = regs[:n]
    dirs = []
    for reg in regs:
        ranked = _ranked_for_register([p for p in pals if not p["flags"]], reg, prof) or \
                 _ranked_for_register(pals, reg, prof)
        if not ranked:
            continue
        pick = ranked[0]
        for p in ranked:  # 差异铁律:与已选方向同板或标签差 <2 的跳到下一块
            if any(p["hexes"] == d["hexes"] or
                   len(set(p["computed_styles"]) ^ set(d["styles"])) < 2 for d in dirs):
                continue
            pick = p
            break
        dirs.append({"register": reg, "name": pick["name"], "hexes": pick["hexes"],
                     "styles": pick["computed_styles"]})
    if len(dirs) < 2:
        print("方向不足 2 个——语域词表太窄或库太浅,先加词条/加板", file=sys.stderr)
        sys.exit(1)
    outdir = args.out_dir or "."
    os.makedirs(outdir, exist_ok=True)
    cells = []
    letters = "ABCDEFGH"
    for i, d in enumerate(dirs):
        dark = "dark" in d["styles"]
        fname = os.path.join(outdir, f"direction_{letters[i]}.html")
        _write_visualize_html(d["hexes"], f"{letters[i]} · {d['name']}", dark, fname)
        best = max((contrast_ratio(a, b) for j, a in enumerate(d["hexes"])
                    for b in d["hexes"][j + 1:]), default=1)
        echo = (f"就用方向 {letters[i]}「{d['name']}」:色板 {','.join('#' + h for h in d['hexes'])}。"
                f"按 60-30-10 出页面,再过 report 四道检查。")
        echo_js = echo.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;")
        chips = "".join(f"<span class='hx' style='background:#{h}'></span>" for h in d["hexes"])
        cells.append(f"""
  <div class="cell">
    <div class="cap"><b>方向 {letters[i]} · {d['name']}</b>
      <span>{d['register']} · [{' '.join(d['styles'])}] · 最优对比 {best:.2f}:1</span></div>
    <div class="meta">{chips}<span class="hexlist">{' '.join('#' + h for h in d['hexes'])}</span></div>
    <iframe src="{os.path.basename(fname)}" loading="lazy"></iframe>
    <div class="pick"><button onclick="pick(this)" data-say="{echo_js}">选它 — 复制回传句</button></div>
  </div>""")
    html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<title>方向对比 — pick one</title><style>
  body{{margin:0;background:#20242B;font-family:system-ui;color:#E8EEF6}}
  header{{padding:18px 26px;font-size:15px;letter-spacing:.08em;
         border-bottom:1px solid rgba(255,255,255,.12)}}
  header b{{color:#F2CC8F}}
  .grid{{display:grid;grid-template-columns:repeat({min(len(cells), 2)},1fr);gap:14px;padding:14px}}
  .cell{{border:1px solid rgba(255,255,255,.14);border-radius:8px;overflow:hidden}}
  .cap{{display:flex;justify-content:space-between;gap:8px;padding:9px 14px;font-size:13px;
       background:rgba(255,255,255,.06)}}
  .cap span{{opacity:.55;font-family:monospace;font-size:11px;text-align:right}}
  .meta{{display:flex;align-items:center;gap:4px;padding:7px 14px;border-bottom:1px solid rgba(255,255,255,.08)}}
  .hx{{width:22px;height:22px;border-radius:5px;display:inline-block;border:1px solid rgba(255,255,255,.25)}}
  .hexlist{{margin-left:auto;font:11px monospace;opacity:.6}}
  iframe{{width:100%;height:72vh;border:0;display:block;background:#fff}}
  .pick{{padding:8px 14px;background:rgba(255,255,255,.06)}}
  button{{background:#F2CC8F;color:#20242B;border:0;border-radius:6px;padding:6px 14px;
         font:600 12px system-ui;cursor:pointer}}
  #say{{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);max-width:80vw;
       background:#F2CC8F;color:#20242B;padding:10px 16px;border-radius:8px;font:13px system-ui;
       display:none;white-space:pre-wrap}}
</style></head><body>
<header>方向对比 —— 语域不同才是方向不同;点「选它」把回传句发给智能体,<b>不要替用户决定</b></header>
<div class="grid">{''.join(cells)}
</div><div id="say"></div>
<script>
function pick(btn){{
  var s = btn.getAttribute('data-say');
  var box = document.getElementById('say');
  box.textContent = s; box.style.display = 'block';
  if (navigator.clipboard) {{ navigator.clipboard.writeText(s).catch(function(){{}}); }}
  clearTimeout(box._t); box._t = setTimeout(function(){{ box.style.display = 'none'; }}, 6000);
}}
</script></body></html>"""
    cpath = os.path.join(outdir, "directions.html")
    with open(cpath, "w", encoding="utf-8") as f:
        f.write(html)
    for d in dirs:
        print(f"  方向 {d['register']}: {d['name']}  [{' '.join(d['hexes'])}]")
    print(f"方向对比页: {cpath}({len(dirs)} 个跨语域方向,整页见 direction_{letters[0]}..{letters[len(dirs)-1]}.html)")
    print("纪律:把对比页给用户点名;用户点名后,把回传句原样作为下一步指令。")


def cmd_check_image(args):
    """一键图像验收(0.8.0):封面/截图 → 取色 → 四道机械检查,一条命令。
    输出组合 JSON(image 摘要+palette+report);退出码=裁决。"""
    if not os.path.exists(args.image):
        print(f"文件不存在: {args.image}", file=sys.stderr)
        sys.exit(2)
    img_fp = hashlib.sha256(open(args.image, "rb").read()).hexdigest()
    engine = os.path.abspath(__file__)

    def _run(*a):
        r = subprocess.run([sys.executable, engine] + list(a), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=180)
        return r.returncode, (r.stdout or r.stderr or "").strip()

    _, ex_out = _run("extract", args.image, "--n", str(args.n))
    hexes = re.findall(r"^#([0-9A-Fa-f]{6})", ex_out, re.M)
    if len(hexes) < 3:
        print(f"取色不足 3 色(需 Pillow;got {len(hexes)})", file=sys.stderr)
        sys.exit(2)
    rc, rep_out = _run("report", "--palette", ",".join(hexes))
    try:
        report = json.loads(rep_out)
    except Exception:
        report = {"error": rep_out[-300:]}
    out = {"image": os.path.abspath(args.image), "image_sha256": img_fp,
           "palette": [h.upper() for h in hexes], "report": report,
           "verdict": report.get("verdict", "UNKNOWN")}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["verdict"] == "PASS" else 1)


def cmd_scene(args):
    """showcase 级单场景(0.9):把场景手艺开放为引擎能力——设备框/证据徽章/真实内容密度。
    AI 默认紫守门:大底角色落紫 hue 域即拒绝(--force 越过留痕)。产出可作实际页面起点。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import scene_kit
    except ImportError as e:
        print(f"缺 scene_kit: {e}", file=sys.stderr)
        sys.exit(2)
    hexes = palette_list(args.palette) if args.palette else []
    if args.theme:
        tpath = os.path.join(os.path.dirname(os.path.abspath(LIBRARY)), "themes.json")
        with open(tpath, encoding="utf-8") as f:
            td = json.load(f)
        ts = td["themes"] if isinstance(td, dict) else td
        rec = next((t for t in ts if t.get("name_en") == args.theme or t["name"] == args.theme), None)
        if rec is None:
            print(f"主题不存在: {args.theme}", file=sys.stderr)
            sys.exit(2)
        c = rec["colors"]
        hexes = [v.lstrip("#").upper() for v in c.values()]
    if len(hexes) < 3:
        print("--theme 或 --palette 必给其一(≥3 色)", file=sys.stderr)
        sys.exit(2)
    name = args.name or (args.theme or "palette")
    if args.kind.lower().strip() not in scene_kit.KINDS:
        print(f"未知场景类型: {args.kind}——可选: {', '.join(scene_kit.KINDS)}", file=sys.stderr)
        sys.exit(2)
    try:
        html, declared = scene_kit.build_scene(args.kind, hexes, name,
                                               dark=bool(args.dark), force=bool(args.force))
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    out = args.out or f"scene-{args.kind}.html"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"scene: {out} (kind={args.kind} name={name})")
    print(f"主题色板(声明): {declared}")
    print("下一步:作为页面起点填充,或嵌入;替换后 report/evidence 验收")


def _safe_out_dir():
    """AE6: 无 --out 时默认落点。cwd 在 skill 包内(只读安装被污染/写失败)→ ~/.cache/aesthete/。"""
    cwd = os.getcwd()
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # skill 根(scripts 的父)
    try:
        inside = os.path.commonpath([cwd, pkg_root]) == pkg_root
    except ValueError:
        inside = False
    if inside:
        d = os.path.join(os.path.expanduser("~"), ".cache", "aesthete")
        os.makedirs(d, exist_ok=True)
        print(f"输出落点: cwd 在 skill 包内,改写 {d}(避免污染安装包;显式 --out 可指定)", file=sys.stderr)
        return d
    return cwd


def cmd_scaffold(args):
    """表现力页面骨架(0.9):主题 → 四幕明暗旅程整页(night-hero/晨坊/夜话/夜约),
    颗粒+巨字对微字+不对称网格+滚动揭示,对比度自动调墨;替换标记就绪,替换后跑验收。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import scaffold_kit
    except ImportError as e:
        print(f"缺 scaffold_kit: {e}", file=sys.stderr)
        sys.exit(2)
    if args.theme:
        tpath = os.path.join(os.path.dirname(os.path.abspath(LIBRARY)), "themes.json")
        with open(tpath, encoding="utf-8") as f:
            td = json.load(f)
        ts = td["themes"] if isinstance(td, dict) else td
        rec = next((t for t in ts if t.get("name_en") == args.theme or t["name"] == args.theme), None)
        if rec is None:
            print(f"主题不存在: {args.theme}——可选: " +
                  ", ".join(t.get("name_en", t["name"]) for t in ts), file=sys.stderr)
            sys.exit(2)
        tokens = scaffold_kit.theme_tokens(rec, args.brand, args.brand_en)
    elif args.palette:
        _hexes = palette_list(args.palette)
        if len(set(_hexes)) < 3:
            print("至少 3 个不同颜色(两色板无法分配角色)", file=sys.stderr)
            sys.exit(2)
        tokens = scaffold_kit.derive({"hexes": _hexes},
                                     args.brand or "山野手作", args.brand_en or "Studio",
                                     args.use_when or "")
    else:
        print("--theme 或 --palette 必给其一", file=sys.stderr)
        sys.exit(2)
    recipe = (getattr(args, "recipe", None) or "AUTO").upper().strip()
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import layout_recipes
        html = layout_recipes.build_recipe(tokens, recipe)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)
    out = args.out or (args.brand or "scaffold").lower().replace(" ", "-") + "-" + recipe.lower().replace("_", "-") + ".html"
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    fonts_mode = (getattr(args, "fonts", "none") or "none").lower()
    if fonts_mode != "none":
        import font_kit
        html, copied = font_kit.emit_faces(os.path.dirname(os.path.abspath(out)), fonts_mode, html,
                                           log=lambda m: print(f"fonts: {m}"))
        if copied:
            print(f"fonts: {fonts_mode} → {', '.join(os.path.basename(c) for c in copied)}")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"scaffold: {out}")
    print(f"主题色板(声明): {tokens['PALETTE_DECL']}")
    print("下一步:替换『替换』标记的内容 → report/evidence 验收")


def cmd_evidence(args):
    """页面证据卷宗:静态 lint + 四闸 report(+可选渲染探针)合成一份 JSON + 一份人读 HTML。
    退出码 = 裁决(任一闸 FAIL 即非零)。交付前跑一次,卷宗即验收记录。"""
    page = args.page
    if not os.path.exists(page):
        print(f"文件不存在: {page}", file=sys.stderr)
        sys.exit(2)
    hexes = [h.upper() for h in palette_list(args.palette)]
    here = os.path.dirname(os.path.abspath(__file__))
    ev = {"page": os.path.abspath(page), "palette": hexes, "render": None}

    rep = subprocess.run([sys.executable, os.path.abspath(__file__), "report", "--palette", ",".join(hexes)],
                         capture_output=True, text=True)
    _out = rep.stdout.strip()
    _i = _out.find("{")
    try:
        ev["report"] = json.loads(_out[_i:]) if _i >= 0 else {}
    except Exception:
        ev["report"] = {"error": (_out or rep.stderr)[-400:]}
    lint_cmd = [sys.executable, os.path.join(here, "lint_page.py"), page, "--palette", ",".join(hexes)]
    if args.render:
        lint_cmd += ["--render", args.render]
        try:
            ev["render"] = json.load(open(args.render, encoding="utf-8"))
        except Exception:
            pass
    lint = subprocess.run(lint_cmd, capture_output=True, text=True)
    ev["lint"] = {"exit": lint.returncode, "output": (lint.stdout + lint.stderr).strip()[-2000:]}

    rj = ev.get("report") or {}
    verdict = rj.get("verdict", "FAIL" if rj.get("error") else "UNKNOWN")
    ev["verdict"] = "PASS" if (verdict == "PASS" and lint.returncode == 0) else "FAIL"
    # 零模型信任闸:页面字节+声明色板+裁决 摘要互锁,验收记录可对账防篡改
    page_fp = hashlib.sha256(open(page, "rb").read()).hexdigest()
    ev["fingerprint"] = hashlib.sha256(
        ("aesthete-evidence/v1|" + ",".join(hexes) + "|" + page_fp + "|" + ev["verdict"])
        .encode("utf-8")).hexdigest()
    ev["page_sha256"] = page_fp
    base = args.out or (os.path.splitext(page)[0] + ".evidence")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump(ev, f, ensure_ascii=False, indent=1)
    ok = ev["verdict"] == "PASS"
    bar_color, bar_txt = ("#3D8361", "PASS — 四闸 + 静态审计全过") if ok else ("#B04A3A", "FAIL — 有闸未过,禁止交付")
    gates = rj.get("gates", {})
    gate_rows = "".join(
        f"<tr><td>{k}</td><td style='color:{'#3D8361' if v.get('pass') else '#B04A3A'}'>"
        f"{'PASS' if v.get('pass') else 'FAIL'}</td><td><code>{v.get('best') or v.get('detail') or ''}</code></td></tr>"
        for k, v in gates.items())
    html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>证据卷宗 — {os.path.basename(page)}</title>
<style>body{{margin:0;font:14px/1.6 system-ui;background:#F6F2E8;color:#3D405B}}
header{{padding:18px 26px;background:{bar_color};color:#fff}}
h1{{margin:0;font-size:17px}} table{{border-collapse:collapse;width:100%;background:#fff}}
td,th{{border:1px solid #E2DCCB;padding:7px 12px;text-align:left;font-size:13px}}
th{{background:#EFE9D8}} code{{font-size:12px}} pre{{background:#fff;border:1px solid #E2DCCB;
padding:12px;white-space:pre-wrap;font-size:12px}}</style></head><body>
<header><h1>证据卷宗 · {os.path.basename(page)} — {bar_txt}</h1></header>
<div style="padding:16px 26px">
<p>声明色板:{' '.join('#' + h for h in hexes)}　页面:<code>{os.path.abspath(page)}</code></p>
<h3>四道机械闸</h3><table><tr><th>闸</th><th>裁决</th><th>证据</th></tr>{gate_rows}</table>
<h3>静态审计(lint_page)</h3><pre>{ev['lint']['output'] or '(无输出)'}</pre>
{('<h3>渲染证据(render_probe)</h3><pre>' + json.dumps(ev['render'], ensure_ascii=False, indent=1)[:1200] + '</pre>') if ev['render'] else '<p>渲染探针未采集——用浏览器工具执行 render_probe.js 后以 --render 传入,卷宗补渲染事实。</p>'}
</div></body></html>"""
    with open(base + ".html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"证据卷宗: {base}.json + {base}.html — 裁决 {ev['verdict']}")
    sys.exit(0 if ok else 1)


def cmd_tokens(args):
    """设计令牌表(0.9):色板/主题 → 语义 token(CSS+JSON)。
    墨色自动调墨,accent 拆图形/文字双 token,数值注释即证据;指纹互锁。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import token_sheet
    except ImportError as e:
        print(f"缺 token_sheet: {e}", file=sys.stderr)
        sys.exit(2)
    if args.theme:
        hexes = _theme_hexes(args.theme)
    elif args.palette:
        hexes = [h.upper().lstrip("#") for h in palette_list(args.palette)]
    else:
        print("--theme 或 --palette 必给其一(≥3 色)", file=sys.stderr)
        sys.exit(2)
    if len(hexes) < 3:
        print("至少 3 色", file=sys.stderr)
        sys.exit(2)
    payload, rc = token_sheet.emit(
        hexes, args.name or args.theme or "palette", args.brand or "",
        dark=bool(args.dark), out_base=args.out or os.path.join(_safe_out_dir(), "tokens"))
    print(f"tokens: {(args.out or 'tokens')}.css + .json — 裁决 {payload['verdict']}")
    for k, v in payload["ratios"].items():
        print(f"  {k} = {v:.2f}:1")
    if payload["problems"]:
        print("未达标: " + "; ".join(payload["problems"]), file=sys.stderr)
    print("下一步: tokens.css 供页面直接引用;交付前 report/evidence 验收")
    sys.exit(rc)


def cmd_audit(args):
    """外部页面机械审计(0.9):漂移带最近板色/对比对带达标替换值/禁渐变/紫域大底/
    AI 默认签名;P0 存在或 P1≥2 = FAIL。静态范围如实声明(外链 CSS 用 render probe 补)。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import page_audit
    except ImportError as e:
        print(f"缺 page_audit: {e}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.page):
        print(f"文件不存在: {args.page}", file=sys.stderr)
        sys.exit(2)
    pal = palette_list(args.palette) if args.palette else None
    payload = page_audit.run(args.page, pal, floor=args.floor, out_base=args.out)
    n = payload["counts"]
    print(f"audit: {os.path.basename(args.page)} — 裁决 {payload['verdict']} "
          f"(P0×{n['P0']} P1×{n['P1']} P2×{n['P2']})")
    for f in payload["findings"]:
        print(f"[{f['sev']}] {f['msg']}")
        print(f"      ↳ {f['fix']}")
    if not payload["findings"]:
        print("[OK] 未发现机械问题;视觉层(视线顺序/密度/构图)仍需五镜截图自审")
    print(f"指纹: {payload['fingerprint'][:16]}…  范围: {payload['scope']}")
    sys.exit(0 if payload["verdict"] != "FAIL" else 1)


def cmd_chartpal(args):
    """图表用色板(0.10):categorical=CVD 择优系列色 / sequential=单色相明度坡 /
    diverging=双端-中性中点。产出 JSON+标注色样 HTML;区分度/单调性不达标 exit 1。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import chart_kit
    except ImportError as e:
        print(f"缺 chart_kit: {e}", file=sys.stderr)
        sys.exit(2)
    if args.theme:
        hexes = _theme_hexes(args.theme)
    elif args.palette:
        hexes = [h.upper().lstrip("#") for h in palette_list(args.palette)]
    else:
        print("--theme 或 --palette 必给其一", file=sys.stderr)
        sys.exit(2)
    n = max(2, min(args.series, 12))
    if args.kind == "categorical":
        if len(hexes) < 2:
            print("categorical 需 ≥2 候选色", file=sys.stderr)
            sys.exit(2)
        series, checks = chart_kit.categorical(hexes, n,
                                               canvas=(getattr(args, "canvas", None) or "FFFFFF"))
    elif args.kind == "sequential":
        series, checks = chart_kit.sequential(hexes[0], n, reverse=bool(args.reverse))
    elif args.kind == "diverging":
        if len(hexes) < 2:
            print("diverging 需两端色(--palette 至少 2 色)", file=sys.stderr)
            sys.exit(2)
        series, checks = chart_kit.diverging(hexes[0], hexes[1], n)
    else:
        print(f"未知类型: {args.kind}", file=sys.stderr)
        sys.exit(2)
    _cp_out = args.out or os.path.join(_safe_out_dir(), "chartpal")
    payload = chart_kit.emit(args.kind, series, checks, args.name or "", _cp_out,
                             canvas=getattr(args, "canvas", None))
    print(f"chartpal: {_cp_out}.json + .html — 裁决 {payload['verdict']}")
    print("  系列: " + " ".join("#" + h for h in series))
    for k, v in checks.items():
        if k != "verdict":
            print(f"  {k} = {v}")
    print("用色纪律: 一个主角系列给重点;直接标注数据少用图例;数字列 tabular-nums")
    sys.exit(0 if payload["verdict"] == "PASS" else 1)


def cmd_typescale(args):
    """CJK 友好字阶(0.10):模块等比生成 7 级,12px 硬下限,行高配对,
    tabular-nums 数据令牌;产出 tokens CSS + 中英混排样张 + JSON。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import type_kit
    except ImportError as e:
        print(f"缺 type_kit: {e}", file=sys.stderr)
        sys.exit(2)
    payload = type_kit.emit(args.name or "", base=args.base, ratio=args.ratio,
                            floor=args.floor,
                            out_base=args.out or os.path.join(_safe_out_dir(), "typescale"),
                            fluid=bool(getattr(args, "fluid", False)))
    print(f"typescale: {(args.out or 'typescale')}.css + .html + .json — 裁决 {payload['verdict']}")
    for s in ("3xl", "2xl", "xl", "lg", "base", "sm", "xs"):
        t = payload["tokens"][s]
        print(f"  --text-{s}: {t['px']}px/{t['lh']} ({t['role']})")
    if payload["checks"]["clamped_steps"]:
        print(f"  下限钳制: {', '.join(payload['checks']['clamped_steps'])}")
    sys.exit(0 if payload["verdict"] == "PASS" else 1)


def cmd_qc(args):
    """渲染对账(0.11):截图 PNG vs 声明令牌/色板——大底真伪/板外入侵。
    渲染反馈闭环的机械闸:页面声明与实际渲染脱节(变量被覆盖/样式未加载)在此现形。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import qc_kit
    except ImportError as e:
        print(f"缺 qc_kit: {e}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.image):
        print(f"文件不存在: {args.image}", file=sys.stderr)
        sys.exit(2)
    declared, bg = [], None
    if args.tokens:
        with open(args.tokens, encoding="utf-8") as f:
            td = json.load(f)
        tk = td.get("tokens", td)
        for v in tk.values():
            if isinstance(v, str) and re.fullmatch(r"#?[0-9a-fA-F]{6}", v.strip()):
                declared.append(v.strip().lstrip("#").upper())
        bg = tk.get("bg")
    elif args.palette:
        declared = [h.upper().lstrip("#") for h in palette_list(args.palette)]
    else:
        print("--tokens 或 --palette 必给其一", file=sys.stderr)
        sys.exit(2)
    if args.bg:
        bg = args.bg
    if len(declared) < 2:
        print("声明色不足 2 个", file=sys.stderr)
        sys.exit(2)
    payload = qc_kit.qc_image(args.image, declared, bg)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
    n = payload["size"]
    print(f"qc: {os.path.basename(args.image)}({n[0]}×{n[1]}) — 裁决 {payload['verdict']}")
    print("  主色聚类: " + "  ".join(
        f"#{c['hex']} {c['share']*100:.0f}%" for c in payload["clusters"][:5]))
    for f in payload["findings"]:
        print(f"[{f['sev']}] {f['msg']}")
        print(f"      ↳ {f['fix']}")
    if not payload["findings"]:
        print("[OK] 渲染实况与声明一致(聚类级);构图层仍走五镜截图自审")
    print(f"指纹: {payload['fingerprint'][:16]}…")
    sys.exit(0 if payload["verdict"] != "FAIL" else 1)


def cmd_narrate(args):
    """量化叙事(0.12):report 实测数字 → 双语说明文,数字可溯源,句式模板零发挥。
    给"为什么这样配"一个可直接转发的答案;退出码跟 report 裁决。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import narrate_kit
    except ImportError as e:
        print(f"缺 narrate_kit: {e}", file=sys.stderr)
        sys.exit(2)
    if args.theme:
        hexes = _theme_hexes(args.theme)
    else:
        hexes = [h.upper().lstrip("#") for h in palette_list(args.palette or "")]
    if len(hexes) < 3:
        print("--theme 或 --palette 必给其一(≥3 色)", file=sys.stderr)
        sys.exit(2)
    rep = subprocess.run([sys.executable, os.path.abspath(__file__),
                          "report", "--palette", ",".join(hexes)],
                         capture_output=True, text=True)
    _out = rep.stdout.strip()
    _i = _out.find("{")
    try:
        report = json.loads(_out[_i:]) if _i >= 0 else {}
    except Exception:
        print(f"report 解析失败: {(_out or rep.stderr)[-300:]}", file=sys.stderr)
        sys.exit(2)
    roles = _viz_roles(hexes, dark=bool(getattr(args, "dark", False)))
    body, verdict = narrate_kit.emit(report, hexes, roles, args.name or args.theme or "",
                                     out=args.out)
    print(body)
    if not args.out:
        default = os.path.join(_safe_out_dir(), (args.name or args.theme or "palette")
                               .strip().replace(" ", "-") + ".narration.md")
        with open(default, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        print(f"(已写入 {default})")
    sys.exit(0 if verdict == "PASS" else 1)


def cmd_exemplar(args):
    """范例库检索注入(0.16):渲染评审+四闸验证过的配方快照按 kind/register 检索。
    调研定案:范例代码注入 ≥ token 表 > 可判定禁令;检索零命中显式报错不猜。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import exemplar_kit
    except ImportError as e:
        print(f"缺 exemplar_kit: {e}", file=sys.stderr)
        sys.exit(2)
    body, err = exemplar_kit.emit(kind=args.kind, register=args.register, list_only=args.list)
    if err:
        print(err, file=sys.stderr)
        sys.exit(2)
    print(body)
    sys.exit(0)


def cmd_patch(args):
    """定点修改(0.16):audit findings → 字面 search/replace 对;--apply 备份 .bak 后直修并复检。
    检查结果不再只是散文——机械类(脏色大底/字号下限/中文负字距/对比对)当场修,
    不可机械类降级 manual 指引,不猜不改。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import page_audit
    except ImportError as e:
        print(f"缺 page_audit: {e}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.page):
        print(f"文件不存在: {args.page}", file=sys.stderr)
        sys.exit(2)
    pal = [h.upper().lstrip("#") for h in palette_list(args.palette)] if args.palette else None
    with open(args.page, encoding="utf-8", newline="") as f:
        html = f.read()
    findings, _ = page_audit.audit_page(html, pal, args.floor)
    patches = page_audit.patches_for(findings, html)
    if not args.apply:
        lit = [p for p in patches if p["search"]]
        print(f"定点修改清单: 机械可修 {len(lit)} 条 / manual {len(patches) - len(lit)} 条")
        for p in patches:
            if p["search"]:
                print(f"  [{p['sev']}|{p['check']}] {p['search']!r} -> {p['replace']!r}  # {p['note']}")
            else:
                print(f"  [{p['sev']}|{p['check']}] manual: {p['note']}")
        if args.out:
            with open(args.out, "w", encoding="utf-8", newline="\n") as f:
                json.dump(patches, f, ensure_ascii=False, indent=1)
        sys.exit(0 if lit else 2)
    import shutil
    bak = args.page + ".bak"
    if not os.path.exists(bak):
        shutil.copy2(args.page, bak)                    # 仅首轮备份(原始态=回滚点,CRLF/编码不动)
    lit = [p for p in patches if p["search"]]
    applied = 0
    for p in lit:
        if p["search"] in html:
            html = html.replace(p["search"], p["replace"])
            applied += 1
    with open(args.page, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    findings2, _ = page_audit.audit_page(html, pal, args.floor)
    n2 = {s: sum(1 for x in findings2 if x["sev"] == s) for s in ("P0", "P1", "P2")}
    print(f"已应用 {applied}/{len(lit)} 条机械补丁(备份 {bak})")
    print(f"复检: P0={n2['P0']} P1={n2['P1']} P2={n2['P2']}")
    for x in findings2:
        print(f"  [{x['sev']}|{x['check']}] {x['msg']}")
    ok = n2["P0"] == 0 and n2["P1"] < 2
    print("裁决:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def cmd_loop(args):
    """渲染闭环清单(0.16):渲染评审轮编码化为宿主可执行检查单
    (机械预检/截图三铁律/qc 对账/五镜/patch 定点修/停止条件),命令按实参生成。"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import loop_kit
    except ImportError as e:
        print(f"缺 loop_kit: {e}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.page):
        print(f"文件不存在: {args.page}", file=sys.stderr)
        sys.exit(2)
    hexes = [h.upper().lstrip("#") for h in palette_list(args.palette)]
    if len(hexes) < 2:
        print("--palette 至少 2 色", file=sys.stderr)
        sys.exit(2)
    md = loop_kit.emit(args.page, hexes, floor=args.floor, bg=args.bg, out=args.out)
    print(md)
    if not args.out:
        default = os.path.splitext(args.page)[0] + ".loop.md"
        with open(default, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        print(f"(已写入 {default})")
    sys.exit(0)


def cmd_card(args):
    hexes = palette_list(args.palette)
    name = args.name or "Palette"
    roles_css = ""
    try:
        rs = sorted(((oklch_from_hex(h), h) for h in hexes), reverse=True)
        roles_css = "--c-bg:#%s;--c-text:#%s;" % (rs[0][1], rs[-1][1])
    except Exception:
        pass
    swatches = []
    for h in hexes:
        t = readable_text(h)
        swatches.append(f"""
        <div style="background:#{h};color:#{t};flex:1;display:flex;flex-direction:column;
             justify-content:flex-end;padding:18px 14px;min-height:220px">
          <div style="font:600 15px/1.4 system-ui;opacity:.55">#{h.upper()}</div>
        </div>""")
    mock = f"""
    <div style="background:#F7F7F5;padding:26px;border-radius:10px;margin-top:22px">
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px">
        <div style="width:34px;height:34px;border-radius:8px;background:#{hexes[-1] if len(hexes)>3 else hexes[0]}"></div>
        <div style="font:700 17px system-ui;color:#222">Acme</div>
        <div style="margin-left:auto;display:flex;gap:8px">
          <span style="padding:7px 14px;border-radius:6px;background:#{hexes[0]};font:500 13px system-ui;color:#{readable_text(hexes[0])}">Ghost</span>
          <span style="padding:7px 14px;border-radius:6px;background:#{hexes[min(3,len(hexes)-1)]};font:500 13px system-ui;color:#{readable_text(hexes[min(3,len(hexes)-1)])}">CTA</span>
        </div>
      </div>
      <div style="display:flex;gap:10px;align-items:flex-end;height:90px;margin-top:8px">
        {"".join(f'<div style="flex:1;height:{25+((i*37)%70)}%;background:#{h};border-radius:4px 4px 0 0"></div>' for i, h in enumerate(hexes))}
      </div>
      <div style="margin-top:14px;height:10px;border-radius:5px;overflow:hidden;display:flex">{"".join(f'<div style="flex:1;background:#{h}"></div>' for h in hexes)}</div>
    </div>"""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>{name}</title></head>
<body style="margin:0;background:#fff;font-family:system-ui">
  <div style="max-width:860px;margin:0 auto;padding:28px">
    <div style="display:flex;justify-content:space-between;align-items:baseline">
      <h1 style="font:700 22px system-ui;margin:0 0 14px">{name}</h1>
      <span style="font:500 13px system-ui;color:#888">aesthete-agent card</span>
    </div>
    <div style="display:flex;border-radius:10px;overflow:hidden;border:1px solid #eee">
      {''.join(swatches)}
    </div>
    {mock}
  </div>
</body></html>"""
    out = args.out or "palette_card.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"card written: {out}")
    print("self-review: screenshot/emitImage this file, then judge roles+contrast in context")


def cmd_export(args):
    hexes = palette_list(args.palette)
    if args.format == "w3c":
        print(_export_w3c(hexes))
    elif args.format == "context":
        print(_export_context(hexes))
    elif args.format == "prompt":
        print(_export_prompt(hexes))
    elif args.format == "css":
        print(":root{")
        for i, h in enumerate(hexes):
            print(f"  --color-{i+1}: #{h.upper()};")
        print("}")
    elif args.format == "tailwind":
        print("// tailwind.config extend.colors")
        names = ["primary", "secondary", "accent", "muted", "base", "extra"]
        print("colors: {")
        for i, h in enumerate(hexes):
            print(f"  '{names[i] if i < len(names) else f'shade{i}'}': '#{h.upper()}',")
        print("}")
    elif args.format == "json":
        print(json.dumps(hexes))
    elif args.format == "svg":
        w = 120 * len(hexes)
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="120">']
        for i, h in enumerate(hexes):
            t = readable_text(h)
            parts.append(f'<rect x="{i*120}" y="0" width="120" height="120" fill="#{h}"/>')
            parts.append(f'<text x="{i*120+12}" y="108" font-family="monospace" font-size="14" fill="#{t}">#{h.upper()}</text>')
        parts.append("</svg>")
        print("".join(parts))


def main():
    p = argparse.ArgumentParser(description="aesthete-agent: offline frontend-aesthetics & palette engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("harmony")
    s.add_argument("--base", required=True)
    s.add_argument("--mode", default="analogous",
                   choices=["monochromatic", "analogous", "complementary",
                            "split-complementary", "triadic", "tetradic", "square"])
    s.add_argument("--theme", default="light", choices=["light", "dark"])
    s.add_argument("--count", type=int)
    s.set_defaults(fn=cmd_harmony)

    s = sub.add_parser("mutate")
    s.add_argument("--palette", required=True)
    s.add_argument("--shade", type=float, default=0, help="-100..100 darken/lighten")
    s.add_argument("--sat", type=float, default=0, help="-100..100 chroma delta")
    s.add_argument("--hue", type=float, default=0, help="hue rotate degrees")
    s.add_argument("--temp", type=float, default=0, help="-100..100 cool..warm")
    s.add_argument("--lum", type=float, default=0, help="-100..100 lightness delta")
    s.set_defaults(fn=cmd_mutate)

    s = sub.add_parser("contrast")
    s.add_argument("--fg", required=True)
    s.add_argument("--bg", required=True)
    s.add_argument("--large", action="store_true", help="large text threshold 3:1")
    s.add_argument("--method", default="wcag", choices=["wcag", "apca"], help="apca=WCAG3 草案感知算法")
    s.set_defaults(fn=cmd_contrast)

    s = sub.add_parser("roles")
    s.add_argument("--palette", required=True)
    s.add_argument("--theme", default="light", choices=["light", "dark"])
    s.add_argument("--css", action="store_true")
    s.add_argument("--semantic", action="store_true", help="derive success/warning/error/info from accent hue")
    s.set_defaults(fn=cmd_roles)

    s = sub.add_parser("ramp")
    s.add_argument("--base", required=True, help="seed hue/lightness source")
    s.add_argument("--steps", type=int, default=7)
    s.add_argument("--direction", default="light", choices=["light", "dark"], help="light: dark->light ramp; dark: light->dark")
    s.set_defaults(fn=cmd_ramp)

    s = sub.add_parser("score")
    s.add_argument("--palette", required=True)
    s.set_defaults(fn=cmd_score)

    s = sub.add_parser("showcase")
    s.add_argument("--style", help="comma list of style tags")
    s.add_argument("--min-likes", type=int, default=0)
    s.add_argument("--limit", type=int, default=8)
    s.add_argument("--out", default=None)
    s.set_defaults(fn=cmd_showcase)

    s = sub.add_parser("blind")
    s.add_argument("--palette", required=True)
    s.add_argument("--kind", choices=["protanopia", "deuteranopia", "tritanopia"])
    s.set_defaults(fn=cmd_blind)

    s = sub.add_parser("slop")
    s.add_argument("--palette", required=True)
    s.set_defaults(fn=cmd_slop)

    s = sub.add_parser("extract")
    s.add_argument("image")
    s.add_argument("--n", type=int, default=6)
    s.set_defaults(fn=cmd_extract)

    s = sub.add_parser("search")
    s.add_argument("--style", help="comma list: warm,cool,dark,light,mid,pastel,vivid,monochromatic,multihue,deep")
    s.add_argument("--min-likes", type=int, default=0)
    s.add_argument("--no-flags", action="store_true", help="exclude palettes carrying any gate flag")
    s.add_argument("--limit", type=int, default=8)
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("themes")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_themes)

    s = sub.add_parser("theme")
    s.add_argument("name", help="主题名(中文或英文)")
    s.add_argument("--format", default="css", choices=["css", "json"])
    s.set_defaults(fn=cmd_theme)

    s = sub.add_parser("matrix")
    s.add_argument("--palette", required=True)
    s.add_argument("--recommend", action="store_true")
    s.add_argument("--method", default="wcag", choices=["wcag", "apca"], help="apca=WCAG3 草案感知算法")
    s.set_defaults(fn=cmd_matrix)

    s = sub.add_parser("semantic")
    s.add_argument("--count", type=int, default=8,
                   help="deprecated: 图表/分类用色已并入 chartpal --kind categorical,本命令仅保留兼容")
    s.add_argument("--base", default=None, help="基准色(取其色相)")
    s.add_argument("--hue", type=float, default=210.0, help="无 --base 时的起始色相")
    s.set_defaults(fn=cmd_semantic)

    s = sub.add_parser("critique")
    s.add_argument("--palette", default=None)
    s.add_argument("--evidence", default=None, help="render_probe 采集的 evidence.json")
    s.add_argument("--out", default=None)
    s.set_defaults(fn=cmd_critique)

    s = sub.add_parser("doctor")
    s.set_defaults(fn=cmd_doctor)

    s = sub.add_parser("visualize")
    s.add_argument("--palette", required=True)
    s.add_argument("--name", default="Palette")
    s.add_argument("--theme", default=None, choices=["light", "dark"])
    s.add_argument("--svg", default=None, help="对其做重着色(纯黑白保留)")
    s.add_argument("--variants", type=int, default=1, help="同场景 N 次色板排列对比(旋转+反转)")
    s.add_argument("--shuffle", type=int, default=1, help="--svg 重着色排列数(含对比网格页)")
    s.add_argument("--out", default=None)
    s.set_defaults(fn=cmd_visualize)

    s = sub.add_parser("report")
    s.add_argument("--zones", default=None, help="页面区域占比 hex:share,...(给出即加第五闸 drama)")
    s.add_argument("--bold", action="store_true", help="品牌页(drama 准入放宽)")
    s.add_argument("--palette", required=True)
    s.set_defaults(fn=cmd_report)

    s = sub.add_parser("direct", help="色彩导演:整页配色机械度量(0.19)")
    s.add_argument("--zones", default=None, help="hex:share,hex:share,...")
    s.add_argument("--manifest", default=None, help="lab_zones.json 批量裁决")
    s.add_argument("--page", default=None, help="页面名(写入报告头)")
    s.add_argument("--bold", action="store_true", help="品牌页(大域准入)")
    s.set_defaults(fn=cmd_direct)

    s = sub.add_parser("selftest")
    s.set_defaults(fn=cmd_selftest)

    s = sub.add_parser("house")
    s.add_argument("--name", required=True)
    s.add_argument("--hexes", required=True)
    s.add_argument("--from-proj", default=None, help="来源项目名")
    s.set_defaults(fn=cmd_house)

    s = sub.add_parser("match")
    s.add_argument("--brief", required=True, help="需求自然语言,如:儿科教学页/素雅落地页/母婴封面")
    s.add_argument("--register", choices=list(BRIEF_KEYWORDS.keys()), default=None)
    s.add_argument("--no-flags", action="store_true")
    s.add_argument("--limit", type=int, default=6)
    s.set_defaults(fn=cmd_match)

    s = sub.add_parser("directions")
    s.add_argument("--brief", default="", help="需求自然语言,如:素雅耐看的落地页")
    s.add_argument("--registers", default=None, help="逗号分隔语域,显式指定时跳过 brief")
    s.add_argument("--n", type=int, default=3, help="方向数 2-4")
    s.add_argument("--out-dir", default=None)
    s.set_defaults(fn=cmd_directions)

    s = sub.add_parser("scene")
    s.add_argument("--kind", required=True,
                   help="wallet/landing/dashboard/branding/typography/chart/ecom/email/editorial/pattern")
    s.add_argument("--theme", help="主题包 name_en/name")
    s.add_argument("--palette", help="逗号分隔 hex(无主题时)")
    s.add_argument("--name", default=None, help="色板显示名(默认取主题名)")
    s.add_argument("--dark", action="store_true")
    s.add_argument("--force", action="store_true", help="越过 AI 默认紫守门(留痕)")
    s.add_argument("--out", default=None, help="输出路径")
    s.set_defaults(fn=cmd_scene)

    s = sub.add_parser("scaffold")
    s.add_argument("--theme", help="主题包 name_en/name,如 Deep Pine")
    s.add_argument("--palette", help="逗号分隔 hex(无主题时用)")
    s.add_argument("--recipe", default="AUTO",
                   help="布局配方: AUTO(默认,按色板气质路由)/DARK-FOUR-ACT/EDIT-SPLIT/BLUEPRINT/SWISS-POSTER/EDITORIAL-MAG")
    s.add_argument("--fonts", default="none", choices=["none", "preset", "auto"],
                   help="字体资产: none(系统栈,禁 900)/preset(随包子集)/auto(现场子集,缺 fontTools 降级 preset)")
    s.add_argument("--brand", default=None, help="品牌名(默认取主题)")
    s.add_argument("--brand-en", dest="brand_en", default=None)
    s.add_argument("--use-when", dest="use_when", default="")
    s.add_argument("--out", default=None, help="输出路径")
    s.set_defaults(fn=cmd_scaffold)

    s = sub.add_parser("check-image")
    s.add_argument("image", help="图片路径(封面/截图)")
    s.add_argument("--n", type=int, default=5, help="取色数,默认 5")
    s.set_defaults(fn=cmd_check_image)

    s = sub.add_parser("evidence")
    s.add_argument("page", help="已完成的页面 HTML")
    s.add_argument("--palette", required=True, help="声明色板,逗号分隔 hex")
    s.add_argument("--render", default=None, help="render_probe.js 采集的 evidence.json(可选)")
    s.add_argument("--out", default=None, help="输出前缀(默认 <page>.evidence)")
    s.set_defaults(fn=cmd_evidence)

    s = sub.add_parser("tokens")
    s.add_argument("--palette", default=None, help="色板,逗号分隔 hex")
    s.add_argument("--theme", default=None, help="主题包名(与 --palette 二选一)")
    s.add_argument("--name", default=None, help="令牌表名(写入注释头)")
    s.add_argument("--brand", default=None, help="品牌名(写入注释)")
    s.add_argument("--dark", action="store_true", help="深色为主(令牌明暗互换)")
    s.add_argument("--out", default=None, help="输出前缀(默认 tokens)")
    s.set_defaults(fn=cmd_tokens)

    s = sub.add_parser("audit")
    s.add_argument("page", help="外部页面 HTML")
    s.add_argument("--palette", default=None, help="声明色板(给出即查漂移)")
    s.add_argument("--floor", type=float, default=12, help="字号下限 px")
    s.add_argument("--out", default=None, help="JSON 输出前缀")
    s.set_defaults(fn=cmd_audit)

    s = sub.add_parser("chartpal")
    s.add_argument("--kind", required=True,
                   choices=["categorical", "sequential", "diverging"])
    s.add_argument("--palette", default=None, help="候选色(分类≥2;发散=两端色)")
    s.add_argument("--theme", default=None, help="主题包名(与 --palette 二选一)")
    s.add_argument("--series", type=int, default=6, help="系列数(2-12)")
    s.add_argument("--reverse", action="store_true", help="顺序板浅→深反转")
    s.add_argument("--name", default=None)
    s.add_argument("--canvas", default="FFFFFF",
                   help="目标画布 hex(默认 FFFFFF;系列色对画布 <3.0:1 降级,<1.5:1 FAIL)")
    s.add_argument("--out", default=None, help="输出前缀(默认 chartpal)")
    s.set_defaults(fn=cmd_chartpal)

    s = sub.add_parser("typescale")
    s.add_argument("--base", type=float, default=16, help="正文字号 px")
    s.add_argument("--ratio", type=float, default=1.25, help="等比(1.125-1.5)")
    s.add_argument("--floor", type=float, default=12, help="字号硬下限 px")
    s.add_argument("--fluid", action="store_true", help="display 级发流体 clamp(375-1440px 线性)")
    s.add_argument("--name", default=None)
    s.add_argument("--out", default=None, help="输出前缀(默认 typescale)")
    s.set_defaults(fn=cmd_typescale)

    s = sub.add_parser("qc")
    s.add_argument("image", help="渲染截图 PNG")
    s.add_argument("--tokens", default=None, help="tokens.json(令牌对账)")
    s.add_argument("--palette", default=None, help="声明色板,逗号分隔 hex")
    s.add_argument("--bg", default=None, help="声明大底 hex(色板模式建议显式给)")
    s.add_argument("--out", default=None, help="JSON 输出路径")
    s.set_defaults(fn=cmd_qc)

    s = sub.add_parser("narrate")
    s.add_argument("--palette", default=None, help="色板,逗号分隔 hex")
    s.add_argument("--theme", default=None, help="主题包名(与 --palette 二选一)")
    s.add_argument("--name", default=None, help="板名(写入标题)")
    s.add_argument("--dark", action="store_true", help="按暗底推导角色")
    s.add_argument("--out", default=None, help="输出 md 路径")
    s.set_defaults(fn=cmd_narrate)

    s = sub.add_parser("exemplar")
    s.add_argument("--kind", default=None,
                   help="页面类型: landing/tech-landing/poster/editorial/narrative")
    s.add_argument("--register", default=None, choices=["light", "dark"], help="明暗语域")
    s.add_argument("--list", action="store_true", help="只列范例目录")
    s.set_defaults(fn=cmd_exemplar)

    s = sub.add_parser("patch")
    s.add_argument("page", help="页面 HTML")
    s.add_argument("--palette", default=None, help="声明色板(给出即查漂移)")
    s.add_argument("--floor", type=float, default=12, help="字号下限 px")
    s.add_argument("--apply", action="store_true", help="备份 .bak 后应用机械补丁并复检")
    s.add_argument("--out", default=None, help="补丁清单 JSON 输出路径")
    s.set_defaults(fn=cmd_patch)

    s = sub.add_parser("loop")
    s.add_argument("page", help="页面 HTML")
    s.add_argument("--palette", required=True, help="声明色板,逗号分隔 hex")
    s.add_argument("--floor", type=float, default=12, help="字号下限 px")
    s.add_argument("--bg", default=None, help="声明大底 hex(qc 对账用)")
    s.add_argument("--out", default=None, help="检查单输出路径(默认 <page>.loop.md)")
    s.set_defaults(fn=cmd_loop)

    s = sub.add_parser("card")
    s.add_argument("--palette", required=True)
    s.add_argument("--name", default=None)
    s.add_argument("--out", default=None)
    s.set_defaults(fn=cmd_card)

    s = sub.add_parser("export")
    s.add_argument("--palette", required=True)
    s.add_argument("--format", default="css", choices=["css", "tailwind", "json", "svg", "w3c", "context", "prompt"])
    s.set_defaults(fn=cmd_export)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
