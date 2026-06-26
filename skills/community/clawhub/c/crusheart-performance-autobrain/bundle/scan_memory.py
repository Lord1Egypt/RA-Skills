#!/usr/bin/env python3
"""
scan_memory.py — 记忆自动扫描/归档/索引引擎 v1.0

功能：
  1. 扫描 memory/ 目录中的 .md 文件，提取有效记忆内容
  2. 自动 ingest 到 auto_memory（SQLite 主力存储 + 倒排索引）
  3. 自动整理归档：旧日志压缩，合并碎片
  4. 输出扫描报告

用法：
  python3 scripts/scan_memory.py                    # 完整扫描+归档+索引
  python3 scripts/scan_memory.py --scan-only        # 仅扫描ingest
  python3 scripts/scan_memory.py --archive          # 仅归档
  python3 scripts/scan_memory.py --stats            # 仅输出统计
  python3 scripts/scan_memory.py --status           # 输出状态JSON
"""

import json, os, re, sys, glob, time, gzip, shutil, hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from pathlib import Path

BEIJING_TZ = timezone(timedelta(hours=8))
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
ARCHIVE_DIR = os.path.join(WORKSPACE, "memory", ".archive")
STATE_FILE = os.path.join(WORKSPACE, ".scan_memory_state.json")
DEDUP_CACHE = os.path.join(WORKSPACE, ".memory_dedup_cache.json")

# 忽略前缀（系统元数据，不纳入记忆）
IGNORE_PREFIXES = ["[系统消息", "[media", "当前时间", "你是一个", "你是", "# "]


def load_state() -> Dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"last_scan": "", "scanned_files": {}, "total_ingested": 0, "total_archived": 0}


def save_state(state: Dict):
    state["last_scan"] = datetime.now(BEIJING_TZ).isoformat()
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def extract_memories_from_md(filepath: str) -> List[Dict]:
    """从 .md 文件中提取可记忆的条目"""
    memories = []
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        print(f"  ⚠️  读取失败 {os.path.basename(filepath)}: {e}")
        return memories

    lines = content.split("\n")
    current_section = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 跳过忽略前缀
        if any(line.startswith(p) for p in IGNORE_PREFIXES):
            continue
        # 标题行作为 scene
        if line.startswith("#"):
            current_section = line.lstrip("#").strip()
            continue
        # 列表项
        if line.startswith("- ") or line.startswith("* "):
            content_text = line[2:].strip()
            if len(content_text) > 10:  # 过滤太短的
                memories.append({
                    "text": content_text,
                    "scene": current_section or "auto_scan",
                    "tags": ["auto_scan", os.path.basename(filepath).replace(".md", "")]
                })
        # 普通段落（≥15字且有实际信息）
        elif len(line) >= 15 and not line.startswith("```") and not line.startswith(">"):
            # 检测是否是时间戳行
            if re.match(r'^[-*]\s*\[\d{2}:\d{2}\]', line):
                continue
            # 检测是否是元数据行
            if re.match(r'^[-*]\s*\*\*', line):
                continue
            memories.append({
                "text": line[:200],
                "scene": current_section or "auto_scan",
                "tags": ["auto_scan", os.path.basename(filepath).replace(".md", "")]
            })

    return memories


def scan_and_ingest(state: Dict) -> Dict:
    """扫描 memory/ 目录，ingest 到 auto_memory"""
    sys.path.insert(0, WORKSPACE)
    try:
        from core.engines.memory.auto_memory import AutoMemory
        am = AutoMemory()
    except Exception as e:
        return {"status": "error", "error": str(e)[:100]}

    md_files = sorted(glob.glob(os.path.join(MEMORY_DIR, "*.md")))
    stats = {"files_scanned": 0, "entries_ingested": 0, "new_files": 0, "errors": 0}
    
    # 加载去重缓存
    dedup_cache = set()
    if os.path.exists(DEDUP_CACHE):
        try:
            with open(DEDUP_CACHE, encoding="utf-8") as f:
                dedup_cache = set(json.load(f))
        except: pass

    scanned_files = state.get("scanned_files", {})
    
    for fp in md_files:
        fname = os.path.basename(fp)
        # 跳过归档目录内的
        if fname.startswith(".archive"):
            continue
        fsize = os.path.getsize(fp)
        fmtime = os.path.getmtime(fp)
        
        # 增量检查：文件名+大小+mtime 没变就跳过
        cached = scanned_files.get(fname)
        if cached and cached.get("size") == fsize and cached.get("mtime") == fmtime:
            continue

        memories = extract_memories_from_md(fp)
        ingest_count = 0
        for mem in memories:
            # 去重：内容hash去重
            content_hash = hashlib.md5(mem["text"].encode()).hexdigest()
            if content_hash in dedup_cache:
                continue
            try:
                mid = am.save(mem["text"], tags=mem["tags"], scene=mem["scene"])
                dedup_cache.add(content_hash)
                ingest_count += 1
                stats["entries_ingested"] += 1
            except Exception as e:
                print(f"  ⚠️  ingest 失败: {str(e)[:50]}")
                stats["errors"] += 1

        scanned_files[fname] = {"size": fsize, "mtime": fmtime, "ingested": ingest_count}
        stats["files_scanned"] += 1
        if not cached:
            stats["new_files"] += 1
        
        if ingest_count > 0:
            print(f"  📄 {fname}: ingested {ingest_count} 条")

    # 保存去重缓存（限制最多10000条）
    dedup_list = list(dedup_cache)
    if len(dedup_list) > 10000:
        dedup_list = dedup_list[-10000:]
    with open(DEDUP_CACHE, "w", encoding="utf-8") as f:
        json.dump(dedup_list, f, ensure_ascii=False)

    state["scanned_files"] = scanned_files
    state["total_ingested"] = state.get("total_ingested", 0) + stats["entries_ingested"]
    save_state(state)

    stats["status"] = "ok"
    return stats


