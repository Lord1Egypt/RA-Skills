#!/usr/bin/env python3
"""
Fitness Daily — 30 岁青年健身自律打卡器
=========================================

一位 30 岁青年把坚持多年的每日健身习惯固化为打卡清单并共享出来。
四组 15 项：身体活动 / 营养与恢复 / 心理与习惯 / 纪律底线。
勾选今日完成项 → 完成率 → 状态判定 → 下周重点建议。

用法:
    python3 fitness.py check            # 交互式勾选今日打卡
    python3 fitness.py check --done f1,f3,f5   # 直接传已完成项
    python3 fitness.py report            # 生成今日报告
    python3 fitness.py report --date 2026-08-13
    python3 fitness.py trend             # 多日完成率趋势
    python3 fitness.py summary           # 一句话摘要

数据:
    默认保存到 ~/.fitness-daily.csv（每行一天：date,f1..f15，1=完成 0=未完成）
    可用 --log <文件> 指定其他记录文件

说明:
    本 Skill 为非认证众包内容，代表共享者个人的好习惯 / 好做法，仅供参考，
    不构成医疗、营养等专业建议。涉及健康问题请以专业人员意见为准。
"""

import argparse
import csv
import os
import sys
from collections import OrderedDict

# ──────────────────────────────────────────────
# 检查项定义（4 组 15 项）
# ──────────────────────────────────────────────

GROUPS = OrderedDict([
    ('身体活动', [
        ('f1',  '完成 30 分钟中高强度运动', '跑步、骑行、力量训练、游泳均可'),
        ('f2',  '步数 ≥ 8,000 步', '手机或手表记录'),
        ('f3',  '拉伸或放松 10 分钟', '训练前后各 5 分钟'),
    ]),
    ('营养与恢复', [
        ('f4',  '饮水 ≥ 2 升', '约 8 杯水'),
        ('f5',  '蛋白质摄入达标', '每公斤体重 ≥ 1.2g'),
        ('f6',  '蔬菜占一餐一半', '午餐或晚餐'),
        ('f7',  '无深夜进食', '睡前 3 小时不进食'),
        ('f8',  '睡眠 7–9 小时', '实际入睡时长'),
    ]),
    ('心理与习惯', [
        ('f9',  '冥想或深呼吸 5 分钟', '正念、呼吸练习均可'),
        ('f10', '娱乐屏幕时间 ≤ 2 小时', '社交/短视频/游戏'),
        ('f11', '记录今日健康日志', '体重、心情、训练备注'),
        ('f12', '阅读健康相关内容 15 分钟', '营养、训练、恢复'),
    ]),
    ('纪律底线', [
        ('f13', '未饮酒或适量', '不超过 1 个标准杯'),
        ('f14', '未久坐超 1 小时不动', '每小时起身活动 2 分钟'),
        ('f15', '按计划执行，无借口拖延', '当日打卡不隔夜'),
    ]),
])

TOTAL_ITEMS = 15
ITEM_IDS = [iid for _, items in GROUPS.items() for iid, _, _ in items]
GROUP_NAMES = list(GROUPS.keys())

# 分组建议（用于生成下周重点）
GROUP_SUGGEST = {
    '身体活动': '把「30 分钟中高强度运动」绑定到固定时段（如早起或午休），拉伸放进训练后 5 分钟，更容易坚持。',
    '营养与恢复': '把「23 点前熄灯」设成手机自动提醒；蔬菜用「每餐先盛半盘」的笨办法保证；睡眠不足会拖垮第二天所有项。',
    '心理与习惯': '靠微习惯堆叠：冥想 5 分钟放进起床后第一件事，健康日志用一句话模板（体重/心情/备注）降低门槛。',
    '纪律底线': '底线项是「不允许妥协」的。把「不隔夜打卡」和「每小时起身」设成手机定时闹钟，让底线自己提醒你。',
}

HINT_MAP = {iid: hint for _, items in GROUPS.items() for iid, _, hint in items}
LABEL_MAP = {iid: label for _, items in GROUPS.items() for iid, label, _ in items}


# ──────────────────────────────────────────────
# 状态判定
# ──────────────────────────────────────────────

def judge_status(rate):
    """根据完成率判定状态"""
    if rate >= 0.9:
        return '自律达人', '保持节奏，重点巩固相对弱的维度'
    elif rate >= 0.75:
        return '状态良好', '整体在轨道上，补上漏掉的 1-2 项即可冲 90%'
    elif rate >= 0.6:
        return '及格线上', '完成过半，先守住纪律底线项，再逐项补强'
    else:
        return '需要加强', '别贪多，明天从「身体活动 3 项 + 纪律底线 3 项」开始'


# ──────────────────────────────────────────────
# 数据读写
# ──────────────────────────────────────────────

def default_log_path():
    return os.path.join(os.path.expanduser('~'), '.fitness-daily.csv')


