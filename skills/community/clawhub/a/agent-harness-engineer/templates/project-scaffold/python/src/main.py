#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: main
# 说明: Agent入口文件
# 修改建议: 根据实际需求修改配置加载逻辑
# ============================================
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# 添加src到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from agent.core import AgentCore
from utils.logging import setup_logging


def load_config() -> dict:
    """加载配置"""
    config = {
        "provider": os.getenv("LLM_PROVIDER", "anthropic"),
        "model": os.getenv("LLM_MODEL", "claude-sonnet-4-20250514"),
        "api_key": os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY"),
        "base_url": os.getenv("LOCAL_MODEL_BASE_URL"),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4096")),
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
    }
    return config


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("--test-connection", action="store_true", help="测试LLM连接")
    args = parser.parse_args()
    
    # 设置日志
    setup_logging()
    
    # 加载配置
    config = load_config()
    
    # 创建Agent
    agent = AgentCore(llm_config=config)
    
    if args.test_connection:
        print("Testing LLM connection...")
        # TODO: 实现连接测试
        return
    
    # 交互式循环
    print("=" * 50)
    print("Agent started. Type 'exit' to quit.")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                break
            
            result = await agent.run(user_input)
            print(f"\n{result}")
            
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
