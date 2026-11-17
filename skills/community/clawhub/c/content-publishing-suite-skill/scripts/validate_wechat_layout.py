#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公众号正文排版唯一基线校验器。

用途：阻断字号、行高、颜色、间距、背景和结构漂移。
该脚本只校验可确定的 HTML 合约；视觉审查仍由手机预览负责。
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path


def norm(value):
    return re.sub(r"\s+", "", value.strip().lower())


def parse_style(style):
    result = {}
    for part in style.split(";"):
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        result[key.strip().lower()] = norm(value)
    return result


def text_content(fragment):
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", "", html.unescape(fragment))


def attr(tag, name):
    m = re.search(r"\b%s\s*=\s*['\"]([^'\"]*)['\"]" % re.escape(name), tag, re.I)
    return m.group(1) if m else ""


def style_of(tag):
    return parse_style(attr(tag, "style"))


PROPERTY_NAMES = {
    "font_size": "font-size", "font_weight": "font-weight", "text_align": "text-align",
    "line_height": "line-height", "letter_spacing": "letter-spacing", "padding_left": "padding-left",
    "border_left": "border-left", "blockquote_margin": "margin", "section_padding": "padding",
    "border_radius": "border-radius"
}


def check_style(actual, expected, label, failures, keys=None):
    selected = keys or list(expected)
    allowed = set()
    for key in selected:
        css_key = PROPERTY_NAMES.get(key, key)
        allowed.add(css_key)
        expected_value = norm(expected[key])
        if actual.get(css_key) != expected_value:
            failures.append("%s: %s=%r，要求 %r" % (label, css_key, actual.get(css_key), expected_value))
    extras = sorted(set(actual) - allowed)
    if extras:
        failures.append("%s: 存在未授权样式属性 %s" % (label, ", ".join(extras)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html_path")
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    source = Path(args.html_path).read_text(encoding="utf-8")
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    contract = baseline["wechat_snippet"]
    failures = []

    if re.search(r"<style|<script", source, re.I):
        failures.append("包含 <style> 或 <script>")
    if not source.rstrip().endswith(contract["document"]["must_end_with"]):
        failures.append("文末不是 <v2></v2>")
    if re.search(r"position\s*:\s*(fixed|absolute)", source, re.I):
        failures.append("包含 position:fixed/absolute")
    if re.search(r"\bclass\s*=", source, re.I):
        failures.append("可粘贴片段包含 class 属性")
    if "<section" not in source.lower():
        failures.append("缺少 section 内容块")
    for index, tag in enumerate(re.findall(r"<section\b[^>]*>", source, re.I), 1):
        section_style = style_of(tag)
        if "background" in section_style:
            failures.append("section[%d] 不允许设置背景，背景只能由引用块/表格组件承载" % index)
        if "position" in section_style:
            failures.append("section[%d] 不允许设置 position" % index)

    h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", source, re.I | re.S)
    if len(h1) != 1:
        failures.append("h1 数量=%d，要求 1" % len(h1))
    else:
        h1_tag = re.search(r"<h1\b[^>]*>", source, re.I).group(0)
        check_style(style_of(h1_tag), contract["title"], "h1", failures)
        if args.title and text_content(h1[0]) != text_content(args.title):
            failures.append("h1 文本与定稿标题不一致")

    h2_tags = re.findall(r"<h2\b[^>]*>", source, re.I)
    for index, tag in enumerate(h2_tags, 1):
        check_style(style_of(tag), contract["heading"], "h2[%d]" % index, failures)
    if not h2_tags:
        failures.append("未找到 h2，无法确认小标题基线")

    p_matches = list(re.finditer(r"<p\b([^>]*)>(.*?)</p>", source, re.I | re.S))
    if not p_matches:
        failures.append("未找到 p，无法确认正文基线")
    for index, match in enumerate(p_matches, 1):
        tag = "<p%s>" % match.group(1)
        styles = style_of(tag)
        if "text-align" in styles:
            failures.append("正文 p[%d] 禁止设置 text-align；仅 h1 标题允许居中" % index)
        size = styles.get("font-size")
        if size == norm(contract["paragraph"]["font_size"]):
            check_style(styles, contract["paragraph"], "正文 p[%d]" % index, failures)
        elif size == norm(contract["summary"]["font_size"]):
            check_style(styles, contract["summary"], "摘要/引用 p[%d]" % index, failures,
                        ["font_size", "line_height", "color", "margin"])
        else:
            failures.append("p[%d] 使用未定义字号 %r" % (index, size))

    strong_tags = re.findall(r"<strong\b[^>]*>", source, re.I)
    for index, tag in enumerate(strong_tags, 1):
        check_style(style_of(tag), contract["strong"], "strong[%d]" % index, failures)

    for index, match in enumerate(re.finditer(r"<blockquote\b([^>]*)>", source, re.I), 1):
        styles = style_of("<blockquote%s>" % match.group(1))
        check_style(styles, contract["summary"], "blockquote[%d]" % index, failures,
                    ["blockquote_margin", "padding", "background", "border_left", "border_radius"])

    if failures:
        for item in failures:
            print("FAIL  " + item)
        print("排版门禁：未通过（%d 项失败）" % len(failures))
        return 2

    print("排版门禁：通过")
    print("基线：标题 23px / 小标题 18px / 正文 16px / 正文行高 1.8")
    print("结构：h1=1，h2=%d，p=%d，strong=%d" % (len(h2_tags), len(p_matches), len(strong_tags)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
