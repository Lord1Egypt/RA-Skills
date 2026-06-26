import csv
import io
import json
import os

import click
from rich.console import Console

from car_cli.logging_config import get_logger

err_console = Console(stderr=True)
_log = get_logger("export")


def _get_cache_path() -> str:
    config_dir = os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
        "car-cli",
    )
    return os.path.join(config_dir, "last_search.json")


def _load_last_search() -> list[dict]:
    path = _get_cache_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


@click.command("export")
@click.option(
    "--format", "fmt",
    type=click.Choice(["csv", "json"]), default="csv",
    help="导出格式",
)
@click.option("--output", "-o", "output_path", default="", help="输出文件路径（留空输出到 stdout）")
def export_cmd(fmt, output_path):
    """导出上次搜索结果为 CSV 或 JSON。"""
    cache = _get_cache_path()
    _log.debug("export cache_path=%s format=%s out=%r", cache, fmt, output_path or "(stdout)")
    data = _load_last_search()
    if not data:
        err_console.print("[yellow]没有缓存的搜索结果，请先执行 search 命令。[/yellow]")
        raise SystemExit(1)

    if fmt == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        content = _to_csv(data)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        _log.debug("export wrote rows=%s", len(data))
        err_console.print(f"[green]已导出 {len(data)} 条记录到 {output_path}[/green]")
    else:
        click.echo(content)


def _to_csv(data: list[dict]) -> str:
    if not data:
        return ""
    columns = [
        "id", "platform", "title", "price", "brand", "series",
        "model_year", "mileage", "first_reg_date", "transmission",
        "displacement", "city", "color", "url",
    ]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return buf.getvalue()
