#!/usr/bin/env python3
"""自动化告警管理 - 付费版

用法:
    python3 alert_manager.py --action list
    python3 alert_manager.py --action add --metric cpu --threshold 90 --operator gt
    python3 alert_manager.py --action delete --id 1
    python3 alert_manager.py --action check
"""

import argparse
import json
import os
import sys
from datetime import datetime

ALERT_RULES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "alert_rules.json",
)

# 默认告警规则
DEFAULT_RULES = [
    {
        "id": 1,
        "name": "CPU使用率过高",
        "metric": "cpu",
        "operator": "gt",
        "threshold": 90,
        "enabled": True,
        "severity": "warning",
        "message": "CPU使用率超过{threshold}%，当前: {value}%",
    },
    {
        "id": 2,
        "name": "内存使用率过高",
        "metric": "memory",
        "operator": "gt",
        "threshold": 85,
        "enabled": True,
        "severity": "warning",
        "message": "内存使用率超过{threshold}%，当前: {value}%",
    },
    {
        "id": 3,
        "name": "磁盘空间不足",
        "metric": "disk",
        "operator": "gt",
        "threshold": 80,
        "enabled": True,
        "severity": "critical",
        "message": "磁盘使用率超过{threshold}%，当前: {value}%",
    },
    {
        "id": 4,
        "name": "系统负载过高",
        "metric": "load",
        "operator": "gt",
        "threshold": 4,
        "enabled": True,
        "severity": "warning",
        "message": "系统负载超过{threshold}，当前: {value}",
    },
]


