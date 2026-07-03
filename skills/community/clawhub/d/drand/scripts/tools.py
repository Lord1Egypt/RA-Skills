from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_randomness_latest(
) -> Dict[str, Any]:
    """
    Get the latest random value from drand quicknet
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659468291", "get_randomness_latest", arguments)

def get_randomness_by_round(
    round: float
) -> Dict[str, Any]:
    """
    Get the random value associated with a specfic round from drand quicknet
    
    Args:
        round: null
    
    Returns:
        
    """
    arguments = {
        "round": round
    }
    
    return call_api("1777316659468291", "get_randomness_by_round", arguments)

def get_randomness_by_time(
    time: float
) -> Dict[str, Any]:
    """
    Get the random value associated with a specific time from drand quicknet
    
    Args:
        time: null
    
    Returns:
        
    """
    arguments = {
        "time": time
    }
    
    return call_api("1777316659468291", "get_randomness_by_time", arguments)