def load_log(filepath):
    """读取打卡记录，返回 {date: {item_id: 0/1}}"""
    log = {}
    if not os.path.exists(filepath):
        return log
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row.get('date', '').strip()
            if not date:
                continue
            entry = {}
            for iid in ITEM_IDS:
                v = row.get(iid, '0').strip()
                entry[iid] = 1 if v in ('1', 'true', 'TRUE', '是', 'y', 'Y') else 0
            log[date] = entry
    return log


def save_log(filepath, log):
    """写回打卡记录"""
    parent = os.path.dirname(filepath)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date'] + ITEM_IDS)
        writer.writeheader()
        for date in sorted(log.keys()):
            row = {'date': date}
            row.update({iid: log[date].get(iid, 0) for iid in ITEM_IDS})
            writer.writerow(row)


# ──────────────────────────────────────────────
# 核心计算
# ──────────────────────────────────────────────

def analyze_day(entry):
    """分析单日打卡：完成率 + 分组明细 + 状态"""
    done = sum(1 for iid in ITEM_IDS if entry.get(iid, 0) == 1)
    rate = done / TOTAL_ITEMS
    status, status_note = judge_status(rate)

    dims = OrderedDict()
    for gname, items in GROUPS.items():
        g_done = sum(1 for iid, _, _ in items if entry.get(iid, 0) == 1)
        g_total = len(items)
        dims[gname] = {
            'done': g_done,
            'total': g_total,
            'rate': g_done / g_total if g_total else 0,
            'missing': [iid for iid, _, _ in items if entry.get(iid, 0) != 1],
        }

    # 底线检查：纪律底线任一未完成 → 提示
    bottom = dims['纪律底线']
    bottom_breach = [iid for iid in bottom['missing']]

    # 下周重点建议：从未完成维度提取
    suggestions = []
    for gname in GROUP_NAMES:
        if dims[gname]['missing']:
            suggestions.append(f"{gname}：{GROUP_SUGGEST[gname]}")
    if not suggestions:
        suggestions = ['今日全项达成，保持当前节奏即可']

    result = OrderedDict([
        ('done', done),
        ('total', TOTAL_ITEMS),
        ('rate', round(rate * 100, 1)),
        ('status', status),
        ('status_note', status_note),
        ('dimensions', dims),
        ('bottom_breach', bottom_breach),
        ('suggestions', suggestions),
    ])
    return result


# ──────────────────────────────────────────────
# 交互式打卡
# ──────────────────────────────────────────────

def interactive_check():
    """逐项询问，返回 entry"""
    entry = {}
    print('逐项打卡（y=完成 / n=未完成 / 直接回车=未完成）\n')
    for gname, items in GROUPS.items():
        print(f"── {gname} ──")
        for iid, label, hint in items:
            while True:
                raw = input(f"  {label} [{hint}] (y/n): ").strip().lower()
                if raw in ('y', 'yes', '是', '1'):
                    entry[iid] = 1
                    break
                elif raw in ('', 'n', 'no', '否', '0'):
                    entry[iid] = 0
                    break
                else:
                    print('  请输入 y 或 n')
    return entry


# ──────────────────────────────────────────────
# 输出渲染
# ──────────────────────────────────────────────

def render_report(result, date_str, log_path):
    print("═" * 55)
    print(f"  每日健身纪律 — 今日追踪报告")
    print("═" * 55)
    print(f"  日期:       {date_str}")
    print(f"  完成率:     {result['done']}/{result['total']} ({result['rate']}%)")
    print(f"  状态:       {result['status']}")
    print(f"  建议:       {result['status_note']}")
    print()
    print("  ── 分组明细 ──")
    for gname in GROUP_NAMES:
        d = result['dimensions'][gname]
        bar_len = int(d['rate'] * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"  {gname} [{bar}] {d['done']}/{d['total']}")
        if d['missing']:
            miss_names = ', '.join(LABEL_MAP[iid] for iid in d['missing'])
            print(f"     未完成: {miss_names}")
    if result['bottom_breach']:
        print()
        print(f"  ⚠ 纪律底线未守住: {', '.join(LABEL_MAP[i] for i in result['bottom_breach'])}")
    print()
    print("  ── 下周重点建议 ──")
    for s in result['suggestions']:
        print(f"  • {s}")
    print("═" * 55)
    print(f"  记录文件: {log_path}")


