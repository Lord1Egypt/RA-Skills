#!/usr/bin/env python3
"""
测试：大模型应用 2026年3月17日到现在的最重要10个进展
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    topic = """大语言模型AI应用在2026年3月17日到2026年3月24日这一周内，最重要的10个进展是什么？列出相关文章，分别讲了什么，为什么这10篇最重要。"""
    
    result = tools.full_research_flow(
        topic, 
        sources=['arxiv', 'pubmed', 'openalex', 'semantic'],
        max_results=30
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
