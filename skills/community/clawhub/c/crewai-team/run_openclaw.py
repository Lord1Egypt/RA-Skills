#!/usr/bin/env python3
"""
CrewAI - OpenClaw 集成脚本
先生，在 OpenClaw 中直接调用这个脚本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用已配置的 API Key
os.environ["OPENAI_API_KEY"] = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
os.environ["OPENAI_API_BASE"] = "https://coding.dashscope.aliyuncs.com/v1"

from team_config_multi_model import create_product_team

def analyze_product(product_idea: str) -> str:
    """
    分析产品创意，返回 PRD 文档
    
    Args:
        product_idea: 产品创意描述
    
    Returns:
        PRD 文档内容
    """
    print(f"🚀 开始分析：{product_idea}")
    
    # 创建团队
    crew = create_product_team(product_idea, verbose=False)
    
    # 执行分析
    result = crew.kickoff()
    
    return str(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3.10 run_openclaw.py <产品创意>")
        sys.exit(1)
    
    product_idea = " ".join(sys.argv[1:])
    result = analyze_product(product_idea)
    print(result)
