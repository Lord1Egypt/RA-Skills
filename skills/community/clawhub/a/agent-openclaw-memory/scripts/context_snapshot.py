#!/usr/bin/env python3
"""
context_snapshot.py — 压缩前保存上下文快照

从 SQLite 读取最近会话摘要，结合 vault 变更，保存到 vault。
避免 compaction 后丢失关键信息。

用法: python scripts/context_snapshot.py [--clean]
集成: heartbeat 中压缩步骤前执行
"""
import _suppress_windows

import json, os, sqlite3, sys
from pathlib import Path
from datetime import datetime, timedelta

from shared_config import VAULT_DIR as VAULT
SNAPSHOT_DIR = VAULT / "05-存档" / "上下文快照"
STATE_FILE = Path.home() / ".openclaw" / ".context_snapshot_state.json"
MEMORY_DB = Path.home() / ".openclaw" / "memory" / "main.sqlite"

MAX_SNAPSHOTS = 20  # 保留最近 20 个快照
MAX_VAULT_CHANGES = 10
MAX_SESSION_CHUNKS = 8  # 最近会话摘要条数


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"last_snapshot": None, "session_count": 0}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def get_recent_sessions():
    """从 SQLite 读取最近的会话摘要 chunks。"""
    if not MEMORY_DB.exists():
        return []
    try:
        db = sqlite3.connect(str(MEMORY_DB))
        c = db.cursor()
        cutoff_ts = int((datetime.now() - timedelta(hours=48)).timestamp()) * 1000
        c.execute(
            "SELECT path, text, updated_at FROM chunks "
            "WHERE path LIKE 'memory/2026-%' AND updated_at > ? "
            "ORDER BY updated_at DESC LIMIT ?",
            (cutoff_ts, MAX_SESSION_CHUNKS * 3),  # 取多一些，后面去重
        )
        rows = c.fetchall()
        db.close()

        # 按 path 去重（同一会话文件只保留最新 chunk）
        seen = {}
        for path, text, ts in rows:
            if path not in seen:
                seen[path] = (text, ts)
            if len(seen) >= MAX_SESSION_CHUNKS:
                break

        return [(path, text, ts) for path, (text, ts) in seen.items()]
    except Exception as e:
        print(f"  [WARN] SQLite 读取失败: {e}")
        return []


def get_vault_changes():
    """最近 vault 变更，排除快照文件自身。"""
    if not VAULT.exists():
        return []
    changes = []
    cutoff = datetime.now() - timedelta(hours=24)
    for f in VAULT.rglob("*.md"):
        # 跳过快照目录
        if "上下文快照" in str(f):
            continue
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime > cutoff:
                changes.append((f, mtime))
        except Exception:
            continue
    changes.sort(key=lambda x: x[1], reverse=True)
    return changes[:MAX_VAULT_CHANGES]


def get_recent_lessons():
    """最近修改的教训/偏好文件。"""
    lessons_path = VAULT / "04-教训"
    if not lessons_path.exists():
        return []
    files = sorted(lessons_path.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    return files[:5]


def cleanup_old_snapshots():
    """删除旧快照，保留最近 MAX_SNAPSHOTS 个。"""
    if not SNAPSHOT_DIR.exists():
        return 0
    snapshots = sorted(SNAPSHOT_DIR.glob("snapshot_*.md"), key=lambda f: f.stat().st_mtime)
    to_delete = snapshots[:-MAX_SNAPSHOTS]
    for f in to_delete:
        try:
            f.unlink()
        except Exception:
            pass
    return len(to_delete)


def take_snapshot():
    """保存当前关键状态到 vault 快照。"""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    snapshot_file = SNAPSHOT_DIR / f"snapshot_{timestamp}.md"

    state = load_state()
    version = state.get("session_count", 0) + 1

    # ── 采集数据 ──
    sessions = get_recent_sessions()
    vault_changes = get_vault_changes()
    lessons = get_recent_lessons()

    # ── 写快照 ──
    with open(snapshot_file, "w", encoding="utf-8") as f:
        f.write(f"# 上下文快照 #{version}\n\n")
        f.write(f"**时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**触发:** Heartbeat\n\n")
        f.write("---\n\n")

        # 1. 最近会话摘要（从 SQLite）
        f.write("## 最近会话\n\n")
        if sessions:
            for path, text, ts in sessions:
                # 提取时间戳
                ts_str = datetime.fromtimestamp(ts / 1000).strftime("%m-%d %H:%M")
                # 截取前 300 字符作为摘要
                summary = text.strip()[:300]
                if len(text) > 300:
                    summary += "..."
                f.write(f"### {path} ({ts_str})\n\n{summary}\n\n---\n\n")
        else:
            f.write("无最近会话数据。\n\n")

        # 2. 最近 vault 变更（排除快照）
        f.write("## 最近 vault 变更\n\n")
        if vault_changes:
            for fpath, mtime in vault_changes:
                rel = fpath.relative_to(VAULT)
                mtime_str = mtime.strftime("%m-%d %H:%M")
                size = fpath.stat().st_size
                f.write(f"- {rel} ({mtime_str}, {size}B)\n")
            f.write("\n")
        else:
            f.write("无最近变更。\n\n")

        # 3. 最近教训/偏好
        f.write("## 用户偏好/决策\n\n")
        if lessons:
            for l in lessons:
                rel = l.relative_to(VAULT)
                content = l.read_text(encoding="utf-8", errors="replace")[:300]
                f.write(f"### {rel}\n\n{content}\n\n---\n\n")
        else:
            f.write("无最近偏好变更。\n\n")

        f.write(f"\n---\n*自动快照 #{version}*  \n")
        f.write(f"*生成于 {datetime.now().isoformat()}*\n")

    # ── 更新状态 ──
    state["last_snapshot"] = datetime.now().isoformat()
    state["session_count"] = version
    save_state(state)

    # ── 清理旧快照 ──
    cleaned = cleanup_old_snapshots()
    if cleaned:
        print(f"  清理了 {cleaned} 个旧快照")

    print(f"快照已保存: {snapshot_file}")
    return snapshot_file


# ── Health report ──
try:
    from system_health import task_report
    task_report("context_snapshot", status="ok")
except Exception:
    pass


if __name__ == "__main__":
    if "--clean" in sys.argv:
        cleaned = cleanup_old_snapshots()
        print(f"清理了 {cleaned} 个旧快照")
    else:
        take_snapshot()
