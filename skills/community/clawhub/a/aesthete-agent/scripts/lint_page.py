#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_page.py — HTML 交付前的静态审计(机制,非散文)。

检查:
  1. 色板漂移   — 页面实际使用的颜色 vs 声明色板(未声明的"私货色"逐个点名)
  2. 黑名单族   — profile.json 的 banned hex 家族(中位数陷阱)
  3. 字号下限   — CSS 中的 px 字号低于 --floor 即点名(投影件建议 24-34)
  4. 渐变剂量   — linear/radial/conic 渐变出现即 P0(审美铁律: 禁渐变, 纯色分层替代)
  5. emoji      — 出现 emoji 计 P2(除非品牌系统使用)
  6. --render evidence.json — 渲染级证据(render_probe.js 采集):主题 vs 档案、
     强调色剂量(areaRatio vs accent_max)、实测最小字号、最差对比对

裁决:P0 存在或 P1≥2 → exit 1。纯 stdlib,无浏览器依赖;
render_probe.js 由会话浏览器工具执行(见 SKILL 第 6 步闸门链)。
"""
import argparse
import json
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
NEUTRAL = lambda r, g, b: (max(r, g, b) - min(r, g, b)) < 30  # 近中性/纸系洗色不算"私货"


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
        if not NEUTRAL(r, g, b):
            found.add("%02X%02X%02X" % (r, g, b))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--palette", required=True, help="声明的色板,逗号分隔 hex")
    ap.add_argument("--floor", type=float, default=12, help="字号下限 px(投影件建议 24-34)")
    ap.add_argument("--max-grad", type=int, default=0, help="渐变容量(默认 0=禁渐变)")
    ap.add_argument("--render", default=None, help="render_probe.js 采集的 evidence.json")
    args = ap.parse_args()

    with open(args.page, encoding="utf-8") as f:
        html = f.read()
    declared = set()
    for h in args.palette.replace("#", ",").split(","):
        h = h.strip().upper()
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if h:
            declared.add(h)
    used = used_colors(html)

    findings = []
    drift = sorted(c for c in used - declared
                   if not (c.startswith("0") and NEUTRAL(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
                           or c in {"FFFFFF"}))
    # 近中性(灰阶/近白近黑)不算漂移;上面过滤不完善时人工复核 P3
    drift = [c for c in drift
             if not NEUTRAL(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))]
    if drift:
        findings.append(("P1", f"色板漂移:页面使用了声明色板之外的颜色 {', '.join('#'+c for c in drift)} —— 每个私货色必须回答'它编码什么'(镜3)"))

    banned = {}
    try:
        with open(PROFILE, encoding="utf-8") as f:
            banned = json.load(f).get("banned_hex_families", {})
    except Exception:
        pass
    for fam, hexes in banned.items():
        hit = sorted(set(h.upper() for h in hexes) & used)
        if hit:
            findings.append(("P0" if fam == "tailwind_defaults" else "P1",
                             f"黑名单族 {fam} 命中: {', '.join('#'+h for h in hit)}"))

    sizes = [float(g1 or g2) for g1, g2 in FONT_RE.findall(html)]
    small = sorted(s for s in sizes if s < args.floor)
    if small:
        findings.append(("P1", f"字号低于下限 {args.floor}px: {sorted(set(small))}(含 font: 简写形态)"))

    grads = len(re.findall(r"linear-gradient|radial-gradient|conic-gradient", html))
    if grads > args.max_grad:
        findings.append(("P0", f"禁渐变: 渐变出现 {grads} 次(>0)——一律用纯色分层替代, 渐变即不合格"))

    emojis = EMOJI_RE.findall(html)
    if emojis:
        findings.append(("P2", f"emoji 出现 {len(emojis)} 处(除非品牌系统使用)"))

    if args.render:
        ev = json.load(open(args.render, encoding="utf-8"))
        prof = {}
        try:
            with open(PROFILE, encoding="utf-8") as f:
                prof = json.load(f)
        except Exception:
            pass
        dreg = prof.get("registers", {}).get(prof.get("default_register", ""), {})
        want, acc_max = dreg.get("theme"), dreg.get("accent_max_area", 0.10)
        if want and ev.get("theme") != want:
            findings.append(("P1", f"PROFILE/渲染: 档案要求 {want} 底,页面实测 {ev.get('theme')} 底(bodyBg={ev.get('bodyBg')})"))
        bg_hex = (ev.get("bodyBg") or "").upper()
        loud = [c for c in ev.get("colors", [])[1:]
                if c["hex"] != bg_hex and c["areaRatio"] > acc_max
                and not NEUTRAL(int(c["hex"][0:2], 16), int(c["hex"][2:4], 16), int(c["hex"][4:6], 16))]
        if loud:
            findings.append(("P1", "剂量失控(渲染实测): " +
                             ", ".join(f"#{c['hex']} 占 {c['areaRatio']*100:.0f}% (>{acc_max*100:.0f}%)" for c in loud[:3])))
        mf = ev.get("minFont", 99)
        if mf < args.floor:
            findings.append(("P2", f"渲染实测最小字号 {mf}px < {args.floor}px(样本: {ev.get('fontSample','')[:20]})"))
        worst = [p for p in ev.get("worstPairs", []) if p["ratio"] < 3.0]
        if worst:
            findings.append(("P1", "实测对比对不足 3:1: " +
                             ", ".join(f"#{p['fg']}/#{p['bg']}={p['ratio']}" for p in worst[:3])))

    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    for sev, msg in sorted(findings, key=lambda t: order[t[0]]):
        print(f"[{sev}] {msg}")
    if not findings:
        print("[OK] 静态审计通过;渲染级证据(视线顺序/密度/构图)由五镜自审截图环节补齐")
    n_p0 = sum(1 for s, _ in findings if s == "P0")
    n_p1 = sum(1 for s, _ in findings if s == "P1")
    sys.exit(1 if n_p0 or n_p1 >= 2 else 0)


if __name__ == "__main__":
    main()
