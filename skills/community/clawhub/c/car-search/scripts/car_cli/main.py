import click

from car_cli.commands.search import search
from car_cli.commands.detail import detail
from car_cli.commands.compare import compare
from car_cli.commands.loan import loan
from car_cli.commands.export import export_cmd
from car_cli.commands.series import series
from car_cli.logging_config import resolve_debug_flags, setup_logging


@click.group()
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="详细调试日志（输出到 stderr：请求、解析步骤、筛选条件等）",
)
@click.option(
    "--trace-http",
    is_flag=True,
    help="同时打开 httpx/httpcore 的 DEBUG 日志（极其冗长；也可设环境变量 CAR_CLI_TRACE_HTTP=1）",
)
@click.version_option(version="0.1.0")
@click.pass_context
def cli(ctx, debug, trace_http):
    """Car CLI — 二手车多平台聚合搜索工具。"""
    ctx.ensure_object(dict)
    dbg, trace = resolve_debug_flags(debug, trace_http)
    if trace and not dbg:
        dbg = True
    ctx.obj["debug"] = dbg
    ctx.obj["trace_http"] = trace
    setup_logging(debug=dbg, trace_http=trace)


cli.add_command(search)
cli.add_command(detail)
cli.add_command(compare)
cli.add_command(loan)
cli.add_command(export_cmd, name="export")
cli.add_command(series)


if __name__ == "__main__":
    cli()
