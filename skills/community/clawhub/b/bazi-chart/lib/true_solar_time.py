"""
真太阳时修正模块
公式：真太阳时 = 北京时间 + (出生地经度 - 120°) × 4分钟/度 + 均时差(EoT)
"""

import math
from datetime import datetime, timedelta, timezone

CST = timezone(timedelta(hours=8))


def equation_of_time(dt):
    """
    计算均时差 (Equation of Time)
    使用 Spencer 公式（精度约 ±30 秒）
    
    Args:
        dt: datetime 对象
    
    Returns:
        均时差（分钟），正值表示真太阳时快于平太阳时
    """
    # 一年中的天数（从1月1日起）
    day_of_year = dt.timetuple().tm_yday
    # 日角 B（弧度）
    B = 2 * math.pi * (day_of_year - 81) / 365.0
    
    # Spencer 公式（结果单位：分钟）
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    
    return eot


def correct_to_true_solar_time(dt_cst, longitude):
    """
    将北京时间修正为真太阳时
    
    Args:
        dt_cst: 北京时间 datetime (aware or naive, 按CST处理)
        longitude: 出生地经度（度）
    
    Returns:
        真太阳时 datetime (CST aware)
    """
    # 确保有时区信息
    if dt_cst.tzinfo is None:
        dt_cst = dt_cst.replace(tzinfo=CST)
    
    # 经度修正：每度差4分钟
    longitude_correction = (longitude - 120.0) * 4.0  # 分钟
    
    # 均时差
    eot = equation_of_time(dt_cst)
    
    # 总修正量（分钟）
    total_correction = longitude_correction + eot
    
    # 应用修正
    true_solar_time = dt_cst + timedelta(minutes=total_correction)
    
    return true_solar_time


def get_correction_info(dt_cst, longitude):
    """
    获取真太阳时修正的详细信息
    
    Returns:
        dict with correction details
    """
    eot = equation_of_time(dt_cst)
    lon_corr = (longitude - 120.0) * 4.0
    total = lon_corr + eot
    true_time = correct_to_true_solar_time(dt_cst, longitude)
    
    return {
        "longitude": longitude,
        "longitude_correction_min": round(lon_corr, 2),
        "equation_of_time_min": round(eot, 2),
        "total_correction_min": round(total, 2),
        "original_time": dt_cst.strftime("%H:%M"),
        "true_solar_time": true_time.strftime("%H:%M"),
    }
