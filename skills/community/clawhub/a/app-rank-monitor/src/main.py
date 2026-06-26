#!/usr/bin/env python3
"""
App Monitor - 应用榜单监控平台
主入口文件

功能：爬取应用榜单数据
"""

import asyncio
import argparse
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from monitor import AppMonitor
from utils.logger import setup_logger

console = Console()
logger = setup_logger()


async def main():
    parser = argparse.ArgumentParser(description="应用榜单监控平台")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 榜单爬取
    parser_rank = subparsers.add_parser("rank", help="爬取榜单数据")
    parser_rank.add_argument("--send-report", action="store_true", help="爬取后发送日报")
    parser_rank.add_argument("--platform", choices=["all", "diandian", "diandian_android", "apple"], default="all", help="指定平台")
    parser_rank.add_argument("--channels", nargs="+", help="安卓渠道列表 (huawei/xiaomi/tencent/oppo/vivo/baidu/qihoo360/wandoujia)")
    
    # 日报
    parser_report = subparsers.add_parser("report", help="发送日报")
    parser_report.add_argument("--date", help="指定日期 (YYYY-MM-DD)")
    
    # 苹果榜单专用命令
    parser_apple = subparsers.add_parser("apple-rank", help="爬取苹果榜单")
    parser_apple.add_argument("--full", action="store_true", help="爬取所有分类（全量模式，默认 False）")
    parser_apple.add_argument("--top-only", action="store_true", help="只爬取总榜（快速模式，默认 True）")
    parser_apple.add_argument("--retention-days", type=int, default=7, help="数据保留天数（默认 7 天）")
    
    # 统计
    subparsers.add_parser("stats", help="查看数据统计")
    
    args = parser.parse_args()
    
    console.print(Panel.fit("📊 App Monitor", style="bold cyan"))
    
    monitor = AppMonitor()
    
    if args.command == "rank":
        await fetch_ranks(monitor, send_report=args.send_report, platform=args.platform, channels=args.channels)
    elif args.command == "report":
        await send_report(monitor, date_str=args.date)
    elif args.command == "apple-rank":
        fetch_all = args.full  # 默认只爬总榜，除非指定 --full
        await fetch_apple_ranks(monitor, fetch_all=fetch_all, retention_days=args.retention_days)
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()


async def fetch_ranks(monitor: AppMonitor, send_report: bool = False, platform: str = "all", channels: list = None):
    """爬取榜单数据"""
    console.print(f"[cyan]📊 开始爬取榜单数据... (platform={platform})[/cyan]")
    
    if platform == "all":
        await monitor.fetch_all_ranks(platform=platform, android_channels=channels)
    elif platform == "diandian_android":
        # 爬取安卓渠道
        await monitor.fetch_diandian_android_all_channels(channels)
    else:
        # 只爬取指定平台
        if platform in monitor.rankers:
            ranker = monitor.rankers[platform]
            data = await ranker.fetch_all()
            monitor.reporter.save_rank_data(platform, data)
            console.print(f"[green]✓ {platform} 榜单爬取完成[/green]")
        else:
            console.print(f"[red]✗ 不支持的平台：{platform}[/red]")
            return
    
    if send_report:
        console.print("[cyan]📧 发送日报...[/cyan]")
        await monitor.send_daily_report()
        console.print("[green]✓ 日报已发送[/green]")
    
    console.print("[green]✓ 榜单爬取完成[/green]")


async def send_report(monitor: AppMonitor, date_str: str = None):
    """发送日报"""
    from datetime import date
    
    if date_str:
        try:
            report_date = date.fromisoformat(date_str)
        except ValueError:
            console.print("[red]✗ 日期格式错误，请使用 YYYY-MM-DD[/red]")
            return
    else:
        report_date = date.today()
    
    console.print(f"[cyan]📧 发送日报 ({report_date.isoformat()})...[/cyan]")
    await monitor.send_daily_report()
    console.print("[green]✓ 日报已发送[/green]")


async def fetch_apple_ranks(monitor: AppMonitor, fetch_all: bool = True, retention_days: int = 7):
    """爬取苹果榜单"""
    mode_str = "全量模式" if fetch_all else "快速模式"
    console.print(f"[cyan]🍎 开始爬取苹果榜单 ({mode_str})...[/cyan]")
    console.print(f"[cyan]📦 数据保留策略：{retention_days} 天[/cyan]")
    
    try:
        await monitor._fetch_apple_charts(fetch_all=fetch_all, retention_days=retention_days)
        console.print("[green]✓ 苹果榜单爬取完成[/green]")
    except Exception as e:
        console.print(f"[red]✗ 爬取失败：{e}[/red]")


def show_stats():
    """查看数据统计"""
    import subprocess
    import sys
    from pathlib import Path
    
    # 调用 show_stats.py 工具
    stats_script = Path(__file__).parent.parent / "tools" / "show_stats.py"
    if stats_script.exists():
        subprocess.run([sys.executable, str(stats_script)])
    else:
        console.print("[red]✗ 统计工具不存在[/red]")


if __name__ == "__main__":
    asyncio.run(main())
