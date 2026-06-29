#!/usr/bin/env python3
"""
广告投手 CLI - 统一命令行入口
用法: python cli.py <command> [options]

Commands:
  import <file>        导入广告数据文件
  analyze <file>       快速分析数据（摘要+异常+趋势）
  diagnose <file>      综合诊断（健康评分+问题清单）
  budget <file>        预算分配建议
  creative <file>      素材分析和疲劳度检测
  optimize <file>      全方位优化建议
  report <file>        生成可视化HTML报告
  compare <a> <b>      对比两个素材/计划
  config               显示/修改配置

Options:
  --output, -o PATH    指定输出文件路径
  --type TYPE          报告类型: daily/weekly/monthly/diagnose
  --format FORMAT      输出格式: text/json/html
"""

import sys
import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from data_manager import load_file, get_summary, save_normalized
from performance import diagnose, anomaly_detect, trend_analysis, campaign_ranking
from optimizer import budget_allocation, bid_optimizer, creative_analysis, ab_test_analysis
from report import generate_report


def print_usage():
    print(__doc__)


def print_separator(title=""):
    print(f"\n{'='*60}")
    if title:
        print(f"  {title}")
        print(f"{'='*60}")


def cmd_import(args):
    """导入数据"""
    if len(args) < 1:
        print("❌ 请指定数据文件路径")
        return

    file_path = args[0]
    output_path = None
    if "--output" in args or "-o" in args:
        idx = args.index("--output") if "--output" in args else args.index("-o")
        if idx + 1 < len(args):
            output_path = args[idx + 1]

    print(f"📥 正在导入: {file_path}")
    records, platform, meta = load_file(file_path)

    platform_names = {
        "tencent_ads": "腾讯广告",
        "ocean_engine": "巨量引擎", 
        "baidu_ads": "百度推广",
        "meta_ads": "Meta Ads",
        "google_ads": "Google Ads",
        "unknown": "未知平台"
    }

    print(f"✅ 导入成功")
    print(f"   平台: {platform_names.get(platform, '未知')}")
    print(f"   格式: {meta['format']}")
    print(f"   记录数: {len(records)} 条")

    summary = get_summary(records)
    print(f"\n📊 数据概览:")
    print(f"   日期范围: {summary.get('date_range', '未知')}")
    print(f"   总消耗: ¥{summary['total_cost']:,.2f}")
    print(f"   总曝光: {summary['total_impressions']:,}")
    print(f"   总点击: {summary['total_clicks']:,}")
    print(f"   总转化: {summary['total_conversions']:,}")
    print(f"   总收入: ¥{summary['total_revenue']:,.2f}")
    print(f"   ROAS: {summary['roas']}")
    print(f"   平均CPA: ¥{summary['avg_cpa']:.2f}")

    if output_path:
        save_normalized(records, output_path)
        print(f"\n💾 标准化数据已保存: {output_path}")


