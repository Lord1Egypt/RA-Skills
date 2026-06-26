"""
大运计算模块
根据性别、年干阴阳决定顺逆排，计算起运年龄和每步大运
"""

from .constants import TIAN_GAN, DI_ZHI, GAN_YINYANG
from .solar_terms import find_adjacent_jie


def calculate_major_luck(birth_dt_cst, gender, year_gan, month_gan, month_zhi, birth_year, num_periods=8):
    """
    计算大运
    
    规则：
    - 阳年男命 / 阴年女命 → 顺排
    - 阴年男命 / 阳年女命 → 逆排
    - 起运年龄：出生日到最近节气的天数 / 3 = 年数（精确到月）
    - 每步大运10年
    
    Args:
        birth_dt_cst: 出生时间 (CST)
        gender: "male" 或 "female"
        year_gan: 年干
        month_gan: 月干
        month_zhi: 月支
        birth_year: 出生年份
        num_periods: 大运步数（默认8）
    
    Returns:
        dict: {"start_age": int, "periods": [{"age": str, "years": str, "stem": str, "branch": str}]}
    """
    is_yang_year = GAN_YINYANG[year_gan]  # True=阳, False=阴
    is_male = (gender == "male")
    
    # 顺排条件：阳年男命 或 阴年女命
    is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
    
    # 计算起运年龄
    if is_forward:
        # 顺排：从出生到下一个节
        adj_jie = find_adjacent_jie(birth_dt_cst, direction="next")
    else:
        # 逆排：从出生到上一个节
        adj_jie = find_adjacent_jie(birth_dt_cst, direction="prev")
    
    if adj_jie is None:
        # fallback
        start_age = 5
    else:
        _, jie_moment = adj_jie
        diff = abs((jie_moment - birth_dt_cst).total_seconds())
        diff_days = diff / 86400.0
        # 3天 = 1年，精确到月
        start_age_years = diff_days / 3.0
        # 四舍五入到整数年
        start_age = max(1, round(start_age_years))
    
    # 计算大运干支序列
    month_gan_idx = TIAN_GAN.index(month_gan)
    month_zhi_idx = DI_ZHI.index(month_zhi)
    
    periods = []
    for i in range(num_periods):
        step = i + 1
        if is_forward:
            gan_idx = (month_gan_idx + step) % 10
            zhi_idx = (month_zhi_idx + step) % 12
        else:
            gan_idx = (month_gan_idx - step) % 10
            zhi_idx = (month_zhi_idx - step) % 12
        
        age_start = start_age + i * 10
        age_end = age_start + 9
        year_start = birth_year + age_start
        year_end = birth_year + age_end
        
        periods.append({
            "age": f"{age_start}-{age_end}",
            "years": f"{year_start}-{year_end}",
            "stem": TIAN_GAN[gan_idx],
            "branch": DI_ZHI[zhi_idx],
        })
    
    return {
        "start_age": start_age,
        "direction": "顺排" if is_forward else "逆排",
        "periods": periods,
    }
