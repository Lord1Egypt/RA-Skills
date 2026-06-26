#!/usr/bin/env python3
"""重新生成价值链分析第二部分"""

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
    
    # 第二部分
    prompt = """继续完成这份价值链分析报告，从"3. 关键技术"开始，完整写完所有章节：

## 3. 关键技术  
请总结支撑AI问诊控费的关键技术，每个技术说明对控费的贡献：
- 指令微调（Instruction Tuning）
- 多代理协同框架（Multi‑Agent Collaboration）
- 多源信息融合（Information Fusion）
- 输出可信度评估（Credibility Evaluation）
- 不确定性推理（Uncertainty Reasoning）

## 4. 控费价值传导机制  
完整传导链：
```
AI能力提升 → 诊疗环节优化 → 具体成本节约 → 最终控费结果
```

然后分环节给出量化节约（基于文献）：
1. **初筛分诊**：能减少多少百分比的什么成本？
2. **检查/检验推荐**：能减少多少百分比的不必要检查？
3. **重症早期预警**：能降低多少百分比的长期治疗成本？
4. **慢病持续管理**：能减少多少百分比的并发症？
5. **理赔审核**：能减少多少百分比的欺诈和过度理赔？

## 5. 场景价值排序  
按控费价值从大到小排序这五个场景，并说明每个排序的理由。

## 6. 风险与局限性  
分析限制AI控费价值实现的因素：
- 误诊风险
- 责任界定
- 数据隐私
- 医生/患者接受度
- 其他

## 7. 对商业保险的具体建议  
给出落地建议：
- **短期（0-1年）**：优先做什么？
- **中期（1-3年）**：建设什么能力？
- **长期（3年以上）**：怎么构建生态？

请完整写出所有内容，不要截断。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成价值链分析第二部分...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '03_value_chain_part2.md')
    
    if report:
        print(f"\n✅ 第二部分已保存，长度: {len(report)} 字符")
        lines = report.count('\n')
        print(f"   行数: {lines}")
    
    # 合并第一部分和第二部分
    print("\n[合并完整报告...]")
    with open(output_dir + '03_value_chain_analysis.md', 'r') as f:
        part1 = f.read()
    
    full_report = part1 + '\n' + report
    
    with open(output_dir + '03_value_chain_analysis.md', 'w') as f:
        f.write(full_report)
    
    print(f"\n✅ 完整价值链分析已合并")
    total_lines = full_report.count('\n')
    print(f"   总行数: {total_lines}")
    
    return full_report

if __name__ == '__main__':
    main()
