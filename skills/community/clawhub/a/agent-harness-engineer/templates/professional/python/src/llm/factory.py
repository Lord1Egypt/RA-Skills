"""
LLM 客户端工厂模块
规模: Professional
预期行数: ~60行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. LLMProvider enum - 支持的供应商列表 (ANTHROPIC, OPENAI, LOCAL 等)
2. create_llm_client(provider, config) -> LLMClient 工厂函数:
   - 根据 provider 参数选择对应的客户端实现
   - 从 config 中读取 API Key、模型名称等参数
   - 返回实现了 LLMClient 接口的具体客户端

⚠ 不要硬编码供应商名称, 使用注册表模式或简单的 if/elif 分支
⚠ 配置文件中的 api_key 应从环境变量读取, 不直接写在配置中
⚠ 工厂函数负责客户端初始化, 调用者不需要知道具体实现
"""

from enum import Enum
from typing import Dict, Any

# TODO: 导入 LLM 客户端接口
# from .client import LLMClient

# TODO: 实现供应商枚举和工厂函数
# class LLMProvider(Enum): ...

# def create_llm_client(provider: str, config: Dict[str, Any]) -> LLMClient:
#     """创建 LLM 客户端实例"""
#     pass
pass