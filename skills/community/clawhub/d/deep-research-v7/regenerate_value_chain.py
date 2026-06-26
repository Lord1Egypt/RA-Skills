#!/usr/bin/env python3
"""重新生成完整价值链分析"""

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

## 研究问题
AI大模型问诊能力提升，如何传导为医保/商保控费价值？

请基于提供的论文，完整分析以下内容：

### 1. 研究背景
- AI大模型在医疗问诊领域的发展现状
- 医保/商保当前面临的成本压力
- 核心研究问题陈述

### 2. 论文总结表格
请列出所有相关论文，每篇一行，包含：编号、论文标题、研究主题、核心贡献简述

### 3. 关键技术
请总结支撑AI问诊控费的关键技术：
- 指令微调
- 多代理协同
- 信息融合
- 可信度评估
- 不确定性推理

每个技术简要说明它对控费的贡献。

### 4. 控费价值传导机制
请写出完整的传导链：
```
AI能力提升 → 哪些环节优化 → 哪些成本减少 → 最终控费结果
```

然后分环节分析：
1. 初筛分诊：能减少多少百分比的什么成本？
2. 检查/检验推荐：能减少多少百分比的不必要检查？
3. 重症早期预警：能降低多少百分比的长期治疗成本？
4. 慢病持续管理：能减少多少百分比的并发症？
5. 理赔审核：能减少多少百分比的欺诈和过度理赔？

每个环节请给出基于文献的量化数据范围。

### 5. 场景价值排序
按控费价值从大到小排序这五个场景，并说明排序理由。

### 6. 风险与局限性
分析哪些因素会限制AI控费价值的实现：
- 误诊风险
- 责任界定
- 数据隐私
- 医生/患者接受度
- 其他

### 7. 对商业保险的建议
给出具体落地建议：
- 短期（0-1年）优先做什么
- 中期（1-3年）建设什么能力
- 长期（3年以上）怎么构建生态

请完整写出所有章节，不要截断，结构清晰。用中文回答。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[重新生成完整价值链分析...]")
    
    # 删除旧文件
    if os.path.exists(output_dir + '03_value_chain_analysis.md'):
        os.remove(output_dir + '03_value_chain_analysis.md')
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '03_value_chain_analysis.md')
    
    if report:
        print(f"\n✅ 价值链分析已保存，长度: {len(report)} 字符")
        lines = report.count('\n')
        print(f"   行数: {lines}")
    
    return report

if __name__ == '__main__':
    main()
