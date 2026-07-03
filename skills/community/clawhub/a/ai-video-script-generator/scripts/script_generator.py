#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI视频脚本生成器
输入主题+平台 → 输出完整视频脚本（含分镜、台词、BGM、标签）
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# ============ 平台配置 ============

PLATFORM_CONFIG = {
    "douyin": {
        "name": "抖音",
        "duration_range": (15, 60),
        "default_duration": 45,
        "hook_types": ["冲突型", "数字型", "悬念型", "揭秘型"],
        "script_structure": [
            (0, 3, "开场钩子"),
            (3, 15, "核心内容（3个要点）"),
            (15, 30, "详细展开（案例/演示）"),
            (30, 45, "价值升华（收益/成果）"),
            (45, 60, "行动号召（关注/评论/转发）"),
        ],
        "hashtag_count": 8,
        "best_times": ["12:00", "18:00", "21:00"],
    },
    "xhs": {
        "name": "小红书",
        "duration_range": (30, 90),
        "default_duration": 60,
        "hook_types": ["种草型", "测评型", "教程型"],
        "script_structure": [
            (0, 5, "痛点引入"),
            (5, 20, "方法介绍（3步法）"),
            (20, 45, "实操演示"),
            (45, 60, "效果展示"),
            (60, 90, "互动引导（收藏/关注）"),
        ],
        "hashtag_count": 10,
        "best_times": ["08:00", "12:00", "20:00"],
    },
    "bilibili": {
        "name": "B站",
        "duration_range": (180, 600),
        "default_duration": 300,
        "hook_types": ["深度型", "揭秘型", "教程型"],
        "script_structure": [
            (0, 30, "精彩预告（高光片段）"),
            (30, 120, "引入背景 + 问题提出"),
            (120, 300, "核心内容展开（分章节）"),
            (300, 480, "案例/演示"),
            (480, 600, "总结 + 互动引导"),
        ],
        "hashtag_count": 8,
        "best_times": ["18:00", "22:00"],
    },
}

# ============ 风格模板库 ============

STYLE_TEMPLATES = {
    "tutorial": {
        "hooks": [
            "别再{action}了！{num}个技巧让你{method}",
            "学会这{num}点，{topic}不再难",
            "{num}年经验总结：{topic}最重要的{num}件事",
        ],
        "transitions": ["接下来", "然后", "第三步", "最后"],
        "closings": ["学会了吗？关注我，更多干货", "收藏起来慢慢看", "评论区告诉我你的想法"],
    },
    "story": {
        "hooks": [
            "我以为{topic}很难，直到我用了这个方法",
            "关于{topic}，今天说点不一样的",
            "这个{topic}技巧，80%的人不会",
        ],
        "transitions": ["后来", "没想到", "结果", "最后发现"],
        "closings": ["这就是我的故事", "希望对你有启发", "记得点赞关注哦"],
    },
    "review": {
        "hooks": [
            "{topic}测评｜真实使用感受",
            "花{num}元买的{topic}，值不值？",
            "3款{topic}横向对比，谁赢了？",
        ],
        "transitions": ["首先看", "然后是", "接着测试", "最后总结"],
        "closings": ["总体来说", "推荐指数：{num}星", "你会买吗？评论区见"],
    },
}

# ============ 核心逻辑 ============

def generate_hook(topic, style="tutorial"):
    """生成开场钩子"""
    import random
    templates = STYLE_TEMPLATES.get(style, STYLE_TEMPLATES["tutorial"])["hooks"]
    template = random.choice(templates)

    # 填充模板
    result = template.replace("{topic}", topic)
    result = result.replace("{num}", str(random.randint(3, 7)))
    result = result.replace("{action}", "浪费时间")
    result = result.replace("{method}", "效率翻倍")

    return result


def generate_script_structure(platform, duration, topic, style="tutorial"):
    """生成分镜脚本"""
    cfg = PLATFORM_CONFIG[platform]
    structure = cfg["script_structure"]

    script = []
    for (start, end, desc) in structure:
        if end > duration:
            end = duration
        if start >= duration:
            break

        # 生成该时间段的台词
        line_duration = end - start
        line_template = f"{desc}（{line_duration}秒）"
        script.append({
            "start": start,
            "end": end,
            "duration": line_duration,
            "scene": desc,
            "line": f"【{desc}】这里是{topic}的内容...",
            "visual": "画面描述",
            "bgm": "BGM建议",
        })

    return script


