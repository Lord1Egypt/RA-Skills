#!/usr/bin/env python3
"""
Dan Koe 写作系统 - Idea Spark (重构版)
从积木库中随机组合，生成多个可写的创意方向，输出 JSON 供 Agent 使用

用法:
    python spark.py                          # 随机生成3个方向 (Markdown)
    python spark.py --count 5               # 生成5个方向
    python spark.py --topic "写作"          # 指定话题过滤
    python spark.py --json                   # 输出 JSON 格式
    python spark.py --hook                  # 只用钩子生成
"""

import os
import re
import random
import json
import argparse
from pathlib import Path
from datetime import datetime

# ========== 配置 ==========
KNOWLEDGE_DIR = Path(__file__).parent.parent / "references" / "knowledge"
OUTPUT_JSON = False

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
            # 第一项是文件头元数据，跳过
            for entry in entries[1:]:
                stripped = entry.strip()
                # 跳过纯元数据行
                if stripped and not stripped.startswith("# ") and not stripped.startswith("> " * 3):
                    knowledge[key].append(entry)
    return knowledge


def extract_title(entry: str) -> str:
    """从条目中提取标题"""
    lines = entry.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# ") or line.startswith("**") or line.startswith("---"):
            continue
        if line.startswith("## "):
            # 去除来源日期信息
            title = line.replace("## ", "").strip()
            title = re.sub(r"\s*\(来源:.*?日期:.*?\)", "", title)
            return title
        if line.startswith("### "):
            return line.replace("### ", "").strip()
    # 取第一行非空非元数据行
    for line in lines:
        line = line.strip()
        if line and not line.startswith("*最后更新") and not line.startswith("## "):
            return line[:50]
    return ""


def extract_text(entry: str) -> str:
    """从条目中提取核心文本"""
    lines = entry.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# ") or line.startswith("## ") or line.startswith("---"):
            continue
        for prefix in ["**原文片段:**", "**悖论原文:**", "**核心观点:**", "> \"", "**为什么有力:**", "**为什么有效:**"]:
            if prefix in line:
                return line.replace(prefix, "").replace("\"", "").strip()
        # 捕获 ### 标题
        if line.startswith("### "):
            return line.replace("### ", "").strip()
    return ""


def parse_entry(entry: str, entry_type: str) -> dict:
    """解析单个积木条目"""
    lines = entry.split("\n")
    result = {
        "title": extract_title(entry),
        "text": extract_text(entry),
        "type": entry_type
    }
    
    # 提取额外字段
    for line in lines:
        line = line.strip()
        if line.startswith("**类型:**"):
            result["hook_type"] = line.replace("**类型:**", "").strip()
        elif line.startswith("**为什么有效:**"):
            result["why_works"] = line.replace("**为什么有效:**", "").strip()
        elif line.startswith("**适用场景:**"):
            result["when_to_use"] = line.replace("**适用场景:**", "").strip()
        elif line.startswith("**为什么有力:**"):
            result["why_powerful"] = line.replace("**为什么有力:**", "").strip()
        elif line.startswith("**适用话题:**"):
            result["topics"] = [t.strip() for t in line.replace("**适用话题:**", "").split(",")]
        elif line.startswith("**典型话题:**"):
            result["topics"] = [t.strip() for t in line.replace("**典型话题:**", "").split(",")]
        elif line.startswith("**激活词/触发语:**"):
            result["trigger_words"] = [t.strip() for t in line.replace("**激活词/触发语:**", "").split(",")]
    
    return result


