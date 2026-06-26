#!/usr/bin/env python3
"""补全价值链分析结尾"""

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
    prompt = """请继续完成这一段：

...
**关键举措：**
1. 组建或引入AI研发团队，建立自主可控的技术能力
2. 与头部医院建立深度科研合作，获取高质量脱敏数据
3. 探索"保险+医疗+健康管理

请完整写完这一段，然后继续完成：

### 7.3 长期（3年以上）：怎么构建生态？

请完整写完所有内容直到结尾。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    
    print("\n[补全结尾...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=None)
    
    if report:
        print(f"\n✅ 结尾生成，长度: {len(report)} 字符")
        
        # 读取现有文件
        with open(output_dir + '03_value_chain_analysis.md', 'r') as f:
            existing = f.read()
        
        # 合并
        full = existing + '\n' + report
        
        with open(output_dir + '03_value_chain_analysis.md', 'w') as f:
            f.write(full)
        
        print(f"\n✅ 完整价值链分析已完成")
        total_lines = full.count('\n')
        print(f"   总行数: {total_lines}")
        
        return full

if __name__ == '__main__':
    main()
