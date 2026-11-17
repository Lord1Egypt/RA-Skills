"""统一输出模块 — 人类友好的 Rich 格式 + AI 友好的 JSON 格式。"""

from __future__ import annotations

import json
import sys

from rich.console import Console

console = Console()
err_console = Console(stderr=True)


def output(data, json_mode: bool) -> None:
    """输出数据到 stdout。

    json_mode=True → 纯 JSON（供 AI 工具解析）
    json_mode=False → Rich 格式化（供人类阅读）
    """
    if json_mode:
        print(json.dumps(data, indent=2, default=str))
        return

    if isinstance(data, str):
        console.print(data)
    elif isinstance(data, dict):
        if not data:
            return
        max_key = max(len(str(k)) for k in data)
        for k, v in data.items():
            console.print(f"  [bold]{str(k).ljust(max_key)}[/bold]  {v}")
    elif isinstance(data, list):
        if not data:
            console.print("[dim](无)[/dim]")
            return
        if isinstance(data[0], dict):
            _print_table(data)
        else:
            for item in data:
                console.print(f"  {item}")
    else:
        console.print(str(data))


def error(msg: str) -> None:
    """输出错误信息到 stderr。"""
    err_console.print(f"[bold red]错误:[/bold red] {msg}")


def success(msg: str) -> None:
    """输出成功信息。"""
    console.print(f"[green]✅[/green] {msg}")


def status(msg: str) -> None:
    """输出状态提示。"""
    console.print(f"[dim]{msg}[/dim]")


def _print_table(rows: list[dict]) -> None:
    """将 dict 列表渲染为 Rich 表格。"""
    from rich.table import Table

    if not rows:
        return

    keys = list(rows[0].keys())
    table = Table(show_header=True, header_style="bold")
    for k in keys:
        table.add_column(k.upper())
    for row in rows:
        table.add_row(*[str(row.get(k, "")) for k in keys])
    console.print(table)
