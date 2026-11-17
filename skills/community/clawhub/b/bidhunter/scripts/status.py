#!/usr/bin/env python3
"""
status.py - BidHunter采集状态查看工具

Usage:
  python3 status.py [cache_dir] [rules_file]

  cache_dir: 缓存目录路径（默认: bid_cache/）
  rules_file: 规则库路径（默认: qual_rules.json）
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


def load_rules(rules_path):
    if not os.path.exists(rules_path):
        return None
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl_count(file_path):
    """Count lines in a jsonl file."""
    if not os.path.exists(file_path):
        return 0
    count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return count


def file_age_hours(file_path):
    """Return age of file in hours as float."""
    if not os.path.exists(file_path):
        return None
    mtime = os.path.getmtime(file_path)
    now = datetime.now().timestamp()
    return (now - mtime) / 3600


def freshness_label(hours):
    """Return emoji + label for freshness."""
    if hours is None:
        return ("🔴", "无数据")
    if hours < 1:
        return ("🟢", "刚刚更新")
    if hours < 4:
        return ("🟢", f"{hours:.1f}h 前")
    if hours < 12:
        return ("🟡", f"{hours:.1f}h 前")
    return ("🔴", f"{hours:.1f}h 前")


def dir_size_kb(dir_path):
    """Return total size of directory in KB."""
    if not os.path.exists(dir_path):
        return 0
    total = 0
    for root, _, files in os.walk(dir_path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total / 1024


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Determine cache_dir and rules_file
    if len(sys.argv) >= 2:
        cache_dir = sys.argv[1]
    else:
        cache_dir = os.path.join(script_dir, "bid_cache")

    if len(sys.argv) >= 3:
        rules_file = sys.argv[2]
    else:
        rules_file = os.path.join(script_dir, "qual_rules.json")

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    print("=" * 52)
    print(f"  BidHunter 采集状态  {now.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 52)
    print()

    # --- Cache directory ---
    print(f"📁 缓存目录: {cache_dir}")
    if os.path.exists(cache_dir):
        size_kb = dir_size_kb(cache_dir)
        print(f"   大小: {size_kb:.1f} KB")
    else:
        print("   状态: 目录不存在（尚未采集）")
    print()

    # --- Today's data ---
    today_cache = os.path.join(cache_dir, f"bid_{today_str}.jsonl")
    today_count = load_jsonl_count(today_cache)
    age_h = file_age_hours(today_cache)
    freshness_emoji, freshness_label_text = freshness_label(age_h)

    print(f"📊 今日数据 ({today_str}):")
    print(f"   条数: {today_count} 条  {freshness_emoji} {freshness_label_text}")
    if age_h is not None:
        print(f"   文件: {today_cache}")
    print()

    # --- Last 7 days trend ---
    print("📈 近7天趋势:")
    days = []
    for i in range(7):
        day = now - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        day_file = os.path.join(cache_dir, f"bid_{day_str}.jsonl")
        cnt = load_jsonl_count(day_file)
        age_h = file_age_hours(day_file)
        age_str = f"({age_h:.0f}h ago)" if age_h else ""
        bar = "█" * min(cnt, 20) + "░" * max(0, 20 - cnt)
        marker = "←今日" if i == 0 else ""
        print(f"   {day_str}: {bar} {cnt:3d} {marker}")
    print()

    # --- Rules summary ---
    rules = load_rules(rules_file)
    if rules:
        entities = rules.get("entities", {})
        red_alerts = rules.get("red_alerts", [])
        special_rules = rules.get("special_rules", [])
        total_caps = sum(len(e.get("capabilities", [])) for e in entities.values())

        print(f"📋 规则库摘要 ({rules_file}):")
        print(f"   版本: {rules.get('version', 'unknown')}")
        print(f"   主体数: {len(entities)} 个")
        print(f"   能力词总数: {total_caps} 个")
        print(f"   红色预警: {len(red_alerts)} 项")
        print(f"   特殊规则: {len(special_rules)} 条")
        print(f"   重点地区: {', '.join(rules.get('region_priority', {}).get('high', [])) or '未配置'}")
        print()
    else:
        print("📋 规则库: 未找到或加载失败")
        print()

    # --- Health summary ---
    print("🏥 健康总结:")
    if today_count > 0:
        print("   ✅ 今日数据已采集")
    else:
        print("   ⚠️  今日暂无数据，请运行 pipeline.sh")

    if age_h is not None and age_h > 12:
        print(f"   ⚠️  数据超过12小时未更新，建议重新采集")
    elif age_h is not None and age_h < 4:
        print("   ✅ 数据新鲜")

    if rules:
        if not entities:
            print("   ⚠️  规则库缺少主体配置（entities），需编辑 qual_rules.json")
        if not all(e.get("capabilities") for e in entities.values()):
            print("   ⚠️  部分主体能力词为空，请检查 qual_rules.json")
    else:
        print("   ⚠️  规则库加载失败，请检查文件路径")
    print()

    # --- Next steps ---
    print("📌 下一步操作建议:")
    print("   1. 查看报告: bash pipeline.sh --dry-run")
    print("   2. 精华版:   bash pipeline.sh --dry-run --summary")
    print("   3. 强制采集: bash pipeline.sh --fresh")
    print("   4. 定时任务: 配置每日 10:00 自动运行 pipeline.sh")
    print()

    # --- Push status (v1.2) ---
    push_cfg = os.path.expanduser("~/.config/bidhunter/push.json")
    print("📮 推送状态:")
    if os.path.exists(push_cfg):
        try:
            sys.path.insert(0, script_dir)
            import push_manager
            st = push_manager.get_stats()
            hc = push_manager.health_check()
            chs = [c for c, n, ok in st["by_channel"]]
            print(f"   通道: {', '.join(chs) if chs else '已配置但无推送记录'}")
            print(f"   累计: {st['total']} 条（成功 {st['success']} / 失败 {st['failed']}）")
            print(f"   近3天: 成功 {hc['recent_ok_3d']} / 失败 {hc['recent_fail_3d']}"
                  + ("  🚨 触发告警" if hc["alert"] else "  ✅"))
        except Exception as e:  # noqa: BLE001
            print(f"   ⚠️ 推送统计读取失败: {e}")
    else:
        print("   ⚪ 未配置推送（运行 python3 scripts/config_wizard.py）")
    print()


def main_push_stats():
    """--push-stats 子命令：详细推送统计。"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    import push_manager
    st = push_manager.get_stats()
    hc = push_manager.health_check()
    print("📮 推送统计")
    print(f"   累计: {st['total']} 条 | 成功 {st['success']} | 失败 {st['failed']}")
    for ch, n, ok in st["by_channel"]:
        rate = (ok or 0) / n * 100 if n else 0
        print(f"   {ch}: {n} 条，成功率 {rate:.0f}%")
    print(f"   近3天: 成功 {hc['recent_ok_3d']} / 失败 {hc['recent_fail_3d']}")
    print("   告警: " + ("🚨 触发（连续失败）" if hc["alert"] else "✅ 正常"))


if __name__ == "__main__":
    if "--push-stats" in sys.argv:
        main_push_stats()
    else:
        main()
