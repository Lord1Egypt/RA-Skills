# -*- coding: utf-8 -*-
"""scene_kit.py — showcase 级单场景构建器(scene 命令的实现体)。

把推广 showcase 的场景手艺(设备框/证据徽章/真实内容密度)开放为引擎能力:
scene --kind wallet --theme "Deep Pine" → 独立 HTML,可作实际页面的起点或嵌入块。
含 AI 默认紫守门:大底角色落在紫 hue 域即拒绝(用户令 2026-10-20)。
"""
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_CSS = io_open = None


def _load_css():
    global SCENE_CSS
    if SCENE_CSS is None:
        with open(os.path.join(_HERE, "scene_css.css"), encoding="utf-8") as f:
            SCENE_CSS = f.read()
    return SCENE_CSS


def _hue(h):
    """OKLCH hue(度)。"""
    import colorsys
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360


def purple_guard(hexes, roles_map, force=False):
    """AI 默认紫守门:大底/大面积角色(最浅或最深)落在紫 hue 域(265-330)即拒绝。
    返回 (ok, message)。--force 可越过但会留下记录。"""
    import colorsys
    for h in hexes:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
        hue = hh * 360
        # 紫域窗口 255-330(紫罗兰→品红);高饱和才触发(低饱灰紫不算大面积紫)
        if 255 <= hue <= 330 and ss > 0.30 and 0.10 < ll < 0.85:
            if force:
                return True, f"FORCE: 紫 hue 色 #{h}(hue {hue:.0f})——已记录,质量责任自负"
            return False, (f"AI 默认紫守门:#{h}(hue {hue:.0f})在紫域且高饱和,极可能形成大面积紫。"
                           f"紫渐变/紫大底是 AI 默认审美的头号签名——换板,或 --force 强行越过。")
    return True, ""


def _lum(h):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


KINDS = {
    "wallet": "sc_mobile",
    "landing": "sc_landing",
    "dashboard": "sc_dashboard",
    "branding": "sc_branding",
    "typography": "sc_typography",
    "chart": "sc_chart",
    "ecom": "sc_ecom",
    "email": "sc_email",
    "editorial": "sc_editorial",
    "pattern": "sc_pattern",
}


def css_tokens(hexes, R):
    """色板 → scene_css.css 的令牌取值表(用户令: 模板不得再写死板外色)。
    只从声明板取:_viz_roles 已给 bg/surface/ink/ink2/danger;line=板内次浅色(发丝线),
    ok=板内绿/青域且对底 ≥3:1 的色(板里没有绿系达标色时退 atext —— 那属于"必须扩板",
    最小方案见 references: 给主题记录补 ok 角色)。"""
    import palette_forge as pf
    bg, ink, ink2, surf = R["bg"], R["ink"], R["ink2"], R["surface"]
    cand = [h for h in dict.fromkeys(hexes) if h not in (bg, ink, surf, R["accent"], R["danger"])]
    line = min(cand, key=lambda h: -pf.oklch_from_hex(h)[0]) if cand else surf
    ok = None
    for h in sorted(cand, key=lambda h: -pf.contrast_ratio(h, bg)):
        _L, _C, _H = pf.oklch_from_hex(h)
        if 80 <= _H <= 190 and _C >= 0.04 and pf.contrast_ratio(h, bg) >= 3.0:
            ok = h
            break
    for k in ("muted", "disabled"):
        if not R.get(k):
            raise ValueError("assert_weak_roles_present: 色板推导缺角色 %s"
                             "(_viz_roles 未含 A2 弱声部)——拒绝产出" % k)
    toks = {"__BG__": bg, "__SURF__": surf, "__INK__": ink, "__INK2__": ink2,
            "__LINE__": line, "__DANGER__": R["danger"], "__OK__": ok or R["atext"],
            "__MUTED__": R["muted"], "__DISABLED__": R["disabled"]}
    assert_weak_voice_floor(pf, R, toks)
    return toks


def assert_weak_voice_floor(pf, R, toks):
    """弱声部落地闸: muted/disabled 对它可能落的每一面(大底 bg 与卡面 surface)都必须 >=3:1
    (WCAG 1.4.11 非文字口径)。不达标直接 raise, 不静默放过、不回落硬编码灰。"""
    for tok, role in (("__MUTED__", "muted"), ("__DISABLED__", "disabled")):
        for face in ("bg", "surface"):
            r = pf.contrast_ratio(toks[tok], R[face])
            if r < 3.0:
                raise ValueError("assert_weak_voice_floor: %s(#%s) 对 %s(#%s) 只有 %.2f:1"
                                 " (<3:1), 拒绝产出" % (role, toks[tok], face, R[face], r))


