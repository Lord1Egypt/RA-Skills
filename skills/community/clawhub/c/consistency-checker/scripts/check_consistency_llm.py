#!/usr/bin/env python3
"""
小说一致性检查器 (LLM 版本) - 通过 LLM 进行深层一致性推理

功能：
- 检测时间线矛盾
- 检测季节/天气矛盾
- 检测角色年龄/状态矛盾
- 输出结构化一致性报告

Usage:
    python3 check_consistency_llm.py --book-dir projects/my-novel --output report.json
    python3 check_consistency_llm.py --book-dir projects/my-novel --model qwen3-max-2026-01-23
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
DEFAULT_MODEL = "qwen3-max-2026-01-23"


def load_chapters(books_dir: str) -> list[dict[str, Any]]:
    """加载所有章节文件"""
    chapters = []
    chapters_path = Path(books_dir) / "chapters"
    if not chapters_path.exists():
        console.print(f"[yellow]⚠️ 章节目录不存在：{chapters_path}[/yellow]")
        return chapters
    
    for md_file in sorted(chapters_path.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        chapters.append({
            "name": md_file.stem,
            "content": content[:2000],  # 限制长度
            "length": len(content),
        })
    
    if not chapters:
        console.print(f"[yellow]⚠️ 没有找到章节文件：{chapters_path}/*.md[/yellow]")
    
    return chapters


def load_characters(books_dir: str) -> list[dict[str, Any]]:
    """加载角色档案"""
    characters = []
    chars_path = Path(books_dir) / "characters"
    if not chars_path.exists():
        return characters
    
    for yml_file in sorted(chars_path.glob("*.yml")):
        with open(yml_file, "r", encoding="utf-8") as f:
            char_data = yaml.safe_load(f)
            if char_data:
                characters.append(char_data)
    
    return characters


def check_consistency(
    chapters: list[dict[str, Any]],
    characters: list[dict[str, Any]],
    model: str = DEFAULT_MODEL,
) -> list[dict[str, Any]]:
    """通过 LLM 检测一致性问题"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        console.print("[red]❌ 环境变量 DASHSCOPE_API_KEY 未设置[/red]")
        sys.exit(1)

    # 构建角色信息摘要
    char_summary = ""
    if characters:
        char_lines = []
        for char in characters[:5]:  # 最多 5 个角色
            name = char.get("name", "未知")
            age = char.get("age", "")
            traits = char.get("traits", [])
            char_lines.append(f"- {name}: 年龄={age}, 特征={', '.join(traits[:3])}")
        char_summary = "\n".join(char_lines)
    
    # 构建章节信息摘要
    chapter_summary = ""
    for i, ch in enumerate(chapters[:10], 1):  # 最多 10 章
        chapter_summary += f"\n### 第 {i} 章：{ch['name']}\n{ch['content'][:300]}..."

    prompt = f"""你是一名小说编辑，擅长检测文本中的一致性问题。

## 角色档案
{char_summary if char_summary else "无角色档案"}

## 章节内容
{chapter_summary if chapter_summary else "无章节内容"}

## 检测任务
请检测以下一致性问题：
1. **时间线矛盾**：如"第二天"但情节不连贯、时间跳跃不合理
2. **季节/天气矛盾**：如前一章"大雪纷飞"后一章"春暖花开"但时间只过了一天
3. **角色状态矛盾**：如角色年龄突变、已死亡角色又出现、特征前后不一致
4. **地点矛盾**：如角色在同一时间出现在两个不同地点

## 输出要求
请输出 JSON 数组格式，每个元素包含：
- "type": 问题类型（timeline/season/character/location）
- "chapter": 问题所在章节
- "description": 问题描述
- "severity": 严重程度（high/medium/low）

如果没有发现问题，输出空数组 []。
"""

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
                "content": "你是一名专业的小说编辑，擅长检测文本中的一致性问题。必须输出标准 JSON 格式。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]正在调用 LLM 检测一致性...[/bold cyan]"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("checking", total=None)
        response = requests.post(url, headers=headers, json=payload, timeout=90)

    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def print_report(issues: list[dict[str, Any]]) -> None:
    """打印一致性报告"""
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]一致性检查完成！[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    if not issues:
        console.print("[green]✓ 未发现一致性问题[/green]")
        return

    severity_colors = {
        "high": "red",
        "medium": "yellow",
        "low": "green",
    }

    table = Table(title="一致性问题列表", show_header=True, header_style="bold magenta")
    table.add_column("序号", style="dim", width=6)
    table.add_column("类型", width=12)
    table.add_column("严重程度", width=10)
    table.add_column("章节", width=15)
    table.add_column("问题描述", overflow="fold")

    for i, issue in enumerate(issues, 1):
        severity = issue.get("severity", "medium")
        color = severity_colors.get(severity, "white")
        table.add_row(
            str(i),
            issue.get("type", "unknown"),
            f"[{color}]{severity}[/{color}]",
            issue.get("chapter", "N/A"),
            issue.get("description", "")[:80],
        )

    console.print(table)
    console.print(f"\n[red]总计发现 {len(issues)} 个一致性问题[/red]")


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="小说一致性检查器 (LLM 版本) - 通过 LLM 进行深层一致性推理"
    )
    parser.add_argument(
        "--book-dir",
        required=True,
        help="小说项目目录路径",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"使用的模型（默认：{DEFAULT_MODEL}）",
    )
    parser.add_argument(
        "--output",
        help="输出报告文件路径（JSON 格式）",
    )
    args = parser.parse_args()

    console.print("[bold]🔍 一致性检查器 (LLM 版本)[/bold]")
    console.print(f"项目目录：[yellow]{args.book_dir}[/yellow]")
    console.print(f"使用模型：[yellow]{args.model}[/yellow]")

    # 加载数据
    chapters = load_chapters(args.book_dir)
    characters = load_characters(args.book_dir)

    if not chapters:
        console.print("[red]❌ 没有找到章节文件，无法进行检查[/red]")
        return 1

    console.print(f"加载 {len(chapters)} 章，{len(characters)} 个角色")

    # 检测一致性
    issues = check_consistency(chapters, characters, args.model)

    # 输出报告
    print_report(issues)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
        console.print(f"\n[green]✓ 报告已保存至：{args.output}[/green]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
