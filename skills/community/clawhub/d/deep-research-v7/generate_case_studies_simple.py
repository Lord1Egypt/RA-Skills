#!/usr/bin/env python3
"""补充案例分析 + 国际对比（简化版）"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    import json
    with open('v9_papers_filtered.json', 'r') as f:
        papers = json.load(f)
    
    print(f"加载 {len(papers)} 篇论文")
    
    prompt = """# 案例分析与国际对比

## 1. 典型案例（3个）

### 案例1：儿科AI问诊
场景：
功能：
效果：
控费价值：

### 案例2：急诊影像诊断
场景：
功能：
效果：
控费价值：

### 案例3：保险理赔审核
场景：
功能：
效果：
控费价值：

## 2. 中美对比

| 维度 | 中国 | 美国 |
|------|------|------|
| 政策支持 | | |
| 技术成熟度 | | |
| 商业化进展 | | |
| 医保覆盖 | | |

## 3. 中国机遇与挑战

机遇：
1.
2.
3.

挑战：
1.
2.
3.

用中文回答，完整填写所有表格。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v11.0-20260324-final/'
    
    print("\n[生成补充内容...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '01_case_studies.md')
    
    if report:
        print(f"\n✅ 完成，长度: {len(report)} 字符")
        print(f"   行数: {report.count(chr(10))}")
    
    return report

if __name__ == '__main__':
    main()
