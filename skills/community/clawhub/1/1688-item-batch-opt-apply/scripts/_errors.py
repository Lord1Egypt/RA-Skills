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


class LedgerError(SkillError):
    """台账读写/状态机非法流转 (500)"""

    def __init__(self, message: str = "任务台账读写失败"):
        super().__init__(message, code=500)


class ServiceError(SkillError):
    """服务端/环境异常 (500)"""

    def __init__(self, message: str = "服务异常，请稍后重试"):
        super().__init__(message, code=500)
