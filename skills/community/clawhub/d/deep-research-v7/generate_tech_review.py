#!/usr/bin/env python3
"""生成技术综述"""

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
    
    # 生成技术综述
    prompt = """# AI大模型问诊诊疗价值深度研究 - 技术综述

## 研究主题
对比四代诊疗技术的能力演进：
1. **第一代**：人类医生问诊
2. **第二代**：规则专家系统（1970s-2000s）
3. **第三代**：早期机器学习（2010s-2020）
4. **第四代**：AI大语言模型（2020-现在）

请基于提供的论文，分析：

### 1. 诊断准确率对比
- 各代技术的准确率范围是什么？
- AI大模型相对前几代提升了多少百分点？
- AI vs 人类医生，谁的准确率更高？

### 2. 关键能力维度对比
对比四代技术在以下维度：
- 知识覆盖广度
- 自然语言理解能力
- 处理非结构化数据能力
- 知识更新速度
- 可解释性
- 边际成本

### 3. 技术代际演进的核心驱动力
为什么大模型能超越前两代？核心技术突破是什么？

### 4. 结论
AI大模型相对传统方法究竟有多大提升？哪些场景已经超越，哪些场景仍需人类？

请引用相关论文，给出具体数据。用中文回答，结构清晰。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成技术综述...]")
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '02_technical_review.md')
    
    if report:
        print(f"\n✅ 技术综述已保存，长度: {len(report)} 字符")
    
    return report

if __name__ == '__main__':
    main()