def combine_into_idea(knowledge: dict, topic_filter: str = "") -> dict:
    """从积木库中随机组合生成一个创意方向"""

    def filter_by_topic(items, keyword):
        if not keyword:
            return items
        return [item for item in items if keyword.lower() in item.lower()]

    # 随机选择一个钩子
    hooks = filter_by_topic(knowledge.get("hooks", []), topic_filter)
    selected_hook = random.choice(hooks) if hooks else None

    # 随机选择一个悖论
    paradoxes = filter_by_topic(knowledge.get("paradoxes", []), topic_filter)
    selected_paradox = random.choice(paradoxes) if paradoxes else None

    # 随机选择一个转化弧
    arcs = filter_by_topic(knowledge.get("arcs", []), topic_filter)
    selected_arc = random.choice(arcs) if arcs else None

    # 随机选择1-2个金句
    phrases = filter_by_topic(knowledge.get("golden_phrases", []), topic_filter)
    selected_phrases = random.sample(phrases, min(2, len(phrases))) if phrases else []

    # 随机选择一个结构
    structures = filter_by_topic(knowledge.get("structures", []), topic_filter)
    selected_structure = random.choice(structures) if structures else None

    # 随机选择一个观点
    perspectives = filter_by_topic(knowledge.get("perspectives", []), topic_filter)
    selected_perspective = random.choice(perspectives) if perspectives else None

    return {
        "hook": selected_hook,
        "paradox": selected_paradox,
        "arc": selected_arc,
        "phrases": selected_phrases,
        "structure": selected_structure,
        "perspective": selected_perspective
    }


def format_idea_as_markdown(idea: dict, index: int) -> str:
    """格式化输出一个创意方向 (Markdown)"""
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"📝 创意方向 #{index}")
    output.append(f"{'='*60}\n")

    if idea["hook"]:
        parsed = parse_entry(idea["hook"], "hook")
        output.append(f"🎣 钩子:")
        output.append(f"   {parsed['text'] or parsed['title']}")
        if parsed.get("hook_type"):
            output.append(f"   类型: {parsed['hook_type']}")
        output.append("")

    if idea["paradox"]:
        parsed = parse_entry(idea["paradox"], "paradox")
        output.append("🔄 悖论:")
        output.append(f"   \"{parsed['text'] or parsed['title']}\"")
        output.append("")

    if idea["arc"]:
        parsed = parse_entry(idea["arc"], "arc")
        output.append("📈 转化弧:")
        output.append(f"   {parsed['title']}")
        output.append("")

    if idea["phrases"]:
        output.append("✨ 金句:")
        for phrase in idea["phrases"]:
            parsed = parse_entry(phrase, "phrase")
            text = parsed["text"] or parsed["title"]
            if text:
                output.append(f"   • \"{text[:80]}...\"")
        output.append("")

    if idea["structure"]:
        parsed = parse_entry(idea["structure"], "structure")
        output.append("🏗️ 结构:")
        output.append(f"   {parsed['title']}")
        output.append("")

    if idea["perspective"]:
        parsed = parse_entry(idea["perspective"], "perspective")
        output.append("💡 观点:")
        output.append(f"   {parsed['text'] or parsed['title']}")
        output.append("")

    # 生成写作提示
    output.append("-" * 40)
    output.append("💭 写作提示:")
    if idea["hook"]:
        parsed = parse_entry(idea["hook"], "hook")
        hook_text = parsed["text"] or parsed["title"]
        output.append(f"   用「{hook_text[:30]}...」作为开头，")
    if idea["paradox"]:
        output.append(f"   引入认知冲突，")
    if idea["arc"]:
        parsed = parse_entry(idea["arc"], "arc")
        output.append(f"   沿着「{parsed['title']}」的转化弧展开，")
    output.append("   最后用金句收尾并给出行动号召。")

    return "\n".join(output)


def format_idea_as_json(idea: dict, index: int) -> dict:
    """格式化输出一个创意方向 (JSON)"""
    result = {"index": index}

    if idea["hook"]:
        result["hook"] = parse_entry(idea["hook"], "hook")
    if idea["paradox"]:
        result["paradox"] = parse_entry(idea["paradox"], "paradox")
    if idea["arc"]:
        result["arc"] = parse_entry(idea["arc"], "arc")
    if idea["phrases"]:
        result["phrases"] = [parse_entry(p, "phrase") for p in idea["phrases"]]
    if idea["structure"]:
        result["structure"] = parse_entry(idea["structure"], "structure")
    if idea["perspective"]:
        result["perspective"] = parse_entry(idea["perspective"], "perspective")

    return result


