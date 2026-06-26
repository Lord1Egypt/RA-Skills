#!/usr/bin/env python3
"""
内容结构分析脚本

功能：分析文本内容的结构特征，包括段落密度、数据密度、标题层级、关键特征等，并生成优化建议

参数：
  --content: 待分析的文本内容（必需，可以是文件路径或直接文本）
  --file: 是否将 --content 参数视为文件路径（可选，默认为 False）
  --output: 输出格式，可选 json 或 text（默认 json）

输出：JSON 格式的分析报告和建议
"""

import argparse
import json
import re
import sys
from pathlib import Path


def analyze_content_structure(content: str) -> dict:
    """
    分析内容结构
    
    Args:
        content: 待分析的文本内容
    
    Returns:
        包含结构分析结果的字典
    """
    # 基础统计
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    words = content.split()
    sentences = re.split(r'[。！？.!?]', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # 段落分析
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
    
    # 标题分析（识别 Markdown 格式的标题）
    headings = []
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    for match in heading_pattern.finditer(content):
        level = len(match.group(1))
        text = match.group(2).strip()
        headings.append({
            'level': level,
            'text': text,
            'length': len(text)
        })
    
    # 数据密度分析
    # 数字出现次数
    numbers = re.findall(r'\d+(?:\.\d+)?%?', content)
    number_count = len(numbers)
    
    # 百分比出现次数
    percentages = re.findall(r'\d+(?:\.\d+)?%', content)
    percentage_count = len(percentages)
    
    # 年份/日期出现次数
    dates = re.findall(r'\b(?:19|20)\d{2}\b', content)
    date_count = len(dates)
    
    # 引用标识（引号、书名号等）
    quotes = re.findall(r'[""「」『』《》]', content)
    quote_count = len(quotes)
    
    # 关键词分析
    # 列表项（以 - 或 * 开头）
    list_items = re.findall(r'^[\-\*]\s+.+$', content, re.MULTILINE)
    list_count = len(list_items)
    
    # 对比表格特征（识别简单的表格结构）
    table_rows = re.findall(r'\|.+\|', content)
    table_count = len(table_rows)
    
    # 加粗文本（Markdown 格式）
    bold_texts = re.findall(r'\*\*([^*]+)\*\*', content)
    bold_count = len(bold_texts)
    
    # 外链特征（URL 出现次数）
    urls = re.findall(r'https?://[^\s\)]+', content)
    url_count = len(urls)
    
    # 权威性特征评分
    authority_score = 0
    authority_features = []
    
    # 数据支撑
    if number_count > 10:
        authority_score += 15
        authority_features.append('丰富的数据支撑')
    elif number_count > 5:
        authority_score += 8
        authority_features.append('适度的数据支撑')
    
    # 引用来源
    if url_count > 3:
        authority_score += 12
        authority_features.append('多处引用外部来源')
    elif url_count > 0:
        authority_score += 5
        authority_features.append('有引用外部来源')
    
    # 结构清晰度
    if len(headings) >= 3:
        authority_score += 10
        authority_features.append('清晰的标题层级')
    
    # 对比分析
    if table_count > 0:
        authority_score += 10
        authority_features.append('包含对比表格')
    
    # 关键结论标识
    if bold_count > 0:
        authority_score += 8
        authority_features.append('标注关键结论')
    
    # 内容完整度
    if len(words) > 1000:
        authority_score += 10
        authority_features.append('内容详实完整')
    elif len(words) > 500:
        authority_score += 5
        authority_features.append('内容较为完整')
    
    # 混淆结构检测
    confusing_issues = []
    
    # 检查长段落（超过 200 字的段落）
    long_paragraphs = [p for p in paragraphs if len(p) > 200]
    if long_paragraphs:
        confusing_issues.append({
            'issue': '段落过长',
            'description': f'发现 {len(long_paragraphs)} 个超过 200 字的段落，建议拆分以提高可读性',
            'severity': 'medium'
        })
    
    # 检查模糊标题
    vague_headings = []
    for h in headings:
        # 标题过于简短或模糊
        if h['length'] < 5 or re.match(r'^(介绍|概述|总结|结论)$', h['text']):
            vague_headings.append(h['text'])
    
    if vague_headings:
        confusing_issues.append({
            'issue': '标题模糊',
            'description': f'发现 {len(vague_headings)} 个过于模糊的标题：{", ".join(vague_headings[:3])}，建议改为具体、数据化的表述',
            'severity': 'high'
        })
    
    # 检查缺少结论
    conclusion_keywords = ['结论', '总结', '综上', '因此', '建议', 'conclusion', 'summary']
    has_conclusion = any(keyword in content.lower() for keyword in conclusion_keywords)
    
    if not has_conclusion and len(words) > 500:
        confusing_issues.append({
            'issue': '缺少明确结论',
            'description': '内容较长但未发现明确的结论句，建议在末尾添加总结性结论',
            'severity': 'high'
        })
    
    # 检查数据缺失
    if number_count < 3 and len(words) > 300:
        confusing_issues.append({
            'issue': '数据支撑不足',
            'description': '内容缺少具体数据支撑，建议添加统计数据、百分比或具体案例',
            'severity': 'medium'
        })
    
    # 构建分析结果
    result = {
        'basic_stats': {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': round(avg_paragraph_length, 1),
            'heading_count': len(headings)
        },
        'content_features': {
            'number_count': number_count,
            'percentage_count': percentage_count,
            'date_count': date_count,
            'quote_count': quote_count,
            'list_count': list_count,
            'table_count': table_count,
            'bold_count': bold_count,
            'url_count': url_count
        },
        'authority_analysis': {
            'score': authority_score,
            'max_score': 65,
            'level': '高' if authority_score >= 45 else '中' if authority_score >= 25 else '低',
            'features': authority_features
        },
        'confusing_structure': {
            'issue_count': len(confusing_issues),
            'issues': confusing_issues
        },
        'headings': headings
    }
    
    return result


def generate_optimization_suggestions(analysis: dict) -> list:
    """
    基于分析结果生成优化建议
    
    Args:
        analysis: 内容结构分析结果
    
    Returns:
        优化建议列表
    """
    suggestions = []
    
    # 权威性提升建议
    authority = analysis['authority_analysis']
    if authority['level'] == '低':
        suggestions.append({
            'priority': '高',
            'category': '权威性提升',
            'action': '增加数据支撑',
            'details': '添加统计数据、百分比、案例研究等具体数据，提升内容可信度'
        })
    
    if analysis['content_features']['url_count'] < 2:
        suggestions.append({
            'priority': '高',
            'category': '权威性提升',
            'action': '添加外部引用',
            'details': '引用权威来源（如研究报告、官方数据、行业白皮书），增加外链'
        })
    
    # 结构优化建议
    if analysis['basic_stats']['heading_count'] < 3:
        suggestions.append({
            'priority': '中',
            'category': '结构优化',
            'action': '增加标题层级',
            'details': '使用清晰的标题层级（H2、H3）组织内容，提升可读性和结构化程度'
        })
    
    if analysis['content_features']['table_count'] == 0 and analysis['basic_stats']['word_count'] > 500:
        suggestions.append({
            'priority': '中',
            'category': '结构优化',
            'action': '添加对比表格',
            'details': '对于产品对比、优劣势分析等内容，使用表格形式呈现更易被引用'
        })
    
    # 混淆结构修复建议
    for issue in analysis['confusing_structure']['issues']:
        suggestions.append({
            'priority': '高' if issue['severity'] == 'high' else '中',
            'category': '混淆结构修复',
            'action': f'修复：{issue["issue"]}',
            'details': issue['description']
        })
    
    # 关键结论突出建议
    if analysis['content_features']['bold_count'] < 3:
        suggestions.append({
            'priority': '低',
            'category': '关键结论突出',
            'action': '加粗关键结论',
            'details': '使用加粗格式突出关键结论和数据，提升内容辨识度'
        })
    
    return suggestions


def main():
    parser = argparse.ArgumentParser(description='分析内容结构并生成优化建议')
    parser.add_argument('--content', required=True, help='待分析的文本内容或文件路径')
    parser.add_argument('--file', action='store_true', help='将 --content 参数视为文件路径')
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 读取内容
    if args.file:
        try:
            content = Path(args.content).read_text(encoding='utf-8')
        except Exception as e:
            result = {
                'success': False,
                'error_message': f'文件读取失败: {str(e)}'
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
    else:
        content = args.content
    
    # 执行分析
    analysis = analyze_content_structure(content)
    
    # 生成优化建议
    suggestions = generate_optimization_suggestions(analysis)
    
    # 构建完整结果
    result = {
        'success': True,
        'analysis': analysis,
        'optimization_suggestions': suggestions
    }
    
    # 输出结果
    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== 内容结构分析报告 ===\n")
        print(f"基础统计：")
        print(f"  字数: {analysis['basic_stats']['word_count']}")
        print(f"  句子数: {analysis['basic_stats']['sentence_count']}")
        print(f"  段落数: {analysis['basic_stats']['paragraph_count']}")
        print(f"  标题数: {analysis['basic_stats']['heading_count']}")
        print(f"\n权威性评分: {analysis['authority_analysis']['score']}/{analysis['authority_analysis']['max_score']} ({analysis['authority_analysis']['level']})")
        print(f"权威性特征: {', '.join(analysis['authority_analysis']['features'])}")
        
        if analysis['confusing_structure']['issue_count'] > 0:
            print(f"\n混淆结构问题 ({analysis['confusing_structure']['issue_count']} 个):")
            for issue in analysis['confusing_structure']['issues']:
                print(f"  - {issue['issue']}: {issue['description']}")
        
        if suggestions:
            print(f"\n优化建议 ({len(suggestions)} 条):")
            for i, s in enumerate(suggestions, 1):
                print(f"  {i}. [{s['priority']}] {s['action']}: {s['details']}")


if __name__ == '__main__':
    main()
