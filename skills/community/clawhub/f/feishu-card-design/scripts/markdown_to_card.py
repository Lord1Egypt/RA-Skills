#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feishu-card-design Markdown → Card 2.0 转换器

把一份 Markdown 文档转换为飞书 Card 2.0 JSON.
适合 Agent 用 markdown 写报告, 然后一键转卡片推送.

转换规则:
  - 第一个 # 一级标题  → header.title
  - 第二个 # 一级标题或第一行  → header.subtitle (若存在)
  - ## 二级标题 + 段落    → column_block (主推色 blue-50)
  - ### 三级标题 + 段落   → column_block (亮点色 yellow-50)
  - > 引用块              → column_block (亮点色 yellow-50)
  - ``` 代码块            → column_block (中性色 grey-50)
  - 表格                  → column_block (统计色 grey-50)
  - 普通段落              → markdown 元素 (无背景)
  - 分隔线 ---            → hr 元素

色系规则:
  - 默认 header.template = 'blue', 可通过 --template 切换
  - 自动根据 template 校验 background_style 是否在邻近色环内
  - 若不合规, fallback 到 'default'

用法:
    python markdown_to_card.py report.md --template blue --title "..." --doc-url "..."
    python markdown_to_card.py report.md --output card.json
    cat report.md | python markdown_to_card.py --stdin --template green

输出:
    Card 2.0 JSON 到 stdout, 或写入 --output 指定文件
"""
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Optional

# 复用 card_builder 的函数
sys.path.insert(0, str(Path(__file__).parent))
from card_builder import (
    build_card, header, markdown, column_block, hr, button, note,
    ALLOWED_TEMPLATES, _check_bg_color, CardBuildError,
)


# ============================================================
# Markdown 解析 (轻量级, 不依赖第三方库)
# ============================================================

def parse_markdown(md_text: str) -> dict:
    """解析 Markdown, 返回结构化 dict

    Returns:
        {
            "h1": [str],           # 所有一级标题
            "h2": [{"title", "body"}],  # 二级标题 + 正文
            "h3": [{"title", "body"}],  # 三级标题 + 正文
            "quotes": [str],       # 引用块
            "code_blocks": [str],  # 代码块
            "tables": [str],       # 表格 (整段文本)
            "paragraphs": [str],   # 普通段落
            "hrs": [int],          # 分隔线位置 (顺序索引)
        }
    """
    result = {
        "h1": [], "h2": [], "h3": [],
        "quotes": [], "code_blocks": [],
        "tables": [], "paragraphs": [], "hrs": [],
    }
    lines = md_text.split("\n")
    i = 0
    current_h2 = None
    current_h3 = None
    current_h2_body = []
    current_h3_body = []
    table_buffer = []

    def flush_h2():
        nonlocal current_h2, current_h2_body
        if current_h2:
            result["h2"].append({
                "title": current_h2,
                "body": "\n".join(current_h2_body).strip(),
            })
        current_h2 = None
        current_h2_body = []

    def flush_h3():
        nonlocal current_h3, current_h3_body
        if current_h3:
            result["h3"].append({
                "title": current_h3,
                "body": "\n".join(current_h3_body).strip(),
            })
        current_h3 = None
        current_h3_body = []

    def flush_table():
        nonlocal table_buffer
        if table_buffer:
            result["tables"].append("\n".join(table_buffer))
        table_buffer = []

    while i < len(lines):
        line = lines[i]

        # 代码块
        if line.strip().startswith("```"):
            flush_h3()
            flush_h2()
            flush_table()
            code_lines = [line]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                code_lines.append(lines[i])  # 闭合 ```
                i += 1
            result["code_blocks"].append("\n".join(code_lines))
            continue

        # 一级标题
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            flush_h3()
            flush_h2()
            flush_table()
            result["h1"].append(m.group(1).strip())
            i += 1
            continue

        # 二级标题
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            flush_h3()
            flush_table()
            if current_h2:
                flush_h2()
            current_h2 = m.group(1).strip()
            current_h2_body = []
            i += 1
            continue

        # 三级标题
        m = re.match(r"^###\s+(.+?)\s*$", line)
        if m:
            flush_table()
            if current_h3:
                flush_h3()
            current_h3 = m.group(1).strip()
            current_h3_body = []
            i += 1
            continue

        # 分隔线
        if re.match(r"^---+\s*$", line) or re.match(r"^\*\*\*+\s*$", line):
            flush_h3()
            flush_h2()
            flush_table()
            result["hrs"].append(len(result["paragraphs"]) + len(result["h2"]) + len(result["h3"]))
            i += 1
            continue

        # 引用块
        m = re.match(r"^>\s?(.*)$", line)
        if m:
            flush_h3()
            flush_h2()
            flush_table()
            quote_lines = [m.group(1)]
            i += 1
            while i < len(lines) and (m := re.match(r"^>\s?(.*)$", lines[i])):
                quote_lines.append(m.group(1))
                i += 1
            result["quotes"].append("\n".join(quote_lines))
            continue

        # 表格 (| ... |)
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            flush_h3()
            flush_h2()
            table_buffer.append(line)
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_buffer.append(lines[i])
                i += 1
            flush_table()
            continue

        # 普通段落 (归属到当前 h2/h3 或独立段落)
        if current_h3:
            current_h3_body.append(line)
        elif current_h2:
            current_h2_body.append(line)
        elif line.strip():
            flush_table()
            result["paragraphs"].append(line)

        i += 1

    flush_h3()
    flush_h2()
    flush_table()
    return result


