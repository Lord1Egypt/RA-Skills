#!/usr/bin/env python3
"""
Skill 统一错误定义
"""


class SkillError(Exception):
    """Skill 基础异常"""
    pass


class AuthError(SkillError):
    """认证失败（AK 未配置、签名无效等）"""
    pass


class ParamError(SkillError):
    """参数不合法"""
    pass


class RateLimitError(SkillError):
    """请求被限流"""
    pass


class ServiceError(SkillError):
    """服务异常（HTTP 错误、业务错误等）"""
    pass


class BrowserError(SkillError):
    """浏览器操作异常"""
    pass


class FlowError(SkillError):
    """绑店流程异常"""
    pass
