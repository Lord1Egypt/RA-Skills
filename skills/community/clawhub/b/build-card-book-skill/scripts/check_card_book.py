#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_card_book.py — 自动检查生成的卡片书 HTML（硬编码自检）
用法: python3 check_card_book.py out.html
检查: ① section/div 闭合平衡 ② 占位符残留 ③ 目录/导航/主题卡 id 一一对应
      ④ safe center ⑤ 左右箭头分侧 ⑥ 首尾禁用 ⑦ 无外部依赖(除 hero 图)
"""
import re, sys, os

def main():
    if len(sys.argv) < 2:
        print("用法: python3 check_card_book.py out.html"); sys.exit(1)
    p = sys.argv[1]
    c = open(p, encoding="utf-8").read()
    c2 = re.sub(r"<!--.*?-->", "", c, flags=re.S)
    ok = True
    def chk(name, cond, hint=""):
        nonlocal ok
        print(("✅" if cond else "❌"), name, hint if not cond else "")
        if not cond: ok = False
    # 1. 结构平衡
    for tag in ["section", "div"]:
        o = len(re.findall(rf"<{tag}[ >]", c2))
        cl = len(re.findall(rf"</{tag}>", c2))
        chk(f"{tag} 闭合平衡 ({o}/{cl})", o == cl, "→ 有未闭合标签")
    # 2. 占位符残留
    ph = set(re.findall(r"\{\{[^}]+\}\}", c2))
    chk("无占位符残留", not ph, f"→ 残留: {ph}")
    # 3. id 对应（目录/导航/主题卡）
    idx_ids = set(re.findall(r'class="idx" href="#(c\d+)"', c2))
    nav_ids = set(re.findall(r'nav-drop-panel.*?(?:</div>\s*){2}</nav>', c2, re.S) and
                  re.findall(r'<a href="#(c\d+)"', re.search(r'nav-drop-panel.*?</nav>', c2, re.S).group(0) if re.search(r'nav-drop-panel.*?</nav>', c2, re.S) else ""))
    card_ids = set(re.findall(r'<section class="page" id="(c\d+)"', c2))
    chk("目录/导航/卡片 id 对应", idx_ids == card_ids and nav_ids == card_ids,
        f"→ 目录{len(idx_ids)} 导航{len(nav_ids)} 卡{len(card_ids)}")
    # 4. safe center
    chk("safe center", "safe center" in c2)
    # 5. 箭头分侧
    chk("箭头分侧(.prev left/.next right)",
        bool(re.search(r'\.flip\.prev\{[^}]*left', c2)) and bool(re.search(r'\.flip\.next\{[^}]*right', c2)))
    chk("基类 .flip 无 left/right 冲突", not re.search(r'\.flip\s*\{[^}]*left', c2))
    # 6. 翻页入口
    chk("键盘/横滑/下拉入口", all(k in c2 for k in ["keydown", "touchstart", "navDrop"]))
    # 7. 外部依赖（除 hero 图）
    ext = re.findall(r'<script src=|<link rel="stylesheet"|@import', c2)
    chk("无外部 CSS/JS 依赖", not ext)
    print("\n" + ("✅ 全部通过" if ok else "⚠️ 存在问题，请修复"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
