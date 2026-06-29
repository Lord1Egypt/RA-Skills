#!/usr/bin/env python3
"""
艾宾浩斯遗忘曲线复习引擎
- 根据复习间隔计算下次复习日期
- daily-review：输出今日应复习的条目列表
- mark-reviewed：标记条目已复习，更新下次复习日期
- 复习间隔（天）：1, 2, 4, 7, 15, 30, 60, 120

调用 breadcrumb.py 的 review-records 获取数据
调用 breadcrumb.py 的 update_review_record 更新数据
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
BREADCRUMB_PY = str(SKILL_DIR / "scripts" / "breadcrumb.py")
TOPOLOGY_DONUT_PY = str(SKILL_DIR / "scripts" / "topology_donut.py")

# 艾宾浩斯复习间隔（天数）
EBBINGHAUS_INTERVALS = [1, 2, 4, 7, 15, 30, 60, 120]


def get_next_review_interval(review_count):
    """
    根据已复习次数，返回下次复习应间隔的天数
    review_count: 0 → 间隔1天 (第1次复习)
    review_count: 1 → 间隔2天 (第2次复习)
    ...
    超过列表长度则取最后一个
    """
    if review_count >= len(EBBINGHAUS_INTERVALS):
        return EBBINGHAUS_INTERVALS[-1]
    return EBBINGHAUS_INTERVALS[review_count]


def get_review_records():
    """从 breadcrumb.py 获取复习记录"""
    result = subprocess.run(
        [sys.executable, BREADCRUMB_PY, "review-records"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        print(json.dumps({"error": f"获取复习记录失败: {result.stderr}"}, ensure_ascii=False))
        sys.exit(1)
    data = json.loads(result.stdout)
    return data.get("records", [])


def update_review_record(entry_id, review_count, last_reviewed_at, next_review_at):
    """更新复习记录"""
    # 直接导入 breadcrumb 模块（同目录）
    scripts_dir = str(SKILL_DIR / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from breadcrumb import update_review_record as urr
    result = urr(entry_id, review_count, last_reviewed_at, next_review_at)
    return {"updated": result}


def get_pending_reviews(count=None):
    """
    获取今日应复习的条目
    规则：
    1. 所有 next_review_at <= 现在 的条目
    2. 优先选择最"紧急"的（next_review_at 最早的）
    3. 如果 count 指定，返回最多 count 条
    """
    records = get_review_records()
    now = datetime.now()

    pending = []
    for r in records:
        next_review = r.get("next_review_at")
        if next_review:
            try:
                nr_dt = datetime.fromisoformat(next_review)
                if nr_dt <= now:
                    pending.append(r)
            except ValueError:
                pass

    # 按紧急程度排序：最久未复习的优先
    pending.sort(key=lambda r: r.get("next_review_at", "9999"))

    if count and len(pending) > count:
        pending = pending[:count]

    return pending


def mark_reviewed(entry_id):
    """标记条目已复习，计算下次复习日期"""
    records = get_review_records()
    target = None
    for r in records:
        if r["id"] == entry_id:
            target = r
            break

    if not target:
        return {"error": f"条目 {entry_id} 不存在"}

    now = datetime.now()
    new_review_count = target.get("review_count", 0) + 1
    interval = get_next_review_interval(new_review_count - 1)  # 当前是第N次复习
    next_review = now + timedelta(days=interval)

    last_reviewed = now.isoformat()
    next_review_str = next_review.isoformat()

    result = update_review_record(entry_id, new_review_count, last_reviewed, next_review_str)

    return {
        "id": entry_id,
        "title": target.get("title", ""),
        "review_count": new_review_count,
        "last_reviewed_at": last_reviewed,
        "next_review_at": next_review_str,
        "interval_days": interval,
        "updated": result.get("updated", False)
    }


def reset_review(entry_id):
    """重置某条目的复习记录（从头开始）"""
    records = get_review_records()
    target = None
    for r in records:
        if r["id"] == entry_id:
            target = r
            break

    if not target:
        return {"error": f"条目 {entry_id} 不存在"}

    now = datetime.now()
    next_review = now + timedelta(days=1)  # 重置后1天后复习

    result = update_review_record(entry_id, 0, None, next_review.isoformat())
    return {
        "id": entry_id,
        "reset": True,
        "next_review_at": next_review.isoformat(),
        "updated": result.get("updated", False)
    }


def stats():
    """复习统计"""
    records = get_review_records()
    now = datetime.now()
    total = len(records)

    # 各复习阶段分布
    stage_dist = {}
    for r in records:
        rc = r.get("review_count", 0)
        stage = f"第{rc}次复习" if rc > 0 else "未复习"
        stage_dist[stage] = stage_dist.get(stage, 0) + 1

    # 今日待复习
    pending = sum(1 for r in records
                  if r.get("next_review_at") and r["next_review_at"] <= now.isoformat())

    # 平均复习次数
    avg_reviews = sum(r.get("review_count", 0) for r in records) / max(total, 1)

    return {
        "total_entries": total,
        "pending_review_today": pending,
        "avg_review_count": round(avg_reviews, 1),
        "stage_distribution": stage_dist,
        "intervals": EBBINGHAUS_INTERVALS
    }


def expand_topology(entry_id):
    """
    调用拓扑甜甜圈引擎，获取关联面包屑
    """
    try:
        result = subprocess.run(
            [sys.executable, TOPOLOGY_DONUT_PY, "expand", "--id", entry_id],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception as e:
        return {"error": f"拓扑扩展失败: {e}"}
    return {"error": "拓扑引擎调用失败"}


def daily_review_with_expand(count=None):
    """
    获取今日应复习条目，并附加拓扑甜甜圈关联扩展。
    每个待复习条目都会查询其所属甜甜圈及关联面包屑。
    """
    pending = get_pending_reviews(count=count)

    expanded = []
    for entry in pending:
        eid = entry.get("id", "")
        topology = expand_topology(eid)
        entry["_topology"] = topology
        expanded.append(entry)

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_pending": len(expanded),
        "intervals_used": EBBINGHAUS_INTERVALS,
        "entries": expanded,
        "note": "每个条目附带 _topology.expansions 展示拓扑甜甜圈关联扩展信息"
    }


def main():
    parser = argparse.ArgumentParser(description="艾宾浩斯复习引擎")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # daily-review
    review_parser = subparsers.add_parser("daily-review", help="获取今日应复习条目")
    review_parser.add_argument("--count", type=int, default=5, help="返回条数（默认5）")
    review_parser.add_argument("--expand", action="store_true", help="附加拓扑甜甜圈关联扩展")

    # daily-review-expand
    expand_review_parser = subparsers.add_parser("daily-review-expand",
        help="获取今日应复习条目并附加拓扑甜甜圈关联扩展（等同于 daily-review --expand）")
    expand_review_parser.add_argument("--count", type=int, default=5, help="返回条数（默认5）")

    # mark-reviewed
    mark_parser = subparsers.add_parser("mark-reviewed", help="标记条目已复习")
    mark_parser.add_argument("--id", required=True, help="条目ID")

    # expand-topology
    expand_parser = subparsers.add_parser("expand-topology",
        help="对指定条目进行拓扑甜甜圈关联扩展")
    expand_parser.add_argument("--id", required=True, help="条目ID")

    # reset
    reset_parser = subparsers.add_parser("reset", help="重置某条目复习记录")
    reset_parser.add_argument("--id", required=True, help="条目ID")

    # stats
    subparsers.add_parser("stats", help="复习统计")

    args = parser.parse_args()

    if args.command == "daily-review":
        if args.expand:
            result = daily_review_with_expand(count=args.count)
        else:
            pending = get_pending_reviews(count=args.count)
            result = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "total_pending": len(pending),
                "intervals_used": EBBINGHAUS_INTERVALS,
                "entries": pending
            }

    elif args.command == "daily-review-expand":
        result = daily_review_with_expand(count=args.count)

    elif args.command == "expand-topology":
        topology = expand_topology(args.id)
        # 同时获取条目基本信息
        from breadcrumb import show_entry
        entry = show_entry(args.id)
        result = {
            "entry": {"id": entry["id"], "title": entry.get("title", ""),
                      "tags": entry.get("tags", [])} if entry else None,
            "topology": topology
        }

    elif args.command == "mark-reviewed":
        result = mark_reviewed(args.id)

    elif args.command == "reset":
        result = reset_review(args.id)

    elif args.command == "stats":
        result = stats()

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
