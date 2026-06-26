"""工具函数模块

提供配置管理和提示词管理功能。
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


# 默认配置路径
DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "default_config.json"
USER_CONFIG_DIR = Path.home() / ".nowcoder-search"
USER_CONFIG_PATH = USER_CONFIG_DIR / "config.json"
USER_PROMPTS_DIR = USER_CONFIG_DIR / "prompts"
DEFAULT_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def get_default_config() -> Dict[str, Any]:
    """获取默认配置

    Returns:
        默认配置字典
    """
    with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config() -> Dict[str, Any]:
    """加载用户配置，如果不存在则返回默认配置

    Returns:
        配置字典
    """
    # 如果用户配置存在，优先使用
    if USER_CONFIG_PATH.exists():
        try:
            with open(USER_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # 配置文件损坏，返回默认配置
            return get_default_config()

    # 否则返回默认配置
    return get_default_config()


def save_config(config: Dict[str, Any]) -> None:
    """保存配置到用户目录

    Args:
        config: 配置字典
    """
    # 确保目录存在
    USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # 保存配置
    with open(USER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_prompt(prompt_name: str) -> str:
    """加载提示词模板

    优先从用户目录加载，如果不存在则使用默认模板。

    Args:
        prompt_name: 提示词名称（不含扩展名），如 'report_summary'

    Returns:
        提示词内容
    """
    # 检查用户自定义提示词
    user_prompt_path = USER_PROMPTS_DIR / f"{prompt_name}.md"
    if user_prompt_path.exists():
        with open(user_prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    # 使用默认提示词
    default_prompt_path = DEFAULT_PROMPTS_DIR / f"{prompt_name}.md"
    if default_prompt_path.exists():
        with open(default_prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    raise FileNotFoundError(f"提示词模板不存在: {prompt_name}")


def save_prompt(prompt_name: str, content: str) -> None:
    """保存自定义提示词到用户目录

    Args:
        prompt_name: 提示词名称（不含扩展名）
        content: 提示词内容
    """
    # 确保目录存在
    USER_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    # 保存提示词
    prompt_path = USER_PROMPTS_DIR / f"{prompt_name}.md"
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(content)


def reset_prompt(prompt_name: str) -> bool:
    """重置提示词为默认版本

    Args:
        prompt_name: 提示词名称

    Returns:
        是否成功重置
    """
    user_prompt_path = USER_PROMPTS_DIR / f"{prompt_name}.md"
    if user_prompt_path.exists():
        user_prompt_path.unlink()
        return True
    return False


def format_timestamp(timestamp_ms: int) -> str:
    """格式化时间戳为可读字符串

    Args:
        timestamp_ms: 毫秒级时间戳

    Returns:
        格式化的时间字符串
    """
    from datetime import datetime

    if timestamp_ms == 0:
        return "未知"

    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return dt.strftime("%Y-%m-%d %H:%M")


def get_tag_name(tag_id: Optional[int]) -> str:
    """获取标签名称

    Args:
        tag_id: 标签ID

    Returns:
        标签名称
    """
    tag_map = {
        818: "面经",
        861: "求职进度",
        823: "内推",
        856: "公司评价",
        None: "全部"
    }
    return tag_map.get(tag_id, "未知")


def get_order_name(order: str) -> str:
    """获取排序方式名称

    Args:
        order: 排序方式

    Returns:
        排序方式名称
    """
    order_map = {
        "": "默认排序",
        "create": "按时间排序"
    }
    return order_map.get(order, "未知")
