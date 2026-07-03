from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_completion(
    prompt: str
) -> Dict[str, Any]:
    """
    null
    
    Args:
        prompt: null
    
    Returns:
        
    """
    arguments = {
        "prompt": prompt
    }
    
    return call_api("1777316659317763", "get_completion", arguments)

def analyze_code(
    code: str
) -> Dict[str, Any]:
    """
    null
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659317763", "analyze_code", arguments)

def developer_tip(
    topic: Optional[str] = None
) -> Dict[str, Any]:
    """
    null
    
    Args:
        topic: null
    
    Returns:
        
    """
    arguments = {
        "topic": topic
    }
    
    return call_api("1777316659317763", "developer_tip", arguments)

def gc(
    prompt: str
) -> Dict[str, Any]:
    """
    null
    
    Args:
        prompt: null
    
    Returns:
        
    """
    arguments = {
        "prompt": prompt
    }
    
    return call_api("1777316659317763", "gc", arguments)

def ac(
    code: str
) -> Dict[str, Any]:
    """
    null
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659317763", "ac", arguments)

def tip(
    topic: Optional[str] = None
) -> Dict[str, Any]:
    """
    null
    
    Args:
        topic: null
    
    Returns:
        
    """
    arguments = {
        "topic": topic
    }
    
    return call_api("1777316659317763", "tip", arguments)

