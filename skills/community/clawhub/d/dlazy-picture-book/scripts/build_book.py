#!/usr/bin/env python3
"""把 book.json 注入绘本模版，生成可独立打开的 index.html。

用法:
    python build_book.py <book.json> [-o index.html] [-t template.html]

book.json 结构:
{
  "title":       "绘本标题",            # 必填
  "subtitle":    "副标题/一句话简介",    # 可选
  "cover_image": "images/cover.png",    # 可选，封面图（相对路径）
  "music":       "music/bgm.mp3",       # 可选，背景音乐（相对路径）
  "pages": [                            # 必填，每页一图一文
    {"image": "images/page-01.png", "text": "这一页的文字。可用 \\n 分段。"},
    ...
  ]
}

图片 / 音乐用相对路径引用（相对于 index.html），因此把 index.html、images/、music/
放在同一个输出文件夹里即可整体分享或预览。
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(HERE, "..", "assets", "template.html")
PLACEHOLDER = "__BOOK_DATA_JSON__"


def main():
    ap = argparse.ArgumentParser(description="Build a picture-book HTML from book.json")
    ap.add_argument("book", help="path to book.json")
    ap.add_argument("-o", "--output", default="index.html", help="output HTML path (default: index.html)")
    ap.add_argument("-t", "--template", default=DEFAULT_TEMPLATE, help="template.html path")
    args = ap.parse_args()

    with open(args.book, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("title"):
        sys.exit("error: book.json 缺少 title")
    pages = data.get("pages") or []
    if not pages:
        sys.exit("error: book.json 的 pages 为空")
    for i, p in enumerate(pages, 1):
        if not p.get("text"):
            print(f"warning: 第 {i} 页缺少 text", file=sys.stderr)

    with open(args.template, "r", encoding="utf-8") as f:
        template = f.read()
    if PLACEHOLDER not in template:
        sys.exit(f"error: 模版中找不到占位符 {PLACEHOLDER}")

    # 用 </script> 转义避免 JSON 内容意外闭合脚本标签
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    html = template.replace(PLACEHOLDER, payload)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 已生成绘本：{args.output}（{len(pages)} 页）")


if __name__ == "__main__":
    main()
