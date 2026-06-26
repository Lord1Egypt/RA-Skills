#!/usr/bin/env python3
"""生成优化版报告 - 第一部分（AI增量价值矩阵+AI超越人类疾病领域）"""

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
    
    # 第一部分 - 核心增量价值
    prompt = """# AI大模型问诊诊疗价值 - 优化版报告 Part 1

## 1. AI增量价值矩阵（核心章节）

请用完整表格回答：**AI相对传统方法的增量价值到底在哪里？**

| AI核心能力 | 传统方法局限 | AI如何突破 | 增量价值 | 控费传导路径 |
|-----------|-------------|-----------|---------|-------------|
| 自然语言理解 | 规则系统只能处理结构化输入 | 大模型可理解患者自然语言描述 | | |
| 知识覆盖广度 | 人类医生受限于个人经验 | 预训练覆盖全医学文献 | | |
| 24x7可用性 | 人类医生需要休息 | AI随时可问 | | |
| 持续学习更新 | 知识更新周期长 | 实时更新知识库 | | |
| 多模态融合 | 传统方法需分别处理 | 文本+影像+检验统一推理 | | |
| 大规模并发 | 受医生数量限制 | 可同时服务万人 | | |

请完整填满表格，每格都要有内容。

## 2. AI超越人类的疾病领域

请回答：**AI在哪些疾病诊断上准确率超过人类医生？**

| 疾病领域 | AI准确率 | 人类医生准确率 | AI优势原因 | 数据来源 |
|---------|---------|---------------|-----------|----------|
| 皮肤癌识别 | | | | |
| 糖尿病视网膜病变 | | | | |
| 肺结节检测 | | | | |
| 骨折诊断 | | | | |
| 乳腺癌筛查 | | | | |

请基于文献填写具体数据（如有）。

## 3. AI超越人类的共性原因

总结为什么AI在这些领域能超越人类。

用中文回答，完整填写所有表格。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v10.0-20260324-optimized/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成第一部分：AI增量价值矩阵...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '01_ai_incremental_value.md')
    
    if report:
        print(f"\n✅ 第一部分完成，长度: {len(report)} 字符")
    
    return report

if __name__ == '__main__':
    main()
