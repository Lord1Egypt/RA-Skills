#!/usr/bin/env python3
"""
外卖评价智能监控 - 主入口
用法:
  python monitor.py --file reviews.csv                    # CSV导入分析
  python monitor.py --file reviews.xlsx --platform meituan # 指定平台
  python monitor.py --compare new.csv old.csv              # 对比两个时段
  python monitor.py --setup                                # 初始化配置
  python monitor.py --history                              # 查看历史摘要
"""
import sys
import os
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from data_loader import ReviewDataLoader, load_reviews, load_history
from analyzer import analyze_reviews, compare_periods
from reporter import generate_html_report, generate_summary_text

# 默认配置
DEFAULT_CONFIG = {
    "shop_name": "我的店铺",
    "platforms": {
        "meituan": {"enabled": False, "shop_id": "", "api_key": ""},
        "eleme": {"enabled": False, "shop_id": "", "api_key": ""},
        "jd": {"enabled": False, "shop_id": "", "api_key": ""},
    },
    "alert_thresholds": {
        "taste_negative_ratio": 30,
        "delivery_issue_ratio": 15,
        "service_negative_ratio": 20,
        "low_rating_threshold": 4.0,
        "negative_surge_multiplier": 2.0,
    },
    "report_dir": "~/.food_review_monitor/reports",
    "data_dir": "~/.food_review_monitor/data",
}


def get_config_path():
    """获取配置文件路径"""
    config_dir = os.path.expanduser("~/.food_review_monitor")
    return os.path.join(config_dir, "config.json")


def load_config():
    """加载配置"""
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_config(config):
    """保存配置"""
    config_path = get_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"✅ 配置已保存到: {config_path}")


def cmd_setup():
    """初始化配置"""
    print("🍔 外卖评价监控 - 初始化设置")
    print("=" * 40)

    config_path = get_config_path()
    if os.path.exists(config_path):
        print(f"⚠️  配置文件已存在: {config_path}")
        resp = input("是否覆盖? (y/N): ").strip().lower()
        if resp != 'y':
            print("已取消")
            return

    config = DEFAULT_CONFIG.copy()

    config["shop_name"] = input(f"店铺名称 [{config['shop_name']}]: ").strip() or config["shop_name"]

    # 平台配置
    for platform in ["meituan", "eleme", "jd"]:
        names = {"meituan": "美团外卖", "eleme": "饿了么/淘宝闪购", "jd": "京东外卖"}
        print(f"\n📱 {names[platform]}:")
        enable = input("  是否启用API对接? (y/N): ").strip().lower()
        if enable == 'y':
            config["platforms"][platform]["enabled"] = True
            config["platforms"][platform]["shop_id"] = input("  店铺ID: ").strip()
            config["platforms"][platform]["api_key"] = input("  API密钥: ").strip()

    # 告警阈值
    print("\n⚙️  告警阈值设置 (直接回车使用默认值):")
    th = config["alert_thresholds"]
    th["taste_negative_ratio"] = float(
        input(f"  口味负面占比告警线% [{th['taste_negative_ratio']}]: ").strip() or th["taste_negative_ratio"]
    )
    th["delivery_issue_ratio"] = float(
        input(f"  配送问题告警线% [{th['delivery_issue_ratio']}]: ").strip() or th["delivery_issue_ratio"]
    )
    th["service_negative_ratio"] = float(
        input(f"  服务负面告警线% [{th['service_negative_ratio']}]: ").strip() or th["service_negative_ratio"]
    )
    th["low_rating_threshold"] = float(
        input(f"  低评分告警线 [{th['low_rating_threshold']}]: ").strip() or th["low_rating_threshold"]
    )

    save_config(config)
    print("\n✅ 初始化完成!")
    print(f"   报告目录: {os.path.expanduser(config['report_dir'])}")
    print(f"   数据目录: {os.path.expanduser(config['data_dir'])}")


def cmd_analyze(file_path: str, platform: str = None, config: dict = None):
    """分析评价数据"""
    print("🍔 外卖评价智能监控")
    print("=" * 50)

    # 加载数据
    loader = ReviewDataLoader(
        data_dir=os.path.expanduser(
            (config or DEFAULT_CONFIG)["data_dir"]
        )
    )
    df = loader.load(file_path, platform=platform)

    # 分析
    print("\n🔍 正在分析评价数据...")
    result = analyze_reviews(df)

    # 预览文本摘要
    print("\n" + generate_summary_text(result))

    # 生成HTML报告
    report_dir = os.path.expanduser(
        (config or DEFAULT_CONFIG)["report_dir"]
    )
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shop_name = (config or DEFAULT_CONFIG).get("shop_name", "report")
    report_path = os.path.join(report_dir, f"review_report_{shop_name}_{timestamp}.html")

    generate_html_report(result, output_path=report_path)
    print(f"\n📄 HTML报告: {report_path}")

    # 返回结果供外部调用
    return {
        "report_path": report_path,
        "result": result,
        "anomaly_count": len(result.get("anomalies", [])),
    }


