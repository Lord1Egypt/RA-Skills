#!/usr/bin/env python3
"""
论文摘要智能分析器
自动提取：问题、方法、结论、工程实践建议
"""

import re
from typing import Dict, List, Optional

# 问题提取模式
PROBLEM_PATTERNS = [
    r'(?:however|but|yet|unfortunately),?\s+(.{20,200}?(?:limited|challenging|difficult|expensive|inefficient|lack|cannot|fail|struggle|suffer))',
    r'(?:we\s+address|this\s+paper\s+addresses|we\s+tackle|solving)\s+(.{15,120})',
    r'(?:existing|current|traditional|prior)\s+(?:methods|approaches|works?)\s+(.{20,150}?(?:cannot|fail|limited|struggle|suffer|ignore))',
]

# 方法提取模式
METHOD_PATTERNS = [
    r'(?:we\s+(?:propose|present|introduce|develop|design|build)\s+(.{15,200}))',
    r'(?:our\s+(?:method|approach|framework|system|model)\s+(?:is|uses|employs|leverages|combines)\s+(.{15,150}))',
]

# 结论提取模式
CONCLUSION_PATTERNS = [
    r'(?:experiments|results|evaluations?)\s+(?:show|demonstrate|indicate|reveal|confirm)\s+(.{20,200})',
    r'(?:we\s+achieve|achieving|our\s+method\s+achieves)\s+(.{15,150})',
    r'(?:outperform|surpass|beat|exceed)\s+(.{15,100}?(?:baseline|state-of-the-art|SOTA))',
]

def extract_sentences(text: str) -> List[str]:
    """将文本分割成句子"""
    text = re.sub(r'\b(e\.g|i\.e|etc|vs|Dr|Prof)\.\s*', r'\1<dot> ', text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.replace('<dot>', '.') for s in sentences]
    return sentences

def extract_method_name(title: str, summary: str) -> str:
    """提取方法名称"""
    # 从标题提取（通常是第一个词或缩写）
    title_match = re.search(r'^([A-Z][A-Za-z0-9\-]{2,})', title)
    if title_match:
        name = title_match.group(1)
        if name.lower() not in ['the', 'a', 'an', 'new', 'towards', 'on', 'learning', 'deep']:
            return name
    
    # 从摘要提取
    method_match = re.search(r'(?:called|named|termed|introducing|presents?)\s+([A-Z][A-Za-z0-9\-]{2,})', summary)
    if method_match:
        return method_match.group(1)
    
    # 尝试找大写缩写
    acronym_match = re.search(r'\b([A-Z]{2,}[A-Za-z]*)\b', title)
    if acronym_match:
        return acronym_match.group(1)
    
    return "该方法"

def extract_practice_suggestions(summary: str) -> List[str]:
    """从摘要中提取工程实践建议"""
    suggestions = []
    seen = set()
    summary_lower = summary.lower()
    
    # 1. 先尝试提取明确的实践建议
    direct_patterns = [
        r'(?:we\s+recommend|we\s+suggest|practitioners\s+should|engineers\s+should|users\s+can)\s+(.{20,150})',
        r'(?:suitable\s+for|applicable\s+to|can\s+be\s+applied\s+to)\s+(.{20,100})',
    ]
    
    for pattern in direct_patterns:
        matches = re.findall(pattern, summary, re.IGNORECASE | re.DOTALL)
        for match in matches:
            text = match.strip() if isinstance(match, str) else match[0].strip()
            text = re.sub(r'\s+', ' ', text)
            # 排除方法描述
            if 'we propose' not in text.lower() and 'we present' not in text.lower():
                text = text[:120] + '...' if len(text) > 120 else text
                key = text[:40].lower()
                if key not in seen and len(text) > 15:
                    seen.add(key)
                    suggestions.append(text)
    
    # 2. 基于关键词推断工程价值（更实用的建议）
    inference_rules = [
        # 性能与效率
        (r'\breal-time\b', '支持实时处理，适合对延迟敏感的应用场景'),
        (r'\befficient\b|\befficiency\b', '计算效率高，资源消耗可控'),
        (r'\bscalable\b|\bscale\b', '可扩展到大规模数据和用户场景'),
        (r'\blow-latency\b|\blow\s+latency\b', '低延迟设计，适合实时交互系统'),
        
        # 应用场景
        (r'\bproduction\b|\bdeploy\b', '可在生产环境部署使用'),
        (r'\bbenchmark\b', '在标准基准测试中验证，结果可复现'),
        (r'\bopen-source\b|\bgithub\b', '代码开源，便于复现和二次开发'),
        
        # 方法特点
        (r'\bmodular\b|\bflexible\b', '模块化设计，易于定制和扩展'),
        (r'\brobust\b', '鲁棒性强，适合复杂多变的环境'),
        (r'\blightweight\b|\bsimple\b', '轻量级实现，部署成本低'),
        
        # 数据相关
        (r'\bfew-shot\b|\bzero-shot\b', '支持少样本/零样本场景，数据需求低'),
        (r'\bmulti-modal\b|\bcross-modal\b', '支持多模态输入，应用场景广泛'),
        
        # 效果相关
        (r'\bstate-of-the-art\b|\bsota\b', '达到当前最优效果，可作为强基线'),
        (r'\bsignificant\s+improv', '效果显著提升，值得尝试'),
    ]
    
    for pattern, suggestion in inference_rules:
        if re.search(pattern, summary_lower):
            key = suggestion[:30]
            if key not in seen:
                seen.add(key)
                suggestions.append(suggestion)
    
    # 3. 如果还是没有，给出通用但有用的建议
    if not suggestions:
        suggestions = [
            '建议阅读论文实验部分，了解具体应用场景和效果',
            '关注论文中讨论的局限性和适用条件',
            '对比论文方法与现有方案的差异，选择适合的场景'
        ]
    
    return suggestions[:4]

