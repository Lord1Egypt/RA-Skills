#!/usr/bin/env python3
"""
测试修复版：搜索正常，生成报告
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    topic = """大语言模型AI应用在2026年3月最近一周内（3月17日-3月24日），最重要的技术进展有哪些？列出arxiv上最新预印本中最重要的10篇，分别讲了什么，为什么这10篇最重要。"""
    
    # 只搜索arxiv
    print("[1] 搜索arxiv...")
    papers = tools.search(topic, sources=['arxiv'], max_results=20)
    print(f"   共找到 {len(papers)} 篇")
    
    print("\n[2] 生成Survey报告...")
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/ai-research/weekly-progress/'
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}20260317-20260324-top-10-progress.md"
    
    report = tools.generate_survey_report(papers, topic, output_path=output_file)
    
    if report:
        print(f"\n✅ 报告已保存: {output_file}")
        print(f"   报告长度: {len(report)} 字符")
    
    return {
        'papers': papers,
        'report': report
    }

if __name__ == '__main__':
    main()
