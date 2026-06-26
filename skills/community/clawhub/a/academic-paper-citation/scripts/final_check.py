#!/usr/bin/env python3
"""
最终检查验证脚本
验证生成的论文是否符合要求
"""

import re
import json
from pathlib import Path

def load_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def count_chinese_chars(text):
    """统计中文字符数（不含标点）"""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)

def count_total_chars(text):
    """统计总字符数（含标点、空格）"""
    return len(text)

def extract_chapters(content):
    """提取章节结构"""
    chapters = []
    
    # 匹配各级标题
    h1_pattern = re.compile(r'^# (.+)$', re.MULTILINE)
    h2_pattern = re.compile(r'^## (.+)$', re.MULTILINE)
    h3_pattern = re.compile(r'^### (.+)$', re.MULTILINE)
    
    for match in h1_pattern.finditer(content):
        chapters.append({'level': 1, 'title': match.group(1).strip()})
    
    for match in h2_pattern.finditer(content):
        chapters.append({'level': 2, 'title': match.group(1).strip()})
    
    for match in h3_pattern.finditer(content):
        chapters.append({'level': 3, 'title': match.group(1).strip()})
    
    return chapters

def count_citations(content):
    """统计引用标记"""
    citations = re.findall(r'\[(\d+)\]', content)
    return {
        'total': len(citations),
        'unique': len(set(citations)),
        'ids': sorted(set([int(c) for c in citations]))
    }

def check_references_section(content):
    """检查参考文献章节"""
    has_ref_section = '参考文献' in content
    
    # 提取参考文献列表
    ref_pattern = r'参考文献\s*\n(.*?)(?=致谢|$)'
    match = re.search(ref_pattern, content, re.DOTALL)
    
    if match:
        ref_section = match.group(1)
        ref_count = len(re.findall(r'\[\d+\]', ref_section))
        return {'has_section': True, 'count': ref_count}
    
    return {'has_section': has_ref_section, 'count': 0}

