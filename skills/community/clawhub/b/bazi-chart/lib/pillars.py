"""
四柱计算模块
年柱、月柱、日柱、时柱的天干地支计算
"""

from datetime import datetime, timedelta, timezone
from .constants import TIAN_GAN, DI_ZHI, GAN_YINYANG
from .solar_terms import determine_month_zhi
from .hidden_stems import get_hidden_stems

CST = timezone(timedelta(hours=8))


def _year_gan_zhi(year, birth_dt_cst):
    """
    计算年柱（干支）
    注意：年柱以立春为界，立春前算上一年
    
    Args:
        year: 公历年份
        birth_dt_cst: 出生时间(CST) —— 用于判断是否过了立春
    
    Returns:
        (gan, zhi): 年干, 年支
    """
    from .solar_terms import get_jieqi_moment
    
    # 获取当年立春时刻
    lichun = get_jieqi_moment(year, "立春")
    
    # 如果出生在立春之前，算上一年
    if birth_dt_cst < lichun:
        year -= 1
    
    # 天干：(year - 4) % 10 -> 甲=0
    gan_idx = (year - 4) % 10
    # 地支：(year - 4) % 12 -> 子=0
    zhi_idx = (year - 4) % 12
    
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx]


def _month_gan_zhi(year_gan, month_zhi_idx):
    """
    计算月柱
    月干由年干推算（五虎遁月法）
    
    五虎遁月法：
    甲己年 -> 寅月起丙寅
    乙庚年 -> 寅月起戊寅
    丙辛年 -> 寅月起庚寅
    丁壬年 -> 寅月起壬寅
    戊癸年 -> 寅月起甲寅
    
    Args:
        year_gan: 年干
        month_zhi_idx: 月支在DI_ZHI中的索引
    
    Returns:
        (gan, zhi): 月干, 月支
    """
    # 年干决定寅月的起始天干
    start_gan = {
        "甲": 2, "己": 2,  # 丙
        "乙": 4, "庚": 4,  # 戊
        "丙": 6, "辛": 6,  # 庚
        "丁": 8, "壬": 8,  # 壬
        "戊": 0, "癸": 0,  # 甲
    }
    
    # 寅月的天干索引
    yin_gan_idx = start_gan[year_gan]
    
    # 月支索引相对于寅月(2)的偏移
    offset = (month_zhi_idx - 2) % 12
    
    # 月干索引
    month_gan_idx = (yin_gan_idx + offset) % 10
    
    return TIAN_GAN[month_gan_idx], DI_ZHI[month_zhi_idx]


def _day_gan_zhi(date):
    """
    计算日柱
    使用高氏日柱公式（简化版）
    以已知基准日推算
    
    基准：1900年1月1日 = 甲戌日 -> 干索引0, 支索引10
    但更精确的基准：2000年1月1日 = 甲子日... 不对
    
    用固定算法：以儒略日为基础
    1900-01-31（农历正月初一）= 甲戌
    
    更简单：已知 1900年1月1日 是 甲戌日（天干0 地支10 -> 干支序数10）
    干支序数 = (JDN + 9) % 60 (其中 JDN 是儒略日数)
    """
    # 计算儒略日数 (JDN)
    y = date.year
    m = date.month
    d = date.day
    
    # 标准儒略日算法
    a = (14 - m) // 12
    y_adj = y + 4800 - a
    m_adj = m + 12 * a - 3
    
    jdn = d + (153 * m_adj + 2) // 5 + 365 * y_adj + y_adj // 4 - y_adj // 100 + y_adj // 400 - 32045
    
    # 已知：2000年1月7日 JDN=2451551 是甲子日 (干支序数=0)
    # 干支序数 = (jdn - 2451551) % 60
    gz_idx = (jdn - 2451551) % 60
    
    gan_idx = gz_idx % 10
    zhi_idx = gz_idx % 12
    
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx]


def _hour_gan_zhi(day_gan, hour):
    """
    计算时柱
    
    五鼠遁时法（日上起时）：
    甲己日 -> 子时起甲子
    乙庚日 -> 子时起丙子
    丙辛日 -> 子时起戊子
    丁壬日 -> 子时起庚子
    戊癸日 -> 子时起壬子
    
    Args:
        day_gan: 日干
        hour: 小时(0-23)
    
    Returns:
        (gan, zhi): 时干, 时支
    """
    # 确定时支
    if hour == 23 or hour == 0:
        zhi_idx = 0  # 子
    else:
        zhi_idx = ((hour + 1) // 2) % 12
    
    # 日干决定子时的起始天干
    start_gan = {
        "甲": 0, "己": 0,  # 甲
        "乙": 2, "庚": 2,  # 丙
        "丙": 4, "辛": 4,  # 戊
        "丁": 6, "壬": 6,  # 庚
        "戊": 8, "癸": 8,  # 壬
    }
    
    zi_gan_idx = start_gan[day_gan]
    hour_gan_idx = (zi_gan_idx + zhi_idx) % 10
    
    return TIAN_GAN[hour_gan_idx], DI_ZHI[zhi_idx]


def calculate_pillars(birth_dt_cst):
    """
    计算四柱八字
    
    Args:
        birth_dt_cst: 出生时间 datetime (CST/真太阳时)
    
    Returns:
        dict: {
            "year": {"stem": str, "branch": str, "hidden_stems": list},
            "month": {"stem": str, "branch": str, "hidden_stems": list},
            "day": {"stem": str, "branch": str, "hidden_stems": list},
            "hour": {"stem": str, "branch": str, "hidden_stems": list},
        }
    """
    # 确保有时区
    if birth_dt_cst.tzinfo is None:
        birth_dt_cst = birth_dt_cst.replace(tzinfo=CST)
    
    # 处理晚子时（23:00-23:59）：日柱需要算下一天
    # 在传统八字中，23:00后属于下一天的子时
    day_date = birth_dt_cst.date()
    if birth_dt_cst.hour == 23:
        day_date = (birth_dt_cst + timedelta(days=1)).date()
    
    # 年柱
    year_gan, year_zhi = _year_gan_zhi(birth_dt_cst.year, birth_dt_cst)
    
    # 月柱（需要节气判断）
    month_zhi_idx = determine_month_zhi(birth_dt_cst)
    month_gan, month_zhi = _month_gan_zhi(year_gan, month_zhi_idx)
    
    # 日柱
    day_gan, day_zhi = _day_gan_zhi(day_date)
    
    # 时柱
    hour_gan, hour_zhi = _hour_gan_zhi(day_gan, birth_dt_cst.hour)
    
    return {
        "year": {
            "stem": year_gan,
            "branch": year_zhi,
            "hidden_stems": get_hidden_stems(year_zhi),
        },
        "month": {
            "stem": month_gan,
            "branch": month_zhi,
            "hidden_stems": get_hidden_stems(month_zhi),
        },
        "day": {
            "stem": day_gan,
            "branch": day_zhi,
            "hidden_stems": get_hidden_stems(day_zhi),
        },
        "hour": {
            "stem": hour_gan,
            "branch": hour_zhi,
            "hidden_stems": get_hidden_stems(hour_zhi),
        },
    }
