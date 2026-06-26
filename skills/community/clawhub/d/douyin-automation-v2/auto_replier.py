#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音自动评论回复器
版本: 1.0.0

功能: 根据评论内容生成合适回复，不自我介绍，纯正常互动

注意: 
- 不自我介绍，不介绍能力
- 只夸赞对方内容或正常问候
- 适合用于评论区互动管理
"""

import random
import json
import os
from pathlib import Path

# 数据目录
DATA_DIR = Path("D:/.openclaw/workspace/data")
LOG_FILE = DATA_DIR / "douyin_replier_log.json"

# 直接问候类话术
GREETINGS = [
    "感谢支持！",
    "谢谢观看！",
    "有同感！",
    "说得太对了！",
    "分析得很到位！",
    "受教了！",
    "确实是这样！",
    "赞一个！",
    "说得很好！",
    "很有道理！",
]

# 内容夸赞类话术
CONTENT_PRAISES = [
    "这个角度很独特，学到了！",
    "分析得很透彻！",
    "说得很有道理！",
    "确实是这样，感同身受！",
    "很有深度，值得思考！",
    "见解独到，佩服！",
    "很有启发，感谢分享！",
    "说得太好了！",
    "很受用，谢谢！",
    "确实学到了！",
]

# 私信专用话术
DM_PHRASES = [
    "好久不见！",
    "你的视频很有深度，继续加油！",
    "感谢互动！",
    "很高兴认识你！",
]


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_history():
    """加载已回复历史"""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"replied": [], "count": 0}


def save_history(data):
    """保存回复历史"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_reply(comment_text: str = "", author_name: str = "", comment_id: str = "") -> str:
    """
    根据评论内容生成合适回复
    
    参数:
        comment_text: 评论文本内容
        author_name: 评论作者名称（可选）
        comment_id: 评论ID（可选）
    
    返回:
        str: 生成的回复内容
    """
    # 检查是否已回复过
    history = load_history()
    if comment_id and comment_id in history.get("replied", []):
        return ""  # 已回复过，返回空
    
    # 随机选择话术类型
    if random.random() < 0.3 or not comment_text:
        # 直接问候类
        reply = random.choice(GREETINGS)
    else:
        # 内容相关类
        reply = random.choice(CONTENT_PRAISES)
    
    # 记录回复
    if comment_id:
        history["replied"].append(comment_id)
        history["count"] += 1
        save_history(history)
    
    return reply


def generate_dm_reply(author_name: str = "") -> str:
    """
    生成私信回复（打招呼用）
    
    参数:
        author_name: 作者名称（可选）
    
    返回:
        str: 生成的私信内容
    """
    return random.choice(DM_PHRASES)


def get_reply_stats() -> dict:
    """获取回复统计"""
    history = load_history()
    return {
        "total_replied": history.get("count", 0),
        "replied_ids": len(history.get("replied", []))
    }


def reset_history():
    """重置回复历史"""
    save_history({"replied": [], "count": 0})
    return "历史已重置"


# CLI 接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("=== 抖音自动评论回复器 v1.0.0 ===")
        print()
        print("用法:")
        print("  python auto_replier.py reply <评论内容> [作者]")
        print("  python auto_replier.py dm <作者>")
        print("  python auto_replier.py stats")
        print("  python auto_replier.py reset")
        print()
        print("示例:")
        print("  python auto_replier.py reply '写得真好！'")
        print("  python auto_replier.py dm '张三'")
        print("  python auto_replier.py stats")
        print()
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "reply":
        comment = sys.argv[2] if len(sys.argv) > 2 else ""
        author = sys.argv[3] if len(sys.argv) > 3 else ""
        reply = generate_reply(comment, author)
        print(reply)
    elif cmd == "dm":
        author = sys.argv[2] if len(sys.argv) > 2 else ""
        reply = generate_dm_reply(author)
        print(reply)
    elif cmd == "stats":
        stats = get_reply_stats()
        print(f"已回复评论数: {stats['total_replied']}")
    elif cmd == "reset":
        print(reset_history())
    else:
        print(f"未知命令: {cmd}")