def main():
    parser = argparse.ArgumentParser(description="Dan Koe Idea Spark - 从积木库生成创意方向")
    parser.add_argument("--count", "-n", type=int, default=3, help="生成创意方向的数量 (默认: 3)")
    parser.add_argument("--topic", "-t", default="", help="指定话题关键词过滤 (如: 写作、自律)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--hook", action="store_true", help="只用钩子模式 (快速生成)")
    parser.add_argument("--arc", action="store_true", help="只用转化弧模式")
    parser.add_argument("--seed", type=int, default=0, help="随机种子 (用于复现)")

    args = parser.parse_args()

    global OUTPUT_JSON
    OUTPUT_JSON = args.json

    if args.seed:
        random.seed(args.seed)

    print(f"\n🔮 Dan Koe 写作系统 - 创意发生器")
    print(f"{'='*60}")

    if args.topic:
        print(f"话题过滤: {args.topic}")
        print(f"注意: 仅返回包含该关键词的积木组合")
        print()

    knowledge = load_knowledge()

    # 检查积木库是否为空
    total_blocks = sum(len(v) for v in knowledge.values())
    if total_blocks == 0:
        print("⚠️  积木库为空！")
        print("请先运行 goldmine.py 拆解内容来填充积木库")
        return

    print(f"📚 积木库状态: {total_blocks} 条积木已加载")
    print(f"   钩子: {len(knowledge.get('hooks', []))} 条")
    print(f"   悖论: {len(knowledge.get('paradoxes', []))} 条")
    print(f"   转化弧: {len(knowledge.get('arcs', []))} 条")
    print(f"   金句: {len(knowledge.get('golden_phrases', []))} 条")
    print(f"   结构: {len(knowledge.get('structures', []))} 条")
    print(f"   观点: {len(knowledge.get('perspectives', []))} 条")
    print()

    if args.hook:
        # 快速模式：只用钩子
        hooks = knowledge.get("hooks", [])
        if hooks:
            count = min(args.count, len(hooks))
            selected = random.sample(hooks, count)
            
            if args.json:
                result = [{"hook": parse_entry(h, "hook")} for h in selected]
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                for i, hook in enumerate(selected, 1):
                    parsed = parse_entry(hook, "hook")
                    print(f"\n🎣 钩子 #{i}:")
                    print(f"   {parsed['text'] or parsed['title']}")
                    if parsed.get("hook_type"):
                        print(f"   类型: {parsed['hook_type']}")
        else:
            print("⚠️  钩子库为空")
    
    elif args.arc:
        # 快速模式：只用转化弧
        arcs = knowledge.get("arcs", [])
        if arcs:
            count = min(args.count, len(arcs))
            selected = random.sample(arcs, count)
            
            if args.json:
                result = [{"arc": parse_entry(a, "arc")} for a in selected]
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                for i, arc in enumerate(selected, 1):
                    parsed = parse_entry(arc, "arc")
                    print(f"\n📈 转化弧 #{i}:")
                    print(f"   {parsed['title']}")
        else:
            print("⚠️  转化弧库为空")
    
    else:
        # 完整模式：随机组合所有积木类型
        ideas = []
        for i in range(args.count):
            idea = combine_into_idea(knowledge, args.topic)
            
            if args.json:
                ideas.append(format_idea_as_json(idea, i + 1))
            else:
                print(format_idea_as_markdown(idea, i + 1))
        
        if args.json:
            print(json.dumps(ideas, ensure_ascii=False, indent=2))

    print(f"\n{'='*60}")
    print("💡 提示:")
    print("   - 再次运行获取不同组合: python spark.py")
    print("   - 指定数量: python spark.py --count 5")
    print("   - 固定随机种子复现: python spark.py --seed 42")
    print("   - 话题过滤: python spark.py --topic 写作")
    print("   - 输出 JSON: python spark.py --json")
    print()


if __name__ == "__main__":
    main()
