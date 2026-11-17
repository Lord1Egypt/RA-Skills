#!/usr/bin/env python3
"""
福彩全玩法号码筛选分析工具
用法:
  python ssq_analyzer.py --type <玩法> --analyze
  python ssq_analyzer.py --type <玩法> --generate
  python ssq_analyzer.py --type <玩法> --query <期号>
  python ssq_analyzer.py --type <玩法> --latest

玩法: ssq(双色球), fc3d(福彩3D), qlc(七乐彩), kl8(快乐8), df61(东方6+1), 15x5(15选5)
"""

import csv
import sys
import os
import random
from collections import Counter

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'references')

GAMES = {
    'ssq': {
        'name': '双色球', 'pools': {'main': (1, 33), 'bonus': (1, 16)},
        'pick': 6, 'file': 'ssq-history.csv',
        'fields': ['红球1','红球2','红球3','红球4','红球5','红球6','蓝球','日期'],
        'prime': [2,3,5,7,11,13,17,19,23,29,31], 'sum_range': (21, 183)
    },
    'fc3d': {
        'name': '福彩3D', 'pools': {'bai': (0, 9), 'shi': (0, 9), 'ge': (0, 9)},
        'pick': 3, 'file': 'fc3d-history.csv',
        'fields': ['期号','百位','十位','个位','和值','跨度','日期'],
        'sum_range': (0, 27)
    },
    'qlc': {
        'name': '七乐彩', 'pools': {'main': (1, 30)},
        'pick': 7, 'file': 'qlc-history.csv',
        'fields': ['期号','号码1','号码2','号码3','号码4','号码5','号码6','号码7','特别号','日期'],
        'prime': [2,3,5,7,11,13,17,19,23,29], 'sum_range': (28, 189)
    },
    'kl8': {
        'name': '快乐8', 'pools': {'main': (1, 80)},
        'pick': 20, 'file': 'kl8-history.csv',
        'fields': ['期号'] + [f'号码{i}' for i in range(1, 21)] + ['日期'],
        'sum_range': (210, 1410)
    },
    'df61': {
        'name': '东方6+1', 'pools': {'digits': (0, 9), 'zodiac': list(range(1, 13))},
        'pick': 6, 'file': 'df61-history.csv',
        'fields': ['期号','数字1','数字2','数字3','数字4','数字5','数字6','生肖','日期'],
    },
    '15x5': {
        'name': '15选5', 'pools': {'main': (1, 15)},
        'pick': 5, 'file': '15x5-history.csv',
        'fields': ['期号','号码1','号码2','号码3','号码4','号码5','日期'],
        'prime': [2,3,5,7,11,13], 'sum_range': (15, 65)
    },
}

ZODIACS = ['鼠','牛','虎','兔','龙','蛇','马','羊','猴','鸡','狗','猪']


def get_game(gtype):
    return GAMES.get(gtype, GAMES['ssq'])


def history_file(gtype):
    return os.path.join(DATA_DIR, get_game(gtype)['file'])


def load_history(gtype='ssq'):
    path = history_file(gtype)
    if not os.path.exists(path):
        print(f"⚠️ 数据文件不存在: {path}")
        return []
    game = get_game(gtype)
    rows = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            row = {'phase': r['期号'], 'date': r.get('日期', '')}
            if gtype == 'ssq':
                row['numbers'] = sorted([int(r[f'红球{i}']) for i in range(1, 7)])
                row['bonus'] = int(r['蓝球'])
            elif gtype == 'fc3d':
                row['numbers'] = [int(r['百位']), int(r['十位']), int(r['个位'])]
            elif gtype == 'qlc':
                row['numbers'] = sorted([int(r[f'号码{i}']) for i in range(1, 8)])
                row['bonus'] = int(r['特别号']) if '特别号' in r else 0
            elif gtype == 'kl8':
                row['numbers'] = sorted([int(r[f'号码{i}']) for i in range(1, 21)])
            elif gtype == 'df61':
                row['numbers'] = [int(r[f'数字{i}']) for i in range(1, 7)]
                zodiac_idx = int(r['生肖'])
                row['bonus'] = ZODIACS[zodiac_idx - 1] if 1 <= zodiac_idx <= 12 else r['生肖']
            elif gtype == '15x5':
                row['numbers'] = sorted([int(r[f'号码{i}']) for i in range(1, 6)])
            rows.append(row)
    return rows


