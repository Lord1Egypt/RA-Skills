#!/usr/bin/env python3
"""
抖音发布元数据提取器

从琪琪故事视频项目目录提取发布元数据，供浏览器自动化使用。

用法:
    python3 extract_publish_meta.py <project_dir>
    
输出:
    生成 publish_meta.json，包含标题、描述、话题标签
"""

import json
import os
import sys
import glob


def extract_meta(project_dir: str) -> dict:
    """从项目目录提取发布元数据"""
    
    # 查找设计计划书
    design_plan = None
    for f in glob.glob(os.path.join(project_dir, "*design*plan*.json")):
        with open(f, 'r', encoding='utf-8') as fp:
            design_plan = json.load(fp)
            break
    
    # 查找发布清单
    checklist = None
    for f in glob.glob(os.path.join(project_dir, "PUBLISH_CHECKLIST.md")):
        with open(f, 'r', encoding='utf-8') as fp:
            checklist = fp.read()
            break
    
    # 查找视频文件
    video_files = []
    for ext in ['*.mp4', '*.mov']:
        video_files.extend(glob.glob(os.path.join(project_dir, ext)))
    
    # 提取故事名
    story_name = os.path.basename(project_dir)
    # 清理日期前缀
    for prefix in ['story-', 'qiqi-']:
        if story_name.startswith(prefix):
            story_name = story_name[len(prefix):]
    
    # 尝试从设计计划书获取更详细的信息
    title = f"{story_name} 琪琪睡前故事"
    description = "儿童成长故事，适合3-8岁小朋友"
    topics = ["#儿童故事", "#睡前故事", "#亲子时光"]
    
    if design_plan:
        story_info = design_plan.get('story', {})
        title = story_info.get('title', story_info.get('name', title))
        description = design_plan.get('summary', description)
        
        # 提取关键词作为话题
        keywords = design_plan.get('keywords', [])
        if keywords:
            topics = [f"#{kw}" for kw in keywords[:3]] + topics[:2]
    
    if checklist:
        # 从发布清单提取标题和话题
        for line in checklist.split('\n'):
            if line.startswith('标题:') or line.startswith('标题：'):
                title = line.split(':', 1)[-1].strip()
            if line.startswith('话题:') or line.startswith('话题：'):
                topic_line = line.split(':', 1)[-1].strip()
                topics = [t.strip() for t in topic_line.split() if t.startswith('#')]
    
    # 找到竖版视频（抖音 9:16）
    vertical_video = None
    horizontal_video = None
    for vf in video_files:
        basename = os.path.basename(vf)
        if 'vertical' in basename.lower() or '竖版' in basename:
            vertical_video = vf
        elif 'horizontal' in basename.lower() or '横版' in basename:
            horizontal_video = vf
    
    # 优先用竖版，没有就用第一个视频
    video_path = vertical_video or horizontal_video or (video_files[0] if video_files else None)
    
    result = {
        "video_path": os.path.abspath(video_path) if video_path else None,
        "title": title,
        "description": description,
        "topics": topics,
        "full_description": f"{description} {' '.join(topics)}"
    }
    
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python3 extract_publish_meta.py <project_dir>")
        print("示例: python3 extract_publish_meta.py project/story-20260514-bee/")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    if not os.path.isdir(project_dir):
        print(f"错误: 目录不存在 - {project_dir}")
        sys.exit(1)
    
    meta = extract_meta(project_dir)
    
    # 输出 JSON
    output_path = os.path.join(project_dir, 'publish_meta.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 元数据已提取到: {output_path}")
    print(f"📹 视频: {meta['video_path']}")
    print(f"📝 标题: {meta['title']}")
    print(f"💬 描述: {meta['full_description']}")
    print(f"🏷️ 话题: {', '.join(meta['topics'])}")
    
    return meta


if __name__ == '__main__':
    main()
