#!/usr/bin/env python3
"""
管综199 · 每日题目更新脚本
- 从题库 (data/questions/bank.json) 随机抽取4道逻辑题
- 排除已出过的题目（记录在 data/questions/used_ids.json）
- 覆盖写入 data/questions/today.json
- 每天上午8点由自动化任务调用

⚠️ 题库耗尽时：脚本会清空已出记录并重新抽取，同时输出警告
   请尽快补充新年份真题到 bank.json
"""

import json
import random
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANK_PATH = os.path.join(BASE_DIR, 'data', 'questions', 'bank.json')
USED_PATH = os.path.join(BASE_DIR, 'data', 'questions', 'used_ids.json')
TODAY_PATH = os.path.join(BASE_DIR, 'data', 'questions', 'today.json')

# 每日题目数量
DAILY_COUNT = 4
# 题库剩余预警阈值（道），低于此值时输出警告
WARNING_THRESHOLD = 8


def load_json(path):
    """加载JSON文件"""
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """保存JSON文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_used_ids():
    """加载已出题目ID列表"""
    data = load_json(USED_PATH)
    if data is None:
        return []
    return data.get('used_ids', [])


def save_used_ids(used_ids, reason=''):
    """保存已出题目ID列表"""
    save_json(USED_PATH, {
        'description': '已出过的题目ID，用于避免重复。如需重置请删除此文件或清空used_ids数组。',
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'reset_reason': reason,
        'used_ids': used_ids
    })


def main():
    # 1. 加载题库
    bank = load_json(BANK_PATH)
    if not bank:
        print('❌ 题库文件不存在:', BANK_PATH)
        return False

    all_questions = bank.get('questions', [])
    if not all_questions:
        print('❌ 题库为空，请在 bank.json 中添加题目')
        return False

    # 2. 加载已出题目ID
    used_ids = load_used_ids()

    # 3. 筛选可用题目（排除已出过的）
    available = [q for q in all_questions if q['id'] not in used_ids]

    # 4. 处理题库不足的情况
    if len(available) < DAILY_COUNT:
        print(f'')
        print(f'╔══════════════════════════════════════════════════════════════════╗')
        print(f'║  ⚠️  题库已耗尽！                                           ║')
        print(f'║                                                              ║')
        print(f'║  所有 {len(all_questions)} 道题目均已出过一遍。                        ║')
        print(f'║  已自动清空出题记录，重新从题库抽取。                           ║')
        print(f'║                                                              ║')
        print(f'║  📥 请尽快补充新年份真题到 bank.json：                         ║')
        print(f'║     - 2018年管综逻辑真题（第26-55题，共30道）                  ║')
        print(f'║     - 2019年管综逻辑真题（第26-55题，共30道）                  ║')
        print(f'║     - 2020年管综逻辑真题（第26-55题，共30道）                  ║')
        print(f'║     - 2021年管综逻辑真题（第26-55题，共30道）                  ║')
        print(f'║     - 2023年管综逻辑真题（第26-55题，共30道）                  ║')
        print(f'╚══════════════════════════════════════════════════════════════════╝')
        print(f'')
        used_ids = []
        available = [q for q in all_questions if q['id'] not in used_ids]
        save_used_ids(used_ids, reason='题库耗尽，自动重置')

    # 5. 题库快用完时发出预警
    elif len(available) <= WARNING_THRESHOLD:
        print(f'')
        print(f'⚠️  ⚠️  ⚠️  题库即将耗尽！')
        print(f'   当前剩余可用题目：{len(available)} 道（约 {len(available)//DAILY_COUNT} 天后耗尽）')
        print(f'   请尽快补充新年份真题到 data/questions/bank.json')
        print(f'   需要补充的年份：2018、2019、2020、2021、2023')
        print(f'')

    # 6. 随机抽取
    selected = random.sample(available, DAILY_COUNT)

    # 7. 构建今日题目数据
    today_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'questions': selected
    }

    # 8. 保存今日题目
    save_json(TODAY_PATH, today_data)

    # 9. 更新已出ID列表
    new_used = used_ids + [q['id'] for q in selected]
    save_used_ids(new_used, reason='日常更新')

    # 10. 输出结果
    print(f'✅ 今日题目已更新 ({datetime.now().strftime("%Y-%m-%d")})')
    print(f'   题库总量: {len(all_questions)} 道')
    print(f'   已出数量: {len(new_used)} 道')
    print(f'   剩余可用: {len(all_questions) - len(new_used)} 道')
    print()
    for i, q in enumerate(selected, 1):
        print(f'   {i}. [{q["category"]}] {q["source"]} — {q["id"]}')
    print()
    print(f'   已写入: {TODAY_PATH}')
    print()

    return True


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
