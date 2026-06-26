#!/usr/bin/env python3
"""
Flomo 笔记完整获取工具 - 智能三级降级策略
月 → 周 → 天，确保获取指定月份的所有笔记
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from calendar import monthrange
from collections import Counter

def run_mcporter(tool: str, **kwargs):
    """调用 mcporter - 使用 --config 指定配置文件路径"""
    import os
    
    # 获取 mcporter 配置文件路径
    config_path = os.path.expanduser("~/.openclaw/workspace/config/mcporter.json")
    
    cmd_parts = ["mcporter", "--config", config_path, "call", f"flomo.{tool}"]
    for k, v in kwargs.items():
        cmd_parts.append(f'{k}="{v}"')
    cmd = " ".join(cmd_parts)
    
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True, 
        shell=True,
        env=os.environ.copy()
    )
    try:
        return json.loads(result.stdout)
    except:
        print(f"API 错误: {result.stderr[:200]}", file=sys.stderr)
        return {}

def search_by_range(start_date: str, end_date: str):
    """按日期范围搜索笔记"""
    result = run_mcporter("memo_search", start_date=start_date, end_date=end_date, limit=50)
    return result.get("memos", [])

def fetch_month_memos(year: int, month: int, verbose: bool = False):
    """
    智能获取某月的所有笔记
    策略: 按周 → 满50条则降级按天
    """
    all_memos = []
    seen_ids = set()
    api_calls = 0
    
    _, last_day = monthrange(year, month)
    week_start = 1
    week_num = 1
    
    if verbose:
        print(f"📅 获取 {year}年{month}月 的笔记...")
    
    while week_start <= last_day:
        week_s = datetime(year, month, week_start)
        week_e = min(week_s + timedelta(days=6), datetime(year, month, last_day))
        
        # 按周获取
        week_memos = search_by_range(
            week_s.strftime("%Y-%m-%d"), 
            week_e.strftime("%Y-%m-%d")
        )
        api_calls += 1
        
        if len(week_memos) < 50:
            # 该周安全，直接添加
            for m in week_memos:
                if m["id"] not in seen_ids:
                    seen_ids.add(m["id"])
                    all_memos.append(m)
            if verbose:
                print(f"  ✅ 第{week_num}周 ({week_s.day}~{week_e.day}日): {len(week_memos)} 条")
        else:
            # 满额，降级按天获取
            if verbose:
                print(f"  ⚠️ 第{week_num}周 ({week_s.day}~{week_e.day}日): {len(week_memos)} 条 → 降级按天")
            
            for day_offset in range((week_e - week_s).days + 1):
                day = week_s + timedelta(days=day_offset)
                day_str = day.strftime("%Y-%m-%d")
                day_memos = search_by_range(day_str, day_str)
                api_calls += 1
                
                day_new = 0
                for m in day_memos:
                    if m["id"] not in seen_ids:
                        seen_ids.add(m["id"])
                        all_memos.append(m)
                        day_new += 1
                
                if verbose:
                    print(f"     📍 {day_str}: {len(day_memos)} 条, 新增 {day_new} 条")
                time.sleep(0.1)
        
        week_start = week_e.day + 1
        week_num += 1
        time.sleep(0.1)
    
    return {
        "memos": all_memos,
        "total": len(all_memos),
        "api_calls": api_calls,
        "date_range": {
            "start": min(m["created_at"][:10] for m in all_memos) if all_memos else None,
            "end": max(m["created_at"][:10] for m in all_memos) if all_memos else None
        }
    }

def analyze_memos(memos):
    """分析笔记统计信息"""
    if not memos:
        return {}
    
    # 标签统计
    tag_counts = Counter()
    for m in memos:
        for tag in m.get("tags", []):
            tag_counts[tag] += 1
    
    # 字数统计
    word_counts = [m.get("word_count", 0) for m in memos]
    
    # 每日分布
    date_counts = Counter(m["created_at"][:10] for m in memos)
    
    return {
        "tags": tag_counts.most_common(10),
        "word_stats": {
            "avg": sum(word_counts) // len(word_counts),
            "min": min(word_counts),
            "max": max(word_counts),
            "under_20": sum(1 for w in word_counts if w < 20),
            "over_200": sum(1 for w in word_counts if w > 200)
        },
        "daily_avg": len(memos) / len(date_counts) if date_counts else 0,
        "active_days": len(date_counts)
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="获取 Flomo 指定月份的完整笔记")
    parser.add_argument("year", type=int, help="年份")
    parser.add_argument("month", type=int, help="月份")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细进度")
    args = parser.parse_args()
    
    result = fetch_month_memos(args.year, args.month, verbose=args.verbose)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"📊 {args.year}年{args.month}月 Flomo 笔记统计")
        print(f"{'='*60}")
        print(f"总笔记数: {result['total']}")
        print(f"API 调用: {result['api_calls']} 次")
        if result['date_range']['start']:
            print(f"日期范围: {result['date_range']['start']} ~ {result['date_range']['end']}")
        
        if result['total'] > 0:
            stats = analyze_memos(result['memos'])
            print(f"\n🏷️ 热门标签:")
            for tag, count in stats['tags'][:5]:
                print(f"   #{tag}: {count} 条")
            
            print(f"\n📝 字数统计:")
            print(f"   平均: {stats['word_stats']['avg']} 字")
            print(f"   范围: {stats['word_stats']['min']} - {stats['word_stats']['max']} 字")
            print(f"   短笔记(<20字): {stats['word_stats']['under_20']} 条")
        
        # 输出到文件供后续处理
        output_file = f"/tmp/flomo_{args.year}_{args.month:02d}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result['memos'], f, ensure_ascii=False, indent=2)
        print(f"\n💾 笔记已保存: {output_file}")

if __name__ == "__main__":
    main()
