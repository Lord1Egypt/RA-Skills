import asyncio
import json
from dataclasses import asdict

import click
import yaml
from rich.console import Console
from rich.table import Table

from car_cli.client.adapters import ADAPTER_REGISTRY
from car_cli.logging_config import get_logger

err_console = Console(stderr=True)
_log = get_logger("compare")


def _parse_car_id(car_id: str) -> tuple[str, str]:
    if ":" not in car_id:
        raise click.UsageError(
            f"无效的车源 ID 格式: {car_id}。格式应为 platform:id"
        )
    platform, _, raw_id = car_id.partition(":")
    if platform not in ADAPTER_REGISTRY:
        raise click.UsageError(f"未知平台: {platform}")
    return platform, raw_id


async def _fetch_both(p1, id1, p2, id2):
    a1 = ADAPTER_REGISTRY[p1]()
    a2 = ADAPTER_REGISTRY[p2]()
    d1, d2 = await asyncio.gather(a1.detail(id1), a2.detail(id2))
    return d1, d2


def _render_compare(d1, d2):
    table = Table(title="车源对比", show_lines=True)
    table.add_column("字段", style="bold")
    table.add_column(f"{d1.platform}:{d1.id}", max_width=30)
    table.add_column(f"{d2.platform}:{d2.id}", max_width=30)

    rows = [
        ("标题", d1.title, d2.title),
        ("价格", f"{d1.price:.2f}万" if d1.price else "-", f"{d2.price:.2f}万" if d2.price else "-"),
        ("品牌", d1.brand or "-", d2.brand or "-"),
        ("车系", d1.series or "-", d2.series or "-"),
        ("年款", d1.model_year or "-", d2.model_year or "-"),
        ("里程", f"{d1.mileage:.1f}万km" if d1.mileage else "-", f"{d2.mileage:.1f}万km" if d2.mileage else "-"),
        ("首次上牌", d1.first_reg_date or "-", d2.first_reg_date or "-"),
        ("变速箱", d1.transmission or "-", d2.transmission or "-"),
        ("排量", d1.displacement or "-", d2.displacement or "-"),
        ("排放标准", d1.emission_standard or "-", d2.emission_standard or "-"),
        ("燃料类型", d1.fuel_type or "-", d2.fuel_type or "-"),
        ("城市", d1.city or "-", d2.city or "-"),
    ]
    for label, v1, v2 in rows:
        table.add_row(label, str(v1), str(v2))
    err_console.print(table)


@click.command()
@click.argument("id1")
@click.argument("id2")
@click.option(
    "--output", "output_format",
    type=click.Choice(["table", "json", "yaml"]), default="table",
)
def compare(id1, id2, output_format):
    """并排对比两辆车。ID 格式: platform:id"""
    p1, rid1 = _parse_car_id(id1)
    p2, rid2 = _parse_car_id(id2)
    _log.debug("compare %s:%s vs %s:%s", p1, rid1, p2, rid2)

    d1, d2 = asyncio.run(_fetch_both(p1, rid1, p2, rid2))
    _log.debug("compare done titles=%r / %r", d1.title, d2.title)

    if output_format == "json":
        click.echo(json.dumps([asdict(d1), asdict(d2)], ensure_ascii=False, indent=2))
    elif output_format == "yaml":
        click.echo(yaml.dump(
            [asdict(d1), asdict(d2)], allow_unicode=True, default_flow_style=False,
        ))
    else:
        _render_compare(d1, d2)
