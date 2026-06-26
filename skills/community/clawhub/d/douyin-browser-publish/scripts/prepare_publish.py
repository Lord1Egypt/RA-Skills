#!/usr/bin/env python3
"""
抖音发布准备脚本 - Phase 6
从视频项目目录提取元数据，写入发布队列

用法:
    python3 prepare_publish.py <project_dir>
    
输出:
    ~/.openclaw/workspace/publish-queue/pending_<date>.json
"""

import os
import sys
import json
import re
import glob
from datetime import datetime


WORKSPACE = "/home/Vincent/.openclaw/workspace"
QUEUE_DIR = os.path.join(WORKSPACE, "publish-queue")
STORY_TEXT = None

# 主题标签映射
THEME_TAGS = {
    "动物": ["#小动物", "#动物科普", "#可爱动物"],
    "蜜蜂": ["#小蜜蜂", "#勤劳", "#采蜜"],
    "兔子": ["#小兔子", "#可爱", "#花园"],
    "彩虹": ["#彩虹", "#颜色", "#美丽"],
    "友谊": ["#友谊", "#分享", "#好朋友"],
    "勇敢": ["#勇敢", "#不放弃", "#成长"],
    "自然": ["#大自然", "#植物", "#观察"],
    "家庭": ["#家人", "#妈妈", "#温暖"],
}

FIXED_TAGS = ["#儿童故事", "#睡前故事", "#亲子时光"]


def extract_keywords(text: str) -> str:
    """提取故事中的关键词"""
    keywords = []
    animals = {"兔子": "小兔子", "蜜蜂": "小蜜蜂", "松鼠": "小松鼠",
               "鸟": "小鸟", "蝴蝶": "蝴蝶", "青蛙": "小青蛙", "蚂蚁": "小蚂蚁"}
    for keyword, display in animals.items():
        if keyword in text:
            keywords.append(display)
    scenes = ["花园", "森林", "山坡", "院子", "花丛", "草地", "天空", "彩虹"]
    for scene in scenes:
        if scene in text:
            keywords.append(scene)
    emotions = ["快乐", "勇敢", "温暖", "友好", "分享", "爱心"]
    for emotion in emotions:
        if emotion in text:
            keywords.append(emotion)
    return '、'.join(keywords[:5]) if keywords else "可爱的小动物"


def extract_theme(keywords: str) -> str:
    """从关键词提取主题"""
    if not keywords:
        return "通用"
    first_kw = keywords.split('、')[0]
    for theme in THEME_TAGS.keys():
        if theme in first_kw:
            return theme
    return "通用"


def get_topic_tags(keywords: str) -> list:
    """根据关键词获取话题标签"""
    tags = []
    for kw in keywords.split('、'):
        for theme, theme_tags in THEME_TAGS.items():
            if theme in kw or kw in theme:
                tags.extend(theme_tags[:2])
                break
    # 去重
    tags = list(dict.fromkeys(tags))
    return tags[:3]  # 最多3个主题标签


def prepare_publish(project_dir: str) -> dict:
    """从项目目录准备发布数据"""
    # 查找竖版视频
    vertical_video = None
    for pattern in ["story_video_vertical.mp4", "*vertical*.mp4", "*竖版*.mp4"]:
        matches = glob.glob(os.path.join(project_dir, pattern))
        if matches:
            vertical_video = matches[0]
            break
    
    if not vertical_video:
        # 如果找不到竖版，用第一个 mp4
        mp4s = glob.glob(os.path.join(project_dir, "*.mp4"))
        if mp4s:
            vertical_video = mp4s[0]
        else:
            raise FileNotFoundError(f"项目目录中无视频文件: {project_dir}")
    
    # 查找元数据文件
    meta_file = os.path.join(project_dir, "publish_metadata.json")
    story_file = os.path.join(project_dir, "story.json")
    
    story_name = os.path.basename(project_dir)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 从目录名提取信息
    # story-20260514-小蜜蜂采花蜜
    m = re.match(r'story-(\d{4})(\d{2})(\d{2})-(.+)', story_name)
    if m:
        date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        story_name = m.group(4)
    
    # 尝试从已有元数据文件读取
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            title = meta.get("title", f"适合3-8岁的睡前故事 | {story_name} | 琪琪的魔法故事屋")
            description = meta.get("description", "儿童成长故事，适合3-8岁小朋友")
            keywords = meta.get("keywords", "")
    elif os.path.exists(story_file):
        with open(story_file, 'r', encoding='utf-8') as f:
            story = json.load(f)
            story_name = story.get("name", story_name)
            title = f"适合3-8岁的睡前故事 | {story_name} | 琪琪的魔法故事屋"
            description = story.get("text", "")[:100] or "儿童成长故事，适合3-8岁小朋友"
            keywords = extract_keywords(description)
    else:
        title = f"适合3-8岁的睡前故事 | {story_name} | 琪琪的魔法故事屋"
        description = "儿童成长故事，适合3-8岁小朋友"
        keywords = extract_keywords(description)
    
    # 生成话题标签
    topic_tags = get_topic_tags(keywords)
    all_tags = topic_tags + FIXED_TAGS
    # 去重
    all_tags = list(dict.fromkeys(all_tags))
    
    # 生成完整描述
    full_description = f"{description} {' '.join(all_tags)}"
    
    # 限制描述长度（抖音最多1000字）
    if len(full_description) > 800:
        full_description = full_description[:797] + "..."
    
    result = {
        "project_dir": project_dir,
        "video_path": os.path.abspath(vertical_video),
        "title": title[:30],  # 抖音标题最多30字
        "description": full_description,
        "tags": all_tags,
        "date": date_str,
        "story_name": story_name,
        "created_at": datetime.now().isoformat()
    }
    
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python3 prepare_publish.py <project_dir>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    if not os.path.isdir(project_dir):
        print(f"错误: 目录不存在 - {project_dir}")
        sys.exit(1)
    
    # 创建队列目录
    os.makedirs(QUEUE_DIR, exist_ok=True)
    
    # 准备发布数据
    try:
        data = prepare_publish(project_dir)
    except Exception as e:
        print(f"❌ 发布准备失败: {e}")
        sys.exit(1)
    
    # 写入队列文件
    safe_name = re.sub(r'[^\w\u4e00-\u9fff]', '', data['story_name'][:15])
    queue_file = os.path.join(QUEUE_DIR, f"pending_{data['date']}_{safe_name}.json")
    
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 发布队列已创建: {queue_file}")
    print(f"📹 视频: {data['video_path']}")
    print(f"📝 标题: {data['title']}")
    print(f"💬 描述: {data['description'][:50]}...")
    print(f"🏷️ 话题: {' '.join(data['tags'])}")
    
    # 输出 JSON 供 cron 读取
    print(f"\nQUEUE_FILE={queue_file}")


if __name__ == '__main__':
    main()
