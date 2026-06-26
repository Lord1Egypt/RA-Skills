#!/usr/bin/env python3
"""
八字命理分析脚本 - 可复用版本
用法:
  python bazi_analysis.py --year <年> --month <月> --day <日> --gender <男/女>
                          [--lunar] [--hour <时>] [--focus <分析重点>]

参数:
  --year, -y      出生年份 (必填)
  --month, -m     出生月份 (必填)
  --day, -d       出生日期 (必填)
  --gender, -g    性别: 男/女 (必填)
  --lunar         如果输入的是农历日期 (默认公历)
  --hour, -H      出生时辰 0-23 (可选, 默认12点午时)
  --focus, -f     分析重点: 综合/子女/婚姻/事业/财运 (默认综合)
"""

import argparse
import json
from lunar_python import Lunar, Solar, EightChar

# ============================================================
# 基础数据
# ============================================================

WU_XING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

YIN_YANG = {
    '甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳',
    '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴'
}

KE_MAP = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
BEI_KE_MAP = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
SHENG_MAP = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
BEI_SHENG_MAP = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}

LIU_HE = {
    '子': '丑', '丑': '子', '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯', '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳', '午': '未', '未': '午'
}

SAN_HE = {
    '申': ['子', '辰'], '子': ['申', '辰'], '辰': ['申', '子'],
    '寅': ['午', '戌'], '午': ['寅', '戌'], '戌': ['寅', '午'],
    '巳': ['酉', '丑'], '酉': ['巳', '丑'], '丑': ['巳', '酉'],
    '亥': ['卯', '未'], '卯': ['亥', '未'], '未': ['亥', '卯']
}

CHONG = {
    '子': '午', '午': '子', '丑': '未', '未': '丑',
    '寅': '申', '申': '寅', '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰', '巳': '亥', '亥': '巳'
}

SHI_SHEN_MEANING = {
    '比肩': '同辈、兄弟、竞争、合作',
    '劫财': '破耗、争夺、冲动、姐妹',
    '食神': '才华、享受、口福、晚辈',
    '伤官': '创意、叛逆、表达、晚辈',
    '偏财': '意外之财、投机、父亲',
    '正财': '稳定收入、务实、妻子(男)',
    '七杀': '压力、竞争、魄力、儿子(男)',
    '正官': '权力、地位、约束、女儿(男)/丈夫(女)',
    '偏印': '偏门学识、灵感、继母',
    '正印': '学识、保护、贵人、母亲',
}

# ============================================================
# 核心函数
# ============================================================

def get_solar_date(year, month, day, is_lunar=False):
    """获取公历日期"""
    if is_lunar:
        lunar = Lunar.fromYmd(year, month, day)
        solar = lunar.getSolar()
        return lunar, solar
    else:
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        return lunar, solar


def get_bazi_info(lunar, hour=12):
    """获取八字信息"""
    solar_noon = Solar.fromYmdHms(
        lunar.getSolar().getYear(),
        lunar.getSolar().getMonth(),
        lunar.getSolar().getDay(),
        hour, 0, 0
    )
    lunar_noon = solar_noon.getLunar()
    bazi = lunar_noon.getEightChar()
    
    return {
        'year_gz': bazi.getYear(),
        'month_gz': bazi.getMonth(),
        'day_gz': bazi.getDay(),
        'time_gz': bazi.getTime(),
        'year_nayin': bazi.getYearNaYin(),
        'month_nayin': bazi.getMonthNaYin(),
        'day_nayin': bazi.getDayNaYin(),
        'time_nayin': bazi.getTimeNaYin(),
        'day_gan': bazi.getDayGan(),
        'day_zhi': bazi.getDayZhi(),
        'year_gan': bazi.getYearGan(),
        'year_zhi': bazi.getYearZhi(),
        'month_gan': bazi.getMonthGan(),
        'month_zhi': bazi.getMonthZhi(),
        'time_gan': bazi.getTimeGan(),
        'time_zhi': bazi.getTimeZhi(),
        'year_shishen': bazi.getYearShiShenGan(),
        'month_shishen': bazi.getMonthShiShenGan(),
        'time_shishen': bazi.getTimeShiShenGan(),
    }


