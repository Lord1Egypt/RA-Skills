#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短视频脚本生成器
支持抖音、小红书、视频号平台
包含爆款元素：黄金开场、情绪曲线、互动引导
"""

import json
import os
import sys
from dataclasses import dataclass
from typing import Optional

# 尝试导入OpenAI（可选依赖）
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class VideoScript:
    """视频脚本结构"""
    topic: str
    platform: str
    style: str
    duration: str
    shots: list
    tips: list


# 平台规范
PLATFORM_RULES = {
    "抖音": {
        "节奏": "快节奏，前3秒必须抓住眼球",
        "时长": "15-60秒最佳",
        "风格": "接地气、有梗、节奏感强",
        "音乐": "热门BGM、卡点",
        "开场": "反问/痛点/悬念"
    },
    "小红书": {
        "节奏": "沉浸式，娓娓道来",
        "时长": "60-180秒",
        "风格": "精致、真实、有温度",
        "音乐": "轻音乐、治愈系",
        "开场": "场景带入/价值承诺"
    },
    "视频号": {
        "节奏": "专业感，干货为主",
        "时长": "30-90秒",
        "风格": "专业、有深度、实用",
        "音乐": "商务风格BGM",
        "开场": "数据/观点/问题"
    }
}

# 脚本类型模板
SCRIPT_TEMPLATES = {
    "种草": {
        "structure": ["痛点开场", "产品亮相", "功能展示", "使用场景", "效果对比", "互动引导"],
        "情绪曲线": "好奇→痛点→期待→满足→行动"
    },
    "知识分享": {
        "structure": ["问题抛出", "答案预告", "核心内容", "案例说明", "总结升华", "关注引导"],
        "情绪曲线": "困惑→好奇→恍然→收获→认同"
    },
    "情感故事": {
        "structure": ["场景铺垫", "冲突呈现", "情绪爆发", "转折处理", "结局升华", "共鸣引导"],
        "情绪曲线": "平静→紧张→共鸣→感动→治愈"
    },
    "教程讲解": {
        "structure": ["效果预告", "问题引入", "步骤拆解", "要点强调", "成果展示", "练习引导"],
        "情绪曲线": "期待→清晰→掌握→成就感"
    },
    "剧情": {
        "structure": ["开场悬念", "人物设定", "冲突发展", "高潮转折", "结局反转", "互动提问"],
        "情绪曲线": "好奇→紧张→意外→满足→期待"
    },
    "口播": {
        "structure": ["观点抛出", "论据支撑", "案例佐证", "对立观点驳斥", "价值升华", "行动号召"],
        "情绪曲线": "认同→思考→信服→行动"
    }
}

# 爆款开场库
HOOK_TEMPLATES = {
    "反问型": [
        "你还在为{痛点}烦恼吗？",
        "为什么{现象}？今天告诉你真相",
        "90%的人都不知道{秘密}",
        "{问题}怎么办？一招解决"
    ],
    "数据型": [
        "我测试了{数字}款{产品}，发现{结论}",
        "只有{比例}的人知道这个方法",
        "用时{时间}，我{成果}"
    ],
    "痛点型": [
        "如果你也{痛点}，一定要看完",
        "别再{错误做法}了！正确方法是",
        "{问题}真的太难了...直到我发现"
    ],
    "悬念型": [
        "最后{时间}告诉你答案",
        "你可能想不到，{反常识结论}",
        "这个{东西}改变了我的{方面}"
    ],
    "场景型": [
        "场景：{具体场景}，然后{转折}",
        "当你在{场景}时，注意{要点}",
        "想象一下，{理想状态}"
    ]
}


def generate_script_ai(topic: str, platform: str, style: str) -> Optional[VideoScript]:
    """使用AI生成脚本（需要OPENAI_API_KEY）"""
    if not HAS_OPENAI:
        return None

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        client = openai.OpenAI(api_key=api_key)

        rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["抖音"])
        template = SCRIPT_TEMPLATES.get(style, SCRIPT_TEMPLATES["种草"])

        prompt = f"""你是一个短视频脚本专家。请为主题"{topic}"生成一个短视频脚本。

