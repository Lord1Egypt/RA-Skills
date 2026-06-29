#!/usr/bin/env python3
"""
六爻摇卦与纳甲装卦脚本
用法: python liuyao_yaogua.py [-q <问题>] [--json]
      直接运行 = 随机摇卦 + 纳甲装卦
输出: JSON 格式的完整装卦结果
"""

import argparse
import json
import random
import sys
import os

# Ensure common.py is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import get_day_ganzhi, TIANGAN, DIZHI, WUXING, WUXING_SHENG, WUXING_KE

# Fix Windows console encoding for Unicode trigram symbols (GBK -> UTF-8)
try:
    if hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


# ============================================================
# 基础知识表（TIANGAN/DIZHI/WUXING/WUXING_SHENG/WUXING_KE 已从 common.py 导入）
# ============================================================

# 八卦符号
GUA_SYMBOLS = {
    '乾': '☰', '兑': '☱', '离': '☲', '震': '☳',
    '巽': '☴', '坎': '☵', '艮': '☶', '坤': '☷',
}

# 八纯卦纳甲 (name -> {line_pos: (tian_gan, di_zhi)})
NAJIA = {
    '乾': {0: ('甲', '子'), 1: ('甲', '寅'), 2: ('甲', '辰'),
            3: ('壬', '午'), 4: ('壬', '申'), 5: ('壬', '戌')},
    '坎': {0: ('戊', '寅'), 1: ('戊', '辰'), 2: ('戊', '午'),
            3: ('戊', '申'), 4: ('戊', '戌'), 5: ('戊', '子')},
    '艮': {0: ('丙', '辰'), 1: ('丙', '午'), 2: ('丙', '申'),
            3: ('丙', '戌'), 4: ('丙', '子'), 5: ('丙', '寅')},
    '震': {0: ('庚', '子'), 1: ('庚', '寅'), 2: ('庚', '辰'),
            3: ('庚', '午'), 4: ('庚', '申'), 5: ('庚', '戌')},
    '巽': {0: ('辛', '丑'), 1: ('辛', '亥'), 2: ('辛', '酉'),
            3: ('辛', '未'), 4: ('辛', '巳'), 5: ('辛', '卯')},
    '离': {0: ('己', '卯'), 1: ('己', '丑'), 2: ('己', '亥'),
            3: ('己', '酉'), 4: ('己', '未'), 5: ('己', '巳')},
    '坤': {0: ('乙', '未'), 1: ('乙', '巳'), 2: ('乙', '卯'),
            3: ('癸', '丑'), 4: ('癸', '亥'), 5: ('癸', '酉')},
    '兑': {0: ('丁', '巳'), 1: ('丁', '卯'), 2: ('丁', '丑'),
            3: ('丁', '亥'), 4: ('丁', '酉'), 5: ('丁', '未')},
}

# 六十四卦 → 所属八宫
GUA_GONG = {
    '乾为天': '乾', '天风姤': '乾', '天山遁': '乾', '天地否': '乾',
    '风地观': '乾', '山地剥': '乾', '火地晋': '乾', '火天大有': '乾',
    '兑为泽': '兑', '泽水困': '兑', '泽地萃': '兑', '泽山咸': '兑',
    '水山蹇': '兑', '地山谦': '兑', '雷山小过': '兑', '雷泽归妹': '兑',
    '离为火': '离', '火山旅': '离', '火风鼎': '离', '火水未济': '离',
    '山水蒙': '离', '风水涣': '离', '天水讼': '离', '天火同人': '离',
    '震为雷': '震', '雷地豫': '震', '雷水解': '震', '雷风恒': '震',
    '地风升': '震', '水风井': '震', '泽风大过': '震', '泽雷随': '震',
    '巽为风': '巽', '风天小畜': '巽', '风火家人': '巽', '风雷益': '巽',
    '天雷无妄': '巽', '火雷噬嗑': '巽', '山雷颐': '巽', '山风蛊': '巽',
    '坎为水': '坎', '水泽节': '坎', '水雷屯': '坎', '水火既济': '坎',
    '泽火革': '坎', '雷火丰': '坎', '地火明夷': '坎', '地水师': '坎',
    '艮为山': '艮', '山火贲': '艮', '山天大畜': '艮', '山泽损': '艮',
    '火泽睽': '艮', '天泽履': '艮', '风泽中孚': '艮', '风山渐': '艮',
    '坤为地': '坤', '地雷复': '坤', '地泽临': '坤', '地天泰': '坤',
    '雷天大壮': '坤', '泽天夬': '坤', '水天需': '坤', '水地比': '坤',
}

