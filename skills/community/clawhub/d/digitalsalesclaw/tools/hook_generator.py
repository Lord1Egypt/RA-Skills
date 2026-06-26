#!/usr/bin/env python3
"""
DigitalSalesClaw - hook_generator.py
独立钩子生成服务
支持5种钩子风格：提问式、故事式、数据式、对比式、情绪式
可生成多平台适配版本

输入: {"topic": "糖尿病饮食", "style": "auto|提问式|故事式|数据式|对比式|情绪式", "platform": "douyin|xiaohongshu|wechat", "count": 3}
输出: {"hooks: [{style, content, usage_tip, platform_tip}], ...}
"""
import sys
import json
import random
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent

# 5种钩子风格定义
HOOK_STYLES = {
    "提问式": {
        "description": "通过提出直击痛点的问题吸引注意力，引发用户思考和互动",
        "characteristics": ["以问号结尾", "引发好奇心", "让用户自我代入"],
        "platforms": {"douyin": "前3秒必须说完", "xiaohongshu": "标题中使用", "wechat": "导语中使用"},
    },
    "故事式": {
        "description": "通过讲述真实或虚构的故事场景，拉近与用户的距离",
        "characteristics": ["有场景感", "有情绪", "有共鸣"],
        "platforms": {"douyin": "适合15-30秒故事型", "xiaohongshu": "笔记开头", "wechat": "文章切入点"},
    },
    "数据式": {
        "description": "通过震撼的数据或研究发现建立权威性",
        "characteristics": ["具体数字", "权威来源", "反差感"],
        "platforms": {"douyin": "数据可视化配合", "xiaohongshu": "封面数据突出", "wechat": "作为论点支撑"},
    },
    "对比式": {
        "description": "通过对比揭示差异，激发用户好奇心",
        "characteristics": ["前后对比", "好坏对比", "认知反差"],
        "platforms": {"douyin": "分屏对比效果佳", "xiaohongshu": "对比图配文", "wechat": "对比论证"},
    },
    "情绪式": {
        "description": "通过强烈的情绪共鸣，让用户感同身受",
        "characteristics": ["情绪强烈", "情感共鸣", "引导转发"],
        "platforms": {"douyin": "BGM配合增强", "xiaohongshu": "情感类笔记", "wechat": "引发共鸣促转发"},
    },
}

# 模板库
HOOK_TEMPLATES = {
    "提问式": [
        lambda t: f"你知道{t}的真相是什么吗？大多数人都在犯这个错！",
        lambda t: f"为什么{t}越来越年轻化了？背后原因你必须知道",
        lambda t: f"关于{t}，医生绝对不会告诉你的3件事",
        lambda t: f"{t}到底听谁的？专家和普通人说的完全不一样！",
        lambda t: f"出现这些症状，你可能是{t}了！快来看看你中招没",
        lambda t: f"同样是{t}，为什么有人恢复快有人恢复慢？",
        lambda t: f"关于{t}，你最想知道的问题是什么？",
        lambda t: f"有{t}困扰的人注意了！这几点必须了解",
    ],
    "故事式": [
        lambda t: f"昨天门诊遇到一个患者，{t}的问题让他后悔不已……",
        lambda t: f"我见过最严重的{t}案例，教训太深刻了",
        lambda t: f"同事的父亲因为{t}差点出事，幸亏发现得早",
        lambda t: f"一个{t}患者的自述：当初要知道这些就好了",
        lambda t: f"三年{t}史，走了无数弯路，终于找到了正确方法",
        lambda t: f"今天去药店买药，药师说的一句话让我茅塞顿开",
        lambda t: f"邻居王阿姨的{t}经历，说出来给大家提个醒",
        lambda t: f"从{t}到康复，我总结了5条经验分享给大家",
    ],
    "数据式": [
        lambda t: f"最新研究显示：90%的人对{t}存在严重误解！",
        lambda t: f"数据说话：关于{t}，你必须知道的3个真相",
        lambda t: f"全国{t}患者已超过1亿！你在其中吗？",
        lambda t: f"每{t}10个患者中就有3个因为这个原因耽误治疗",
        lambda t: f"关于{t}的最新数据曝光，数字触目惊心！",
        lambda t: f"研究证实：坚持这个习惯，{t}风险降低50%！",
        lambda t: f"大数据分析：{t}人群最常见的5个特征",
        lambda t: f"医院统计数据：{t}最容易在哪个季节高发？",
    ],
    "对比式": [
        lambda t: f"左边是错的，右边是对的！关于{t}一次说清楚",
        lambda t: f"普通人 vs 医生处理{t}的区别，惊了！",
        lambda t: f"同样有{t}问题，为什么差距这么大？",
        lambda t: f"有{t}后，这3件事做与不做区别太大了",
        lambda t: f"关于{t}的2种态度，造就了2种截然不同的结果",
        lambda t: f"之前不知道，知道了后悔没早点了解{t}这件事",
        lambda t: f"关于{t}，网上说的和医生说的竟然不一样！",
        lambda t: f"处理{t}问题，聪明人和普通人的做法对比",
    ],
    "情绪式": [
        lambda t: f"因为{t}，我差点失去了最重要的人……",
        lambda t: f"崩溃！{t}这个问题困扰了我整整三年",
        lambda t: f"为什么没人早点告诉我这些？关于{t}的血泪经验",
        lambda t: f"后悔知道太晚！{t}这件事越早了解越好",
        lambda t: f"看完这篇，我终于和{t}和解了",
        lambda t: f"被{t}折磨的日子太难熬了，分享经历帮到更多人",
        lambda t: f"对不起，如果早点知道这些，{t}就不会发生了",
        lambda t: f"太实用了！终于有人把{t}说清楚了",
    ],
}