def render_trend(rows):
    print("═" * 50)
    print(f"  健身纪律趋势（{len(rows)} 天）")
    print("═" * 50)
    print(f"  {'日期':<12} {'完成率':<8} {'状态':<8} 趋势")
    print("  " + "─" * 40)
    for i, (date, result) in enumerate(rows):
        arrow = ''
        if i > 0:
            diff = result['rate'] - rows[i-1][1]['rate']
            if diff >= 10:
                arrow = '↑↑'
            elif diff >= 1:
                arrow = '↑'
            elif diff <= -10:
                arrow = '↓↓'
            elif diff <= -1:
                arrow = '↓'
            else:
                arrow = '→'
        print(f"  {date:<12} {result['rate']:<8} {result['status']:<8} {arrow}")
    if rows:
        first, last = rows[0][1], rows[-1][1]
        diff = last['rate'] - first['rate']
        if diff > 0:
            w = f"上升 {diff:.1f} 分"
        elif diff < 0:
            w = f"下降 {abs(diff):.1f} 分"
        else:
            w = "持平"
        print()
        print(f"  趋势: {first['rate']}% → {last['rate']}%, {w}")
        print(f"  状态: {first['status']} → {last['status']}")
    print("═" * 50)


# ──────────────────────────────────────────────
# 命令处理
# ──────────────────────────────────────────────

def cmd_check(args):
    """check — 今日打卡"""
    if args.done:
        entry = {iid: 0 for iid in ITEM_IDS}
        for token in args.done.split(','):
            token = token.strip().lower()
            if token in ITEM_IDS:
                entry[token] = 1
            else:
                print(f"  警告: 未知检查项 {token}，忽略")
    else:
        entry = interactive_check()

    log_path = args.log or default_log_path()
    log = load_log(log_path)
    today = args.date
    log[today] = entry
    save_log(log_path, log)
    print(f"\n✓ 已记录 {today} 的打卡到 {log_path}\n")

    result = analyze_day(entry)
    render_report(result, today, log_path)
    return result


def cmd_report(args):
    """report — 生成报告（默认最新一天）"""
    log_path = args.log or default_log_path()
    log = load_log(log_path)
    if not log:
        print("还没有打卡记录。先运行: python3 fitness.py check")
        sys.exit(1)
    date = args.date or sorted(log.keys())[-1]
    if date not in log:
        print(f"错误: {date} 没有记录。可用日期: {', '.join(sorted(log.keys()))}")
        sys.exit(1)
    result = analyze_day(log[date])
    render_report(result, date, log_path)
    return result


def cmd_trend(args):
    """trend — 多日趋势"""
    log_path = args.log or default_log_path()
    log = load_log(log_path)
    if not log:
        print("还没有打卡记录。先运行: python3 fitness.py check")
        sys.exit(1)
    rows = [(date, analyze_day(log[date])) for date in sorted(log.keys())]
    render_trend(rows)


def cmd_summary(args):
    """summary — 一句话摘要"""
    log_path = args.log or default_log_path()
    log = load_log(log_path)
    if not log:
        print("还没有打卡记录。先运行: python3 fitness.py check")
        sys.exit(1)
    date = args.date or sorted(log.keys())[-1]
    if date not in log:
        print(f"错误: {date} 没有记录")
        sys.exit(1)
    result = analyze_day(log[date])
    print(f"🏋️ {date} | 健身自律 {result['status']} ({result['rate']}%)")
    print(f"   完成 {result['done']}/{result['total']} 项。")
    if result['bottom_breach']:
        print(f"   ⚠ 底线未守: {', '.join(LABEL_MAP[i] for i in result['bottom_breach'])}")
    print(f"   [下周重点] {result['suggestions'][0]}")


# ──────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='🏋️ Fitness Daily — 30 岁青年健身自律打卡器（非认证众包 · 好习惯共享）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 fitness.py check                     # 交互式打卡
    python3 fitness.py check --done f1,f3,f5     # 直接传已完成项
    python3 fitness.py report                    # 今日报告
    python3 fitness.py report --date 2026-08-13
    python3 fitness.py trend                     # 多日趋势
    python3 fitness.py summary                   # 一句话摘要

免责声明:
    本 Skill 为非认证众包内容，代表共享者个人的好习惯 / 好做法，仅供参考，
    不构成医疗、营养等专业建议。涉及健康问题请以专业人员意见为准。
        """
    )
    parser.add_argument('command', nargs='?', default='report',
                        choices=['check', 'report', 'trend', 'summary'],
                        help='子命令: check, report, trend, summary (默认 report)')
    parser.add_argument('--done', help='已完成项，逗号分隔，如 f1,f3,f5（配合 check）')
    parser.add_argument('--date', '-d', default=None,
                        help='日期 YYYY-MM-DD（默认今天 / 最新一天）')
    parser.add_argument('--log', '-l', default=None,
                        help='打卡记录文件路径（默认 ~/.fitness-daily.csv）')

    args = parser.parse_args()
    args.date = args.date or __import__('datetime').date.today().isoformat()

    commands = {
        'check': cmd_check,
        'report': cmd_report,
        'trend': cmd_trend,
        'summary': cmd_summary,
    }
    commands[args.command](args)


if __name__ == '__main__':
    main()
