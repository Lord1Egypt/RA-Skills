"""
ClawSoul 钩子 - 觉醒、状态、注入、欢迎语等指令入口
"""

from .awaken import run_awaken_flow, awaken_start, format_awaken_message, MBTI_NICKNAMES
from .inject import run_inject_flow, parse_token, InjectHandler
from .welcome import run_welcome_check, should_show_welcome, get_welcome_message, WelcomeHandler
from .status import format_status, get_status, run_hook_toggle

__all__ = [
    "run_awaken_flow",
    "awaken_start",
    "format_awaken_message",
    "MBTI_NICKNAMES",
    "run_inject_flow",
    "parse_token",
    "InjectHandler",
    "run_welcome_check",
    "should_show_welcome",
    "get_welcome_message",
    "WelcomeHandler",
    "format_status",
    "get_status",
    "run_hook_toggle",
]
