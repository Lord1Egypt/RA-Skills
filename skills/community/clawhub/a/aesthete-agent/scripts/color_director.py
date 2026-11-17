#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""color_director.py — 色彩导演:整页配色的机械度量 v1(2026-10-20 colorlab 渲染验证版)

与 palette_forge 的"亮度会计"(contrast/score/slop:防丑闸)互补,这里度量
"色彩如何在整页上讲故事":温度旅程 / 饱和度曲线 / 面积×饱和预算 / 张力配额 /
邻接振动 / 冷暖焦点 / 主色戏份档位。全部判据为可判定谓词。

输入模型:页面 = 按阅读顺序的分区清单
  zones = [(hex, area_share), ...]        # area_share 合计 = 1
  acts  = [[(hex, share), ...], ...]      # 可选:分幕(滚动旅程的温度按幕计)
  focal = (focus_hex, container_hex)      # 可选:焦点色与其紧邻容器色

温度轴(文档化约定,整层唯一约定):暖极 = OKLCH H 45°(橙),冷极 = 225°(青蓝)。
  t(H) = cos(H − 45°);|t| ≤ 0.30 为中性带(黄绿 118°-162° / 紫红 273°-333° 过渡区)。
  饱和度权重 min(1, C/0.08):近灰场的色相不驱动页面温度。
