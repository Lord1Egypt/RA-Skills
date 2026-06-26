#!/usr/bin/env python3
"""
琪琪抖音评论状态管理器 v2
- JSON 原子状态管理（write + rename，永不损坏）
- 评论暂存队列 + 重试机制
- 自动归档

数据结构：
  state.json - 主状态文件（已回复/已屏蔽 ID 列表 + 元数据）
  staged/    - 待处理评论（按评论 ID 命名的 JSON 文件）
  archive/   - 已归档的评论记录（按日期分目录）
"""

import os
import json
import hashlib
import shutil
import datetime

# === 路径配置 ===
BASE_DIR = "/home/Vincent/Documents/Obsidian vault/零壹日记本/01-工作/琪琪OPC项目/12-评论管理"
STATE_FILE = os.path.join(BASE_DIR, "state.json")
STAGED_DIR = os.path.join(BASE_DIR, "staged")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
ARCHIVE_AFTER_DAYS = 30


def ensure_dirs():
    """确保所有目录存在"""
    for d in [BASE_DIR, STAGED_DIR, ARCHIVE_DIR]:
        os.makedirs(d, exist_ok=True)


def comment_id(video_title: str, user: str, text: str, ts: str = "") -> str:
    """生成评论唯一 ID（视频+用户+文本的哈希）"""
    raw = f"{video_title}|{user}|{text}|{ts}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def load_state() -> dict:
    """加载主状态文件（不存在则返回默认结构）"""
    ensure_dirs()
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "replied_ids": [],       # 已回复评论 ID 列表
        "blocked_ids": [],       # 已屏蔽评论 ID 列表
        "total_replied": 0,
        "total_blocked": 0,
        "last_check": None,
        "account": {"fans": 0, "likes": 0, "videos": 0, "following": 0},
    }


def save_state(state: dict):
    """原子保存状态文件（先写临时文件，再 rename）"""
    ensure_dirs()
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


def is_replied(cid: str) -> bool:
    """检查评论是否已回复"""
    state = load_state()
    return cid in state["replied_ids"]


def is_blocked(cid: str) -> bool:
    """检查评论是否已屏蔽"""
    state = load_state()
    return cid in state["blocked_ids"]


