#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_page.py — HTML 交付前的静态审计(机制,非散文)。

检查:
  1. 色板漂移   — 页面实际使用的颜色 vs 声明色板(未声明的"私货色"逐个点名)。
      声明板来源(缺省顺序): 1) --palette 显式给; 2) 缺省 -> 读被检 HTML 的 meta 板声明
        name="aesthete-palette" content="RRGGBB,..."(引擎产物自带,scene_kit/scaffold_kit 注入);
        两者都没有 -> 记 1 条 P1(声明板未知,漂移闸无法执法),其余字号/渐变/黑名单/emoji 闸照常判。
      定级: 板外非近中性色 >=2 种 = P0(整套自造色阶 = 绕板,不是个别遗漏);恰好 1 种 = P1
        (0.24 裁决:AE-N2 默认严之后 P2 永不进 rc = 私货色永久后门,故由 AE-B 的临时 P2 升回 P1;
         测试方实测当前树 scaffold 板外 0 种、scene 板外 1 种属近中性,升 P1 零新增红)。
      近中性判据见 chromatic() 注释:三条闸可复算;后续要更严只许调小阈值(判据只收紧不放松)。
  2. 黑名单族   — profile.json 的 banned hex 家族(中位数陷阱)
  3. 字号下限   — CSS 中的 px 字号低于 --floor 即点名(投影件建议 24-34)。
      AE-FONTGHOST(0.24):未被本页 DOM 命中的规则(幽灵规则,如 scene_css 全量内联进
      别场景的 .wall 规则)静态降级 P2 并打印覆盖面——静态闸只对"真会渲染的声明"执法,
      真判红交给渲染级 computed style(渲染闸才看得到 DOM)。
  4. 渐变剂量   — linear/radial/conic 渐变出现即 P0(审美铁律: 禁渐变, 纯色分层替代)
  5. emoji      — 出现 emoji 计 P2(除非品牌系统使用)
  6. --render evidence.json — 渲染级证据(render_probe.js 采集):主题 vs 档案、
     强调色剂量(areaRatio vs accent_max)、实测最小字号、最差对比对;
     缺 evidence 时剂量闸显式 [SKIP](点名未测什么、怎么补),绝不静默(AE-N3)。

