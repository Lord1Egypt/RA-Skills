#!/usr/bin/env python3
"""
apply_style.py — 给 HTML 应用 19 种内置样式之一（复用 html-golive 的 CSS 引擎）

不重造样式：直接复用 html-golive 的 css_style_enhancer：
  - 自动给元素打 data-role 标注（CSS 靠它匹配）
  - 注入选中样式的 CSS（视觉属性，不动布局）

引擎来源见 _engine.py（pip install html-golive 即可）。

用法：
  python3 apply_style.py --list                          # 列出 19 种样式
  python3 apply_style.py page.html --style minimal       # 应用样式（覆盖原文件）
  python3 apply_style.py page.html --style bloomberg -o out.html
  python3 apply_style.py page.html --style apple --strip-inline   # 同时清行内 style

退出码：0 成功；1 失败
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _engine import load_engine  # noqa: E402


def _log(msg):
    print(msg, file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="给 HTML 应用 19 种内置样式之一")
    ap.add_argument("html", nargs="?", help="HTML 文件路径")
    ap.add_argument("--style", help="样式 key（如 minimal/bloomberg/apple…）")
    ap.add_argument("--list", action="store_true", help="列出 19 种可用样式")
    ap.add_argument("-o", "--output", help="输出文件（默认覆盖原文件）")
    ap.add_argument("--strip-inline", action="store_true", help="同时清除行内 style 属性")
    args = ap.parse_args()

    enhancer = load_engine()

    if args.list:
        enhancer.list_styles()
        return

    if not args.html or not args.style:
        ap.error("需要提供 <html> 和 --style（或用 --list 查看样式）")

    if args.style not in enhancer.STYLE_MAP:
        keys = ", ".join(enhancer.STYLE_MAP.keys())
        _log(f"❌ 未知样式：{args.style}")
        _log(f"   可用样式：{keys}")
        sys.exit(1)

    if not os.path.exists(args.html):
        _log(f"❌ 文件不存在：{args.html}")
        sys.exit(1)

    with open(args.html, encoding="utf-8", errors="replace") as f:
        html = f.read()

    source_label = os.path.basename(args.html)
    enhanced, backup = enhancer.enhance(
        html, args.style, source_label, strip_inline=args.strip_inline
    )

    out = args.output or args.html
    with open(out, "w", encoding="utf-8") as f:
        f.write(enhanced)

    style_name = enhancer.STYLE_MAP[args.style]
    print(f"✅ 已应用样式「{style_name}」({args.style}) → {out}")
    _log(f"   备份：{backup}")


if __name__ == "__main__":
    main()