stdlib-only;OKLCH 公式与 palette_forge 同源(Ottosson,公有领域)。
"""
import argparse
import json
import math
import sys


# ------------------------------------------------- OKLCH core(同 palette_forge)
def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x


def parse_hex(s):
    s = str(s).strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"bad hex: {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def oklch_from_hex(h):
    r, g, b = (srgb_to_linear(c / 255) for c in parse_hex(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


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


def hex_from_oklch(L, C, H):
    rad = math.radians(H)
    a, b = C * math.cos(rad), C * math.sin(rad)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    rgb = (
        clamp(4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s),
        clamp(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s),
        clamp(-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s),
    )
    def lin(c):
        return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return "%02X%02X%02X" % tuple(int(round(lin(c) * 255)) for c in rgb)


def rel_luminance(h):
    r, g, b = (srgb_to_linear(c / 255) for c in parse_hex(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    l1, l2 = sorted((rel_luminance(a), rel_luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# ------------------------------------------------- 度量原语
def t_hue(H):
    """色相温度:t = cos(H-45°)。+1 暖极(45° 橙),-1 冷极(225° 青蓝)。"""
    return math.cos(math.radians(H - 45.0))


def temp_index(L, C, H):
    """分区温度指数:色相温度 × 饱和度权重(近灰不动温度)。"""
    return t_hue(H) * min(1.0, C / 0.08)


def is_loud(L, C):
    """响亮区:C 与 L 双高——正在"说话"的颜色。"""
    return C > 0.13 and 0.45 <= L <= 0.88


def hue_dist(h1, h2):
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


def zone_temp(z):
    _, share = z
    L, C, H = oklch_from_hex(z[0])
    return temp_index(L, C, H) * share


# ------------------------------------------------- 规则 R1:大底纯洁令
def rule_big_field(zones, bold=False):
    """share≥20% 的分区:
    脏色带 = C∈(0.04,0.105] ∧ L∈(0.45,0.75) —— 任何语域都禁(脏色禁大底的量化版);
    高饱中明带 = C>0.105 ∧ L∈(0.35,0.85) —— 仅强语域(bold)可作大底。"""
    bad = []
    for h, share in zones:
        if share < 0.20:
            continue
        L, C, _ = oklch_from_hex(h)
        if 0.04 < C <= 0.105 and 0.45 < L < 0.75:
            bad.append(f"#{h} 脏色大底 占{share*100:.0f}% (L={L:.2f} C={C:.3f})")
        elif not bold and C > 0.105 and 0.35 < L < 0.85:
            bad.append(f"#{h} 高饱中明大底占{share*100:.0f}% (L={L:.2f} C={C:.3f},仅强语域)")
    return (not bad,
            "; ".join(bad) if bad else "所有 ≥20% 分区均不在脏色带/高饱中明带",
            "脏色带(中明中饱)直接换色:向浅推到 L≥0.85 或向深压到 L≤0.45 并降饱和")


# ------------------------------------------------- 规则 R2:面积×饱和预算(Itten 面积对比的剂量化)
def rule_area_chroma(zones, bold=False, cap=None):
    # 阈值经 11 块验收板校准:标准板 0.006-0.035,强暖/庆典板 0.044-0.061;
    # declarative(品牌即色彩整面版)是声明式例外,显式给 cap
    if cap is None:
        cap = 0.065 if bold else 0.035
    total = sum(share * oklch_from_hex(h)[1] for h, share in zones)
    ok = total <= cap
    return ok, f"Σ面积×C = {total:.4f} (上限 {cap})", \
        "超预算:削最大响亮区的面积,或给该色降饱和——二者选一,不是都调一半"


# ------------------------------------------------- 规则 R3:饱和度曲线(响亮"声部"的合法数量)
def rule_sat_curve(zones, bold=False, last_act_loud=None):
    """响亮区 = C>0.13 且 L∈[0.45,0.88]。按色相族(ΔH<35°)合并成『声部』:
    同一族色反复出现 = 一个声音在呼应(合法);不同族各喊各的 = 嘈杂。"""
    infos = [(oklch_from_hex(h), share, h) for h, share in zones]
    loud_hexes, loud_share = [], 0.0
    for (L, C, H), share, h in infos:
        if is_loud(L, C):
            loud_hexes.append((H, h))
            loud_share += share
    quiet_share = sum(sh for (L, C, _), sh, _ in infos if C < 0.05)
    # 色相族合并
    fams = []
    for H, h in loud_hexes:
        for f in fams:
            if hue_dist(H, f[0]) < 35:
                f[1].append(h)
                break
        else:
            fams.append([H, [h]])
    n_voices = len(fams)
    min_pair = min((hue_dist(a[0], b[0]) for i, a in enumerate(fams)
                    for b in fams[i+1:]), default=360)
    if n_voices == 0:
        return True, f"quiet-plateau:响亮声部 0,静场 {quiet_share*100:.0f}%", ""
    if bold:
        if loud_share <= 0.45 and n_voices <= 3 and min_pair >= 60:
            return True, (f"bipolar(强语域):响亮占比 {loud_share*100:.0f}%,"
                          f"{n_voices} 声部,最小族距 {min_pair:.0f}°"), ""
        return False, (f"响亮占比 {loud_share*100:.0f}% / {n_voices} 声部 / 最小族距 {min_pair:.0f}° "
                       f"(要求 ≤45% / ≤3 声部 / 两两 ≥60°)"), "删一组响亮区或拉开族距"
    if n_voices == 1 and loud_share <= 0.25 and (quiet_share >= 0.55 or last_act_loud):
        kind = "quiet-peak(静场单峰)" if quiet_share >= 0.55 else "crescendo(渐强收束)"
        return True, (f"{kind}:1 声部 {loud_share*100:.0f}%,"
                      f"静场 {quiet_share*100:.0f}%"), ""
    if n_voices >= 2:
        return False, (f"scattered:响亮区 {n_voices} 声部散布全页(占比 {loud_share*100:.0f}%)"
                       f"——视线被劈成 {n_voices} 份"), "并入一族,或除保留族外全部降饱和至 C≤0.10"
    if loud_share > 0.25:
        return False, f"单声部占比 {loud_share*100:.0f}% >25%——响亮色成面即成墙", "缩小到 ≤25% 或降饱和"
    return False, (f"flood:响亮占比 {loud_share*100:.0f}% 且静场仅 {quiet_share*100:.0f}%",
                   "把大底换成低饱和同相色")


# ------------------------------------------------- 规则 R4:温度旅程(幕序列,冷热只许转一次弯)
def rule_temp_journey(acts):
    temps = []
    for act in acts:
        tot = sum(sh for _, sh in act)
        t = sum(zone_temp(z) for z in act) / max(tot, 1e-9)
        temps.append(t)
    seq = [t for t in temps if abs(t) >= 0.08]          # 中性幕不参与转向计数
    reversals = sum(1 for i in range(1, len(seq))
                    if seq[i] * seq[i - 1] < 0)
    if reversals >= 2:
        dir_word = "乱窜"
    elif not seq:
        dir_word = "全中性"
    else:
        dir_word = "单调变暖" if seq[-1] > seq[0] else "单调变冷"
    ok = reversals <= 1
    ev = " → ".join(f"{t:+.2f}" for t in temps) + f" | 转向 {reversals} 次({dir_word})"
    return ok, ev, "冷热各说各话=页面没有气候;法定旅程:单调(0 转向)或 V 形(1 转向)"


# ------------------------------------------------- 规则 R5:张力配额(互补/分裂互补只给焦点)
def rule_tension_quota(zones, bold=False):
    cap = 3 if bold else 2
    seen, chroma = set(), []
    for h, _sh in zones:
        if h in seen:
            continue
        seen.add(h)
        L, C, H = oklch_from_hex(h)
        if C >= 0.08:
            chroma.append((h, H))
    pairs = []
    for i, (ha, Ha) in enumerate(chroma):
        for hb, Hb in chroma[i+1:]:
            d = hue_dist(Ha, Hb)
            if 100 <= d <= 260:
                pairs.append((ha, hb, d))
    ok = len(pairs) <= cap
    ev = "; ".join(f"#{a}×#{b} {d:.0f}°" for a, b, d in pairs) or "无跨族对"
    return ok, f"张力对 {len(pairs)}/{cap}: {ev}", \
        "互补/近补色差是整页最贵的张力,一页只花一两次;其余分区收进 ±60° 同相族"


# ------------------------------------------------- 规则 R6:邻接振动(同时对比的剂量规则)
def rule_vibration(zones):
    """两个高饱和分区直接相邻且色相相近不相同的(8°≤ΔH<35°)、明度接近的(ΔL<0.20),
    边界发生同时对比振动。同色相邻(ΔH<8°)算一个声部,不振动。"""
    bad = []
    for (ha, sa), (hb, sb) in zip(zones, zones[1:]):
        La, Ca, Ha = oklch_from_hex(ha)
        Lb, Cb, Hb = oklch_from_hex(hb)
        d = hue_dist(Ha, Hb)
        if Ca >= 0.12 and Cb >= 0.12 and 8 <= d < 35 and abs(La - Lb) < 0.20:
            bad.append(f"#{ha}紧贴#{hb} (ΔH {d:.0f}° ΔL {abs(La-Lb):.2f})")
    return (not bad,
            "; ".join(bad) if bad else "无高饱和近相同明度紧贴对",
            "修法二择一:中间插一条 C≤0.03 中性缓冲带;或强制 ΔL≥0.25 让明度接管边界")


# ------------------------------------------------- 规则 R7:冷暖焦点
def rule_focal_temp(focal):
    if not focal:
        return True, "未声明焦点(跳过)", ""
    (fh, ch) = focal
    Lf, Cf, Hf = oklch_from_hex(fh)
    Lc, Cc, Hc = oklch_from_hex(ch)
    tf, tc = temp_index(Lf, Cf, Hf), temp_index(Lc, Cc, Hc)
    cr = contrast_ratio(fh, ch)
    if abs(tc) < 0.15:                                   # 容器中性
        ok = abs(tf) >= 0.35 and cr >= 3.0
        return ok, f"中性容器:焦点 t={tf:+.2f} 对比 {cr:.1f}:1", \
            "中性底上焦点要有明确温度且图形对比 ≥3:1"
    ok = (tf * tc < 0) and abs(tf - tc) >= 0.5 and cr >= 3.0
    return ok, f"焦点 t={tf:+.2f} / 容器 t={tc:+.2f} 对比 {cr:.1f}:1", \
        "张力从温度来,不从明度来:焦点与容器异号且温差 ≥0.5"


# ------------------------------------------------- 规则 R8:主色戏份三档(色板气质 → 决策)
def drama_tier(hexes, dark_bg=None):
    """板气质 → 档位。暗幕霓虹特例:accent 亮(L≥0.72)高饱(C≥0.13)且底深(≤0.35)
    时,明度对比放大小面积——戏份上限按 ≤10% 计,不适用 A 档。"""
    Cs = [oklch_from_hex(h)[1] for h in hexes]
    Ls = [oklch_from_hex(h)[0] for h in hexes]
    cmax, cmean = max(Cs), sum(Cs) / len(Cs)
    acc = max(hexes, key=lambda h: oklch_from_hex(h)[1])
    aL, aC, _ = oklch_from_hex(acc)
    if dark_bg is None:
        dark_bg = min(Ls) <= 0.35
    if dark_bg and aL >= 0.72 and aC >= 0.13:
        return ("暗幕霓虹", "亮高饱 accent 在深底上被明度对比放大,占面 ≤10%,只给字形/细线/焦点",
                cmax, cmean)
    if cmax >= 0.15 and cmean >= 0.08:
        return ("A 品牌即色彩", "accent 可拥有一整块 20-40% 的场(整段 hero/整面封底)", cmax, cmean)
    if cmax >= 0.08:
        return ("B 点睛", "accent ≤12%,只给 CTA/链接/数据强调,稀缺即力量", cmax, cmean)
    return ("C 线与字", "低饱 chroma 合计 ≤15%(渲染实证:细条+KPI+引文幕 15% 成立),层次交给墨阶", cmax, cmean)


def rule_drama(hexes, accent_share, dark_bg=None, bold=False):
    """R8 主色戏份(0.19):accent 档位定 cap——强语域 A 品牌即色彩 15-45%/暗幕霓虹 ≤10%/
    B 点睛 ≤12%/C 线与字 ≤15%(0.20 渲染实证);品牌页准入:深暗(L≤0.45)或极浅(L≥0.90)且 C≤0.12 → 15-45% 大域。
    ⚠️0.19 研究课题:C 线与字 4% cap 与 Deep Pine 10% accent 已验证设计矛盾,已裁决:cap 0.15(2026-11-18 drama 实验)。"""
    tier, policy, cmax, cmean = drama_tier(hexes, dark_bg)
    if tier.startswith("暗幕霓虹"):
        ok = accent_share <= 0.10
    elif tier.startswith("A"):
        ok = 0.15 <= accent_share <= 0.45
    elif tier.startswith("B"):
        ok = accent_share <= 0.12
    else:
        # C 线与字档(低饱板):cap 0.04→0.15(0.20 渲染实验 drama-3/8/15 目审:
        # 8% 细条+KPI 清晰不抢戏,15% 引文幕"安静而不缺席"成立;>15% 强调成墙)
        ok = accent_share <= 0.15
    if not ok and bold and not tier.startswith("暗幕霓虹") and not tier.startswith("A"):
        acc = max(hexes, key=lambda h: oklch_from_hex(h)[1])
        aL, aC, _ = oklch_from_hex(acc)
        if (aL <= 0.45 or aL >= 0.90) and aC <= 0.12 and 0.15 <= accent_share <= 0.45:
            ok = True
            tier = tier + "+准入"
    lines = [f"板气质 Cmax={cmax:.2f} Cmean={cmean:.3f} → {tier};实际 accent 占面 {accent_share*100:.0f}%",
             policy]
    return ok, lines


def _norm(zones):
    return [(str(h).strip().lstrip("#").upper(), s) for h, s in zones]


def analyze(name, zones, acts=None, focal=None, bold=False, last_act_loud=None,
            accent_share=None, palette=None, cap=None, only=None):
    zones = _norm(zones)
    acts = [_norm(a) for a in acts] if acts else None
    focal = (focal[0].strip().lstrip("#").upper(), focal[1].strip().lstrip("#").upper()) if focal else None
    out = {"page": name, "findings": []}

    def add(rule, ok, ev, fix=""):
        if only and rule not in only:
            return
        out["findings"].append({"rule": rule, "verdict": "PASS" if ok else "FAIL",
                                "evidence": ev, "fix": fix})

    add("R1 大底纯洁", *rule_big_field(zones, bold))
    add("R2 面积×饱和预算", *rule_area_chroma(zones, bold, cap))
    add("R3 饱和度曲线", *rule_sat_curve(zones, bold, last_act_loud))
    if acts:
        add("R4 温度旅程", *rule_temp_journey(acts))
    add("R5 张力配额", *rule_tension_quota(zones, bold))
    add("R6 邻接振动", *rule_vibration(zones))
    if focal:
        add("R7 冷暖焦点", *rule_focal_temp(focal))
    if palette and accent_share is not None:
        add("R8 主色戏份", *rule_drama([p.strip().lstrip("#").upper() for p in palette],
                                       accent_share, bold=bold))
    out["verdict"] = "PASS" if all(f["verdict"] == "PASS" for f in out["findings"]) else "FAIL"
    return out


def _parse_zones(s):
    zones = []
    for part in s.split(","):
        h, sh = part.strip().split(":")
        zones.append((h.strip().lstrip("#").upper(), float(sh)))
    return zones


def main():
    ap = argparse.ArgumentParser(description="色彩导演:整页配色机械度量")
    ap.add_argument("--manifest", help="lab_zones.json 批量裁决")
    ap.add_argument("--zones", help="单页快判: hex:share,hex:share,...")
    ap.add_argument("--bold", action="store_true")
    args = ap.parse_args()
    if args.manifest:
        cases = json.load(open(args.manifest, encoding="utf-8"))
    else:
        cases = [{"page": "cli", "zones": _parse_zones(args.zones), "bold": args.bold}]
    n_pass = 0
    for c in cases:
        res = analyze(c["page"], [tuple(z) for z in c["zones"]],
                      acts=[list(map(tuple, a)) for a in c.get("acts")] if c.get("acts") else None,
                      focal=tuple(c["focal"]) if c.get("focal") else None,
                      bold=c.get("bold", False),
                      last_act_loud=c.get("last_act_loud"),
                      accent_share=c.get("accent_share"),
                      palette=c.get("palette"),
                      cap=c.get("cap"),
                      only=c.get("only"))
        print(f"\n== {res['page']} → {res['verdict']}")
        for f in res["findings"]:
            mark = "PASS" if f["verdict"] == "PASS" else "FAIL"
            print(f"  [{mark}] {f['rule']}: {f['evidence']}")
            if f["verdict"] == "FAIL" and f["fix"]:
                print(f"         ↳ {f['fix']}")
        n_pass += res["verdict"] == "PASS"
    print(f"\n{n_pass}/{len(cases)} 页 PASS")
    sys.exit(0 if n_pass == len(cases) else 1)


if __name__ == "__main__":
    main()
