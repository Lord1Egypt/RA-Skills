import asyncio
import json
from dataclasses import asdict

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from car_cli.client.adapters import ADAPTER_REGISTRY
from car_cli.logging_config import get_logger

err_console = Console(stderr=True)
_log = get_logger("detail")


def _parse_car_id(car_id: str) -> tuple[str, str]:
    """Parse 'platform:id' format, return (platform, id)."""
    if ":" not in car_id:
        raise click.UsageError(
            f"无效的车源 ID 格式: {car_id}。格式应为 platform:id（如 dongchedi:12345）"
        )
    platform, _, raw_id = car_id.partition(":")
    if platform not in ADAPTER_REGISTRY:
        raise click.UsageError(f"未知平台: {platform}")
    return platform, raw_id


def _render_detail(d):
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("字段", style="bold")
    table.add_column("值")
    table.add_row("标题", d.title)
    table.add_row("平台", d.platform)
    table.add_row("价格", f"{d.price:.2f}万" if d.price else "-")
    if d.brand:
        table.add_row("品牌", d.brand)
    if d.series:
        table.add_row("车系", d.series)
    if d.model_year:
        table.add_row("年款", d.model_year)
    table.add_row("里程", f"{d.mileage:.1f}万公里" if d.mileage else "-")
    if d.first_reg_date:
        table.add_row("首次上牌", d.first_reg_date)
    if d.transmission:
        table.add_row("变速箱", d.transmission)
    if d.displacement:
        table.add_row("排量", d.displacement)
    if d.fuel_type:
        table.add_row("燃料类型", d.fuel_type)
    if d.body_type:
        table.add_row("车身类型", d.body_type)
    if d.drive_type:
        table.add_row("驱动方式", d.drive_type)
    if d.emission_standard:
        table.add_row("排放标准", d.emission_standard)
    if d.color:
        table.add_row("颜色", d.color)
    if d.city:
        table.add_row("车源城市", d.city)
    if d.transfer_count:
        table.add_row("过户次数", d.transfer_count)
    if d.description:
        table.add_row("描述", d.description[:200])
    if d.url:
        table.add_row("链接", d.url)
    err_console.print(Panel(table, title=f"车源详情 [{d.platform}:{d.id}]"))


@click.command()
@click.argument("car_id")
@click.option(
    "--output", "output_format",
    type=click.Choice(["table", "json", "yaml"]), default="table",
)
def detail(car_id, output_format):
    """查看车源详情。CAR_ID 格式: platform:id（如 dongchedi:12345）"""
    platform, raw_id = _parse_car_id(car_id)
    _log.debug("detail platform=%s raw_id=%s output=%s", platform, raw_id, output_format)
    adapter = ADAPTER_REGISTRY[platform]()
    d = asyncio.run(adapter.detail(raw_id))
    _log.debug("detail fetched title=%r", d.title)

    if output_format == "json":
        click.echo(json.dumps(asdict(d), ensure_ascii=False, indent=2))
    elif output_format == "yaml":
        click.echo(yaml.dump(asdict(d), allow_unicode=True, default_flow_style=False))
    else:
        _render_detail(d)
