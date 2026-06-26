#!/usr/bin/env python3
"""最后一步：生成并合并价值链分析最后一部分"""

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
    
    # 最后一部分prompt
    prompt = """请完成下面这份报告。当前已写到：

```
## 四、控费价值传导机制

### 4.1 传导链概述

AI控费的价值实现遵循以下传导链：

```
AI能力提升 → 诊疗环节优化 → 具体成本节约 → 最终控费结果
```

具体而言：

| 传导阶段 | 机制说明 |
|---------|---------|
| AI能力提升 | 通过上述关键技术的应用，AI系统在诊断准确性、信息处理能力、决策支持水平等方面不断提升 |
| 诊疗环节优化 | AI能力提升带来诊疗流程的优化，包括更准确的初筛分诊
```

请从这里继续写完，完整包含以下章节：

### 4.2 各环节量化节约总结
完成表格：

| 环节 | 量化节约（基于文献） |
|------|----------------------|
| **初筛分诊** | |
| **检查/检验推荐** | |
| **重症早期预警** | |
| **慢病持续管理** | |
| **理赔审核** | |

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
分阶段：
- **短期（0-1年）**：优先做什么？
- **中期（1-3年）**：建设什么能力？
- **长期（3年以上）**：怎么构建生态？

请完整写出所有内容，不要截断。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    
    print("\n[生成最后一部分...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=None)
    
    if report:
        print(f"\n✅ 最后一部分生成，长度: {len(report)} 字符")
        
        # 读取现有文件
        with open(output_dir + '03_value_chain_analysis.md', 'r') as f:
            existing = f.read()
        
        # 合并
        # 找到截断位置
        lines = existing.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if '更准确的初筛分诊' in line:
                break
        
        full = '\n'.join(new_lines) + '\n' + report
        
        with open(output_dir + '03_value_chain_analysis.md', 'w') as f:
            f.write(full)
        
        print(f"\n✅ 完整报告已保存")
        total_lines = full.count('\n')
        print(f"   总行数: {total_lines}")
        
        return full

if __name__ == '__main__':
    main()
