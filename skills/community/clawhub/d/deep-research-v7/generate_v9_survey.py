#!/usr/bin/env python3
"""
Generate v9.0 Survey report using Research Claw
主题: AI大模型问诊诊疗价值（相对于机器学习、规则模型、人工问诊）深度研究
目标: 推导其对医保控费的价值
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    # 完整深度研究流程
    topic = """AI大模型问诊诊疗价值深度研究：对比人类医生问诊、传统规则系统、早期机器学习模型，分析AI大模型的技术能力提升以及对医保控费的价值传导机制。

研究问题：
1. AI大模型问诊 vs 人类医生，诊断准确率对比？
2. AI问诊能减少多少不必要的检查/检验？
3. AI能否提升早期疾病发现率（重症预警）？
4. AI问诊 vs 在线人工问诊，成本节约多少？
5. 技术代际对比：人类 → 规则系统 → ML → LLM
"""
    
    result = tools.full_research_flow(
        topic, 
        sources=['arxiv', 'pubmed', 'openalex', 'semantic'],
        max_results=30
    )
    
    # 保存结果到正确目录
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    if result['report']:
        with open(output_dir + '03-SURVEY-FINAL.md', 'w', encoding='utf-8') as f:
            f.write(result['report'])
        print(f"\n✅ 报告已保存: {output_dir}03-SURVEY-FINAL.md")
    
    return result

if __name__ == '__main__':
    main()
