#!/usr/bin/env python3
"""
parse_openeuler_md.py - 解析 OpenEuler 安全配置基线 Markdown 文档

从 MD 文件中提取安全配置条目（配置项路径、参数名、期望值等），
输出结构化的 JSON 文件供后续覆盖分析使用。

用法:
    python parse_openeuler_md.py <openeuler-md-path> -o <output-json-path>
"""

import re
import json
import argparse
import sys
from pathlib import Path


def parse_md_baseline(md_path: str) -> list:
    """
    解析 OpenEuler 安全配置基线 MD 文件。
    提取策略：
    1. 查找 Markdown 标题（# / ## / ###）作为条目分类
    2. 在段落和表格中搜索配置路径（如 /etc/xxx.conf）
    3. 提取参数名和期望值
    4. 根据上下文自动推断覆盖范围
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    items = []
    lines = content.split("\n")

    current_section = ""
    current_subsection = ""

    # 识别表格区域
    in_table = False
    table_headers = []
    table_rows = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 记录当前章节
        header_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if header_match:
            level = len(header_match.group(1))
            title = header_match.group(2)
            if level <= 2:
                current_section = title
                current_subsection = ""
            else:
                current_subsection = title

            # 遇到标题时，结束当前表格
            if in_table and table_rows:
                _extract_items_from_table(items, table_headers, table_rows,
                                          current_section, current_subsection)
                table_rows = []
                in_table = False
            continue

        # 检测表格开始
        if '|' in stripped and '-' not in stripped and not in_table:
            cols = [c.strip() for c in stripped.split('|') if c.strip()]
            if len(cols) >= 2:
                table_headers = cols
                in_table = True
            continue

        # 检测表格分隔行
        if in_table and stripped.startswith('|') and re.match(r'^[\s|:\-]+$', stripped):
            continue

        # 表格数据行
        if in_table and '|' in stripped:
            cols = [c.strip() for c in stripped.split('|') if c.strip()]
            if len(cols) >= 2 and cols != table_headers:
                table_rows.append(cols)
            continue
        else:
            if in_table and table_rows:
                _extract_items_from_table(items, table_headers, table_rows,
                                          current_section, current_subsection)
                table_rows = []
            in_table = False

        # 非表格行：尝试提取配置路径
        if not in_table:
            _extract_items_from_text(items, stripped, current_section,
                                     current_subsection, i, lines)

    # 处理文件末尾残留的表格
    if in_table and table_rows:
        _extract_items_from_table(items, table_headers, table_rows,
                                  current_section, current_subsection)

    return items


def _extract_items_from_table(items: list, headers: list, rows: list,
                               section: str, subsection: str):
    """从 Markdown 表格中提取配置项"""
    # 尝试识别常见列名
    col_indices = {
        "path": -1,
        "param": -1,
        "value": -1,
        "desc": -1,
    }
    for idx, h in enumerate(headers):
        h_lower = h.lower()
        if any(k in h_lower for k in ["路径", "配置项", "文件", "path", "file", "配置路径"]):
            col_indices["path"] = idx
        elif any(k in h_lower for k in ["参数", "键", "key", "param", "parameter", "选项"]):
            col_indices["param"] = idx
        elif any(k in h_lower for k in ["值", "配置值", "期望", "value", "setting", "值要求"]):
            col_indices["value"] = idx
        elif any(k in h_lower for k in ["说明", "描述", "desc", "description", "备注"]):
            col_indices["desc"] = idx

    for row in rows:
        item = {
            "item_id": "",
            "config_path": "",
            "config_param": "",
            "expected_value": "",
            "description": ""
        }

        if col_indices["path"] >= 0 and col_indices["path"] < len(row):
            item["config_path"] = row[col_indices["path"]]
        if col_indices["param"] >= 0 and col_indices["param"] < len(row):
            item["config_param"] = row[col_indices["param"]]
        if col_indices["value"] >= 0 and col_indices["value"] < len(row):
            item["expected_value"] = row[col_indices["value"]]
        if col_indices["desc"] >= 0 and col_indices["desc"] < len(row):
            item["description"] = row[col_indices["desc"]]

        # 填充章节信息作为 item_id
        if section:
            item["item_id"] = f"{section}"
            if subsection:
                item["item_id"] += f" / {subsection}"

        # 清理路径中的多余空格
        item["config_path"] = item["config_path"].strip()
        item["config_param"] = item["config_param"].strip()
        item["expected_value"] = item["expected_value"].strip()

        if item["config_path"]:  # 至少要有路径
            items.append(item)


def _extract_items_from_text(items: list, line: str, section: str,
                              subsection: str, line_num: int, all_lines: list):
    """从非表格文本行中提取配置项"""
    # 匹配配置路径模式
    path_patterns = [
        r'(/\S+(?:/\S+)*\.(?:conf|cfg|ini|cnf|rule|service|sh|policy|xml|yaml|yml|txt|allow|deny))',
        r'(/etc/\S+(?:/\S+)*)',
        r'(/opt/\S+(?:/\S+)*)',
        r'(/usr/\S+(?:/\S+)*)',
        r'(/var/\S+(?:/\S+)*)',
        r'(/boot/\S+(?:/\S+)*)',
        r'(/proc/\S+(?:/\S+)*)',
        r'(/sys/\S+(?:/\S+)*)',
        r'(/selinux/\S+)',
    ]

    for pattern in path_patterns:
        path_match = re.search(pattern, line)
        if path_match:
            config_path = path_match.group(1).strip()

            # 避免重复
            if any(i["config_path"] == config_path for i in items):
                continue

            # 尝试提取参数名和值（key = value, key: value, key value）
            param_value = re.findall(
                r'(\w[\w._-]*)\s*[=:]\s*("?[^"=\s]+"?|[0-9]+)', line)

            item = {
                "item_id": f"{section}/L{line_num}" if section else f"L{line_num}",
                "config_path": config_path,
                "config_param": param_value[0][0] if param_value else "",
                "expected_value": param_value[0][1].strip('"') if param_value else "",
                "description": line.strip()[:120]
            }

            # 读取下一行以获取更完整的值
            if line_num + 1 < len(all_lines):
                next_line = all_lines[line_num + 1].strip()
                # 如果下一行看起来是续行（缩进或键值）
                if next_line and re.match(r'^\s+\S', next_line):
                    item["description"] = (
                        item["description"] + " " + next_line)[:140]

            items.append(item)
            break  # 只匹配第一个路径


def main():
    parser = argparse.ArgumentParser(
        description="解析 OpenEuler 安全配置基线 Markdown 文件")
    parser.add_argument("md_path", help="OpenEuler 安全基线 MD 文件路径")
    parser.add_argument("-o", "--output", default="openeuler_items.json",
                        help="输出 JSON 文件路径 (默认: openeuler_items.json)")
    args = parser.parse_args()

    md_path = Path(args.md_path)
    if not md_path.exists():
        print(f"错误: 文件不存在: {md_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] 读取 MD 基线: {md_path}")
    items = parse_md_baseline(str(md_path))
    print(f"    - 提取条目: {len(items)} 条")

    # 输出 JSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"[✓] 基线条目已保存: {output_path}")
    for item in items[:3]:
        print(f"    示例: [{item['config_path']}] {item['description'][:60]}")


if __name__ == "__main__":
    main()
