#!/usr/bin/env python3
"""
Dan Koe 写作系统 - Writing Clone (重构版)
从积木库构建写作上下文，输出 prompt 供 Agent 使用

用法:
    python write.py --topic "写作"                    # 从积木库生成上下文
    python write.py --topic "写作" --platform wechat  # 针对微信公众号格式
    python write.py --topic "写作" --platform xhs      # 针对小红书格式
    python write.py --topic "写作" --platform twitter   # 针对推特/微博格式
    python write.py --length 500                       # 短文 (500字)
    python write.py --length 2000                      # 长文 (2000字)
    python write.py --json                             # 输出 JSON 格式
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# ========== 配置 ==========
KNOWLEDGE_DIR = Path(__file__).parent.parent / "references" / "knowledge"

# ========== 平台模板 ==========

PLATFORM_TEMPLATES = {
    "wechat": {
        "name": "微信公众号",
        "emoji": "📱",
        "max_length": 30000,
        "style": "长文、深度分析、口语化、有温度、带 emoji",
        "format": "标题\n\n正文（分段落，带 emoji）\n\n#话题标签#"
    },
    "xhs": {
        "name": "小红书",
        "emoji": "📕",
        "max_length": 1000,
        "style": "口语化、短句为主、大量 emoji、分点列表、个人经历分享",
        "format": "【标题】\n\n正文（短句+emoji）\n\n#标签1 #标签2 #标签3"
    },
    "twitter": {
        "name": "Twitter/微博",
        "emoji": "🐦",
        "max_length": 280,
        "style": "极简、一句话一个观点、有洞察力、可转发",
        "format": "一句话 hook\n\n核心观点（1-2句）\n\n[可选] 行动号召或标签"
    },
    "midjourney": {
        "name": "Medium/ newsletter",
        "emoji": "✍️",
        "max_length": 5000,
        "style": "深度分析、结构清晰、有个人 POV、说服力强",
        "format": "标题\n\nHook\n\n正文（分节）\n\n结论 + CTA"
    },
    "default": {
        "name": "通用",
        "emoji": "📝",
        "max_length": 5000,
        "style": "清晰、有观点、有价值",
        "format": "标题\n\n正文\n\n结语"
    }
}

# ========== 加载积木 ==========

def load_knowledge() -> dict:
    """加载所有积木库"""
    files = {
        "hooks": KNOWLEDGE_DIR / "hooks.md",
        "paradoxes": KNOWLEDGE_DIR / "paradoxes.md",
        "arcs": KNOWLEDGE_DIR / "arcs.md",
        "core_problems": KNOWLEDGE_DIR / "core_problems.md",
        "golden_phrases": KNOWLEDGE_DIR / "golden_phrases.md",
        "structures": KNOWLEDGE_DIR / "structures.md",
        "perspectives": KNOWLEDGE_DIR / "perspectives.md"
    }

    knowledge = {}
    for key, filepath in files.items():
        knowledge[key] = []
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            # 按 --- 分隔，但跳过第一块（文件头）
            entries = content.split("---\n")
            for entry in entries[1:]:
                stripped = entry.strip()
                # 跳过纯元数据行（以 # 开头的是标题，以 > 开头的是引用元数据）
                if stripped and not stripped.startswith("# ") and not stripped.startswith("> " * 3):
                    knowledge[key].append(entry)
    return knowledge


def extract_text(entry: str) -> str:
    """从条目中提取核心文本"""
    lines = entry.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# ") or line.startswith("## ") or line.startswith("---"):
            continue
        for prefix in ["**原文片段:", "**悖论原文:", "**核心观点:", "> \""]:
            if prefix in line:
                return line.replace(prefix, "").replace("\"", "").strip()
    return ""


def parse_entry(entry: str) -> dict:
    """解析单个积木条目"""
    lines = entry.split("\n")
    result = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith("### "):
            result["title"] = line.replace("### ", "").strip()
        elif line.startswith("**类型:**"):
            result["type"] = line.replace("**类型:**", "").strip()
        elif line.startswith("**原文片段:"):
            result["text"] = line.replace("**原文片段:", "").strip()
        elif line.startswith("**悖论原文:"):
            result["text"] = line.replace("**悖论原文:", "").strip().strip('"')
        elif line.startswith("**核心观点:"):
            result["text"] = line.replace("**核心观点:", "").strip()
        elif line.startswith("**为什么有效:"):
            result["why_works"] = line.replace("**为什么有效:", "").strip()
        elif line.startswith("**适用场景:"):
            result["when_to_use"] = line.replace("**适用场景:", "").strip()
        elif line.startswith("**适用话题:"):
            result["topics"] = [t.strip() for t in line.replace("**适用话题:", "").split(",")]
    
    if "text" not in result:
        result["text"] = extract_text(entry)
    
    return result


def build_context(knowledge: dict, topic: str = "") -> dict:
    """从积木库构建写作上下文"""
    topic_filter = topic.lower()
    
    result = {
        "platform": None,
        "target_length": None,
        "topic": topic,
        "blocks": {
            "hooks": [],
            "paradoxes": [],
            "arcs": [],
            "core_problems": [],
            "golden_phrases": [],
            "structures": [],
            "perspectives": []
        }
    }

    type_names = {
        "hooks": "🎣 钩子",
        "paradoxes": "🔄 悖论",
        "arcs": "📈 转化弧",
        "core_problems": "💢 核心问题",
        "golden_phrases": "✨ 金句",
        "structures": "🏗️ 结构",
        "perspectives": "💡 观点"
    }

    for block_type, items in knowledge.items():
        if not items:
            continue
        
        # 按话题过滤
        if topic_filter:
            filtered = []
            for item in items:
                parsed = parse_entry(item)
                text = json.dumps(parsed, ensure_ascii=False).lower()
                if topic_filter in text:
                    filtered.append(item)
            filtered = filtered[:5]  # 最多5条
        else:
            filtered = items[:5]
        
        for item in filtered:
            parsed = parse_entry(item)
            if parsed.get("text") or parsed.get("title"):
                result["blocks"][block_type].append(parsed)

    return result


def format_prompt(context: dict, platform: str, length: int) -> str:
    """生成写作 prompt"""
    platform_info = PLATFORM_TEMPLATES.get(platform, PLATFORM_TEMPLATES["default"])
    
    # 构建积木库素材展示
    blocks_text = []
    blocks_text.append("\n【积木库素材】\n")
    
    for block_type, items in context["blocks"].items():
        if not items:
            continue
        type_names = {
            "hooks": "🎣 钩子",
            "paradoxes": "🔄 悖论",
            "arcs": "📈 转化弧",
            "core_problems": "💢 核心问题",
            "golden_phrases": "✨ 金句",
            "structures": "🏗️ 结构",
            "perspectives": "💡 观点"
        }
        blocks_text.append(f"\n## {type_names.get(block_type, block_type)}")
        for item in items[:3]:
            if block_type == "hooks":
                blocks_text.append(f"- [{item.get('type', '未知')}] {item.get('text', item.get('title', ''))}")
            else:
                blocks_text.append(f"- {item.get('text', item.get('title', ''))}")

    prompt = f"""请基于以下素材，写一篇关于「{context['topic']}」的文章。

