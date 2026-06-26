#!/usr/bin/env python3
"""
daily_maintenance.py — 昨日任务总结与系统清理 v1.0

功能：
  1. 健康巡检（引擎状态/磁盘/gateway/异常检测）
  2. 垃圾扫描与清理（临时文件/__pycache__/旧日志/过期文件）
  3. 自纠错数据链路维护（verified_memories/reflexions/replay_buffer）
  4. 每日记忆维护（归档+索引）
  5. Dream-to-TODO 扫描
  6. ReplayBuffer 蒸馏
  7. 执行复盘（审计分析）

统一在凌晨 1:00 运行，合并为一个任务。
"""

import json, os, sys, time, shutil, glob, subprocess, gzip, re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

BEIJING_TZ = timezone(timedelta(hours=8))
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
ARCHIVE_DIR = os.path.join(MEMORY_DIR, ".archive")
STATE_FILE = os.path.join(WORKSPACE, ".daily_maintenance_state.json")
CLEANUP_LOG = os.path.join(WORKSPACE, ".logs", "cleanup_history.jsonl")


def load_state() -> Dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"last_run": "", "total_cleanups": 0, "total_issues": 0}


def save_state(state: Dict):
    state["last_run"] = datetime.now(BEIJING_TZ).isoformat()
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ── 1. 健康巡检 ───────────────────────────────
def health_check() -> Dict:
    """引擎/磁盘/gateway/异常检测"""
    issues = []
    checks = {}

    # 磁盘
    try:
        st = os.statvfs(WORKSPACE)
        free_gb = st.f_frsize * st.f_bavail / (1024**3)
        total_gb = st.f_blocks * st.f_frsize / (1024**3)
        usage_pct = (1 - st.f_bavail / max(st.f_blocks, 1)) * 100
        checks["disk"] = {"free_gb": round(free_gb, 1), "total_gb": round(total_gb, 1), "usage_pct": round(usage_pct, 1)}
        if free_gb < 1:
            issues.append("磁盘剩余空间不足 1GB")
        elif free_gb < 5:
            issues.append("磁盘剩余空间不足 5GB")
    except Exception as e:
        checks["disk"] = {"error": str(e)[:50]}
        issues.append(f"磁盘检测异常: {str(e)[:50]}")

    # Gateway 状态
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:18789/health", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            checks["gateway"] = {"status": status}
            if status != 200:
                issues.append(f"Gateway 返回非200状态: {status}")
    except Exception as e:
        checks["gateway"] = {"error": str(e)[:50]}
        issues.append(f"Gateway 不可达: {str(e)[:50]}")

    # 引擎目录完整性
    engine_groups = ["init", "memory", "quality", "operations", "workflow", "hooks", "tools", "compat"]
    for g in engine_groups:
        d = os.path.join(WORKSPACE, "core/engines", g)
        if not os.path.isdir(d):
            issues.append(f"引擎目录缺失: {g}")
    checks["engine_dirs"] = {g: os.path.isdir(os.path.join(WORKSPACE, "core/engines", g)) for g in engine_groups}

    # 关键数据文件
    critical_files = [".verified_memories.jsonl", ".reflexions.jsonl", ".evolution_log.json"]
    for fname in critical_files:
        fp = os.path.join(WORKSPACE, fname)
        if not os.path.exists(fp):
            issues.append(f"关键数据文件缺失: {fname}")

    return {"status": "ok" if not issues else "issues", "issues": issues, "checks": checks}


