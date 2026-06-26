#!/usr/bin/env python3
"""
Chinese Name Pinyin Sort
按拼音排序中文姓名，遵循中文姓名排序惯例：
1. 先按姓氏拼音分组
2. 同音姓按姓氏笔画数排序（少在前），排完一个姓再排下一个
3. 同姓内按名字拼音排序
4. 同音名按名字笔画数排序
5. 同姓名（如 刘鑫/刘辛/刘欣）标注为同音不可分

用法:
  python3 sort_names.py "张三,李四,王五"
  python3 sort_names.py < input.txt   (每行一个名字，或逗号/顿号分隔)
  echo "张三 李四" | python3 sort_names.py

输出: 排序后的名单，每行一个，附拼音信息
"""

import sys
import re
from collections import defaultdict

try:
    from pypinyin import pinyin, Style
except ImportError:
    print("ERROR: pypinyin not installed. Run: pip install pypinyin", file=sys.stderr)
    sys.exit(1)

# ── 姓氏多音字修正表 ────────────────────────────────────
# key: 姓氏, value: 正确读音(无声调小写)
SURNAME_PINYIN_FIX = {
    '曾': 'zeng',    # 姓氏读 zēng，不是 céng
    '仇': 'qiu',     # 姓氏读 qiú，不是 chóu
    '解': 'xie',     # 姓氏读 xiè，不是 jiě
    '区': 'ou',      # 姓氏读 ōu，不是 qū
    '单': 'shan',    # 姓氏读 shàn，不是 dān
    '朴': 'piao',    # 姓氏读 piáo，不是 pǔ
    '查': 'zha',     # 姓氏读 zhā，不是 chá
    '盖': 'ge',      # 姓氏读 gě，不是 gài
    '繁': 'po',      # 姓氏读 pó，不是 fán
    '翟': 'zhai',    # 姓氏读 zhái，不是 dí（两读均存在，姓多以 zhai 为主）
    '黑': 'he',      # 姓氏读 hè，不是 hēi
    '乐': 'yue',     # 姓氏读 yuè，不是 lè
    '覃': 'qin',     # 姓氏读 qín，不是 tán
    '折': 'she',     # 姓氏读 shé
    '种': 'chong',   # 姓氏读 chóng，不是 zhǒng
    '燕': 'yan',     # 两读，姓以 yān 为主
    '哈': 'ha',      # 姓氏读 hǎ
    '纪': 'ji',      # 姓氏读 jǐ
    '过': 'guo',     # 姓氏读 guō
    '那': 'na',      # 姓氏读 nā
    '应': 'ying',    # 姓氏读 yīng
    '秘': 'bi',      # 姓氏读 bì
    '占': 'zhan',    # 姓氏读 zhān
    '虢': 'guo',     # 姓氏读 guó
    '訾': 'zi',      # 姓氏读 zī
    '句': 'gou',     # 姓氏读 gōu
    '阚': 'kan',     # 姓氏读 kàn
    '乜': 'nie',     # 姓氏读 niè
}

# 姓氏声调修正（用于显示带声调拼音）
SURNAME_TONE_FIX = {
    '曾': 'zēng', '仇': 'qiú', '解': 'xiè', '区': 'ōu',
    '单': 'shàn', '朴': 'piáo', '查': 'zhā', '盖': 'gě',
    '翟': 'zhái', '乐': 'yuè', '覃': 'qín', '种': 'chóng',
}

# ── 复姓列表 ──────────────────────────────────────────────
COMPOUND_SURNAMES = {
    '欧阳', '司马', '上官', '诸葛', '东方', '皇甫', '尉迟',
    '公孙', '令狐', '宇文', '长孙', '慕容', '司徒', '司空',
    '端木', '轩辕', '百里', '南宫', '独孤', '夏侯', '申屠',
    '闻人', '第五', '呼延', '万俟', '赫连', '澹台', '太叔',
}


# ── 笔画数 ──────────────────────────────────────────────

_STROKE_CACHE = {}

