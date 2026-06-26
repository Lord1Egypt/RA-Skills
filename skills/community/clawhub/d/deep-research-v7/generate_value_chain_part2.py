#!/usr/bin/env python3
"""完整生成价值链分析 - 第二部分"""

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
    prompt = """请继续完成这份报告，从这里开始：

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

请完整写完所有章节，不要截断，结构清晰，用markdown格式。用中文回答。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成价值链分析第二部分...]")
    
    report_part2 = tools.generate_survey_report(papers, prompt, output_path=output_dir + '03_value_chain_part2.md')
    
    if report_part2:
        print(f"\n✅ 第二部分完成，长度: {len(report_part2)} 字符")
        lines = report_part2.count('\n')
        print(f"   行数: {lines}")
    
    # 合并两部分
    print("\n[合并完整报告...]")
    with open(output_dir + '03_value_chain_part1.md', 'r') as f:
        part1 = f.read()
    
    full_report = part1 + '\n\n' + report_part2
    
    with open(output_dir + '03_value_chain_analysis.md', 'w') as f:
        f.write(full_report)
    
    print(f"\n✅ 完整价值链分析已生成")
    total_lines = full_report.count('\n')
    print(f"   总行数: {total_lines}")
    
    return full_report

if __name__ == '__main__':
    main()
