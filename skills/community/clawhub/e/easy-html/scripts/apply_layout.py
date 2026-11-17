#!/usr/bin/env python3
"""
apply_layout.py — 注入 easy-html 基础资产（布局骨架 + 可视化组件 + 图表助手）

注入三层基础资产到 HTML：
  1. assets/layout_base.css   —— 布局骨架（居中容器/卡片网格/留白/表格/响应式）
  2. assets/viz_components.css —— 可视化组件库（KPI卡/进度条/环形/对比条/流程/时间轴/标签云）
  3. assets/chart_helper.js   —— Chart.js 多源CDN兜底渲染器（仅当页面含 data-eh-chart 时生效）

为什么需要：html-golive 的 19 套主题 CSS **只写配色，明文禁止写布局**。布局与
可视化组件必须由生成的 HTML 自带。三层资产都用主题 CSS 变量取色，深浅主题自适应。

CSS 注入位置：<head> 开标签后（早于主题 CSS，主题只覆盖配色）。
JS 注入位置：</body> 前（无则文档末尾）。

用法（在 apply_style 之前调用）：
  python3 apply_layout.py page.html               # 覆盖原文件
  python3 apply_layout.py page.html -o out.html
  python3 apply_layout.py page.html --no-chart     # 不注入图表助手JS

幂等：已注入过（含对应标记）则跳过。
"""
import argparse
import os
import re
import sys

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
LAYOUT_CSS = os.path.join(ASSETS, "layout_base.css")
VIZ_CSS = os.path.join(ASSETS, "viz_components.css")
CHART_JS = os.path.join(ASSETS, "chart_helper.js")

_HEAD_OPEN_RE = re.compile(r"<head[^>]*>", re.IGNORECASE)
_BODY_CLOSE_RE = re.compile(r"</body\s*>", re.IGNORECASE)


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def inject_css_head(html, css, mark):
    if mark in html:
        return html, False
    tag = f'<style {mark}="1">\n{css}\n</style>'
    m = _HEAD_OPEN_RE.search(html)
    if m:
        idx = m.end()
        return html[:idx] + "\n" + tag + html[idx:], True
    mb = re.search(r"<body\b", html, re.IGNORECASE)
    if mb:
        return html[:mb.start()] + tag + "\n" + html[mb.start():], True
    return tag + "\n" + html, True


def inject_js_body(html, js, mark):
    if mark in html:
        return html, False
    tag = f'<script {mark}="1">\n{js}\n</script>'
    m = _BODY_CLOSE_RE.search(html)
    if m:
        idx = m.start()
        return html[:idx] + tag + "\n" + html[idx:], True
    return html + "\n" + tag, True


def main():
    ap = argparse.ArgumentParser(description="注入 easy-html 基础资产（布局+可视化组件+图表助手）")
    ap.add_argument("html", help="HTML 文件路径")
    ap.add_argument("-o", "--output", help="输出文件（默认覆盖原文件）")
    ap.add_argument("--no-chart", action="store_true", help="不注入图表助手 JS")
    args = ap.parse_args()

    with open(args.html, encoding="utf-8", errors="replace") as f:
        html = f.read()

    done = []
    html, c1 = inject_css_head(html, _read(LAYOUT_CSS), "data-eh-layout")
    if c1:
        done.append("布局骨架")
    html, c2 = inject_css_head(html, _read(VIZ_CSS), "data-eh-viz")
    if c2:
        done.append("可视化组件")
    if not args.no_chart:
        html, c3 = inject_js_body(html, _read(CHART_JS), "data-eh-chart-helper")
        if c3:
            done.append("图表助手")

    out = args.output or args.html
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    if done:
        print(f"✅ 已注入：{' / '.join(done)} → {out}")
    else:
        print(f"ℹ️  基础资产已存在，跳过 → {out}")


if __name__ == "__main__":
    main()