def load_rules():
    """加载告警规则"""
    if os.path.exists(ALERT_RULES_FILE):
        with open(ALERT_RULES_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_RULES.copy()


def save_rules(rules):
    """保存告警规则"""
    with open(ALERT_RULES_FILE, "w") as f:
        json.dump(rules, ensure_ascii=False, indent=2, fp=f)


def get_cpu_usage():
    """获取CPU使用率"""
    try:
        with open("/proc/stat", "r") as f:
            parts = f.readline().split()
        user, nice, system, idle, iowait = (int(parts[i]) for i in range(1, 6))
        total = user + nice + system + idle + iowait
        return round((1 - (idle + iowait) / total) * 100, 1)
    except Exception:
        return 0


def get_memory_usage():
    """获取内存使用率"""
    try:
        with open("/proc/meminfo", "r") as f:
            info = {}
            for line in f:
                parts = line.split()
                info[parts[0].rstrip(":")] = int(parts[1])
        total = info.get("MemTotal", 1)
        available = info.get("MemAvailable", info.get("MemFree", 0))
        return round((total - available) / total * 100, 1)
    except Exception:
        return 0


def get_disk_usage():
    """获取磁盘使用率"""
    try:
        stat = os.statvfs("/")
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bavail * stat.f_frsize
        return round((total - free) / total * 100, 1)
    except Exception:
        return 0


def get_load():
    """获取1分钟负载"""
    try:
        with open("/proc/loadavg", "r") as f:
            return float(f.read().split()[0])
    except Exception:
        return 0


def check_metric(metric):
    """获取当前指标值"""
    funcs = {
        "cpu": get_cpu_usage,
        "memory": get_memory_usage,
        "disk": get_disk_usage,
        "load": get_load,
    }
    return funcs.get(metric, lambda: 0)()


def check_alerts(rules):
    """检查告警触发"""
    triggered = []
    for rule in rules:
        if not rule.get("enabled", True):
            continue
        current = check_metric(rule["metric"])
        threshold = rule["threshold"]
        op = rule["operator"]

        is_triggered = False
        if op == "gt" and current > threshold:
            is_triggered = True
        elif op == "lt" and current < threshold:
            is_triggered = True
        elif op == "gte" and current >= threshold:
            is_triggered = True
        elif op == "lte" and current <= threshold:
            is_triggered = True
        elif op == "eq" and current == threshold:
            is_triggered = True

        if is_triggered:
            msg = rule["message"].format(threshold=threshold, value=current)
            triggered.append({
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "metric": rule["metric"],
                "current": current,
                "threshold": threshold,
                "severity": rule["severity"],
                "message": msg,
            })

    return triggered


def format_text_rules(rules):
    """格式化规则列表"""
    lines = []
    lines.append("\n🔔 告警规则列表")
    lines.append("=" * 45)
    for r in rules:
        status = "✅" if r.get("enabled", True) else "⏸️"
        sev_emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(r["severity"], "⚪")
        lines.append(f"  {status} #{r['id']} {sev_emoji} {r['name']}")
        lines.append(f"     指标: {r['metric']} | 阈值: {r['operator']} {r['threshold']}")
    return "\n".join(lines)


def format_text_alerts(triggered):
    """格式化触发的告警"""
    if not triggered:
        return "\n✅ 所有指标正常，无告警触发"

    lines = []
    lines.append("\n🚨 触发的告警")
    lines.append("=" * 45)
    for a in triggered:
        sev = a["severity"]
        emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(sev, "⚪")
        lines.append(f"  {emoji} [{sev.upper()}] {a['rule_name']}")
        lines.append(f"     {a['message']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw自动化告警管理")
    parser.add_argument(
        "--action",
        choices=["list", "add", "delete", "check", "enable", "disable"],
        default="check",
        help="操作类型",
    )
    parser.add_argument("--metric", help="指标名称 (cpu/memory/disk/load)")
    parser.add_argument("--threshold", type=float, help="阈值")
    parser.add_argument("--operator", choices=["gt", "lt", "gte", "lte", "eq"],
                        default="gt", help="比较操作符")
    parser.add_argument("--name", help="告警名称")
    parser.add_argument("--severity", choices=["critical", "warning", "info"],
                        default="warning", help="严重级别")
    parser.add_argument("--id", type=int, help="规则ID")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    rules = load_rules()

    if args.action == "list":
        if args.json:
            print(json.dumps(rules, ensure_ascii=False, indent=2))
        else:
            print(format_text_rules(rules))

    elif args.action == "add":
        if not args.metric:
            print("❌ 请指定 --metric 参数")
            sys.exit(1)
        if args.threshold is None:
            print("❌ 请指定 --threshold 参数")
            sys.exit(1)

        max_id = max((r["id"] for r in rules), default=0)
        new_rule = {
            "id": max_id + 1,
            "name": args.name or f"{args.metric}告警",
            "metric": args.metric,
            "operator": args.operator,
            "threshold": args.threshold,
            "enabled": True,
            "severity": args.severity,
            "message": f"{args.name or args.metric}: {{value}} 超过阈值 {{threshold}}",
        }
        rules.append(new_rule)
        save_rules(rules)
        print(f"✅ 告警规则已添加: #{new_rule['id']} {new_rule['name']}")

    elif args.action == "delete":
        if not args.id:
            print("❌ 请指定 --id 参数")
            sys.exit(1)
        rules = [r for r in rules if r["id"] != args.id]
        save_rules(rules)
        print(f"✅ 告警规则 #{args.id} 已删除")

    elif args.action == "check":
        triggered = check_alerts(rules)
        # 同时显示当前值
        metrics = ["cpu", "memory", "disk", "load"]
        if args.json:
            print(json.dumps({
                "metrics": {m: check_metric(m) for m in metrics},
                "triggered": triggered,
                "timestamp": datetime.now().isoformat(),
            }, ensure_ascii=False, indent=2))
        else:
            lines = []
            lines.append("\n📊 当前指标")
            lines.append("=" * 45)
            for m in metrics:
                val = check_metric(m)
                unit = "%" if m in ("cpu", "memory", "disk") else ""
                lines.append(f"  {m}: {val}{unit}")
            print("\n".join(lines))
            print(format_text_alerts(triggered))

    elif args.action in ("enable", "disable"):
        if not args.id:
            print("❌ 请指定 --id 参数")
            sys.exit(1)
        for r in rules:
            if r["id"] == args.id:
                r["enabled"] = (args.action == "enable")
                break
        save_rules(rules)
        status = "启用" if args.action == "enable" else "禁用"
        print(f"✅ 告警规则 #{args.id} 已{status}")


if __name__ == "__main__":
    main()
