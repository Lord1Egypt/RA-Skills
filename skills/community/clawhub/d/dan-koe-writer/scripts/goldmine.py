#!/usr/bin/env python3
"""
Dan Koe 写作系统 - Content Goldmine (重构版)
拆解爆款内容，提取创意积木，输出 JSON 供 Agent 使用

用法:
    python goldmine.py "https://mp.weixin.qq.com/s/xxx"          # 从URL拆解
    python goldmine.py --text "你的文章内容..."                  # 从文本拆解
    python goldmine.py --file article.txt                        # 从文件拆解
    python goldmine.py --text "..." --output-json               # 输出JSON格式
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path

# ========== 配置 ==========
KNOWLEDGE_DIR = Path(__file__).parent.parent / "references" / "knowledge"
OUTPUT_JSON = False  # 默认输出 Markdown 格式

# ========== 积木模板 ==========

BUILDING_BLOCKS_TEMPLATE = """你是一个专业的写作分析师。请从以下内容中提取 Dan Koe 写作方法论中的「创意积木」。

原文内容:
---
{content}
---

请按以下格式提取，输出 JSON:

{{
  "hooks": [
    {{
      "title": "钩子标题（3-5字）",
      "text": "钩子原文或近似表达",
      "type": "大问题|巨大好处|重要思想|转换过程|时间范围|消极经历",
      "why_works": "为什么这个钩子有效（1-2句话）",
      "when_to_use": "适合什么样的内容话题"
    }}
  ],
  "paradoxes": [
    {{
      "title": "悖论标题",
      "text": "悖论的核心表达",
      "why_works": "为什么有效",
      "topics": ["相关话题1", "相关话题2"]
    }}
  ],
  "arcs": [
    {{
      "title": "转化弧标题",
      "before": "起点/问题状态",
      "turning_point": "转折点/顿悟",
      "after": "终点/解决状态",
      "topics": ["话题1", "话题2"]
    }}
  ],
  "core_problems": [
    {{
      "title": "问题名称",
      "text": "问题的核心描述",
      "why_resonates": "为什么会引发共鸣（1-2句话）",
      "trigger_words": ["激活词1", "激活词2"]
    }}
  ],
  "golden_phrases": [
    {{
      "text": "金句原文",
      "why_powerful": "为什么有力（1-2句话）",
      "topics": ["话题1", "话题2"]
    }}
  ],
  "structures": [
    {{
      "title": "结构名称",
      "description": "结构描述",
      "when_to_use": "什么时候用",
      "example_hook": "示例钩子（如果有）"
    }}
  ],
  "perspectives": [
    {{
      "title": "观点标题",
      "core_point": "核心观点（一句话）",
      "origin": "观点的来源或背景",
      "why_unique": "为什么独特/不同",
      "topics": ["适用话题1", "适用话题2"]
    }}
  ]
}}

重要：只输出 JSON，不要有任何其他文字。"""


def get_llm_extraction_prompt(content: str) -> str:
    """获取用于 LLM 提取的 prompt"""
    return BUILDING_BLOCKS_TEMPLATE.format(content=content)


def format_blocks_as_markdown(blocks: dict, source_url: str = "", date: str = "") -> str:
    """将提取的积木格式化为 Markdown"""
    lines = []
    date_str = date or datetime.now().strftime("%Y-%m-%d")
    source_short = source_url[:50] if source_url else "直接输入"

    mapping = [
        ("hooks", "钩子 (Hooks)", "type"),
        ("paradoxes", "悖论 (Paradoxes)", None),
        ("arcs", "转化弧 (Arcs)", None),
        ("core_problems", "核心问题 (Core Problems)", None),
        ("golden_phrases", "金句 (Golden Phrases)", None),
        ("structures", "结构 (Structures)", None),
        ("perspectives", "观点 (Perspectives)", None),
    ]

    for block_key, type_name, extra_field in mapping:
        items = blocks.get(block_key, [])
        if not items:
            continue
        
        lines.append(f"## {type_name}\n")
        
        for item in items:
            if block_key == "hooks":
                lines.append(f"### {item.get('title', '未命名钩子')} (来源: {source_short}, 日期: {date_str})")
                lines.append(f"\n**类型:** {item.get('type', '未知')}\n")
                lines.append(f"**原文片段:**\n> {item.get('text', '')}\n")
                lines.append(f"**为什么有效:** {item.get('why_works', '')}\n")
                lines.append(f"**适用场景:** {item.get('when_to_use', '')}\n")
            
            elif block_key == "paradoxes":
                lines.append(f"### {item.get('title', '未命名悖论')} (来源: {source_short}, 日期: {date_str})")
                lines.append(f"\n**悖论原文:**\n> \"{item.get('text', '')}\"\n")
                lines.append(f"**为什么有效:** {item.get('why_works', '')}\n")
                lines.append(f"**适用话题:** {', '.join(item.get('topics', []))}\n")
            
            elif block_key == "arcs":
                lines.append(f"### {item.get('title', '未命名转化弧')} (来源: {source_short}, 日期: {date_str})")
                lines.append(f"\n**起点 (Before):** {item.get('before', '')}\n")
                lines.append(f"**转折点:** {item.get('turning_point', '')}\n")
                lines.append(f"**终点 (After):** {item.get('after', '')}\n")
                lines.append(f"**典型话题:** {', '.join(item.get('topics', []))}\n")
            
            elif block_key == "core_problems":
                lines.append(f"### {item.get('title', '未命名问题')} (来源: {source_short}, 日期: {date_str})")
                lines.append(f"\n**问题原文:** {item.get('text', '')}\n")
                lines.append(f"**为什么引发共鸣:** {item.get('why_resonates', '')}\n")
                lines.append(f"**激活词/触发语:** {', '.join(item.get('trigger_words', []))}\n")
            
            elif block_key == "golden_phrases":
                lines.append(f"## (来源: {source_short}, 日期: {date_str})")
                lines.append(f"\n> \"{item.get('text', '')}\"\n")
                lines.append(f"**为什么有力:** {item.get('why_powerful', '')}\n")
                lines.append(f"**适用场景:** {', '.join(item.get('topics', []))}\n")
            
            elif block_key == "structures":
                lines.append(f"### {item.get('title', '未命名结构')} (来源: {source_short}, 日期: {date_str})")
                lines.append(f"\n**结构描述:** {item.get('description', '')}\n")
                lines.append(f"**什么时候用:** {item.get('when_to_use', '')}\n")
                if item.get('example_hook'):
                    lines.append(f"**示例钩子:** {item.get('example_hook')}\n")
            
            elif block_key == "perspectives":
                lines.append(f"### {item.get('title', '未命名观点')} (来源: {source_short}, 日期: {date_str})")
                lines.append(f"\n**核心观点:** {item.get('core_point', '')}\n")
                lines.append(f"**背景/来源:** {item.get('origin', '')}\n")
                lines.append(f"**为什么独特:** {item.get('why_unique', '')}\n")
                lines.append(f"**适用话题:** {', '.join(item.get('topics', []))}\n")
            
            lines.append("---\n")

    return "\n".join(lines)


def append_to_file(filepath: Path, content: str):
    """追加内容到文件，如果文件不存在则创建"""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content)


def fetch_content_from_url(url: str) -> tuple:
    """从 URL 获取内容"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            content = page.evaluate("document.getElementById('js_content')?.innerText || ''")
            title = page.title()
            browser.close()
            if not content:
                return None, None
            return content, title
    except ImportError:
        print("错误: 需要安装 playwright (pip install playwright && playwright install chromium)")
        return None, None
    except Exception as e:
        print(f"抓取失败: {e}")
        return None, None