# 六十四卦 → 世爻位置 {line_idx: (shi_line_idx, ying_line_idx)}
SHI_YING = {}
# 八宫八卦的世应规则
GONG_GUA_LIST = {
    '乾': ['乾为天', '天风姤', '天山遁', '天地否', '风地观', '山地剥', '火地晋', '火天大有'],
    '兑': ['兑为泽', '泽水困', '泽地萃', '泽山咸', '水山蹇', '地山谦', '雷山小过', '雷泽归妹'],
    '离': ['离为火', '火山旅', '火风鼎', '火水未济', '山水蒙', '风水涣', '天水讼', '天火同人'],
    '震': ['震为雷', '雷地豫', '雷水解', '雷风恒', '地风升', '水风井', '泽风大过', '泽雷随'],
    '巽': ['巽为风', '风天小畜', '风火家人', '风雷益', '天雷无妄', '火雷噬嗑', '山雷颐', '山风蛊'],
    '坎': ['坎为水', '水泽节', '水雷屯', '水火既济', '泽火革', '雷火丰', '地火明夷', '地水师'],
    '艮': ['艮为山', '山火贲', '山天大畜', '山泽损', '火泽睽', '天泽履', '风泽中孚', '风山渐'],
    '坤': ['坤为地', '地雷复', '地泽临', '地天泰', '雷天大壮', '泽天夬', '水天需', '水地比'],
}

SHI_POSITIONS = [5, 0, 1, 2, 3, 4, 3, 2]  # 本宫/一世/二世/.../归魂 的世爻位置(0-based)
YING_OFFSET = 3  # 应爻与世爻的间隔

for gong, gua_list in GONG_GUA_LIST.items():
    for idx, gua_name in enumerate(gua_list):
        shi = SHI_POSITIONS[idx]
        ying = (shi + YING_OFFSET) % 6
        SHI_YING[gua_name] = (shi, ying)

# 五行表（已从 common.py 导入 WUXING）

# 六亲判定
LIUQIN_RULES = {
    '生我': '父母', '我生': '子孙', '克我': '官鬼',
    '我克': '妻财', '同': '兄弟',
}

# WUXING_SHENG, WUXING_KE 已从 common.py 导入


def get_liuqin(wo_wuxing, yao_wuxing):
    """根据我和爻的五行关系返回六亲"""
    if wo_wuxing == yao_wuxing:
        return '兄弟'
    if WUXING_SHENG.get(wo_wuxing) == yao_wuxing:
        return '子孙'
    if WUXING_KE.get(wo_wuxing) == yao_wuxing:
        return '妻财'
    if WUXING_SHENG.get(yao_wuxing) == wo_wuxing:
        return '父母'
    return '官鬼'


# 六神排法
LIUSHEN = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']


def get_liushen_start(day_tg):
    """按日干确定六神起始"""
    mapping = {
        '甲': 0, '乙': 0,
        '丙': 1, '丁': 1,
        '戊': 2, '己': 3,
        '庚': 4, '辛': 4,
        '壬': 5, '癸': 5,
    }
    return mapping.get(day_tg, 0)


def get_xunkong(ri_tg, ri_dz):
    """计算旬空"""
    XUNKONG_MAP = {
        '甲子': ('戌', '亥'), '甲戌': ('申', '酉'),
        '甲申': ('午', '未'), '甲午': ('辰', '巳'),
        '甲辰': ('寅', '卯'), '甲寅': ('子', '丑'),
    }
    tg_idx = TIANGAN.index(ri_tg)
    dz_idx = DIZHI.index(ri_dz)
    offset = (dz_idx - tg_idx) % 12
    if offset < 0:
        offset += 12
    xunshou_dz = DIZHI[(dz_idx - tg_idx) % 12]
    xunshou = '甲' + xunshou_dz
    return XUNKONG_MAP.get(xunshou, ('?', '?'))