def analyze(gtype='ssq'):
    data = load_history(gtype)
    if not data:
        return
    game = get_game(gtype)
    print(f"## {game['name']} 冷热号分析")
    print(f"分析期数: {len(data)}")

    all_nums = []
    all_bonus = []
    for r in data:
        all_nums.extend(r['numbers'])
        if 'bonus' in r:
            all_bonus.append(r['bonus'])

    counter = Counter(all_nums)
    print(f"\n热号 TOP10: {', '.join(f'{n}({c}次)' for n, c in counter.most_common(10))}")
    cold = counter.most_common()[-11:-1]
    print(f"冷号 TOP10: {', '.join(f'{n}({c}次)' for n, c in cold if c > 0)}")

    if all_bonus:
        bonus_counter = Counter(all_bonus)
        print(f"\n蓝球/特别号热号: {', '.join(f'{n}({c}次)' for n, c in bonus_counter.most_common(5))}")

    if gtype == 'fc3d':
        bai = Counter(r['numbers'][0] for r in data)
        shi = Counter(r['numbers'][1] for r in data)
        ge = Counter(r['numbers'][2] for r in data)
        print(f"\n百位热号: {', '.join(f'{n}({c}次)' for n, c in bai.most_common(5))}")
        print(f"十位热号: {', '.join(f'{n}({c}次)' for n, c in shi.most_common(5))}")
        print(f"个位热号: {', '.join(f'{n}({c}次)' for n, c in ge.most_common(5))}")
        sums = [sum(r['numbers']) for r in data]
        sum_counter = Counter(sums)
        print(f"\n和值热号: {', '.join(f'{n}({c}次)' for n, c in sum_counter.most_common(5))}")

    if gtype == 'kl8':
        sections = [sum(1 for n in r['numbers'] if 1 <= n <= 20) for r in data]
        s2 = [sum(1 for n in r['numbers'] if 21 <= n <= 40) for r in data]
        s3 = [sum(1 for n in r['numbers'] if 41 <= n <= 60) for r in data]
        s4 = [sum(1 for n in r['numbers'] if 61 <= n <= 80) for r in data]
        print(f"\n四分区平均: 一区({sum(sections)/len(sections):.0f}) "
              f"二区({sum(s2)/len(s2):.0f}) 三区({sum(s3)/len(s3):.0f}) "
              f"四区({sum(s4)/len(s4):.0f})")


def generate(gtype='ssq', count=5):
    data = load_history(gtype)
    game = get_game(gtype)

    if data:
        all_nums = []
        for r in data:
            all_nums.extend(r['numbers'])
        pool = [n for n, _ in Counter(all_nums).most_common(max(15, game['pick'] * 2))]
    else:
        print("⚠️ 无历史数据，使用随机生成")
        if gtype == 'ssq':
            pool = list(range(1, 34))
        elif gtype == 'qlc':
            pool = list(range(1, 31))
        elif gtype == 'kl8':
            pool = list(range(1, 81))
        elif gtype == '15x5':
            pool = list(range(1, 16))
        elif gtype == 'fc3d':
            pool = list(range(0, 10))
        elif gtype == 'df61':
            pool = list(range(0, 10))
        else:
            pool = list(range(1, 34))

    print(f"## {game['name']} 推荐方案")
    results = []
    pick = game['pick']
    if gtype == 'kl8':
        pick = 5

    attempts = 0
    while len(results) < count and attempts < 200:
        attempts += 1
        if len(pool) >= pick:
            nums = sorted(random.sample(pool, pick))
        else:
            nums = sorted(random.sample(list(range(1, max(pool)+1)), pick))
        if gtype == 'ssq' and 1 <= nums[-1] <= 16:
            continue
        s = sum(nums)
        if gtype == 'ssq' and not (70 <= s <= 170):
            continue
        if gtype == 'fc3d' and not (4 <= s <= 23):
            continue
        results.append(nums)

    print()
    if gtype == 'ssq':
        print(f"{'方案':<4} {'红球':<20} {'蓝球':<6} {'和值':<6} {'跨度':<6}")
        print("-" * 50)
        for i, nums in enumerate(results, 1):
            blue = random.choice(range(1, 17))
            span = max(nums) - min(nums)
            print(f"{i:<4} {' '.join(f'{n:02d}' for n in nums):<20} {blue:02d}{'':>4} {sum(nums):<6} {span:<6}")
    elif gtype == 'fc3d':
        print(f"{'方案':<4} {'百位':<6} {'十位':<6} {'个位':<6} {'和值':<6} {'跨度':<6}")
        print("-" * 40)
        for i, nums in enumerate(results, 1):
            b, s, g = nums[0], nums[1] if len(nums) > 1 else random.randint(0,9), nums[2] if len(nums) > 2 else random.randint(0,9)
            span = max(b, s, g) - min(b, s, g)
            print(f"{i:<4} {b:<6} {s:<6} {g:<6} {b+s+g:<6} {span:<6}")
    elif gtype == 'df61':
        print(f"{'方案':<4} {'数字位':<20} {'生肖':<6}")
        print("-" * 50)
        for i, nums in enumerate(results, 1):
            zodiac = ZODIACS[random.randint(0, 11)]
            print(f"{i:<4} {' '.join(str(n) for n in nums):<20} {zodiac:<6}")
    elif gtype == 'kl8':
        print(f"{'方案':<4} {'号码':<40}")
        print("-" * 50)
        for i, nums in enumerate(results, 1):
            print(f"{i:<4} {' '.join(f'{n:02d}' for n in nums):<40}")
    else:
        print(f"{'方案':<4} {'号码':<30} {'和值':<6}")
        print("-" * 50)
        for i, nums in enumerate(results, 1):
            print(f"{i:<4} {' '.join(f'{n:02d}' for n in nums):<30} {sum(nums):<6}")


