"""
Bilibili 趋势分析与报告生成

支持：趋势查看、周总结、月总结、已有数据再分析
"""

import argparse
import time
import signal
import sys
from datetime import datetime, timedelta

from config import RANK_CONFIG
from common import (
    load_trend,
    save_summary_report,
    save_trend,
    save_json_data,
    generate_analysis_prompt,
    spawn_analysis_agent,
    fetch_and_process,
    load_json_data,
    ANALYSIS_DIR,
)


def analyze_trend(rank_type=None):
    """生成趋势报告"""
    trend = load_trend()

    if rank_type:
        filtered = [r for r in trend["records"] if r.get("rank_type") == rank_type]
        if len(filtered) < 3:
            rank_name = RANK_CONFIG.get(rank_type, {}).get("name", rank_type)
            return f"{rank_name} 数据不足（需要至少 3 次记录，当前 {len(filtered)} 次）"

        zone_counter = {}
        kw_counter = {}
        for r in filtered:
            zone = r.get("top_zone", "")
            if zone:
                zone_counter[zone] = zone_counter.get(zone, 0) + 1
            for kw in r.get("keywords", []):
                kw_counter[kw] = kw_counter.get(kw, 0) + 1

        rank_name = RANK_CONFIG.get(rank_type, {}).get("name", rank_type)
        report = f"# {rank_name} 趋势分析\n\n"
        report += f"分析次数: {len(filtered)} 次\n\n"
        report += "## 热门分区\n"
        for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
            report += f"- {zone}: {count} 次\n"
        report += "\n## 高频关键词\n"
        for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"- {kw}: {count} 次\n"
        return report

    if len(trend["records"]) < 3:
        return f"数据不足（需要至少 3 次记录，当前 {len(trend['records'])} 次）"

    report = "# Bilibili 全站趋势分析\n\n"

    report += "## 各榜单热度统计\n"
    for rank, count in sorted(trend.get("rank_stats", {}).items(), key=lambda x: x[1], reverse=True):
        rank_name = RANK_CONFIG.get(rank, {}).get("name", rank)
        report += f"- {rank_name}: {count} 次\n"

    report += "\n## 热门分区 TOP 5\n"
    for zone, count in sorted(trend["zones"].items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {zone}: {count} 次登顶\n"

    report += "\n## 高频关键词 TOP 10\n"
    for kw, count in sorted(trend["keywords"].items(), key=lambda x: x[1], reverse=True)[:10]:
        report += f"- {kw}: {count} 次\n"

    return report


def _filter_records_by_days(rank_type, days):
    """按天数筛选趋势记录"""
    trend = load_trend()
    cutoff = datetime.now() - timedelta(days=days)

    records = trend["records"]
    if rank_type:
        records = [r for r in records if r.get("rank_type") == rank_type]

    filtered = []
    for r in records:
        try:
            r_date = datetime.strptime(r.get("date", ""), "%Y-%m-%d")
            if r_date >= cutoff:
                filtered.append(r)
        except ValueError:
            continue

    if not filtered:
        return [], {}, {}, []

    zone_counter = {}
    kw_counter = {}
    interactions = []

    for r in filtered:
        zone = r.get("top_zone", "")
        if zone:
            zone_counter[zone] = zone_counter.get(zone, 0) + 1
        for kw in r.get("keywords", []):
            kw_counter[kw] = kw_counter.get(kw, 0) + 1
        interactions.append(r.get("avg_interaction", 0))

    return filtered, zone_counter, kw_counter, interactions


def generate_weekly_summary(rank_type=None):
    """生成周总结（最近 7 天）"""
    filtered, zone_counter, kw_counter, interactions = _filter_records_by_days(rank_type, 7)

    if not filtered:
        return "本周无数据"

    now = datetime.now()
    week_ago = now - timedelta(days=7)
    avg_interaction = sum(interactions) / len(interactions) if interactions else 0
    rank_label = RANK_CONFIG.get(rank_type, {}).get("name", rank_type) if rank_type else "全站"

    report = f"# 周总结 - {rank_label} ({week_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})\n\n"
    report += f"- 分析次数: {len(filtered)} 次\n"
    report += f"- 平均互动率: {avg_interaction:.2f}%\n\n"
    report += "## 热门分区\n"
    for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:3]:
        report += f"- {zone}: {count} 次\n"
    report += "\n## 热门关键词\n"
    for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {kw}: {count} 次\n"

    prefix = f"weekly-{rank_type}" if rank_type else "weekly"
    save_summary_report(f"{prefix}-{now.strftime('%YW%W')}", report)

    return report


