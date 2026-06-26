#!/usr/bin/env python3
"""
文献摘要生成器
基于论文内容生成参考文献摘要
"""

import json
import re

def load_references():
    with open('/Users/openclaw2026/.qclaw/workspace/references.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_paper_content():
    with open('/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0.md', 'r', encoding='utf-8') as f:
        return f.read()

def find_citations_in_text(content, ref_id):
    """在论文正文中查找引用该文献的段落"""
    # 匹配 [ref_id] 或 (作者, 年份) 格式的引用
    patterns = [
        rf'\[{ref_id}\]',
        rf'\({ref_id}\)'
    ]
    
    citations = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern, line):
                # 获取上下文（前后各2行）
                start = max(0, i-2)
                end = min(len(lines), i+3)
                context = '\n'.join(lines[start:end])
                citations.append({
                    'line': i+1,
                    'context': context.strip()
                })
                break
    
    return citations

def generate_abstracts():
    refs = load_references()
    content = load_paper_content()
    
    abstracts = []
    
    # 为每篇文献生成摘要信息
    for ref in refs:
        ref_id = ref['id']
        citations = find_citations_in_text(content, ref_id)
        
        # 提取引用上下文中的关键描述
        contexts = []
        for cite in citations[:3]:  # 最多取3处引用
            # 清理上下文，提取关键句
            ctx = cite['context']
            # 移除引用标记
            ctx = re.sub(rf'\[{ref_id}\]', '', ctx)
            ctx = re.sub(rf'\({ref_id}\)', '', ctx)
            contexts.append(ctx.strip())
        
        abstract_info = {
            'id': ref_id,
            'raw': ref['raw'],
            'type': ref['type'],
            'citation_count': len(citations),
            'contexts': contexts,
            'keywords': extract_keywords(ref['raw'], contexts)
        }
        
        abstracts.append(abstract_info)
    
    return abstracts

def extract_keywords(raw_ref, contexts):
    """从引用和上下文中提取关键词"""
    keywords = []
    
    # 从文献标题/期刊名提取关键词
    if '银行' in raw_ref:
        keywords.append('银行')
    if '核心系统' in raw_ref or 'Core' in raw_ref:
        keywords.append('核心系统')
    if 'DevOps' in raw_ref or 'devops' in raw_ref.lower():
        keywords.append('DevOps')
    if '敏捷' in raw_ref or 'Agile' in raw_ref:
        keywords.append('敏捷开发')
    if '合规' in raw_ref or 'Compliance' in raw_ref:
        keywords.append('合规')
    if '反洗钱' in raw_ref or 'AML' in raw_ref:
        keywords.append('反洗钱')
    if '数据治理' in raw_ref or 'Data Governance' in raw_ref:
        keywords.append('数据治理')
    if '软件过程' in raw_ref or 'Software Process' in raw_ref:
        keywords.append('软件过程改进')
    if '持续集成' in raw_ref or 'CI' in raw_ref:
        keywords.append('持续集成')
    if '持续交付' in raw_ref or 'CD' in raw_ref:
        keywords.append('持续交付')
    
    # 从上下文中提取更多关键词
    all_context = ' '.join(contexts)
    if '国际化' in all_context:
        keywords.append('国际化')
    if '海外' in all_context:
        keywords.append('海外系统')
    if '监管' in all_context:
        keywords.append('监管科技')
    
    return list(set(keywords))

def save_abstracts(abstracts):
    # 保存为JSON
    with open('/Users/openclaw2026/.qclaw/workspace/literature_abstracts/abstracts.json', 'w', encoding='utf-8') as f:
        json.dump(abstracts, f, ensure_ascii=False, indent=2)
    
    # 保存为Markdown格式便于阅读
    with open('/Users/openclaw2026/.qclaw/workspace/literature_abstracts/abstracts.md', 'w', encoding='utf-8') as f:
        f.write("# 参考文献摘要汇总\n\n")
        f.write(f"共 {len(abstracts)} 篇文献\n\n")
        
        for abs_info in abstracts:
            f.write(f"## [{abs_info['id']}]\n\n")
            f.write(f"**原文**: {abs_info['raw']}\n\n")
            f.write(f"**类型**: {abs_info['type']}\n\n")
            f.write(f"**被引用次数**: {abs_info['citation_count']}\n\n")
            f.write(f"**关键词**: {', '.join(abs_info['keywords']) if abs_info['keywords'] else '待提取'}\n\n")
            
            if abs_info['contexts']:
                f.write("**引用上下文**:\n\n")
                for i, ctx in enumerate(abs_info['contexts'], 1):
                    f.write(f"{i}. {ctx[:300]}...\n\n")
            
            f.write("---\n\n")

if __name__ == "__main__":
    print("正在生成文献摘要...")
    abstracts = generate_abstracts()
    save_abstracts(abstracts)
    print(f"已生成 {len(abstracts)} 篇文献的摘要信息")
    print("保存位置: literature_abstracts/abstracts.json 和 abstracts.md")
