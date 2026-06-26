#!/usr/bin/env python3
"""生成最终整合报告"""

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
    
    # 生成最终整合报告
    prompt = """# AI大模型问诊诊疗价值 vs 传统方法 - 最终综合研究报告 v9.0

## 研究要求
对比四代诊疗技术：**人类医生 → 规则专家系统 → 早期机器学习 → AI大语言模型**

请整合所有分析，给出：

### 1. 执行摘要
- 研究背景和问题
- 核心结论一句话总结
- 对保险行业的关键建议

### 2. 技术代际对比综合表
用markdown表格对比四代技术在以下维度：
- 诊断准确率范围
- 知识覆盖广度
- 自然语言理解
- 处理非结构化数据
- 知识更新速度
- 边际问诊成本
- 可解释性

### 3. 控费价值传导机制
清晰描述完整传导链：
```
AI能力提升 → 环节优化 → 成本节约 → 控费结果
```
并用一句话总结每个环节的量化节约。

### 4. 关键发现总结
- AI大模型相对传统方法的核心进步
- 哪些场景已经可以商用
- 哪些场景还需要发展

### 5. 对商业保险行业的具体建议
- 短期（0-1年）：优先布局什么场景？
- 中期（1-3年）：需要建设什么能力？
- 长期（3年以上）：怎么构建完整生态？

### 6. 未来研究方向
还有哪些开放问题需要进一步研究？

请用中文回答，结构清晰，结论明确。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成最终整合报告...]")
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '04_final_integrated_report.md')
    
    if report:
        print(f"\n✅ 最终报告已保存，长度: {len(report)} 字符")
    
    # 统计最终文件
    print(f"\n📊 最终目录:")
    for f in os.listdir(output_dir):
        if f.endswith('.md'):
            size = os.path.getsize(output_dir + f)
            lines = open(output_dir + f).read().count('\n')
            print(f"  {f}: {lines}行, {size}字节")
    
    return report

if __name__ == '__main__':
    main()
