#!/usr/bin/env python3
"""完整生成价值链分析"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    # 加载筛选后的论文
    import json
    with open('v9_papers_filtered.json', 'r') as f:
        papers = json.load(f)
    
    print(f"加载了 {len(papers)} 篇筛选后的论文")
    
    # 完整prompt
    prompt = """# AI大模型问诊诊疗价值深度研究——医保控费价值链分析

## 1. 研究背景

### 1.1 AI大模型在医疗问诊领域的发展
以GPT、LLM为代表的大语言模型已在症状抽取、预问诊、分诊建议、诊疗决策等方面展示出接近或部分超越人类医生的能力。政策层面，《健康中国2030》《新一代人工智能发展规划》均把"AI+医疗"作为提升服务效率、降低医疗费用的重要抓手。

### 1.2 医保/商保面临的成本压力
门诊过度就医、重复检查、住院不必要的延长、慢病管理不足导致的急性发作等现象，使医保基金面临持续赤字风险。商业健康险在理赔审核、欺诈检测、精算定价等环节同样需要更高效的技术手段。

### 1.3 核心研究问题
AI大模型问诊能力提升，如何转化为医保/商保的**费用控制价值**？本报告通过梳理最新研究，剖析技术路径、量化潜力、风险与局限，并给出商业保险的落地建议。

## 2. 相关论文总结

请基于提供的44篇论文，整理一个表格：
| 编号 | 论文名称 | 研究主题 | 核心贡献（简述） |

请列出所有相关论文。

## 3. 支撑AI问诊控费的关键技术

请分技术说明，每个技术说明它对控费的具体贡献：
- 指令微调（Instruction Tuning）
- 多代理协同框架（Multi‑Agent Collaboration）
- 多源信息融合（Information Fusion）
- 输出可信度评估（Credibility Evaluation）
- 不确定性推理（Uncertainty Reasoning）

## 4. 控费价值传导机制

### 4.1 完整传导链
```
AI能力提升 → 诊疗环节优化 → 具体成本节约 → 最终控费结果
```

### 4.2 各环节量化节约总结
请完成表格：
| 环节 | 量化节约（基于文献研究） |
|------|----------------------|
| **初筛分诊** | |
| **检查/检验推荐** | |
| **重症早期预警** | |
| **慢病持续管理** | |
| **理赔审核** | |

## 5. 场景价值排序
按控费价值从大到小排序这五个场景，并给出每个场景的排序理由。

## 6. 风险与局限性
分析限制AI控费价值实现的因素：
- 误诊风险
- 责任界定
- 数据隐私
- 医生/患者接受度
- 其他

## 7. 对商业保险的具体建议
分阶段给出具体建议：
- **短期（0-1年）**：优先布局什么场景，为什么？
- **中期（1-3年）**：需要建设什么核心能力？
- **长期（3年以上）**：怎么构建完整的AI控费生态？

请完整写出所有章节，不要截断，结构清晰，用markdown格式。用中文回答。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成完整价值链分析...]")
    
    # 删除旧文件
    if os.path.exists(output_dir + '03_value_chain_analysis.md'):
        os.remove(output_dir + '03_value_chain_analysis.md')
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '03_value_chain_analysis.md')
    
    if report:
        print(f"\n✅ 完整价值链分析已保存，长度: {len(report)} 字符")
        lines = report.count('\n')
        print(f"   总行数: {lines}")
    
    return report

if __name__ == '__main__':
    main()
