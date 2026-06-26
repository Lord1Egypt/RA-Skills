#!/usr/bin/env python3
"""
Markdown / 纯文本文档格式校正脚本
功能：修正 Markdown 文本的排版格式，不改动文字内容。
"""

import sys
import re
from pathlib import Path


def fix_markdown(text: str) -> tuple[str, list[str]]:
    """校正 Markdown 格式，返回 (修正后文本, 调整项列表)"""
    changes = []
    lines = text.split('\n')
    result = []
    prev_empty = False

    for line in lines:
        stripped = line.rstrip()

        # 1. 去除行尾多余空格
        if line != stripped:
            changes.append("行尾多余空格已清除")

        # 2. 合并连续空行（最多保留一个空行）
        is_empty = stripped == ''
        if is_empty and prev_empty:
            prev_empty = True
            continue
        prev_empty = is_empty

        # 3. 标题前后确保空行
        if re.match(r'^#{1,6}\s', stripped):
            if result and result[-1] != '':
                result.append('')
                changes.append("标题前补充空行")
            result.append(stripped)
            continue

        # 4. 列表项缩进统一为 2/4 空格倍数
        list_match = re.match(r'^(\s+)([-*+]|\d+[.\)])\s', stripped)
        if list_match:
            indent = len(list_match.group(1))
            normalized = (indent // 2) * 2 or 4
            if indent != normalized:
                stripped = ' ' * normalized + stripped.lstrip()
                changes.append("列表缩进已对齐")

        # 5. 中英文之间加空格（可选，默认关闭以遵守"不改动文字"原则）
        # 此处不执行，保持原文

        result.append(stripped)

    # 6. 文件末尾确保换行
    if result and result[-1] != '':
        result.append('')
        changes.append("文件末尾补充换行")

    # 去重 changes
    seen = set()
    unique_changes = []
    for c in changes:
        if c not in seen:
            seen.add(c)
            unique_changes.append(c)

    return '\n'.join(result), unique_changes


def main():
    if len(sys.argv) < 3:
        print("用法: python fix_markdown.py <输入文件> <输出文件>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    text = Path(input_path).read_text(encoding='utf-8')
    fixed, changes = fix_markdown(text)

    Path(output_path).write_text(fixed, encoding='utf-8')
    print(f"✅ 格式校正完成，输出文件: {output_path}")
    if changes:
        print("调整项目:")
        for c in changes:
            print(f"  • {c}")
    else:
        print("无需调整，格式已规范")


if __name__ == "__main__":
    main()
