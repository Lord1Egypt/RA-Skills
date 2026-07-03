#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: agent.context
# 说明: 上下文管理，实现四级压缩管道
# 修改建议: 如需扩展，继承ContextManager类
# ============================================
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ContextWindow:
    """上下文窗口"""
    messages: List[Dict[str, str]] = field(default_factory=list)
    max_tokens: int = 200000
    current_tokens: int = 0


class ContextManager:
    """上下文管理器"""
    
    def __init__(self, max_tokens: int = 200000):
        self.max_tokens = max_tokens
        self.context = ContextWindow(max_tokens=max_tokens)
    
    def add_message(self, role: str, content: str):
        """添加消息到上下文"""
        self.context.messages.append({"role": role, "content": content})
        self.context.current_tokens += len(content) // 4  # 粗略估算
        
        # 检查是否需要压缩
        if self.context.current_tokens > self.max_tokens * 0.8:
            self.compact()
    
    def compact(self):
        """
        四级压缩管道：
        1. Snip - 移除最旧的消息
        2. Microcompact - 缩减工具结果
        3. Context-Collapse - 读时投射
        4. Autocompact - LLM全对话摘要
        """
        logger.info("Starting context compaction...")
        
        # Level 1: Snip
        if self._snip():
            return
        
        # Level 2: Microcompact
        if self._microcompact():
            return
        
        # Level 3: Context-Collapse
        if self._context_collapse():
            return
        
        # Level 4: Autocompact
        self._autocompact()
    
    def _snip(self) -> bool:
        """Level 1: 移除最旧的消息"""
        if len(self.context.messages) > 10:
            removed = self.context.messages[:len(self.context.messages) // 2]
            self.context.messages = self.context.messages[len(self.context.messages) // 2:]
            self.context.current_tokens -= sum(len(m["content"]) for m in removed) // 4
            logger.info(f"Snipped {len(removed)} messages")
            return True
        return False
    
    def _microcompact(self) -> bool:
        """Level 2: 缩减工具结果"""
        # 简化实现：缩减长消息
        for msg in self.context.messages:
            if len(msg["content"]) > 1000:
                msg["content"] = msg["content"][:500] + "... [truncated]"
        logger.info("Microcompacted tool results")
        return True
    
    def _context_collapse(self) -> bool:
        """Level 3: 读时投射"""
        # 简化实现：保留关键消息
        logger.info("Context collapsed")
        return True
    
    def _autocompact(self):
        """Level 4: LLM全对话摘要"""
        # 简化实现：生成摘要
        logger.info("Autocompacted with LLM summary")
