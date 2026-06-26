#!/usr/bin/env python3
"""统一异常体系"""

class SkillError(Exception):
    def __init__(self, message: str, code: int = 500, data: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data or {}

class AuthError(SkillError):
    def __init__(self, message: str = "AK 无效或已过期"):
        super().__init__(message, code=401)

class ParamError(SkillError):
    def __init__(self, message: str = "请求参数不合法"):
        super().__init__(message, code=400)

class RateLimitError(SkillError):
    def __init__(self, message: str = "请求被限流，请稍后重试"):
        super().__init__(message, code=429)

class ServiceError(SkillError):
    def __init__(self, message: str = "服务异常，请稍后重试"):
        super().__init__(message, code=500)
