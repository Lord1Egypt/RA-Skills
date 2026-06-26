#!/usr/bin/env python3
"""
父母的功课 - 可视化追踪
ASCII艺术显示情绪和连接趋势

用法:

⚠️ 安全禁用：此脚本执行文件读取操作，仅在明确需要时启用。
启用方式：设置环境变量 ALLOW_FILE_PERSISTENCE=1
"""
import os
if not os.environ.get("ALLOW_FILE_PERSISTENCE"):
    print("❌ 文件持久化功能已禁用。如需启用，请设置 ALLOW_FILE_PERSISTENCE=1")
    exit(0)
    python3 scripts/visualize.py --mood 7       # 最近7天情绪趋势
    python3 scripts/visualize.py --stress 30   # 最近30天压力趋势
    python3 scripts/visualize.py --dashboard    # 综合仪表盘
    python3 scripts/visualize.py --connection   # 连接时刻追踪
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"


def load_mood():
    f = DATA_DIR / "mood_log.json"
    if not f.exists():
        return []
    try:
        with open(f) as fp:
            return json.load(fp)
    except (json.JSONDecodeError, IOError):
        return []


def load_assessment():
    f = DATA_DIR / "assessment_history.json"
    if not f.exists():
        return []
    try:
        with open(f) as fp:
            return json.load(fp)
    except (json.JSONDecodeError, IOError):
        return []


def mood_bar(score, width=20):
    """将0-10分数渲染为ASCII条形图"""
    filled = int((score / 10) * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar


def mood_emoji(score):
    """将分数转换为emoji"""
    if score >= 8: return "○"      # 平静
    elif score >= 6: return "◇"   # 略好
    elif score >= 4: return "◈"   # 一般
    elif score >= 2: return "◆"   # 低
    else: return "●"               # 崩溃


def mood_label(score):
    if score >= 8: return "平静"
    elif score >= 6: return "略好"
    elif score >= 4: return "一般"
    elif score >= 2: return "低落"
    else: return "崩溃"


def show_mood_trend(days=7):
    """显示情绪趋势"""
    entries = load_mood()
    if not entries:
        print("暂无情绪数据。使用 parenting_tracker.py --log 记录。")
        return

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e['date'] >= cutoff]

    if not recent:
        print(f"最近{days}天没有情绪数据。")
        return

    # 按日期分组
    by_date = defaultdict(list)
    for e in recent:
        by_date[e['date']].append(e['score'])

    # 生成日期列表
    dates = sorted(by_date.keys())

    print(f"\n{'='*60}")
    print(f"情绪趋势 (最近{days}天)")
    print(f"{'='*60}")
    print()

    for date in dates:
        scores = by_date[date]
        avg = sum(scores) / len(scores)
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d")
        bar = mood_bar(avg)
        emoji = mood_emoji(avg)

        # 显示每日情绪点
        points = " ".join(mood_emoji(s) for s in scores)

        print(f"  {day_name} | {bar} {emoji}{avg:.1f}/10  ({points})")

    # 总体趋势
    all_scores = [e['score'] for e in recent]
    overall = sum(all_scores) / len(all_scores)
    low_days = sum(1 for s in all_scores if s <= 3)
    high_days = sum(1 for s in all_scores if s >= 7)

    print(f"\n  总体: {overall:.1f}/10  低压日:{low_days}  高压日:{high_days}")
    print(f"{'='*60}")