def cmd_compare(new_file: str, old_file: str, config: dict = None):
    """对比两个时段的评价"""
    print("🍔 外卖评价对比分析")
    print("=" * 50)

    df_new = load_reviews(new_file)
    df_old = load_reviews(old_file)

    print(f"\n📊 新数据: {len(df_new)} 条 | 旧数据: {len(df_old)} 条")

    comparison = compare_periods(df_new, df_old)

    # 显示变化
    changes = comparison.get("changes", {})
    print("\n📈 变化摘要:")
    print(f"   差评率变化: {changes.get('negative_ratio_change', 0):+.1f}%")
    print(f"   情感评分变化: {changes.get('sentiment_score_change', 0):+.3f}")

    dim_changes = changes.get("dimensions", {})
    if dim_changes:
        print("\n📋 各维度差评率变化:")
        for dim, data in dim_changes.items():
            emoji = {"口味": "👅", "配送": "🚀", "服务": "💁", "价格": "💰"}.get(dim, "📌")
            print(f"   {emoji} {dim}: {data.get('negative_ratio_change', 0):+.1f}%")

    # 生成对比报告
    report_dir = os.path.expanduser(
        (config or DEFAULT_CONFIG)["report_dir"]
    )
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"compare_report_{timestamp}.html")

    # 合并分析结果用于报告
    result = analyze_reviews(df_new)
    result["comparison"] = comparison
    generate_html_report(result, output_path=report_path)
    print(f"\n📄 对比报告: {report_path}")

    return {"report_path": report_path, "comparison": comparison}


def cmd_history(days: int = 30, config: dict = None):
    """查看历史摘要"""
    data_dir = os.path.expanduser(
        (config or DEFAULT_CONFIG)["data_dir"]
    )
    history = load_history(data_dir)

    if history.empty:
        print("📭 暂无历史评价数据")
        print("   请先使用 --file 参数导入评价数据")
        return

    total = len(history)
    print(f"📊 历史评价数据概览 (共 {total} 条)")
    print("=" * 50)

    if 'review_time' in history.columns:
        times = history['review_time'].dropna()
        if len(times) > 0:
            print(f"   时间范围: {times.min()} ~ {times.max()}")

    if 'platform' in history.columns:
        platforms = history['platform'].value_counts()
        for p, c in platforms.items():
            names = {"meituan": "美团外卖", "eleme": "饿了么/闪购", "jd": "京东外卖"}
            print(f"   {names.get(p, p)}: {c} 条")

    if 'rating' in history.columns:
        ratings = history['rating'].dropna()
        if len(ratings) > 0:
            print(f"   平均评分: {ratings.mean():.2f}")
            print(f"   5星: {(ratings >= 4.5).sum()} | 4星: {((ratings >= 3.5) & (ratings < 4.5)).sum()} | "
                  f"3星: {((ratings >= 2.5) & (ratings < 3.5)).sum()} | "
                  f"1-2星: {(ratings < 2.5).sum()}")

    # 最近分析结果
    result = analyze_reviews(history)
    summary = generate_summary_text(result)
    print("\n" + summary)


def cmd_check():
    """快速检查模式 - 加载所有历史数据综合分析"""
    config = load_config() or DEFAULT_CONFIG
    data_dir = os.path.expanduser(config["data_dir"])
    history = load_history(data_dir)

    if history.empty:
        print("📭 暂无历史评价数据，请先导入数据")
        print("   用法: python monitor.py --file 评价数据.csv")
        return None

    print("🔍 正在分析历史评价数据...")
    result = analyze_reviews(history)

    report_dir = os.path.expanduser(config["report_dir"])
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shop_name = config.get("shop_name", "report")
    report_path = os.path.join(report_dir, f"daily_check_{shop_name}_{timestamp}.html")

    generate_html_report(result, output_path=report_path)

    # 检查是否有异常
    anomalies = result.get("anomalies", [])
    high_anomalies = [a for a in anomalies if a.get("severity") == "high"]

    print("\n" + generate_summary_text(result))
    print(f"\n📄 报告: {report_path}")

    if high_anomalies:
        print(f"\n🚨 发现 {len(high_anomalies)} 个高危异常，建议立即处理！")

    return {"report_path": report_path, "result": result}


def main():
    parser = argparse.ArgumentParser(
        description="🍔 外卖评价智能监控系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python monitor.py --setup                     # 初始化配置
  python monitor.py --file reviews.csv          # 分析CSV文件
  python monitor.py --file data.xlsx --platform meituan  # 指定平台
  python monitor.py --compare new.csv old.csv   # 对比两个时段
  python monitor.py --check                      # 快速检查（基于历史数据）
  python monitor.py --history                    # 查看历史摘要
        """
    )

    parser.add_argument("--setup", action="store_true", help="初始化配置")
    parser.add_argument("--file", type=str, help="评价数据文件路径 (CSV/XLSX)")
    parser.add_argument("--platform", type=str, choices=["meituan", "eleme", "jd"],
                        help="平台类型")
    parser.add_argument("--compare", nargs=2, metavar=("NEW", "OLD"),
                        help="对比两个时段的数据")
    parser.add_argument("--check", action="store_true", help="快速检查模式")
    parser.add_argument("--history", action="store_true", help="查看历史数据摘要")
    parser.add_argument("--days", type=int, default=30, help="历史数据天数")

    args = parser.parse_args()

    config = load_config()

    if args.setup:
        cmd_setup()
    elif args.compare:
        cmd_compare(args.compare[0], args.compare[1], config)
    elif args.file:
        cmd_analyze(args.file, args.platform, config)
    elif args.check:
        cmd_check()
    elif args.history:
        cmd_history(args.days, config)
    else:
        # 无参数时默认快速检查
        print("🍔 外卖评价智能监控")
        print("=" * 50)
        if config:
            print(f"店铺: {config.get('shop_name', '未设置')}")
            enabled_platforms = [
                p for p, v in config.get("platforms", {}).items() if v.get("enabled")
            ]
            if enabled_platforms:
                print(f"已启用API平台: {', '.join(enabled_platforms)}")
            else:
                print("API平台: 未启用（使用CSV导入模式）")
        print("\n用法提示:")
        print("  --setup    初始化配置")
        print("  --file     导入评价数据并分析")
        print("  --check    快速检查（基于历史数据）")
        print("  --compare  对比两个时段数据")
        print("  --history  查看历史摘要")


if __name__ == "__main__":
    main()
