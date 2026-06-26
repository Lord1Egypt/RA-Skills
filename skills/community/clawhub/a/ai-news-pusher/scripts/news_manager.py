#!/usr/bin/env python3
"""
新闻管理脚本 - 用于人工审核待阅池、标记反馈和分析
"""

import os
import sys
import json
import argparse
from pathlib import Path

script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from data_storage import DataStorage
from news_scorer import NewsScorer


def print_news_summary(news, index=None):
    """打印新闻摘要"""
    prefix = f"[{index}] " if index is not None else ""
    print(f"\n{prefix}{'=' * 80}")
    print(f"标题: {news.get('title', '无标题')}")
    print(f"来源: {news.get('source', '未知')} (权重: {news.get('source_weight', 5)}, 分类: {news.get('source_category', 'unknown')})")
    print(f"链接: {news.get('url', '无链接')}")
    print(f"评分: {news.get('score', '未评分')} | 理由: {news.get('rationale', '')}")
    print(f"发布时间: {news.get('published_date', '未知')}")
    print(f"{'-' * 80}")
    print(f"内容: {news.get('content', '无内容')[:500]}...")
    print(f"{'=' * 80}\n")


def review_gray_zone(storage: DataStorage, limit: int = 10):
    """交互式审核待阅池"""
    gray_zone = storage.get_gray_zone(limit=limit, only_unreviewed=True)
    
    if not gray_zone:
        print("✅ 待阅池为空，没有需要审核的新闻")
        return
    
    print(f"📋 待审核新闻数量: {len(gray_zone)}")
    
    for i, news in enumerate(gray_zone, 1):
        print_news_summary(news, i)
        
        while True:
            action = input("操作 (a=批准, r=拒绝, e=提升, s=跳过, q=退出): ").strip().lower()
            
            if action == 'q':
                print("👋 退出审核")
                return
            elif action == 's':
                print("⏭️  跳过")
                break
            elif action in ['a', 'r', 'e']:
                manual_score = None
                notes = ""
                
                get_score = input("是否输入人工评分？(y/n, 默认n): ").strip().lower()
                if get_score == 'y':
                    try:
                        manual_score = int(input("请输入人工评分 (0-100): "))
                    except ValueError:
                        print("⚠️  无效的评分，使用默认值")
                
                get_notes = input("是否添加备注？(y/n, 默认n): ").strip().lower()
                if get_notes == 'y':
                    notes = input("请输入备注: ").strip()
                
                action_map = {'a': 'approve', 'r': 'reject', 'e': 'escalate'}
                news_id = news.get('url', '') or f"{news.get('title', '')}_{news.get('source', '')}"
                
                if storage.review_gray_zone_news(news_id, action_map[action], manual_score, notes):
                    print(f"✅ 操作成功: {action_map[action]}")
                else:
                    print("❌ 操作失败")
                break
            else:
                print("⚠️  无效操作，请重新输入")


def view_stats(storage: DataStorage):
    """查看统计数据"""
    stats = storage.get_stats()
    print("\n📊 统计数据")
    print(f"待审核: {stats['gray_zone_count']}")
    print(f"已推送: {stats['pushed_count']}")
    print(f"已过滤: {stats['filtered_count']}")
    print(f"反馈记录: {stats['feedback_count']}")
    
    config = storage.get_config()
    print(f"\n⚙️ 配置阈值")
    print(f"自动推送: ≥{config.get('auto_push_threshold', 80)}分")
    print(f"待阅池: {config.get('gray_zone_min', 60)}-{config.get('gray_zone_max', 80)}分")


def view_filtered(storage: DataStorage, days: int = 7, limit: int = 10):
    """查看被过滤的新闻（用于抽检）"""
    filtered = storage.get_filtered(days=days, limit=limit)
    
    if not filtered:
        print("✅ 最近没有被过滤的新闻")
        return
    
    print(f"🔍 最近 {days} 天被过滤的新闻 (显示前 {limit} 条):")
    for i, news in enumerate(filtered, 1):
        print_news_summary(news, i)


