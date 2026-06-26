#!/usr/bin/env python3
"""Token Monitor - 监控 AI Token 消耗"""

import json
import os
import sys
import glob
import argparse
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = os.path.expanduser("~/.qclaw/workspace")
SESSIONS_DIR = os.path.expanduser("~/.qclaw/agents/main/sessions")
MEMORY_DIR = os.path.expanduser("~/.qclaw/workspace/memory")

# 异常阈值
ANOMALY_THRESHOLDS = {
    "daily_total": 10_000_000,  # 1000万/天
    "hourly": 2_000_000,        # 200万/小时
    "single_call": 500_000,     # 50万/单次调用
}

def parse_timestamp(ts_str):
    """解析 ISO 格式时间戳"""
    try:
        # 处理带毫秒的时间戳
        if '.' in ts_str:
            ts_str = ts_str.split('.')[0] + '.' + ts_str.split('.')[1][:6]
            return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except:
        return None

def parse_all_sessions_for_date(date_str):
    """解析所有 session 文件中指定日期的数据"""
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    
    tokens_in = 0
    tokens_out = 0
    total_tokens = 0
    message_count = 0
    files_checked = 0
    
    pattern = os.path.join(SESSIONS_DIR, "*.jsonl")
    all_files = glob.glob(pattern)
    
    for filepath in all_files:
        files_checked += 1
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                        if msg.get("type") != "message":
                            continue
                        
                        # 检查时间戳
                        ts_str = msg.get("timestamp", "")
                        msg_time = parse_timestamp(ts_str)
                        if not msg_time:
                            continue
                        
                        # 只统计目标日期的消息
                        if msg_time.date() != target_date:
                            continue
                        
                        # 统计 token
                        message = msg.get("message", {})
                        usage = message.get("usage", {})
                        if usage:
                            tokens_in += usage.get("input", 0)
                            tokens_out += usage.get("output", 0)
                            total_tokens += usage.get("totalTokens", 0)
                            message_count += 1
                            
                    except (json.JSONDecodeError, ValueError):
                        continue
        except Exception as e:
            print(f"Warning: Error reading {filepath}: {e}", file=sys.stderr)
    
    return {
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "total": total_tokens,
        "messages": message_count,
        "files_checked": files_checked,
    }

def format_number(n):
    """格式化数字"""
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def check_date(date_str):
    """检查指定日期消耗"""
    print(f"\n🔍 正在分析 {date_str} 的 Token 消耗...")
    
    stats = parse_all_sessions_for_date(date_str)
    
    if stats["messages"] == 0:
        print(f"📭 {date_str} 无消息记录")
        return 0
    
    print(f"\n📊 Token 消耗报告 - {date_str}")
    print("=" * 50)
    print(f"📁 检查文件: {stats['files_checked']}")
    print(f"💬 消息数量: {stats['messages']}")
    print(f"📥 Input:    {format_number(stats['tokens_in']):>10}")
    print(f"📤 Output:   {format_number(stats['tokens_out']):>10}")
    print(f"📊 Total:    {format_number(stats['total']):>10}")
    print("=" * 50)
    
    # 异常检查
    if stats["total"] > ANOMALY_THRESHOLDS["daily_total"]:
        print(f"\n🚨 警告：单日消耗超过 {format_number(ANOMALY_THRESHOLDS['daily_total'])}！")
        print("   建议检查是否有重复失败或死循环")
        print("   参考: ~/.qclaw/workspace/memory/2026-04-14.md")
    elif stats["total"] > 5_000_000:
        print(f"\n⚠️  提醒：消耗较高，建议检查优化空间")
    
    # 保存统计
    save_stats(date_str, stats)
    
    return stats["total"]

def save_stats(date_str, stats):
    """保存统计到 memory"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    filepath = os.path.join(MEMORY_DIR, f"token-usage-{date_str}.json")
    
    data = {
        "date": date_str,
        "tokens_in": stats["tokens_in"],
        "tokens_out": stats["tokens_out"],
        "total": stats["total"],
        "messages": stats["messages"],
        "recorded_at": datetime.now().isoformat(),
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 统计已保存: memory/token-usage-{date_str}.json")

def generate_report():
    """生成优化报告"""
    print("\n📋 Token 优化建议报告")
    print("=" * 50)
    
    suggestions = [
        ("浏览器快照", "使用 compact=true + depth=1", "可减少 50-80% token"),
        ("失败重试", "同一操作失败3次立即换方案", "避免死循环浪费"),
        ("限速等待", "不设后台轮询，跳转做其他事", "节省等待期 token"),
        ("后台进程", "设好 delay 后不 poll", "减少无效检查"),
        ("长文本", "分段处理，避免单次超大输入", "控制单次调用"),
    ]
    
    for title, action, effect in suggestions:
        print(f"\n✅ {title}")
        print(f"   做法: {action}")
        print(f"   效果: {effect}")
    
    print("\n" + "=" * 50)
    print("📚 详细规则: ~/.qclaw/workspace/AGENTS.md")
    print("📊 历史统计: memory/token-usage-YYYY-MM-DD.json")

def show_history(days=7):
    """显示最近N天历史"""
    print(f"\n📈 最近 {days} 天 Token 消耗趋势")
    print("=" * 50)
    print(f"{'日期':<12} {'Input':>10} {'Output':>10} {'Total':>10}")
    print("-" * 50)
    
    total_in = 0
    total_out = 0
    total_all = 0
    
    for i in range(days-1, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        filepath = os.path.join(MEMORY_DIR, f"token-usage-{date}.json")
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
            print(f"{date:<12} {format_number(data['tokens_in']):>10} {format_number(data['tokens_out']):>10} {format_number(data['total']):>10}")
            total_in += data['tokens_in']
            total_out += data['tokens_out']
            total_all += data['total']
        else:
            print(f"{date:<12} {'-':>10} {'-':>10} {'-':>10}")
    
    print("-" * 50)
    print(f"{'合计':<12} {format_number(total_in):>10} {format_number(total_out):>10} {format_number(total_all):>10}")

def main():
    parser = argparse.ArgumentParser(description="Token Monitor - 监控 AI Token 消耗")
    parser.add_argument("--today", action="store_true", help="检查今日消耗")
    parser.add_argument("--date", type=str, help="检查指定日期 (YYYY-MM-DD)")
    parser.add_argument("--report", action="store_true", help="生成优化报告")
    parser.add_argument("--history", type=int, metavar="N", help="显示最近N天历史")
    
    args = parser.parse_args()
    
    if args.report:
        generate_report()
    elif args.history:
        show_history(args.history)
    elif args.date:
        check_date(args.date)
    else:
        # 默认检查今日
        today = datetime.now().strftime("%Y-%m-%d")
        check_date(today)

if __name__ == "__main__":
    main()
