#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: utils.errors
# 说明: 错误定义
# 修改建议: 如需扩展，添加新的错误类型
# ============================================


class AgentError(Exception):
    """Agent基础错误"""
    pass


class LLMError(AgentError):
    """LLM调用错误"""
    pass


class ToolError(AgentError):
    """工具执行错误"""
    pass


class PermissionDeniedError(AgentError):
    """权限拒绝错误"""
    pass


class ContextOverflowError(AgentError):
    """上下文溢出错误"""
    pass


class SessionNotFoundError(AgentError):
    """会话未找到错误"""
    pass
