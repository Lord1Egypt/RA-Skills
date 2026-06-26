#!/usr/bin/env python3
"""
章节大纲生成器 (LLM 版本) - 为待写章节生成详细的 15 节拍写作大纲

功能：
- 读取故事大纲 (outline.md)
- 读取风格配置 (style.yml)
- 读取角色档案 (characters/*.yml)
- 读取章节列表 (chapters/index.yml)
- LLM 为指定章节生成详细的 15 节拍写作大纲
- 输出 Markdown 格式大纲（给 novel-writer 用）

Usage:
    python3 generate_outline_llm.py --book-dir projects/my-novel --chapter 1 --output outlines/chapter-01-outline.md
    python3 generate_outline_llm.py --book-dir projects/my-novel --chapter 1 --model qwen3.6-plus
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

# 默认模型
DEFAULT_MODEL = "qwen3.6-plus"

# 15 节拍模板
BEAT_TEMPLATES = [
    {"id": 1, "name": "钩子", "phase": "开场", "purpose": "吸引读者注意力"},
    {"id": 2, "name": "设定", "phase": "开场", "purpose": "建立场景背景"},
    {"id": 3, "name": "背景", "phase": "开场", "purpose": "提供必要上下文"},
    {"id": 4, "name": "触发事件", "phase": "发展", "purpose": "引入冲突"},
    {"id": 5, "name": "发展", "phase": "发展", "purpose": "情节推进"},
    {"id": 6, "name": "转折", "phase": "发展", "purpose": "方向变化"},
    {"id": 7, "name": "复杂化", "phase": "发展", "purpose": "新障碍出现"},
    {"id": 8, "name": "对抗", "phase": "高潮", "purpose": "矛盾激化"},
    {"id": 9, "name": "发展", "phase": "高潮", "purpose": "高潮铺垫"},
    {"id": 10, "name": "高潮", "phase": "高潮", "purpose": "冲突顶点"},
    {"id": 11, "name": "转折", "phase": "高潮", "purpose": "高潮转折"},
    {"id": 12, "name": "解决", "phase": "结局", "purpose": "问题解决"},
    {"id": 13, "name": "收尾", "phase": "结局", "purpose": "情节收尾"},
    {"id": 14, "name": "余韵", "phase": "结局", "purpose": "情感延续"},
    {"id": 15, "name": "结局", "phase": "结局", "purpose": "章节结束"},
]


def load_book_data(book_dir: str) -> dict[str, Any]:
    """加载项目数据"""
    book_path = Path(book_dir)
    data = {}

    # 加载故事大纲
    outline_path = book_path / "outline.md"
    if outline_path.exists():
        data["outline"] = outline_path.read_text(encoding="utf-8")
    else:
        console.print("[yellow]⚠️ outline.md 不存在[/yellow]")
        data["outline"] = ""

    # 加载风格配置
    style_path = book_path / "style.yml"
    if style_path.exists():
        with open(style_path, "r", encoding="utf-8") as f:
            data["style"] = yaml.safe_load(f) or {}
    else:
        console.print("[yellow]⚠️ style.yml 不存在[/yellow]")
        data["style"] = {}

    # 加载角色档案
    chars_path = book_path / "characters"
    characters = []
    if chars_path.exists():
        for yml_file in sorted(chars_path.glob("*.yml")):
            with open(yml_file, "r", encoding="utf-8") as f:
                char_data = yaml.safe_load(f)
                if char_data:
                    characters.append(char_data)
    data["characters"] = characters

    # 加载章节列表
    index_path = book_path / "chapters" / "index.yml"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            data["chapter_index"] = yaml.safe_load(f) or {}
    else:
        console.print("[yellow]⚠️ chapters/index.yml 不存在[/yellow]")
        data["chapter_index"] = {}

    return data


def generate_outline(
    chapter_num: int,
    book_data: dict[str, Any],
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """通过 LLM 生成章节写作大纲"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        console.print("[red]❌ 环境变量 DASHSCOPE_API_KEY 未设置[/red]")
        sys.exit(1)

    prompt = _build_prompt(chapter_num, book_data)

    url = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一名专业的小说编辑和大纲策划师，擅长为待写章节生成详细的 15 节拍写作大纲。必须输出标准 JSON 格式。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]正在调用 LLM 生成章节大纲...[/bold cyan]"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("generating", total=None)
        response = requests.post(url, headers=headers, json=payload, timeout=120)

    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def _build_prompt(chapter_num: int, book_data: dict[str, Any]) -> str:
    """构建给 LLM 的提示词"""
    beat_list = "\n".join(
        f"{i}. {b['name']}（{b['phase']}）：{b['purpose']}"
        for i, b in enumerate(BEAT_TEMPLATES, 1)
    )

    style_info = json.dumps(book_data.get("style", {}), ensure_ascii=False, indent=2)
    char_info = json.dumps(book_data.get("characters", [])[:5], ensure_ascii=False, indent=2)
    outline_preview = book_data.get("outline", "")[:1000]

    chapter_index = book_data.get("chapter_index", {})
    chapter_info = ""
    if isinstance(chapter_index, dict):
        chapters = chapter_index.get("chapters", [])
        if isinstance(chapters, list) and chapter_num <= len(chapters):
            chapter_info = json.dumps(chapters[chapter_num - 1], ensure_ascii=False, indent=2)

    return f"""请为以下小说的**第 {chapter_num} 章**生成详细的 15 节拍写作大纲。

## 故事大纲
{outline_preview if outline_preview else "无"}

## 章节信息
{chapter_info if chapter_info else "无"}

## 风格配置
{style_info}

## 角色档案
{char_info if char_info else "无"}

## 15 节拍定义
{beat_list}

## 输出要求
请输出 JSON 格式，包含以下字段：
- "chapter_num": 章节号
- "story_position": 本章在故事中的位置（开场/发展/中段/高潮前/高潮/结局）
- "position_reason": 位置判断理由
- "target_words": 目标字数
- "key_characters": 本章涉及的主要角色列表
- "key_events": 本章关键事件列表
- "beats": 15 个节拍的详细写作指导数组，每个节拍包含：
  - "beat_id": 节拍编号（1-15）
  - "beat_name": 节拍名称
  - "has_content": 本章是否包含该节拍内容（true/false）
  - "writing_guide": 该节拍的具体写作指导（写什么、怎么写、注意事项）
  - "word_allocation": 该节拍的目标字数
  - "character_focus": 该节拍聚焦的角色
  - "key_dialogue_hint": 关键对话提示（如果有）
  - "scene_setting": 场景设置（如果有）
"""


