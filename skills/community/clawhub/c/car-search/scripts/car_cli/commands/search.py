import asyncio
import json
import logging
from dataclasses import asdict

import click
import yaml
from rich.console import Console
from rich.table import Table

from car_cli.client.adapters import get_adapters
from car_cli.logging_config import get_logger
from car_cli.models.filter import SearchFilter

err_console = Console(stderr=True)
_log = get_logger("search")


async def _search_all(adapters, filters: SearchFilter):
    results = []
    tasks = [adapter.search(filters) for adapter in adapters]
    outcomes = await asyncio.gather(*tasks, return_exceptions=True)
    for adapter, outcome in zip(adapters, outcomes):
        if isinstance(outcome, Exception):
            err_console.print(
                f"[yellow]⚠ {adapter.platform_name}: {outcome}[/yellow]"
            )
            if _log.isEnabledFor(logging.DEBUG):
                _log.error(
                    "adapter %s failed",
                    adapter.platform_name,
                    exc_info=outcome,
                )
        else:
            results.extend(outcome)
    return results


def _sort_results(cars, sort_by: str):
    if sort_by == "price_asc":
        return sorted(cars, key=lambda c: c.price)
    elif sort_by == "price_desc":
        return sorted(cars, key=lambda c: c.price, reverse=True)
    elif sort_by == "mileage":
        return sorted(cars, key=lambda c: c.mileage)
    elif sort_by == "date":
        return sorted(cars, key=lambda c: c.first_reg_date, reverse=True)
    return cars


def _render_table(cars):
    table = Table(title="搜索结果", show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("ID", style="cyan", max_width=24)
    table.add_column("标题", max_width=35)
    table.add_column("价格(万)", justify="right")
    table.add_column("里程(万km)", justify="right")
    table.add_column("年款")
    table.add_column("变速箱")
    table.add_column("城市")
    for i, c in enumerate(cars, 1):
        table.add_row(
            str(i),
            f"{c.platform}:{c.id}",
            c.title,
            f"{c.price:.2f}" if c.price else "-",
            f"{c.mileage:.1f}" if c.mileage else "-",
            c.model_year or "-",
            c.transmission or "-",
            c.city or "-",
        )
    err_console.print(table)


@click.command()
@click.option("--city", default="全国", help="城市名称，如 北京、上海、全国")
@click.option("--brand", default="", help="品牌，如 宝马、丰田")
@click.option("--series", default="", help="车系，如 3系、卡罗拉")
@click.option("--min-price", type=float, help="最低价格（万元）")
@click.option("--max-price", type=float, help="最高价格（万元）")
@click.option("--min-mileage", type=float, help="最低里程（万公里）")
@click.option("--max-mileage", type=float, help="最高里程（万公里）")
@click.option("--min-year", type=int, help="最早年份，如 2020")
@click.option("--max-year", type=int, help="最晚年份，如 2024")
@click.option("--transmission", default="", help="变速箱：auto/manual")
@click.option("--platform", default="all", help="平台：dongchedi,guazi,che168,all")
@click.option(
    "--sort", "sort_by", default="default",
    help="排序：default,price_asc,price_desc,mileage,date",
)
@click.option(
    "--output", "output_format",
    type=click.Choice(["table", "json", "yaml"]), default="table",
)
@click.option("--page", type=int, default=1, help="页码")
def search(
    city, brand, series, min_price, max_price, min_mileage, max_mileage,
    min_year, max_year, transmission, platform, sort_by, output_format, page,
):
    """搜索二手车，支持多平台聚合。"""
    filters = SearchFilter(
        city=city,
        brand=brand,
        series=series,
        min_price=min_price,
        max_price=max_price,
        min_mileage=min_mileage,
        max_mileage=max_mileage,
        min_year=min_year,
        max_year=max_year,
        transmission=transmission,
        sort_by=sort_by,
        page=page,
    )

    adapters = get_adapters(platform)
    if not adapters:
        err_console.print("[red]没有可用的平台适配器。[/red]")
        raise SystemExit(1)

    _log.debug(
        "search start platforms=%s filters=%s",
        [a.platform_name for a in adapters],
        asdict(filters),
    )

    cars = asyncio.run(_search_all(adapters, filters))
    _log.debug("search done raw_count=%s", len(cars))
    cars = _sort_results(cars, sort_by)

    if not cars:
        err_console.print("[yellow]未找到符合条件的车源。[/yellow]")
        return

    # Cache results for export command
    _save_last_search(cars)

    if output_format == "json":
        click.echo(json.dumps([asdict(c) for c in cars], ensure_ascii=False, indent=2))
    elif output_format == "yaml":
        click.echo(yaml.dump(
            [asdict(c) for c in cars], allow_unicode=True, default_flow_style=False,
        ))
    else:
        _render_table(cars)
        err_console.print(f"\n[dim]共 {len(cars)} 条结果[/dim]")


def _save_last_search(cars):
    """Cache last search results for the export command."""
    import os
    from dataclasses import asdict

    config_dir = os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
        "car-cli",
    )
    os.makedirs(config_dir, exist_ok=True)
    path = os.path.join(config_dir, "last_search.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([asdict(c) for c in cars], f, ensure_ascii=False, indent=2)
    except OSError:
        pass
