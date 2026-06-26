#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 错误统计面板
生成错误统计数据和可视化报告
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

# 获取skill目录
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
LEDGER_FILE = DATA_DIR / "error_ledger.jsonl"


def load_errors() -> List[dict]:
    """加载所有错误记录"""
    errors = []
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        errors.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return errors


def filter_by_period(errors: List[dict], period: str) -> List[dict]:
    """按时间范围过滤"""
    now = datetime.now()
    
    if period == 'today':
        cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        cutoff = now - timedelta(days=7)
    elif period == 'month':
        cutoff = now - timedelta(days=30)
    elif period == 'all':
        return errors
    else:
        return errors
    
    filtered = []
    for error in errors:
        try:
            ts = datetime.fromisoformat(error.get('timestamp', ''))
            if ts >= cutoff:
                filtered.append(error)
        except (ValueError, TypeError):
            continue
    
    return filtered


def calculate_stats(errors: List[dict]) -> Dict:
    """计算统计数据"""
    if not errors:
        return {
            "total": 0,
            "by_type": {},
            "by_level": {},
            "by_status": {},
            "by_scene": {},
            "high_frequency": [],
            "fix_rate": 0
        }
    
    # 按类型统计
    type_counter = Counter(e.get('error_type', '未知') for e in errors)
    
    # 按等级统计
    level_counter = Counter(e.get('level', '未知') for e in errors)
    
    # 按修复状态统计
    status_counter = Counter(e.get('fix_status', '未知') for e in errors)
    
    # 按场景统计
    scene_counter = Counter(e.get('scene', '未知') for e in errors)
    
    # 计算修复率
    fixed = status_counter.get('已修复', 0) + status_counter.get('已规避', 0)
    fix_rate = (fixed / len(errors) * 100) if errors else 0
    
    # 高频错误（相同类型+相似标签组合）
    error_patterns = {}
    for e in errors:
        pattern_key = f"{e.get('error_type')}:{','.join(sorted(e.get('tags', [])))}"
        if pattern_key not in error_patterns:
            error_patterns[pattern_key] = {
                "error_type": e.get('error_type'),
                "tags": e.get('tags', []),
                "count": 0,
                "example": e
            }
        error_patterns[pattern_key]["count"] += 1
    
    # 按出现次数排序，取TOP 5
    high_frequency = sorted(
        [p for p in error_patterns.values() if p['count'] >= 2],
        key=lambda x: x['count'],
        reverse=True
    )[:5]
    
    return {
        "total": len(errors),
        "by_type": dict(type_counter.most_common()),
        "by_level": dict(level_counter.most_common()),
        "by_status": dict(status_counter.most_common()),
        "by_scene": dict(scene_counter.most_common()),
        "high_frequency": high_frequency,
        "fix_rate": round(fix_rate, 1)
    }


def render_text_report(stats: Dict, period: str) -> str:
    """渲染文本格式的统计报告"""
    lines = []
    
    # 标题
    lines.append("╔══════════════════════════════════════════════╗")
    lines.append("║     Harness Engineering 错误统计面板         ║")
    lines.append("╚══════════════════════════════════════════════╝")
    lines.append("")
    
    # 统计周期
    now = datetime.now()
    if period == 'today':
        period_str = now.strftime("%Y-%m-%d")
    elif period == 'week':
        period_str = f"{(now - timedelta(days=7)).strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}"
    elif period == 'month':
        period_str = f"{(now - timedelta(days=30)).strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}"
    else:
        period_str = "全部"
    
    lines.append(f"统计周期：{period_str}")
    lines.append("")
    lines.append(f"📊 错误总数：{stats['total']}")
    lines.append("")
    
    if stats['total'] == 0:
        lines.append("✨ 暂无错误记录，继续保持！")
        return '\n'.join(lines)
    
    # 按类型分布
    lines.append("📂 按类型分布：")
    total = stats['total']
    for et, count in stats['by_type'].items():
        pct = round(count / total * 100)
        bar = '█' * (pct // 10) + '░' * (10 - pct // 10)
        lines.append(f"  - {et}：{count} ({pct}%) {bar}")
    lines.append("")
    
    # 按等级分布
    lines.append("⚡ 按等级分布：")
    for lv in ['严重', '高', '中', '低']:
        count = stats['by_level'].get(lv, 0)
        if count > 0:
            pct = round(count / total * 100)
            lines.append(f"  - {lv}：{count} ({pct}%)")
    lines.append("")
    
    # 修复状态
    lines.append("🔄 修复状态：")
    for st, count in stats['by_status'].items():
        pct = round(count / total * 100)
        lines.append(f"  - {st}：{count} ({pct}%)")
    lines.append(f"  └─ 修复率：{stats['fix_rate']}%")
    lines.append("")
    
    # 高频错误
    if stats['high_frequency']:
        lines.append("🔥 高频错误 TOP 5：")
        for i, hf in enumerate(stats['high_frequency'], 1):
            tags_str = ', '.join(hf['tags'][:3]) if hf['tags'] else '无标签'
            lines.append(f"  {i}. [{hf['error_type']}] {tags_str} ({hf['count']}次)")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='错误统计面板')
    parser.add_argument('--period', choices=['today', 'week', 'month', 'all'], 
                       default='week', help='统计周期')
    parser.add_argument('--format', choices=['text', 'json'], default='text', 
                       help='输出格式')
    
    args = parser.parse_args()
    
    # 加载错误
    errors = load_errors()
    
    # 按时间范围过滤
    errors = filter_by_period(errors, args.period)
    
    # 计算统计
    stats = calculate_stats(errors)
    
    # 输出
    if args.format == 'json':
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        report = render_text_report(stats, args.period)
        # 设置UTF-8输出解决Windows编码问题
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
        print(report)


if __name__ == '__main__':
    main()
