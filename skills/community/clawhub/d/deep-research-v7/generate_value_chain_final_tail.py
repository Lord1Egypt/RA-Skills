#!/usr/bin/env python3
"""补全价值链分析最后结尾"""

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
    
    # 补全结尾
    prompt = """请继续完成这份报告，当前写到：

...
#### 场景五：理赔审核

**技术基础**：综合应用Paper

请从这里继续写完，完整包含剩余内容：

完成五个场景的说明后，继续：

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

请完整写完所有内容，不要截断。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    
    print("\n[生成结尾...]")
    
    report_tail = tools.generate_survey_report(papers, prompt, output_path=None)
    
    if report_tail:
        print(f"\n✅ 结尾生成，长度: {len(report_tail)} 字符")
        
        # 读取现有文件
        with open(output_dir + '03_value_chain_analysis.md', 'r') as f:
            existing = f.read()
        
        # 合并
        full = existing + '\n' + report_tail
        
        with open(output_dir + '03_value_chain_analysis.md', 'w') as f:
            f.write(full)
        
        print(f"\n✅ 完整价值链分析已完成")
        total_lines = full.count('\n')
        print(f"   总行数: {total_lines}")
        
        return full

if __name__ == '__main__':
    main()
