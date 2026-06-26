"""
翻译管理模块
"""
import json
from pathlib import Path
from typing import Optional, Any

# 翻译文件目录
I18N_DIR = Path(__file__).parent

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

# 支持的语言
SUPPORTED_LANGUAGES = ['zh', 'en']

# 当前语言
_current_language: str = 'zh'

# 翻译数据缓存
_translations: dict = {}


def load_translations(lang: str) -> dict:
    """加载指定语言的翻译文件"""
    filepath = I18N_DIR / f"{lang}.json"
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_saved_language() -> str:
    """从配置文件读取保存的语言设置"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                lang = config.get('language', 'zh')
                if lang in SUPPORTED_LANGUAGES:
                    return lang
        except Exception:
            pass
    return 'zh'


def save_language_to_config(lang: str):
    """保存语言设置到配置文件"""
    config = {'language': lang}
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def set_language(lang: str, save: bool = True) -> bool:
    """设置当前语言

    Args:
        lang: 语言代码 ('zh' 或 'en')
        save: 是否保存到配置文件
    """
    global _current_language, _translations

    if lang not in SUPPORTED_LANGUAGES:
        return False

    _current_language = lang
    _translations = load_translations(lang)

    if save:
        save_language_to_config(lang)

    return True


def get_current_language() -> str:
    """获取当前语言"""
    return _current_language


def get_text(key: str, lang: Optional[str] = None) -> str:
    """
    获取翻译文本

    Args:
        key: 翻译键，使用点号分隔，如 "ui.load_failed" 或 "events.start_1.description"
        lang: 指定语言，不指定则使用当前语言

    Returns:
        翻译后的文本，如果找不到则返回键本身
    """
    if lang:
        trans = load_translations(lang)
    else:
        trans = _translations

    # 如果翻译数据为空，加载默认语言
    if not trans:
        trans = load_translations('zh')

    # 按点号分割键路径
    keys = key.split('.')
    value = trans

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            # 找不到翻译，返回键本身
            return key

    if isinstance(value, str):
        return value
    return key


def get_event_text(event_id: str, field: str, lang: Optional[str] = None) -> str:
    """
    获取事件翻译文本

    Args:
        event_id: 事件ID
        field: 字段名 (description 或 choices.xxx)
        lang: 指定语言

    Returns:
        翻译后的文本
    """
    key = f"events.{event_id}.{field}"
    return get_text(key, lang)


def get_choice_text(event_id: str, choice_id: str, lang: Optional[str] = None) -> str:
    """
    获取选项翻译文本

    Args:
        event_id: 事件ID
        choice_id: 选项ID
        lang: 指定语言

    Returns:
        翻译后的文本
    """
    return get_event_text(event_id, f"choices.{choice_id}", lang)


def get_item_text(item_id: str, field: str = 'description', lang: Optional[str] = None) -> str:
    """
    获取物品翻译文本

    Args:
        item_id: 物品ID
        field: 字段名 (name 或 description)
        lang: 指定语言

    Returns:
        翻译后的文本
    """
    key = f"items.{item_id}.{field}"
    return get_text(key, lang)


def get_ability_text(ability_id: str, field: str = 'description', lang: Optional[str] = None) -> str:
    """
    获取能力翻译文本

    Args:
        ability_id: 能力ID
        field: 字段名 (name 或 description)
        lang: 指定语言

    Returns:
        翻译后的文本
    """
    key = f"abilities.{ability_id}.{field}"
    return get_text(key, lang)


def get_ui_text(key: str, lang: Optional[str] = None) -> str:
    """
    获取UI翻译文本

    Args:
        key: UI键名
        lang: 指定语言

    Returns:
        翻译后的文本
    """
    return get_text(f"ui.{key}", lang)


# 初始化时加载保存的语言设置
set_language(load_saved_language(), save=False)
