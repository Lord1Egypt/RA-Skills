"""
统一异常定义 —— 消除跨文件重复定义。

所有 Code Factory 的自定义异常集中在此模块，
避免 orchestrator.py 和 step_handlers/preflight_handler.py 中重复定义同名类。
"""


class PreflightFailedError(Exception):
    """Phase 0 环境预检失败"""
