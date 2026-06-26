#!/usr/bin/env python3
"""
饮食记录 Skill - 记录饮食 & 统计脚本 v2
支持全部营养字段：宏量+脂肪酸+矿物质+维生素
用法:
  python record_meal.py --add <json> [--meal breakfast|lunch|dinner|snack] [--date YYYY-MM-DD]
  python record_meal.py --stats [--days N | --from YYYY-MM-DD --to YYYY-MM-DD]
"""
import json
import sys
import os
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
LOG_PATH = os.path.join(SKILL_DIR, 'references', 'meal_log.json')

def load_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def add_meal(foods_data, meal_type='lunch', date_str=None, note=''):
    """添加一餐饮食记录（全部营养字段）"""
    log = load_log()

    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # 定义所有营养字段
    nutrient_keys = [
        # 宏量
        'energy_kcal', 'protein_g', 'fat_g', 'carbs_g', 'fiber_g',
        # 脂肪酸
        'saturated_fat_g', 'monounsaturated_fat_g', 'polyunsaturated_fat_g', 'trans_fat_g',
        # 矿物质
        'calcium_mg', 'magnesium_mg', 'sodium_mg', 'potassium_mg', 'phosphorus_mg',
        'iron_mg', 'zinc_mg', 'selenium_mg', 'copper_mg', 'manganese_mg',
        # 维生素
        'vitamin_a_mcg', 'vitamin_c_mg', 'vitamin_d_mcg', 'vitamin_e_mg', 'vitamin_k_mcg',
        'vitamin_b1_mg', 'vitamin_b2_mg', 'vitamin_b3_mg', 'vitamin_b5_mg',
        'vitamin_b6_mg', 'vitamin_b7_mcg', 'vitamin_b9_mcg', 'vitamin_b12_mcg',
    ]

    # 初始化总计
    total = {k: 0.0 for k in nutrient_keys}

    for food in foods_data:
        for key in nutrient_keys:
            total[key] += food.get(key, 0.0)

    # 四舍五入
    total = {k: round(v, 2) for k, v in total.items()}

    entry = {
        'date': date_str,
        'meal': meal_type,
        'foods': foods_data,
        'total': total,
        'note': note
    }

    log.append(entry)
    save_log(log)

    return entry

def get_stats(days=7, from_date=None, to_date=None):
    """获取阶段性营养统计"""
    log = load_log()

    if from_date and to_date:
        start = datetime.strptime(from_date, '%Y-%m-%d')
        end = datetime.strptime(to_date, '%Y-%m-%d')
    else:
        end = datetime.now()
        start = end - timedelta(days=days - 1)

    # 筛选日期范围内的记录
    filtered = []
    for entry in log:
        try:
            d = datetime.strptime(entry['date'], '%Y-%m-%d')
            if start <= d <= end:
                filtered.append(entry)
        except:
            continue

    nutrient_keys = [
        'energy_kcal', 'protein_g', 'fat_g', 'carbs_g', 'fiber_g',
        'saturated_fat_g', 'monounsaturated_fat_g', 'polyunsaturated_fat_g', 'trans_fat_g',
        'calcium_mg', 'magnesium_mg', 'sodium_mg', 'potassium_mg', 'phosphorus_mg',
        'iron_mg', 'zinc_mg', 'selenium_mg',
        'vitamin_a_mcg', 'vitamin_c_mg', 'vitamin_e_mg',
        'vitamin_b1_mg', 'vitamin_b2_mg', 'vitamin_b3_mg', 'vitamin_b9_mcg', 'vitamin_b12_mcg',
    ]

    if not filtered:
        return {
            'period': f'{start.strftime("%Y-%m-%d")} ~ {end.strftime("%Y-%m-%d")}',
            'days': 0,
            'total': {k: 0 for k in nutrient_keys},
            'daily_avg': {k: 0 for k in nutrient_keys},
            'daily': []
        }

    # 按日汇总
    daily_data = {}
    for entry in filtered:
        d = entry['date']
        if d not in daily_data:
            daily_data[d] = {k: 0.0 for k in nutrient_keys}
        t = entry['total']
        for k in nutrient_keys:
            daily_data[d][k] += t.get(k, 0)

    num_days = len(daily_data)

    # 总计
    total_all = {k: round(sum(v[k] for v in daily_data.values()), 2) for k in nutrient_keys}
    daily_avg = {k: round(total_all[k] / num_days, 2) for k in nutrient_keys}

    return {
        'period': f'{start.strftime("%Y-%m-%d")} ~ {end.strftime("%Y-%m-%d")}',
        'days': num_days,
        'total': total_all,
        'daily_avg': daily_avg,
        'daily': [{'date': d, ** {k: round(v, 2) for k, v in row.items()}} for d, row in sorted(daily_data.items())]
    }

def main():
    if len(sys.argv) < 2:
        print('用法:')
        print('  添加: python record_meal.py --add <json> [--meal lunch] [--date 2026-04-14]')
        print('  统计: python record_meal.py --stats [--days 7]')
        sys.exit(1)

    args = sys.argv[1:]
    action = args[0]

    if action == '--add':
        meal_type = 'lunch'
        date_str = None
        note = ''
        foods_json = None

        i = 1
        while i < len(args):
            if args[i] == '--meal' and i + 1 < len(args):
                meal_type = args[i + 1]; i += 2
            elif args[i] == '--date' and i + 1 < len(args):
                date_str = args[i + 1]; i += 2
            elif args[i] == '--note' and i + 1 < len(args):
                note = args[i + 1]; i += 2
            elif not args[i].startswith('--'):
                foods_json = args[i]; i += 1
            else:
                i += 1

        if not foods_json:
            print(json.dumps({'error': '缺少 foods JSON'}, ensure_ascii=False))
            sys.exit(1)

        try:
            foods_data = json.loads(foods_json)
        except:
            print(json.dumps({'error': f'无法解析 JSON'}, ensure_ascii=False))
            sys.exit(1)

        entry = add_meal(foods_data, meal_type, date_str, note)
        print(json.dumps({'status': 'ok', 'entry': entry}, ensure_ascii=False, indent=2))

    elif action == '--stats':
        days = 7
        from_date = None
        to_date = None

        i = 1
        while i < len(args):
            if args[i] == '--days' and i + 1 < len(args):
                days = int(args[i + 1]); i += 2
            elif args[i] == '--from' and i + 1 < len(args):
                from_date = args[i + 1]; i += 2
            elif args[i] == '--to' and i + 1 < len(args):
                to_date = args[i + 1]; i += 2
            else:
                i += 1

        stats = get_stats(days=days, from_date=from_date, to_date=to_date)
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    else:
        print(json.dumps({'error': f'未知操作: {action}'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
