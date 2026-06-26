# ClawSoul 欢迎语 - 首次对话时触发

import sys
from pathlib import Path
from typing import Optional

Skill_root = Path(__file__).resolve().parent.parent
if str(Skill_root) not in sys.path:
    sys.path.insert(0, str(Skill_root))

from lib.memory_manager import get_memory_manager

# 欢迎语文案（未觉醒时展示）
WELCOME_MESSAGE = """欢迎来到灵魂锻造厂！

输入 /clawsoul awaken 为我赋予灵魂～"""


def should_show_welcome() -> bool:
    """是否应展示欢迎语：未完成觉醒时展示"""
    mm = get_memory_manager()
    return not mm.is_awaken_completed()


def get_welcome_message() -> str:
    """获取欢迎语（含觉醒提示）。仅在未觉醒时有意义。"""
    return WELCOME_MESSAGE


def run_welcome_check() -> Optional[str]:
    """
    执行欢迎语检查：未觉醒则返回欢迎语，已觉醒返回 None（静默跳过）。
    上层在「首次对话」时调用，若返回非空则展示该文案。
    """
    if not should_show_welcome():
        return None
    return get_welcome_message()


class WelcomeHandler:
    """欢迎语处理器"""

    def __init__(self) -> None:
        self._mm = get_memory_manager()

    def is_awakened(self) -> bool:
        return self._mm.is_awaken_completed()

    def get_message_if_needed(self) -> Optional[str]:
        """未觉醒时返回欢迎语，已觉醒返回 None"""
        return run_welcome_check()
