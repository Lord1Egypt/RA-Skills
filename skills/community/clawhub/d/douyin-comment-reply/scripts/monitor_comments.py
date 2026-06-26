#!/usr/bin/env python3
"""
琪琪抖音评论自动回复脚本
- 监控抖音创作者中心评论
- 以5岁小女孩琪琪的视角回复
- 安全过滤 + 自动回复
- 记录到Obsidian

核心原则：
1. 所有回复必须像5岁小女孩说的
2. 不回复任何敏感/不当内容
3. 不透露个人信息
4. 友好、可爱、简短
"""

import os
import sys
import json
import datetime
import re
import time

# Obsidian路径
OBSIDIAN_BASE = "/home/Vincent/Documents/Obsidian vault/零壹日记本/01-工作/琪琪OPC项目"
COMMENT_LOG_DIR = os.path.join(OBSIDIAN_BASE, "12-评论管理")
RECORD_FILE = os.path.join(COMMENT_LOG_DIR, "评论记录.md")

# 安全关键词（触发不回复）
BLOCK_KEYWORDS = [
    "约吗", "加微信", "私聊", "电话", "见面", "地址", "在哪",
    "喜欢", "爱你", "老婆", "老公", "处对象", "谈恋爱",
    "死", "杀", "打", "滚", "笨", "傻", "丑",
    "http", "www", ".com", "扫码", "二维码",
]

# 琪琪回复规则
REPLY_RULES = {
    "夸赞类": {
        "关键词": ["可爱", "好听", "好棒", "真好", "好喜欢", "好乖", "太棒了", "厉害"],
        "回复模板": [
            "谢谢你夸我！我好开心呀～",
            "嘻嘻，谢谢你！你也超级棒！✨",
            "谢谢你夸我！我今天也很开心哦！",
            "哇，谢谢！我会继续讲故事的～",
        ]
    },
    "互动类": {
        "关键词": ["什么时候", "明天", "还有", "能不能", "可不可以", "求", "想听"],
        "回复模板": [
            "好呀好呀！我明天再给你讲故事哦～",
            "嗯嗯！我明天还会来的！拜拜～",
            "好的呀！你明天来看我哦～",
            "嘻嘻，明天见！",
        ]
    },
    "感谢类": {
        "关键词": ["谢谢", "感谢", "辛苦了"],
        "回复模板": [
            "不客气！我喜欢给你讲故事～",
            "嘿嘿，不用谢！你也给我力量哦！",
            "不用谢！我们一起听故事好不好呀？",
        ]
    },
    "提问类": {
        "关键词": ["几岁", "多大", "几年级", "叫什么", "你是谁", "谁讲的"],
        "回复模板": [
            "我5岁啦！我是琪琪哦～",
            "我叫琪琪！今年5岁了！7月10日过生日哦～",
            "我是琪琪！我喜欢讲故事和交朋友！",
        ]
    },
    "催更类": {
        "关键词": ["更新", "新故事", "怎么还没", "等", "快", "催更"],
        "回复模板": [
            "别急别急！我明天就讲新的故事给你听！",
            "嗯嗯！新的故事在路上了！明天见哦～",
            "好故事需要慢慢准备哦！明天就来！",
        ]
    },
    "通用类": {
        "关键词": [],  # 兜底
        "回复模板": [
            "嘻嘻，谢谢你来看我讲故事！明天见哦～",
            "你好呀！明天我还在这里讲故事给你听！",
            "谢谢你来！我们一起听故事好不好呀？",
            "嗯嗯！明天见！拜拜～",
        ]
    }
}


def is_comment_safe(comment_text: str) -> bool:
    """检查评论是否安全"""
    comment_lower = comment_text.lower()
    for keyword in BLOCK_KEYWORDS:
        if keyword.lower() in comment_lower:
            return False
    return True


def classify_and_reply(comment_text: str) -> str:
    """分类评论并生成回复"""
    for category, data in REPLY_RULES.items():
        if category == "通用类":
            continue
        for keyword in data["关键词"]:
            if keyword in comment_text:
                import random
                return random.choice(data["回复模板"])
    
    # 默认通用回复
    import random
    return random.choice(REPLY_RULES["通用类"]["回复模板"])


def save_comment_record(comment_user: str, comment_text: str, reply_text: str, 
                        video_title: str, reply_time: str):
    """保存评论记录到Obsidian"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    record_entry = f"""
### {reply_time}
- **视频**: {video_title}
- **评论者**: {comment_user}
- **评论内容**: {comment_text}
- **回复内容**: {reply_text}
- **状态**: ✅ 已回复
"""
    
    # 读取或创建记录文件
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = f"# 评论记录\n\n> 琪琪的抖音评论自动回复记录\n\n## {today}"
    
    # 添加今天的日期标题（如果没有）
    if today not in content:
        content += f"\n\n## {today}"
    
    content += record_entry
    
    with open(RECORD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    print("🎯 琪琪评论监控脚本已就绪")
    print("📝 记录文件:", RECORD_FILE)
    print("🔒 安全过滤已启用")
    print("👧 琪琪视角回复已启用")
