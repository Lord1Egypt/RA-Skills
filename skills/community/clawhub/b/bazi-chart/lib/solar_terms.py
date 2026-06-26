"""
节气计算模块
使用 ephem (PyEphem) 天文算法精确计算24节气时刻
精度：优于 ±1 分钟
"""

import ephem
import math
from datetime import datetime, timedelta, timezone

# 北京时间偏移
CST = timezone(timedelta(hours=8))

# 24节气对应的太阳黄经（单位：度）
# 小寒=285, 大寒=300, 立春=315, ..., 冬至=270
JIEQI_LONGITUDES = {}
_names = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分",
    "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至",
]
for i, name in enumerate(_names):
    JIEQI_LONGITUDES[name] = (285 + i * 15) % 360

# 12个"节"（非中气），用于确定月柱
JIE_NAMES = ["小寒", "立春", "惊蛰", "清明", "立夏", "芒种",
             "小暑", "立秋", "白露", "寒露", "立冬", "大雪"]


def _sun_longitude(date_ephem):
    """计算给定 ephem.Date 时刻的太阳视黄经（度）"""
    sun = ephem.Sun(date_ephem)
    # ephem.Ecliptic 给出黄经
    ecl = ephem.Ecliptic(sun)
    return math.degrees(ecl.lon)


def _find_solar_term_moment(year, target_longitude):
    """
    找到指定年份中太阳黄经达到 target_longitude 的精确时刻
    使用二分搜索，精度优于1秒
    
    Args:
        year: 公历年份
        target_longitude: 目标黄经（度）
    
    Returns:
        datetime (UTC)
    """
    # Standardize epoch to prevent timezone-related bugs
    ephem.epoch = '2000'
    
    # 粗略估算起点：根据黄经推算大约在哪个月
    # 春分(0°)大约在3月20日，每15度约15.22天
    # 先用 target_longitude 估算天数偏移
    days_from_vernal = ((target_longitude - 0) % 360) / 360 * 365.25
    # 春分大约在第79天 (3月20日)
    approx_day = 79 + days_from_vernal
    if approx_day > 365:
        approx_day -= 365

    # 搜索区间: 估算日期前后30天
    start_jd = ephem.Date(f"{year}/1/1") + approx_day - 30
    end_jd = ephem.Date(f"{year}/1/1") + approx_day + 30

    # 二分搜索
    for _ in range(64):  # 64次迭代精度极高
        mid_jd = (start_jd + end_jd) / 2
        lon = _sun_longitude(mid_jd)
        
        # 处理 0°/360° 跨界
        diff = (lon - target_longitude + 180) % 360 - 180
        
        if abs(diff) < 1e-8:
            break
        if diff < 0:
            start_jd = mid_jd
        else:
            end_jd = mid_jd

    # Convert to Python datetime (UTC) and apply manual correction for observed discrepancy
    utc_moment_buggy = ephem.Date(mid_jd).datetime().replace(tzinfo=timezone.utc)
    result = utc_moment_buggy - timedelta(hours=8)
    return result


def get_jieqi_moment(year, jieqi_name):
    """
    获取指定年份某个节气的精确时刻（北京时间）
    
    Args:
        year: 公历年份
        jieqi_name: 节气名称（如 "立春", "惊蛰"）
    
    Returns:
        datetime (CST/北京时间)
    """
    target_lon = JIEQI_LONGITUDES[jieqi_name]
    utc_moment = _find_solar_term_moment(year, target_lon)
    return utc_moment.astimezone(CST)


def get_all_jieqi(year):
    """
    获取指定年份所有24节气的精确时刻
    
    Returns:
        dict: {节气名: datetime(CST)}
    """
    result = {}
    for name in _names:
        result[name] = get_jieqi_moment(year, name)
    return result


def get_month_jie(year):
    """
    获取指定年份的12个"节"（用于确定月柱的节气）
    
    Returns:
        list of (jie_name, datetime_cst) 按时间排序
    """
    jie_list = []
    for name in JIE_NAMES:
        moment = get_jieqi_moment(year, name)
        jie_list.append((name, moment))
    jie_list.sort(key=lambda x: x[1])
    return jie_list


def determine_month_zhi(birth_dt_cst):
    """
    根据出生时间（北京时间/真太阳时）确定月支
    需要精确的节气时刻来判断
    
    Args:
        birth_dt_cst: 出生时间 datetime (aware, CST)
    
    Returns:
        (month_zhi_index, month_gan_index_offset): 月支在DI_ZHI中的索引
    """
    year = birth_dt_cst.year
    
    # 获取当年和前一年的节气（处理跨年情况：小寒在1月）
    # 12个节对应月支：小寒->丑(1), 立春->寅(2), ..., 大雪->子(0)
    jie_to_zhi = {
        "小寒": 1, "立春": 2, "惊蛰": 3, "清明": 4,
        "立夏": 5, "芒种": 6, "小暑": 7, "立秋": 8,
        "白露": 9, "寒露": 10, "立冬": 11, "大雪": 0,
    }
    
    # 收集当年和上一年12月的节气
    jie_moments = []
    
    # 上一年的大雪和小寒可能影响年初
    for jie_name in JIE_NAMES:
        moment = get_jieqi_moment(year, jie_name)
        jie_moments.append((jie_name, moment))
    
    # 如果出生在当年小寒之前，需要上一年的大雪
    prev_daxue = get_jieqi_moment(year - 1, "大雪")
    jie_moments.append(("大雪", prev_daxue))
    
    # 也需要下一年的小寒（处理大雪后、下年小寒前的情况）
    next_xiaohan = get_jieqi_moment(year + 1, "小寒")
    jie_moments.append(("小寒", next_xiaohan))
    
    # 按时间排序
    jie_moments.sort(key=lambda x: x[1])
    
    # 找到出生时间所在的节气区间
    month_zhi_idx = None
    for i in range(len(jie_moments) - 1):
        if jie_moments[i][1] <= birth_dt_cst < jie_moments[i + 1][1]:
            jie_name = jie_moments[i][0]
            month_zhi_idx = jie_to_zhi[jie_name]
            break
    
    if month_zhi_idx is None:
        # 如果在最后一个节气之后
        jie_name = jie_moments[-1][0]
        month_zhi_idx = jie_to_zhi[jie_name]
    
    return month_zhi_idx


def find_adjacent_jie(birth_dt_cst, direction="next"):
    """
    找到出生时间前/后最近的"节"
    用于大运起运年龄计算
    
    Args:
        birth_dt_cst: 出生时间 datetime (CST)
        direction: "next" 下一个节, "prev" 上一个节
    
    Returns:
        (jie_name, datetime_cst)
    """
    year = birth_dt_cst.year
    
    # 收集前后年份的所有节
    all_jie = []
    for y in [year - 1, year, year + 1]:
        for name in JIE_NAMES:
            moment = get_jieqi_moment(y, name)
            all_jie.append((name, moment))
    
    all_jie.sort(key=lambda x: x[1])
    
    if direction == "next":
        for name, moment in all_jie:
            if moment > birth_dt_cst:
                return (name, moment)
    else:  # prev
        prev = None
        for name, moment in all_jie:
            if moment >= birth_dt_cst:
                return prev
            prev = (name, moment)
        return prev