def generate_markdown(outline_data: dict[str, Any]) -> str:
    """生成 Markdown 格式大纲"""
    lines = []

    # 标题
    chapter_num = outline_data.get("chapter_num", "?")
    lines.append(f"# 第 {chapter_num} 章 写作大纲")
    lines.append("")

    # 基本信息
    lines.append(f"**故事位置**: {outline_data.get('story_position', '未知')}")
    lines.append(f"**位置判断**: {outline_data.get('position_reason', 'N/A')}")
    lines.append(f"**目标字数**: {outline_data.get('target_words', 'N/A')}")

    # 角色和事件
    key_chars = outline_data.get("key_characters", [])
    if key_chars:
        lines.append(f"\n**涉及角色**: {', '.join(key_chars)}")

    key_events = outline_data.get("key_events", [])
    if key_events:
        lines.append("\n**关键事件**:")
        for event in key_events:
            lines.append(f"- {event}")

    # 15 节拍
    lines.append("\n## 15 节拍写作指导")

    beats = outline_data.get("beats", [])
    for beat in beats:
        if beat.get("has_content"):
            lines.append(f"\n### {beat['beat_id']}. {beat['beat_name']}")
            lines.append(f"\n**写作指导**: {beat.get('writing_guide', '')}")
            lines.append(f"\n**字数分配**: {beat.get('word_allocation', 'N/A')} 字")

            if beat.get("character_focus"):
                lines.append(f"\n**聚焦角色**: {beat['character_focus']}")
            if beat.get("key_dialogue_hint"):
                lines.append(f"\n**关键对话**: {beat['key_dialogue_hint']}")
            if beat.get("scene_setting"):
                lines.append(f"\n**场景设置**: {beat['scene_setting']}")

    return "\n".join(lines)


def print_result(outline_data: dict[str, Any]) -> None:
    """美化输出结果"""
    console.print("\n")
    console.print(
        Panel.fit(
            f"[bold cyan]第 {outline_data.get('chapter_num', '?')} 章大纲生成完成！[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    table = Table(title="章节大纲概览", show_header=True, header_style="bold magenta")
    table.add_column("项目", style="cyan")
    table.add_column("内容", style="green", overflow="fold")

    table.add_row("故事位置", outline_data.get("story_position", "N/A"))
    table.add_row("目标字数", str(outline_data.get("target_words", "N/A")))

    key_chars = outline_data.get("key_characters", [])
    table.add_row("涉及角色", ", ".join(key_chars) if key_chars else "N/A")

    key_events = outline_data.get("key_events", [])
    table.add_row("关键事件", "\n".join(f"• {e}" for e in key_events[:3]) if key_events else "N/A")

    # 节拍统计
    beats = outline_data.get("beats", [])
    has_content_count = sum(1 for b in beats if b.get("has_content"))
    table.add_row("节拍覆盖", f"{has_content_count}/15 个节拍有内容")

    console.print(table)


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="章节大纲生成器 (LLM 版本) - 为待写章节生成详细的 15 节拍写作大纲"
    )
    parser.add_argument(
        "--book-dir",
        required=True,
        help="小说项目目录路径",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        required=True,
        help="章节号",
    )
    parser.add_argument(
        "--output",
        help="输出大纲文件路径（Markdown 格式）",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"使用的模型（默认：{DEFAULT_MODEL}）",
    )
    args = parser.parse_args()

    console.print("[bold]📝 章节大纲生成器 (LLM 版本)[/bold]")
    console.print(f"项目目录：[yellow]{args.book_dir}[/yellow]")
    console.print(f"章节号：[yellow]{args.chapter}[/yellow]")
    console.print(f"使用模型：[yellow]{args.model}[/yellow]")

    # 加载项目数据
    book_data = load_book_data(args.book_dir)

    # 生成大纲
    outline_data = generate_outline(args.chapter, book_data, args.model)

    # 输出
    print_result(outline_data)

    if args.output:
        markdown = generate_markdown(outline_data)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        console.print(f"\n[green]✓ 大纲已保存至：{args.output}[/green]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
