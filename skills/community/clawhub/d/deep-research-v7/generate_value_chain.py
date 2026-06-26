#!/usr/bin/env python3
"""生成价值链分析"""

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
    
    # 生成价值链分析
    prompt = """# AI大模型问诊诊疗价值深度研究 - 医保控费价值链分析

## 研究问题
AI大模型问诊能力提升，如何传导为医保/商保控费价值？

请基于提供的论文，分析：

### 1. 控费价值传导机制
绘制完整传导链：
```
AI大模型能力提升 → 哪些诊疗环节得到优化 → 哪些成本得到节约 → 最终医保支出减少
```
解释每一步传导逻辑。

### 2. 量化证据总结
从现有研究中总结：
- AI预问诊能减少多少百分比的不必要检查/检验？
- AI分诊能减少多少百分比的不必要门诊/住院？
- AI早期预警能降低多少百分比的长期治疗成本？
- AI问诊相对人工问诊能降低多少百分比的直接成本？

请给出具体数据范围，并说明数据来源（基于检索到的论文）。

### 3. 场景价值排序
按控费价值从大到小排序：
- 初筛分诊
- 检查/检验推荐
- 重症早期预警
- 慢病持续管理
- 理赔审核

说明为什么这个排序。

### 4. 风险与局限性
哪些因素会限制AI控费价值的实现？
- 误诊风险
- 责任界定
- 数据隐私
- 医生/患者接受度

### 5. 对商业保险的建议
保险行业应该怎么布局AI问诊控费？
- 短期（0-1年）先做什么？
- 中期（1-3年）布局什么？
- 长期（3年以上）布局什么？

请用中文回答，结构清晰，给出具体结论。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成价值链分析...]")
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '03_value_chain_analysis.md')
    
    if report:
        print(f"\n✅ 价值链分析已保存，长度: {len(report)} 字符")
    
    return report

if __name__ == '__main__':
    main()
