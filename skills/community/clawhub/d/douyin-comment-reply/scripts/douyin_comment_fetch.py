#!/usr/bin/env python3
"""
抖音评论抓取脚本（Phase A）
- 从抖音创作者中心拉取最新评论
- 去重后暂存到 staged/ 目录
- 输出 JSON 供 Phase B 处理

用法：
  # 输出暂存的评论列表（JSON）
  python3 douyin_comment_fetch.py --mode fetch
  
  # 手动添加评论（浏览器不可用时降级）
  python3 douyin_comment_fetch.py --mode manual --video "视频名" --user "用户名" --text "评论内容"
"""

import os
import sys
import json
import datetime
import argparse

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comment_state import (
    ensure_dirs, stage_comment, is_replied, is_blocked,
    update_account, get_stats
)

OBSIDIAN_BASE = "/home/Vincent/Documents/Obsidian vault/零壹日记本/01-工作/琪琪OPC项目"
RECORD_FILE = os.path.join(OBSIDIAN_BASE, "12-评论管理/评论记录.md")


def parse_markdown_records() -> list:
    """
    从旧版 Markdown 评论记录中解析已回复的评论
    （用于迁移到新的 JSON 状态系统）
    """
    if not os.path.exists(RECORD_FILE):
        return []
    
    replied = []
    with open(RECORD_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 解析表格行：| 时间 | 视频名 | 评论者 | 评论内容 | 回复内容 | 状态 |
    import re
    pattern = r"\|\s*([\d\-]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*✅\s*已回复\s*\|"
    for match in re.finditer(pattern, content):
        ts, video, user, text, reply = [m.strip() for m in match.groups()]
        if text and text != "-" and user and user != "-":
            replied.append({
                "video_title": video,
                "user": user,
                "text": text,
                "reply": reply,
                "timestamp": ts,
            })
    
    return replied


def migrate_from_markdown():
    """从旧版 Markdown 迁移已回复评论到 JSON 状态系统"""
    from comment_state import load_state, save_state, comment_id, mark_replied
    
    records = parse_markdown_records()
    if not records:
        print("  没有需要迁移的记录")
        return 0
    
    state = load_state()
    migrated = 0
    
    for rec in records:
        cid = comment_id(rec["video_title"], rec["user"], rec["text"], rec["timestamp"])
        if cid not in state["replied_ids"]:
            # 写入 staged 文件（标记为已回复）
            data = {
                "id": cid,
                "video_title": rec["video_title"],
                "video_url": "",
                "user": rec["user"],
                "text": rec["text"],
                "timestamp": rec["timestamp"],
                "staged_at": datetime.datetime.now().isoformat(),
                "status": "replied",
                "reply": rec["reply"],
                "reply_category": "migrated",
                "retry_count": 0,
                "error": None,
            }
            ensure_dirs()
            fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "staged", f"{cid}.json")
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            state["replied_ids"].append(cid)
            state["total_replied"] += 1
            migrated += 1
    
    state["last_check"] = datetime.datetime.now().isoformat()
    save_state(state)
    return migrated


def fetch_from_browser_instructions() -> dict:
    """
    生成浏览器操作的指令清单（供 OpenClaw agent 执行）
    返回结构化 JSON，描述需要浏览器做什么
    """
    return {
        "instructions": [
            {
                "step": 1,
                "action": "navigate",
                "url": "https://creator.douyin.com/",
                "timeout_seconds": 30,
            },
            {
                "step": 2,
                "action": "snapshot",
                "purpose": "检查登录状态和账号概况（粉丝数、获赞数、作品数）",
            },
            {
                "step": 3,
                "action": "navigate",
                "url": "https://creator.douyin.com/creator-micro/content/manage",
                "timeout_seconds": 20,
            },
            {
                "step": 4,
                "action": "snapshot",
                "purpose": "获取已发布作品列表及每个作品的评论数",
            },
            {
                "step": 5,
                "action": "for_each_recent_video",
                "count": 5,
                "sub_steps": [
                    {"action": "click_video", "purpose": "进入视频详情页"},
                    {"action": "snapshot_comments", "purpose": "获取最新评论列表"},
                    {"action": "extract_comment_data", "fields": ["user", "text", "timestamp", "video_title"]},
                    {"action": "navigate_back", "purpose": "返回作品管理页"},
                ],
            },
            {
                "step": 6,
                "action": "output_json",
                "purpose": "输出抓取结果到标准输出",
                "format": {
                    "account": {"fans": "int", "likes": "int", "videos": "int", "following": "int"},
                    "videos": [
                        {"title": "str", "comments": [{"user": "str", "text": "str", "timestamp": "str"}]}
                    ],
                },
            },
        ],
        "output_file": "/tmp/douyin_comments_raw.json",
    }


