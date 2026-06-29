from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_zodiac_info(
    zodiac: str
) -> Dict[str, Any]:
    """
    获取指定星座的详细信息，包括性格特征、守护星、元素等
    
    Args:
        zodiac: 星座名称（中文或英文）
    
    Returns:
        
    """
    arguments = {
        "zodiac": zodiac
    }
    
    return call_api("1777316659203075", "get_zodiac_info", arguments)

def get_daily_horoscope(
    zodiac: str,
    category: Optional[str] = "luck"
) -> Dict[str, Any]:
    """
    获取指定星座的今日运势
    
    Args:
        zodiac: 星座名称（中文或英文）
        category: 运势类别
    
    Returns:
        
    """
    arguments = {
        "zodiac": zodiac,
        "category": category
    }
    
    return call_api("1777316659203075", "get_daily_horoscope", arguments)

def get_compatibility(
    zodiac1: str,
    zodiac2: str
) -> Dict[str, Any]:
    """
    获取两个星座的配对指数和关系分析
    
    Args:
        zodiac1: 第一个星座名称（中文或英文）
        zodiac2: 第二个星座名称（中文或英文）
    
    Returns:
        
    """
    arguments = {
        "zodiac1": zodiac1,
        "zodiac2": zodiac2
    }
    
    return call_api("1777316659203075", "get_compatibility", arguments)

def get_all_zodiacs(
) -> Dict[str, Any]:
    """
    获取所有星座的基本信息列表
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659203075", "get_all_zodiacs", arguments)

def get_zodiac_by_date(
    month: int,
    day: int
) -> Dict[str, Any]:
    """
    根据出生日期确定星座
    
    Args:
        month: 出生月份（1-12）
        day: 出生日期（1-31）
    
    Returns:
        
    """
    arguments = {
        "month": month,
        "day": day
    }
    
    return call_api("1777316659203075", "get_zodiac_by_date", arguments)

def get_rising_sign(
    birthHour: int,
    birthMinute: int,
    latitude: float,
    longitude: float,
    birthMonth: int,
    birthDay: int,
    birthYear: int
) -> Dict[str, Any]:
    """
    计算上升星座，需要出生时间、地点和日期
    
    Args:
        birthHour: 出生小时（0-23）
        birthMinute: 出生分钟（0-59）
        latitude: 出生地纬度（-90到90）
        longitude: 出生地经度（-180到180）
        birthMonth: 出生月份（1-12）
        birthDay: 出生日期（1-31）
        birthYear: 出生年份（1900-2100）
    
    Returns:
        
    """
    arguments = {
        "birthHour": birthHour,
        "birthMinute": birthMinute,
        "latitude": latitude,
        "longitude": longitude,
        "birthMonth": birthMonth,
        "birthDay": birthDay,
        "birthYear": birthYear
    }
    
    return call_api("1777316659203075", "get_rising_sign", arguments)

def get_rising_sign_info(
    risingSign: str
) -> Dict[str, Any]:
    """
    获取指定上升星座的详细信息
    
    Args:
        risingSign: 上升星座名称（中文或英文）
    
    Returns:
        
    """
    arguments = {
        "risingSign": risingSign
    }
    
    return call_api("1777316659203075", "get_rising_sign_info", arguments)

