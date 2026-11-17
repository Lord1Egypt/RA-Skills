# -*- coding: utf-8 -*-
"""token_sheet.py — tokens 命令实现体:色板 → 全套语义设计令牌(CSS + JSON)。

在 scaffold_kit 的角色派生(自动调墨)之上补工程语义层:
  色 token 带明暗双幕(bg/ink 与 night/on-night 交叉成对,页面可混排明暗幕) +
  --accent(图形用)与 --accent-ink(文字用)分离——强调色直接做正文是常见翻车点,
  不达标自动爬坡调墨并给出达标值;字阶/间距/圆角/动效 token 一并发出。
tokens.json 记录全部实测对比度 + 指纹互锁(sha256 输入+裁决),验收可对账。
零依赖(纯 stdlib),被 palette_forge.py 的 cmd_tokens 调用。
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scaffold_kit import derive, _contrast, _mix  # noqa: E402

SPACE_SCALE = [4, 8, 12, 16, 24, 32, 48, 64, 96, 128]
RADII = [("sm", 8), ("md", 12), ("lg", 16), ("xl", 24)]
MOTION = [("dur-1", "150ms"), ("dur-2", "300ms"), ("dur-3", "600ms"),
          ("ease-out", "cubic-bezier(.2,.6,.2,1)")]
FONTS = [
    ("font-serif", "'Noto Serif SC','Source Han Serif SC','Songti SC',Georgia,serif"),
    ("font-sans", "-apple-system,'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif"),
    ("font-mono", "ui-monospace,'SF Mono',Consolas,'JetBrains Mono',monospace"),
]


def scale12(hexes):
    """五色 → 12 步语义阶(Radix 式):1 最浅…12 最深,浅暗双模式共用语义。
    色板色按亮度秩映射到对应档,再向目标亮度微调(与白/黑混合)。"""
    uniq = []
    for h in hexes:
        h = h.upper().lstrip("#")
        if len(h) == 6 and h not in uniq:
            uniq.append(h)

    def lum(h):
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def tint(h, k):
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return "".join(f"{round(v + (255 - v) * k):02X}" for v in (r, g, b))

    def shade(h, k):
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return "".join(f"{round(v * (1 - k)):02X}" for v in (r, g, b))

    ranked = sorted(uniq, key=lum)                     # 浅→深
    n = len(ranked)
    steps = {}
    for i in range(1, 13):
        tpos = (i - 1) / 11
        idx = min(n - 1, round(tpos * (n - 1)))
        base = ranked[idx]
        target = 0.97 - (i - 1) * 0.76 / 11
        h = base
        for _ in range(8):
            cur = lum(h)
            diff = target - cur
            if abs(diff) < 0.02:
                break
            h = tint(h, 0.25) if diff > 0 else shade(h, 0.25)
        steps[i] = h.upper()
    return steps


def _tune_text(hex_fg, hex_bg, need=4.5):
    """把前景调到达标:按明度关系选向黑压或向白提,逐级混合,返回(达标色, 实测比)。"""
    r = _contrast(hex_fg, hex_bg)
    if r >= need:
        return hex_fg, r
    toward = "000000" if _lum(hex_fg) <= _lum(hex_bg) else "FFFFFF"
    for k in range(1, 21):
        cand = _mix(hex_fg, toward, k / 20.0)
        r = _contrast(cand, hex_bg)
        if r >= need:
            return cand, r
    return hex_fg, r


def _lum(h):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _ratio(t):
    return "%.2f" % t if t < 10 else "%.1f" % t


def build_tokens(hexes, name="", brand="", dark=False):
    """色板 → (tokens dict, ratios dict, problems list)。全部墨色自动调墨到位。"""
    d = derive({"hexes": hexes}, brand or name or "Brand", "", "")
    night, pale = d["NIGHT"], d["PALE"]
    card, ink2, mist = d["CARD"], d["INK2"], d["MIST"]
    accent, line = d["ACCENT"], d["LINE"]
    surface = d["SURFACE"]

    if dark:
        bg = night
        bg_raised = _mix(night, "FFFFFF", 0.07)
        ink = pale
        ink_muted = mist
        line_c = _mix(night, "FFFFFF", 0.14)
        paper, on_paper = pale, night
    else:
        bg = pale
        bg_raised = card
        ink = night
        ink_muted = ink2
        line_c = line
        paper, on_paper = night, pale

    ink, r_ink = _tune_text(ink, bg, 4.5)
    ink_muted = _tune_text(ink_muted, bg, 4.5)[0]
    ink_muted = _tune_text(ink_muted, bg_raised, 4.5)[0]
    on_paper = _tune_text(on_paper, paper, 4.5)[0]
    accent_ink, r_acc = _tune_text(accent, bg, 4.5)
    on_night = pale
    on_night_muted = mist

    t = {
        "bg": bg, "bg_raised": bg_raised, "ink": ink, "ink_muted": ink_muted,
        "line": line_c, "accent": accent, "accent_ink": accent_ink,
        "accent_soft": _mix(accent, bg, 0.78),
        "night": night, "on_night": on_night, "on_night_muted": on_night_muted,
        "surface": surface, "paper": paper, "on_paper": on_paper,
    }
    ratios = {
        "ink/bg": _contrast(t["ink"], t["bg"]),
        "ink_muted/bg": _contrast(t["ink_muted"], t["bg"]),
        "ink_muted/bg_raised": _contrast(t["ink_muted"], t["bg_raised"]),
        "on_paper/paper": _contrast(t["on_paper"], t["paper"]),
        "on_night/night": _contrast(t["on_night"], t["night"]),
        "on_night_muted/night": _contrast(t["on_night_muted"], t["night"]),
        "accent_ink/bg": _contrast(t["accent_ink"], t["bg"]),
        "accent/bg(图形≥3)": _contrast(t["accent"], t["bg"]),
    }
    problems = []
    for k in ("ink/bg", "ink_muted/bg", "ink_muted/bg_raised",
              "on_paper/paper", "on_night/night", "on_night_muted/night", "accent_ink/bg"):
        if ratios[k] < 4.5:
            problems.append(f"{k} = {ratios[k]:.2f} < 4.5")
    return t, ratios, problems


def emit(hexes, name="", brand="", dark=False, out_base="tokens"):
    """生成 tokens.css + tokens.json;返回(dict 摘要, 退出码)。"""
    t, ratios, problems = build_tokens(hexes, name, brand, dark)
    verdict = "PASS" if not problems else "FAIL"

    def c(k):
        return "#" + t[k]

    lines = [
        "/* %s — aesthete-agent tokens(0.9.0)" % (name or "palette"),
        "   色板: " + " ".join("#" + h.upper() for h in hexes),
        "   模式: %s · 裁决 %s" % ("dark-primary" if dark else "light-primary", verdict),
        "   墨色已按对比度自动调墨;数值注释为 WCAG 实测比。*/",
        ":root{",
    ]
    rows = [
        ("--bg", t["bg"], "大底(与 --ink %s:1)" % _ratio(ratios["ink/bg"])),
        ("--bg-raised", t["bg_raised"], "卡片面(次字 %s:1)" % _ratio(ratios["ink_muted/bg_raised"])),
        ("--ink", t["ink"], "主字(%s:1)" % _ratio(ratios["ink/bg"])),
        ("--ink-muted", t["ink_muted"], "次字/说明(%s:1)" % _ratio(ratios["ink_muted/bg"])),
        ("--line", t["line"], "发丝线/分隔"),
        ("--accent", t["accent"],
         "强调·图形/色块(图形比 %s:1)%s" % (
             _ratio(ratios["accent/bg(图形≥3)"]),
             ";做正文请用 --accent-ink" if ratios["accent_ink/bg"] > ratios["accent/bg(图形≥3)"] else "")),
        ("--accent-ink", t["accent_ink"], "强调·文字(%s:1)" % _ratio(ratios["accent_ink/bg"])),
        ("--accent-soft", t["accent_soft"], "强调柔态:标签底/hover 面"),
        ("--night", t["night"], "暗幕大底(明暗旅程的暗段)"),
        ("--on-night", t["on_night"], "暗幕主字(%s:1)" % _ratio(ratios["on_night/night"])),
        ("--on-night-muted", t["on_night_muted"], "暗幕次字(%s:1)" % _ratio(ratios["on_night_muted/night"])),
        ("--paper", t["paper"], "反幕大底(暗页中的亮节)"),
        ("--on-paper", t["on_paper"], "反幕主字(%s:1)" % _ratio(ratios["on_paper/paper"])),
    ]
    lines += ["  %s:#%s;  /* %s */" % (k, v, note) for k, v, note in rows]
    for k, v in FONTS:
        lines.append("  --%s:%s;" % (k, v))
    for i, s in enumerate(SPACE_SCALE, 1):
        lines.append("  --s%d:%dpx;" % (i, s))
    for suf, v in RADII:
        lines.append("  --r-%s:%dpx;" % (suf, v))
    for k, v in MOTION:
        lines.append("  --%s:%s;" % (k, v))
    lines += [
        "}",
        "/* 用法:明暗幕成对使用——暗段容器底 var(--night) 字 var(--on-night);",
        "   减动效:@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}} */",
    ]
    css = "\n".join(lines) + "\n"

    payload = {
        "name": name, "brand": brand, "dark_primary": bool(dark),
        "palette": [h.upper() for h in hexes],
        "tokens": {k: "#" + v for k, v in t.items()},
        "ratios": ratios, "problems": problems, "verdict": verdict,
    }
    payload["fingerprint"] = hashlib.sha256(
        ("aesthete-tokens/v1|" + ",".join(h.upper() for h in sorted(hexes)) +
         ("|dark" if dark else "|light") + "|" + verdict).encode("utf-8")).hexdigest()

    with open(out_base + ".css", "w", encoding="utf-8", newline="\n") as f:
        f.write(css)
    # 12 步语义阶(Radix 式):五色全阶映射,浅暗双模式共用语义
    try:
        steps12 = scale12([h.lstrip("#").upper() for h in hexes])
        sem = ["app-bg", "sub-bg", "el-bg", "el-hover", "el-active", "border",
               "border-strong", "solid", "solid-hover", "text-low", "text-high", "ink-deep"]
        payload["scale12"] = {sem[i - 1]: steps12.get(i) for i in range(1, 13)}
        block = "\n/* 12 步语义阶(浅暗双模式共用语义) */\n:root{\n"
        for i, name in enumerate(sem, 1):
            block += f"  --step-{i:02d}-{name}: #{steps12.get(i, 'CCCCCC')};\n"
        block += "}\n"
        css = css + block
        with open(out_base + ".css", "w", encoding="utf-8", newline="\n") as f2:
            f2.write(css)
    except Exception:
        payload["scale12"] = {}
    with open(out_base + ".json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    return payload, (0 if verdict == "PASS" else 1)
