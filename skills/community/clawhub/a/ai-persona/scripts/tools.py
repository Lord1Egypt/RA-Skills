from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def summon_persona(
    persona_name: str
) -> Dict[str, Any]:
    """
    召唤指定人格来处理任务
    
    Args:
        persona_name: 人格名称（如：暴躁老哥、自省姐、粉丝妹）
    
    Returns:
        
    """
    arguments = {
        "persona_name": persona_name
    }
    
    return call_api("1777316659338243", "summon_persona", arguments)

def list_personas(
) -> Dict[str, Any]:
    """
    列出所有可用的人格
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659338243", "list_personas", arguments)

def version(
) -> Dict[str, Any]:
    """
    获取当前MCP服务版本信息
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659338243", "version", arguments)

def interactive_persona(
) -> Dict[str, Any]:
    """
    智能人格协作分析 - 根据当前对话上下文自动选择合适的人格进行逐步分析
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659338243", "interactive_persona", arguments)

