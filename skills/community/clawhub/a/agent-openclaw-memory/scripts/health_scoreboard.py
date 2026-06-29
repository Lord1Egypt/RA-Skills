"""
health_scoreboard.py — 每日可靠性指标

从 system_health.json 历史数据计算管道成功率、平均延迟、待处理异常。
推送到微信，一行数字就够了，不用 Grafana。

用法: python scripts/health_scoreboard.py
"""
import json
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path(__file__).parent.parent
DATA = WORKSPACE / "data"
HEALTH_FILE = DATA / "system_health.json"


def rolling_stats():
    """从 system_health 计算累计指标"""
    if not HEALTH_FILE.exists():
        return None

    with open(HEALTH_FILE, encoding="utf-8") as f:
        health = json.load(f)

    tasks = health.get("tasks", {})
    if not tasks:
        return None

    total = 0
    ok = 0
    warn = 0
    fail = 0
    durations = []

    for name, data in tasks.items():
        if not isinstance(data, dict):
            continue
        tr = data.get("total_runs", 0)
        tf = data.get("total_failures", 0)
        dur = data.get("last_duration_ms", 0)
        status = data.get("last_status", "?")

        total += tr
        fail += tf
        if status == "warning": warn += 1
        if dur > 0: durations.append(dur)

    if total == 0:
        return None

    ok = total - fail - warn
    success_rate = round(ok / total * 100, 1) if total > 0 else 0
    avg_duration = round(sum(durations) / len(durations) / 1000, 1) if durations else 0

    issues = []
    for name, data in tasks.items():
        if not isinstance(data, dict): continue
        cf = data.get("consecutive_failures", 0)
        status = data.get("last_status", "?")
        if cf >= 2 or status == "error":
            issues.append(f"{name}:{status}(x{cf})")

    return {
        "total_runs": total,
        "ok": ok,
        "warn": warn,
        "fail": fail,
        "success_rate": success_rate,
        "avg_duration_s": avg_duration,
        "active_issues": issues,
        "score": health.get("system_health_score", "?"),
    }


def main():
    stats = rolling_stats()
    if not stats:
        print("暂无数据")
        return

    print(f"=== 系统可靠性 ===")
    s = stats
    print(f"管道成功率: {s['success_rate']}% ({s['ok']}/{s['total_runs']})")
    print(f"平均延迟:   {s['avg_duration_s']}s")
    print(f"健康评分:   {stats['score']}/100")
    if stats["active_issues"]:
        print(f"待处理:     {len(stats['active_issues'])} 项")
        for i in stats["active_issues"][:5]:
            print(f"  - {i}")
    else:
        print("待处理:     无")


if __name__ == "__main__":
    main()