def css_raw_tokens(R, shadow=True):
    """非 hex 令牌(投影)单独一张表 —— 不进声明板、不进 tokens 元信息(它不是颜色)。
    取值从板内派生,不写死 rgba(0,0,0,):palette_forge 自陈 ink2 = secondary details and
    shadows,且明令 AVOID pure black shadows。
      shadow=True  亮底: 用 ink 的 rgb 做半透明投影; 暗底: 大底沿 OKLCH 压暗两档再取 rgb。
      shadow=False 关闭投影: 取值 none —— 同样把占位符吃掉, 不留 __SH__。
    """
    import palette_forge as pf
    if not shadow:
        return {"__SH__": "none"}
    if R.get("dark"):
        L, C, H = pf.oklch_from_hex(R["bg"])
        L2 = max(0.02, L - 0.22)
        base = pf.hex_from_oklch(L2, pf.gamut_fit(L2, C * 0.6, H), H)
        a = ".45"
    else:
        base = R["ink"]
        a = ".18"
    rr, gg, bb = (int(base[i:i + 2], 16) for i in (0, 2, 4))
    depth = "0 24px 60px rgba(%d,%d,%d,%s)" % (rr, gg, bb, a)
    assert not (rr == 0 and gg == 0 and bb == 0), "投影色不许是纯黑"
    return {"__SH__": depth}


def _fill_css(css, toks, raw=None):
    """令牌取值: 色令牌补 #, 非 hex 令牌(raw, 如 __SH__)按原样填。
    未知/未映射令牌一律 raise, 零豁免 —— 旧版把 __SH__ 从残留断言里排除,
    等于放行 11 个占位符漏进产物。
    """
    for k, v in toks.items():
        css = css.replace(k, "#" + v)
    for k, v in (raw or {}).items():
        css = css.replace(k, v)
    left = sorted(set(re.findall(r"__[A-Z0-9_]+__", css)))
    if left:
        raise ValueError("scene_css.css 出现未映射令牌,拒绝产出: " + ", ".join(left))
    return css

def build_scene(kind, hexes, name, dark=False, force=False, shadow=True):
    """kind + 色板 → (html, declared_palette)。紫守门不过则抛 ValueError。shadow=False 关闭投影:__SH__ → none,不留占位符。"""
    import _showcase_scenes as ss
    kind = kind.lower().strip()
    if kind not in KINDS:
        raise ValueError(f"未知场景类型: {kind}——可选: {', '.join(KINDS)}")
    hexes = [h.upper().lstrip("#") for h in hexes]
    ok, msg = purple_guard(hexes, None, force=force)
    if not ok:
        raise ValueError(msg)
    p = {"hexes": hexes, "theme": "dark" if dark else "light", "name": name}
    R = ss.roles(p)
    inner = getattr(ss, KINDS[kind])(R)
    badges = ss.badge(R)
    toks = css_tokens(hexes, R)
    css = _fill_css(_load_css(), toks, css_raw_tokens(R, shadow=shadow))
    board = sorted(set(hexes) | set(toks.values()))
    meta = ('<meta name="aesthete-palette" content="%s">'
            '<meta name="aesthete-tokens" content="%s">' % (
                ",".join(board),
                ",".join("%s=%s" % (k.strip("_").lower(), v) for k, v in sorted(toks.items()))))
    html = (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        f"<title>scene · {kind} · {name}</title>\n" + meta + "<style>\n"
        "body{margin:0;padding:34px 20px;display:flex;justify-content:center;"
        "font-family:system-ui,sans-serif}\n"
        + css +
        "\n</style>\n</head>\n<body>\n"
        "<div class='stage' style=\"border-radius:24px;padding:56px 40px;display:flex;"
        "justify-content:center;align-items:center;min-height:420px\">\n"
        + inner + "\n" + badges + "\n</div>\n</body>\n</html>\n"
    )
    declared = ",".join(sorted(set(hexes) | set(toks.values())))
    return html, declared