# ── 2. 垃圾扫描与清理 ────────────────────────────
def garbage_scan(clean: bool = False) -> Dict:
    """扫描并清理垃圾文件"""
    cleaned = 0
    freed_bytes = 0
    found = []

    # __pycache__ 目录
    for root, dirs, _ in os.walk(WORKSPACE):
        for d in dirs:
            if d == "__pycache__":
                full = os.path.join(root, d)
                try:
                    size = sum(os.path.getsize(os.path.join(full, f))
                               for f in os.listdir(full)
                               if os.path.isfile(os.path.join(full, f)))
                    if clean:
                        shutil.rmtree(full)
                        cleaned += 1
                        freed_bytes += size
                    else:
                        found.append({"path": full, "size_bytes": size, "type": "__pycache__"})
                except: pass

    # .pyc 文件
    for fp in glob.glob(os.path.join(WORKSPACE, "**/*.pyc"), recursive=True):
        try:
            size = os.path.getsize(fp)
            if clean:
                os.remove(fp)
                cleaned += 1
                freed_bytes += size
            else:
                found.append({"path": fp, "size_bytes": size, "type": "pyc"})
        except: pass

    # memory/ 目录中超过 90 天的归档
    now = datetime.now(BEIJING_TZ)
    if os.path.isdir(MEMORY_DIR):
        for fp in glob.glob(os.path.join(MEMORY_DIR, "*.md")):
            fname = os.path.basename(fp)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', fname)
            if not date_match:
                continue
            try:
                file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").replace(tzinfo=BEIJING_TZ)
                if (now - file_date).days > 90:
                    size = os.path.getsize(fp)
                    if clean:
                        os.makedirs(ARCHIVE_DIR, exist_ok=True)
                        with open(fp, "rb") as f_in:
                            with gzip.open(os.path.join(ARCHIVE_DIR, fname + ".gz"), "wb") as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        os.remove(fp)
                        cleaned += 1
                        freed_bytes += size
                    else:
                        found.append({"path": fp, "size_bytes": size, "type": "old_memory_log"})
            except: pass

    # /tmp 下本进程遗留文件
    if clean:
        for f in glob.glob("/tmp/analyze_skill*") + glob.glob("/tmp/repack_bundle*"):
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
            except: pass

    return {"found": len(found), "cleaned": cleaned, "freed_bytes": freed_bytes, "items": found[:20]}


# ── 3. 自纠错数据链路维护 ─────────────────────────
def correction_maintenance() -> Dict:
    """确保自纠错数据文件完整"""
    sys.path.insert(0, WORKSPACE)
    try:
        import importlib
        icd = importlib.import_module("scripts.init_correction_data")
        result = icd.run_init(force=False)
        return {"status": "ok", "detail": result.get("data_files", {})}
    except Exception as e:
        return {"status": "error", "error": str(e)[:80]}


# ── 4. 记忆维护 ─────────────────────────────
def memory_maintenance() -> Dict:
    """记忆全量维护（扫描+归档+索引重建）"""
    sys.path.insert(0, WORKSPACE)
    try:
        import importlib
        sm = importlib.import_module("scripts.scan_memory")
        result = sm.scan_directory()
        return {"status": "ok", "detail": result}
    except Exception as e:
        return {"status": "error", "error": str(e)[:80]}


# ── 5. Dream-to-TODO 扫描 ──────────────────────
def dream_to_todo() -> Dict:
    """梦境发现自动提取 TODO"""
    dream_dir = os.path.join(MEMORY_DIR, ".dreams")
    if not os.path.isdir(dream_dir):
        return {"status": "skipped", "reason": "无梦境目录"}
    # 简单扫描：从 dream 文件中提取 TODO 相关内容
    todo_candidates = []
    for fp in glob.glob(os.path.join(dream_dir, "*.md")):
        try:
            with open(fp, encoding="utf-8", errors="replace") as f:
                content = f.read()
            items = re.findall(r'(?:TODO|待办|需要|应该|可以)[：:]\s*(.+?)(?:\n|$)', content)
            for item in items:
                if len(item.strip()) > 5:
                    todo_candidates.append(item.strip())
        except: pass
    return {"status": "ok", "todo_candidates": todo_candidates, "count": len(todo_candidates)}


