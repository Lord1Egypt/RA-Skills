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


class AuthError(SkillError):
    """本地网关登录态失效 / 未授权 / accio-mcp-cli 不可用 (401)"""

    def __init__(self, message: str = "本地网关鉴权失败或登录态失效"):
        super().__init__(message, code=401)


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
