#!/usr/bin/env python3
"""
make_favicon.py — 用 emoji 或单字生成 favicon（零依赖）

把一个 emoji（如 📊）或一个汉字/字母生成一个 SVG data URI，
可直接作为 <link rel="icon" href="..."> 的值，无需上传 CDN、无外部依赖。

用法：
  python3 make_favicon.py --emoji 📊
  python3 make_favicon.py --text 红 --bg "#FF2442" --fg "#FFFFFF"
  python3 make_favicon.py --emoji 📈 --as-link    # 直接输出 <link> 标签

输出（默认）：data URI 字符串（stdout 一行）
  data:image/svg+xml,<svg ...>

说明：
  - FavIcon 是可选的。easy-html 默认可跳过（不设时浏览器用默认图标）。
  - 仅当用户想要一个简单的 emoji/字符图标、又不想上传图片时用本脚本。
  - 想用图片做 favicon → 先把图片传到任意可访问图床，再把 URL 传给 set_meta.py --favicon。
"""
import argparse
import sys
from urllib.parse import quote


def build_svg(content, bg=None, fg="#FFFFFF", rounded=True):
    """生成一个 64x64 SVG。content 为 emoji 或单字。

    bg=None 且是 emoji 时透明背景（emoji 自带色）；
    指定 bg 时画圆角底 + 居中文字。
    """
    if bg:
        rx = 14 if rounded else 0
        rect = (f'<rect width="64" height="64" rx="{rx}" fill="{bg}"/>')
        text = (f'<text x="32" y="33" font-size="38" text-anchor="middle" '
                f'dominant-baseline="central" fill="{fg}" '
                f'font-family="PingFang SC,-apple-system,Segoe UI,sans-serif" '
                f'font-weight="700">{content}</text>')
        inner = rect + text
    else:
        # 透明底，纯 emoji
        text = (f'<text x="32" y="34" font-size="48" text-anchor="middle" '
                f'dominant-baseline="central">{content}</text>')
        inner = text
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="0 0 64 64" width="64" height="64">{inner}</svg>')
    return svg


def to_data_uri(svg):
    # SVG data URI：用 utf8 + URL 编码，兼容性好于 base64 且可读
    return "data:image/svg+xml,%s" % quote(svg, safe="")


def main():
    ap = argparse.ArgumentParser(description="生成 emoji/单字 favicon (SVG data URI)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--emoji", help="一个 emoji，如 📊")
    g.add_argument("--text", help="一个汉字或字母，如 红 / A")
    ap.add_argument("--bg", default=None, help="背景色 hex（emoji 默认透明；text 默认 #FF2442）")
    ap.add_argument("--fg", default="#FFFFFF", help="前景/文字色 hex（默认白）")
    ap.add_argument("--as-link", action="store_true", help="输出完整 <link rel=icon> 标签")
    args = ap.parse_args()

    if args.emoji:
        content = args.emoji.strip()[:2]  # emoji 可能是双码点
        bg = args.bg  # emoji 默认透明
    else:
        content = args.text.strip()[:1]
        bg = args.bg or "#FF2442"

    if not content:
        print("ERROR: emoji/text 不能为空", file=sys.stderr)
        sys.exit(1)

    svg = build_svg(content, bg=bg, fg=args.fg)
    uri = to_data_uri(svg)
    if args.as_link:
        print(f'<link rel="icon" href="{uri}">')
    else:
        print(uri)


if __name__ == "__main__":
    main()
