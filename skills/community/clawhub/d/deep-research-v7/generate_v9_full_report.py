#!/usr/bin/env python3
"""
生成v9.0完整报告：
1. 技术综述
2. 价值链分析
"""

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
    topic_tech = """# AI大模型问诊诊疗价值深度研究 - 技术综述

## 研究主题
对比四代诊疗技术：人类医生问诊 → 规则专家系统 → 早期机器学习 → AI大语言模型

分析每个代际的技术能力提升：
1. 诊断准确率对比
2. 知识覆盖范围对比
3. 语言理解能力对比
4. 成本结构对比
5. 可解释性对比

请基于提供的44篇论文，总结每个对比维度的研究发现，引用相关论文。

最后给出结论：AI大模型相对传统方法究竟有多大提升？
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[1] 生成技术综述...")
    report_tech = tools.generate_survey_report(papers, topic_tech, output_path=output_dir + '02_technical_review.md')
    
    # 生成价值链分析
    topic_value = """# AI大模型问诊诊疗价值深度研究 - 医保控费价值链分析

## 研究问题
AI大模型问诊能力提升，如何传导为医保/商保控费价值？

请分析：
1. 传导机制：诊断能力提升 → 哪些环节减少成本？
2. 量化证据：现有研究中，AI能减少多少%不必要检查？减少多少%成本？
3. 场景分析：哪个控费场景价值最大（初筛/检查推荐/早期预警/慢病管理）？
4. 风险局限性：哪些限制因素影响控费价值实现？
5. 商业建议：保险行业应该怎么布局？

请基于提供的论文，总结研究发现，给出具体数据和建议。
"""
    
    print("\n[2] 生成价值链分析...")
    report_value = tools.generate_survey_report(papers, topic_value, output_path=output_dir + '03_value_chain_analysis.md')
    
    # 生成最终整合报告
    topic_final = """# AI大模型问诊诊疗价值 vs 传统方法 - 最终综合报告

## 要求
整合之前的分析，给出：
1. 执行摘要（1页）
2. 技术代际对比表
3. 控费价值传导图
4. 关键发现总结
5. 对保险行业的具体建议
6. 未来研究方向

请完整总结，结构清晰。
"""
    
    print("\n[3] 生成最终整合报告...")
    # 把所有论文放进去再次总结
    report_final = tools.generate_survey_report(papers, topic_final, output_path=output_dir + '04_final_survey.md')
    
    print(f"\n✅ 所有报告生成完成！")
    print(f"   输出目录: {output_dir}")
    
    return {
        'papers': papers,
        'tech_review': report_tech,
        'value_chain': report_value,
        'final': report_final
    }

if __name__ == '__main__':
    main()
