"""
Agent 核心类
规模: Minimal
预期行数: ~60行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. 创建LLM客户端 (直接实例化, 不使用工厂)
2. run() 方法 - 单轮对话: 发送消息 → 获取响应 → 返回
3. 简单的错误处理 (try/except)

⚠ 不需要事件循环、工具系统、权限系统
⚠ 这是最简单的 Agent 实现, 仅做 LLM 调用封装
"""

from typing import Optional

# TODO: 导入 LLM 客户端 (直接使用 SDK)
# import openai
# import anthropic

class Agent:
    """极简 Agent - 单轮LLM调用封装"""

    # TODO: 实现 __init__, run(), 简单错误处理
    pass