def stage_new_comments(raw_data: dict) -> dict:
    """
    处理浏览器抓取的原始数据，去重后暂存新评论
    raw_data: 浏览器抓取结果
    返回: 统计信息
    """
    from comment_state import comment_id, stage_comment, update_account
    
    ensure_dirs()
    stats = {"new": 0, "duplicate": 0, "blocked": 0, "videos_checked": 0}
    
    # 更新账号概况
    account = raw_data.get("account", {})
    if account:
        update_account(
            fans=account.get("fans", 0),
            likes=account.get("likes", 0),
            videos=account.get("videos", 0),
            following=account.get("following", 0),
        )
    
    # 处理每个视频的评论
    for video in raw_data.get("videos", []):
        video_title = video.get("title", "未知视频")
        stats["videos_checked"] += 1
        
        for comment in video.get("comments", []):
            user = comment.get("user", "").strip()
            text = comment.get("text", "").strip()
            ts = comment.get("timestamp", "")
            
            if not user or not text:
                continue
            
            cid = comment_id(video_title, user, text, ts)
            
            # 去重检查
            if is_replied(cid):
                stats["duplicate"] += 1
                continue
            
            if is_blocked(cid):
                stats["blocked"] += 1
                continue
            
            # 暂存新评论
            stage_comment(video_title, user, text, ts)
            stats["new"] += 1
    
    return stats


def manual_add_comment(video: str, user: str, text: str, ts: str = ""):
    """手动添加评论（浏览器不可用时的降级方案）"""
    from comment_state import comment_id, stage_comment
    
    cid = comment_id(video, user, text, ts)
    if is_replied(cid) or is_blocked(cid):
        print(f"⏭️  评论已处理（已回复或已屏蔽）")
        return
    
    data = stage_comment(video, user, text, ts or datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    print(f"✅ 评论已暂存: {user}: {text[:30]}...")
    print(f"   ID: {data['id']}")
    print(f"   状态: pending")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抖音评论抓取脚本")
    parser.add_argument("--mode", choices=["fetch", "manual", "migrate", "stats", "instructions"], default="stats")
    parser.add_argument("--video", help="视频名（manual 模式）")
    parser.add_argument("--user", help="评论者（manual 模式）")
    parser.add_argument("--text", help="评论内容（manual 模式）")
    parser.add_argument("--raw", help="浏览器抓取的原始 JSON 文件路径（fetch 模式）")
    args = parser.parse_args()
    
    if args.mode == "instructions":
        # 输出浏览器操作指令
        instructions = fetch_from_browser_instructions()
        print(json.dumps(instructions, ensure_ascii=False, indent=2))
    
    elif args.mode == "fetch":
        # 处理浏览器抓取的原始数据
        if args.raw and os.path.exists(args.raw):
            with open(args.raw, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        else:
            # 尝试读取默认路径
            default_path = "/tmp/douyin_comments_raw.json"
            if os.path.exists(default_path):
                with open(default_path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
            else:
                print("❌ 未找到原始数据文件。请提供 --raw 参数或确保 /tmp/douyin_comments_raw.json 存在")
                sys.exit(1)
        
        stats = stage_new_comments(raw_data)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.mode == "manual":
        if not all([args.video, args.user, args.text]):
            print("❌ manual 模式需要 --video, --user, --text 参数")
            sys.exit(1)
        manual_add_comment(args.video, args.user, args.text)
    
    elif args.mode == "migrate":
        n = migrate_from_markdown()
        print(f"✅ 迁移完成: {n} 条记录已迁移到 JSON 状态系统")
    
    elif args.mode == "stats":
        stats = get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
