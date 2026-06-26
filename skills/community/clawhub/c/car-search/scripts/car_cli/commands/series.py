import asyncio

import click
from rich.console import Console
from rich.table import Table

from car_cli.client.adapters import ADAPTER_REGISTRY
from car_cli.logging_config import get_logger

err_console = Console(stderr=True)
_log = get_logger("series")


def _render_series(platform: str, brand: str, series_list: list[dict[str, str]]):
    table = Table(title=f"[{platform}] {brand} — 可用车系", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("车系名称", style="cyan")
    table.add_column("系列 ID", style="dim")
    for i, s in enumerate(series_list, 1):
        table.add_row(str(i), s["series_name"], s["series_id"])
    err_console.print(table)


@click.command()
@click.argument("brand")
@click.option("--platform", default="dongchedi", help="平台：dongchedi,che168,guazi")
def series(brand, platform):
    """查询品牌下的车系列表。用法: car series 宝马"""
    cls = ADAPTER_REGISTRY.get(platform)
    if cls is None:
        err_console.print(f"[red]未知平台: {platform}[/red]")
        raise SystemExit(1)

    adapter = cls()
    series_list = asyncio.run(adapter.list_series(brand))
    if not series_list:
        err_console.print(f"[yellow]{platform} 暂不支持车系查询，或未找到 {brand} 的车系数据。[/yellow]")
        return

    _render_series(platform, brand, series_list)
    err_console.print(
        f"\n[dim]共 {len(series_list)} 个车系。"
        f"使用 --series 筛选，如: car search --brand {brand} --series {series_list[0]['series_name']}[/dim]"
    )
