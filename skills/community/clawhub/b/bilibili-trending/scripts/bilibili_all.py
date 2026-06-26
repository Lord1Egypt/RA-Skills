"""
Bilibili 热门数据抓取与分析自动化脚本

完整流程：抓取数据 → 保存 JSON → 更新趋势 → 自动调用子 Agent 分析
"""

import argparse
import sys
import io

from config import RANK_CONFIG
from common import (
    fetch_and_process,
    save_json_data,
    save_trend,
    generate_analysis_prompt,
    spawn_analysis_agent,
    ANALYSIS_DIR,
)

# Windows 控制台编码修复
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Bilibili 热门数据分析")
    parser.add_argument("--rank", "-r", type=str, default="all", help="榜单类型")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有榜单")
    parser.add_argument("--manual", "-m", action="store_true", help="手动模式（不调用子 Agent）")
    parser.add_argument("--alert", "-a", action="store_true", help="运行异常检测")
    args = parser.parse_args()

    if args.list:
        print("\n可用榜单:")
        for key, config in RANK_CONFIG.items():
            print(f"  {key:15} - {config['name']}")
        return

    rank_type = args.rank
    if rank_type not in RANK_CONFIG:
        print(f"未知榜单: {rank_type}，使用 --list 查看可用榜单")
        return

    config = RANK_CONFIG[rank_type]
    rank_name = config["name"]

    print(f"\n{'=' * 50}")
    print(f"开始抓取 {rank_name} 榜单...")
    print("=" * 50)

    # Step 1: 抓取数据
    try:
        videos, summary = fetch_and_process(rank_type)
    except Exception as e:
        print(f"抓取失败: {e}")
        return

    print(f"已抓取 {len(videos)} 条数据")
    print(f"  总播放: {summary['total_views']:,}")
    print(f"  平均互动率: {summary['avg_interaction_rate']}%")
    print(f"  最热分区: {summary['top_zone']}")

    # Step 2: 保存 JSON
    output_path = save_json_data(rank_type, rank_name, videos, summary)
    print(f"数据已保存: {output_path}")

    # Step 3: 生成 prompt 并更新趋势
    prompt, top_keywords = generate_analysis_prompt(rank_type, videos, summary)
    save_trend(rank_type, summary.get("top_zone", ""), top_keywords, summary.get("avg_interaction_rate", 0))
    print("趋势数据已更新")

    # Step 3.5: 异常检测（如果启用）
    if args.alert:
        from alerts import detect_all, format_alerts, save_alerts
        alerts = detect_all(rank_type, videos, summary, top_keywords)
        if alerts:
            save_alerts(alerts)
            print(format_alerts(alerts))
        else:
            print("未检测到异常")

    # Step 4: 自动调用子 Agent（除非 --manual）
    if args.manual:
        print(f"\n{'=' * 50}")
        print("手动模式，跳过子 Agent")
        print("=" * 50)
        print("Prompt 如下：")
        print("-" * 50)
        print(prompt)
        return

    print(f"\n{'=' * 50}")
    print("正在调用子 Agent 分析...")
    print("=" * 50)

    if spawn_analysis_agent(prompt, label=f"bili-{rank_type}"):
        print(f"子 Agent 已启动，报告将保存到: {ANALYSIS_DIR}")
    else:
        print("子 Agent 不可用，以下是 prompt 供手动使用：")
        print("-" * 50)
        print(prompt)


if __name__ == "__main__":
    main()
