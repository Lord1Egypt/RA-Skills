#!/usr/bin/env python3
"""
增强版引用标记插入器
基于论文中已有的引用模式，全面添加引用标记
"""

import re
import json

def load_paper_content():
    with open('/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0.md', 'r', encoding='utf-8') as f:
        return f.read()

def comprehensive_citation_insertion(content):
    """
    全面插入引用标记
    基于论文中已有的引用模式进行补充
    """
    
    # 定义详细的引用插入规则
    # 格式: (原文片段, 引用编号)
    citation_rules = [
        # 第2章 基础理论与文献综述
        # 2.1 银行核心系统理论
        ('从系统功能的角度界定，核心系统是指处理存款、贷款、支付结算', 3),
        ('狭义的核心系统仅指账务处理引擎', 2),
        ('广义的核心系统则涵盖客户信息管理、产品管理', 51),
        ('核心系统的主要功能模块包括以下七个方面', 3),
        ('银行核心系统的技术演进与信息技术发展密切相关，大致经历了六个主要阶段', 4),
        ('第一阶段，手工记账时代', 4),
        ('第二阶段，单机处理时代', 4),
        ('第三阶段，联机交易时代', 4),
        ('第四阶段，数据大集中时代', 4),
        ('第五阶段，"瘦核心"时代', 4),
        ('第六阶段，分布式时代', 4),
        ('银行国际化是指银行按照国际规则', 6),
        ('中资银行海外分行系统建设呈现以下四个趋势', 8),
        
        # 2.2 软件过程改进理论
        ('软件生命周期（Software Life Cycle）是指软件产品从概念提出到最终退役的完整过程', 59),
        ('软件生命周期概念的建立被认为是软件工程的一次重要突破', 34),
        ('典型的软件生命周期包括以下八个阶段', 60),
        ('软件过程模型是跨越整个软件生命周期的系统开发、运行、维护所实施的全部工作和任务的结构框架', 61),
        ('在计算机发展的历史中，软件开发经历了无模型阶段、瀑布模型阶段', 62),
        ('瀑布模型将软件开发过程划分为需求分析、设计、编码、测试、维护等阶段', 61),
        ('迭代模型将软件开发过程划分为多个迭代周期', 34),
        ('敏捷开发方法自2001年《敏捷宣言》发布以来', 21),
        ('敏捷宣言强调个体和互动高于流程和工具', 21),
        ('软件过程改进（Software Process Improvement，SPI）是指通过系统的方法论和实践', 63),
        ('软件过程改进的核心思想是软件产品的质量很大程度上取决于开发和维护软件的过程质量', 64),
        ('DevOps是敏捷开发的延伸', 36),
        ('DevOps的核心理念包括文化（Culture）、自动化（Automation）、测量（Measurement）和共享（Sharing）', 36),
        
        # 2.3 DevOps理论与实践
        ('DevOps来源于Development和Operation的合成', 9),
        ('DevOps基于2009年欧洲传统IT模式的反思', 9),
        ('Jennifer Davis在《Effective DevOps》', 65),
        ('DevOps的核心思想包括以下四个维度', 36),
        ('DevOps与敏捷开发存在密切关联', 36),
        ('Lwakatare等的研究表明，DevOps是敏捷开发的进一步发展', 42),
        ('持续集成（Continuous Integration，CI）', 35),
        ('持续交付（Continuous Delivery，CD）', 35),
        ('Jenkins是当前最流行的持续集成工具', 14),
        ('基础设施即代码（Infrastructure as Code，IaC）', 35),
        ('蓝绿部署与金丝雀发布', 35),
        
        # DevOps研究现状
        ('Lucy Ellen Lwakatare等从起源、应用、实现和目标四个方面比较了DevOps与敏捷', 42),
        ('Soon K. Bang等通过将定性分析方法应用于多个Web应用程序开发项目', 43),
        ('Constantine Aaron Cois等认为DevOps的成功实施可以弥合项目团队之间的信息鸿沟', 44),
        ('Floris Erich等认为DevOps是一个概念', 53),
        ('Olsson和Bosch通过对多家软件企业的案例研究', 67),
        ('刘博涵等对DevOps在我国的应用现状进行了调查研究', 12),
        ('耿泉峰等概述了DevOps的软件开发流程', 13),
        ('陈咏秋等提出了一套完整的DevOps知识分类与管理方法', 15),
        ('王海燕研究了基于DevOps的持续交付实践', 47),
        
        # 2.4 海外金融合规理论
        ('反洗钱（Anti-Money Laundering，AML）是指为了预防通过各种方式掩饰', 55),
        ('金融机构反洗钱合规的核心要求包括以下五个方面', 54),
        ('在海外经营中，银行还需满足东道国的反洗钱监管要求', 55),
        ('数据治理（Data Governance）是对数据资产管理行使权力和控制的活动集合', 57),
        ('银行数据治理的核心内容包括以下四个方面', 33),
        ('欧盟的《通用数据保护条例》（GDPR）是最具代表性的数据保护法规', 56),
        
        # 2.5 规范驱动编程理论
        ('规范驱动编程（Specification-Driven Programming）是一种将系统规范用形式化或半形式化语言表达的软件开发方法', 29),
        ('规范驱动编程的主要特点包括以下四个方面', 30),
        ('在金融领域，规范驱动编程可用于将复杂的反洗钱规则', 31),
        ('规范驱动编程与敏捷开发可以相互补充', 32),
        
        # 第3章 H银行海外核心系统研发现状分析
        # 研究方法
        ('案例研究是对实际情境中的现象进行深入研究的方法', 38),
        ('扎根理论是一种质性研究方法', 39),
        ('主题分析是一种识别、分析和报告数据中模式的方法', 40),
        
        # 第4章 改进方案设计
        ('Scrum是最流行的敏捷框架之一', 21),
        ('用户故事（User Story）是敏捷开发中描述需求的标准方式', 21),
        
        # 第5章 改进成效评价
        ('层次分析法（AHP）是一种定性与定量相结合的多准则决策方法', 26),
        ('模糊综合评价法是一种基于模糊数学的综合评价方法', 25),
    ]
    
    modified_content = content
    insertions_made = []
    
    for text_pattern, ref_id in citation_rules:
        if text_pattern in modified_content:
            # 检查该位置是否已有引用
            # 找到文本位置
            idx = modified_content.find(text_pattern)
            if idx == -1:
                continue
                
            # 检查该句子是否已有引用标记
            # 获取该句子（到句号为止）
            sentence_end = modified_content.find('。', idx)
            if sentence_end == -1:
                sentence_end = len(modified_content)
            
            sentence = modified_content[idx:sentence_end+1]
            
            # 如果句子中已有引用标记，跳过
            if re.search(r'\[\d+\]', sentence):
                continue
            
            # 在句子末尾插入引用
            new_sentence = sentence[:-1] + f'[{ref_id}]' + sentence[-1:]
            modified_content = modified_content[:idx] + modified_content[idx:sentence_end+1].replace(sentence, new_sentence) + modified_content[sentence_end+1:]
            
            insertions_made.append({
                'pattern': text_pattern[:40],
                'ref_id': ref_id,
                'sentence': sentence[:60]
            })
    
    return insertions_made, modified_content

def main():
    content = load_paper_content()
    
    print(f"原始论文字数: {len(content)}")
    print("开始全面插入引用标记...")
    
    insertions, modified_content = comprehensive_citation_insertion(content)
    
    print(f"\n成功插入了 {len(insertions)} 处引用标记")
    print("\n插入详情（前20个）:")
    for i, ins in enumerate(insertions[:20], 1):
        print(f"{i}. [{ins['ref_id']}] {ins['pattern']}...")
    
    if len(insertions) > 20:
        print(f"... 还有 {len(insertions) - 20} 处引用")
    
    # 保存修改后的内容
    output_path = '/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0_citations_enhanced.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"\n增强版论文已保存: {output_path}")
    print(f"修改后字数: {len(modified_content)}")
    
    # 统计引用情况
    citation_count = len(re.findall(r'\[\d+\]', modified_content))
    unique_refs = set(re.findall(r'\[(\d+)\]', modified_content))
    print(f"论文中引用标记总数: {citation_count}")
    print(f"引用的不同文献数: {len(unique_refs)}")

if __name__ == "__main__":
    main()