def view_feedback(storage: DataStorage, limit: int = 20):
    """查看反馈记录"""
    feedback = storage.get_feedback(limit=limit)
    
    if not feedback:
        print("✅ 暂无反馈记录")
        return
    
    print(f"\n💬 反馈记录 (显示前 {limit} 条):")
    for fb in feedback:
        print(f"\n{'-' * 60}")
        print(f"新闻ID: {fb.get('news_id', '')}")
        print(f"原始评分: {fb.get('original_score', 0)} → 人工评分: {fb.get('manual_score', 0)}")
        print(f"备注: {fb.get('notes', '')}")
        print(f"时间: {fb.get('timestamp', '')}")


def analyze_feedback(storage: DataStorage):
    """分析反馈并给出优化建议"""
    feedback = storage.get_feedback()
    
    if not feedback:
        print("⚠️  需要先收集一些反馈数据才能分析")
        return
    
    scorer = NewsScorer()
    for fb in feedback:
        scorer.add_feedback(fb['news_id'], fb['original_score'], fb['manual_score'], fb.get('notes', ''))
    
    analysis = scorer.analyze_feedback()
    
    print("\n📈 反馈分析")
    print(f"总反馈数: {analysis['total_feedback']}")
    print(f"平均评分差: {analysis['avg_score_diff']:.1f}")
    print(f"高估次数: {analysis['over_estimates']}")
    print(f"低估次数: {analysis['under_estimates']}")
    print(f"\n💡 建议: {analysis['recommendation']}")


def update_thresholds(storage: DataStorage):
    """更新评分阈值"""
    config = storage.get_config()
    
    print(f"当前配置:")
    print(f"自动推送阈值: {config.get('auto_push_threshold', 80)}")
    print(f"待阅池下限: {config.get('gray_zone_min', 60)}")
    print(f"待阅池上限: {config.get('gray_zone_max', 80)}")
    
    updates = {}
    
    try:
        val = input("\n新的自动推送阈值 (直接回车保持当前): ").strip()
        if val:
            updates['auto_push_threshold'] = int(val)
        
        val = input("新的待阅池下限 (直接回车保持当前): ").strip()
        if val:
            updates['gray_zone_min'] = int(val)
        
        val = input("新的待阅池上限 (直接回车保持当前): ").strip()
        if val:
            updates['gray_zone_max'] = int(val)
        
        if updates:
            storage.update_config(updates)
            print("✅ 配置已更新")
        else:
            print("⏭️  未做更改")
    except ValueError:
        print("❌ 无效的数值")


def main():
    parser = argparse.ArgumentParser(
        description='AI新闻管理工具 - 审核待阅池、管理反馈和分析',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 交互式审核待阅池
  python3 news_manager.py review
  
  # 查看统计数据
  python3 news_manager.py stats
  
  # 查看被过滤的新闻（抽检）
  python3 news_manager.py filtered --days 3 --limit 20
  
  # 查看反馈记录
  python3 news_manager.py feedback
  
  # 分析反馈
  python3 news_manager.py analyze
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # review命令
    review_parser = subparsers.add_parser('review', help='交互式审核待阅池')
    review_parser.add_argument('--limit', type=int, default=10, help='限制审核数量')
    
    # stats命令
    subparsers.add_parser('stats', help='查看统计数据')
    
    # filtered命令
    filtered_parser = subparsers.add_parser('filtered', help='查看被过滤的新闻（抽检）')
    filtered_parser.add_argument('--days', type=int, default=7, help='查看最近N天')
    filtered_parser.add_argument('--limit', type=int, default=10, help='限制显示数量')
    
    # feedback命令
    feedback_parser = subparsers.add_parser('feedback', help='查看反馈记录')
    feedback_parser.add_argument('--limit', type=int, default=20, help='限制显示数量')
    
    # analyze命令
    subparsers.add_parser('analyze', help='分析反馈数据')
    
    # config命令
    subparsers.add_parser('config', help='更新评分阈值配置')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    storage = DataStorage()
    
    if args.command == 'review':
        review_gray_zone(storage, args.limit)
    elif args.command == 'stats':
        view_stats(storage)
    elif args.command == 'filtered':
        view_filtered(storage, args.days, args.limit)
    elif args.command == 'feedback':
        view_feedback(storage, args.limit)
    elif args.command == 'analyze':
        analyze_feedback(storage)
    elif args.command == 'config':
        update_thresholds(storage)


if __name__ == '__main__':
    main()
