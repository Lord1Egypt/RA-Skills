"""
上下文管理模块
规模: Professional
预期行数: ~80行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. ContextManager 类
2. build_context() - 构建发送给 LLM 的完整上下文:
   - 系统提示词 (来自 config)
   - 历史消息 (最近 N 条, 按 token 预算截断)
   - 当前用户输入
3. estimate_tokens() - 简单 token 估算 (字符数/4)
4. truncate_history() - 按 token 预算截断历史

⚠ 不导入 tiktoken, 使用字符估算
⚠ 需要管理 token 预算避免超出上下文窗口
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

# TODO: 实现 ContextManager
# class ContextManager:
#     def __init__(self, system_prompt: str, max_context_tokens: int = 100000): ...
#     def build_context(self, messages: List[Dict], user_input: str) -> List[Dict]: ...
#     def estimate_tokens(self, text: str) -> int: ...
#     def truncate_history(self, messages: List[Dict], max_tokens: int) -> List[Dict]: ...
pass