def analyze_paper(paper: dict) -> dict:
    """分析论文摘要，提取关键信息"""
    title = paper.get('title', '')
    summary = paper.get('summary', '')
    
    result = {
        'method_name': extract_method_name(title, summary),
        'problem': None,
        'method': None,
        'conclusion': None,
        'practice_suggestions': [],
        'highlights': [],
    }
    
    # 提取问题
    for pattern in PROBLEM_PATTERNS:
        match = re.search(pattern, summary, re.IGNORECASE | re.DOTALL)
        if match:
            result['problem'] = match.group(1).strip()
            break
    
    # 提取方法
    for pattern in METHOD_PATTERNS:
        match = re.search(pattern, summary, re.IGNORECASE | re.DOTALL)
        if match:
            result['method'] = match.group(1).strip()
            break
    
    # 提取结论
    for pattern in CONCLUSION_PATTERNS:
        match = re.search(pattern, summary, re.IGNORECASE | re.DOTALL)
        if match:
            result['conclusion'] = match.group(1).strip()
            break
    
    # 提取工程实践建议
    result['practice_suggestions'] = extract_practice_suggestions(summary)
    
    # 提取亮点关键词
    highlight_keywords = [
        'novel', 'new', 'first', 'state-of-the-art', 'SOTA', 'best',
        'significant', 'substantial', 'efficient', 'real-time',
        'production', 'scalable', 'robust', 'open-source'
    ]
    for kw in highlight_keywords:
        if kw.lower() in summary.lower():
            result['highlights'].append(kw)
    
    return result

def generate_summary_text(paper: dict, analysis: dict) -> str:
    """生成1分钟速览文本"""
    method_name = analysis.get('method_name') or '该方法'
    problem = analysis.get('problem') or '某个问题'
    method = analysis.get('method') or '某种方法'
    conclusion = analysis.get('conclusion') or '取得了良好效果'
    
    # 截断过长的文本
    problem = problem[:80] + '...' if len(problem) > 80 else problem
    method = method[:80] + '...' if len(method) > 80 else method
    conclusion = conclusion[:80] + '...' if len(conclusion) > 80 else conclusion
    
    summary = f"""**{method_name}** 解决了 {problem}。核心方法是 {method}。实验表明 {conclusion}。"""
    
    return summary

def format_analysis_report(paper: dict, analysis: dict) -> dict:
    """格式化分析结果为报告可用的结构"""
    return {
        'one_line_summary': generate_summary_text(paper, analysis),
        'problem_solved': analysis.get('problem') or '待进一步阅读论文确定',
        'conclusion': analysis.get('conclusion') or '待进一步阅读论文确定',
        'method_used': analysis.get('method') or '待进一步阅读论文确定',
        'highlights': analysis.get('highlights') or [],
        'practice_suggestions': analysis.get('practice_suggestions') or [
            '建议阅读论文实验部分，了解具体应用场景',
            '关注论文中讨论的局限性和适用条件',
            '对比论文方法与现有方案的差异'
        ],
    }

def main():
    import json
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            paper = json.load(f)
    else:
        paper = {
            'title': 'Video Streaming Thinking: VideoLLMs Can Watch and Think Simultaneously',
            'summary': '''Understanding and reconstructing the 3D world through omnidirectional perception is an inevitable trend. However, existing 3D occupancy prediction methods are constrained by limited perspective inputs and predefined training distribution, making them difficult to apply to embodied agents. We present VST, a novel framework that enables real-time video understanding with efficient processing. Our experiments show that VST achieves state-of-the-art performance on multiple benchmarks, outperforming existing methods by 15%. We recommend applying this framework in real-time robotics applications where computational efficiency is critical.'''
        }
    
    analysis = analyze_paper(paper)
    report = format_analysis_report(paper, analysis)
    
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