# ── 6. ReplayBuffer 蒸馏 ──────────────────────
def replay_distill() -> Dict:
    """纠正信号蒸馏"""
    replay_dir = os.path.join(WORKSPACE, ".replay_buffer")
    if not os.path.isdir(replay_dir):
        return {"status": "skipped", "reason": "无 replay_buffer 目录"}
    records_file = os.path.join(replay_dir, "records.jsonl")
    if not os.path.exists(records_file):
        return {"status": "skipped", "reason": "无 records.jsonl"}
    try:
        count = 0
        distilled = []
        with open(records_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        distilled.append(json.loads(line))
                        count += 1
                    except: pass
        # 只保留最近 100 条
        if count > 100:
            with open(records_file, "w", encoding="utf-8") as f:
                for r in distilled[-100:]:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        return {"status": "ok", "records_count": count, "distilled": len(distilled[:10])}
    except Exception as e:
        return {"status": "error", "error": str(e)[:80]}


# ── 7. 执行复盘 ─────────────────────────────
def execution_review() -> Dict:
    """执行复盘分析（JSON 字段级检测，避免字符串 in 误匹配）"""
    results = {"logs_checked": 0, "errors_found": 0}
    ERROR_LEVELS = {"error", "critical", "fatal", "panic"}
    for log_dir in [os.path.join(WORKSPACE, ".logs"), os.path.join(WORKSPACE, ".hooks")]:
        if os.path.isdir(log_dir):
            for fp in glob.glob(os.path.join(log_dir, "*.jsonl")):
                try:
                    with open(fp, encoding="utf-8", errors="replace") as f:
                        for line in f:
                            results["logs_checked"] += 1
                            line = line.strip()
                            if not line:
                                continue
                            # 仅检查结构化 JSON 日志的 level/severity 字段
                            try:
                                entry = json.loads(line)
                                if isinstance(entry, dict):
                                    level = str(entry.get("level", "") or entry.get("severity", "") or "").lower()
                                    if level in ERROR_LEVELS:
                                        results["errors_found"] += 1
                            except json.JSONDecodeError:
                                # 非 JSON 行，跳过
                                pass
                except: pass
    return results


# ── 统一入口 ────────────────────────────────
def run() -> Dict:
    """运行完整维护任务"""
    print("🔄 昨日任务总结与系统清理 开始...")
    start = time.time()

    results = {}

    print("  [1/7] 健康巡检...")
    results["health_check"] = health_check()

    print("  [2/7] 垃圾扫描与清理...")
    results["garbage_cleanup"] = garbage_scan(clean=True)

    print("  [3/7] 自纠错链路维护...")
    results["correction"] = correction_maintenance()

    print("  [4/7] 记忆维护...")
    results["memory"] = memory_maintenance()

    print("  [5/7] Dream-to-TODO...")
    results["dreams"] = dream_to_todo()

    print("  [6/7] Replay 蒸馏...")
    results["replay"] = replay_distill()

    print("  [7/7] 执行复盘...")
    results["review"] = execution_review()

    elapsed = time.time() - start

    # 汇总
    summary = {
        "run_at": datetime.now(BEIJING_TZ).isoformat(),
        "elapsed_seconds": round(elapsed, 1),
        "health_issues": len(results.get("health_check", {}).get("issues", [])),
        "cleaned_items": results.get("garbage_cleanup", {}).get("cleaned", 0),
        "freed_bytes": results.get("garbage_cleanup", {}).get("freed_bytes", 0),
        "memory_ingested": results.get("memory", {}).get("detail", {}).get("scan", {}).get("entries_ingested", 0),
        "dream_candidates": results.get("dreams", {}).get("count", 0),
        "replay_records": results.get("replay", {}).get("records_count", 0),
        "review_errors": results.get("review", {}).get("errors_found", 0),
    }

    state = load_state()
    state["total_cleanups"] = state.get("total_cleanups", 0) + summary["cleaned_items"]
    state["total_issues"] = state.get("total_issues", 0) + summary["health_issues"]
    save_state(state)

    results["summary"] = summary

    print(f"\n✅ 完成。耗时 {elapsed:.1f}s")
    print(f"  健康问题: {summary['health_issues']} 个")
    print(f"  清理文件: {summary['cleaned_items']} 个 ({summary['freed_bytes']/1024:.0f} KB)")
    print(f"  记忆采集: {summary['memory_ingested']} 条")
    print(f"  Dream提取: {summary['dream_candidates']} 条")

    return results


if __name__ == "__main__":
    if "--dry-run" in sys.argv:
        # 只扫描不清理
        print("🔍 垃圾扫描（预览模式，不清理）")
        result = garbage_scan(clean=False)
        print(f"  发现 {result['found']} 个可清理项")
        for item in result["items"][:10]:
            print(f"    {item['path']} ({item['size_bytes']} bytes)")
        sys.exit(0)

    if "--health-only" in sys.argv:
        result = health_check()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    if "--garbage-only" in sys.argv:
        clean = "--clean" in sys.argv
        result = garbage_scan(clean=clean)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    result = run()
    if "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
