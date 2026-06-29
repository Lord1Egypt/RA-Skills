"""
session_cleaner.py — 清理过期 session 文件和临时文件

解决的问题：
  1. agents/*/sessions/ 下 .jsonl 持续堆积（当前 273 文件/311MB）
  2. memory/main.sqlite.tmp-* 残留临时文件
  3. workspace/data/temp_*.py 调试脚本残留
  4. .openclaw/ 根目录 .rejected.* .bak.* 残留

用法:
  python scripts/session_cleaner.py              # dry-run（-n），只报告不删除
  python scripts/session_cleaner.py --execute    # 实际删除
  python scripts/session_cleaner.py --keep 14    # 保留 N 天（默认 14）
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
OPENCLAW = WORKSPACE.parent
AGENTS_DIR = OPENCLAW / "agents"
MEMORY_DIR = OPENCLAW / "memory"
DATA_DIR = WORKSPACE / "data"

# ── 扫描 ──

def scan_old_sessions(keep_days=14):
    """扫描 agents/*/sessions/ 下过期文件"""
    found = []
    cutoff = (datetime.now() - timedelta(days=keep_days)).timestamp()

    if not AGENTS_DIR.exists():
        return found

    for agent_dir in AGENTS_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.exists():
            continue

        for f in sessions_dir.glob("*.jsonl"):
            # 跳过非 session 文件
            if any(skip in f.name for skip in [".trajectory.", "sessions.json", "usage-cost"]):
                continue
            if f.stat().st_mtime < cutoff:
                found.append({
                    "path": str(f),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                    "age_days": round((datetime.now().timestamp() - f.stat().st_mtime) / 86400, 1),
                    "type": "session",
                })

        # 扫描 trajectory 文件（通常伴随 session，可一同清理）
        for f in sessions_dir.glob("*.trajectory.jsonl"):
            if f.stat().st_mtime < cutoff:
                found.append({
                    "path": str(f),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                    "age_days": round((datetime.now().timestamp() - f.stat().st_mtime) / 86400, 1),
                    "type": "trajectory",
                })
        for f in sessions_dir.glob("*.trajectory-path.json"):
            if f.stat().st_mtime < cutoff:
                found.append({
                    "path": str(f),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                    "age_days": round((datetime.now().timestamp() - f.stat().st_mtime) / 86400, 1),
                    "type": "trajectory_path",
                })

    return found


def scan_temp_files():
    """扫描临时文件"""
    found = []

    # memory/ SQLite tmp
    if MEMORY_DIR.exists():
        for f in MEMORY_DIR.glob("main.sqlite.tmp-*"):
            found.append({
                "path": str(f),
                "size_kb": round(f.stat().st_size / 1024, 1),
                "age_days": round((datetime.now().timestamp() - f.stat().st_mtime) / 86400, 1),
                "type": "sqlite_tmp",
            })

    # workspace/data/ temp_*.py tmp_*.py
    if DATA_DIR.exists():
        for pattern in ["temp_*.py", "tmp_*.py", "bing_debug.png"]:
            for f in DATA_DIR.glob(pattern):
                if (datetime.now().timestamp() - f.stat().st_mtime) > 7 * 86400:
                    found.append({
                        "path": str(f),
                        "size_kb": round(f.stat().st_size / 1024, 1),
                        "age_days": round((datetime.now().timestamp() - f.stat().st_mtime) / 86400, 1),
                        "type": "temp_script",
                    })

    # workspace root tmp_*.py
    for pattern in ["tmp_*.py", "tmp_check_*.py", "tmp_debug*.py"]:
        for f in WORKSPACE.glob(pattern):
            if (datetime.now().timestamp() - f.stat().st_mtime) > 7 * 86400:
                found.append({
                    "path": str(f),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                    "age_days": round((datetime.now().timestamp() - f.stat().st_mtime) / 86400, 1),
                    "type": "workspace_tmp",
                })

    # .openclaw/ 根目录 rejected / bak
    for pattern in ["openclaw.json.rejected.*", "openclaw.json.bak.*", "openclaw.json.*.tmp",
                    "observe_queue.bak", "config/gateway.json.bak", "cron/jobs.json.bak"]:
        for f in OPENCLAW.glob(pattern):
            if (datetime.now().timestamp() - f.stat().st_mtime) > 7 * 86400:
                found.append({
                    "path": str(f),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                    "age_days": round((datetime.now().timestamp() - f.stat().st_mtime) / 86400, 1),
                    "type": "config_bak",
                })

    # 空目录
    for d in [WORKSPACE / "skills-temp", WORKSPACE / "snapshots" / "tmp"]:
        if d.exists():
            try:
                d.rmdir()
                found.append({"path": str(d), "size_kb": 0, "age_days": 0, "type": "empty_dir", "deleted": True})
            except OSError:
                pass

    return found


def execute_cleanup(items):
    """执行删除"""
    deleted = []
    for item in items:
        if item.get("deleted"):
            deleted.append(item)
            continue
        try:
            os.remove(item["path"])
            deleted.append(item)
        except Exception as e:
            print(f"  ❌ 删除失败 {item['path']}: {e}")
    return deleted


def run(dry_run=True, keep_days=14):
    sessions = scan_old_sessions(keep_days)
    temps = scan_temp_files()
    all_items = sessions + temps

    total_kb = sum(i["size_kb"] for i in all_items)

    print(f"=== session_cleaner {'DRY-RUN' if dry_run else 'EXECUTE'} ===")
    print(f"  保留 {keep_days} 天内文件")
    print(f"  找到 {len(all_items)} 个可清理项 ({total_kb:.0f} KB / {total_kb/1024:.1f} MB)")
    print()

    # 分组显示
    by_type = {}
    for item in all_items:
        t = item["type"]
        by_type.setdefault(t, []).append(item)

    for t, items in sorted(by_type.items()):
        kb = sum(i["size_kb"] for i in items)
        print(f"  {t}: {len(items)} 文件, {kb:.0f} KB")
        if len(items) <= 5:
            for item in items:
                print(f"    {Path(item['path']).name} ({item['size_kb']} KB, {item['age_days']}天)")

    if dry_run:
        print(f"\n  💡 使用 --execute 执行实际删除")
        return all_items

    # 执行删除
    deleted = execute_cleanup(all_items)
    print(f"\n  ✅ 已删除 {len(deleted)} 个文件")
    return deleted

# ── Health report ──
try:
    from system_health import task_report
    task_report("session_cleaner", status="ok")
except Exception:
    pass


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true", help="实际删除（默认 dry-run）")
    p.add_argument("--keep", type=int, default=14, help="保留天数")
    args = p.parse_args()
    run(dry_run=not args.execute, keep_days=args.keep)
