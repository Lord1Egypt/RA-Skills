"""
基金持仓管理系统 - 统计视图功能
"""
import json
from typing import Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.database import Database
from src.models import FundHolding, GroupColumn


class Statistics:
    """统计视图类"""

    def __init__(self, database: Database):
        self.database = database
        self.console = Console()

    def show_group_statistics(self, column: GroupColumn, output_format: str = "table"):
        """显示分组统计

        Args:
            column: 分组列名（GroupColumn 枚举）
            output_format: 输出格式，"table" 或 "json"
        """
        data = self.database.get_group_statistics(column.value)

        if not data:
            if output_format == "json":
                result = {"error": f"暂无{GroupColumn.get_display_name(column)}分布数据"}
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                self.console.print(f"[yellow]暂无{GroupColumn.get_display_name(column)}分布数据[/]")
            return

        display_name = GroupColumn.get_display_name(column)
        total = sum(item['total'] or 0 for item in data)
        total_count = sum(item['count'] for item in data)

        if output_format == "json":
            # JSON 格式输出
            items = []
            for item in data:
                item_total = item['total'] or 0
                percentage = (item_total / total * 100) if total > 0 else 0
                items.append({
                    "name": str(item['name'] or "未知"),
                    "count": item['count'],
                    "total": item_total,
                    "percentage": round(percentage, 2)
                })
            result = {
                "column": display_name,
                "items": items,
                "summary": {
                    "total_count": total_count,
                    "total_value": round(total, 2)
                }
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 表格格式输出
            table = Table(title=f"{display_name}分布", show_header=True, header_style="bold cyan")
            table.add_column(display_name, style="cyan")
            table.add_column("持仓数", justify="right", style="blue")
            table.add_column("资产价值", justify="right", style="green")
            table.add_column("占比", justify="right", style="yellow")

            for item in data:
                item_total = item['total'] or 0
                percentage = (item_total / total * 100) if total > 0 else 0
                table.add_row(
                    str(item['name'] or "未知"),
                    str(item['count']),
                    f"¥{item_total:,.2f}",
                    f"{percentage:.2f}%"
                )

            self.console.print(table)

            # 显示汇总信息
            self.console.print(f"\n[green]总计: {total_count} 条记录, 资产价值: ¥{total:,.2f}[/]")

    def show_query_result(self, column: GroupColumn, value: str, output_format: str = "table"):
        """显示查询结果（展示所有导入字段）

        Args:
            column: 查询列名（GroupColumn 枚举）
            value: 查询值
            output_format: 输出格式，"table" 或 "json"
        """
        holdings = self.database.query_holdings(column.value, value)

        if not holdings:
            if output_format == "json":
                result = {"error": f"未找到匹配 '{value}' 的持仓记录"}
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                self.console.print(f"[yellow]未找到匹配 '{value}' 的持仓记录[/]")
            return

        display_name = GroupColumn.get_display_name(column)
        total_value = sum(h.asset_value for h in holdings)

        if output_format == "json":
            # JSON 格式输出
            items = []
            for h in holdings:
                items.append({
                    "fund_code": h.fund_code,
                    "fund_name": h.fund_name or "",
                    "share_class": h.share_class or "",
                    "fund_manager": h.fund_manager or "",
                    "fund_account": h.fund_account or "",
                    "trade_account": h.trade_account or "",
                    "sales_agency": h.sales_agency or "",
                    "holding_shares": round(h.holding_shares, 2) if h.holding_shares else 0,
                    "share_date": str(h.share_date) if h.share_date else "",
                    "nav": round(h.nav, 4) if h.nav else None,
                    "nav_date": str(h.nav_date) if h.nav_date else "",
                    "asset_value": round(h.asset_value, 2) if h.asset_value else 0,
                    "settlement_currency": h.settlement_currency or "",
                    "dividend_method": h.dividend_method or ""
                })
            result = {
                "query": {
                    "column": display_name,
                    "value": value
                },
                "items": items,
                "summary": {
                    "total_count": len(holdings),
                    "total_value": round(total_value, 2)
                }
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 表格格式输出
            table = Table(
                title=f"查询结果: {display_name} 包含 '{value}' (共{len(holdings)}条)",
                show_header=True,
                header_style="bold cyan",
                expand=False,
            )

            # 添加所有导入字段列（不限制宽度，完整显示）
            table.add_column("基金代码", style="cyan")
            table.add_column("基金名称", style="white")
            table.add_column("份额类别", style="blue")
            table.add_column("基金管理人", style="magenta")
            table.add_column("基金账户", style="green")
            table.add_column("交易账户", style="yellow")
            table.add_column("销售机构", style="blue")
            table.add_column("持有份额", justify="right", style="green")
            table.add_column("份额日期", justify="center", style="white")
            table.add_column("净值", justify="right", style="yellow")
            table.add_column("净值日期", justify="center", style="white")
            table.add_column("资产价值", justify="right", style="green")
            table.add_column("结算币种", justify="center", style="blue")
            table.add_column("分红方式", style="cyan")

            # 显示所有记录，不做截取
            for holding in holdings:
                table.add_row(
                    holding.fund_code,
                    holding.fund_name or "",
                    holding.share_class or "",
                    holding.fund_manager or "",
                    holding.fund_account or "",
                    holding.trade_account or "",
                    holding.sales_agency or "",
                    f"{holding.holding_shares:,.2f}",
                    str(holding.share_date) if holding.share_date else "",
                    f"{holding.nav:.4f}" if holding.nav else "",
                    str(holding.nav_date) if holding.nav_date else "",
                    f"¥{holding.asset_value:,.2f}",
                    holding.settlement_currency or "",
                    holding.dividend_method or "",
                )

            self.console.print(table)

            # 显示汇总信息
            self.console.print(f"\n[green]总计: {len(holdings)} 条记录, 资产价值: ¥{total_value:,.2f}[/]")

    def _get_column_value(self, holding: FundHolding, column: GroupColumn) -> Any:
        """获取持仓记录中指定列的值"""
        if column == GroupColumn.FUND_CODE:
            return holding.fund_code
        elif column == GroupColumn.FUND_NAME:
            return holding.fund_name
        elif column == GroupColumn.FUND_MANAGER:
            return holding.fund_manager
        elif column == GroupColumn.FUND_ACCOUNT:
            return holding.fund_account
        elif column == GroupColumn.TRADE_ACCOUNT:
            return holding.trade_account
        elif column == GroupColumn.SALES_AGENCY:
            return holding.sales_agency
        elif column == GroupColumn.CURRENCY:
            return holding.settlement_currency
        elif column == GroupColumn.DIVIDEND_METHOD:
            return holding.dividend_method
        elif column == GroupColumn.INVEST_TYPE:
            # 投资类型需要从 fund_info 获取
            fund_info = self.database.get_fund_info(holding.fund_code)
            return fund_info.fund_invest_type if fund_info else "未知"
        return None

    def show_fund_detail(self, fund_code: str):
        """显示单个基金的详细信息"""
        # 获取基础信息
        fund_info = self.database.get_fund_info(fund_code)
        # 获取持仓详情
        holdings_detail = self.database.get_fund_holdings_detail(fund_code)
        # 获取用户持仓
        user_holdings = []
        all_holdings = self.database.get_fund_holdings()
        for h in all_holdings:
            if h.fund_code == fund_code:
                user_holdings.append(h)

        if not fund_info and not user_holdings:
            self.console.print(f"[red]未找到基金: {fund_code}[/]")
            return

        # 显示基金基础信息
        if fund_info:
            info_text = f"""
[bold cyan]基金代码:[/] {fund_info.fund_code}
[bold cyan]基金名称:[/] {fund_info.fund_name}
[bold cyan]投资类型:[/] {fund_info.fund_invest_type or '未知'}
[bold cyan]风险等级:[/] {fund_info.risk_5_level or '未知'}
[bold cyan]最新净值:[/] {fund_info.nav or '未知'} ({fund_info.nav_date or '未知'})
[bold cyan]基金规模:[/] {fund_info.net_asset}亿 ({fund_info.fund_invest_type or ''})
[bold cyan]成立日期:[/] {fund_info.setup_date or '未知'}
"""
            if fund_info.yearly_roe:
                info_text += f"[bold cyan]七日年化:[/] {fund_info.yearly_roe}%\n"
            if fund_info.one_year_return:
                info_text += f"[bold cyan]近一年收益:[/] {fund_info.one_year_return}%\n"
            if fund_info.manager_names:
                info_text += f"[bold cyan]基金经理:[/] {fund_info.manager_names}\n"

            self.console.print(Panel(info_text, title="[bold green]基金基础信息[/]", border_style="green"))

        # 显示用户持仓
        if user_holdings:
            table = Table(title="我的持仓", show_header=True, header_style="bold cyan")
            table.add_column("基金账户", style="cyan")
            table.add_column("交易账户", style="blue")
            table.add_column("持有份额", justify="right", style="green")
            table.add_column("资产价值", justify="right", style="yellow")

            for h in user_holdings:
                table.add_row(
                    h.fund_account,
                    h.trade_account,
                    f"{h.holding_shares:,.2f}",
                    f"¥{h.asset_value:,.2f}"
                )

            self.console.print(table)

        # 显示持仓详情
        if holdings_detail:
            detail_text = f"\n[bold cyan]报告日期:[/] {holdings_detail.report_date or '未知'}\n"
            if holdings_detail.stock_invest_ratio:
                detail_text += f"[bold cyan]股票仓位:[/] {holdings_detail.stock_invest_ratio}%\n"
            if holdings_detail.bond_invest_ratio:
                detail_text += f"[bold cyan]债券仓位:[/] {holdings_detail.bond_invest_ratio}%\n"

            self.console.print(Panel(detail_text, title="[bold green]持仓分析[/]", border_style="green"))

            # 显示十大重仓股
            if holdings_detail.top_stocks:
                stock_table = Table(title="十大重仓股", show_header=True, header_style="bold cyan")
                stock_table.add_column("代码", style="cyan", width=12)
                stock_table.add_column("名称", style="white", width=20)
                stock_table.add_column("占比", justify="right", style="green")
                stock_table.add_column("金额(亿)", justify="right", style="yellow")

                for stock in holdings_detail.top_stocks[:10]:
                    stock_table.add_row(
                        stock.stock_code,
                        stock.stock_name,
                        f"{stock.holding_ratio}%" if stock.holding_ratio else "-",
                        f"{stock.holding_amount}" if stock.holding_amount else "-"
                    )

                self.console.print(stock_table)

            # 显示十大重仓债
            if holdings_detail.top_bonds:
                bond_table = Table(title="十大重仓债", show_header=True, header_style="bold cyan")
                bond_table.add_column("代码", style="cyan", width=12)
                bond_table.add_column("名称", style="white", width=20)
                bond_table.add_column("占比", justify="right", style="green")
                bond_table.add_column("金额(亿)", justify="right", style="yellow")

                for bond in holdings_detail.top_bonds[:10]:
                    bond_table.add_row(
                        bond.bond_code,
                        bond.bond_name,
                        f"{bond.holding_ratio}%" if bond.holding_ratio else "-",
                        f"{bond.holding_amount}" if bond.holding_amount else "-"
                    )

                self.console.print(bond_table)