def query(gtype='ssq', phase=None):
    data = load_history(gtype)
    if not data:
        print("⚠️ 无数据")
        return
    game = get_game(gtype)
    if phase:
        for r in data:
            if r['phase'] == phase:
                _print_result(game, gtype, r)
                return
        print(f"⚠️ 未找到期号 {phase}")
    else:
        _print_result(game, gtype, data[-1])


def _print_result(game, gtype, r):
    print(f"## {game['name']} {r['phase']} 期开奖结果")
    print(f"日期: {r['date']}")
    nums = r['numbers']
    if gtype == 'ssq':
        print(f"红球: {' '.join(f'{n:02d}' for n in nums)} | 蓝球: {r['bonus']:02d}")
        print(f"和值: {sum(nums)} | 跨度: {max(nums)-min(nums)}")
    elif gtype == 'fc3d':
        print(f"号码: {' '.join(str(n) for n in nums)}")
        print(f"和值: {sum(nums)} | 跨度: {max(nums)-min(nums)}")
    elif gtype == 'qlc':
        print(f"号码: {' '.join(f'{n:02d}' for n in nums)} | 特别号: {r.get('bonus','')}")
    elif gtype == 'kl8':
        print(f"号码(20个): {' '.join(f'{n:02d}' for n in nums)}")
    elif gtype == 'df61':
        print(f"数字: {' '.join(str(n) for n in nums)} | 生肖: {r.get('bonus','')}")
    elif gtype == '15x5':
        print(f"号码: {' '.join(f'{n:02d}' for n in nums)}")
        print(f"和值: {sum(nums)} | 跨度: {max(nums)-min(nums)}")


def usage():
    print("用法:")
    print("  python ssq_analyzer.py --type <玩法> --analyze")
    print("  python ssq_analyzer.py --type <玩法> --generate")
    print("  python ssq_analyzer.py --type <玩法> --query <期号>")
    print("  python ssq_analyzer.py --type <玩法> --latest")
    print("  玩法: ssq(双色球) fc3d(福彩3D) qlc(七乐彩) kl8(快乐8) df61(东方6+1) 15x5(15选5)")


if __name__ == '__main__':
    gtype = 'ssq'
    if '--type' in sys.argv:
        idx = sys.argv.index('--type')
        if idx + 1 < len(sys.argv):
            gtype = sys.argv[idx + 1]
    if gtype not in GAMES:
        print(f"❌ 未知玩法: {gtype}")
        usage()
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    if '--analyze' in sys.argv:
        analyze(gtype)
    elif '--query' in sys.argv:
        idx = sys.argv.index('--query')
        phase = sys.argv[idx + 1] if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith('--') else None
        query(gtype, phase)
    elif '--latest' in sys.argv:
        query(gtype)
    elif '--generate' in sys.argv:
        generate(gtype)
    else:
        usage()