裁决:P0 存在或 P1>=1 即 exit 1(0.24 默认严;--lenient 过渡口径 P1>=2 ——
AE-N2 裁决(2026-11-18):旧 n_p1>=2 把"恰好 1 条 P1"永久吞成 rc=0,闸有牙被退出码口径阉掉;
同族 qc_kit 本就 n_p1>=1)。
纯 stdlib,无浏览器依赖;render_probe.js 由会话浏览器工具执行(见 SKILL 第 6 步闸门链)。
"""
import argparse
import json
import math
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PROFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "profile.json")
HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGB_RE = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")
FONT_RE = re.compile(r"font-size:\s*(\d+(?:\.\d+)?)px|font:\s*(?:(?:italic|oblique)\s+)?(?:bold\s+|bolder\s+|lighter\s+|[1-9]00\s+)?(?:[\d.]+\s*/\s*[\d.]+\s+)?(\d+(?:\.\d+)?)px")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2700-\u27BF\u2600-\u26FF]")

# -- 近中性判据(AE-B ③ / AE-NEUTRAL,可复算,零依赖) ---------------------------------
# 旧口径只有一条 `max-min < 30`(8-bit 跨度,无出处、无文档),它同时漏掉两类私货色:
#   深色带: #1B2233 跨度 24(<30 被豁免)但 HSV S_v=0.47、OKLab C*=0.034 —— 视觉上是一块有色相的墨;
#   浅中调带: #7F8C8C 跨度 13 被豁免,而它的 CIELAB 色度 abC*=4.97(远高于大平面最小可辨色度 dC*~1-2)。
# 一条线性阈值管不住"色相 x 明度"整个面,所以这里用**三条闸,任一命中即判"有色"(非近中性)**:
#   记 8-bit 通道 R,G,B 属于 [0,255]; C8 = max-min(绝对色度跨度); V = max(HSV 明度)
#   S_v = C8 / V (V=0 即纯黑 => S_v := 0)                                        HSV 饱和度 0..1
#   (L_ok, C_ok) = OKLab(Ottosson) 的明度与彩度 C* = sqrt(a^2 + b^2)             0..~0.4
#   闸1 绝对跨度:   C8 >= NEUTRAL_C8_ABS   (=30, 11.8%)   —— 旧口径原值,**没有调大**(调大=更多豁免)
#   闸2 深色相对:   C8 >= NEUTRAL_C8_MIN 且 S_v >= NEUTRAL_SV_MIN  (=12 且 0.20)
#   闸3 浅中调感知: L_ok >= NEUTRAL_L_MIN 且 C_ok >= NEUTRAL_C_OK  (=0.55 且 0.014)
#   近中性(near-neutral) <=> 三条都不命中
# 阈值出处(都能在 5 行内手算复现):
#   * 30/255 = 11.8%:沿用旧值不放宽 => 判据**单调收紧**,旧口径判"有色"的色这里一律仍判"有色"。
#   * 12/255 = 每通道约正负 4 的抖动带:跨度低于它的深色(纯灰、近黑墨)一律中性,
#     免得 #1E2028(设备框墨, C8=10, S_v=0.25)被闸2 误伤成私货。
#   * 0.20 = HSV 洗色带上界:S_v 低于 20% 是灰/纸/米白族;深板青 #1B2233 的 0.47 稳稳越过。
#   * OKLab C* 0.014:实测换算 = CIELAB 色度 4.6~5.0(本文件自证里逐条打印),即最小可辨色度 dC*~1-2
#     的 2~3 倍 => 不会因轻微去饱和误报;而板外带调灰 #9AA8A0(abC* 6.93)、#9FB3BC(8.52)都在闸内。
#     明度门 0.55 不可省:#1E2028 的 C*(0.0155)与父例 #7F8C8C(0.0151)几乎相同,**只有明度能把
#     "深墨带"与"浅中调带"分开**(L=0.245 对 0.630);深色带靠闸2,浅色带靠闸3,互不越界。
#   * 方向纪律:后续要更严只允许**调小** C_OK / SV_MIN 或调小 L_MIN;调大 = 更多颜色静默豁免 = AE-NEUTRAL 复发。
# 算例(每条可手算): #1E2028 C8=10,L=0.245 => 中性; #1B2233 S_v=0.47 => 有色(闸2);
#   #7F8C8C L=0.630,C*=0.0151 => 有色(闸3); #526871 C8=31 => 有色(闸1,与旧口径同判);
#   #FAF3DD L=0.964,C*=0.0299 => 有色(浅色奶油不再是免死金牌); #E8EEF6 C*=0.0126 => 中性;
#   #E0E6D3(surf,板上) => 有色但板上不入 drift; #222222/#888888/#000000/#FFFFFF C*=0 => 中性。
NEUTRAL_C8_ABS = 30
NEUTRAL_C8_MIN = 12
NEUTRAL_SV_MIN = 0.20
NEUTRAL_L_MIN = 0.55
NEUTRAL_C_OK = 0.014
# 板外非近中性色到这个种数即 P0(2 种起是成体系的自造色阶;1 种在 0.24 由临时 P2 升回 P1,
# 理由见文件头 docstring —— AE-N2 默认严后 P2 永不进 rc,留着就是私货色后门)
OFF_PALETTE_P0_MIN = 2


def _srgb_lin(u):
    """sRGB 8-bit 通道 -> 线性光(Ottosson OKLab 的入参口径)。"""
    c = abs(u / 255.0)
    return 12.92 * c if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def oklab_lc(r, g, b):
    """(OKLab 明度 L, OKLab 彩度 C* = hypot(a,b))。纯 stdlib,矩阵取 Ottosson 原文常数。
    与引擎 palette_forge.oklch_from_hex 同一条公式(测试里按 1e-6 对齐复算)。
    出处:Bjorn Ottosson, "A perceptual color space for image processing"(OKLab, 2020)。
    """
    R, G, B = _srgb_lin(r), _srgb_lin(g), _srgb_lin(b)
    l = (0.4122214708 * R + 0.5363325363 * G + 0.0514459929 * B) ** (1.0 / 3.0)
    m = (0.2119034982 * R + 0.6806995451 * G + 0.1073969566 * B) ** (1.0 / 3.0)
    s = (0.0883024619 * R + 0.2817188376 * G + 0.6299787005 * B) ** (1.0 / 3.0)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            math.hypot(1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                       0.0259040371 * l + 0.7827717662 * m - 0.8086757160 * s))


def chromatic(r, g, b):
    """True = 非近中性(是一块有选择的颜色);False = 近中性/纸系洗色。三条闸见上方判据注释。"""
    mx, mn = max(r, g, b), min(r, g, b)
    c8 = mx - mn
    if c8 >= NEUTRAL_C8_ABS:  # 闸1:绝对跨度(旧口径原值,不放宽)
        return True
    if c8 >= NEUTRAL_C8_MIN and (mx == 0 or c8 / float(mx) >= NEUTRAL_SV_MIN):
        return True  # 闸2:深色带相对饱和度
    L_ok, C_ok = oklab_lc(r, g, b)
    return L_ok >= NEUTRAL_L_MIN and C_ok >= NEUTRAL_C_OK  # 闸3:浅中调带感知彩度


def hex_chromatic(hx):
    """hx: 6 位大写、无 # 的 hex 串。"""
    return chromatic(int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))


