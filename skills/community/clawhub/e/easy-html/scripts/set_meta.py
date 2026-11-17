#!/usr/bin/env python3
"""
set_meta.py — 设置/替换 HTML 的 <title> 和 favicon

幂等地为一个 HTML 文件设置页面标题和 favicon：
  - <title>：有则替换，无则插入到 <head> 内
  - favicon：有 <link rel="icon"> 则替换 href，无则插入

用法：
  python3 set_meta.py page.html --title "2026 上半年复盘"
  python3 set_meta.py page.html --title "月报" --favicon "data:image/svg+xml,..."
  python3 set_meta.py page.html --favicon "https://cdn.../icon.png"
  python3 set_meta.py page.html --title "x" --in-place      # 覆盖原文件（默认行为）
  python3 set_meta.py page.html --title "x" -o out.html      # 写到新文件

注意：
  - favicon 是可选的。不传 --favicon 不会动 favicon（交给浏览器默认值）。
  - 仅当 HTML 没有 <head> 时才会报错提示（应是异常 HTML）。
"""
import argparse
import re
import sys


_HEAD_OPEN_RE = re.compile(r"<head[^>]*>", re.IGNORECASE)
_TITLE_RE = re.compile(r"<title[^>]*>.*?</title>", re.IGNORECASE | re.DOTALL)
_ICON_LINK_RE = re.compile(
    r'<link[^>]*\brel=["\']?(?:shortcut\s+)?icon["\']?[^>]*>',
    re.IGNORECASE,
)


def _esc_title(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def set_title(html, title):
    tag = f"<title>{_esc_title(title)}</title>"
    if _TITLE_RE.search(html):
        return _TITLE_RE.sub(tag, html, count=1)
    # 无 title：插到 <head> 开标签之后
    m = _HEAD_OPEN_RE.search(html)
    if m:
        idx = m.end()
        return html[:idx] + "\n" + tag + html[idx:]
    return None  # 没有 head


def set_favicon(html, href):
    # href 用单引号包裹，data URI 里可能含双引号
    safe_href = href.replace("'", "&#39;")
    tag = f"<link rel='icon' href='{safe_href}'>"
    if _ICON_LINK_RE.search(html):
        return _ICON_LINK_RE.sub(tag, html, count=1)
    m = _HEAD_OPEN_RE.search(html)
    if m:
        idx = m.end()
        return html[:idx] + "\n" + tag + html[idx:]
    return None


def main():
    ap = argparse.ArgumentParser(description="设置 HTML 的 title 和 favicon")
    ap.add_argument("html", help="HTML 文件路径")
    ap.add_argument("--title", help="页面标题")
    ap.add_argument("--favicon", help="favicon URL 或 data URI（不传则不改 favicon）")
    ap.add_argument("-o", "--output", help="输出文件（默认覆盖原文件）")
    ap.add_argument("--in-place", action="store_true", help="覆盖原文件（默认行为）")
    args = ap.parse_args()

    if not args.title and not args.favicon:
        ap.error("至少要提供 --title 或 --favicon 之一")

    with open(args.html, encoding="utf-8", errors="replace") as f:
        html = f.read()

    changed = []
    if args.title:
        new = set_title(html, args.title)
        if new is None:
            print("ERROR: HTML 中没有 <head>，无法插入 <title>", file=sys.stderr)
            sys.exit(1)
        html = new
        changed.append("title")
    if args.favicon:
        new = set_favicon(html, args.favicon)
        if new is None:
            print("ERROR: HTML 中没有 <head>，无法插入 favicon", file=sys.stderr)
            sys.exit(1)
        html = new
        changed.append("favicon")

    out = args.output or args.html
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 已更新 {', '.join(changed)} → {out}")


if __name__ == "__main__":
    main()
