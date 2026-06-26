#!/usr/bin/env python3
"""生成AI增量价值矩阵（简化版）"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    import json
    with open('v9_papers_filtered.json', 'r') as f:
        papers = json.load(f)
    
    print(f"加载了 {len(papers)} 篇筛选后的论文")
    
    # 简化prompt
    prompt = """# AI增量价值矩阵

请回答：**AI大模型相对传统方法（人类医生、规则系统、早期机器学习）的增量价值是什么？**

用markdown表格回答，包含以下列：
- AI核心能力
- 传统方法局限
- AI如何突破
- 增量价值
- 控费传导路径

请列出6个核心能力，每个能力都要完整填写所有列。

然后回答：
# AI超越人类的疾病领域

哪些疾病的诊断AI准确率超过人类？请用表格回答，包含疾病领域、AI准确率、人类准确率、AI优势原因、数据来源。

用中文回答。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v10.0-20260324-optimized/'
    
    print("\n[生成AI增量价值矩阵...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '02_ai_incremental_matrix.md')
    
    if report:
        print(f"\n✅ 生成完成，长度: {len(report)} 字符")
    
    return report

if __name__ == '__main__':
    main()
