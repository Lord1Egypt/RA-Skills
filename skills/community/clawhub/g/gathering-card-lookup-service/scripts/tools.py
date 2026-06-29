from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_card_by_set_and_number(
    set: str,
    collector_number: str
) -> Dict[str, Any]:
    """
    通过系列代码和收集编号获取单张卡牌。
    
    Args:
        set: 系列代码，例如 'NEO'、'MOM'
        collector_number: 收集编号，例如 '1'、'112'、'1a'
    
    Returns:
        
    """
    arguments = {
        "set": set,
        "collector_number": collector_number
    }
    
    return call_api("1777316659870723", "get_card_by_set_and_number", arguments)

def search_cards(
    q: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    order: Optional[str] = None,
    unique: Optional[str] = None,
    priority_chinese: Optional[bool] = None
) -> Dict[str, Any]:
    """
    通过查询字符串搜索卡牌，支持分页和排序。

**查询语法示例:**
- `t:creature c:r` (红色生物)
- `pow>=5 or mv<2` (力量大于等于5或法术力值小于2)
- `o:"draw a card" -c:u` (包含"抓一张牌"的非蓝色牌)
- `(t:instant or t:sorcery) mv<=3` (3费或以下的瞬间或法术)

**分页参数:**
- `page`: 页码 (整数, 默认 1)
- `page_size`: 每页数量 (整数, 默认 20, 最大 100)

**排序参数:**
- `order`: 按字段排序，逗号分隔。前缀 `-` 表示降序
  (例如: `name`, `-mv`, `name,-rarity`)
  默认排序: `name`

**其他参数:**
- `unique`: 去重方式 (id, oracle_id, illustration_id)
- `priority_chinese`: 是否优先显示中文卡牌
    
    Args:
        q: 查询字符串，例如 't:creature c:r'、'pow>=5 or mv<2'、's:TDM -t:creature'
        page: 页码 (默认 1)
        page_size: 每页数量 (默认 20，最大 100)
        order: 排序字段 (例如: name, -mv, rarity)
        unique: 去重方式: id(不去重), oracle_id(按卡牌名去重), illustration_id(按插图去重)
        priority_chinese: 是否优先显示中文卡牌 (默认 true)
    
    Returns:
        
    """
    arguments = {
        "q": q,
        "page": page,
        "page_size": page_size,
        "order": order,
        "unique": unique,
        "priority_chinese": priority_chinese
    }
    
    return call_api("1777316659870723", "search_cards", arguments)

def get_sets(
) -> Dict[str, Any]:
    """
    返回所有MTG卡牌系列的完整数据，按发布日期降序排列
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659870723", "get_sets", arguments)

def get_set(
    set_code: str
) -> Dict[str, Any]:
    """
    根据系列代码获取单个系列的详细信息
    
    Args:
        set_code: 系列代码，例如 'NEO'、'MOM'
    
    Returns:
        
    """
    arguments = {
        "set_code": set_code
    }
    
    return call_api("1777316659870723", "get_set", arguments)

def get_set_cards(
    set_code: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    order: Optional[str] = None,
    priority_chinese: Optional[bool] = None
) -> Dict[str, Any]:
    """
    获取特定系列的所有卡牌，支持分页和排序。
    
    Args:
        set_code: 系列代码，例如 'NEO'、'MOM'
        page: 页码 (默认 1)
        page_size: 每页数量 (默认 20，最大 100)
        order: 排序字段 (例如: collector_number, name, -mv)
        priority_chinese: 是否优先显示中文卡牌 (默认 true)
    
    Returns:
        
    """
    arguments = {
        "set_code": set_code,
        "page": page,
        "page_size": page_size,
        "order": order,
        "priority_chinese": priority_chinese
    }
    
    return call_api("1777316659870723", "get_set_cards", arguments)

def hzls(
    target_sentence: str,
    cut_full_image: Optional[bool] = None,
    with_link: Optional[bool] = None
) -> Dict[str, Any]:
    """
    活字乱刷（使用卡牌图像拼接句子），将输入的文本使用魔法卡牌图像拼接成图片
    
    Args:
        target_sentence: 要拼接的目标句子/文本
        cut_full_image: 是否使用卡牌完整图像 (默认 true)
        with_link: 是否包含链接水印 (默认 true)
    
    Returns:
        
    """
    arguments = {
        "target_sentence": target_sentence,
        "cut_full_image": cut_full_image,
        "with_link": with_link
    }
    
    return call_api("1777316659870723", "hzls", arguments)

