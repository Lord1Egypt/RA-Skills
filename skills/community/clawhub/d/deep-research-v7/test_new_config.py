#!/usr/bin/env python3
"""测试新配置：minimax-m2.5 + 64k tokens"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    # 简单测试
    topic = "AI大模型在医疗问诊中的主要应用场景"
    
    print(f"[测试] 模型: minimax-m2.5, max_tokens: 64000")
    print(f"[测试] 主题: {topic}")
    print("\n生成中...")
    
    # 搜索
    papers = tools.search(topic, sources=['arxiv'], max_results=5)
    print(f"找到 {len(papers)} 篇论文")
    
    # 生成报告
    report = tools.generate_survey_report(papers, topic)
    
    if report:
        print(f"\n✅ 测试成功！报告长度: {len(report)} 字符")
        print(f"   行数: {report.count(chr(10))}")
    else:
        print("\n❌ 测试失败")
    
    return report

if __name__ == '__main__':
    main()
