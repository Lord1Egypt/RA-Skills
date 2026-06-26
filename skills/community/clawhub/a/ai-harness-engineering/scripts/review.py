#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 定期回顾脚本
周期性回顾机制，持续优化
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
ERRORS_FILE = DATA_DIR / "error_ledger.jsonl"
LEARNINGS_FILE = DATA_DIR / "learnings_ledger.jsonl"
FEATURES_FILE = DATA_DIR / "feature_ledger.jsonl"


def load_errors() -> list:
    """加载错误记录"""
    errors = []
    if ERRORS_FILE.exists():
        with open(ERRORS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        errors.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return errors


def load_learnings() -> list:
    """加载学习记录"""
    learnings = []
    if LEARNINGS_FILE.exists():
        with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        learnings.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return learnings


def load_features() -> list:
    """加载功能请求"""
    features = []
    if FEATURES_FILE.exists():
        with open(FEATURES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        features.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return features


def render_status_report(errors: list, learnings: list, features: list) -> str:
    """渲染状态概览报告"""
    lines = []
    lines.append("╔═══════════════════════════════════════════════════╗")
    lines.append("║       Harness Engineering 定期回顾 - 状态概览     ║")
    lines.append("╚═══════════════════════════════════════════════════╝")
    lines.append("")
    
    # 错误统计
    total_errors = len(errors)
    pending_errors = len([e for e in errors if e.get('fix_status') == '未修复'])
    resolved_errors = len([e for e in errors if e.get('fix_status') in ['已修复', '已规避']])
    
    lines.append(f"📊 错误记录：{total_errors} 条")
    lines.append(f"   └─ 未处理：{pending_errors} 条")
    lines.append(f"   └─ 已解决：{resolved_errors} 条")
    lines.append("")
    
    # 学习统计
    total_learnings = len(learnings)
    pending_learnings = len([l for l in learnings if l.get('status') == 'pending'])
    promoted_learnings = len([l for l in learnings if l.get('status') == 'promoted'])
    
    lines.append(f"📚 学习记录：{total_learnings} 条")
    lines.append(f"   └─ 待处理：{pending_learnings} 条")
    lines.append(f"   └─ 已提升：{promoted_learnings} 条")
    lines.append("")
    
    # 功能请求统计
    total_features = len(features)
    pending_features = len([f for f in features if f.get('status') == 'pending'])
    
    lines.append(f"✨ 功能请求：{total_features} 条")
    lines.append(f"   └─ 待处理：{pending_features} 条")
    lines.append("")
    
    # 计算总体健康度
    total_items = total_errors + total_learnings + total_features
    if total_items > 0:
        resolved = resolved_errors + promoted_learnings
        health = round(resolved / total_items * 100, 1)
        lines.append(f"💚 总体健康度：{health}%")
    else:
        lines.append("💚 总体健康度：100%（暂无记录）")
    
    lines.append("")
    lines.append("提示：使用 --action high_priority 查看需要优先处理的项目")
    
    return '\n'.join(lines)


def render_high_priority_report(errors: list, learnings: list, features: list) -> str:
    """渲染高优先级报告"""
    lines = []
    lines.append("╔═══════════════════════════════════════════════════╗")
    lines.append("║       高优先级项目 - 需要立即关注                 ║")
    lines.append("╚═══════════════════════════════════════════════════╝")
    lines.append("")
    
    # 高优先级错误
    high_errors = [e for e in errors if e.get('level') in ['高', '严重'] and e.get('fix_status') == '未修复']
    if high_errors:
        lines.append("🚨 高优先级错误：")
        for e in high_errors[:5]:
            lines.append(f"   • {e.get('error_id')} [{e.get('error_type')}] {e.get('question', '')[:50]}...")
        lines.append("")
    
    # 高优先级学习
    high_learnings = [l for l in learnings if l.get('priority') in ['high', 'critical'] and l.get('status') == 'pending']
    if high_learnings:
        lines.append("📌 高优先级学习：")
        for l in high_learnings[:5]:
            lines.append(f"   • {l.get('learning_id')} [{l.get('category')}] {l.get('summary', '')[:50]}...")
        lines.append("")
    
    # 高优先级功能请求
    high_features = [f for f in features if f.get('priority') in ['high', 'critical'] and f.get('status') == 'pending']
    if high_features:
        lines.append("💡 高优先级功能请求：")
        for f in high_features[:5]:
            lines.append(f"   • {f.get('feature_id')} [{f.get('complexity')}] {f.get('feature_name', '')[:50]}...")
        lines.append("")
    
    if not high_errors and not high_learnings and not high_features:
        lines.append("✨ 暂无高优先级项目，继续保持！")
    
    return '\n'.join(lines)


def render_full_review_report(errors: list, learnings: list, features: list) -> str:
    """渲染完整回顾报告"""
    lines = []
    now = datetime.now()
    
    lines.append("# Harness Engineering 完整回顾报告")
    lines.append(f"\n生成时间：{now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 一、错误回顾
    lines.append("## 一、错误回顾\n")
    
    # 按类型统计
    if errors:
        type_counter = Counter(e.get('error_type', '未知') for e in errors)
        lines.append("### 按类型分布")
        for et, count in type_counter.most_common():
            lines.append(f"- {et}：{count} 条")
        
        lines.append("\n### 按等级分布")
        level_counter = Counter(e.get('level', '未知') for e in errors)
        for lv, count in level_counter.most_common():
            lines.append(f"- {lv}：{count} 条")
        
        lines.append("\n### 未修复错误")
        pending_errors = [e for e in errors if e.get('fix_status') == '未修复']
        if pending_errors:
            for e in pending_errors[:10]:
                lines.append(f"- {e.get('error_id')}: {e.get('question', '')[:60]}...")
        else:
            lines.append("全部已修复！🎉")
        lines.append("")
    
    # 二、学习回顾
    lines.append("## 二、学习回顾\n")
    
    if learnings:
        cat_counter = Counter(l.get('category', '未知') for l in learnings)
        lines.append("### 按类别分布")
        for cat, count in cat_counter.most_common():
            lines.append(f"- {cat}：{count} 条")
        
        lines.append("\n### 重复学习（需要提升）")
        recurring = [l for l in learnings if l.get('recurrence_count', 1) >= 2]
        if recurring:
            for l in recurring[:5]:
                lines.append(f"- {l.get('learning_id')}：出现 {l.get('recurrence_count')} 次")
        else:
            lines.append("暂无重复学习")
        lines.append("")
    
    # 三、功能请求回顾
    lines.append("## 三、功能请求回顾\n")
    
    if features:
        lines.append(f"总计：{len(features)} 条")
        pending = [f for f in features if f.get('status') == 'pending']
        lines.append(f"待处理：{len(pending)} 条")
        
        if pending:
            lines.append("\n### 待实现功能")
            for f in pending[:5]:
                lines.append(f"- {f.get('feature_id')}: {f.get('feature_name')} ({f.get('complexity')})")
        lines.append("")
    
    # 四、建议
    lines.append("## 四、改进建议\n")
    
    if pending_errors := [e for e in errors if e.get('fix_status') == '未修复']:
        lines.append(f"1. 优先处理 {len(pending_errors)} 条未修复错误")
    
    if recurring := [l for l in learnings if l.get('recurrence_count', 1) >= 3]:
        lines.append(f"2. 提升 {len(recurring)} 条重复学习到workspace文件")
    
    if pending_features := [f for f in features if f.get('status') == 'pending' and f.get('complexity') == '简单']:
        lines.append(f"3. 考虑实现 {len(pending_features)} 个简单功能请求")
    
    if not pending_errors and not recurring and not pending_features:
        lines.append("状态良好，继续保持！🎉")
    
    lines.append("\n---\n*本报告由 Harness Engineering 自动生成*")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='定期回顾机制')
    parser.add_argument('--action', required=True,
                       choices=['status', 'high_priority', 'full_review'],
                       help='回顾操作')
    
    args = parser.parse_args()
    
    errors = load_errors()
    learnings = load_learnings()
    features = load_features()
    
    if args.action == 'status':
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
        print(render_status_report(errors, learnings, features))
    elif args.action == 'high_priority':
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
        print(render_high_priority_report(errors, learnings, features))
    elif args.action == 'full_review':
        print(render_full_review_report(errors, learnings, features))


if __name__ == '__main__':
    main()