from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_templates(
    query: str,
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
根据关键词搜索 epub360 模板

Args:
    query: 搜索关键词，例如：商务、教育、科技等
    limit: 返回结果数量限制，默认10个，最多50个

Returns:
    JSON 格式的搜索结果

    
    Args:
        query: null
        limit: null
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777419078389763", "search_templates", arguments)

