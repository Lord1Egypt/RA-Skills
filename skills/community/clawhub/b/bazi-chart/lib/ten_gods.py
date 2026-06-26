"""
十神计算模块
以日干为"我"，推算其他天干的十神关系
"""

from .constants import GAN_WUXING, GAN_YINYANG, WUXING_SHENG, WUXING_KE


def get_ten_god(day_stem, other_stem):
    """
    计算 other_stem 相对于 day_stem 的十神
    
    十神规则：
    - 同我：比肩（同阴阳）/ 劫财（异阴阳）
    - 生我：偏印（同阴阳）/ 正印（异阴阳）
    - 我生：食神（同阴阳）/ 伤官（异阴阳）
    - 克我：偏官/七杀（同阴阳）/ 正官（异阴阳）
    - 我克：偏财（同阴阳）/ 正财（异阴阳）
    
    Args:
        day_stem: 日干
        other_stem: 另一个天干
    
    Returns:
        十神名称字符串
    """
    if day_stem == other_stem:
        return "比肩"
    
    me_wx = GAN_WUXING[day_stem]
    other_wx = GAN_WUXING[other_stem]
    same_polarity = (GAN_YINYANG[day_stem] == GAN_YINYANG[other_stem])
    
    # 判断五行关系
    if me_wx == other_wx:
        # 同五行
        return "比肩" if same_polarity else "劫财"
    elif WUXING_SHENG[other_wx] == me_wx:
        # 他生我（other 的五行生 me 的五行）
        return "偏印" if same_polarity else "正印"
    elif WUXING_SHENG[me_wx] == other_wx:
        # 我生他
        return "食神" if same_polarity else "伤官"
    elif WUXING_KE[other_wx] == me_wx:
        # 他克我
        return "偏官" if same_polarity else "正官"
    elif WUXING_KE[me_wx] == other_wx:
        # 我克他
        return "偏财" if same_polarity else "正财"
    
    return "未知"


def get_all_ten_gods(day_stem, year_stem, month_stem, hour_stem):
    """
    计算四柱天干的十神关系
    
    Returns:
        dict: {position: {"stem": stem, "god": god_name}}
    """
    result = {}
    
    if year_stem:
        result["year_stem"] = {
            "stem": year_stem,
            "god": get_ten_god(day_stem, year_stem)
        }
    
    if month_stem:
        result["month_stem"] = {
            "stem": month_stem,
            "god": get_ten_god(day_stem, month_stem)
        }
    
    if hour_stem:
        result["hour_stem"] = {
            "stem": hour_stem,
            "god": get_ten_god(day_stem, hour_stem)
        }
    
    return result