def generate_report(original_md, enhanced_md, output_dir):
    """生成检查报告"""
    
    original_content = load_markdown(original_md)
    enhanced_content = load_markdown(enhanced_md)
    
    report = []
    report.append("=" * 60)
    report.append("论文生成质量检查报告")
    report.append("=" * 60)
    report.append("")
    
    # 1. 字数检查
    report.append("【1. 字数统计】")
    report.append("-" * 40)
    
    orig_total = count_total_chars(original_content)
    enh_total = count_total_chars(enhanced_content)
    orig_chinese = count_chinese_chars(original_content)
    enh_chinese = count_chinese_chars(enhanced_content)
    
    report.append(f"原始论文总字符数: {orig_total}")
    report.append(f"增强版论文总字符数: {enh_total}")
    report.append(f"原始论文中文字符数: {orig_chinese}")
    report.append(f"增强版论文中文字符数: {enh_chinese}")
    
    # 硕士论文通常要求3-5万字
    word_count_estimate = enh_chinese  # 中文字符数约等于字数
    report.append(f"估算字数（中文字符）: {word_count_estimate}")
    
    if word_count_estimate >= 50000:
        report.append(f"✅ 字数要求满足（≥50000字）")
    elif word_count_estimate >= 30000:
        report.append(f"⚠️ 字数接近要求（30000-50000字）")
    else:
        report.append(f"❌ 字数不足（<30000字）")
    report.append("")
    
    # 2. 章节结构检查
    report.append("【2. 章节结构检查】")
    report.append("-" * 40)
    
    orig_chapters = extract_chapters(original_content)
    enh_chapters = extract_chapters(enhanced_content)
    
    report.append(f"原始论文章节数: {len(orig_chapters)}")
    report.append(f"增强版论文章节数: {len(enh_chapters)}")
    
    if len(orig_chapters) == len(enh_chapters):
        report.append("✅ 章节结构保持一致")
    else:
        report.append("⚠️ 章节结构有变化")
    
    report.append("\n主要章节:")
    for chap in enh_chapters[:20]:  # 显示前20个章节
        indent = "  " * (chap['level'] - 1)
        report.append(f"{indent}{'#' * chap['level']} {chap['title']}")
    report.append("")
    
    # 3. 引用标记检查
    report.append("【3. 引用标记检查】")
    report.append("-" * 40)
    
    orig_citations = count_citations(original_content)
    enh_citations = count_citations(enhanced_content)
    
    report.append(f"原始论文引用标记数: {orig_citations['total']}")
    report.append(f"原始论文引用文献数: {orig_citations['unique']}")
    report.append(f"增强版论文引用标记数: {enh_citations['total']}")
    report.append(f"增强版论文引用文献数: {enh_citations['unique']}")
    
    if enh_citations['total'] > orig_citations['total']:
        report.append(f"✅ 新增引用标记: {enh_citations['total'] - orig_citations['total']} 处")
    report.append("")
    
    # 4. 参考文献检查
    report.append("【4. 参考文献检查】")
    report.append("-" * 40)
    
    ref_check = check_references_section(enhanced_content)
    report.append(f"参考文献章节: {'✅ 存在' if ref_check['has_section'] else '❌ 缺失'}")
    report.append(f"参考文献条目数: {ref_check['count']}")
    report.append("")
    
    # 5. 文件输出检查
    report.append("【5. 输出文件检查】")
    report.append("-" * 40)
    
    output_files = [
        ('论文初稿v5.0.docx', '/Users/openclaw2026/.qclaw/workspace/output/论文初稿v5.0.docx'),
        ('文献摘要JSON', '/Users/openclaw2026/.qclaw/workspace/literature_abstracts/abstracts.json'),
        ('文献摘要Markdown', '/Users/openclaw2026/.qclaw/workspace/literature_abstracts/abstracts.md'),
    ]
    
    for name, path in output_files:
        if Path(path).exists():
            size = Path(path).stat().st_size
            report.append(f"✅ {name}: 存在 ({size} bytes)")
        else:
            report.append(f"❌ {name}: 缺失")
    report.append("")
    
    # 6. 总结
    report.append("【6. 检查总结】")
    report.append("-" * 40)
    
    checks_passed = 0
    checks_total = 5
    
    if word_count_estimate >= 30000:
        checks_passed += 1
        report.append("✅ 字数要求")
    else:
        report.append("❌ 字数要求")
    
    if len(orig_chapters) == len(enh_chapters):
        checks_passed += 1
        report.append("✅ 章节结构")
    else:
        report.append("⚠️ 章节结构")
    
    if enh_citations['total'] > 0:
        checks_passed += 1
        report.append("✅ 引用标记")
    else:
        report.append("❌ 引用标记")
    
    if ref_check['has_section']:
        checks_passed += 1
        report.append("✅ 参考文献")
    else:
        report.append("❌ 参考文献")
    
    if Path('/Users/openclaw2026/.qclaw/workspace/output/论文初稿v5.0.docx').exists():
        checks_passed += 1
        report.append("✅ 输出文件")
    else:
        report.append("❌ 输出文件")
    
    report.append("")
    report.append(f"检查通过率: {checks_passed}/{checks_total}")
    report.append("")
    report.append("=" * 60)
    
    return '\n'.join(report)

def main():
    original_md = '/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0.md'
    enhanced_md = '/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0_citations_enhanced.md'
    output_dir = '/Users/openclaw2026/.qclaw/workspace/output'
    
    print("正在进行最终检查验证...")
    print()
    
    report = generate_report(original_md, enhanced_md, output_dir)
    
    # 保存报告
    report_path = '/Users/openclaw2026/.qclaw/workspace/output/检查报告.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print()
    print(f"检查报告已保存: {report_path}")

if __name__ == "__main__":
    main()