def get_dayun(bazi, gender):
    """获取大运信息"""
    yun = bazi.getYun(1 if gender == '男' else 0)
    da_yun = yun.getDaYun()
    
    result = {
        'start_year': yun.getStartYear(),
        'start_month': yun.getStartMonth(),
        'start_date': yun.getStartSolar().toYmd(),
        'da_yun': []
    }
    
    for i in range(1, min(9, len(da_yun))):
        dy = da_yun[i]
        result['da_yun'].append({
            'index': i,
            'gan_zhi': dy.getGanZhi(),
            'start_year': dy.getStartYear(),
            'end_year': dy.getEndYear(),
        })
    
    return result


def get_child_stars(day_gan, gender):
    """根据日主和性别获取子女星"""
    wx = WU_XING[day_gan]
    yy = YIN_YANG[day_gan]
    
    if gender == '男':
        # 男命: 克我者为子女星 (官杀)
        bei_ke_wx = BEI_KE_MAP[wx]
        stars = []
        for gan, w in WU_XING.items():
            if w == bei_ke_wx:
                if YIN_YANG[gan] != yy:
                    stars.append({'name': '正官', 'gan': gan, 'child': '女儿'})
                else:
                    stars.append({'name': '七杀', 'gan': gan, 'child': '儿子'})
        return stars
    else:
        # 女命: 我生者为子女星 (食伤)
        sheng_wx = SHENG_MAP[wx]
        stars = []
        for gan, w in WU_XING.items():
            if w == sheng_wx:
                if YIN_YANG[gan] == yy:
                    stars.append({'name': '食神', 'gan': gan, 'child': '女儿'})
                else:
                    stars.append({'name': '伤官', 'gan': gan, 'child': '儿子'})
        return stars


def get_marriage_stars(day_gan, gender):
    """根据日主和性别获取婚姻星"""
    wx = WU_XING[day_gan]
    yy = YIN_YANG[day_gan]
    
    if gender == '男':
        # 男命: 我克者为妻星 (财星)
        ke_wx = KE_MAP[wx]
        stars = []
        for gan, w in WU_XING.items():
            if w == ke_wx:
                if YIN_YANG[gan] != yy:
                    stars.append({'name': '正财', 'gan': gan, 'meaning': '正妻'})
                else:
                    stars.append({'name': '偏财', 'gan': gan, 'meaning': '偏缘/情人'})
        return stars
    else:
        # 女命: 克我者为夫星 (官杀)
        bei_ke_wx = BEI_KE_MAP[wx]
        stars = []
        for gan, w in WU_XING.items():
            if w == bei_ke_wx:
                if YIN_YANG[gan] != yy:
                    stars.append({'name': '正官', 'gan': gan, 'meaning': '正夫'})
                else:
                    stars.append({'name': '七杀', 'gan': gan, 'meaning': '偏缘/情人'})
        return stars


def get_career_stars(day_gan):
    """根据日主获取事业相关星"""
    wx = WU_XING[day_gan]
    yy = YIN_YANG[day_gan]
    
    stars = []
    # 官杀代表事业、权力
    bei_ke_wx = BEI_KE_MAP[wx]
    for gan, w in WU_XING.items():
        if w == bei_ke_wx:
            if YIN_YANG[gan] != yy:
                stars.append({'name': '正官', 'gan': gan, 'meaning': '正职、管理'})
            else:
                stars.append({'name': '七杀', 'gan': gan, 'meaning': '创业、竞争'})
    
    # 印星代表学识、贵人
    bei_sheng_wx = BEI_SHENG_MAP[wx]
    for gan, w in WU_XING.items():
        if w == bei_sheng_wx:
            if YIN_YANG[gan] != yy:
                stars.append({'name': '正印', 'gan': gan, 'meaning': '正途学识、贵人'})
            else:
                stars.append({'name': '偏印', 'gan': gan, 'meaning': '偏门学识、灵感'})
    
    return stars


