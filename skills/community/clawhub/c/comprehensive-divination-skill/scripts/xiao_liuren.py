#!/usr/bin/env python3
"""
小六壬掌诀推算脚本
用法: python xiao_liuren.py -m <农历月> -d <农历日> -t <时辰(0-23)>
      或 python xiao_liuren.py -n <数1> <数2> <数3>
      或 python xiao_liuren.py --auto（使用当前时间自动推算）
输出: JSON 格式的推算结果
"""

import argparse
import json
import sys
import os

# Ensure common.py is importable from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import get_current_lunar_info, validate_month, validate_day, validate_hour

# Fix Windows console encoding for Unicode output (GBK -> UTF-8)
try:
    if hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


# 六宫定义
LIU_GONG = {
    1: {
        'name': '大安',
        'wuxing': '木',
        'color': '青色',
        'direction': '东方',
        'numbers': '1、5、7',
        'ji_xiong': '大吉',
        'shen': '青龙',
        'summary': '身不动时，事事大吉。求谋得利，出行顺遂。',
    },
    2: {
        'name': '留连',
        'wuxing': '水',
        'color': '黑色',
        'direction': '南方',
        'numbers': '2、8、10',
        'ji_xiong': '凶',
        'shen': '玄武',
        'summary': '人未归时，事难成就。去者未回，宜耐心等待。',
    },
    3: {
        'name': '速喜',
        'wuxing': '火',
        'color': '红色',
        'direction': '南方',
        'numbers': '3、6、9',
        'ji_xiong': '大吉',
        'shen': '朱雀',
        'summary': '喜事来临，万事迅速。求谋有喜，行人立至。',
    },
    4: {
        'name': '赤口',
        'wuxing': '金',
        'color': '白色',
        'direction': '西方',
        'numbers': '4、7、10',
        'ji_xiong': '凶',
        'shen': '白虎',
        'summary': '官非口舌，是非缠身。言语谨慎，莫与人争。',
    },
    5: {
        'name': '小吉',
        'wuxing': '水',
        'color': '黑色',
        'direction': '东方',
        'numbers': '1、5、7',
        'ji_xiong': '吉',
        'shen': '六合',
        'summary': '人来喜时，凡事皆合。大吉大利，和合之象。',
    },
    6: {
        'name': '空亡',
        'wuxing': '土',
        'color': '黄色',
        'direction': '中央',
        'numbers': '5、10',
        'ji_xiong': '大凶',
        'shen': '勾陈',
        'summary': '音信稀时，事难如人意。谋事落空，劳而无成。',
    },
}


def calc_gong(start_gong: int, count: int) -> int:
    """从起始宫位数，顺时针数 count 步，返回落宫(1-6)"""
    return ((start_gong - 1) + count - 1) % 6 + 1


def by_month_day_hour(month: int, day: int, hour: int) -> dict:
    """月日时推算法"""
    # 时辰转序数
    # 子=1 (23-1), 丑=2 (1-3), ...
    if hour == 0 or hour == 23:
        time_idx = 1
    else:
        time_idx = ((hour + 1) // 2) + 1

    # 月上起日
    gong_a = calc_gong(1, month)
    # 日上起时
    gong_b = calc_gong(gong_a, day)
    # 时上定时
    gong_c = calc_gong(gong_b, time_idx)

    return {
        'method': '月日时推算',
        'params': {'month': month, 'day': day, 'hour': hour, 'shichen': time_idx},
        'steps': [
            {'from': '大安(1)', 'count': month, 'result': gong_a,
             'desc': f'正月起大安，数至{month}月 → {LIU_GONG[gong_a]["name"]}({gong_a})'},
            {'from': f'{LIU_GONG[gong_a]["name"]}({gong_a})', 'count': day, 'result': gong_b,
             'desc': f'初一从{LIU_GONG[gong_a]["name"]}起，数至{day}日 → {LIU_GONG[gong_b]["name"]}({gong_b})'},
            {'from': f'{LIU_GONG[gong_b]["name"]}({gong_b})', 'count': time_idx, 'result': gong_c,
             'desc': f'子时从{LIU_GONG[gong_b]["name"]}起，数至第{time_idx}时辰 → {LIU_GONG[gong_c]["name"]}({gong_c})'},
        ],
        'result_gong': gong_c,
        'result': LIU_GONG[gong_c],
    }


def by_numbers(n1: int, n2: int, n3: int) -> dict:
    """用户报数法"""
    gong_a = calc_gong(1, n1)
    gong_b = calc_gong(gong_a, n2)
    gong_c = calc_gong(gong_b, n3)

    return {
        'method': '用户报数',
        'params': {'n1': n1, 'n2': n2, 'n3': n3},
        'steps': [
            {'from': '大安(1)', 'count': n1, 'result': gong_a,
             'desc': f'从大安起数{n1} → {LIU_GONG[gong_a]["name"]}({gong_a})'},
            {'from': f'{LIU_GONG[gong_a]["name"]}({gong_a})', 'count': n2, 'result': gong_b,
             'desc': f'从{LIU_GONG[gong_a]["name"]}起数{n2} → {LIU_GONG[gong_b]["name"]}({gong_b})'},
            {'from': f'{LIU_GONG[gong_b]["name"]}({gong_b})', 'count': n3, 'result': gong_c,
             'desc': f'从{LIU_GONG[gong_b]["name"]}起数{n3} → {LIU_GONG[gong_c]["name"]}({gong_c})'},
        ],
        'result_gong': gong_c,
        'result': LIU_GONG[gong_c],
    }


def main():
    parser = argparse.ArgumentParser(description='小六壬掌诀推算')
    parser.add_argument('-m', '--month', type=int, help='农历月 (1-12)')
    parser.add_argument('-d', '--day', type=int, help='农历日 (1-30)')
    parser.add_argument('-t', '--hour', type=int, help='时辰 24小时制 (0-23)')
    parser.add_argument('-n', '--numbers', type=int, nargs=3, help='三个报数')
    parser.add_argument('--auto', action='store_true', help='使用当前时间自动推算')

    args = parser.parse_args()

    if args.numbers:
        for i, n in enumerate(args.numbers):
            if n < 1:
                parser.error(f'第{i+1}个数必须 ≥ 1，当前值: {n}')
        result = by_numbers(*args.numbers)
    elif args.month and args.day and args.hour is not None:
        try:
            validate_month(args.month)
            validate_day(args.day)
            validate_hour(args.hour)
        except ValueError as e:
            parser.error(str(e))
        result = by_month_day_hour(args.month, args.day, args.hour)
    elif args.auto:
        info = get_current_lunar_info()
        result = by_month_day_hour(info['lunar_month'], info['lunar_day'], info['hour'])
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