def NEUTRAL(r, g, b):
    """近中性判定(保留旧函数名与旧调用点);等价于 not chromatic(r, g, b)。"""
    return not chromatic(r, g, b)


def used_colors(html):
    """收集 <style>/内联样式里声明的颜色(hex 归一 6 位 + rgb 转 hex)。"""
    styles = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))
    styles += " ".join(re.findall(r'style="([^"]+)"', html))
    found = set()
    for m in HEX_RE.finditer(styles):
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        found.add(h.upper())
    for m in RGB_RE.finditer(styles):
        r, g, b = (int(x) for x in m.groups())
        if chromatic(r, g, b):
            found.add("%02X%02X%02X" % (r, g, b))
    return found


def normalize_palette(text):
    """板文本 -> 归一色集(6 位大写、无 #),显式 --palette 与 meta 共用一套口径。
    容错: # 前缀、3 位短写展开、大小写、逗号/分号/空白分隔、去重;非 hex 直接丢弃。"""
    out = set()
    if not text:
        return out
    flat = str(text).replace("#", ",").replace(";", ",")
    for piece in flat.split(","):
        h = piece.strip().upper()
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6 and all(c in "0123456789ABCDEF" for c in h):
            out.add(h)
    return out


def _meta_tags(html):
    """逐个字面量取 meta 标签(不用正则:少一个能被引号/属性顺序玩坏的解析器)。"""
    out, low, i = [], html.lower(), 0
    while True:
        j = low.find("<meta", i)
        if j < 0:
            return out
        k = low.find(">", j)
        if k < 0:
            return out
        out.append(html[j:k + 1])
        i = k + 1


def _meta_attr(tag, name):
    """从单个 meta 标签取属性值:属性顺序不敏感,单双引号都收,无引号不认。
    lower() 只用于定位、不改变下标,所以切片仍取原文(大小写原样进 normalize)。"""
    low, key = tag.lower(), name.lower() + "="
    j = low.find(key)
    if j < 0:
        return None
    j += len(key)
    while j < len(tag) and tag[j].isspace():
        j += 1
    if j >= len(tag) or tag[j] not in ('"', "'"):
        return None
    q = tag[j]
    k = tag.find(q, j + 1)
    return None if k < 0 else tag[j + 1:k]


