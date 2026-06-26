#!/usr/bin/env python3
"""
八字排盘系统
支持农历输入，排出生辰八字、大运流年、五行分析
"""

import sys
from datetime import datetime, timedelta
from typing import Tuple, List, Dict

# 十天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 十二地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 生肖
SHENGXIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 天干五行
TG_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 地支五行
DZ_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水",
}

# 地支藏干
DZ_CANGGAN = {
    "子": ["癸"], "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"], "卯": ["乙"],
    "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"], "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "辛"], "酉": ["辛"],
    "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"],
}

# 月令地支对应的节气
YUELING = {
    1: "寅", 2: "卯", 3: "辰", 4: "巳",
    5: "午", 6: "未", 7: "申", 8: "酉",
    9: "戌", 10: "亥", 11: "子", 12: "丑",
}

# 月令地支对应的天干（年干起，详见五虎遁）
YUE_GAN = {
    "寅": ["甲", "丙", "戊", "庚", "壬"],
    "卯": ["乙", "丁", "己", "辛", "癸"],
    "辰": ["甲", "丙", "戊", "庚", "壬"],
    "巳": ["乙", "丁", "己", "辛", "癸"],
    "辰": ["甲", "丙", "戊", "庚", "壬"],
    "巳": ["乙", "丁", "己", "辛", "癸"],
    "午": ["丙", "戊", "庚", "壬", "甲"],
    "未": ["丁", "己", "辛", "癸", "乙"],
    "申": ["庚", "壬", "甲", "丙", "戊"],
    "酉": ["辛", "癸", "乙", "丁", "己"],
    "戌": ["庚", "壬", "甲", "丙", "戊"],
    "亥": ["辛", "癸", "乙", "丁", "己"],
    "子": ["壬", "甲", "丙", "戊", "庚"],
    "丑": ["癸", "乙", "丁", "己", "辛"],
}

# 五行强度权重
WUXING_WEIGHT = {
    # 申酉金旺于申酉，亥子水旺于亥子...
    "金": {"申": 1.2, "酉": 1.2, "申酉": 1.5, "辰戌丑未": 0.8},
    "水": {"亥": 1.2, "子": 1.2, "亥子": 1.5, "辰戌丑未": 0.8},
    "木": {"寅": 1.2, "卯": 1.2, "寅卯": 1.5, "申酉": 0.8},
    "火": {"巳": 1.2, "午": 1.2, "巳午": 1.5, "亥子": 0.8},
    "土": {"辰": 1.0, "戌": 1.0, "丑": 1.0, "未": 1.0, "四季": 1.2},
}


def get_year_gan(year: int) -> str:
    """年干：年份-3后除10"""
    return TIANGAN[(year - 3) % 10]


def get_year_zhi(year: int) -> str:
    """年支：年份-3后除12"""
    return DIZHI[(year - 3) % 12]


def get_month_gan(year_gan: str, month: int) -> str:
    """月干：年干 + 月份（详见五虎遁）"""
    # 甲己之年丙作首，乙庚之年戊为头
    # 丙辛必定寻庚起，丁壬壬位顺行流
    # 戊癸之年何方发，甲寅之上好追求
    start_gan = {
        "甲": 0, "丙": 0, "戊": 0, "庚": 0, "壬": 0,  # 阳干
        "乙": 5, "丁": 5, "己": 5, "辛": 5, "癸": 5,  # 阴干
    }
    idx = start_gan.get(year_gan, 0)
    return TIANGAN[(idx + month - 1) % 10]


def get_month_zhi(month: int) -> str:
    """月支：正月为寅"""
    return YUELING[month]


def get_day_gan_index(year: int, month: int, day: int) -> int:
    """计算日干索引：日期+月份*2+年份*5（简化算法）"""
    return (year * 5 + month * 2 + day) % 10


def get_day_zhi_index(year: int, month: int, day: int) -> int:
    """计算日支索引"""
    return (year * 5 + month * 2 + day) % 12


def get_day_gan_zhi(year: int, month: int, day: int) -> Tuple[str, str]:
    """计算日柱"""
    gan_idx = get_day_gan_index(year, month, day)
    zhi_idx = get_day_zhi_index(year, month, day)
    return TIANGAN[gan_idx], DIZHI[zhi_idx]


def get_hour_zhi(hour: int) -> str:
    """时支：23:00-1:00为子时"""
    if 23 <= hour or hour < 1:
        return "子"
    elif 1 <= hour < 3:
        return "丑"
    elif 3 <= hour < 5:
        return "寅"
    elif 5 <= hour < 7:
        return "卯"
    elif 7 <= hour < 9:
        return "辰"
    elif 9 <= hour < 11:
        return "巳"
    elif 11 <= hour < 13:
        return "午"
    elif 13 <= hour < 15:
        return "未"
    elif 15 <= hour < 17:
        return "申"
    elif 17 <= hour < 19:
        return "酉"
    elif 19 <= hour < 21:
        return "戌"
    else:
        return "亥"


def get_hour_gan(day_gan: str, hour_zhi: str) -> str:
    """时干：日干 + 时支（详见五鼠遁）"""
    # 甲己还生甲，乙庚丙作初
    # 丙辛从戊起，丁壬庚子居
    # 戊癸何方发，壬子是真途
    start_gan = {
        "甲": 0, "丙": 2, "戊": 4, "庚": 6, "壬": 8,
        "乙": 0, "丁": 2, "己": 4, "辛": 6, "癸": 8,
    }
    zhi_order = {"子": 0, "丑": 1, "寅": 2, "卯": 3, "辰": 4, "巳": 5,
                 "午": 6, "未": 7, "申": 8, "酉": 9, "戌": 10, "亥": 11}
    idx = start_gan.get(day_gan, 0)
    return TIANGAN[(idx + zhi_order.get(hour_zhi, 0)) % 10]


