#!/usr/bin/env python3
"""
梅花易数起卦脚本
用法: python meihua_qigua.py -n <数1> <数2> [<数3>]  # 报数起卦
      或 python meihua_qigua.py -d 2026-05-29 -t 14    # 时间起卦
      或 python meihua_qigua.py --auto                  # 自动使用当前时间
输出: JSON 格式的起卦结果
"""

import argparse
import json
import sys
import os

# Ensure common.py is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import get_current_lunar_info, solar_to_lunar_date, DIZHI, WUXING_SHENG, WUXING_KE, validate_hour
from datetime import datetime

# Fix Windows console encoding for Unicode trigram symbols (GBK -> UTF-8)
try:
    if hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


# 先天八卦
BAGUA = {
    1: {'name': '乾', 'symbol': '☰', 'wuxing': '金', 'nature': '天'},
    2: {'name': '兑', 'symbol': '☱', 'wuxing': '金', 'nature': '泽'},
    3: {'name': '离', 'symbol': '☲', 'wuxing': '火', 'nature': '火'},
    4: {'name': '震', 'symbol': '☳', 'wuxing': '木', 'nature': '雷'},
    5: {'name': '巽', 'symbol': '☴', 'wuxing': '木', 'nature': '风'},
    6: {'name': '坎', 'symbol': '☵', 'wuxing': '水', 'nature': '水'},
    7: {'name': '艮', 'symbol': '☶', 'wuxing': '土', 'nature': '山'},
    8: {'name': '坤', 'symbol': '☷', 'wuxing': '土', 'nature': '地'},
}

# DIZHI/WUXING_SHENG/WUXING_KE 已从 common.py 导入

# 六十四卦查找表 (up_num, down_num) → 卦名
GUA_NAMES = {
    (1, 1): '乾为天', (1, 2): '天泽履', (1, 3): '天火同人', (1, 4): '天雷无妄',
    (1, 5): '天风姤', (1, 6): '天水讼', (1, 7): '天山遁', (1, 8): '天地否',
    (2, 1): '泽天夬', (2, 2): '兑为泽', (2, 3): '泽火革', (2, 4): '泽雷随',
    (2, 5): '泽风大过', (2, 6): '泽水困', (2, 7): '泽山咸', (2, 8): '泽地萃',
    (3, 1): '火天大有', (3, 2): '火泽睽', (3, 3): '离为火', (3, 4): '火雷噬嗑',
    (3, 5): '火风鼎', (3, 6): '火水未济', (3, 7): '火山旅', (3, 8): '火地晋',
    (4, 1): '雷天大壮', (4, 2): '雷泽归妹', (4, 3): '雷火丰', (4, 4): '震为雷',
    (4, 5): '雷风恒', (4, 6): '雷水解', (4, 7): '雷山小过', (4, 8): '雷地豫',
    (5, 1): '风天小畜', (5, 2): '风泽中孚', (5, 3): '风火家人', (5, 4): '风雷益',
    (5, 5): '巽为风', (5, 6): '风水涣', (5, 7): '风山渐', (5, 8): '风地观',
    (6, 1): '水天需', (6, 2): '水泽节', (6, 3): '水火既济', (6, 4): '水雷屯',
    (6, 5): '水风井', (6, 6): '坎为水', (6, 7): '水山蹇', (6, 8): '水地比',
    (7, 1): '山天大畜', (7, 2): '山泽损', (7, 3): '山火贲', (7, 4): '山雷颐',
    (7, 5): '山风蛊', (7, 6): '山水蒙', (7, 7): '艮为山', (7, 8): '山地剥',
    (8, 1): '地天泰', (8, 2): '地泽临', (8, 3): '地火明夷', (8, 4): '地雷复',
    (8, 5): '地风升', (8, 6): '地水师', (8, 7): '地山谦', (8, 8): '坤为地',
}


def num_to_gua(num):
    """数字→卦(1-8)"""
    n = num % 8
    if n == 0:
        n = 8
    return BAGUA[n]


def yao_to_num(num):
    """取动爻(1-6)"""
    n = num % 6
    if n == 0:
        n = 6
    return n


def by_numbers(n1, n2, n3=None):
    """报数起卦法"""
    up_gua_num = n1 % 8
    if up_gua_num == 0:
        up_gua_num = 8
    down_gua_num = n2 % 8
    if down_gua_num == 0:
        down_gua_num = 8

    if n3 is not None:
        dong_yao = yao_to_num(n3)
    else:
        dong_yao = yao_to_num(n1 + n2)

    up_gua = BAGUA[up_gua_num]
    down_gua = BAGUA[down_gua_num]

    return build_result(up_gua_num, down_gua_num, dong_yao, f'报数起卦：{n1},{n2},{n3 or "自动"}',
                        {'n1': n1, 'n2': n2, 'n3': n3})


