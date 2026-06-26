import click
from rich.console import Console

from car_cli.logging_config import get_logger
from rich.table import Table

err_console = Console(stderr=True)
_log = get_logger("loan")


def _calc_equal_principal_interest(principal: float, monthly_rate: float, months: int):
    """等额本息: fixed monthly payment."""
    if monthly_rate == 0:
        return principal / months, principal, 0
    monthly = principal * monthly_rate * (1 + monthly_rate) ** months / (
        (1 + monthly_rate) ** months - 1
    )
    total = monthly * months
    interest = total - principal
    return monthly, total, interest


def _calc_equal_principal(principal: float, monthly_rate: float, months: int):
    """等额本金: decreasing monthly payment."""
    monthly_principal = principal / months
    first_month = monthly_principal + principal * monthly_rate
    last_month = monthly_principal + monthly_principal * monthly_rate
    total_interest = (principal * monthly_rate * (months + 1)) / 2
    total = principal + total_interest
    return first_month, last_month, total, total_interest


@click.command()
@click.option("--total", type=float, required=True, help="车辆总价（万元）")
@click.option("--down-payment", type=float, default=0.3, help="首付比例（0-1），默认 0.3")
@click.option("--years", type=int, default=3, help="贷款年限，默认 3 年")
@click.option(
    "--method",
    type=click.Choice(["equal_principal_interest", "equal_principal"]),
    default="equal_principal_interest",
    help="还款方式",
)
@click.option("--rate", type=float, default=4.0, help="年利率（%%），默认 4.0%%")
def loan(total, down_payment, years, method, rate):
    """车贷计算器，支持等额本息和等额本金。"""
    _log.debug(
        "loan total_wan=%s down=%s years=%s method=%s rate=%s%%",
        total,
        down_payment,
        years,
        method,
        rate,
    )
    total_yuan = total * 10000
    down = total_yuan * down_payment
    loan_amount = total_yuan - down
    months = years * 12
    monthly_rate = rate / 100 / 12

    table = Table(title="车贷计算", show_lines=True)
    table.add_column("项目", style="bold")
    table.add_column("数值", justify="right")

    table.add_row("车辆总价", f"{total:.2f}万元")
    table.add_row("首付比例", f"{down_payment * 100:.0f}%")
    table.add_row("首付金额", f"{down / 10000:.2f}万元")
    table.add_row("贷款金额", f"{loan_amount / 10000:.2f}万元")
    table.add_row("贷款年限", f"{years}年")
    table.add_row("年利率", f"{rate}%")
    table.add_row("还款方式", "等额本息" if method == "equal_principal_interest" else "等额本金")

    if method == "equal_principal_interest":
        monthly, total_pay, interest = _calc_equal_principal_interest(
            loan_amount, monthly_rate, months,
        )
        table.add_row("月供", f"{monthly:.2f}元")
        table.add_row("总利息", f"{interest / 10000:.2f}万元")
        table.add_row("还款总额", f"{total_pay / 10000:.2f}万元")
    else:
        first, last, total_pay, interest = _calc_equal_principal(
            loan_amount, monthly_rate, months,
        )
        table.add_row("首月月供", f"{first:.2f}元")
        table.add_row("末月月供", f"{last:.2f}元")
        table.add_row("总利息", f"{interest / 10000:.2f}万元")
        table.add_row("还款总额", f"{total_pay / 10000:.2f}万元")

    err_console.print(table)
