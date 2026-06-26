#!/usr/bin/env python3
"""
CrewAI 交互式运行脚本
先生，用这个脚本可以逐步查看每个角色的输出
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用已配置的 API Key
os.environ["OPENAI_API_KEY"] = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
os.environ["OPENAI_API_BASE"] = "https://coding.dashscope.aliyuncs.com/v1"

from team_config_multi_model import (
    create_product_team,
    market_analyst,
    design_expert,
    tech_director,
    fullstack_dev,
    qa_expert
)

def run_interactive(product_idea: str):
    """交互式运行，逐步显示每个角色的输出"""
    
    print("=" * 70)
    print("🚀 CrewAI 产品分析 - 交互式运行")
    print("=" * 70)
    print(f"\n📝 产品创意：{product_idea}\n")
    
    # 创建团队
    crew = create_product_team(product_idea, verbose=True)
    
    print("\n" + "=" * 70)
    print("👥 团队准备就绪，开始执行...")
    print("=" * 70 + "\n")
    
    # 执行
    result = crew.kickoff()
    
    print("\n" + "=" * 70)
    print("✅ 分析完成！")
    print("=" * 70)
    
    # 保存结果
    output_file = "prd_output.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# PRD: {product_idea}\n\n")
        f.write(str(result))
    
    print(f"\n💾 结果已保存到：{output_file}")
    print(f"\n📊 完整输出预览:")
    print("-" * 70)
    print(str(result)[:2000] + "..." if len(str(result)) > 2000 else str(result))
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3.10 run_interactive.py <产品创意>")
        print("\n示例:")
        print('  python3.10 run_interactive.py "一个 AI 驱动的需求收集机器人"')
        sys.exit(1)
    
    product_idea = " ".join(sys.argv[1:])
    run_interactive(product_idea)
