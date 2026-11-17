#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML 产物保真 + 结构校验（与 validate_docx.py 同口径）。

用法：
  python validate_html.py --json <中间json或source/markdown字段> --html <产物.html>

判定与 docx 一致：以字符级 CJK 覆盖率（≥99%）为准；emoji 以 --strip-emoji
同口径从源文剥离后再比对，防止剥除误报。结构检查：目录锚点、表格、
源页标注、证据溯源附录的存在性（存在与否均为信息，不参与判定）。
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser

CJK = re.compile(r"[\u4e00-\u9fff]")
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u2190-\u21FF\u2B00-\u2BFF]")
# 设计铁律（业界同类排版工具的可机械判定铁律写法 → CSS 断言）
MAX_CHROMATIC = 3
CJK_FONT_HINTS = ("Noto Sans SC", "Noto Sans CJK", "微软雅黑", "Microsoft YaHei",
                  "PingFang SC", "Source Han", "思源黑体")


def _chroma(hex6):
    """颜色的彩度：RGB 三通道极差。近灰（≤24）不算彩色。"""
    r = int(hex6[0:2], 16); g = int(hex6[2:4], 16); b = int(hex6[4:6], 16)
    return max(r, g, b) - min(r, g, b)


def _luma(hex6):
    """WCAG 相对亮度。"""

    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r = lin(int(hex6[0:2], 16)); g = lin(int(hex6[2:4], 16)); b = lin(int(hex6[4:6], 16))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(a, b):
    la, lb = _luma(a), _luma(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def css_audit(html_raw):
    """审计 <style> 块：非零圆角 / 阴影 / 有彩色数 / CJK 字体栈 / 主文对比度。"""
    m = re.search(r"<style[^>]*>(.*?)</style>", html_raw, re.S)
    css = m.group(1) if m else ""
    radius_bad = 0
    for decl in re.findall(r"border-radius\s*:\s*([^;}>]+)", css):
        if any(tok.strip() and not tok.strip().startswith("0")
               for tok in decl.split()):
            radius_bad += 1
    shadows = len(re.findall(r"(?:box|text)-shadow\s*:\s*(?!none)", css))
    chroma = set()
    for hex6 in re.findall(r"#([0-9A-Fa-f]{6})\b", css):
        if _chroma(hex6.upper()) > 24:
            chroma.add(hex6.upper())
    has_cjk_font = any(h.lower() in css.lower() for h in CJK_FONT_HINTS)
    # 主文对比度：--ink vs --panel（或白底），都有则参与判定
    ink = re.search(r"--ink\s*:\s*#([0-9A-Fa-f]{6})", css)
    panel = re.search(r"--panel\s*:\s*#([0-9A-Fa-f]{6})", css)
    contrast = (_contrast(ink.group(1).upper(), panel.group(1).upper())
                if ink and panel else None)
    return {"radius_bad": radius_bad, "shadows": shadows,
            "chroma": sorted(chroma), "has_cjk_font": has_cjk_font,
            "contrast": contrast}


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buf = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip = max(self.skip - 1, 0)

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)


def text_of_html(path):
    p = _Text()
    p.feed(open(path, encoding="utf-8").read())
    return "".join(p.buf)


def norm_chars(s):
    s = EMOJI.sub("", s or "")
    return [c for c in s if CJK.match(c)]


def source_markdown(data):
    """单源取 markdown；多源取 sources[].markdown 拼接（与渲染口径一致）。"""
    if data.get("sources") or data.get("analysis"):
        parts = []
        ana = data.get("analysis")
        if ana:
            parts.append(ana.get("markdown") if isinstance(ana, dict) else str(ana))
        parts.extend(s.get("markdown") or "" for s in data.get("sources") or [])
        return "\n\n".join(parts)
    return data.get("markdown") or ""


def main():
    ap = argparse.ArgumentParser(description="omni2docx HTML 保真校验器")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--json", help="渲染时输入的中间 JSON")
    g.add_argument("--md", help="若用 --md 直出，则给该 markdown 文件（替代 --json 的源）")
    ap.add_argument("--html", required=True)
    ap.add_argument("--no-toc", action="store_true", help="渲染时未开目录则加此开关")
    args = ap.parse_args()

    if args.md:
        src_md = open(args.md, encoding="utf-8").read()
    else:
        src_md = source_markdown(json.load(open(args.json, encoding="utf-8")))

    html_raw = open(args.html, encoding="utf-8").read()
    html_text = text_of_html(args.html)

    src_cjk = Counter(norm_chars(src_md))
    out_cjk = Counter(norm_chars(html_text))
    if src_cjk:
        hit = sum(min(v, out_cjk.get(k, 0)) for k, v in src_cjk.items())
        coverage = hit / sum(src_cjk.values())
        missing = {k: v for k, v in src_cjk.items() if out_cjk.get(k, 0) < v}
    else:
        coverage, missing = 1.0, {}

    anchors = len(re.findall(r'id="[^"]+"', html_raw))
    toc = 'class="toc"' in html_raw
    pagemarks = html_raw.count('class="pagemark"')
    tables = html_raw.count("<table>")
    appendix = 'class="appendix"' in html_raw
    selfcontained = ("<style>" in html_raw and "http" not in
                     " ".join(re.findall(r'(?:src|href)="(http[^"]+)"', html_raw)))
    design = css_audit(html_raw)

    print("=" * 64)
    print("Omni2Docx HTML 保真 + 结构校验 :", os.path.basename(args.html))
    print("=" * 64)
    print("[内容保真]")
    print("  源文 CJK 字符种类 :", len(src_cjk))
    print("  HTML 含源文 CJK 覆盖率 : %.2f%%" % (coverage * 100))
    print("  缺失 CJK 字符(种类) :", len(missing), list(missing)[:20])
    print("[结构]")
    print("  锚点(id) 数 :", anchors)
    print("  目录 :", "有" if toc else ("无" if args.no_toc else "无（未加 --no-toc，异常）"))
    print("  源页标注 :", pagemarks)
    print("  表格数 :", tables)
    print("  溯源附录 :", "有" if appendix else "无")
    print("  自包含(无外链) :", "是" if selfcontained else "否")
    print("[设计铁律]")
    print("  非零圆角声明 :", design["radius_bad"], "（铁律：0）")
    print("  阴影声明 :", design["shadows"], "（铁律：0）")
    print("  有彩色数 :", len(design["chroma"]), design["chroma"],
          "（铁律：≤%d，近灰不计）" % MAX_CHROMATIC)
    print("  CJK 字体栈 :", "有" if design["has_cjk_font"] else "缺失（铁律：必须有）")
    if design["contrast"] is not None:
        print("  主文对比度 : %.2f（铁律：≥4.5，--ink vs --panel）" % design["contrast"])

    problems = []
    if coverage < 0.99:
        problems.append("CJK 覆盖率 <99%")
    if design["radius_bad"]:
        problems.append("非零圆角 %d 处" % design["radius_bad"])
    if design["shadows"]:
        problems.append("阴影 %d 处" % design["shadows"])
    if len(design["chroma"]) > MAX_CHROMATIC:
        problems.append("有彩色 %d 种 >%d" % (len(design["chroma"]), MAX_CHROMATIC))
    if not design["has_cjk_font"]:
        problems.append("缺 CJK 字体栈")
    if design["contrast"] is not None and design["contrast"] < 4.5:
        problems.append("主文对比度 %.2f <4.5" % design["contrast"])
    ok = not problems
    print("判定 :", "PASS" if ok else "FAIL（%s）" % "；".join(problems))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