平台：{platform}
类型：{style}

平台规范：
- 节奏：{rules['节奏']}
- 时长：{rules['时长']}
- 风格：{rules['风格']}
- 开场风格：{rules['开场']}

脚本结构应包含：{' → '.join(template['structure'])}

请以JSON格式输出，包含以下字段：
{{
  "topic": "主题",
  "platform": "平台",
  "style": "类型",
  "duration": "建议时长",
  "shots": [
    {{
      "shot_number": 1,
      "time": "0-3秒",
      "type": "黄金开场",
      "scene": "画面描述",
      "dialogue": "台词/旁白",
      "music": "BGM/音效",
      "notes": "拍摄要点"
    }}
  ],
  "tips": ["拍摄建议1", "拍摄建议2"]
}}

只输出JSON，不要其他内容。"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=2000
        )

        content = response.choices[0].message.content
        # 提取JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        data = json.loads(content.strip())
        return VideoScript(
            topic=data["topic"],
            platform=data["platform"],
            style=data["style"],
            duration=data["duration"],
            shots=data["shots"],
            tips=data["tips"]
        )
    except Exception as e:
        print(f"AI生成失败: {e}", file=sys.stderr)
        return None


def generate_script_template(topic: str, platform: str, style: str) -> VideoScript:
    """模板生成脚本（无需API）"""
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["抖音"])
    template = SCRIPT_TEMPLATES.get(style, SCRIPT_TEMPLATES["种草"])

    # 根据类型生成不同的分镜
    shots = []

    if style == "种草":
        shots = [
            {
                "shot_number": 1,
                "time": "0-3秒",
                "type": "黄金开场（痛点）",
                "scene": f"特写镜头：展示{topic}解决的问题场景（如疲惫/困扰状态）",
                "dialogue": f"还在为{topic}的效果发愁？今天分享我的真实体验",
                "music": "卡点音效+热门BGM前奏",
                "notes": "眼神要有戏，表情真实"
            },
            {
                "shot_number": 2,
                "time": "3-10秒",
                "type": "产品亮相",
                "scene": f"产品特写：{topic}正面展示，光线打亮质感",
                "dialogue": f"就是这个{topic}，我已经用了X周了",
                "music": "BGM渐强",
                "notes": "产品要拍出高级感"
            },
            {
                "shot_number": 3,
                "time": "10-25秒",
                "type": "功能展示",
                "scene": f"使用过程：展示{topic}的核心功能/用法，多个场景切换",
                "dialogue": "它的XX功能真的很实用，特别是XX场景下",
                "music": "轻快节奏",
                "notes": "展示真实使用过程，不要太刻意"
            },
            {
                "shot_number": 4,
                "time": "25-40秒",
                "type": "效果对比",
                "scene": "分屏对比：使用前后的变化",
                "dialogue": "来看对比，效果真的很明显",
                "music": "音效突出对比时刻",
                "notes": "对比要真实可信"
            },
            {
                "shot_number": 5,
                "time": "40-55秒",
                "type": "价值总结",
                "scene": "产品+人物同框，自然光",
                "dialogue": f"{topic}真的改变了我的XX，强烈推荐给XX人群",
                "music": "BGM高潮",
                "notes": "真诚是必杀技"
            },
            {
                "shot_number": 6,
                "time": "55-60秒",
                "type": "互动引导",
                "scene": "人物面对镜头，手势引导",
                "dialogue": "评论区说说你的使用心得吧～关注我，下期分享XX",
                "music": "BGM渐弱",
                "notes": "表情要自然期待"
            }
        ]
    elif style == "知识分享":
        shots = [
            {
                "shot_number": 1,
                "time": "0-3秒",
                "type": "问题抛出",
                "scene": "人物面对镜头，背景简洁",
                "dialogue": f"关于{topic}，很多人都搞错了",
                "music": "疑问音效",
                "notes": "语气要权威但不傲慢"
            },
            {
                "shot_number": 2,
                "time": "3-8秒",
                "type": "答案预告",
                "scene": "文字卡片+人物讲解",
                "dialogue": "今天告诉你正确答案，记得看到最后",
                "music": "轻快BGM",
                "notes": "制造期待感"
            },
            {
                "shot_number": 3,
                "time": "8-35秒",
                "type": "核心内容",
                "scene": "图示/演示+讲解",
                "dialogue": f"关于{topic}的三个要点：第一...第二...第三...",
                "music": "背景音乐稳定",
                "notes": "信息密度要高，但不要着急"
            },
            {
                "shot_number": 4,
                "time": "35-50秒",
                "type": "案例说明",
                "scene": "真实案例图片/视频",
                "dialogue": "举个例子，XX就是用了这个方法...",
                "music": "案例部分BGM变化",
                "notes": "案例要真实可验证"
            },
            {
                "shot_number": 5,
                "time": "50-58秒",
                "type": "总结升华",
                "scene": "人物特写",
                "dialogue": f"总结一下，{topic}的关键就是...",
                "music": "总结感BGM",
                "notes": "提炼核心价值"
            },
            {
                "shot_number": 6,
                "time": "58-60秒",
                "type": "关注引导",
                "scene": "手势引导关注",
                "dialogue": "关注我，每天分享XX干货",
                "music": "BGM收尾",
                "notes": "动作要自然"
            }
        ]
    else:
        # 通用结构
        for i, stage in enumerate(template["structure"]):
            shots.append({
                "shot_number": i + 1,
                "time": f"{i * 10}-{(i + 1) * 10}秒",
                "type": stage,
                "scene": f"【{stage}】画面待设计",
                "dialogue": f"【{stage}】台词待填写",
                "music": "BGM建议待定",
                "notes": "根据实际内容调整"
            })

    return VideoScript(
        topic=topic,
        platform=platform,
        style=style,
        duration=rules["时长"],
        shots=shots,
        tips=[
            f"遵循{platform}平台规范：{rules['风格']}",
            f"开场使用{rules['开场']}方式",
            f"建议配乐风格：{rules['音乐']}",
            "保持情绪曲线完整",
            "结尾必须有互动引导"
        ]
    )


