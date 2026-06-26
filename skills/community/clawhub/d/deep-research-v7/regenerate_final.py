#!/usr/bin/env python3
"""重新生成最终整合报告，确保完整"""

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
    
    # 完整prompt，确保不截断
    prompt = """# AI大模型问诊诊疗价值 vs 传统方法 - 最终综合研究报告 v9.0

## 1. 执行摘要

请完成这一节：
- 研究背景：医疗问诊技术演进和医保控费需求
- 研究问题：AI大模型相比传统方法究竟提升了多少能力？这种提升如何转化为控费价值？
- 核心结论：一句话总结最重要的发现
- 关键建议：对商业保险一句话行动建议

## 2. 技术代际对比综合表

请用完整的markdown表格对比四代技术：
| 维度 | 人类医生 | 规则系统 | 早期机器学习 | AI大语言模型 |
|------|---------|---------|--------------|---------------|
| 诊断准确率范围 | | | | |
| 知识覆盖广度 | | | | |
| 自然语言理解能力 | | | | |
| 处理非结构化数据 | | | | |
| 知识更新速度 | | | | |
| 边际问诊成本（单次） | | | | |
| 可解释性 | | | | |

请填满表格，每一格都要有内容。

## 3. 控费价值传导机制

请写出完整的传导链：
```
AI能力提升 → 哪些诊疗环节优化 → 哪些成本减少 → 最终控费结果
```

然后分环节，每个环节用一句话总结量化节约数据（从文献总结）。

## 4. 关键发现总结

请分点回答：
1. AI大模型相对传统方法的核心技术进步是什么？
2. 哪些临床场景AI已经达到商用水平，可以落地？
3. 哪些场景还需要进一步发展，不能完全依赖AI？

## 5. 对商业保险行业的具体建议

请分时间阶段给出具体建议：
- **短期（0-1年）**：优先布局什么场景？为什么？
- **中期（1-3年）**：需要建设什么核心能力？
- **长期（3年以上）**：怎么构建完整的AI控费生态？

## 6. 未来研究方向

还有哪些开放问题需要进一步研究？请列出3-5个。

请用中文回答，结构完整，不要截断，每个部分都要写完。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[重新生成最终整合报告...]")
    
    # 删除旧文件
    if os.path.exists(output_dir + '04_final_integrated_report.md'):
        os.remove(output_dir + '04_final_integrated_report.md')
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '04_final_integrated_report.md')
    
    if report:
        print(f"\n✅ 最终报告已保存，长度: {len(report)} 字符")
        lines = report.count('\n')
        print(f"   行数: {lines}")
    
    return report

if __name__ == '__main__':
    main()