_COMMON_STROKES = {
    '于': 3, '刁': 3, '万': 3,
    '王': 4, '仇': 4, '毛': 4, '方': 4, '孔': 4, '尤': 4, '尹': 4,
    '邓': 4, '巴': 4, '戈': 4,
    '白': 5, '石': 5, '田': 5, '包': 5, '冯': 5, '司': 5, '兰': 5,
    '叶': 5, '卢': 5, '史': 5, '冉': 5, '付': 5, '代': 5,
    '刘': 6, '江': 6, '吕': 6, '乔': 6, '任': 6, '伍': 6, '向': 6,
    '邬': 6, '华': 6, '伊': 6, '安': 6, '庄': 6, '齐': 6, '米': 6,
    '许': 6, '危': 6, '邢': 6, '毕': 6, '曲': 6, '牟': 6,
    '吴': 7, '张': 7, '余': 7, '邱': 7, '何': 7, '但': 7, '冷': 7,
    '汪': 7, '沈': 7, '宋': 7, '陆': 7, '陈': 7, '苏': 7, '杜': 7,
    '杨': 7, '邹': 7, '邵': 7, '李': 7, '肖': 7, '连': 7, '严': 7,
    '时': 7, '闵': 7, '沃': 7, '闵': 7, '芮': 7, '利': 7,
    '林': 8, '周': 8, '金': 8, '季': 8, '孟': 8, '岳': 8, '范': 8,
    '郎': 8, '郁': 8, '罗': 8, '易': 8, '苗': 8, '郑': 8, '武': 8,
    '单': 8, '居': 8, '屈': 8, '练': 8, '杭': 8, '尚': 8, '卓': 8,
    '明': 8, '庞': 8, '和': 8,
    '姜': 9, '俞': 9, '柳': 9, '赵': 9, '胡': 9, '施': 9, '洪': 9,
    '姚': 9, '贺': 9, '侯': 9, '段': 9, '费': 9, '钟': 9, '骆': 9,
    '项': 9, '宫': 9, '查': 9, '秋': 9, '彦': 9, '封': 9, '冒': 9,
    '韦': 9, '郝': 9, '欧': 9,
    '徐': 10, '孙': 10, '马': 10, '高': 10, '郭': 10, '秦': 10,
    '袁': 10, '贾': 10, '夏': 10, '顾': 10, '倪': 10, '翁': 10,
    '殷': 10, '晏': 10, '涂': 10, '柴': 10, '党': 10, '钱': 10,
    '浦': 10, '聂': 10, '奚': 10, '桂': 10, '留': 10,
    '黄': 11, '曹': 11, '章': 11, '梅': 11, '崔': 11, '龚': 11,
    '盛': 11, '常': 11, '康': 11, '阎': 11, '梁': 11, '麻': 11,
    '屠': 11, '宿': 11, '扈': 11, '邢': 11,
    '谢': 12, '韩': 12, '董': 12, '彭': 12, '蒋': 12, '程': 12,
    '鲁': 12, '傅': 12, '温': 12, '曾': 12, '覃': 12, '焦': 12,
    '舒': 12, '童': 12, '葛': 12, '游': 12, '靳': 12, '鲍': 12,
    '惠': 12, '雷': 13, '虞': 13, '裘': 13, '解': 13, '詹': 13,
    '楚': 13, '甄': 13, '廉': 13, '雍': 13, '满': 13, '路': 13,
    '蒙': 13, '楼': 13, '蒲': 13, '訾': 13,
    '廖': 14, '蔡': 14, '管': 14, '翟': 14, '谭': 14, '熊': 14,
    '缪': 14, '慕': 14, '漆': 14, '阚': 14, '臧': 14, '赫': 14,
    '裴': 14,
    '樊': 15, '黎': 15, '墨': 15, '潘': 15, '滕': 15, '颜': 15,
    '巩': 15, '厉': 15, '暴': 15,
    '霍': 16, '薛': 16, '穆': 16, '冀': 16, '薄': 16, '衡': 16,
    '磨': 16,
    '戴': 17, '魏': 17, '鞠': 17, '糜': 17, '霞': 17,
    '瞿': 18, '丰': 18, '鳌': 18,
    '关': 19,
}


def _get_stroke(char):
    if char in _STROKE_CACHE:
        return _STROKE_CACHE[char]
    if char in _COMMON_STROKES:
        _STROKE_CACHE[char] = _COMMON_STROKES[char]
        return _COMMON_STROKES[char]
    # 退化估算
    approx = 8
    _STROKE_CACHE[char] = approx
    return approx


def surname_stroke_count(full_name):
    surname = get_surname(full_name)
    return sum(_get_stroke(c) for c in surname)


def given_name_stroke_count(full_name):
    given = get_given_name(full_name)
    return sum(_get_stroke(c) for c in given)


# ── 姓氏/名字提取 ──────────────────────────────────────

def get_surname(full_name):
    for cs in COMPOUND_SURNAMES:
        if full_name.startswith(cs):
            return cs
    return full_name[0]


def get_given_name(full_name):
    surname = get_surname(full_name)
    return full_name[len(surname):]


# ── 拼音获取 ──────────────────────────────────────────────

def get_surname_pinyin_normal(full_name):
    """获取姓氏拼音（无声调），使用修正表"""
    surname = get_surname(full_name)
    if surname in SURNAME_PINYIN_FIX:
        return SURNAME_PINYIN_FIX[surname]
    result = pinyin(surname, style=Style.NORMAL, heteronym=False)
    return ''.join([p[0] for p in result])


def get_surname_pinyin_tone(full_name):
    """获取姓氏拼音（带声调），使用修正表"""
    surname = get_surname(full_name)
    if surname in SURNAME_TONE_FIX:
        return SURNAME_TONE_FIX[surname]
    result = pinyin(surname, style=Style.TONE, heteronym=False)
    return ''.join([p[0] for p in result])


def get_given_name_pinyin_normal(full_name):
    given = get_given_name(full_name)
    result = pinyin(given, style=Style.NORMAL, heteronym=False)
    return ''.join([p[0] for p in result])


