#!/usr/bin/env python3
"""使用 LLM 识别文本中的伏笔/暗示/铺垫。"""

import argparse
import json
import os
import sys
from typing import Any

import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


def parse_args() -> argparse.Namespace:
    """解析 CLI 参数。"""
    parser = argparse.ArgumentParser(
        description="使用 LLM 识别文本中的伏笔/暗示/铺垫"
    )
    parser.add_argument("--input", required=True, help="输入文本文件路径")
    parser.add_argument("--chapter", type=int, help="章节号（可选）")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    parser.add_argument(
        "--model",
        default="qwen3-max-2026-01-23",
        help="DashScope 模型名称（默认: qwen3-max-2026-01-23）",
    )
    return parser.parse_args()


def load_api_key() -> str:
    """从环境变量加载 API Key。"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        console.print("[red]错误: 未设置 DASHSCOPE_API_KEY 环境变量[/red]")
        sys.exit(1)
    return api_key


def read_text_file(file_path: str) -> str:
    """读取文本文件内容。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        console.print(f"[red]错误: 文件不存在 {file_path}[/red]")
        sys.exit(1)
    except PermissionError:
        console.print(f"[red]错误: 无权限读取文件 {file_path}[/red]")
        sys.exit(1)
    except UnicodeDecodeError:
        console.print(f"[red]错误: 文件编码不是 UTF-8 {file_path}[/red]")
        sys.exit(1)


def extract_foreshadowing(
    text: str, model: str, api_key: str, chapter: int | None = None
) -> list[dict[str, Any]]:
    """通过 DashScope API 调用 LLM 识别伏笔。"""
    url = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
    
    chapter_info = f"第 {chapter} 章\n" if chapter else ""
    prompt = (
        f"请分析以下小说文本，识别其中的伏笔/暗示/铺垫。"
        f"{chapter_info}"
        f"输出格式为 JSON 数组，每个元素包含: text（原文）, type（环境/物品/对话/心理/其他）, "
        f"confidence（0.0-1.0 置信度）, explanation（为什么这是伏笔）。\n\n"
        f"文本:\n{text}"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一个小说分析专家，擅长识别文本中的伏笔、暗示和铺垫。必须输出标准 JSON 格式。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return json.loads(content)
    except requests.exceptions.RequestException as e:
        console.print(f"[red]API 请求失败: {e}[/red]")
        sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]JSON 解析失败: {e}[/red]")
        console.print(f"[yellow]原始响应: {content}[/yellow]")
        sys.exit(1)


def save_json(data: list[dict[str, Any]], output_path: str) -> None:
    """保存 JSON 到文件。"""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except PermissionError:
        console.print(f"[red]错误: 无权限写入文件 {output_path}[/red]")
        sys.exit(1)


def print_results(results: list[dict[str, Any]], chapter: int | None = None) -> None:
    """使用 rich 打印结果摘要。"""
    console.print("\n" + "=" * 60)
    title = "伏笔追踪结果 - " + (f"第 {chapter} 章" if chapter else "全文")
    console.print(f"[bold cyan]{title}[/bold cyan]")
    console.print("=" * 60)

    if not results:
        console.print("[yellow]未识别到伏笔[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("序号", style="dim", width=6)
    table.add_column("类型", width=12)
    table.add_column("置信度", width=10)
    table.add_column("伏笔原文", overflow="fold")
    table.add_column("解释", overflow="fold")

    for i, item in enumerate(results, 1):
        table.add_row(
            str(i),
            item.get("type", "其他"),
            f"{item.get('confidence', 0):.2f}",
            item.get("text", "")[:50],
            item.get("explanation", "")[:50],
        )

    console.print(table)
    console.print(f"\n[green]总计识别 {len(results)} 处伏笔[/green]")


def main() -> None:
    """主函数。"""
    args = parse_args()

    console.print("[bold]📖 伏笔追踪 - LLM 版[/bold]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("读取文本文件...", total=None)
        text = read_text_file(args.input)

        progress.add_task("调用 LLM 分析...", total=None)
        api_key = load_api_key()
        results = extract_foreshadowing(
            text, args.model, api_key, args.chapter
        )

    save_json(results, args.output)
    print_results(results, args.chapter)


if __name__ == "__main__":
    main()