def run_archive(state: Dict) -> Dict:
    """归档过旧的 memory 日志文件（>90天的压缩为 .gz）"""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    now = datetime.now(BEIJING_TZ)
    stats = {"archived": 0, "skipped": 0, "errors": 0}

    for fp in glob.glob(os.path.join(MEMORY_DIR, "*.md")):
        fname = os.path.basename(fp)
        # 从文件名解析日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', fname)
        if not date_match:
            continue
        file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").replace(tzinfo=BEIJING_TZ)
        age_days = (now - file_date).days

        if age_days > 90:
            # 压缩归档
            gz_path = os.path.join(ARCHIVE_DIR, fname + ".gz")
            if os.path.exists(gz_path):
                stats["skipped"] += 1
                continue
            try:
                with open(fp, "rb") as f_in:
                    with gzip.open(gz_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(fp)
                stats["archived"] += 1
                print(f"  🗜️  {fname} → .archive/ (已归档)")
            except Exception as e:
                print(f"  ⚠️  归档失败 {fname}: {e}")
                stats["errors"] += 1

    state["total_archived"] = state.get("total_archived", 0) + stats["archived"]
    return stats


def run_stats() -> Dict:
    """输出记忆系统统计"""
    sys.path.insert(0, WORKSPACE)
    try:
        from core.engines.memory.auto_memory import AutoMemory
        am = AutoMemory()
        mem_stats = am.stats()
    except Exception as e:
        mem_stats = {"error": str(e)[:100]}

    state = load_state()
    
    md_files = sorted(glob.glob(os.path.join(MEMORY_DIR, "*.md")))
    archived_files = sorted(glob.glob(os.path.join(ARCHIVE_DIR, "*.gz")))

    total_size = sum(os.path.getsize(f) for f in md_files)
    
    return {
        "memory_dir": {
            "active_files": len([f for f in md_files if not os.path.basename(f).startswith(".")]),
            "archived_files": len(archived_files),
            "total_size_kb": round(total_size / 1024, 1),
        },
        "ingest": {
            "total_ingested": state.get("total_ingested", 0),
            "total_archived": state.get("total_archived", 0),
            "last_scan": state.get("last_scan", "never"),
        },
        "auto_memory": mem_stats,
    }


def scan_directory(db=None) -> Dict:
    """外部调用的扫描入口（供 cron 等调用）"""
    state = load_state()
    scan_result = scan_and_ingest(state)
    archive_result = run_archive(state)
    return {
        "scan": scan_result,
        "archive": archive_result,
        "last_scan": datetime.now(BEIJING_TZ).isoformat(),
    }


if __name__ == "__main__":
    
    if "--status" in sys.argv:
        result = run_stats()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    if "--stats" in sys.argv:
        result = run_stats()
        print(f"📊 记忆系统状态")
        print(f"  活跃日志: {result['memory_dir']['active_files']} 个")
        print(f"  归档日志: {result['memory_dir']['archived_files']} 个")
        print(f"  总大小: {result['memory_dir']['total_size_kb']} KB")
        print(f"  累计采集: {result['ingest']['total_ingested']} 条")
        print(f"  最近扫描: {result['ingest']['last_scan']}")
        if isinstance(result.get("auto_memory"), dict):
            am = result["auto_memory"]
            if "error" not in am:
                print(f"  记忆库: {am.get('total', 0)} 条")
        sys.exit(0)

    if "--scan-only" in sys.argv:
        state = load_state()
        result = scan_and_ingest(state)
        print(f"扫描完成: {result}")
        sys.exit(0)

    if "--archive" in sys.argv:
        state = load_state()
        result = run_archive(state)
        print(f"归档完成: {result}")
        sys.exit(0)

    print("🔍 记忆自动扫描归档 开始...")
    state = load_state()
    
    print("  [步骤1/2] 扫描 memory/ 并 ingest...")
    scan_result = scan_and_ingest(state)
    print(f"  → {scan_result['files_scanned']} 个文件, {scan_result['entries_ingested']} 条新记忆")
    
    print("  [步骤2/2] 归档旧日志...")
    archive_result = run_archive(state)
    print(f"  → 归档 {archive_result['archived']} 个, 跳过 {archive_result['skipped']} 个")

    print(f"\n✅ 完成. 累计采集: {state.get('total_ingested', 0)} 条")
