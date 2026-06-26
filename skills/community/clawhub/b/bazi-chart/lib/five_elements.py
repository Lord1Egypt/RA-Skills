"""
五行力量分析模块
统计命盘中五行的力量分布
"""

from .constants import GAN_WUXING, WUXING_EN, WUXING_SHENG
from .hidden_stems import get_hidden_stems_with_weight


def analyze_five_elements(pillars):
    """
    分析五行力量分布
    
    天干：每个天干计1分
    地支藏干：按权重计分（本气0.6，中气0.3，余气0.1）
    
    Args:
        pillars: dict with year/month/day/hour, each having stem and branch
    
    Returns:
        dict: {element: {"score": float, "percent": str}}
    """
    scores = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}
    
    # 四柱天干计分
    for pos in ["year", "month", "day", "hour"]:
        stem = pillars[pos]["stem"]
        wx = GAN_WUXING[stem]
        scores[wx] += 1.0
    
    # 四柱地支藏干计分
    for pos in ["year", "month", "day", "hour"]:
        branch = pillars[pos]["branch"]
        for stem, weight in get_hidden_stems_with_weight(branch):
            wx = GAN_WUXING[stem]
            scores[wx] += weight
    
    # 计算百分比
    total = sum(scores.values())
    result = {}
    for wx in ["木", "火", "土", "金", "水"]:
        en = WUXING_EN[wx]
        score = round(scores[wx], 1)
        pct = round(scores[wx] / total * 100) if total > 0 else 0
        result[en] = {
            "score": score,
            "percent": f"{pct}%",
            "chinese": wx,
        }
    
    return result


def judge_day_master_strength(day_stem, month_branch, pillars):
    """
    简易判断日主强弱
    考量：得令、得地、得生、得助
    
    Args:
        day_stem: 日干
        month_branch: 月支
        pillars: 四柱数据
    
    Returns:
        str: "偏强" 或 "偏弱"
    """
    me_wx = GAN_WUXING[day_stem]
    support_count = 0
    total_checks = 4
    
    # 1. 得令：月支本气五行 生我 或 同我
    from .hidden_stems import get_hidden_stems
    month_hidden = get_hidden_stems(month_branch)
    if month_hidden:
        main_qi_wx = GAN_WUXING[month_hidden[0]]
        if main_qi_wx == me_wx or WUXING_SHENG[main_qi_wx] == me_wx:
            support_count += 1
    
    # 2. 得地：日支藏干有 同我五行 的
    day_branch = pillars["day"]["branch"]
    day_hidden = get_hidden_stems(day_branch)
    for s in day_hidden:
        if GAN_WUXING[s] == me_wx:
            support_count += 1
            break
    
    # 3. 得生：其他天干中有 生我五行 的
    sheng_me_wx = None
    for wx, target in WUXING_SHENG.items():
        if target == me_wx:
            sheng_me_wx = wx
            break
    
    for pos in ["year", "month", "hour"]:
        stem = pillars[pos]["stem"]
        if GAN_WUXING[stem] == sheng_me_wx:
            support_count += 1
            break
    
    # 4. 得助：其他天干中有 同我五行 的
    for pos in ["year", "month", "hour"]:
        stem = pillars[pos]["stem"]
        if GAN_WUXING[stem] == me_wx:
            support_count += 1
            break
    
    return "偏强" if support_count >= 2 else "偏弱"