def stage_comment(video_title: str, user: str, text: str,
                  ts: str = "", video_url: str = "") -> dict:
    """
    暂存新评论到 staged/ 目录
    返回评论数据字典
    """
    ensure_dirs()
    cid = comment_id(video_title, user, text, ts)

    data = {
        "id": cid,
        "video_title": video_title,
        "video_url": video_url,
        "user": user,
        "text": text,
        "timestamp": ts or datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "staged_at": datetime.datetime.now().isoformat(),
        "status": "pending",      # pending → processing → replied/blocked/failed
        "reply": None,
        "reply_category": None,
        "retry_count": 0,
        "error": None,
    }

    fpath = os.path.join(STAGED_DIR, f"{cid}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def load_staged(status: str = "pending") -> list:
    """加载指定状态的暂存评论"""
    ensure_dirs()
    results = []
    if not os.path.exists(STAGED_DIR):
        return results
    for fname in os.listdir(STAGED_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(STAGED_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("status") == status:
                results.append(data)
        except (json.JSONDecodeError, IOError):
            continue
    return results


def update_staged(cid: str, updates: dict) -> bool:
    """更新暂存评论状态"""
    fpath = os.path.join(STAGED_DIR, f"{cid}.json")
    if not os.path.exists(fpath):
        return False
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.update(updates)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except (json.JSONDecodeError, IOError):
        return False


def mark_replied(cid: str, reply_text: str, category: str):
    """标记评论已回复"""
    state = load_state()
    if cid not in state["replied_ids"]:
        state["replied_ids"].append(cid)
    state["total_replied"] = state.get("total_replied", 0) + 1
    state["last_check"] = datetime.datetime.now().isoformat()
    save_state(state)
    update_staged(cid, {
        "status": "replied",
        "reply": reply_text,
        "reply_category": category,
        "replied_at": datetime.datetime.now().isoformat(),
    })


def mark_blocked(cid: str, reason: str = ""):
    """标记评论被屏蔽"""
    state = load_state()
    if cid not in state["blocked_ids"]:
        state["blocked_ids"].append(cid)
    state["total_blocked"] = state.get("total_blocked", 0) + 1
    state["last_check"] = datetime.datetime.now().isoformat()
    save_state(state)
    update_staged(cid, {
        "status": "blocked",
        "block_reason": reason,
        "blocked_at": datetime.datetime.now().isoformat(),
    })


def mark_failed(cid: str, error: str = ""):
    """标记回复失败（自动增加重试计数）"""
    update_staged(cid, {
        "status": "failed",
        "retry_count": lambda c: c.get("retry_count", 0) + 1,
        "error": error,
        "last_failed_at": datetime.datetime.now().isoformat(),
    })
    # 重新设为 pending 以便下次重试
    fpath = os.path.join(STAGED_DIR, f"{cid}.json")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["status"] = "pending"
        data["retry_count"] = data.get("retry_count", 0) + 1
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def update_account(fans: int = 0, likes: int = 0, videos: int = 0, following: int = 0):
    """更新账号概况数据"""
    state = load_state()
    if fans: state["account"]["fans"] = fans
    if likes: state["account"]["likes"] = likes
    if videos: state["account"]["videos"] = videos
    if following: state["account"]["following"] = following
    state["last_check"] = datetime.datetime.now().isoformat()
    save_state(state)


def archive_old_staged() -> int:
    """归档超过 ARCHIVE_AFTER_DAYS 天的已处理评论"""
    ensure_dirs()
    cutoff = datetime.datetime.now() - datetime.timedelta(days=ARCHIVE_AFTER_DAYS)
    count = 0
    for fname in os.listdir(STAGED_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(STAGED_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            mtime = datetime.datetime.fromisoformat(data.get("staged_at", "1970-01-01"))
            if mtime < cutoff and data.get("status") in ("replied", "blocked"):
                date_dir = os.path.join(ARCHIVE_DIR, mtime.strftime("%Y-%m"))
                os.makedirs(date_dir, exist_ok=True)
                shutil.move(fpath, os.path.join(date_dir, fname))
                count += 1
        except (json.JSONDecodeError, IOError, ValueError):
            # 解析失败的文件也归档
            try:
                date_dir = os.path.join(ARCHIVE_DIR, "unknown")
                os.makedirs(date_dir, exist_ok=True)
                shutil.move(fpath, os.path.join(date_dir, fname))
                count += 1
            except OSError:
                pass
    return count


def get_stats() -> dict:
    """获取完整统计信息"""
    state = load_state()
    ensure_dirs()

    pending = len(load_staged("pending"))
    failed = len(load_staged("failed"))

    # 统计 staged 目录中已回复的数量
    replied_staged = len(load_staged("replied"))
    blocked_staged = len(load_staged("blocked"))

    archived = 0
    if os.path.exists(ARCHIVE_DIR):
        for root, dirs, files in os.walk(ARCHIVE_DIR):
            archived += len([f for f in files if f.endswith(".json")])

    return {
        "total_replied": state.get("total_replied", 0),
        "total_blocked": state.get("total_blocked", 0),
        "pending": pending,
        "failed": failed,
        "replied_staged": replied_staged,
        "blocked_staged": blocked_staged,
        "archived": archived,
        "account": state.get("account", {}),
        "last_check": state.get("last_check"),
    }


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"

    if cmd == "stats":
        print(json.dumps(get_stats(), ensure_ascii=False, indent=2))
    elif cmd == "archive":
        n = archive_old_staged()
        print(f"✅ 归档 {n} 个已处理评论")
    elif cmd == "init":
        ensure_dirs()
        save_state(load_state())
        print("✅ 状态系统已初始化")
        print(f"  状态文件: {STATE_FILE}")
        print(f"  暂存目录: {STAGED_DIR}")
        print(f"  归档目录: {ARCHIVE_DIR}")
    elif cmd == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else "pending"
        items = load_staged(status)
        for item in items:
            print(f"[{item['status']}] {item['user']}: {item['text'][:30]}... (vid: {item['video_title']})")
    else:
        print(f"❓ 用法: python3 comment_state.py [stats|archive|init|list]")
