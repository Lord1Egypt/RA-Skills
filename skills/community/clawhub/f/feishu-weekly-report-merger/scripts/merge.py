#!/usr/bin/env python3
"""
feishu_weekly_report_merge.py
按章节维度原地拼接多份周报文档的原文，不修改、不总结、保留全部格式标签。
"""

import sys
import re

PART_PATTERN = re.compile(
    r"^#\s*\**\s*Part\s*([1-5])[\s　:：]*【(.+?)】.*$",
    re.UNICODE | re.MULTILINE
)

SECTION_NAMES = {
    1: "AI优先：本周核心工作复盘总结",
    2: "学习心得：AI 认知迭代与能力进阶",
    3: "本周工作总结",
    4: "下周工作计划",
    5: "关键经营指标",
}

def extract_parts(markdown_text: str) -> dict[int, str]:
    parts = {}
    matches = list(PART_PATTERN.finditer(markdown_text))
    for i, m in enumerate(matches):
        part_num = int(m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown_text)
        parts[part_num] = markdown_text[start:end]
    return parts

def normalize_part_header(part_num: int) -> str:
    name = SECTION_NAMES.get(part_num, f"Part{part_num}")
    return f"# **Part{part_num}：【{name}】**"

def merge(name_path_pairs: list[tuple[str, str]]) -> str:
    doc_parts_list: list[tuple[str, dict[int, str]]] = []
    for name, path in name_path_pairs:
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            parts = extract_parts(text)
            doc_parts_list.append((name, parts))
        except FileNotFoundError:
            print(f"警告：未找到文件 '{path}' (对应姓名: {name})，已跳过该文件。", file=sys.stderr)
            continue
        except Exception as e:
            print(f"警告：读取文件 '{path}' 时发生错误：{e}，已跳过该文件。", file=sys.stderr)
            continue

    lines = []
    for part_num in sorted(SECTION_NAMES.keys()):
        lines.append(normalize_part_header(part_num))
        lines.append("")
        lines.append("---")
        lines.append("")

        for name, doc_parts in doc_parts_list:
            if part_num not in doc_parts:
                continue

            content = doc_parts[part_num]
            m = PART_PATTERN.search(content)
            if m:
                after_header = content[m.end():]
            else:
                after_header = content
            
            # 【修复点1】只去掉开头的换行符，保留正文开头的空格(防止破坏缩进引用和代码块)
            after_header = after_header.lstrip('\r\n')

            # 去掉末尾的 --- 行（原文 Part 之间分隔线），限制必须是独立的一行分隔线
            after_header = re.sub(r'\n[ \t]*[-─]{3,}[ \t]*(?:\n[ \t]*)*$', '', after_header)
            
            # 【修复点2】只去掉末尾的换行符，保留可能存在的 Markdown 行尾双空格
            after_header = after_header.rstrip('\r\n')

            lines.append(f"## 【{name}】")
            lines.append("")
            if after_header:
                lines.append(after_header)
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 merge.py \"姓名1/姓名2/姓名3\" \"姓名1\" doc1.md \"姓名2\" doc2.md ...", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]
    args = sys.argv[2:]
    if len(args) % 2 != 0:
        print("错误：参数数量应为偶数（姓名 + 路径交替）", file=sys.stderr)
        sys.exit(1)

    name_path_pairs = list(zip(args[::2], args[1::2]))

    header = f"**[AIO]-[{title}]**"
    body = merge(name_path_pairs)
    output = f"{header}\n\n{body}"
    print(output)