def get_wealth_stars(day_gan):
    """根据日主获取财运相关星"""
    wx = WU_XING[day_gan]
    yy = YIN_YANG[day_gan]
    
    # 我克者为财
    ke_wx = KE_MAP[wx]
    stars = []
    for gan, w in WU_XING.items():
        if w == ke_wx:
            if YIN_YANG[gan] != yy:
                stars.append({'name': '正财', 'gan': gan, 'meaning': '正职收入、稳定'})
            else:
                stars.append({'name': '偏财', 'gan': gan, 'meaning': '意外之财、投资'})
    
    return stars


def analyze_liunian(bazi_info, child_stars, marriage_stars, career_stars, wealth_stars, 
                    focus='综合', start_year=2025, end_year=2030):
    """分析流年运势"""
    results = []
    day_zhi = bazi_info['day_zhi']
    
    for year in range(start_year, end_year + 1):
        lunar_year = Lunar.fromYmd(year, 1, 1)
        year_gz = lunar_year.getYearInGanZhi()
        year_gan = lunar_year.getYearGan()
        year_zhi = lunar_year.getYearZhi()
        shengxiao = lunar_year.getYearShengXiao()
        
        year_info = {
            'year': year,
            'gan_zhi': year_gz,
            'shengxiao': shengxiao,
            'events': []
        }
        
        # 检查子女星
        if focus in ['综合', '子女']:
            for star in child_stars:
                if star['gan'] == year_gan:
                    year_info['events'].append(
                        f"⭐ 子女星出现: {star['name']}({star['child']})"
                    )
        
        # 检查婚姻星
        if focus in ['综合', '婚姻']:
            for star in marriage_stars:
                if star['gan'] == year_gan:
                    year_info['events'].append(
                        f"💕 婚姻星出现: {star['name']}({star['meaning']})"
                    )
        
        # 检查事业星
        if focus in ['综合', '事业']:
            for star in career_stars:
                if star['gan'] == year_gan:
                    year_info['events'].append(
                        f"💼 事业星出现: {star['name']}({star['meaning']})"
                    )
        
        # 检查财运星
        if focus in ['综合', '财运']:
            for star in wealth_stars:
                if star['gan'] == year_gan:
                    year_info['events'].append(
                        f"💰 财运星出现: {star['name']}({star['meaning']})"
                    )
        
        # 检查地支关系
        if LIU_HE.get(year_zhi) == day_zhi:
            year_info['events'].append("🤝 流年地支与日支六合(吉)")
        
        if day_zhi in SAN_HE.get(year_zhi, []):
            year_info['events'].append("🔗 流年地支与日支三合(吉)")
        
        if CHONG.get(year_zhi) == day_zhi:
            year_info['events'].append("⚡ 流年地支与日支冲(动)")
        
        results.append(year_info)
    
    return results


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='八字命理分析')
    parser.add_argument('--year', '-y', type=int, required=True, help='出生年份')
    parser.add_argument('--month', '-m', type=int, required=True, help='出生月份')
    parser.add_argument('--day', '-d', type=int, required=True, help='出生日期')
    parser.add_argument('--gender', '-g', choices=['男', '女'], required=True, help='性别')
    parser.add_argument('--lunar', action='store_true', help='如果输入的是农历日期')
    parser.add_argument('--hour', '-H', type=int, default=12, help='出生时辰 0-23 (默认12点午时)')
    parser.add_argument('--focus', '-f', choices=['综合', '子女', '婚姻', '事业', '财运'],
                        default='综合', help='分析重点')
    
    args = parser.parse_args()
    
    # 1. 获取日期
    lunar, solar = get_solar_date(args.year, args.month, args.day, args.lunar)
    
    print("=" * 60)
    print(f"八字排盘 ({args.gender}命)")
    print("=" * 60)
    
    if args.lunar:
        print(f"农历: {args.year}年{args.month}月{args.day}日")
    else:
        print(f"公历: {args.year}年{args.month}月{args.day}日")
    print(f"公历: {solar.getYear()}年{solar.getMonth()}月{solar.getDay()}日")
    print(f"生肖: {lunar.getYearShengXiao()}")
    
    # 2. 八字信息
    bazi_info = get_bazi_info(lunar, args.hour)
    
    print(f"\n【四柱】")
    print(f"  年柱: {bazi_info['year_gz']} ({bazi_info['year_nayin']})")
    print(f"  月柱: {bazi_info['month_gz']} ({bazi_info['month_nayin']})")
    print(f"  日柱: {bazi_info['day_gz']} ({bazi_info['day_nayin']})")
    if args.hour != 12:
        print(f"  时柱: {bazi_info['time_gz']} ({bazi_info['time_nayin']})")
    else:
        print(f"  时柱: {bazi_info['time_gz']} ({bazi_info['time_nayin']}) [按午时计算]")
    
    day_gan = bazi_info['day_gan']
    day_wx = WU_XING[day_gan]
    day_yy = YIN_YANG[day_gan]
    print(f"\n【日主】: {day_gan} ({day_wx}命, {day_yy})")
    
    print(f"\n【十神】")
    print(f"  年干: {bazi_info['year_shishen']} — {SHI_SHEN_MEANING.get(bazi_info['year_shishen'], '')}")
    print(f"  月干: {bazi_info['month_shishen']} — {SHI_SHEN_MEANING.get(bazi_info['month_shishen'], '')}")
    print(f"  时干: {bazi_info['time_shishen']} — {SHI_SHEN_MEANING.get(bazi_info['time_shishen'], '')}")
    
    # 3. 大运
    bazi = lunar.getEightChar()
    dayun = get_dayun(bazi, args.gender)
    
    print(f"\n【大运】")
    print(f"  起运: {dayun['start_year']}年{dayun['start_month']}个月 ({dayun['start_date']})")
    for dy in dayun['da_yun']:
        print(f"  第{dy['index']}步: {dy['gan_zhi']} ({dy['start_year']}-{dy['end_year']}岁)")
    
    # 4. 专项分析
    child_stars = get_child_stars(bazi_info['day_gan'], args.gender)
    marriage_stars = get_marriage_stars(bazi_info['day_gan'], args.gender)
    career_stars = get_career_stars(bazi_info['day_gan'])
    wealth_stars = get_wealth_stars(bazi_info['day_gan'])
    
    print(f"\n【{args.focus}分析】")
    
    if args.focus in ['综合', '子女']:
        print(f"\n  子女星:")
        for star in child_stars:
            print(f"    {star['name']}({star['gan']}) → {star['child']}")
    
    if args.focus in ['综合', '婚姻']:
        print(f"\n  婚姻星:")
        for star in marriage_stars:
            print(f"    {star['name']}({star['gan']}) → {star['meaning']}")
    
    if args.focus in ['综合', '事业']:
        print(f"\n  事业星:")
        for star in career_stars:
            print(f"    {star['name']}({star['gan']}) → {star['meaning']}")
    
    if args.focus in ['综合', '财运']:
        print(f"\n  财运星:")
        for star in wealth_stars:
            print(f"    {star['name']}({star['gan']}) → {star['meaning']}")
    
    # 5. 流年分析
    liunian = analyze_liunian(
        bazi_info, child_stars, marriage_stars, career_stars, wealth_stars,
        args.focus, 2026, 2030
    )
    
    print(f"\n【流年运势 (2026-2030)】")
    for yn in liunian:
        print(f"\n  --- {yn['year']}年 {yn['gan_zhi']}年 ({yn['shengxiao']}年) ---")
        if yn['events']:
            for event in yn['events']:
                print(f"    {event}")
        else:
            print(f"    (无明显特殊关系)")
    
    # 6. 提醒
    print(f"\n{'=' * 60}")
    print("⚠️ 重要提示:")
    print("  1. 缺少出生时辰时，时柱(子女宫)无法准确推算")
    print("  2. 八字属于传统文化，结果仅供娱乐参考")
    print("  3. 科学态度和实际行动才是最重要的")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