# ============================================================
# 转换器
# ============================================================

def convert(md_text: str,
            template: str = "blue",
            override_title: Optional[str] = None,
            override_subtitle: Optional[str] = None,
            doc_url: Optional[str] = None,
            footer: Optional[str] = None) -> dict:
    """把 Markdown 转换为 Card 2.0 JSON

    Args:
        md_text: Markdown 文本
        template: header.template, 决定邻近色环
        override_title: 覆盖标题 (不传则用第一个 # 一级标题)
        override_subtitle: 覆盖副标题
        doc_url: 「查看完整云文档」按钮 URL
        footer: footer note 内容

    Returns:
        Card 2.0 dict
    """
    if template not in ALLOWED_TEMPLATES:
        raise CardBuildError(f"template={template!r} 不在允许列表")

    parsed = parse_markdown(md_text)

    # 标题
    title = override_title or (parsed["h1"][0] if parsed["h1"] else "未命名报告")
    subtitle = override_subtitle
    if not subtitle and len(parsed["h1"]) > 1:
        subtitle = parsed["h1"][1]
    elif not subtitle and parsed["h2"]:
        subtitle = parsed["h2"][0]["title"]

    elements = []

    # 选择 bg_color (带邻近色环校验)
    def safe_bg(target: str) -> str:
        try:
            _check_bg_color(target, template)
            return target
        except CardBuildError:
            return "default"

    main_bg = safe_bg(f"{template}-50")  # 主推色
    highlight_bg = "yellow-50"           # 亮点色 (黄色与所有色系邻近)
    stat_bg = "grey-50"                  # 统计色 (中性)

    # 普通段落先放 (开场段落, 不加背景色)
    for p in parsed["paragraphs"]:
        if p.strip():
            elements.append(markdown(p))

    # 二级标题块 → 主推色 column_block
    for h2 in parsed["h2"]:
        content = f"## {h2['title']}\n\n{h2['body']}" if h2["body"] else f"## {h2['title']}"
        if h2["body"]:
            content = f"**{h2['title']}**\n\n{h2['body']}"
        else:
            content = f"**{h2['title']}**"
        elements.append(hr() if elements else None) if elements else None
        elements.append(column_block(content, bg_color=main_bg, header_template=template))

    # 三级标题块 → 亮点色 column_block
    for h3 in parsed["h3"]:
        if h3["body"]:
            content = f"**{h3['title']}**\n\n{h3['body']}"
        else:
            content = f"**{h3['title']}**"
        elements.append(column_block(content, bg_color=highlight_bg, header_template=template))

    # 引用块 → 亮点色 column_block
    for q in parsed["quotes"]:
        elements.append(column_block(f"> {q}", bg_color=highlight_bg, header_template=template))

    # 代码块 → 统计色 column_block
    for code in parsed["code_blocks"]:
        elements.append(column_block(code, bg_color=stat_bg, header_template=template))

    # 表格 → 统计色 column_block
    for table in parsed["tables"]:
        elements.append(column_block(table, bg_color=stat_bg, header_template=template))

    # 去掉 None (filter)
    elements = [e for e in elements if e is not None]

    # 行动按钮
    if doc_url:
        elements.append(hr())
        elements.append(button("📄 查看完整云文档", url=doc_url, button_type="primary"))

    # footer
    if footer:
        elements.append(note(footer))

    return build_card(
        header=header(title, template=template, subtitle=subtitle),
        elements=elements,
    )


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="feishu-card-design Markdown → Card 2.0 转换器"
    )
    parser.add_argument("input", nargs="?", help="Markdown 文件路径 (留空则读 stdin)")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读 Markdown")
    parser.add_argument("--template", default="blue",
                        choices=sorted(ALLOWED_TEMPLATES),
                        help="header.template (默认 blue)")
    parser.add_argument("--title", help="覆盖标题")
    parser.add_argument("--subtitle", help="覆盖副标题")
    parser.add_argument("--doc-url", help="查看完整云文档按钮 URL")
    parser.add_argument("--footer", help="footer note 内容")
    parser.add_argument("--output", "-o", help="输出文件路径 (留空则 stdout)")
    args = parser.parse_args()

    # 读 Markdown
    if args.stdin or not args.input:
        md_text = sys.stdin.read()
    else:
        md_text = Path(args.input).read_text(encoding="utf-8")

    # 转换
    try:
        card = convert(
            md_text,
            template=args.template,
            override_title=args.title,
            override_subtitle=args.subtitle,
            doc_url=args.doc_url,
            footer=args.footer,
        )
    except CardBuildError as e:
        print(f"❌ 转换失败: {e}", file=sys.stderr)
        sys.exit(2)

    # 输出
    out = json.dumps(card, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"✅ 已写入 {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