def meta_palette(html):
    """缺省 --palette 时的取板路径(AE-B ①):读被检 HTML 里的引擎板声明。
      格式(scene_kit/scaffold_kit 注入):
        meta name="aesthete-palette" content="01161E,124559,...,EFF6E0"   6 位大写无 # 逗号分隔
      多个 meta 取并集;取不到返回空集(调用方记 1 条 P1)。
      只认 aesthete-palette:aesthete-tokens 是角色表(bg=/surf=),拿它当板会把角色名当色。"""
    found = set()
    for tag in _meta_tags(html):
        if (_meta_attr(tag, "name") or "").strip().lower() == "aesthete-palette":
            found |= normalize_palette(_meta_attr(tag, "content") or "")
    return found


def _dom_class_ids(html):
    """本页 DOM 出现过的 class/id 名(静态保守口径;JS 运行时注入的类归渲染闸管)。
    三种属性形态都收:双引号/单引号/无引号。"""
    dom = set()
    for m in re.finditer(r'class\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>"\']+))', html):
        dom.update((m.group(1) or m.group(2) or m.group(3) or "").split())
    for m in re.finditer(r'id\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>"\']+))', html):
        v = m.group(1) or m.group(2) or m.group(3)
        if v:
            dom.add(v)
    return dom


def _font_scan(html):
    """收集字号声明,分"会渲染"(used)/"幽灵规则"(ghost)两桶(AE-FONTGHOST)。
    归属口径(静态保守):内联 style 恒为 used;<style> 规则按选择器引用的 class/id
    是否出现在本页 DOM 判定(任一命中即算 used);@media 内层规则保守全部算 used
    (响应式规则按条件命中,静态无法证伪);无 class/id 的元素选择器算可能命中。"""
    dom = _dom_class_ids(html)
    used, ghost = [], []
    n_total = n_unused = 0
    inline = " ".join(re.findall(r'style="([^"]+)"', html))
    inline_sizes = [float(g1 or g2) for g1, g2 in FONT_RE.findall(inline)]
    used.extend(inline_sizes)
    n_total += len(inline_sizes)
    for block in re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I):
        for mm in re.finditer(r"@media[^{]*\{((?:[^{}]*\{[^{}]*\})*[^{}]*)\}", block):
            media_sizes = [float(g1 or g2) for g1, g2 in FONT_RE.findall(mm.group(1))]
            used.extend(media_sizes)
            n_total += len(media_sizes)
        body = re.sub(r"@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", " ", block)
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", body):
            sizes = [float(g1 or g2) for g1, g2 in FONT_RE.findall(m.group(2))]
            if not sizes:
                continue
            n_total += len(sizes)
            toks = {t for pair in re.findall(r"\.([A-Za-z_][\w-]*)|#([A-Za-z_][\w-]*)", m.group(1))
                    for t in pair}
            if toks and not (toks & dom):
                n_unused += len(sizes)
                ghost.extend(sizes)
            else:
                used.extend(sizes)
    return used, ghost, n_total, n_unused


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--palette", default=None,
                    help="声明的色板,逗号分隔 hex;缺省时自动读被检 HTML 里的 "
                         "meta name=aesthete-palette 板声明(引擎产物自带)")
    ap.add_argument("--floor", type=float, default=12, help="字号下限 px(投影件建议 24-34)")
    ap.add_argument("--max-grad", type=int, default=0, help="渐变容量(默认 0=禁渐变)")
    ap.add_argument("--lenient", action="store_true",
                    help="过渡口径:P1 需 >=2 条才红(夜间先跑;默认严:单条 P1 即红)")
    ap.add_argument("--render", default=None, help="render_probe.js 采集的 evidence.json")
    args = ap.parse_args()

    with open(args.page, encoding="utf-8") as f:
        html = f.read()
    declared, board_src = normalize_palette(args.palette), "--palette"
    if not declared:  # 缺省(或给了空串)=> 自动取产物 meta 声明
        declared, board_src = meta_palette(html), "meta"
    used = used_colors(html)

    findings = []
    drift = []
    if not declared:
        findings.append(("P1", "色板漂移闸跳过:未传 --palette 且页面无 meta name=aesthete-palette 声明"
                         " => 声明板未知,无法判定私货色(引擎产物应自带 meta;其余闸门照常)"))
    else:
        print(f"[INFO] 声明板来源={board_src},共 {len(declared)} 色")
        # 板外非近中性色。旧代码那两条冗余过滤(startswith("0") / FFFFFF)已被判据覆盖,删掉:
        # 近中性只有一条可复算定义,不留第二套"看起来更严"的旁路。
        # 声明板未知时**不判漂移**(否则 used - 空集 = 全部自用色,会把引擎自己的板当私货)。
        drift = sorted(c for c in used - declared if hex_chromatic(c))
    if drift:
        # 定级阶梯:>=2 种 = P0(执法点);恰好 1 种 = P1(0.24 由临时 P2 升回 —— AE-N2 裁决)
        sev = "P0" if len(drift) >= OFF_PALETTE_P0_MIN else "P1"
        findings.append((sev, f"色板漂移[{len(drift)} 种板外非近中性色,{sev}]:"
                         f"页面使用了声明色板之外的颜色 {', '.join('#'+c for c in drift)}"
                         " —— 每个私货色必须回答'它编码什么'(镜3)"
                         + ("" if sev == "P1" else
                            f";{OFF_PALETTE_P0_MIN} 种及以上即整套自造色阶(绕板),不是个别遗漏 => P0")))

    banned = {}
    try:
        with open(PROFILE, encoding="utf-8") as f:
            banned = json.load(f).get("banned_hex_families", {})
    except Exception as e:
        # 0.26 闸门诚实:黑名单闸数据不可读绝不静默 —— 跳过即记 P1(默认严=红)
        findings.append(("P1", f"黑名单族闸跳过:profile.json 不可读({e}) —— tailwind 默认/紫域黑名单本轮未测,修复后重跑"))
    for fam, hexes in banned.items():
        hit = sorted(set(h.upper() for h in hexes) & used)
        if hit:
            findings.append(("P0" if fam == "tailwind_defaults" else "P1",
                             f"黑名单族 {fam} 命中: {', '.join('#'+h for h in hit)}"))

    used_sizes, ghost_sizes, n_sizes, n_ghost = _font_scan(html)
    small = sorted(s for s in used_sizes if s < args.floor)
    if small:
        findings.append(("P1", f"字号低于下限 {args.floor}px: {sorted(set(small))}(含 font: 简写形态)"))
    small_ghost = sorted(s for s in ghost_sizes if s < args.floor)
    if small_ghost:
        findings.append(("P2", f"幽灵规则字号低于下限 {args.floor}px: {sorted(set(small_ghost))}"
                         " —— 所在规则未命中本页 DOM,不渲染;渲染级 computed style 才判真红"))
    print(f"[INFO] 字号闸: 扫描 {n_sizes} 条字号声明, 其中 {n_ghost} 条所在规则未命中本页 DOM(幽灵,降级 P2)")

    grads = len(re.findall(r"linear-gradient|radial-gradient|conic-gradient", html))
    if grads > args.max_grad:
        findings.append(("P0", f"禁渐变: 渐变出现 {grads} 次(>0)——一律用纯色分层替代, 渐变即不合格"))

    emojis = EMOJI_RE.findall(html)
    if emojis:
        findings.append(("P2", f"emoji 出现 {len(emojis)} 处(除非品牌系统使用)"))

    dosage_gate, n_measured = "SKIP", 0
    if args.render:
        ev = json.load(open(args.render, encoding="utf-8"))
        prof = {}
        try:
            with open(PROFILE, encoding="utf-8") as f:
                prof = json.load(f)
        except Exception as e:
            # 0.26 闸门诚实:档案(主题/剂量阈值)不可读绝不静默
            findings.append(("P1", f"档案闸跳过:profile.json 不可读({e}) —— 主题对账与剂量阈值未核"))
        dreg = prof.get("registers", {}).get(prof.get("default_register", ""), {})
        want, acc_max = dreg.get("theme"), dreg.get("accent_max_area", 0.10)
        if want and ev.get("theme") != want:
            findings.append(("P1", f"PROFILE/渲染: 档案要求 {want} 底,页面实测 {ev.get('theme')} 底(bodyBg={ev.get('bodyBg')})"))
        bg_hex = (ev.get("bodyBg") or "").upper()
        n_measured = len(ev.get("colors", []))
        dosage_gate = "MEASURED"
        # AE-N3:不再无条件砍掉首位(旧 `[1:]` 让 accent 大底漏判)——bg_hex 过滤本就在下一行
        loud = [c for c in ev.get("colors", [])
                if c["hex"] != bg_hex and c["areaRatio"] > acc_max
                and not NEUTRAL(int(c["hex"][0:2], 16), int(c["hex"][2:4], 16), int(c["hex"][4:6], 16))]
        if loud:
            findings.append(("P1", "剂量失控(渲染实测): " +
                             ", ".join(f"#{c['hex']} 占 {c['areaRatio']*100:.0f}% (>{acc_max*100:.0f}%)" for c in loud[:3])))
        mf = ev.get("minFont", 99)
        if mf < args.floor:
            findings.append(("P2", f"渲染实测最小字号 {mf}px < {args.floor}px(样本: {ev.get('fontSample','')[:20]})"))
        # 0.22 分区复验:probe v2 zones(顶层区块渲染 bg)的脏色大底,渲染事实级
        import colorsys as _cs
        for z in ev.get("zones", []):
            zh_ = str(z.get("hex", "")).upper()
            if len(zh_) != 6 or z.get("share", 0) < 0.12:
                continue
            rr, gg, bb = (int(zh_[i:i + 2], 16) / 255 for i in (0, 2, 4))
            hh, ll, ss = _cs.rgb_to_hls(rr, gg, bb)
            if ss >= 0.25 and 0.30 < ll < 0.85:
                findings.append(("P2", "渲染事实:区块大底 #%s 占 %.0f%% 命中中饱和中明带(显脏)"
                                 % (zh_, z["share"] * 100)))
        worst = [p for p in ev.get("worstPairs", []) if p["ratio"] < 3.0]
        if worst:
            findings.append(("P1", "实测对比对不足 3:1: " +
                             ", ".join(f"#{p['fg']}/#{p['bg']}={p['ratio']}" for p in worst[:3])))
    else:
        # AE-N3: 剂量维度缺失绝不静默 —— 显式点名未测什么、为什么、怎么补
        print("[SKIP] 剂量闸 SKIP(未提供 --render evidence.json): 强调色剂量/主题/实测字号/最差对比对 本轮未测 —— "
              "用 scripts/render_probe.js 采集后以 --render 传入")

    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    for sev, msg in sorted(findings, key=lambda t: order[t[0]]):
        print(f"[{sev}] {msg}")
    if not findings:
        print("[OK] 静态审计通过;渲染级证据(视线顺序/密度/构图)由五镜自审截图环节补齐")
    n_p0 = sum(1 for s, _ in findings if s == "P0")
    n_p1 = sum(1 for s, _ in findings if s == "P1")
    n_p2 = sum(1 for s, _ in findings if s == "P2")
    dg_txt = dosage_gate if dosage_gate == "SKIP" else f"{dosage_gate}(扫描 {n_measured} 色)"
    print(f"[SUMMARY] P0={n_p0} P1={n_p1} P2={n_p2} 剂量闸={dg_txt}")
    p1_gate = 2 if args.lenient else 1
    sys.exit(1 if n_p0 or n_p1 >= p1_gate else 0)


if __name__ == "__main__":
    main()
