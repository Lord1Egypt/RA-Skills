#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_card_book.py — 从内容 JSON 生成「翻阅式卡片工具书」单文件 HTML（硬编码版）
用法:
    python3 build_card_book.py cards.json [-o out.html] [--basic]
示例 cards.json:
{
  "书名": "毛泽东选集", "书印单字": "毛", "副标题": "方法论口袋书",
  "导语": "遇事翻一翻，把书读薄。", "关键词": "你的回复关键词",
  "公众号名": "你的公众号名",
  "卡片": [
    {"名": "调查研究", "描述": "情况不明先蹲下去",
     "命题": "没有调查，没有发言权。",
     "原文": "调查就像"十月怀胎"，解决问题就像"一朝分娩"。",
     "出处": "《反对本本主义》(1930)",
     "场景": ["写方案前先收集一线事实", "接手新业务先摸清现状", "判断争议先听不同声音"]}
  ]
}
输出: 单文件 HTML（默认用 themed 模板，--basic 用基础模板）
"""
import json, re, sys, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

def esc(s):
    return html.escape(str(s or ""), quote=False)

def gen_index_item(n, name, desc):
    return (f'<a class="idx" href="#c{n:02d}"><div class="b">{n:02d}</div>'
            f'<div class="meta"><div class="nm">{esc(name)}</div>'
            f'<div class="ds">{esc(desc)}</div></div></a>')

def gen_nav_item(n, name):
    return f'<a href="#c{n:02d}"><span class="nb">{n:02d}</span>{esc(name)}</a>'

def gen_card(n, c):
    k = (n - 1) % 3 + 1  # c1/c2/c3 色循环
    scenes = c.get("场景", ["", "", ""])
    s = [f'<div class="s"><div class="lab">{lab}</div><div class="tx">{esc(scenes[i] if i < len(scenes) else "")}</div></div>'
         for i, lab in enumerate(["工作与决策", "团队与管理", "个人成长"])]
    # 怎么用（步骤列表）
    steps = c.get("步骤", [])
    steps_html = ""
    if steps:
        lis = "\n        ".join(f"<li>{esc(x)}</li>" for x in steps)
        steps_html = (f'<div class="steps"><div class="lab">怎么用</div>'
                      f'<ol class="st">\n        {lis}\n      </ol></div>')
    # 别踩的坑
    avoid = c.get("避免", "")
    avoid_html = (f'<div class="avoid"><div class="lab">别踩的坑</div>'
                  f'<div class="tx">{esc(avoid)}</div></div>') if avoid else ""
    return (f'<section class="page" id="c{n:02d}"><article class="sheet card c{k}">\n'
            f'  <div class="head"><div class="badge">{n:02d}</div><div class="nm">{esc(c["名"])}</div></div>\n'
            f'  <div class="thesis">{esc(c.get("命题", ""))}</div>\n'
            f'  <div class="quote">"{esc(c.get("原文", ""))}"<span class="src">——{esc(c.get("出处", ""))}</span></div>\n'
            f'  <div class="scn">' + "\n".join(s) + '</div>\n'
            + steps_html + '\n'
            + avoid_html + '\n'
            f'  <div class="back"><a href="#page-index">↑ 返回目录</a></div>\n'
            f'</article></section>')

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    src = sys.argv[1]
    out = None
    for i, a in enumerate(sys.argv[2:]):
        if a == "-o" and i + 2 < len(sys.argv): out = sys.argv[i + 3]
        if a == "--basic": tpl = "card-book-template.html"
    tpl = os.path.join(ASSETS, "card-book-template.themed.html") if "--basic" not in sys.argv else os.path.join(ASSETS, "card-book-template.html")
    with open(src, encoding="utf-8") as f:
        d = json.load(f)
    cards = d.get("卡片", [])
    n = len(cards)
    c = open(tpl, encoding="utf-8").read()
    # 目录页（index-grid 整段替换）
    idx_html = "\n          ".join(gen_index_item(i + 1, x.get("名", ""), x.get("描述", "")) for i, x in enumerate(cards))
    c = re.sub(r'<div class="index-grid">.*?</div>\s*</article>', '<div class="index-grid">\n          ' + idx_html + '\n        </div>\n      </article>', c, flags=re.S)
    # 导航下拉（nav-drop-panel 整段替换）
    nav_html = "\n        ".join(gen_nav_item(i + 1, x.get("名", "")) for i, x in enumerate(cards))
    c = re.sub(r'<div class="nav-drop-panel">.*?</div>\s*</div>\s*</nav>', '<div class="nav-drop-panel">\n        ' + nav_html + '\n        </div>\n      </div>\n    </nav>', c, flags=re.S)
    # 主题卡（从第一个 c01 section 到封底开标签前整段替换）
    card_html = "\n\n    ".join(gen_card(i + 1, x) for i, x in enumerate(cards))
    c = re.sub(r'<!-- 3~N\+2 主题卡片 -->.*?(?=<section class="page page-back")',
               '<!-- 3~N+2 主题卡片 -->\n    ' + card_html + '\n\n    ', c, flags=re.S)
    # 文本占位符
    default_steps = [
        "遇到卡点：信息不全 / 资源劣势 / 局面复杂。",
        "从顶部「目录」挑一张对应的卡片主题。",
        "看「核心命题 + 原文」，再读 3 个现实场景。",
        "把场景里的动作，套进你当下的具体决策。",
    ]
    steps4 = d.get("使用步骤", default_steps) or default_steps
    repl = {
        "{{N}}": str(n),
        "{{书名}}": esc(d.get("书名", "")),
        "{{书印单字}}": esc(d.get("书印单字", "")[:1]),
        "{{副标题}}": esc(d.get("副标题", "")),
        "{{导语}}": esc(d.get("导语", "")),
        "{{一句话总览：把本书核心方法论拆成 N 张可左右翻阅的卡片。}}": esc(d.get("总览", "")),
        "{{关键词}}": esc(d.get("关键词", "")),
        "{{公众号名}}": esc(d.get("公众号名", "")),
        "{{金句}}": esc(d.get("金句", "")),
        "{{文章跨度/年代}}": esc(d.get("年代", "")),
        "{{遇到卡点：信息不全/资源劣势/局面复杂。}}": esc(steps4[0] if len(steps4) > 0 else ""),
        "{{从顶部\"目录\"挑一张对应的卡片主题。}}": esc(steps4[1] if len(steps4) > 1 else ""),
        "{{看\"核心命题 + 原文\"，再读 3 个现实场景。}}": esc(steps4[2] if len(steps4) > 2 else ""),
        "{{把场景里的动作，套进你当下的具体决策。}}": esc(steps4[3] if len(steps4) > 3 else ""),
    }
    for k, v in repl.items():
        c = c.replace(k, v)
    # 兜底：清掉剩余 {{占位符}}
    c = re.sub(r"\{\{[^}]+\}\}", "", c)
    if not out:
        out = re.sub(r"[^\w\u4e00-\u9fff]+", "-", d.get("书名", "cardbook")) + ".html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"✅ 生成: {out} | {n} 张卡片 | 使用模板: {os.path.basename(tpl)}")

if __name__ == "__main__":
    main()