def cmd_analyze(args):
    """快速分析"""
    if len(args) < 1:
        print("❌ 请指定数据文件路径")
        return

    file_path = args[0]
    format_type = "text"

    if "--format" in args:
        idx = args.index("--format")
        if idx + 1 < len(args):
            format_type = args[idx + 1]

    records, platform, meta = load_file(file_path)
    summary = get_summary(records)
    anomalies = anomaly_detect(records)
    trends = trend_analysis(records)

    if format_type == "json":
        result = {
            "summary": summary,
            "anomalies": anomalies,
            "trends": trends,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return

    print_separator("📊 投放数据快速分析")
    print(f"\n💰 总消耗: ¥{summary['total_cost']:,.2f} | "
          f"总曝光: {summary['total_impressions']:,} | "
          f"总转化: {summary['total_conversions']:,}")
    print(f"📈 ROAS: {summary['roas']} | "
          f"ROI: {summary['roi']}% | "
          f"平均CPA: ¥{summary['avg_cpa']:.2f}")
    print(f"👆 CTR: {summary['avg_ctr']}% | "
          f"CVR: {summary['avg_cvr']}% | "
          f"CPC: ¥{summary['avg_cpc']:.2f}")

    if anomalies:
        print(f"\n🚨 检测到 {len(anomalies)} 个异常:")
        for a in anomalies[:5]:
            icon = "🔴" if a.get("severity") == "critical" else "🟡"
            print(f"   {icon} [{a.get('type')}] {a.get('message', '')}")
            if a.get("suggestion"):
                print(f"      💡 {a['suggestion']}")
    else:
        print(f"\n✅ 未检测到异常")

    print(f"\n📉 趋势信号: {trends.get('health_signal', '未知')}")
    print(f"   CTR趋势: {trends.get('ctr_direction', '未知')}")
    print(f"   CPA趋势: {trends.get('cpa_direction', '未知')}")


def cmd_diagnose(args):
    """综合诊断"""
    if len(args) < 1:
        print("❌ 请指定数据文件路径")
        return

    file_path = args[0]
    records, platform, meta = load_file(file_path)
    result = diagnose(records)

    print_separator("🔍 综合诊断报告")
    print(f"\n🏥 健康评分: {result['health_score']}/100 — {result['grade']}")

    if result["issues"]:
        print(f"\n⚠️ 发现 {len(result['issues'])} 个问题:")
        for issue in result["issues"]:
            icon = "🔴" if issue["severity"] == "critical" else "🟡" if issue["severity"] == "warning" else "🔵"
            print(f"   {icon} [{issue['item']}] {issue['message']}")

    anomalies = result.get("anomalies", [])
    if anomalies:
        print(f"\n🚨 {len(anomalies)} 个异常:")
        for a in anomalies[:5]:
            print(f"   • {a.get('message', '')}")

    trends = result.get("trends", {})
    print(f"\n📉 趋势信号: {trends.get('health_signal', '未知')}")


def cmd_budget(args):
    """预算分配建议"""
    if len(args) < 1:
        print("❌ 请指定数据文件路径")
        return

    file_path = args[0]
    records, platform, meta = load_file(file_path)
    result = budget_allocation(records)

    print_separator("💰 预算分配建议 (532法则)")
    total = result.get("total_budget", 0)
    print(f"\n总预算参考: ¥{total:,.2f}")

    tiers = result.get("tiers", {})
    for tier_name, tier_data in tiers.items():
        print(f"\n{'🟢' if 'A' in tier_name else '🟡' if 'B' in tier_name else '🔴'} {tier_name.replace('_', ' ')}")
        print(f"   预算: ¥{tier_data.get('amount', 0):,.2f} ({tier_data.get('budget_share', '')})")
        print(f"   策略: {tier_data.get('rule', '')}")
        for plan in tier_data.get("plans", []):
            print(f"   └─ {plan.get('name', '')}: ¥{plan.get('budget', 0):,.0f} | ROAS={plan.get('roas', 0)} | CPA=¥{plan.get('cpa', 0):.1f}")


def cmd_creative(args):
    """素材分析"""
    if len(args) < 1:
        print("❌ 请指定数据文件路径")
        return

    file_path = args[0]
    records, platform, meta = load_file(file_path)
    result = creative_analysis(records)

    print_separator("🎨 素材分析")
    health = result.get("health", {})
    print(f"\n素材总数: {result.get('total_creatives', 0)}")
    print(f"   🟢 健康: {health.get('fresh', 0)}")
    print(f"   🟡 注意: {health.get('warning', 0)}")
    print(f"   🔴 疲劳: {health.get('fatigued', 0)}")

    top = result.get("top_performer")
    if top:
        print(f"\n🏆 最佳素材: {top.get('name', '')}")
        print(f"   ROAS: {top.get('roas', 0)} | CTR: {top.get('ctr', 0)}% | CVR: {top.get('cvr', 0)}%")
        print(f"   CPA: ¥{top.get('cpa', 0):.1f} | 在线: {top.get('active_days', 0)}天")

    print(f"\n📋 优化建议:")
    for rec in result.get("recommendations", []):
        print(f"   [{rec.get('priority')}] {rec.get('type')}: {rec.get('message')}")
        print(f"   → {rec.get('action')}")


def cmd_optimize(args):
    """全方位优化建议"""
    if len(args) < 1:
        print("❌ 请指定数据文件路径")
        return

    file_path = args[0]
    records, platform, meta = load_file(file_path)

    budget = budget_allocation(records)
    bid = bid_optimizer(records)
    creative = creative_analysis(records)

    print_separator("🚀 全方位优化建议")

    print("\n📊 出价优化:")
    for rec in bid.get("recommendations", []):
        action_icon = {"建议加量": "🟢", "维持观察": "🔵", "谨慎观望": "🟡", "建议关停或大幅调整": "🔴", "数据不足": "⚪"}
        icon = action_icon.get(rec.get("action", ""), "⚪")
        print(f"   {icon} {rec.get('plan', '')}: {rec.get('action')}")
        print(f"      ROAS={rec.get('current_roas', 0)} CPA=¥{rec.get('current_cpa', 0):.1f}")
        print(f"      → {rec.get('suggestion', '')}")

    print(f"\n💡 通用建议:")
    for advice in bid.get("general_advice", []):
        print(f"   • {advice}")

    print(f"\n🎨 素材建议:")
    for rec in creative.get("recommendations", []):
        print(f"   [{rec.get('priority')}] {rec.get('message')}")
        print(f"   → {rec.get('action')}")


def cmd_report(args):
    """生成可视化报告"""
    if len(args) < 1:
        print("❌ 请指定数据文件路径")
        return

    file_path = args[0]
    report_type = "daily"
    output_path = None

    if "--type" in args:
        idx = args.index("--type")
        if idx + 1 < len(args):
            report_type = args[idx + 1]

    if "--output" in args or "-o" in args:
        idx = args.index("--output") if "--output" in args else args.index("-o")
        if idx + 1 < len(args):
            output_path = args[idx + 1]

    print(f"📊 正在生成 {report_type} 报告...")
    result = generate_report(file_path, report_type, output_path)
    print(f"✅ 报告已生成: {result}")


def cmd_compare(args):
    """对比两个素材"""
    if len(args) < 3:
        print("❌ 用法: python cli.py compare <数据文件> <素材A> <素材B>")
        return

    file_path = args[0]
    creative_a = args[1]
    creative_b = args[2]

    records, platform, meta = load_file(file_path)
    result = ab_test_analysis(records, creative_a, creative_b)

    if "error" in result:
        print(f"❌ {result['error']}")
        return

    print_separator(f"🔬 A/B测试对比: {creative_a} vs {creative_b}")

    a = result["creative_a"]
    b = result["creative_b"]
    print(f"\n{'指标':<10} {'A: ' + creative_a[:20]:<25} {'B: ' + creative_b[:20]:<25} {'胜出'}")
    print("-" * 70)
    for metric, comp in result.get("comparison", {}).items():
        a_val = a.get(metric.lower().replace(" ", "_"), 0) if hasattr(a, 'get') else 0
        print(f"{metric:<10} {comp}")

    winner = result.get("overall_winner", "未知")
    print(f"\n🏆 综合优胜: {winner}")
    print(f"💡 {result.get('recommendation', '')}")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    commands = {
        "import": cmd_import,
        "analyze": cmd_analyze,
        "diagnose": cmd_diagnose,
        "budget": cmd_budget,
        "creative": cmd_creative,
        "optimize": cmd_optimize,
        "report": cmd_report,
        "compare": cmd_compare,
        "help": lambda _: print_usage(),
        "--help": lambda _: print_usage(),
        "-h": lambda _: print_usage(),
    }

    if command in commands:
        try:
            commands[command](args)
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ 未知命令: {command}")
        print_usage()


if __name__ == "__main__":
    main()
