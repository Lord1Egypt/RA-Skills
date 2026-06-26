"""
农历/阳历转换模块
支持：用户输入自动识别 + 互转
"""

import sxtwl
from typing import Optional, Tuple

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 农历月份别称
LUNAR_MONTHS = {
    1: '正月', 2: '二月', 3: '三月', 4: '四月', 5: '五月', 6: '六月',
    7: '七月', 8: '八月', 9: '九月', 10: '十月', 11: '冬月', 12: '腊月'
}


def solar_to_lunar(year: int, month: int, day: int) -> dict:
    """阳历 → 农历"""
    solar = sxtwl.fromSolar(year, month, day)
    return {
        'year': solar.getLunarYear(),
        'month': solar.getLunarMonth(),
        'day': solar.getLunarDay(),
        'is_leap': solar.isLunarLeap(),
    }


def lunar_to_solar(year: int, month: int, day: int, is_leap: bool = False) -> dict:
    """农历 → 阳历"""
    solar = sxtwl.fromLunar(year, month, day, is_leap)
    return {
        'year': solar.getSolarYear(),
        'month': solar.getSolarMonth(),
        'day': solar.getSolarDay(),
    }


def is_lunar_date(text: str) -> bool:
    """判断输入是否是农历表述"""
    lunar_markers = ['农历', '阴历', '闰']
    return any(m in text for m in lunar_markers)


def parse_birth_date(text: str) -> Tuple[int, int, int, int, bool]:
    """
    解析出生日期字符串，自动识别农历/阳历
    返回：(year, month, day, hour, is_lunar)

    支持格式：
    - 1990年5月15日10时
    - 1990年5月15日 10点
    - 农历1990年5月15日10时
    - 1990/5/15 10
    - 90年5月15日10时
    """
    import re
    text = text.strip()

    # 判断是否农历
    is_lunar = is_lunar_date(text)
    text = text.replace('农历', '').replace('阴历', '').replace('闰', '闰')

    # 提取数字
    nums = re.findall(r'\d+', text)
    if len(nums) < 4:
        raise ValueError(f"日期格式不正确：{text}，示例：1990年5月15日10时")

    year = int(nums[0])
    if year < 100:
        year += 1900 if year >= 50 else 2000
    month = int(nums[1])
    day = int(nums[2])
    hour = int(nums[3]) if len(nums) > 3 else 0

    # 阳历直接返回
    if not is_lunar:
        return year, month, day, hour, False

    # 农历：检查是否闰月
    is_leap = '闰' in text and month > 0

    # 转换为阳历
    solar = lunar_to_solar(year, month, day, is_leap)
    return solar['year'], solar['month'], solar['day'], hour, True


if __name__ == '__main__':
    # 测试
    print("=== 阳历 → 农历 ===")
    print(solar_to_lunar(1986, 2, 19))  # 应该是 1986年1月11日

    print("=== 农历 → 阳历 ===")
    print(lunar_to_solar(1986, 1, 21))  # 应该是 1986年3月1日

    print("=== 解析器测试 ===")
    print(parse_birth_date("1986年2月19日5时"))
    print(parse_birth_date("农历1986年1月21日5时"))
    print(parse_birth_date("1990年5月15日10时"))
    print(parse_birth_date("农历闰六月十五10时"))
