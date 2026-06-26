#!/usr/bin/env python3
"""
parse_cis_pdf.py - 从 CIS RHEL Benchmark PDF 中提取安全规则清单

从 PDF 中提取规则编号、标题、配置项路径、参数名、期望值等字段，
输出结构化的 JSON 文件供后续覆盖分析使用。

用法:
    python parse_cis_pdf.py <cis-pdf-path> -o <output-json-path>
"""

import re
import json
import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("错误: 需要 pdfplumber。请运行: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """读取 PDF 全文，返回拼接文本"""
    text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_pages.append(page_text)
    return "\n".join(text_pages)


def extract_tables_from_pdf(pdf_path: str) -> list:
    """读取 PDF 中的所有表格"""
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            for table in tables:
                all_tables.append({"page": page_num, "data": table})
    return all_tables


def parse_cis_rules(text: str, tables: list) -> list:
    """
    解析 CIS 规则清单。
    策略：
    1. 扫描正则模式如 "X.Y.Z Title" 的规则编号
    2. 从表格中提取详细配置参数
    3. 合并两者得到完整规则清单
    """
    rules = []

    # 模式 1：从正文中提取规则编号和标题
    # CIS 规则编号格式如：1.1.1.1, 1.2.3, 5.2.1 等
    rule_patterns = [
        (r'^(\d+(?:\.\d+)+)\s+(.+)$', re.MULTILINE),          # "1.1.1.1 Ensure ..."
        (r'^(\d+(?:\.\d+)+)\n+\s*(.+)$', re.MULTILINE),        # 跨行
    ]

    seen_rules = {}  # rule_id -> {title, level, scoring}
    for pattern, flags in rule_patterns:
        for match in re.finditer(pattern, text, flags):
            rule_id = match.group(1).strip()
            title = match.group(2).strip()
            if rule_id not in seen_rules:
                seen_rules[rule_id] = {
                    "rule_id": rule_id,
                    "title": title,
                    "config_path": "",
                    "config_param": "",
                    "expected_value": "",
                    "level": "",
                    "scoring": ""
                }

    # 尝试提取级别信息(Level 1 / Level 2)
    for rule_id in seen_rules:
        # 在规则附近搜索 "Level 1" 或 "Level 2"
        pattern = re.escape(rule_id) + r'.*?(Level\s+\d)'
        m = re.search(pattern, text, re.DOTALL)
        if m:
            seen_rules[rule_id]["level"] = m.group(1)

        # 搜索评分状态 (Scored / Not Scored)
        scoring_p = re.escape(rule_id) + r'.*?(Scored|Not\s+Scored)'
        m = re.search(scoring_p, text, re.DOTALL)
        if m:
            seen_rules[rule_id]["scoring"] = m.group(1)

    # 模式 2：从表格中提取配置参数
    for table_info in tables:
        for row in table_info["data"]:
            if not row or len(row) < 2:
                continue
            row_text = " ".join([str(c or "") for c in row]).strip()
            # 查找配置路径
            path_match = re.search(r'(/\S+(?:/\S+)+)', row_text)
            if not path_match:
                continue
            config_path = path_match.group(1)

            # 尝试匹配规则编号
            rule_id_match = re.search(r'(\d+(?:\.\d+)+)', row_text)
            rule_id = rule_id_match.group(1) if rule_id_match else ""

            # 提取参数名和值
            param_value = re.findall(r'(\w[\w._-]*)\s*[=:]\s*(\S+)', row_text)

            # 如果已有匹配规则，更新配置参数
            if rule_id and rule_id in seen_rules:
                seen_rules[rule_id]["config_path"] = config_path
                if param_value:
                    seen_rules[rule_id]["config_param"] = param_value[0][0]
                    seen_rules[rule_id]["expected_value"] = param_value[0][1]
            elif not rule_id:
                # 无规则编号的配置项，尝试创建新条目
                key = config_path
                if key not in seen_rules:
                    seen_rules[key] = {
                        "rule_id": "",
                        "title": "",
                        "config_path": config_path,
                        "config_param": param_value[0][0] if param_value else "",
                        "expected_value": param_value[0][1] if param_value else "",
                        "level": "",
                        "scoring": ""
                    }

    # 清理无意义数据项
    rules = [v for v in seen_rules.values()
             if v["rule_id"] or v["config_path"]]

    return rules


def main():
    parser = argparse.ArgumentParser(
        description="从 CIS RHEL Benchmark PDF 中提取安全规则清单")
    parser.add_argument("pdf_path", help="CIS Benchmark PDF 文件路径")
    parser.add_argument("-o", "--output", default="cis_rules.json",
                        help="输出 JSON 文件路径 (默认: cis_rules.json)")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"错误: 文件不存在: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] 读取 PDF: {pdf_path}")
    text = extract_text_from_pdf(str(pdf_path))
    tables = extract_tables_from_pdf(str(pdf_path))
    print(f"    - 文本长度: {len(text):,} 字符")
    print(f"    - 提取表格: {len(tables)} 个")

    print("[*] 解析规则...")
    rules = parse_cis_rules(text, tables)
    print(f"    - 提取规则: {len(rules)} 条")

    # 输出 JSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)

    print(f"[✓] 规则清单已保存: {output_path}")
    # 打印前几条示例
    for r in rules[:3]:
        print(f"    示例: [{r['rule_id']}] {r['title'][:60]}")


if __name__ == "__main__":
    main()
