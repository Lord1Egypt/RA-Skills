#!/usr/bin/env python3
"""补充价值链分析最后一部分"""

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
    
    # 最后一部分
    prompt = """请继续完成这份报告，从这里开始写：

...
| 传导阶段 | 机制说明 |
|---------|---------|
| AI能力提升 | 通过上述关键技术的应用，AI系统在诊断准确性、信息处理能力、决策支持水平等方面不断提升 |
| 诊疗环节优化 | AI能力提升带来诊疗流程的优化，包括更准确的初筛分诊

请继续写完：

## 4. 控费价值传导机制
（续）

完成传导机制表格后，继续写：

### 4.2 各环节量化节约总结
分每个环节，给出基于文献的量化数据：
1. **初筛分诊**
2. **检查/检验推荐**
3. **重症早期预警**
4. **慢病持续管理**
5. **理赔审核**

### 5. 场景价值排序
按控费价值从大到小排序这五个场景，每个场景给出排序理由。

### 6. 风险与局限性
分析：
- 误诊风险
- 责任界定
- 数据隐私
- 医生/患者接受度
- 其他

### 7. 对商业保险的具体建议
分阶段给出建议：
- **短期（0-1年）**
- **中期（1-3年）**
- **长期（3年以上）**

请完整写完所有章节，不要截断。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成价值链分析最后一部分...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '03_value_chain_part3.md')
    
    if report:
        print(f"\n✅ 最后一部分已保存，长度: {len(report)} 字符")
        lines = report.count('\n')
        print(f"   行数: {lines}")
    
    # 合并
    print("\n[合并最终完整报告...]")
    with open(output_dir + '03_value_chain_analysis.md', 'r') as f:
        full = f.read()
    
    full += '\n' + report
    
    with open(output_dir + '03_value_chain_analysis.md', 'w') as f:
        f.write(full)
    
    print(f"\n✅ 完整价值链分析已完成")
    total_lines = full.count('\n')
    print(f"   总行数: {total_lines}")
    
    return full

if __name__ == '__main__':
    main()
