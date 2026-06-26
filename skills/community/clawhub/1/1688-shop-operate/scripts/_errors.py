#!/usr/bin/env python3
"""
统一异常体系
"""


class SkillError(Exception):
    def __init__(self, message: str, code: int = 500, data: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data or {}


class AuthError(SkillError):
    """AK 无效 / 签名失败 / 未配置 (401)"""
    def __init__(self, message: str = "AK 无效或已过期"):
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


class GatewayAuthError(SkillError):
    """
    1688 网关返回的 Token 相关错误（Agent 可自动恢复）

    当网关响应包含 1688_token_expired、1688_invalid_token 等错误码时抛出。
    Agent 识别 error_code 后自动调用 account-auth-skill 完成授权恢复。
    """
    def __init__(self, error_code: str, message: str, required_scope: str = ""):
        super().__init__(message, code=403)
        self.error_code = error_code
        self.required_scope = required_scope
