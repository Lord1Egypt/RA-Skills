"""
八字排盘核心算法
基于 sxtwl 日历库
"""

import sxtwl
from typing import Tuple

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
ELEMENTS = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}
BRANCH_ELEMENTS = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
    '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
    '戌': '土', '亥': '水'
}

# 五行相生：木→火→土→金→水→木
# 五行相克：木克土克水克火克金克木

def get_bazi(year: int, month: int, day: int, hour: int) -> dict:
    """
    排八字
    year/month/day: 阳历日期
    hour: 小时 (0-23)
    """
    # sxtwl 使用12小时制
    hour_gan = hour

    solar = sxtwl.fromSolar(year, month, day)

    year_gz = solar.getYearGZ()
    month_gz = solar.getMonthGZ()
    day_gz = solar.getDayGZ()
    hour_gz = solar.getHourGZ(hour_gan)

    bazi = {
        'year': {'stem': STEMS[year_gz.tg], 'branch': BRANCHES[year_gz.dz]},
        'month': {'stem': STEMS[month_gz.tg], 'branch': BRANCHES[month_gz.dz]},
        'day': {'stem': STEMS[day_gz.tg], 'branch': BRANCHES[day_gz.dz]},
        'hour': {'stem': STEMS[hour_gz.tg], 'branch': BRANCHES[hour_gz.dz]},
    }

    # 八字字符串
    bazi['str'] = (
        f"{bazi['year']['stem']}{bazi['year']['branch']} "
        f"{bazi['month']['stem']}{bazi['month']['branch']} "
        f"{bazi['day']['stem']}{bazi['day']['branch']} "
        f"{bazi['hour']['stem']}{bazi['hour']['branch']}"
    )

    # 五行统计
    bazi['elements'] = {
        '木': 0, '火': 0, '土': 0, '金': 0, '水': 0
    }
    for col in ['year', 'month', 'day', 'hour']:
        bazi['elements'][ELEMENTS[bazi[col]['stem']]] += 1
        bazi['elements'][BRANCH_ELEMENTS[bazi[col]['branch']]] += 1

    # 日主
    bazi['day_master'] = bazi['day']['stem']

    return bazi


def get_day_ganzhi(year: int, month: int, day: int) -> str:
    """获取日干支字符串（用于查日柱）"""
    solar = sxtwl.fromSolar(year, month, day)
    day_gz = solar.getDayGZ()
    return f"{STEMS[day_gz.tg]}{BRANCHES[day_gz.dz]}"


def analyze_wuxing(bazi: dict) -> dict:
    """分析五行强弱"""
    elements = bazi['elements']
    day_master = bazi['day_master']

    # 日主对应五行
    day_element = ELEMENTS[day_master]

    # 计算五行得分（简单版：个数×权重）
    scores = {}
    total = sum(elements.values())

    # 身强：日干在月令旺、相 + 得多助
    # 简单判断：日干是否得月支
    month_branch = bazi['month']['branch']

    # 月支藏干（简化版）
    month_stems_hidden = {
        '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'],
        '卯': ['乙'], '辰': ['戊', '乙', '癸'], '巳': ['丙', '庚', '戊'],
        '午': ['丁', '己'], '未': ['己', '丁', '乙'], '申': ['庚', '壬', '戊'],
        '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
    }

    # 判断日主是否得月令
    # 旺、相月份：木→寅卯月旺、相于冬；火→巳午月旺、相于春；土→辰戌丑未；金→申酉月旺、相于夏；水→亥子月旺、相于秋
    month_season = {
        '寅': '木', '卯': '木',    # 春
        '巳': '火', '午': '火',    # 夏
        '辰': '土', '戌': '土', '未': '土', '丑': '土',  # 四季
        '申': '金', '酉': '金',    # 秋
        '亥': '水', '子': '水',    # 冬
    }

    season = month_season[month_branch]

    strength = elements[day_element]
    if season == day_element:
        strength += 2  # 月令当令
    elif (
        (day_element == '木' and season in ['水']) or
        (day_element == '火' and season in ['木']) or
        (day_element == '土' and season in ['火']) or
        (day_element == '金' and season in ['土']) or
        (day_element == '水' and season in ['金'])
    ):
        strength += 1  # 月令相

    if strength >= 4:
        status = '身强'
    elif strength >= 2:
        status = '身中'
    else:
        status = '身弱'

    bazi['strength'] = status
    bazi['strength_score'] = strength
    bazi['season'] = season

    return bazi


def get_hsci(bazi: dict) -> str:
    """
    获取大运（简化版：仅支持顺逆排）
    大运：阳男阴女顺排，阴男阳女逆排
    这里简化处理，仅输出命理信息字符串
    """
    return bazi['str']


if __name__ == '__main__':
    # 测试：1984年4月4日和文章中张雪峰的八字
    # 文章：甲子 己巳 壬子 乙巳
    # 反推生日...这里先测一个已知八字
    test = get_bazi(1984, 4, 4, 10)
    print("1984年4月4日10时:", test['str'])
    print("五行:", test['elements'])
    test = analyze_wuxing(test)
    print("身强:", test['strength'])
