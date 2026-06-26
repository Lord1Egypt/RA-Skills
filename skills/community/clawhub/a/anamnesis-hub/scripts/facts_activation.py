#!/usr/bin/env python3
"""
facts_activation.py - facts.db 激活与衰减系统

实现 Hebbian activation(访问即升温)+ 每日衰减 + Hot/Warm/Cool 三级分类。
可独立调用,也可被 daily-memory-pipeline.sh 调用。

用法:
  python3 facts_activation.py activate --entity Emby --key ip
  python3 facts_activation.py decay
  python3 facts_activation.py classify
  python3 facts_activation.py stats
  python3 facts_activation.py gc --threshold 0.01   # 清理 COOL 事实
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

FACTS_DB = Path.home() / ".openclaw" / "memory" / "facts.sqlite"

# ─── 热度阈值 ────────────────────────────────────────────────────────────────
HOT_THRESHOLD = 2.0    # activation > 2.0 = HOT(高频访问,MEMORY.md 索引层)
COOL_THRESHOLD = 0.02  # activation < 0.02 = COOL(低频,候选清理)
DECAY_RATE = 0.95      # 每日衰减系数(非永久事实)


def get_conn() -> sqlite3.Connection:
    if not FACTS_DB.exists():
        print(json.dumps({"status": "error", "message": "facts.db not found. Run seed-facts-db.py first."}))
        sys.exit(1)
    conn = sqlite3.connect(str(FACTS_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def cmd_activate(entity: str, key: str):
    """查询时触发 Hebbian activation: access_count+1, activation+0.5"""
    conn = get_conn()
    cursor = conn.execute("""
        UPDATE facts
        SET access_count = access_count + 1,
            activation = activation + 0.5,
            last_accessed = datetime('now')
        WHERE entity = ? AND key = ?
    """, (entity, key))
    if cursor.rowcount == 0:
        print(json.dumps({"status": "not_found", "entity": entity, "key": key}))
    else:
        row = conn.execute(
            "SELECT activation, access_count, last_accessed FROM facts WHERE entity=? AND key=?",
            (entity, key)
        ).fetchone()
        conn.commit()
        print(json.dumps({
            "status": "activated",
            "entity": entity, "key": key,
            "activation": round(row[0], 4),
            "access_count": row[1],
            "last_accessed": row[2],
        }))
    conn.close()


def cmd_decay():
    """每日衰减:非永久事实 activation *= DECAY_RATE(底限 0.005)"""
    conn = get_conn()
    cursor = conn.execute("""
        UPDATE facts
        SET activation = MAX(activation * ?, 0.005)
        WHERE permanent = 0
    """, (DECAY_RATE,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    print(json.dumps({
        "status": "decayed",
        "decay_rate": DECAY_RATE,
        "affected_facts": affected,
        "timestamp": datetime.now().isoformat(),
    }))


def cmd_classify():
    """三级分类:HOT / WARM / COOL"""
    conn = get_conn()
    stats = {
        "HOT": conn.execute(
            "SELECT COUNT(*) FROM facts WHERE activation > ?", (HOT_THRESHOLD,)
        ).fetchone()[0],
        "WARM": conn.execute(
            "SELECT COUNT(*) FROM facts WHERE activation BETWEEN ? AND ?",
            (COOL_THRESHOLD, HOT_THRESHOLD)
        ).fetchone()[0],
        "COOL": conn.execute(
            "SELECT COUNT(*) FROM facts WHERE activation < ?", (COOL_THRESHOLD,)
        ).fetchone()[0],
    }

    # 列出 HOT 事实(最可能出现在 MEMORY.md 索引层)
    hot_facts = conn.execute(
        "SELECT entity, key, substr(value,1,40), activation FROM facts WHERE activation > ? ORDER BY activation DESC LIMIT 10",
        (HOT_THRESHOLD,)
    ).fetchall()

    # 列出 COOL 事实(候选清理)
    cool_facts = conn.execute(
        "SELECT entity, key, substr(value,1,40), activation FROM facts WHERE activation < ? ORDER BY activation ASC LIMIT 5",
        (COOL_THRESHOLD,)
    ).fetchall()

    conn.close()

    print(json.dumps({
        "status": "classified",
        "thresholds": {"HOT": HOT_THRESHOLD, "COOL": COOL_THRESHOLD},
        "distribution": stats,
        "hot_top10": [{"entity": r[0], "key": r[1], "value_preview": r[2], "activation": round(r[3],4)} for r in hot_facts],
        "cool_bottom5": [{"entity": r[0], "key": r[1], "value_preview": r[2], "activation": round(r[3],4)} for r in cool_facts],
    }, ensure_ascii=False, indent=2))


def cmd_stats():
    """数据库统计"""
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
    entities = conn.execute("SELECT COUNT(DISTINCT entity) FROM facts").fetchone()[0]
    permanent = conn.execute("SELECT COUNT(*) FROM facts WHERE permanent=1").fetchone()[0]
    total_access = conn.execute("SELECT SUM(access_count) FROM facts").fetchone()[0] or 0
    avg_activation = conn.execute("SELECT ROUND(AVG(activation), 4) FROM facts").fetchone()[0] or 0
    top_entity = conn.execute(
        "SELECT entity, COUNT(*) as cnt FROM facts GROUP BY entity ORDER BY cnt DESC LIMIT 1"
    ).fetchone()

    # 前5激活事实
    top5 = conn.execute(
        "SELECT entity, key, activation, access_count FROM facts ORDER BY activation DESC LIMIT 5"
    ).fetchall()

    conn.close()

    print(json.dumps({
        "status": "ok",
        "total_facts": total,
        "entities": entities,
        "permanent": permanent,
        "total_accesses": total_access,
        "avg_activation": avg_activation,
        "top_entity": f"{top_entity[0]} ({top_entity[1]} facts)" if top_entity else "N/A",
        "top5_by_activation": [
            {"entity": r[0], "key": r[1], "activation": round(r[2],4), "access_count": r[3]}
            for r in top5
        ],
    }, ensure_ascii=False, indent=2))


def cmd_gc(threshold: float = 0.01, force: bool = False):
    """垃圾回收：清理 COOL 事实"""
    conn = get_conn()
    candidates = conn.execute(
        "SELECT entity, key, activation FROM facts WHERE permanent=0 AND activation < ?",
        (threshold,)
    ).fetchall()

    if not candidates:
        print(json.dumps({"status": "ok", "message": "no facts eligible for GC", "candidates": 0}))
        conn.close()
        return

    print(json.dumps({
        "status": "preview",
        "candidates": len(candidates),
        "threshold": threshold,
        "preview": [{"entity": r[0], "key": r[1], "activation": round(r[2], 4)} for r in candidates[:10]],
    }, ensure_ascii=False, indent=2))

    if force:
        deleted = conn.execute(
            "DELETE FROM facts WHERE permanent=0 AND activation < ?",
            (threshold,)
        ).rowcount
        conn.commit()
        print(json.dumps({"status": "ok", "deleted": deleted}), file=sys.stderr)

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="facts.db activation & decay system")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("decay", help="Daily activation decay for non-permanent facts")
    sub.add_parser("classify", help="Show Hot/Warm/Cool distribution")
    sub.add_parser("stats", help="Database statistics")

    act = sub.add_parser("activate", help="Trigger Hebbian activation on fact access")
    act.add_argument("--entity", required=True)
    act.add_argument("--key", required=True)

    gc = sub.add_parser("gc", help="Preview GC candidates (use --force to delete)")
    gc.add_argument("--threshold", type=float, default=0.01)
    gc.add_argument("--force", action="store_true", help="实际执行删除(默认仅预览)")

    args = parser.parse_args()

    if args.command == "activate":
        cmd_activate(args.entity, args.key)
    elif args.command == "decay":
        cmd_decay()
    elif args.command == "classify":
        cmd_classify()
    elif args.command == "stats":
        cmd_stats()
    elif args.command == "gc":
        cmd_gc(args.threshold, args.force)
    elif args.command == "gc":
        cmd_gc(args.threshold)


if __name__ == "__main__":
    main()
