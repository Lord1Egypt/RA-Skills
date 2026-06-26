#!/usr/bin/env python3
"""
测试简化版：只搜索arxiv，减少网络请求
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    topic = """大语言模型AI应用在2026年3月最近一周内，最重要的技术进展有哪些？列出最重要的10篇预印本，分别讲了什么，为什么重要。"""
    
    # 只搜索arxiv，减少网络请求
    result = tools.full_research_flow(
        topic, 
        sources=['arxiv'],
        max_results=20
    )
    
    # 保存结果
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/ai-research/weekly-progress/'
    os.makedirs(output_dir, exist_ok=True)
    
    if result['report']:
        output_file = f"{output_dir}20260317-20260324-top-10-progress.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['report'])
        print(f"\n✅ 报告已保存: {output_file}")
    
    return result

if __name__ == '__main__':
    main()
