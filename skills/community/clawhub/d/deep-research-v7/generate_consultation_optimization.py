#!/usr/bin/env python3
"""补充生成：AI问诊过程优化专门章节"""

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
    
    # 专门聚焦问诊过程优化
    prompt = """# AI问诊过程优化深度分析

## 核心问题
AI大模型在**问诊过程本身**带来了什么增量价值？请具体分析：

## 1. AI问诊 vs 人类医生问诊对比

请用markdown表格对比：

| 维度 | 人类医生问诊 | AI大模型问诊 | AI增量价值 |
|------|-------------|-------------|-----------|
| 症状采集完整性 | | | |
| 症状采集正确率 | | | |
| 问诊时间 | | | |
| 问诊可及性 | | | |
| 问诊一致性 | | | |
| 多轮对话能力 | | | |
| 隐含症状识别 | | | |

请完整填满表格。

## 2. AI问诊流程优化

请说明AI如何优化问诊流程：

1. **症状采集优化**：AI如何通过多轮对话系统化采集症状？相比人类医生有什么优势？
2. **症状理解优化**：AI如何理解患者自然语言描述？如何处理模糊表述？
3. **漏诊预防**：AI如何通过知识图谱和系统化问诊降低漏诊率？
4. **问诊效率**：AI问诊平均时间？人类医生问诊平均时间？效率提升多少？

## 3. 症状采集正确率提升

请用表格说明：

| 症状类型 | AI正确率 | 人类正确率 | 提升幅度 | 原因 |
|---------|---------|-----------|---------|------|
| 常见症状（发热、咳嗽等） | | | | |
| 隐含症状（需要追问） | | | | |
| 复杂症状（多系统） | | | | |
| 儿科症状（表达困难） | | | | |

如有文献数据请引用。

## 4. 问诊效率对比

请用具体数据说明：
- AI问诊平均时间：xx分钟
- 人类医生问诊平均时间：xx分钟
- 效率提升：xx%

## 5. 典型案例

请举1-2个具体案例，说明AI问诊如何优于传统问诊。

用中文回答，完整填写所有表格，给出具体数据。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v10.0-20260324-optimized/'
    
    print("\n[生成AI问诊过程优化专门章节...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '03_consultation_optimization.md')
    
    if report:
        print(f"\n✅ 问诊优化章节生成完成，长度: {len(report)} 字符")
    
    return report

if __name__ == '__main__':
    main()
