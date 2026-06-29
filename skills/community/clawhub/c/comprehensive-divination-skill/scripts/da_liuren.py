#!/usr/bin/env python3
"""
大六壬天地盘 + 四课三传推算脚本
用法: python da_liuren.py -d 2026-05-29 -t 14
      或 python da_liuren.py --auto
输出: JSON 格式的天地盘、四课、三传结果
"""

import argparse
import json
import sys
import os
from datetime import datetime

# Ensure common.py is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    TIANGAN, DIZHI, DIZHI_WUXING as _DZ_WX,
    WUXING_KE as _WX_KE, TIANGAN_JIGONG,
    get_current_lunar_info, get_yuejiang_by_solar_term,
    get_day_ganzhi, solar_to_lunar_date, validate_hour,
)

# Fix Windows console encoding for Unicode output (GBK -> UTF-8)
try:
    if hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


# ============================================================
# 基础知识
# ============================================================

DIZHI_WUXING = _DZ_WX
WUXING_KE = _WX_KE

# 保留 get_shichen（天地盘构建需要）


def get_shichen(hour):
    """时辰→地支"""
    if hour == 0 or hour == 23:
        return '子'
    mapping = {
        1: '丑', 2: '丑', 3: '寅', 4: '寅', 5: '卯', 6: '卯',
        7: '辰', 8: '辰', 9: '巳', 10: '巳', 11: '午', 12: '午',
        13: '未', 14: '未', 15: '申', 16: '申', 17: '酉', 18: '酉',
        19: '戌', 20: '戌', 21: '亥', 22: '亥',
    }
    return mapping.get(hour, '子')


def build_tiandi_pan(yuejiang_dz, shichen_dz):
    """构建天地盘"""
    # 地盘：固定子丑寅卯...
    dipan = list(DIZHI)

    # 天盘：月将放在时辰位置，顺排
    yuejiang_idx = DIZHI.index(yuejiang_dz)
    shichen_idx = DIZHI.index(shichen_dz)

    tianpan = [''] * 12
    for i in range(12):
        tianpan[(shichen_idx + i) % 12] = DIZHI[(yuejiang_idx + i) % 12]

    # 组装成盘
    pan = []
    for i in range(12):
        pan.append({
            'position': i + 1,
            'dipan': dipan[i],
            'tianpan': tianpan[i],
        })

    return {
        'dipan': dipan,
        'tianpan': tianpan,
        'pan': pan,
        'yuejiang': yuejiang_dz,
        'shichen': shichen_dz,
    }


def get_tianpan_at(dipan_zhi, tianpan, dipan):
    """获取某地盘位置上的天盘"""
    idx = dipan.index(dipan_zhi)
    return tianpan[idx]


def build_sike(day_tg, day_dz, tianpan, dipan):
    """构建四课（使用天干寄宫映射）"""
    # 天干寄宫：甲→寅、乙→辰、丙→巳、丁→未、戊→巳、己→未、庚→申、辛→戌、壬→亥、癸→丑
    tg_jigong = TIANGAN_JIGONG.get(day_tg, day_dz)

    # 第一课：日干寄宫 + 其上方天盘
    ke1_up = get_tianpan_at(tg_jigong, tianpan, dipan)
    ke1_down = tg_jigong
    ke1 = {'ke': 1, 'up': ke1_up, 'down': ke1_down,
           'desc': f'日干{day_tg}寄{tg_jigong}宫，天盘{ke1_up}'}

    # 第二课：第一课天盘作地盘 + 其上方天盘
    ke2_down = ke1_up
    ke2_up = get_tianpan_at(ke2_down, tianpan, dipan)
    ke2 = {'ke': 2, 'up': ke2_up, 'down': ke2_down,
           'desc': f'以{ke1_up}为地盘，天盘{ke2_up}'}

    # 第三课：日支 + 日支上方天盘
    ke3_up = get_tianpan_at(day_dz, tianpan, dipan)
    ke3_down = day_dz
    ke3 = {'ke': 3, 'up': ke3_up, 'down': ke3_down,
           'desc': f'日支{day_dz}宫，天盘{ke3_up}'}

    # 第四课：第三课天盘作地盘 + 其上方天盘
    ke4_down = ke3_up
    ke4_up = get_tianpan_at(ke4_down, tianpan, dipan)
    ke4 = {'ke': 4, 'up': ke4_up, 'down': ke4_down,
           'desc': f'以{ke3_up}为地盘，天盘{ke4_up}'}

    return [ke1, ke2, ke3, ke4]


