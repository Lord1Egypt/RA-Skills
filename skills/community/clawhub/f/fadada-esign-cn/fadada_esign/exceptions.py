#!/usr/bin/env python3
"""
法大大电子签 SDK 异常类
"""


class FaDaDaError(Exception):
    """基础异常类"""
    
    def __init__(self, message, code=None, response=None):
        super().__init__(message)
        self.code = code
        self.response = response


class FaDaDaAuthError(FaDaDaError):
    """认证相关异常"""
    pass


class FaDaDaAPIError(FaDaDaError):
    """API 调用异常"""
    pass


class FaDaDaConfigError(FaDaDaError):
    """配置错误"""
    pass


class FaDaDaFileError(FaDaDaError):
    """文件操作错误"""
    pass
