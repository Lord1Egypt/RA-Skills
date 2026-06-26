#!/usr/bin/env python3
"""
基金持仓管理系统 - CLI主程序
"""
import sys

import click
from rich.console import Console
from rich.prompt import Confirm

from .database import Database
from .csv_importer import CSVImporter
from .excel_importer import ExcelImporter
from .mcp_service import MCPService
from .statistics import Statistics
from .env_checker import EnvChecker
from .config import get_db_path
from .models import GroupColumn


console = Console()


# 分组列名选项
COLUMN_CHOICES = [col.value for col in GroupColumn]


# 字段帮助说明（用于 query 和 group 命令的 epilog）
# 注意：使用 \b (block) 让 Click 保留原始格式，不重新换行
COLUMN_HELP_EPILOG = """
\b
支持的查询/分组字段:
  fund_code        基金代码    基金的唯一标识代码
  fund_name        基金名称    基金的完整名称
  fund_manager     基金管理人  基金管理公司名称
  fund_account     基金账户    持有该基金的账户编号
  trade_account    交易账户    进行交易的账户编号
  sales_agency     销售机构    销售该基金的机构名称
  invest_type      投资类型    基金投资类型(如股票型、债券型)
  currency         结算币种    资产结算使用的货币类型
  dividend_method  分红方式    基金的分红方式(如现金分红)

\b
示例:
  fund-tools query -c fund_name -v 货币    查询名称包含"货币"的基金
  fund-tools group -c fund_manager         按基金管理人分组统计
"""


@click.group()
@click.option("--db", default=None, help="数据库文件路径（默认: $HOME/.fund-advisor/fund_portfolio_v1.db）")
@click.pass_context
def cli(ctx, db):
    """基金持仓管理系统 - 管理您的基金投资组合"""
    ctx.ensure_object(dict)
    db_path = db if db is not None else get_db_path()
    ctx.obj["db_path"] = db_path
    ctx.obj["database"] = Database(db_path)


# ==================== 环境初始化命令 ====================

@cli.command()
@click.option("--check", is_flag=True, help="仅检查环境状态")
@click.option("--force", is_flag=True, help="强制重新配置")
@click.pass_context
def init(ctx, check, force):
    """初始化环境（检查并配置mcporter和qieman-mcp）"""
    env_checker = EnvChecker()

    if check:
        results = env_checker.check_environment()
    else:
        results = env_checker.init_environment(force)

    console.print(env_checker.get_report())

    if results.get("status") == "error":
        sys.exit(1)


# ==================== 数据导入命令 ====================

@cli.command()
@click.argument("csv_path", type=click.Path(exists=True))
@click.pass_context
def import_csv(ctx, csv_path):
    """从CSV文件导入持仓数据"""
    database = ctx.obj["database"]
    importer = CSVImporter(database)

    console.print(f"[cyan]正在导入: {csv_path}[/]")

    # 验证CSV
    is_valid, errors = importer.validate_csv(csv_path)
    if not is_valid:
        for error in errors:
            console.print(f"[red]错误: {error}[/]")
        return

    # 导入数据
    success, fail, errors = importer.import_from_csv(csv_path)

    console.print(f"\n[green]导入完成![/]")
    console.print(f"  成功: {success} 条")
    if fail > 0:
        console.print(f"  失败: {fail} 条")
        for error in errors[:10]:  # 只显示前10条错误
            console.print(f"  [red]{error}[/]")


@cli.command()
@click.argument("excel_path", type=click.Path(exists=True))
@click.pass_context
def import_excel(ctx, excel_path):
    """从Excel文件导入持仓数据（支持.xlsx和.xls格式）"""
    database = ctx.obj["database"]
    importer = ExcelImporter(database)

    console.print(f"[cyan]正在导入: {excel_path}[/]")

    # 验证Excel
    is_valid, errors = importer.validate_excel(excel_path)
    if not is_valid:
        for error in errors:
            console.print(f"[red]错误: {error}[/]")
        return

    # 导入数据
    success, fail, errors = importer.import_from_excel(excel_path)

    console.print(f"\n[green]导入完成![/]")
    console.print(f"  成功: {success} 条")
    if fail > 0:
        console.print(f"  失败: {fail} 条")
        for error in errors[:10]:  # 只显示前10条错误
            console.print(f"  [red]{error}[/]")