def fa_sanzhuan(sike, day_tg, tianpan, dipan):
    """发三传（实现贼克法 + 比用法）"""
    # 分析四课中的上下相克
    ke_relations = []
    for ke in sike:
        up_wx = DIZHI_WUXING.get(ke['up'], '?')
        down_wx = DIZHI_WUXING.get(ke['down'], '?')

        if WUXING_KE.get(up_wx) == down_wx:
            ke['relation'] = '上克下'
            ke_relations.append(ke)
        elif WUXING_KE.get(down_wx) == up_wx:
            ke['relation'] = '下克上'
            ke_relations.append(ke)
        else:
            ke['relation'] = '无克'

    if not ke_relations:
        # 无上下克，暂不实现遥克等，返回占位
        return {
            'method': '贼克法（无克，需进阶法则）',
            'chuzhuan': None, 'zhongzhuan': None, 'mozhuan': None,
            'note': '四课中无上下相克，建议使用 AI 推理层完成遥克/昂星等后续法则',
        }

    # 优先选下克上，若有则取最上一个
    xia_ke = [k for k in ke_relations if k['relation'] == '下克上']
    if xia_ke:
        chuzhuan_ke = xia_ke[0]  # 取第一个下克上
        method = '贼克法（下克上）'
    else:
        # 均为上克下
        if len(ke_relations) == 1:
            chuzhuan_ke = ke_relations[0]
            method = '贼克法（上克下）'
        else:
            # 多课上克下，需比用法
            day_yin_yang = '阳' if day_tg in '甲丙戊庚壬' else '阴'
            day_dz_yin_yang = {dz: ('阳' if dz in '子寅辰午申戌' else '阴') for dz in DIZHI}
            matching = [k for k in ke_relations if day_dz_yin_yang.get(k['up']) == day_yin_yang]
            if matching:
                chuzhuan_ke = matching[0]
                method = '比用法'
            else:
                chuzhuan_ke = ke_relations[0]
                method = '贼克法（上克下）'

    # 确定初传
    chuzhuan = chuzhuan_ke['up']

    # 中传：初传在地盘位置上的天盘
    zhongzhuan = get_tianpan_at(chuzhuan, tianpan, dipan)

    # 末传：中传在地盘位置上的天盘
    mozhuan = get_tianpan_at(zhongzhuan, tianpan, dipan)

    return {
        'method': method,
        'chuzhuan': chuzhuan,
        'zhongzhuan': zhongzhuan,
        'mozhuan': mozhuan,
        'chuzhuan_detail': chuzhuan_ke,
    }


def main():
    parser = argparse.ArgumentParser(description='大六壬天地盘 + 四课推算')
    parser.add_argument('-d', '--date', type=str, help='日期 (YYYY-MM-DD)')
    parser.add_argument('-t', '--hour', type=int, default=12, help='时辰 (0-23)')
    parser.add_argument('--auto', action='store_true', help='使用当前时间（精确农历+节气月将）')
    args = parser.parse_args()

    if args.auto:
        info = get_current_lunar_info()
        year, month, day = info['lunar_year'], info['lunar_month'], info['lunar_day']
        hour = info['hour']
        shichen_dz = info['shichen']
        yuejiang_dz = info['yuejiang_dz']
        yuejiang_name = info['yuejiang_name']
        day_tg, day_dz, day_gz = info['day_tg'], info['day_dz'], info['day_gz']
        year_tg, year_dz, year_gz = info['year_tg'], info['year_dz'], info['year_gz']
        gz = {
            'year_gz': year_gz, 'year_tg': year_tg, 'year_dz': year_dz,
            'day_gz': day_gz, 'day_tg': day_tg, 'day_dz': day_dz,
        }
        solar_date = info['solar_date']
    elif args.date:
        try:
            dt = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            parser.error(f'日期格式错误，应为 YYYY-MM-DD，当前值: {args.date}')
        year, month, day = dt.year, dt.month, dt.day
        hour = args.hour
        try:
            validate_hour(hour)
        except ValueError as e:
            parser.error(str(e))
        shichen_dz = get_shichen(hour)
        yuejiang_dz, yuejiang_name = get_yuejiang_by_solar_term(dt.date())
        day_tg, day_dz, day_gz = get_day_ganzhi(dt.date())
        # BUG-4 修复：公历日期需转农历年再取年干支（1-2月春节前农历年小1）
        from common import get_year_ganzhi
        lunar_info = solar_to_lunar_date(dt.year, dt.month, dt.day)
        year_tg, year_dz, year_gz = get_year_ganzhi(lunar_info['lunar_year'])
        gz = {
            'year_gz': year_gz, 'year_tg': year_tg, 'year_dz': year_dz,
            'day_gz': day_gz, 'day_tg': day_tg, 'day_dz': day_dz,
        }
        solar_date = args.date
    else:
        parser.print_help()
        sys.exit(1)

    # 构建天地盘
    tdpan = build_tiandi_pan(yuejiang_dz, shichen_dz)

    # 构建四课
    sike = build_sike(gz['day_tg'], gz['day_dz'], tdpan['tianpan'], tdpan['dipan'])

    # 发三传（传入天地盘用于中传末传推导）
    sanzhuan = fa_sanzhuan(sike, gz['day_tg'], tdpan['tianpan'], tdpan['dipan'])

    result = {
        'solar_date': solar_date,
        'lunar': f'{year}年{month}月{day}日',
        'hour': hour,
        'shichen': shichen_dz,
        'year_gz': gz['year_gz'],
        'day_gz': gz['day_gz'],
        'day_tg': gz['day_tg'],
        'day_dz': gz['day_dz'],
        'yuejiang': {'dz': yuejiang_dz, 'name': yuejiang_name},
        'tiandi_pan': tdpan,
        'sike': sike,
        'sanzhuan': sanzhuan,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
