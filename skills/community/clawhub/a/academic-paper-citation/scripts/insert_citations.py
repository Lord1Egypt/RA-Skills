#!/usr/bin/env python3
"""
引用标记插入器
在论文Markdown中插入引用标记
"""

import re
import json

def load_references():
    with open('/Users/openclaw2026/.qclaw/workspace/references.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_paper_content():
    with open('/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0.md', 'r', encoding='utf-8') as f:
        return f.read()

def identify_citation_opportunities(content, refs):
    """
    识别可以插入引用标记的位置
    基于文献标题和论文内容的相关性
    """
    opportunities = []
    
    # 定义引用映射规则（基于文献内容与论文主题的关联）
    citation_rules = [
        # 银行核心系统相关
        {'keywords': ['核心系统', 'Core Banking'], 'ref_ids': [2, 3, 4, 5], 'section': '银行核心系统理论'},
        
        # 银行国际化相关
        {'keywords': ['国际化', '海外', 'internationalization'], 'ref_ids': [6, 7, 8], 'section': '银行国际化'},
        
        # DevOps相关
        {'keywords': ['DevOps', '持续交付', 'CI/CD'], 'ref_ids': [9, 10, 11, 12, 13, 35, 36, 37], 'section': 'DevOps理论'},
        
        # 软件过程改进相关
        {'keywords': ['软件过程', 'CMMI', '敏捷', 'Agile'], 'ref_ids': [16, 17, 18, 19, 20, 21, 22, 23, 63, 64], 'section': '软件过程改进'},
        
        # 持续集成/持续交付
        {'keywords': ['持续集成', '持续交付', 'Jenkins'], 'ref_ids': [14, 35, 36, 66], 'section': 'CI/CD实践'},
        
        # 评价方法相关
        {'keywords': ['AHP', '层次分析法', '模糊综合评价'], 'ref_ids': [25, 26, 27], 'section': '评价方法'},
        
        # 合规科技相关
        {'keywords': ['合规', 'RegTech', '反洗钱', 'AML'], 'ref_ids': [28, 54, 55, 56], 'section': '合规科技'},
        
        # 规范驱动编程
        {'keywords': ['规范驱动', 'Specification-Driven'], 'ref_ids': [29, 30, 31], 'section': '规范驱动编程'},
        
        # 数据治理
        {'keywords': ['数据治理', 'Data Governance', 'GDPR'], 'ref_ids': [33, 48, 56, 57], 'section': '数据治理'},
        
        # 软件工程基础
        {'keywords': ['软件工程', '软件生命周期'], 'ref_ids': [34, 50, 59, 60, 61, 62], 'section': '软件工程基础'},
        
        # 研究方法
        {'keywords': ['案例研究', '访谈', '问卷调查'], 'ref_ids': [38, 39, 40, 41], 'section': '研究方法'},
        
        # 分布式架构
        {'keywords': ['分布式', '微服务', '云原生'], 'ref_ids': [45, 46], 'section': '分布式架构'},
    ]
    
    lines = content.split('\n')
    modified_lines = []
    
    for line_num, line in enumerate(lines):
        modified_line = line
        
        # 跳过标题行、空行和参考文献部分
        if line.startswith('#') or not line.strip() or '参考文献' in line:
            modified_lines.append(modified_line)
            continue
        
        # 检查是否匹配引用规则
        for rule in citation_rules:
            for keyword in rule['keywords']:
                if keyword in line and len(line) > 20:  # 只处理内容行
                    # 检查是否已经有引用标记
                    if not re.search(r'\[\d+\]', line):
                        # 在句子末尾插入引用标记
                        # 找到句子的结束位置
                        sentence_end = max(line.rfind('。'), line.rfind('.'), line.rfind('；'))
                        if sentence_end > 0:
                            # 选择一个合适的引用（这里简化处理，使用第一个）
                            ref_id = rule['ref_ids'][0]
                            # 在句子末尾前插入引用
                            modified_line = line[:sentence_end] + f'[{ref_id}]' + line[sentence_end:]
                            opportunities.append({
                                'line': line_num + 1,
                                'original': line,
                                'modified': modified_line,
                                'ref_id': ref_id,
                                'keyword': keyword
                            })
                            break
            if modified_line != line:
                break
        
        modified_lines.append(modified_line)
    
    return opportunities, '\n'.join(modified_lines)

def insert_citations_simple(content, refs):
    """
    简化版引用插入：在关键主题段落末尾添加引用
    """
    # 定义关键引用点（基于论文已有引用模式）
    key_insertions = [
        # 银行核心系统定义相关
        ('关于核心系统的功能边界，学术界和业界存在不同理解', 3),
        ('银行核心系统的技术演进与信息技术发展密切相关', 4),
        ('中资银行海外分行系统建设呈现以下四个趋势', 8),
        
        # 软件过程改进相关
        ('软件生命周期概念的建立被认为是软件工程的一次重要突破', 34),
        ('瀑布模型将软件开发过程划分为需求分析、设计、编码、测试、维护等阶段', 61),
        ('敏捷开发方法自2001年《敏捷宣言》发布以来', 21),
        
        # DevOps相关
        ('DevOps来源于Development和Operation的合成', 9),
        ('DevOps的核心思想包括以下四个维度', 36),
        ('持续集成的关键实践包括代码频繁提交', 14),
        
        # 合规相关
        ('金融机构反洗钱合规的核心要求包括以下五个方面', 54),
        ('数据治理是对数据资产管理行使权力和控制的活动集合', 57),
        ('欧盟的《通用数据保护条例》（GDPR）是最具代表性的数据保护法规', 56),
        
        # 规范驱动编程
        ('规范驱动编程是一种将系统规范用形式化或半形式化语言表达的软件开发方法', 29),
        
        # 研究方法
        ('案例研究是对实际情境中的现象进行深入研究的方法', 38),
    ]
    
    modified_content = content
    insertions_made = []
    
    for text_pattern, ref_id in key_insertions:
        if text_pattern in modified_content:
            # 在文本后插入引用标记
            pattern = re.escape(text_pattern)
            # 找到句子结束位置
            def insert_ref(match):
                matched_text = match.group(0)
                # 检查是否已经有引用
                if re.search(r'\[\d+\]', matched_text):
                    return matched_text
                # 在句子末尾插入引用
                return matched_text + f'[{ref_id}]'
            
            # 匹配包含该文本的句子
            modified_content, count = re.subn(
                f'({pattern}[^。]*。)',
                insert_ref,
                modified_content
            )
            if count > 0:
                insertions_made.append({
                    'pattern': text_pattern[:50],
                    'ref_id': ref_id,
                    'count': count
                })
    
    return insertions_made, modified_content

def main():
    refs = load_references()
    content = load_paper_content()
    
    print(f"原始论文字数: {len(content)}")
    
    # 使用简化方法插入引用
    insertions, modified_content = insert_citations_simple(content, refs)
    
    print(f"\n插入了 {len(insertions)} 处引用标记")
    for ins in insertions[:10]:  # 显示前10个
        print(f"  - [{ins['ref_id']}] {ins['pattern']}...")
    
    # 保存修改后的内容
    output_path = '/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0_with_citations.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"\n修改后的论文已保存: {output_path}")
    print(f"修改后字数: {len(modified_content)}")
    
    # 统计引用情况
    citation_count = len(re.findall(r'\[\d+\]', modified_content))
    print(f"论文中引用标记总数: {citation_count}")

if __name__ == "__main__":
    main()
