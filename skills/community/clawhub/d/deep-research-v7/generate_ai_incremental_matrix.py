#!/usr/bin/env python3
"""生成AI增量价值矩阵和AI超越人类的疾病领域"""

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
    
    # 核心prompt - AI增量价值矩阵
    prompt = """请回答两个核心问题，用完整表格：

## 1. AI增量价值矩阵

请用完整表格回答：**AI相对传统方法（人类医生、规则系统、早期机器学习）的增量价值到底在哪里？**

| AI核心能力 | 传统方法局限 | AI如何突破 | 增量价值 | 控费传导路径 |
|-----------|-------------|-----------|---------|-------------|
| 自然语言理解 | 规则系统只能处理结构化输入，早期ML需特征工程 | 大模型可理解患者自然语言描述，无需人工特征 | | |
| 知识覆盖广度 | 人类医生受限于个人经验，规则系统受限于规则库 | 预训练覆盖全医学文献，知识图谱支撑 | | |
| 24x7可用性 | 人类医生需要休息，只能工作时间问诊 | AI随时可问，无时间限制 | | |
| 持续学习更新 | 知识更新周期长（月-年），规则系统需手动更新 | 实时更新知识库，增量学习 | | |
| 多模态融合 | 传统方法需分别处理文本、影像、检验 | 文本+影像+检验统一推理 | | |
| 大规模并发 | 受医生数量限制，无法规模化 | 可同时服务万人，无限扩展 | | |

请完整填满表格，每格都要有具体内容，说明AI带来的增量价值和如何传导为控费。

## 2. AI超越人类的疾病领域

请用完整表格回答：**AI在哪些疾病诊断上准确率超过人类医生？**

| 疾病领域 | AI准确率 | 人类医生准确率 | AI优势原因 | 数据来源（基于检索文献） |
|---------|---------|---------------|-----------|------------------------|
| 皮肤癌识别 | | | | |
| 糖尿病视网膜病变 | | | | |
| 肺结节检测 | | | | |
| 骨折诊断 | | | | |
| 乳腺癌筛查 | | | | |

请基于文献填写具体数据。如果没有相关数据，请标注"暂无文献数据"并说明原因。

## 3. AI超越人类的共性原因

请总结：为什么AI在这些领域能超越人类医生？（如：图像识别能力强、不受疲劳影响、可学习海量病例、无主观偏差等）

用中文回答，完整填写所有表格。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v10.0-20260324-optimized/'
    
    print("\n[生成AI增量价值矩阵和AI超越人类疾病领域...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '02_ai_incremental_matrix.md')
    
    if report:
        print(f"\n✅ 核心内容生成完成，长度: {len(report)} 字符")
    
    return report

if __name__ == '__main__':
    main()
