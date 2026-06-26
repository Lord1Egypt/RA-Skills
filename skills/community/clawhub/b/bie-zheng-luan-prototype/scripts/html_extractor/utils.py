"""
辅助函数模块
提供HTML元素查找等通用功能
"""

from typing import List, Any


def find_by_patterns(container, patterns: List[str], find_all: bool = False) -> Any:
    """
    根据多个CSS选择器模式查找元素

    Args:
        container: BeautifulSoup元素容器
        patterns: CSS选择器模式列表
        find_all: 是否查找所有匹配元素

    Returns:
        单个元素或元素列表
    """
    results = []
    for pattern in patterns:
        if not pattern:
            continue
        try:
            if find_all:
                found = container.select(pattern)
                results.extend(found)
            else:
                found = container.select_one(pattern)
                if found:
                    return found
        except Exception:
            pass
    return results if find_all else None