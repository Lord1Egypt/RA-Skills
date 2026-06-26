"""
自定义异常类

Core 层统一异常定义。
注意：此文件只包含类型定义，不包含具体实现逻辑。
"""


class ComplianceCheckerError(Exception):
    """合规检查器基础异常"""

    ...


class ChecklistError(ComplianceCheckerError):
    """清单相关错误"""

    ...


class DocumentParseError(ComplianceCheckerError):
    """文档解析错误"""

    ...


class CheckExecutionError(ComplianceCheckerError):
    """检查执行错误"""

    ...