# ============================================================
# 主逻辑
# ============================================================

def yaogua():
    """模拟六次摇卦，返回爻列表（三枚铜钱二项分布 B(3,0.5)）"""
    lines = []
    for i in range(6):
        # 三枚铜钱各抛一次，背面数服从二项分布 B(3, 0.5)
        backs = sum(random.randint(0, 1) for _ in range(3))
        if backs == 3:
            yaoxiang = '老阳'
            symbol = '○'
            is_dong = True
            yin_yang = '阳'
        elif backs == 2:
            yaoxiang = '少阴'
            symbol = '- -'
            is_dong = False
            yin_yang = '阴'
        elif backs == 1:
            yaoxiang = '少阳'
            symbol = '—'
            is_dong = False
            yin_yang = '阳'
        else:
            yaoxiang = '老阴'
            symbol = '×'
            is_dong = True
            yin_yang = '阴'
        lines.append({
            'pos': i + 1,
            'pos_name': ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'][i],
            'backs': backs,
            'yaoxiang': yaoxiang,
            'symbol': symbol,
            'yin_yang': yin_yang,
            'is_dong': is_dong,
        })
    return lines


def get_gua_name(lines):
    """从爻列表获取本卦名"""
    # 用六位二进制表示卦：阳=1, 阴=0, 从下到上
    # 下卦 = 低三位, 上卦 = 高三位
    BAGUA_BITS = {
        0b111: '乾', 0b011: '兑', 0b101: '离', 0b001: '震',
        0b110: '巽', 0b010: '坎', 0b100: '艮', 0b000: '坤',
    }

    down = sum((1 if l['yin_yang'] == '阳' else 0) << i for i, l in enumerate(lines[:3]))
    up = sum((1 if l['yin_yang'] == '阳' else 0) << i for i, l in enumerate(lines[3:]))

    # 标准化为三位
    down_gua = BAGUA_BITS.get(down, '?')
    up_gua = BAGUA_BITS.get(up, '?')

    # 查找六十四卦名
    GUA_NAMES = {
        ('乾', '乾'): '乾为天', ('乾', '兑'): '天泽履', ('乾', '离'): '天火同人', ('乾', '震'): '天雷无妄',
        ('乾', '巽'): '天风姤', ('乾', '坎'): '天水讼', ('乾', '艮'): '天山遁', ('乾', '坤'): '天地否',
        ('兑', '乾'): '泽天夬', ('兑', '兑'): '兑为泽', ('兑', '离'): '泽火革', ('兑', '震'): '泽雷随',
        ('兑', '巽'): '泽风大过', ('兑', '坎'): '泽水困', ('兑', '艮'): '泽山咸', ('兑', '坤'): '泽地萃',
        ('离', '乾'): '火天大有', ('离', '兑'): '火泽睽', ('离', '离'): '离为火', ('离', '震'): '火雷噬嗑',
        ('离', '巽'): '火风鼎', ('离', '坎'): '火水未济', ('离', '艮'): '火山旅', ('离', '坤'): '火地晋',
        ('震', '乾'): '雷天大壮', ('震', '兑'): '雷泽归妹', ('震', '离'): '雷火丰', ('震', '震'): '震为雷',
        ('震', '巽'): '雷风恒', ('震', '坎'): '雷水解', ('震', '艮'): '雷山小过', ('震', '坤'): '雷地豫',
        ('巽', '乾'): '风天小畜', ('巽', '兑'): '风泽中孚', ('巽', '离'): '风火家人', ('巽', '震'): '风雷益',
        ('巽', '巽'): '巽为风', ('巽', '坎'): '风水涣', ('巽', '艮'): '风山渐', ('巽', '坤'): '风地观',
        ('坎', '乾'): '水天需', ('坎', '兑'): '水泽节', ('坎', '离'): '水火既济', ('坎', '震'): '水雷屯',
        ('坎', '巽'): '水风井', ('坎', '坎'): '坎为水', ('坎', '艮'): '水山蹇', ('坎', '坤'): '水地比',
        ('艮', '乾'): '山天大畜', ('艮', '兑'): '山泽损', ('艮', '离'): '山火贲', ('艮', '震'): '山雷颐',
        ('艮', '巽'): '山风蛊', ('艮', '坎'): '山水蒙', ('艮', '艮'): '艮为山', ('艮', '坤'): '山地剥',
        ('坤', '乾'): '地天泰', ('坤', '兑'): '地泽临', ('坤', '离'): '地火明夷', ('坤', '震'): '地雷复',
        ('坤', '巽'): '地风升', ('坤', '坎'): '地水师', ('坤', '艮'): '地山谦', ('坤', '坤'): '坤为地',
    }

    gua_name = GUA_NAMES.get((up_gua, down_gua), f'{up_gua}{down_gua}卦')

    return {
        'gua_name': gua_name,
        'up_gua_name': up_gua,
        'down_gua_name': down_gua,
        'up_gua_symbol': GUA_SYMBOLS.get(up_gua, '?'),
        'down_gua_symbol': GUA_SYMBOLS.get(down_gua, '?'),
        'up_bits': up,
        'down_bits': down,
    }


