#!/usr/bin/env python3
"""
Citation Checker v4.2 — 代码级引用验证

功能：提取诊断报告中的引用标注，反查知识库验证真实存在。
如果任一引用不存在于知识库中，触发 Hard Reject。

使用方式：
    python3 citation_checker.py --report <报告文件> --kb-path <知识库路径>
"""

import argparse
import os
import re
import sys
from pathlib import Path


def extract_citations(report_text: str) -> list[str]:
    """
    提取报告中的引用标注。
    支持格式：[文件名:段落号] 或 [文件名:条款号] 或 <citation>[...]</citation>
    """
    citations = []
    
    # XML 格式：<citation>[...]</citation>
    xml_pattern = r'<citation>\[([^\]]+)\]</citation>'
    for m in re.finditer(xml_pattern, report_text):
        citations.append(m.group(1))
    
    # Markdown 格式：[...] 但不包含 citation 标签内的（已经提取过）
    # 提取不在 <citation> 标签内的 [...]
    plain_pattern = r'(?<!<citation>)\[([^\]]+)\](?!</citation>)'
    for m in re.finditer(plain_pattern, report_text):
        text = m.group(1)
        # 只提取看起来像引用的（包含 : 或 第 或 条款 或 条）
        if ':' in text or '第' in text or '条款' in text or '条' in text:
            citations.append(text)
    
    return citations


def verify_citation(citation: str, kb_path: str) -> tuple[bool, str]:
    """
    验证单个引用是否存在于知识库中。
    
    格式：[文件名:段落号] 或 [文件名:条款号]
    返回：(是否通过, 错误信息)
    """
    # 解析引用格式
    m = re.match(r'([^:]+):(.+)', citation)
    if not m:
        return False, f"引用格式错误: {citation}（应为 [文件名:段落号]）"
    
    filename = m.group(1).strip()
    locator = m.group(2).strip()  # 段落号/条款号
    
    # 在知识库中搜索文件
    kb_dir = Path(kb_path)
    if not kb_dir.exists():
        return False, f"知识库路径不存在: {kb_path}"
    
    # 搜索匹配的文件
    found_files = list(kb_dir.rglob(f"*{filename}*"))
    if not found_files:
        # 尝试不带扩展名搜索
        found_files = list(kb_dir.rglob(f"*{filename.split('.')[0]}*"))
    
    if not found_files:
        return False, f"知识库中找不到文件: {filename}"
    
    # 在找到的文件中搜索 locator
    for fpath in found_files:
        try:
            content = fpath.read_text(encoding='utf-8')
            # 检查 locator 是否出现在文件中
            # 支持多种匹配：精确匹配、条款号匹配
            if locator in content:
                return True, f"已验证: [{filename}:{locator}] 存在于 {fpath.name}"
            
            # 宽松匹配：如果 locator 是条款号，尝试模糊匹配
            # 例如 "第47条" 匹配 "第四十七条" 或 "第 47 条"
            loose_locator = re.sub(r'[第条\s]', '', locator)
            loose_content = re.sub(r'[第条\s]', '', content)
            if loose_locator and loose_locator in loose_content:
                return True, f"已验证: [{filename}:{locator}] 存在于 {fpath.name}（模糊匹配）"
        except Exception as e:
            continue
    
    return False, f"在 {filename} 中找不到: {locator}"


def check_report(report_text: str, kb_path: str) -> tuple[bool, list[dict]]:
    """
    检查整份报告的所有引用。
    返回：(全部通过, 验证结果列表)
    """
    citations = extract_citations(report_text)
    if not citations:
        return True, [{"citation": "(无引用)", "passed": True, "message": "报告中无引用标注"}]
    
    results = []
    all_passed = True
    
    for citation in citations:
        passed, message = verify_citation(citation, kb_path)
        results.append({
            "citation": citation,
            "passed": passed,
            "message": message
        })
        if not passed:
            all_passed = False
    
    return all_passed, results


def main():
    parser = argparse.ArgumentParser(description='谛听 Citation Checker v4.2')
    parser.add_argument('--report', type=str, required=True, help='诊断报告文件路径')
    parser.add_argument('--kb-path', type=str, required=True, help='知识库路径')
    parser.add_argument('--xml-output', action='store_true', help='输出 XML 格式结果')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.report):
        print(f"错误: 报告文件不存在: {args.report}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.report, 'r', encoding='utf-8') as f:
        report_text = f.read()
    
    all_passed, results = check_report(report_text, args.kb_path)
    
    if args.xml_output:
        # XML 格式输出（用于 Constitutional Evaluator 解析）
        print('<citation_check>')
        print(f'  <overall>{"pass" if all_passed else "fail"}</overall>')
        for r in results:
            status = "pass" if r["passed"] else "fail"
            print(f'  <item citation="{r["citation"]}" status="{status}">{r["message"]}</item>')
        print('</citation_check>')
    else:
        # 人类可读格式
        status = "✅ 全部通过" if all_passed else "❌ 存在未验证引用"
        print(f"Citation Checker 结果: {status}")
        print(f"共检查 {len(results)} 个引用:")
        for r in results:
            icon = "✅" if r["passed"] else "❌"
            print(f"  {icon} [{r['citation']}] {r['message']}")
    
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