def main():
    parser = argparse.ArgumentParser(description="Dan Koe Content Goldmine - 拆解爆款内容，提取创意积木")
    parser.add_argument("url", nargs="?", help="要拆解的内容URL")
    parser.add_argument("--text", "-t", help="直接输入要拆解的文本")
    parser.add_argument("--file", "-f", help="从文件读取内容")
    parser.add_argument("--source", "-s", default="", help="内容来源名称/标题")
    parser.add_argument("--output-json", action="store_true", help="输出 JSON 格式（供 Agent 调用 LLM）")
    parser.add_argument("--output-prompt", action="store_true", help="只输出 LLM 提取 prompt")
    parser.add_argument("--date", "-d", default="", help="内容日期 (YYYY-MM-DD)")
    parser.add_argument("--no-save", action="store_true", help="只输出，不保存到知识库")

    args = parser.parse_args()

    global OUTPUT_JSON
    OUTPUT_JSON = args.output_json

    # 获取内容
    source_name = args.source
    content = None

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
        source_name = source_name or Path(args.file).stem
    elif args.text:
        content = args.text
        source_name = source_name or "直接输入"
    elif args.url:
        content, title = fetch_content_from_url(args.url)
        if not content:
            sys.exit(1)
        source_name = source_name or title
        print(f"成功抓取: {title}")
    else:
        print("错误: 请提供 URL、--text 或 --file 参数")
        parser.print_help()
        sys.exit(1)

    # 截断过长内容
    if len(content) > 10000:
        content = content[:10000]
        print("注意: 内容已截断至 10000 字符")

    print(f"\n📝 内容来源: {source_name}")
    print(f"📏 内容长度: {len(content)} 字符")

    # 只输出 prompt 模式（供 Agent 调用自己的 LLM）
    if args.output_prompt:
        prompt = get_llm_extraction_prompt(content)
        print("\n" + "=" * 60)
        print("📋 LLM 提取 Prompt（复制给 AI 调用）:")
        print("=" * 60)
        print(prompt)
        return

    # 输出 JSON 模式（供 Agent 解析）
    if args.output_json:
        prompt = get_llm_extraction_prompt(content)
        print("\n" + "=" * 60)
        print("📋 LLM 提取 Prompt:")
        print("=" * 60)
        print(prompt)
        print("\n" + "=" * 60)
        print("💡 请将 LLM 输出（JSON 格式）保存为 blocks.json")
        print("   然后用以下命令保存到知识库:")
        print("   python goldmine.py --load-json blocks.json")
        print("=" * 60)
        return

    # 交互模式
    print("\n" + "=" * 60)
    print("🎯 下一步操作:")
    print("=" * 60)
    print("1. 使用 --output-json 获取 LLM prompt")
    print("2. 让 AI Agent 调用自己的模型提取积木")
    print("3. 将提取结果保存为 JSON")
    print("4. 使用 --load-json 保存到知识库")
    print()
    print("示例流程:")
    print("  python goldmine.py --text \"...\" --output-json")
    print("  # -> 把 prompt 给 AI Agent")
    print("  # -> AI Agent 返回 JSON")
    print("  python goldmine.py --load-json result.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