def generate_hook(topic: str, style: str = "auto", platform: str = "douyin", count: int = 3) -> dict:
    """生成钩子"""
    if style == "auto":
        style = random.choice(list(HOOK_STYLES.keys()))

    style_info = HOOK_STYLES.get(style, HOOK_STYLES["提问式"])
    templates = HOOK_TEMPLATES.get(style, HOOK_TEMPLATES["提问式"])

    hooks = []
    used_templates = set()

    for _ in range(count * 2):
        if len(hooks) >= count:
            break
        template_fn = random.choice(templates)
        content = template_fn(topic)
        if content not in used_templates:
            used_templates.add(content)
            hooks.append({
                "style": style,
                "content": content,
                "characteristics": style_info["characteristics"],
                "platform_tip": style_info["platforms"].get(platform, ""),
                "usage_tip": f"适合{platform}平台，{style_info['platforms'].get(platform, '')}",
            })

    return {
        "topic": topic,
        "style": style,
        "platform": platform,
        "hooks": hooks,
        "style_description": style_info["description"],
        "all_styles_available": list(HOOK_STYLES.keys()),
    }


def generate_all_styles(topic: str, platform: str = "douyin") -> dict:
    """一次性生成所有5种风格的钩子"""
    all_hooks = {}
    for style in HOOK_STYLES.keys():
        result = generate_hook(topic, style, platform, count=2)
        all_hooks[style] = result["hooks"]

    return {
        "topic": topic,
        "platform": platform,
        "all_styles": all_hooks,
        "styles_available": list(HOOK_STYLES.keys()),
    }


def adapt_hook(hook_content: str, from_platform: str, to_platform: str) -> dict:
    """跨平台适配钩子"""
    # 长度适配
    length_map = {
        "douyin": {"min": 15, "max": 40, "tip": "前3秒说完，语言简洁有力"},
        "xiaohongshu": {"min": 20, "max": 60, "tip": "可稍长，增加emoji和悬念"},
        "wechat": {"min": 30, "max": 80, "tip": "可更长，支持复杂句式"},
    }

    adapted = hook_content
    if to_platform == "xiaohongshu" and len(hook_content) > 40:
        # 缩短并增加emoji
        adapted = f"📢 {hook_content[:35]}..."
    elif to_platform == "wechat" and len(hook_content) < 25:
        # 扩充
        adapted = f"【重要提醒】{hook_content}，今天一次说清楚"

    return {
        "original": hook_content,
        "from_platform": from_platform,
        "to_platform": to_platform,
        "adapted": adapted,
        "tip": length_map.get(to_platform, {}).get("tip", ""),
    }


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"topic": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"topic": data}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    topic = args.get("topic", "健康科普")
    style = args.get("style", "auto")
    platform = args.get("platform", "douyin")
    count = args.get("count", 3)
    hook_content = args.get("hook_content")

    if args.get("action") == "all_styles":
        result = generate_all_styles(topic, platform)
    elif args.get("action") == "adapt" and hook_content:
        result = adapt_hook(hook_content, args.get("from_platform", "douyin"), args.get("to_platform", "xiaohongshu"))
    else:
        result = generate_hook(topic, style, platform, count)

    print(json.dumps(result, ensure_ascii=False, indent=2))