@cli.command()
@click.pass_context
def reset(ctx):
    """清空所有持仓记录"""
    database = ctx.obj["database"]
    count = database.clear_all_holdings()
    console.print(f"[green]已清空 {count} 条持仓记录[/]")


# ==================== 持仓管理命令 ====================

@cli.command()
@click.argument("fund_code")
@click.pass_context
def detail(ctx, fund_code):
    """查看基金详情"""
    database = ctx.obj["database"]
    stats = Statistics(database)
    stats.show_fund_detail(fund_code)


# ==================== 分组统计和查询命令 ====================

@cli.command(epilog=COLUMN_HELP_EPILOG)
@click.option("-c", "--column", required=True, type=click.Choice(COLUMN_CHOICES),
              help="分组字段名称")
@click.option("-f", "--format", "output_format", type=click.Choice(["table", "json"]),
              default="table", help="输出格式: table(表格) 或 json")
@click.pass_context
def group(ctx, column, output_format):
    """按指定字段分组统计持仓数据

    对持仓记录按指定字段进行分组，并计算每组的份额、市值等汇总信息。
    支持表格和 JSON 两种输出格式，便于数据处理和脚本集成。
    """
    database = ctx.obj["database"]
    stats = Statistics(database)
    group_column = GroupColumn(column)
    stats.show_group_statistics(group_column, output_format)


@cli.command(epilog=COLUMN_HELP_EPILOG)
@click.option("-c", "--column", required=True, type=click.Choice(COLUMN_CHOICES),
              help="查询字段名称")
@click.option("-v", "--value", required=True, help="查询值（支持模糊匹配）")
@click.option("-f", "--format", "output_format", type=click.Choice(["table", "json"]),
              default="table", help="输出格式: table(表格) 或 json")
@click.pass_context
def query(ctx, column, value, output_format):
    """按条件查询持仓明细记录

    根据指定字段和值筛选持仓记录，支持模糊匹配。
    查询结果展示匹配记录的详细信息，包括份额、市值等。
    支持表格和 JSON 两种输出格式，便于数据处理和脚本集成。
    """
    database = ctx.obj["database"]
    stats = Statistics(database)
    group_column = GroupColumn(column)
    stats.show_query_result(group_column, value, output_format)


# ==================== 数据同步命令 ====================

@cli.command()
@click.option("--info", is_flag=True, help="同步基金基础信息")
@click.option("--detail", is_flag=True, help="同步基金持仓详情")
@click.option("--all", "sync_all", is_flag=True, help="同步所有信息")
@click.option("--batch-size", default=10, type=int, help="每批次获取基金数量（最大10）")
@click.pass_context
def sync(ctx, info, detail, sync_all, batch_size):
    """同步基金数据（从MCP服务获取）"""
    database = ctx.obj["database"]

    env_checker = EnvChecker()
    if not env_checker.check_mcporter_installed():
        console.print("[red]错误: mcporter未安装，请先运行 'fund-tools init' 初始化环境[/]")
        return

    if not env_checker.check_qieman_mcp_configured():
        console.print("[yellow]qieman-mcp未配置，正在自动配置...[/]")
        env_checker.setup_qieman_mcp_config()

    mcp = MCPService(batch_size=batch_size)

    fund_codes = database.get_all_fund_code()

    if not fund_codes:
        console.print("[yellow]没有找到持仓基金代码，请先导入持仓数据[/]")
        return

    console.print(f"[cyan]发现 {len(fund_codes)} 只基金需要同步，批次大小: {batch_size}[/]")

    if not info and not detail and not sync_all:
        sync_all = True

    if sync_all or info:
        # 同步基金基础信息
        console.print("\n[cyan]正在同步基金基础信息...[/]")
        console.print(f"  需要同步: {len(fund_codes)} 只")
        success, fail = mcp.sync_fund_info(fund_codes, database)
        console.print(f"  [green]成功: {success}[/], [red]失败: {fail}[/]")

    if sync_all or detail:
        # 同步基金持仓详情
        console.print("\n[cyan]正在同步基金持仓详情...[/]")
        console.print(f"  需要同步: {len(fund_codes)} 只")
        success, fail = mcp.sync_fund_holdings(fund_codes, database)
        console.print(f"  [green]成功: {success}[/], [red]失败: {fail}[/]")