def get_full_pinyin_tone(full_name):
    """获取完整姓名带声调拼音"""
    surname_py = get_surname_pinyin_tone(full_name)
    given = get_given_name(full_name)
    result = pinyin(given, style=Style.TONE, heteronym=False)
    given_py = ''.join([p[0] for p in result])
    # 首字母大写
    if surname_py:
        surname_py = surname_py[0].upper() + surname_py[1:]
    if given_py:
        given_py = given_py[0].upper() + given_py[1:]
    return f"{surname_py} {given_py}".strip()


# ── 排序逻辑 ──────────────────────────────────────────────

def sort_key(full_name):
    """
    排序键:
    1. 姓氏拼音（无声调字母序）
    2. 姓氏笔画数（同音姓按笔画排，如 于3<余7<俞9<虞13）
    3. 姓氏本身（同音同笔画按字排）
    4. 名字拼音（无声调字母序）
    5. 名字笔画数（同音名按笔画排）
    6. 全名（最终兜底）
    """
    surname_py = get_surname_pinyin_normal(full_name)
    surname_stroke = surname_stroke_count(full_name)
    surname_char = get_surname(full_name)
    given_py = get_given_name_pinyin_normal(full_name)
    given_stroke = given_name_stroke_count(full_name)

    return (surname_py, surname_stroke, surname_char, given_py, given_stroke, full_name)


def sort_chinese_names(names):
    return sorted(names, key=sort_key)


# ── 格式化输出 ──────────────────────────────────────────

def format_result(sorted_names, numbered=True):
    lines = []
    for i, name in enumerate(sorted_names, 1):
        py = get_full_pinyin_tone(name)
        prefix = f"{i}. " if numbered else ""
        lines.append(f"{prefix}{name}（{py}）")
    return '\n'.join(lines)


# ── 同音标记 ──────────────────────────────────────────────

def find_homophones(sorted_names):
    groups = defaultdict(list)
    for name in sorted_names:
        surname = get_surname(name)
        surname_py = get_surname_pinyin_normal(name)
        given_py = get_given_name_pinyin_normal(name)
        key = f"{surname_py}_{given_py}"
        groups[key].append(name)

    result = []
    for key, names_list in groups.items():
        # 检查是否有不同姓氏的同音
        surnames = set(get_surname(n) for n in names_list)
        if len(surnames) > 1 or len(names_list) > 1:
            # 仅在有多于一个不同字时标记
            chars = set(name for name in names_list)
            if len(chars) > 1:
                result.append((key, names_list))
    return result


# ── 分组输出（按姓分组） ────────────────────────────────

def format_grouped(sorted_names):
    """按姓氏分组输出，更易阅读"""
    groups = defaultdict(list)
    for name in sorted_names:
        surname = get_surname(name)
        surname_py = get_surname_pinyin_normal(name)
        groups[(surname_py, surname)].append(name)

    # 组内排序 + 组间排序
    sorted_groups = sorted(groups.keys(), key=lambda x: (x[0], surname_stroke_count(x[1] * 2) if False else _get_stroke(x[1])))

    lines = []
    idx = 1
    for surname_py, surname in sorted_groups:
        for name in groups[(surname_py, surname)]:
            py = get_full_pinyin_tone(name)
            lines.append(f"{idx}. {name}（{py}）")
            idx += 1

    return '\n'.join(lines)


# ── 输入解析 ──────────────────────────────────────────────

def parse_input(text):
    text = text.replace('、', ',').replace('，', ',').replace('\t', ',')
    parts = re.split(r'[,\n]', text)
    names = [p.strip() for p in parts if p.strip()]
    valid = []
    for n in names:
        # 允许2-5个中文字符（含复姓）
        if re.match(r'^[\u4e00-\u9fff]{2,5}$', n):
            valid.append(n)
        else:
            print(f"WARN: 跳过非姓名项: '{n}'", file=sys.stderr)
    return valid


# ── 主入口 ──────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description='中文姓名拼音排序')
    parser.add_argument('names', nargs='*', help='姓名列表（逗号/顿号/空格分隔）')
    parser.add_argument('--no-number', action='store_true', help='不显示序号')
    parser.add_argument('--grouped', action='store_true', help='按姓氏分组显示')
    args = parser.parse_args()

    if args.names:
        input_text = ' '.join(args.names)
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
    else:
        print(__doc__)
        sys.exit(0)

    names = parse_input(input_text)
    if not names:
        print("ERROR: 未找到有效的中文姓名", file=sys.stderr)
        sys.exit(1)

    sorted_names = sort_chinese_names(names)

    if args.grouped:
        print(format_grouped(sorted_names))
    else:
        print(format_result(sorted_names, numbered=not args.no_number))

    # 同音提示
    homophones = find_homophones(sorted_names)
    if homophones:
        print("\n⚠ 同音不可分组：")
        for key, group in homophones:
            print(f"  {'、'.join(group)}（{get_full_pinyin_tone(group[0])}）")


if __name__ == '__main__':
    main()