def count_wuxing(bazi: Dict) -> Dict[str, int]:
    """统计五行数量"""
    counts = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    for col in ["year", "month", "day", "hour"]:
        gan = bazi[col]["gan"]
        zhi = bazi[col]["zhi"]
        counts[TG_WUXING[gan]] += 1
        counts[DZ_WUXING[zhi]] += 1
    
    return counts


def analyze_rizhu(rizhu_gan: str, month_zhi: str, wuxing_counts: Dict) -> Dict:
    """分析日主强弱"""
    rizhu_wuxing = TG_WUXING[rizhu_gan]
    
    # 简单判断：看日主五行在八字中的数量
    my_count = wuxing_counts.get(rizhu_wuxing, 0)
    
    # 月令判断
    yueling_wuxing = DZ_WUXING[month_zhi]
    
    if my_count >= 3:
        strength = "偏强"
        advice = f"日主{rizhu_wuxing}气偏强，可用官杀或财星"
    elif my_count <= 1:
        strength = "偏弱"
        advice = f"日主{rizhu_wuxing}气偏弱，喜印比生扶"
    else:
        strength = "中和"
        advice = f"日主{rizhu_wuxing}气中和，需看具体组合"
    
    return {"strength": strength, "advice": advice}


def get_dayun(rizhu_gan: str, year: int, gender: str = "男") -> List[str]:
    """计算大运"""
    # 简化：阳干顺排，阴干逆排
    yang_gan = ["甲", "丙", "戊", "庚", "壬"]
    direction = 1 if rizhu_gan in yang_gan else -1
    
    rizhu_idx = TIANGAN.index(rizhu_gan)
    start_gan_idx = (rizhu_idx + direction) % 10
    start_zhi_idx = (rizhu_idx + direction) % 12
    
    dayun = []
    for i in range(8):
        gan_idx = (start_gan_idx + i * direction) % 10
        zhi_idx = (start_zhi_idx + i * direction) % 12
        age = 5 + i * 10
        dayun.append(f"{age}岁：{TIANGAN[gan_idx]}{DIZHI[zhi_idx]}")
    
    return dayun


def format_output(bazi: Dict, wuxing_counts: Dict, rizhu_analysis: Dict, dayun: List) -> str:
    """格式化输出"""
    yz = bazi["year"]["zhi"]
    mxz = bazi["month"]["zhi"]
    sx = SHENGXIAO[DIZHI.index(yz)]
    mx = SHENGXIAO[DIZHI.index(mxz)]
    
    dzz = bazi["day"]["zhi"]
    hzz = bazi["hour"]["zhi"]
    dsx = SHENGXIAO[DIZHI.index(dzz)]
    hsx = SHENGXIAO[DIZHI.index(hzz)]
    
    output = f"""📊 八字排盘

【基本信息】
出生：{bazi['year']['year']}年 农历{bazi['month']['month']}月{bazi['day']['day']}日 {bazi['hour']['hour']}:00

【八字】
年柱：{bazi['year']['gan']}{bazi['year']['zhi']}（{sx}）  |  月柱：{bazi['month']['gan']}{bazi['month']['zhi']}（{mx}）
日柱：{bazi['day']['gan']}{bazi['day']['zhi']}（{dsx}）  |  时柱：{bazi['hour']['gan']}{bazi['hour']['zhi']}（{hsx}）

【五行分布】
金：{wuxing_counts['金']}  |  木：{wuxing_counts['木']}  |  水：{wuxing_counts['水']}  |  火：{wuxing_counts['火']}  |  土：{wuxing_counts['土']}

【日主】
{bazi['day']['gan']}，生于{bazi['month']['zhi']}月
日主{rizhu_analysis['strength']}，{rizhu_analysis['advice']}

【大运】
"""
    for dy in dayun:
        output += f"  {dy}\n"
    
    output += """
---
※ 八字仅供参考，命理需综合判断 ※"""
    
    return output


def cmd_bazi(year: int, month: int, day: int, hour: int):
    """排盘命令"""
    # 年柱
    year_gan = get_year_gan(year)
    year_zhi = get_year_zhi(year)
    
    # 月柱
    month_gan = get_month_gan(year_gan, month)
    month_zhi = get_month_zhi(month)
    
    # 日柱
    day_gan, day_zhi = get_day_gan_zhi(year, month, day)
    
    # 时柱
    hour_zhi = get_hour_zhi(hour)
    hour_gan = get_hour_gan(day_gan, hour_zhi)
    
    bazi = {
        "year": {"year": year, "gan": year_gan, "zhi": year_zhi},
        "month": {"month": month, "gan": month_gan, "zhi": month_zhi},
        "day": {"day": day, "gan": day_gan, "zhi": day_zhi},
        "hour": {"hour": hour, "gan": hour_gan, "zhi": hour_zhi},
    }
    
    # 五行统计
    wuxing_counts = count_wuxing(bazi)
    
    # 日主分析
    rizhu_analysis = analyze_rizhu(day_gan, month_zhi, wuxing_counts)
    
    # 大运
    dayun = get_dayun(day_gan, year)
    
    print(format_output(bazi, wuxing_counts, rizhu_analysis, dayun))


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法: python bazi.py <年份> <月份> <日期> <小时>")
        print("例: python bazi.py 1990 8 15 14")
        sys.exit(1)
    
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        hour = int(sys.argv[4])
        cmd_bazi(year, month, day, hour)
    except Exception as e:
        print(f"错误: {e}")
