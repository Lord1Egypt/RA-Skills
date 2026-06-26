"""
国际化模块

使用方式:
    from i18n import get_text, set_language, get_current_language
    from i18n import get_event_text, get_choice_text, get_item_text, get_ui_text

    # 设置语言
    set_language('en')

    # 获取翻译
    text = get_text("ui.load_failed")
    desc = get_event_text("start_1", "description")
    choice = get_choice_text("start_1", "continue")
"""

from .translations import (
    get_text,
    set_language,
    get_current_language,
    get_event_text,
    get_choice_text,
    get_item_text,
    get_ability_text,
    get_ui_text,
    load_saved_language,
    SUPPORTED_LANGUAGES,
)

__all__ = [
    'get_text',
    'set_language',
    'get_current_language',
    'get_event_text',
    'get_choice_text',
    'get_item_text',
    'get_ability_text',
    'get_ui_text',
    'load_saved_language',
    'SUPPORTED_LANGUAGES',
]
