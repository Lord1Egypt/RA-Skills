from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def add(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行浮点数加法运算
    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419065937923", "add", arguments)

def subtract(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行浮点数减法运算
    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419065937923", "subtract", arguments)

def multiply(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行浮点数乘法运算
    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419065937923", "multiply", arguments)

def divide(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行浮点数除法运算
Args:
    b: 除数（必须非零）

    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419065937923", "divide", arguments)

def power(
    base: float,
    exponent: float
) -> Dict[str, Any]:
    """
    计算幂运算
    
    Args:
        base: null
        exponent: null
    
    Returns:
        null
    """
    arguments = {
        "base": base,
        "exponent": exponent
    }
    
    return call_api("1777419065937923", "power", arguments)

def sqrt(
    number: float
) -> Dict[str, Any]:
    """
    计算平方根
    
    Args:
        number: null
    
    Returns:
        null
    """
    arguments = {
        "number": number
    }
    
    return call_api("1777419065937923", "sqrt", arguments)

def factorial(
    n: int
) -> Dict[str, Any]:
    """
    计算整数阶乘
    
    Args:
        n: null
    
    Returns:
        null
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777419065937923", "factorial", arguments)