def generate_monthly_summary(rank_type=None):
    """生成月总结（最近 30 天）"""
    filtered, zone_counter, kw_counter, interactions = _filter_records_by_days(rank_type, 30)

    if not filtered:
        return "本月无数据"

    now = datetime.now()
    month_ago = now - timedelta(days=30)
    avg_interaction = sum(interactions) / len(interactions) if interactions else 0
    rank_label = RANK_CONFIG.get(rank_type, {}).get("name", rank_type) if rank_type else "全站"

    report = f"# 月总结 - {rank_label} ({month_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})\n\n"
    report += f"- 分析次数: {len(filtered)} 次\n"
    report += f"- 平均互动率: {avg_interaction:.2f}%\n\n"
    report += "## 分区排名\n"
    for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {zone}: {count} 次登顶\n"
    report += "\n## 关键词排行\n"
    for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        report += f"- {kw}: {count} 次\n"
    report += "\n## 趋势洞察\n"
    if kw_counter:
        top_kw = max(kw_counter.items(), key=lambda x: x[1])[0]
        report += f"- 下月预测: {top_kw} 相关内容可能持续火热\n"

    prefix = f"monthly-{rank_type}" if rank_type else "monthly"
    save_summary_report(f"{prefix}-{now.strftime('%Y-%m')}", report)

    return report


def run_workflow(rank_type="all", auto_spawn=True):
    """对已有 JSON 数据运行分析工作流"""
    json_data = load_json_data(rank_type)
    videos = json_data["data"]["videos"]
    summary = json_data["data"]["summary"]

    prompt, _ = generate_analysis_prompt(rank_type, videos, summary)

    if not auto_spawn:
        print(prompt)
        return {"status": "ready", "prompt": prompt}

    print(f"\n{'=' * 50}")
    print("正在调用子 Agent 分析...")
    print("=" * 50)

    if spawn_analysis_agent(prompt, label=f"bili-{rank_type}"):
        print(f"子 Agent 已启动，报告将保存到: {ANALYSIS_DIR}")
        return {"status": "spawned", "rank_type": rank_type}
    else:
        print("子 Agent 不可用，以下是 prompt 供手动使用：")
        print("-" * 50)
        print(prompt)
        return {"status": "failed", "prompt": prompt}


