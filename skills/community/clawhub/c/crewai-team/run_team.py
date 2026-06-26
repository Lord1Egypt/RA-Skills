#!/usr/bin/env python3
"""
CrewAI 团队 - OpenClaw 集成脚本
先生，用这个脚本可以直接调用 CrewAI 团队
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from team_config import create_product_team

def run_crewai_analysis(product_idea: str):
    """
    运行 CrewAI 产品分析
    
    Args:
        product_idea: 产品创意描述
    
    Returns:
        分析结果
    """
    print(f"🚀 开始分析产品创意：{product_idea[:50]}...")
    print("=" * 60)
    
    try:
        # 创建团队
        crew = create_product_team(product_idea, verbose=True)
        
        # 执行分析
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("✅ 分析完成！")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python run_team.py <产品创意描述>")
        print("\n示例:")
        print('  python run_team.py "一个 AI 驱动的需求收集机器人"')
        sys.exit(1)
    
    product_idea = " ".join(sys.argv[1:])
    run_crewai_analysis(product_idea)
