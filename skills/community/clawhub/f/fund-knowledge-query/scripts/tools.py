from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def fund.echo(
    message: str
) -> Dict[str, Any]:
    """
    Echo back a message. Example interface for scaffold.
    
    Args:
        message: Text to echo back
    
    Returns:
        
    """
    arguments = {
        "message": message
    }
    
    return call_api("1777316659313667", "fund.echo", arguments)

def fund.knoewledge(
    kw: Optional[str] = None,
    pageSize: Optional[float] = None,
    pageNum: Optional[float] = None
) -> Dict[str, Any]:
    """
    获取的知识库列表信息
    
    Args:
        kw: 关键词，支持模糊查询
        pageSize: 每页数量，默认10
        pageNum: 页码，默认1
    
    Returns:
        
    """
    arguments = {
        "kw": kw,
        "pageSize": pageSize,
        "pageNum": pageNum
    }
    
    return call_api("1777316659313667", "fund.knoewledge", arguments)

def fund.stock_search(
    input: str,
    count: Optional[float] = 10.0
) -> Dict[str, Any]:
    """
    搜索股票信息，基于东方财富API
    
    Args:
        input: 搜索关键字，如股票代码、股票名称或拼音简称
        count: 返回结果数量，默认10，最大50
    
    Returns:
        
    """
    arguments = {
        "input": input,
        "count": count
    }
    
    return call_api("1777316659313667", "fund.stock_search", arguments)