def _parse_interval(val):
    """解析间隔时间，支持 2h / 30m / 90s 格式"""
    val = val.strip().lower()
    if val.endswith("h"):
        return int(float(val[:-1]) * 60)
    elif val.endswith("m"):
        return int(float(val[:-1]))
    elif val.endswith("s"):
        return max(1, int(float(val[:-1]) // 60))
    return int(val)


def _parse_ranks(val):
    """解析榜单列表，支持逗号分隔或 'all'"""
    val = val.strip()
    if val == "all":
        return list(RANK_CONFIG.keys())
    return [r.strip() for r in val.split(",") if r.strip() in RANK_CONFIG]


def run_daemon(ranks, interval_minutes, enable_alerts=True):
    """定时采集循环"""
    rank_names = ", ".join(RANK_CONFIG[r]["name"] for r in ranks)
    cycle = 0
    running = True

    def on_interrupt(sig, frame):
        nonlocal running
        print(f"\n收到中断信号，完成当前周期后退出...")
        running = False

    signal.signal(signal.SIGINT, on_interrupt)
    signal.signal(signal.SIGTERM, on_interrupt)

    print(f"\n定时采集已启动")
    print(f"  榜单: {rank_names}")
    print(f"  间隔: {interval_minutes} 分钟")
    print(f"  异常检测: {'开' if enable_alerts else '关'}")
    print(f"  按 Ctrl+C 停止\n")

    while running:
        cycle += 1
        start_time = datetime.now()
        print(f"{'=' * 50}")
        print(f"第 {cycle} 轮采集  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 50}")

        for rank_type in ranks:
            rank_name = RANK_CONFIG[rank_type]["name"]
            try:
                videos, summary = fetch_and_process(rank_type)
                save_json_data(rank_type, rank_name, videos, summary)

                prompt, top_keywords = generate_analysis_prompt(rank_type, videos, summary)
                save_trend(rank_type, summary.get("top_zone", ""), top_keywords,
                           summary.get("avg_interaction_rate", 0))

                print(f"  [{rank_name}] {len(videos)} 条 | 播放 {summary['total_views']:,} | "
                      f"互动率 {summary['avg_interaction_rate']}%")

                if enable_alerts:
                    from alerts import detect_all, format_alerts, save_alerts
                    alerts = detect_all(rank_type, videos, summary, top_keywords)
                    if alerts:
                        save_alerts(alerts)
                        print(format_alerts(alerts))

            except Exception as e:
                print(f"  [{rank_name}] 采集失败: {e}")
                continue

        elapsed = (datetime.now() - start_time).total_seconds()
        sleep_seconds = max(0, interval_minutes * 60 - elapsed)

        if running and sleep_seconds > 0:
            next_time = datetime.now() + timedelta(seconds=sleep_seconds)
            print(f"\n下一轮: {next_time.strftime('%H:%M:%S')} "
                  f"({sleep_seconds / 60:.1f} 分钟后)\n")
            # 分段 sleep，支持快速响应中断
            while sleep_seconds > 0 and running:
                chunk = min(10, sleep_seconds)
                time.sleep(chunk)
                sleep_seconds -= chunk

    print(f"\n定时采集已停止，共完成 {cycle} 轮")


def main():
    parser = argparse.ArgumentParser(description="Bilibili 趋势分析与报告")
    sub = parser.add_subparsers(dest="cmd", help="子命令")

    sub.add_parser("list", help="列出所有榜单")

    trend_p = sub.add_parser("trend", help="查看趋势")
    trend_p.add_argument("rank", nargs="?", default=None, help="榜单类型（可选）")

    weekly_p = sub.add_parser("weekly", help="生成周总结")
    weekly_p.add_argument("rank", nargs="?", default=None, help="榜单类型（可选）")

    monthly_p = sub.add_parser("monthly", help="生成月总结")
    monthly_p.add_argument("rank", nargs="?", default=None, help="榜单类型（可选）")

    workflow_p = sub.add_parser("workflow", help="对已有数据运行分析")
    workflow_p.add_argument("rank", nargs="?", default="all", help="榜单类型")
    workflow_p.add_argument("--manual", "-m", action="store_true", help="手动模式")

    daemon_p = sub.add_parser("daemon", help="定时采集模式")
    daemon_p.add_argument("--interval", "-i", type=str, default="2h", help="采集间隔 (如 2h/30m/90s)")
    daemon_p.add_argument("--ranks", "-r", type=str, default="all", help="榜单列表，逗号分隔 (默认 all)")
    daemon_p.add_argument("--no-alert", action="store_true", help="关闭异常检测")

    args = parser.parse_args()

    if args.cmd == "list" or args.cmd is None:
        print("\n可用榜单:")
        for key, config in RANK_CONFIG.items():
            print(f"  {key:15} - {config['name']}")
        if args.cmd is None:
            print("\n使用 --help 查看完整命令")
        return

    if args.cmd == "trend":
        print(analyze_trend(args.rank))
    elif args.cmd == "weekly":
        print(generate_weekly_summary(args.rank))
    elif args.cmd == "monthly":
        print(generate_monthly_summary(args.rank))
    elif args.cmd == "workflow":
        run_workflow(args.rank, auto_spawn=not args.manual)
    elif args.cmd == "daemon":
        ranks = _parse_ranks(args.ranks)
        interval = _parse_interval(args.interval)
        if interval < 1:
            print("间隔时间至少 1 分钟")
            return
        run_daemon(ranks, interval, enable_alerts=not args.no_alert)


if __name__ == "__main__":
    main()