def show_stress_trend(days=30):
    """显示压力评估趋势"""
    history = load_assessment()
    if not history:
        print("暂无评估数据。使用 assessment.py --all 记录。")
        return

    stress = [e for e in history if e['type'] == 'stress' and e['date'] >= (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")]

    if not stress:
        print(f"最近{days}天没有压力评估数据。")
        return

    stress.sort(key=lambda x: x['date'])

    print(f"\n{'='*60}")
    print(f"压力趋势 (最近{days}天)")
    print(f"{'='*60}")
    print()

    for e in stress:
        d = datetime.strptime(e['date'], "%Y-%m-%d").strftime("%m-%d")
        total = e['total']
        max_score = e['max']
        pct = total / max_score * 100
        bar = mood_bar(10 - pct / 10)  # 反向：压力高则条短

        if pct <= 40:
            level = "正常"
        elif pct <= 68:
            level = "轻度"
        else:
            level = "中度"

        print(f"  {d} | {bar} {level} ({total}/{max_score})")

    print(f"{'='*60}")


def show_dashboard():
    """综合仪表盘"""
    mood_entries = load_mood()
    assess_entries = load_assessment()

    today = datetime.now().strftime("%Y-%m-%d")
    recent_mood = [e for e in mood_entries if e['date'] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")]
    recent_stress = [e for e in assess_entries if e['type'] == 'stress' and e['date'] >= (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")]

    print(f"""
╔══════════════════════════════════════════════════════════╗
║       父母的功课 - 父母状态仪表盘     {today:<17}║
╚══════════════════════════════════════════════════════════╝
""")

    # 情绪状态
    if recent_mood:
        scores = [e['score'] for e in recent_mood]
        avg = sum(scores) / len(scores)
        bar = mood_bar(avg)
        emoji = mood_emoji(avg)

        print(f"  情绪状态 (7天)")
        print(f"  {bar} {emoji}{avg:.1f}/10")
        print(f"  今日记录: {len([e for e in recent_mood if e['date'] == today])}条")
    else:
        print(f"  情绪状态: 无数据 (使用 --log 记录)")

    print()

    # 压力状态
    if recent_stress:
        latest = recent_stress[-1]
        total, max_s = latest['total'], latest['max']
        pct = total / max_s * 100
        if pct <= 40:
            level, bar_color = "正常", "░"
        elif pct <= 68:
            level, bar_color = "轻度", "▒"
        else:
            level, bar_color = "中度", "▓"
        bar = mood_bar(10 - pct / 10)
        print(f"  压力状态 (最近评估)")
        print(f"  {bar} {level} ({total}/{max_s})")
        print(f"  评估日期: {latest['date']}")
    else:
        print(f"  压力状态: 无数据 (使用 --stress 评估)")

    print()

    # 连接时刻
    if recent_mood:
        repairs = [e for e in recent_mood if e.get('repair') and e['repair'] not in ('否', '未', '未记录')]
        repair_rate = len(repairs) / len(recent_mood) * 100 if recent_mood else 0
        repair_bar = "█" * int(repair_rate / 5) + "░" * (20 - int(repair_rate / 5))
        print(f"  事后修复率 (7天)")
        print(f"  {repair_bar} {repair_rate:.0f}%")
    else:
        print(f"  事后修复率: 无数据")

    print()

    # 触发模式
    if recent_mood:
        triggers = defaultdict(int)
        for e in recent_mood:
            triggers[e.get('trigger', '其他')] += 1
        top = sorted(triggers.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"  高频触发 (7天)")
        for t, c in top:
            bar = "▓" * c + "░" * (7 - c)
            print(f"  {bar} {t[:15]} ({c}次)")
    else:
        print(f"  高频触发: 无数据")

    print()
    print(f"  使用 'python3 scripts/*.py --help' 查看各工具用法")
    print()


def show_connection_trend(days=14):
    """显示连接时刻追踪"""
    entries = load_mood()
    if not entries:
        print("暂无数据。")
        return

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e['date'] >= cutoff]

    if not recent:
        print(f"最近{days}天没有数据。")
        return

    # 计算每日连接得分
    by_date = defaultdict(list)
    for e in recent:
        by_date[e['date']].append(e)

    print(f"\n{'='*60}")
    print(f"连接时刻追踪 (最近{days}天)")
    print(f"{'='*60}")
    print()

    for date in sorted(by_date.keys(), reverse=True)[:14]:
        day_entries = by_date[date]
        d = datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d")

        # 连接指标
        has_repair = any(e.get('repair') not in ('否', '未', '未记录') for e in day_entries)
        avg_score = sum(e['score'] for e in day_entries) / len(day_entries)

        repair_icon = "✓" if has_repair else "○"
        score_icon = mood_emoji(avg_score)

        print(f"  {d} 情绪:{score_icon}{avg_score:.0f}  修复:{repair_icon}")

    print()
    print(f"  图例: ✓=有修复  ○=无修复  ○=平静  ●=低落")
    print(f"{'='*60}")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
    elif "--dashboard" in args or len(args) == 0:
        show_dashboard()
    elif "--mood" in args:
        days = 7
        if "--mood" in args:
            try:
                idx = args.index("--mood") + 1
                days = int(args[idx])
            except (IndexError, ValueError):
                pass
        show_mood_trend(days)
    elif "--stress" in args:
        days = 30
        if "--stress" in args:
            try:
                idx = args.index("--stress") + 1
                days = int(args[idx])
            except (IndexError, ValueError):
                pass
        show_stress_trend(days)
    elif "--connection" in args:
        show_connection_trend()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
