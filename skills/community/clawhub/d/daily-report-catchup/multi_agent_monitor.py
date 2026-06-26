#!/usr/bin/env python3
"""
多 Agent 日报汇总监控
汇总所有 agent 的日报状态，生成统一视图
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 支持的工作区列表（可配置）
WORKSPACES = [
    "/home/colbert/.openclaw/workspace-coding-advisor",
    # 添加更多工作区路径...
]

def scan_workspace(workspace_path):
    """扫描单个工作区的日报状态"""
    report_dir = Path(workspace_path) / "memory/daily-reports"
    index_file = report_dir / "INDEX.md"
    
    if not report_dir.exists():
        return None
    
    workspace_name = Path(workspace_path).name
    stats = {
        "workspace": workspace_name,
        "path": workspace_path,
        "total_indexed": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "missed": 0,
        "caught_up": 0,
        "today_status": None,
        "last_7_days": [],
    }
    
    # 读取 INDEX
    if index_file.exists():
        for line in index_file.read_text().splitlines():
            if line.startswith("|") and "2026-" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) < 4:
                    continue
                date = parts[1]
                status = parts[3]
                
                stats["total_indexed"] += 1
                
                if status == "success":
                    stats["success"] += 1
                elif status == "failed":
                    stats["failed"] += 1
                elif status == "skipped":
                    stats["skipped"] += 1
                elif status == "missed":
                    stats["missed"] += 1
                elif status == "caught-up":
                    stats["caught_up"] += 1
                
                # 最近7天
                if "2026-04-" in date:
                    day = int(date.split("-")[2])
                    if day >= 14:  # 4月14日以来
                        stats["last_7_days"].append((date, status))
    
    # 检查今日状态
    today = datetime.now().strftime("%Y-%m-%d")
    today_file = report_dir / f"{today}.md"
    if today_file.exists():
        stats["today_status"] = "file_exists"
    else:
        stats["today_status"] = "no_file"
    
    return stats

def generate_summary():
    """生成汇总报告"""
    print("\n" + "=" * 60)
    print("📊 多 Agent 日报状态汇总")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    all_stats = []
    
    for workspace in WORKSPACES:
        if os.path.exists(workspace):
            stats = scan_workspace(workspace)
            if stats:
                all_stats.append(stats)
    
    if not all_stats:
        print("\n❌ 未找到任何工作区")
        return
    
    # 汇总统计
    total_success = sum(s["success"] for s in all_stats)
    total_failed = sum(s["failed"] for s in all_stats)
    total_missed = sum(s["missed"] for s in all_stats)
    total_caught_up = sum(s["caught_up"] for s in all_stats)
    
    print(f"\n📈 总体统计")
    print(f"{'-' * 40}")
    print(f"✅ 成功: {total_success}")
    print(f"❌ 失败: {total_failed}")
    print(f"⚠️ 漏发: {total_missed}")
    print(f"📝 已补录: {total_caught_up}")
    
    print(f"\n👥 各 Agent 状态")
    print(f"{'-' * 60}")
    
    for stats in all_stats:
        print(f"\n📁 {stats['workspace']}")
        print(f"   路径: {stats['path']}")
        print(f"   今日: {stats['today_status']}")
        print(f"   近7天: {len(stats['last_7_days'])} 条记录")
        
        # 近7天详情
        if stats['last_7_days']:
            for date, status in sorted(stats['last_7_days']):
                status_icon = {
                    "success": "✅",
                    "failed": "❌",
                    "skipped": "⏭️",
                    "missed": "⚠️",
                    "caught-up": "📝",
                }.get(status, "❓")
                print(f"      {date}: {status_icon} {status}")
    
    # 问题提醒
    if total_failed > 0 or total_missed > 0:
        print(f"\n⚠️ 需要关注")
        print(f"{'-' * 40}")
        for stats in all_stats:
            if stats["failed"] > 0:
                print(f"  {stats['workspace']}: {stats['failed']} 天失败")
            if stats["missed"] > 0:
                print(f"  {stats['workspace']}: {stats['missed']} 天漏发")

def main():
    generate_summary()

if __name__ == "__main__":
    main()
