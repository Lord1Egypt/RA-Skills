#!/usr/bin/env python3
"""
统一异常体系

所有 capability 的 service 层抛出此处定义的异常，
由 cmd 层统一捕获并转为 {success: false, markdown, data} 输出。
"""


class SkillError(Exception):
    """所有 skill 异常的基类"""

    def __init__(self, message: str, code: int = 500, data: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data or {}


class ParamError(SkillError):
    """请求参数不合法 (400)"""

    def __init__(self, message: str = "请求参数不合法"):
        super().__init__(message, code=400)


class RateLimitError(SkillError):
    """请求被限流 (429)"""

    def __init__(self, message: str = "请求被限流，请稍后重试"):
        super().__init__(message, code=429)


class ServiceError(SkillError):
    """服务端异常 / 网络异常 (500)"""

    def __init__(self, message: str = "服务异常，请稍后重试"):
        super().__init__(message, code=500)


class AuthError(SkillError):
    """认证失败 (401)"""

    def __init__(self, message: str = "认证失败，请检查 AK 配置"):
        super().__init__(message, code=401)


class TimeoutError(SkillError):
    """请求超时"""

    def __init__(self, message: str = "请求超时，请稍后重试"):
        super().__init__(message, code=504)