平台: {platform_info['name']}
风格: {platform_info['style']}
字数目标: 约 {length} 字

输出格式:
{platform_info['format']}

{''.join(blocks_text)}

写作要求:
1. 先用强钩子抓住注意力（参考提供的积木库素材）
2. 引入认知冲突或悖论引发共鸣
3. 给出清晰的结构和可操作的建议
4. 用金句收尾，制造记忆点
5. 融入提供的积木库素材，但不要照抄，要重新组合
6. 不要列提纲，直接写完整的正文内容

重要: 写完后请用 JSON 格式输出文章:
{{
  "title": "文章标题",
  "content": "完整正文（不要分点，要连贯段落）",
  "tags": ["标签1", "标签2"]
}}"""

    return prompt


def format_context_as_markdown(context: dict, platform: str, length: int) -> str:
    """格式化为 Markdown 输出"""
    platform_info = PLATFORM_TEMPLATES.get(platform, PLATFORM_TEMPLATES["default"])
    
    lines = []
    lines.append(f"\n{'='*50}")
    lines.append(f"📝 写作上下文")
    lines.append(f"{'='*50}\n")
    
    lines.append(f"🎯 主题: {context['topic']}")
    lines.append(f"📱 平台: {platform_info['name']}")
    lines.append(f"📏 字数: 约 {length} 字")
    lines.append(f"🎨 风格: {platform_info['style']}")
    lines.append("")
    
    type_names = {
        "hooks": "🎣 钩子",
        "paradoxes": "🔄 悖论",
        "arcs": "📈 转化弧",
        "core_problems": "💢 核心问题",
        "golden_phrases": "✨ 金句",
        "structures": "🏗️ 结构",
        "perspectives": "💡 观点"
    }
    
    for block_type, items in context["blocks"].items():
        if items:
            lines.append(f"\n## {type_names.get(block_type, block_type)} ({len(items)}条)")
            for item in items[:3]:
                if block_type == "hooks":
                    lines.append(f"- [{item.get('type', '未知')}] {item.get('text', item.get('title', ''))}")
                else:
                    lines.append(f"- {item.get('text', item.get('title', ''))}")
    
    lines.append(f"\n{'='*50}")
    lines.append("💡 使用说明:")
    lines.append("   1. 将上述素材作为 context 让 AI Agent 生成文章")
    lines.append("   2. 或者运行: python write.py --topic ... --json")
    lines.append("=" * 50)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Dan Koe Writing Clone - 从积木库生成写作上下文")
    parser.add_argument("--topic", "-t", default="", help="文章主题/话题")
    parser.add_argument("--platform", "-p", default="default",
                        choices=["wechat", "xhs", "twitter", "midjourney", "default"],
                        help="目标平台")
    parser.add_argument("--length", "-l", type=int, default=2000, help="目标字数")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式 (包含 prompt)")

    args = parser.parse_args()

    platform_info = PLATFORM_TEMPLATES.get(args.platform, PLATFORM_TEMPLATES["default"])

    print(f"\n✍️  Dan Koe 写作系统 - {platform_info['name']} 生成器")
    print(f"{'='*50}")

    knowledge = load_knowledge()
    total_blocks = sum(len(v) for v in knowledge.values())

    if total_blocks == 0:
        print("⚠️  积木库为空！")
        print("请先运行 goldmine.py 填充积木库")
        return

    print(f"📚 积木库: {total_blocks} 条积木")
    print(f"🎯 平台: {platform_info['name']}")
    print(f"📏 字数: 约 {args.length} 字")
    print()

    # 构建上下文
    topic = args.topic or "个人成长和内容创作"
    context = build_context(knowledge, topic)
    context["platform"] = args.platform
    context["target_length"] = args.length

    if args.json:
        # 输出完整 JSON（包含 prompt）
        prompt = format_prompt(context, args.platform, args.length)
        context["prompt"] = prompt
        
        # 计算积木总数
        total = sum(len(v) for v in context["blocks"].values())
        
        print(json.dumps({
            "success": True,
            "context": context,
            "prompt": prompt,
            "stats": {
                "total_blocks": total,
                "hooks": len(context["blocks"]["hooks"]),
                "paradoxes": len(context["blocks"]["paradoxes"]),
                "arcs": len(context["blocks"]["arcs"]),
                "golden_phrases": len(context["blocks"]["golden_phrases"]),
                "structures": len(context["blocks"]["structures"]),
                "perspectives": len(context["blocks"]["perspectives"])
            }
        }, ensure_ascii=False, indent=2))
    else:
        # 输出 Markdown 格式
        print(format_context_as_markdown(context, args.platform, args.length))

    print(f"\n{'='*50}")
    print("💡 后续步骤:")
    print("   - 将 context 和 prompt 交给 AI Agent 生成文章")
    print("   - 运行 spark.py 探索更多创意方向")
    print("   - 运行 goldmine.py 拆解这篇内容，补充积木库")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