def format_output(script: VideoScript) -> str:
    """格式化输出"""
    lines = []
    lines.append(f"【短视频脚本】主题：{script.topic}")
    lines.append(f"【平台】{script.platform}")
    lines.append(f"【类型】{script.style}")
    lines.append(f"【时长】{script.duration}")
    lines.append("")
    lines.append("=== 分镜脚本 ===")
    lines.append("")

    for shot in script.shots:
        lines.append(f"【镜头{shot['shot_number']}】{shot['time']}（{shot['type']}）")
        lines.append(f"画面：{shot['scene']}")
        lines.append(f"台词：{shot['dialogue']}")
        lines.append(f"音效：{shot['music']}")
        lines.append(f"备注：{shot['notes']}")
        lines.append("")

    lines.append("=== 拍摄建议 ===")
    for i, tip in enumerate(script.tips, 1):
        lines.append(f"{i}. {tip}")

    return "\n".join(lines)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="短视频脚本生成器")
    parser.add_argument("--topic", "-t", required=True, help="主题/产品")
    parser.add_argument("--platform", "-p", default="抖音", choices=["抖音", "小红书", "视频号"], help="目标平台")
    parser.add_argument("--style", "-s", default="种草", choices=["种草", "知识分享", "情感故事", "教程讲解", "剧情", "口播"], help="脚本类型")
    parser.add_argument("--ai", action="store_true", help="使用AI增强生成（需要OPENAI_API_KEY）")

    args = parser.parse_args()

    # 尝试AI生成
    if args.ai or os.environ.get("OPENAI_API_KEY"):
        script = generate_script_ai(args.topic, args.platform, args.style)
        if script:
            print(format_output(script))
            return

    # 模板生成
    script = generate_script_template(args.topic, args.platform, args.style)
    print(format_output(script))


if __name__ == "__main__":
    main()