def generate_hashtags(topic, platform):
    """生成话题标签"""
    base_tags = [
        f"#{topic}",
        "#AI工具", "#干货分享", "#效率神器",
        "#自媒体", "#涨粉技巧", "#副业赚钱",
    ]

    platform_tags = {
        "douyin": ["#抖音运营", "#短视频制作", "#爆款视频"],
        "xhs": ["#小红书运营", "#种草清单", "#好物推荐"],
        "bilibili": ["#B站UP主", "#知识分享", "#科技数码"],
    }

    tags = base_tags + platform_tags.get(platform, [])
    return list(set(tags))[:PLATFORM_CONFIG[platform]["hashtag_count"]]


def generate_full_script(topic, platform="douyin", style="tutorial", duration=None):
    """生成完整脚本"""
    cfg = PLATFORM_CONFIG[platform]

    if duration is None:
        duration = cfg["default_duration"]

    # 确保时长在合理范围内
    min_d, max_d = cfg["duration_range"]
    duration = max(min_d, min(max_d, duration))

    # 生成各部分
    hook = generate_hook(topic, style)
    script_structure = generate_script_structure(platform, duration, topic, style)
    hashtags = generate_hashtags(topic, platform)

    # 组装完整脚本
    full_script = {
        "topic": topic,
        "platform": cfg["name"],
        "platform_id": platform,
        "style": style,
        "duration": duration,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hook": hook,
        "script": script_structure,
        "hashtags": hashtags,
        "best_times": cfg["best_times"],
        "cover_text": f"{hook[:15]}...",
    }

    return full_script


def format_script_markdown(script):
    """格式化为Markdown"""
    md = f"""# {script['platform']}脚本 - {script['topic']}（{script['style']}类）

## 基本信息
- 主题：{script['topic']}
- 平台：{script['platform']}
- 时长：{script['duration']}秒
- 风格：{script['style']}类

## 开场钩子（0-3秒）
{script['hook']}

## 分镜脚本

| 时间 | 画面 | 台词 | BGM |
|------|------|------|-----|
"""

    for scene in script["script"]:
        md += f"| {scene['start']}-{scene['end']}秒 | {scene['visual']} | {scene['line']} | {scene['bgm']} |\n"

    md += f"""
## 封面文案
{script['cover_text']}

## 话题标签
{' '.join(script['hashtags'])}

## 最佳发布时间
{', '.join(script['best_times'])}
"""

    return md


def save_script(script, output_dir=None):
    """保存脚本到文件"""
    output_dir = Path(output_dir or Path.home() / "video-scripts")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 保存到 history 子目录
    history_dir = output_dir / "history"
    history_dir.mkdir(exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"{script['platform_id']}_{script['topic'][:10]}_{date_str}.md"
    filepath = history_dir / filename

    markdown = format_script_markdown(script)
    filepath.write_text(markdown, encoding="utf-8")

    # 更新 memory.md（简化版）
    memory_path = output_dir / "memory.md"
    if not memory_path.exists():
        memory_path.write_text(f"# 视频脚本风格记忆\n\n## 最近脚本\n\n")

    with open(memory_path, "a", encoding="utf-8") as f:
        f.write(f"### {script['topic']} ({script['platform']})\n")
        f.write(f"- 风格：{script['style']}\n")
        f.write(f"- 钩子：{script['hook']}\n")
        f.write(f"- 时间：{script['generated_at']}\n\n")

    return filepath


def main():
    parser = argparse.ArgumentParser(description="AI视频脚本生成器")
    parser.add_argument("--topic", "-t", type=str, required=True, help="视频主题")
    parser.add_argument("--platform", "-p", type=str, default="douyin",
                        choices=["douyin", "xhs", "bilibili"], help="目标平台")
    parser.add_argument("--style", "-s", type=str, default="tutorial",
                        choices=["tutorial", "story", "review"], help="内容风格")
    parser.add_argument("--duration", "-d", type=int, help="视频时长（秒）")
    parser.add_argument("--output", "-o", type=str, help="输出目录")
    args = parser.parse_args()

    print(f"\n🎬 正在为【{args.topic}】生成{PLATFORM_CONFIG[args.platform]['name']}脚本...")
    print(f"   风格：{args.style} | 平台：{args.platform}\n")

    script = generate_full_script(args.topic, args.platform, args.style, args.duration)
    markdown = format_script_markdown(script)

    print(markdown)

    if args.output or True:  # 默认保存
        path = save_script(script, args.output)
        print(f"\n✅ 脚本已保存: {path}")


if __name__ == "__main__":
    main()