def get_biangua_name(lines):
    """获取变卦名（动爻翻转后）"""
    flipped = []
    for l in lines:
        if l['is_dong']:
            flipped.append('阳' if l['yin_yang'] == '阴' else '阴')
        else:
            flipped.append(l['yin_yang'])
    # 构建 fake lines for get_gua_name
    fake_lines = [{'yin_yang': y} for y in flipped]
    return get_gua_name(fake_lines)


def zhuanggua(lines, day_tg):
    """装卦：给每个爻配纳甲+六亲+六神"""
    gua_info = get_gua_name(lines)
    gua_name = gua_info['gua_name']
    gong = GUA_GONG.get(gua_name, '?')
    gong_wuxing = WUXING.get(gong, '?')

    # 纳甲：按内外卦分别取纳甲（非按宫）
    # 下卦(初爻/二爻/三爻)取下卦八纯卦纳甲，上卦(四爻/五爻/六爻)取上卦八纯卦纳甲
    down_najia = NAJIA.get(gua_info['down_gua_name'], {})
    up_najia = NAJIA.get(gua_info['up_gua_name'], {})

    # 六神起始
    liushen_start = get_liushen_start(day_tg)
    # 世应
    shi_line, ying_line = SHI_YING.get(gua_name, (0, 3))

    # 动爻
    dong_lines = [i for i, l in enumerate(lines) if l['is_dong']]

    result = []
    for i, line in enumerate(lines):
        if i < 3:
            tg_dz = down_najia.get(i, ('?', '?'))
        else:
            tg_dz = up_najia.get(i, ('?', '?'))
        yao_wuxing = WUXING.get(tg_dz[1], '?')
        liuqin = get_liuqin(gong_wuxing, yao_wuxing)
        liushen = LIUSHEN[(liushen_start + i) % 6]
        shi_ying = '世' if i == shi_line else ('应' if i == ying_line else '')

        result.append({
            'pos': line['pos'],
            'pos_name': line['pos_name'],
            'yaoxiang': line['yaoxiang'],
            'symbol': line['symbol'],
            'is_dong': line['is_dong'],
            'tian_gan': tg_dz[0],
            'di_zhi': tg_dz[1],
            'wuxing': yao_wuxing,
            'liuqin': liuqin,
            'liushen': liushen,
            'shi_ying': shi_ying,
        })

    biangua_info = get_biangua_name(lines) if dong_lines else None

    return {
        'gua_name': gua_name,
        'gua_gong': gong,
        'gong_wuxing': gong_wuxing,
        'up_gua': {'name': gua_info['up_gua_name'], 'symbol': gua_info['up_gua_symbol']},
        'down_gua': {'name': gua_info['down_gua_name'], 'symbol': gua_info['down_gua_symbol']},
        'biangua_name': biangua_info['gua_name'] if biangua_info else None,
        'biangua_up': {'name': biangua_info['up_gua_name'], 'symbol': biangua_info['up_gua_symbol']} if biangua_info else None,
        'biangua_down': {'name': biangua_info['down_gua_name'], 'symbol': biangua_info['down_gua_symbol']} if biangua_info else None,
        'dong_lines': [[i + 1, lines[i]['symbol']] for i in dong_lines],
        'shi_line': shi_line + 1,
        'ying_line': ying_line + 1,
        'lines': result,
    }