def by_time(year_dz, month, day, hour):
    """时间起卦法"""
    # 年支序数 (子=1)
    year_idx = DIZHI.index(year_dz) + 1 if year_dz in DIZHI else 1

    up_num = (year_idx + month) % 8
    if up_num == 0:
        up_num = 8
    down_num = (year_idx + month + day) % 8
    if down_num == 0:
        down_num = 8

    # 时辰序数
    if hour == 0 or hour == 23:
        time_idx = 1
    else:
        time_idx = ((hour + 1) // 2) + 1

    dong_num = year_idx + month + day + time_idx
    dong_yao = yao_to_num(dong_num)

    return build_result(up_num, down_num, dong_yao,
                        f'时间起卦：{year_dz}年{month}月{day}日{time_idx}时',
                        {'year_dz': year_dz, 'month': month, 'day': day, 'hour': hour, 'shichen': time_idx})


def build_result(up_num, down_num, dong_yao, method_desc, params):
    """构建完整起卦结果"""
    up_gua = BAGUA[up_num]
    down_gua = BAGUA[down_num]
    ben_gua_name = GUA_NAMES.get((up_num, down_num), f'{up_gua["name"]}{down_gua["name"]}卦')

    # 体用判定：动爻在上卦则上为用下为体，否则上为体下为用
    if dong_yao <= 3:
        ti_gua = down_gua
        yong_gua = up_gua
        ti_pos = '下卦'
        yong_pos = '上卦'
    else:
        ti_gua = up_gua
        yong_gua = down_gua
        ti_pos = '上卦'
        yong_pos = '下卦'

    # 变卦：翻转动爻位置的阴阳
    if dong_yao <= 3:
        bian_down_num = _flip_gua_bit(down_num, dong_yao)
        bian_up_num = up_num
    else:
        bian_up_num = _flip_gua_bit(up_num, dong_yao - 3)
        bian_down_num = down_num

    bian_gua_name = GUA_NAMES.get((bian_up_num, bian_down_num), '?')

    # 互卦：取本卦2-5爻
    hu_up_num, hu_down_num = _calc_hu_gua(up_num, down_num)
    hu_gua_name = GUA_NAMES.get((hu_up_num, hu_down_num), '?')

    hu_info = {
        'name': hu_gua_name,
        'up': {'num': hu_up_num, 'name': BAGUA[hu_up_num]['name'], 'symbol': BAGUA[hu_up_num]['symbol'],
               'wuxing': BAGUA[hu_up_num]['wuxing']},
        'down': {'num': hu_down_num, 'name': BAGUA[hu_down_num]['name'], 'symbol': BAGUA[hu_down_num]['symbol'],
                 'wuxing': BAGUA[hu_down_num]['wuxing']},
        'desc': '互卦取本卦2,3,4爻为下卦，3,4,5爻为上卦',
    }

    # 五行生克关系
    sheng_ke = _get_shengke(ti_gua['wuxing'], yong_gua['wuxing'])

    return {
        'method': method_desc,
        'params': params,
        'ben_gua': {
            'name': ben_gua_name,
            'up': {'num': up_num, 'name': up_gua['name'], 'symbol': up_gua['symbol'], 'wuxing': up_gua['wuxing']},
            'down': {'num': down_num, 'name': down_gua['name'], 'symbol': down_gua['symbol'], 'wuxing': down_gua['wuxing']},
            'display': f"{down_gua['symbol']}{up_gua['symbol']}",
        },
        'dong_yao': dong_yao,
        'ti_gua': {'name': ti_gua['name'], 'symbol': ti_gua['symbol'], 'wuxing': ti_gua['wuxing'], 'position': ti_pos},
        'yong_gua': {'name': yong_gua['name'], 'symbol': yong_gua['symbol'], 'wuxing': yong_gua['wuxing'], 'position': yong_pos},
        'ti_yong_shengke': sheng_ke,
        'bian_gua': {
            'name': bian_gua_name,
            'up': {'num': bian_up_num, 'name': BAGUA[bian_up_num]['name'], 'symbol': BAGUA[bian_up_num]['symbol']},
            'down': {'num': bian_down_num, 'name': BAGUA[bian_down_num]['name'], 'symbol': BAGUA[bian_down_num]['symbol']},
        },
        'hu_gua': hu_info,
    }


def _gua_to_bits(gua_num):
    """将卦序号(1-8)转为3位二爻列表 [初爻, 二爻, 三爻]（1=阳, 0=阴）"""
    bit_map = {1: 7, 2: 3, 3: 5, 4: 1, 5: 6, 6: 2, 7: 4, 8: 0}
    val = bit_map.get(gua_num, 0)
    return [(val >> i) & 1 for i in range(3)]  # [初爻, 二爻, 三爻]


def _bits_to_gua(bits):
    """3位二爻列表 → 卦序号(1-8)"""
    val = bits[0] | (bits[1] << 1) | (bits[2] << 2)
    rev_bit_map = {7: 1, 3: 2, 5: 3, 1: 4, 6: 5, 2: 6, 4: 7, 0: 8}
    return rev_bit_map.get(val, 8)


def _flip_gua_bit(gua_num, line):
    """翻转卦爻(三爻卦)的某一位"""
    bit_map = {1: 7, 2: 3, 3: 5, 4: 1, 5: 6, 6: 2, 7: 4, 8: 0}
    rev_bit_map = {7: 1, 3: 2, 5: 3, 1: 4, 6: 5, 2: 6, 4: 7, 0: 8}

    val = bit_map.get(gua_num, 0)
    flipped = val ^ (1 << (line - 1))
    return rev_bit_map.get(flipped, 8)


def _calc_hu_gua(up_num, down_num):
    """计算互卦：取本卦2-5爻
    互卦下卦 = 本卦2,3,4爻（下卦2,3 + 上卦1）
    互卦上卦 = 本卦3,4,5爻（下卦3 + 上卦1,2）
    """
    down_bits = _gua_to_bits(down_num)  # [初爻, 二爻, 三爻]
    up_bits = _gua_to_bits(up_num)      # [四爻, 五爻, 六爻]（对应初/二/三位置）

    # 本卦6爻从下到上: down_bits[0], down_bits[1], down_bits[2], up_bits[0], up_bits[1], up_bits[2]
    # 即: 1爻=down[0], 2爻=down[1], 3爻=down[2], 4爻=up[0], 5爻=up[1], 6爻=up[2]

    # 互卦下卦 = 2,3,4爻 → down[1], down[2], up[0]
    hu_down_bits = [down_bits[1], down_bits[2], up_bits[0]]
    # 互卦上卦 = 3,4,5爻 → down[2], up[0], up[1]
    hu_up_bits = [down_bits[2], up_bits[0], up_bits[1]]

    hu_down_num = _bits_to_gua(hu_down_bits)
    hu_up_num = _bits_to_gua(hu_up_bits)

    return hu_up_num, hu_down_num


# WUXING_SHENG, WUXING_KE 已从 common.py 导入


def _get_shengke(ti_wx, yong_wx):
    """体卦对用卦的五行生克"""
    if ti_wx == yong_wx:
        return {'relation': '比和', 'ji_xiong': '吉', 'level': 2}
    if WUXING_SHENG.get(ti_wx) == yong_wx:
        return {'relation': '体生用', 'ji_xiong': '小凶', 'level': -1, 'note': '我在付出，耗泄自己'}
    if WUXING_KE.get(ti_wx) == yong_wx:
        return {'relation': '体克用', 'ji_xiong': '小吉', 'level': 1, 'note': '我方能掌控，但需努力'}
    if WUXING_SHENG.get(yong_wx) == ti_wx:
        return {'relation': '用生体', 'ji_xiong': '大吉', 'level': 3, 'note': '环境有利于我'}
    if WUXING_KE.get(yong_wx) == ti_wx:
        return {'relation': '用克体', 'ji_xiong': '大凶', 'level': -3, 'note': '环境压制我'}
    return {'relation': '未知'}


def main():
    parser = argparse.ArgumentParser(description='梅花易数起卦')
    parser.add_argument('-n', '--numbers', type=int, nargs='+', help='报数 (2或3个数字)')
    parser.add_argument('-d', '--date', type=str, help='日期 (YYYY-MM-DD)')
    parser.add_argument('-t', '--hour', type=int, help='时辰 (0-23)')
    parser.add_argument('--auto', action='store_true', help='使用当前时间')
    args = parser.parse_args()

    if args.numbers and len(args.numbers) >= 2:
        for i, n in enumerate(args.numbers):
            if n < 1:
                parser.error(f'第{i+1}个数必须 ≥ 1，当前值: {n}')
        n3 = args.numbers[2] if len(args.numbers) >= 3 else None
        result = by_numbers(args.numbers[0], args.numbers[1], n3)
    elif args.date:
        try:
            dt = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            parser.error(f'日期格式错误，应为 YYYY-MM-DD，当前值: {args.date}')
        hour = args.hour if args.hour is not None else 12
        try:
            validate_hour(hour)
        except ValueError as e:
            parser.error(str(e))
        # 公历 → 农历转换（与 --auto 一致）
        lunar = solar_to_lunar_date(dt.year, dt.month, dt.day)
        result = by_time(lunar['year_dz'], lunar['lunar_month'], lunar['lunar_day'], hour)
    elif args.auto:
        info = get_current_lunar_info()
        year_dz = info['year_dz']
        result = by_time(year_dz, info['lunar_month'], info['lunar_day'], info['hour'])
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