def main():
    parser = argparse.ArgumentParser(description='六爻摇卦与纳甲装卦')
    parser.add_argument('-q', '--question', type=str, default='', help='占问事项')
    parser.add_argument('--json', action='store_true', help='仅输出 JSON')
    parser.add_argument('--day-tg', type=str, default='', help='日干（不指定则自动获取当前日干）')
    parser.add_argument('--day-dz', type=str, default='', help='日支（不指定则自动获取当前日支）')
    parser.add_argument('--auto', action='store_true', help='自动使用当前日干支（默认行为）')
    args = parser.parse_args()

    lines = yaogua()

    # 获取日干支：优先用户传入，否则自动检测
    if args.day_tg and args.day_dz:
        if args.day_tg not in TIANGAN:
            parser.error(f'日干无效，应为: {",".join(TIANGAN)}，当前值: {args.day_tg}')
        if args.day_dz not in DIZHI:
            parser.error(f'日支无效，应为: {",".join(DIZHI)}，当前值: {args.day_dz}')
        day_tg = args.day_tg
        day_dz = args.day_dz
    elif args.day_tg:
        if args.day_tg not in TIANGAN:
            parser.error(f'日干无效，应为: {",".join(TIANGAN)}，当前值: {args.day_tg}')
        day_tg = args.day_tg
        day_dz = '子'  # 仅传入日干时，日支默认子（旬空将不准确，建议同时传入日支）
    else:
        from datetime import date
        day_tg, day_dz, day_gz = get_day_ganzhi(date.today())

    result = zhuanggua(lines, day_tg)

    # 自动 mode 也需要更新日干支到结果
    result['day_tg'] = day_tg
    result['day_dz'] = day_dz

    result['question'] = args.question

    # 计算旬空
    xunkong = get_xunkong(day_tg, day_dz)
    result['xunkong'] = xunkong

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 完整输出
        print(f"占问事项：{args.question or '(未指定)'}")
        print(f"当前日干支：{day_tg}{day_dz}")
        print(f"\n{'='*60}")
        print("【摇卦记录】")
        print(f"{'爻位':<6}{'背面数':<8}{'爻象':<8}{'标记'}")
        for l in lines:
            print(f"{l['pos_name']:<6}{l['backs']:<8}{l['yaoxiang']:<8}{l['symbol']}")
        print(f"\n本卦：{result['gua_name']} {result['down_gua']['symbol']}{result['up_gua']['symbol']}")
        if result['biangua_name']:
            print(f"变卦：{result['biangua_name']} {result['biangua_down']['symbol']}{result['biangua_up']['symbol']}")
            print(f"动爻：{', '.join([f'{pos}爻{sym}' for pos, sym in result['dong_lines']])}")
        print(f"卦宫：{result['gua_gong']}（{result['gong_wuxing']}）")
        print(f"\n{'='*60}")
        print("【装卦表】")
        print(f"{'爻位':<6}{'天干':<6}{'地支':<6}{'五行':<6}{'六亲':<6}{'六神':<6}{'世应'}")
        for l in result['lines']:
            print(f"{l['pos_name']:<6}{l['tian_gan']:<6}{l['di_zhi']:<6}{l['wuxing']:<6}{l['liuqin']:<6}{l['liushen']:<6}{l['shi_ying']}")
        print(f"\n世爻：第{result['shi_line']}爻  应爻：第{result['ying_line']}爻")
        print(f"旬空：{result['xunkong'][0]}{result['xunkong'][1]}")


if __name__ == '__main__':
    main()
