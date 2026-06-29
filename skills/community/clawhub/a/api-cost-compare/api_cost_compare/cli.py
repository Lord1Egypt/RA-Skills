"""CLI 入口模块 — 基于 click 的命令行工具。

提供四个子命令：
  list      列出所有模型及其定价
  compare   并排对比两个模型
  recommend 根据任务类型和预算推荐最佳模型
  estimate  估算指定模型的 API 调用成本
"""

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box

from api_cost_compare.providers import (
    get_all_pricing,
    compare_models,
    estimate_cost,
    find_model,
)

console = Console()


# ────────────────────────────────────────────────────────────────
# 辅助函数
# ────────────────────────────────────────────────────────────────

def _price_str(price: float) -> str:
    """格式化价格为易读字符串。"""
    if price >= 1:
        return f"${price:.2f}"
    elif price >= 0.01:
        return f"${price:.4f}"
    else:
        return f"${price:.6f}"


def _context_str(tokens: int) -> str:
    """格式化上下文窗口大小。"""
    if tokens >= 1_000_000:
        return f"{tokens / 1_000_000:.0f}M"
    elif tokens >= 1_000:
        return f"{tokens / 1_000:.0f}K"
    return str(tokens)


def _build_pricing_table(models, highlight_idx: int = -1) -> Table:
    """构建通用的模型定价表格。"""
    table = Table(
        title="LLM API 定价对比",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold white",
        show_lines=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("模型名称", style="bold")
    table.add_column("提供商", style="magenta")
    table.add_column("输入价格 /1M", justify="right")
    table.add_column("输出价格 /1M", justify="right")
    table.add_column("上下文窗口", justify="right")
    table.add_column("任务标签")

    for i, m in enumerate(models):
        style = "bold yellow" if i == highlight_idx else None
        row_style = "on grey30" if i == highlight_idx else ""
        table.add_row(
            str(i + 1),
            m.model_name,
            m.provider_name,
            _price_str(m.input_price_per_1M),
            _price_str(m.output_price_per_1M),
            _context_str(m.context_window),
            ", ".join(m.task_tags),
            style=row_style,
        )
    return table


def _sort_by_input_price(models):
    """按输入价格升序排列。"""
    return sorted(models, key=lambda m: m.input_price_per_1M)


# ────────────────────────────────────────────────────────────────
# CLI 命令
# ────────────────────────────────────────────────────────────────

@click.group()
@click.version_option(version="1.0.0", prog_name="api-cost-compare")
def main():
    """api-cost-compare — 对比各大 LLM 提供商 API 定价。

    支持 Anthropic、OpenAI、DeepSeek、Google、OpenRouter、Mistral 等提供商。
    """
    pass


@main.command("list")
def list_models():
    """列出所有模型，按输入价格从低到高排序。"""
    models = _sort_by_input_price(get_all_pricing())

    console.print()
    console.print(
        Panel.fit(
            "[bold]📋 所有 LLM 模型定价列表[/bold]\n按输入价格从低到高排列",
            border_style="green",
        )
    )
    console.print()

    table = Table(
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold white",
        show_lines=True,
    )
    table.add_column("模型名称", style="bold")
    table.add_column("提供商", style="magenta")
    table.add_column("输入价格 /1M", justify="right", style="green")
    table.add_column("输出价格 /1M", justify="right", style="yellow")
    table.add_column("上下文窗口", justify="right")
    table.add_column("任务标签")

    for m in models:
        table.add_row(
            m.model_name,
            m.provider_name,
            _price_str(m.input_price_per_1M),
            _price_str(m.output_price_per_1M),
            _context_str(m.context_window),
            ", ".join(m.task_tags),
        )

    console.print(table)

    # 摘要
    cheapest = models[0]
    most_expensive = models[-1]
    console.print()
    console.print(
        f"[dim]共 {len(models)} 个模型 | "
        f"最低输入价格: [green]{_price_str(cheapest.input_price_per_1M)}[/green] ({cheapest.model_name}) | "
        f"最高输入价格: [red]{_price_str(most_expensive.input_price_per_1M)}[/red] ({most_expensive.model_name})[/dim]"
    )
    console.print()


@main.command("compare")
@click.argument("model1")
@click.argument("model2")
def compare_cmd(model1, model2):
    """并排对比两个模型的定价。"""
    m1 = find_model(model1)
    m2 = find_model(model2)

    if not m1:
        console.print(f"\n[red]❌ 未找到模型: {model1}[/red]")
        console.print("[dim]提示: 使用 [bold]api-cost-compare list[/bold] 查看所有可用模型[/dim]\n")
        return
    if not m2:
        console.print(f"\n[red]❌ 未找到模型: {model2}[/red]")
        console.print("[dim]提示: 使用 [bold]api-cost-compare list[/bold] 查看所有可用模型[/dim]\n")
        return

    console.print()
    console.print(
        Panel.fit(
            f"[bold]⚖️  模型对比: {m1.model_name} vs {m2.model_name}[/bold]",
            border_style="blue",
        )
    )

    # 并排表格
    table = Table(box=box.ROUNDED, header_style="bold cyan", show_lines=True)
    table.add_column("指标", style="bold", width=20)
    table.add_column(m1.model_name, justify="center")
    table.add_column(m2.model_name, justify="center")

    rows = [
        ("提供商", m1.provider_name, m2.provider_name),
        ("输入价格 /1M", _price_str(m1.input_price_per_1M), _price_str(m2.input_price_per_1M)),
        ("输出价格 /1M", _price_str(m1.output_price_per_1M), _price_str(m2.output_price_per_1M)),
        ("上下文窗口", _context_str(m1.context_window), _context_str(m2.context_window)),
        ("任务标签", ", ".join(m1.task_tags), ", ".join(m2.task_tags)),
    ]

    for label, v1, v2 in rows:
        # 高亮价格较低的一方
        if "输入价格" in label:
            if m1.input_price_per_1M < m2.input_price_per_1M:
                v1 = f"[green]{v1} ✅[/green]"
                v2 = f"[red]{v2}[/red]"
            elif m1.input_price_per_1M > m2.input_price_per_1M:
                v1 = f"[red]{v1}[/red]"
                v2 = f"[green]{v2} ✅[/green]"
        elif "输出价格" in label:
            if m1.output_price_per_1M < m2.output_price_per_1M:
                v1 = f"[green]{v1} ✅[/green]"
                v2 = f"[red]{v2}[/red]"
            elif m1.output_price_per_1M > m2.output_price_per_1M:
                v1 = f"[red]{v1}[/red]"
                v2 = f"[green]{v2} ✅[/green]"

        table.add_row(label, v1, v2)

    console.print(table)

    # 成本示例
    console.print()
    examples = [
        (1_000, 500, "小"),
        (10_000, 5_000, "中"),
        (100_000, 50_000, "大"),
    ]
    cost_table = Table(
        title="💰 成本对比示例",
        box=box.SIMPLE,
        header_style="bold cyan",
    )
    cost_table.add_column("场景 (输入/输出)", justify="center")
    cost_table.add_column(m1.model_name, justify="right")
    cost_table.add_column(m2.model_name, justify="right")
    cost_table.add_column("节省", justify="right", style="green")

    for inp, out, label in examples:
        c1 = (m1.input_price_per_1M * inp + m1.output_price_per_1M * out) / 1_000_000
        c2 = (m2.input_price_per_1M * inp + m2.output_price_per_1M * out) / 1_000_000
        saving = abs(c1 - c2)
        saving_pct = (saving / max(c1, c2)) * 100 if max(c1, c2) > 0 else 0

        if c1 < c2:
            c1_str = f"[green]{_price_str(c1)}[/green]"
            c2_str = f"[red]{_price_str(c2)}[/red]"
            cost_table.add_row(
                f"{label}规模 ({inp:,}/{out:,})",
                c1_str,
                c2_str,
                f"省 {_price_str(saving)} ({saving_pct:.0f}%)",
            )
        elif c2 < c1:
            c1_str = f"[red]{_price_str(c1)}[/red]"
            c2_str = f"[green]{_price_str(c2)}[/green]"
            cost_table.add_row(
                f"{label}规模 ({inp:,}/{out:,})",
                c1_str,
                c2_str,
                f"省 {_price_str(saving)} ({saving_pct:.0f}%)",
            )
        else:
            cost_table.add_row(
                f"{label}规模 ({inp:,}/{out:,})",
                _price_str(c1),
                _price_str(c2),
                "相同",
            )

    console.print(cost_table)
    console.print()


@main.command("recommend")
@click.option(
    "--task",
    type=click.Choice(["chat", "coding", "reasoning"]),
    default="chat",
    help="任务类型: chat（对话）, coding（编码）, reasoning（推理）",
)
@click.option(
    "--budget",
    type=float,
    default=10.00,
    help="月度预算（美元），用于计算可处理的请求量",
)
@click.option(
    "--input-tokens",
    type=int,
    default=1000,
    help="每次请求的平均输入 token 数",
)
@click.option(
    "--output-tokens",
    type=int,
    default=500,
    help="每次请求的平均输出 token 数",
)
def recommend_cmd(task, budget, input_tokens, output_tokens):
    """根据任务类型和预算推荐最佳模型。"""
    task_names = {"chat": "对话", "coding": "编码", "reasoning": "推理"}
    task_name = task_names.get(task, task)

    console.print()
    console.print(
        Panel.fit(
            f"[bold]🎯 推荐模型[/bold]\n"
            f"任务类型: [cyan]{task_name}[/cyan] | "
            f"月度预算: [yellow]${budget:.2f}[/yellow] | "
            f"每次用量: {input_tokens:,} 输入 / {output_tokens:,} 输出 tokens",
            border_style="green",
        )
    )
    console.print()

    results = compare_models(task_type=task, input_tokens=input_tokens, output_tokens=output_tokens)

    if not results:
        console.print("[yellow]⚠️ 没有找到匹配的模型[/yellow]\n")
        return

    table = Table(
        title=f"📊 {task_name}任务模型推荐",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("排名", style="dim", width=4, justify="right")
    table.add_column("模型名称", style="bold")
    table.add_column("提供商", style="magenta")
    table.add_column("单次成本", justify="right", style="green")
    table.add_column("月度可用请求数", justify="right", style="yellow")
    table.add_column("上下文窗口", justify="right")

    for rank, (m, cost) in enumerate(results, 1):
        per_request = (m.input_price_per_1M * input_tokens + m.output_price_per_1M * output_tokens) / 1_000_000
        requests_per_month = int(budget / per_request) if per_request > 0 else 0
        style = "on grey30" if rank == 1 else ""

        table.add_row(
            str(rank),
            m.model_name,
            m.provider_name,
            _price_str(per_request),
            f"{requests_per_month:,}",
            _context_str(m.context_window),
            style=style,
        )

    console.print(table)

    # 推荐小结
    best_model, best_cost = results[0]
    console.print()
    console.print(
        f"[bold green]🏆 推荐: {best_model.model_name} ({best_model.provider_name})[/bold green]"
    )
    console.print(
        f"   单次请求成本: {_price_str(best_cost)}, "
        f"月度可完成约 {int(budget / best_cost):,} 次请求"
    )
    console.print()


@main.command("estimate")
@click.option("--model", required=True, help="模型名称（如 'GPT-4o'、'deepseek-chat'）")
@click.option("--input", "input_tokens", type=int, default=1000, help="输入 token 数量")
@click.option("--output", "output_tokens", type=int, default=500, help="输出 token 数量")
def estimate_cmd(model, input_tokens, output_tokens):
    """估算指定模型的单次 API 调用成本。"""
    m = find_model(model)

    if not m:
        console.print(f"\n[red]❌ 未找到模型: {model}[/red]")
        console.print("[dim]提示: 使用 [bold]api-cost-compare list[/bold] 查看所有可用模型[/dim]")
        console.print("[dim]模型名称需要完全匹配，包括大小写和空格[/dim]\n")
        return

    cost = estimate_cost(model, input_tokens, output_tokens)
    input_cost = m.input_price_per_1M * input_tokens / 1_000_000
    output_cost = m.output_price_per_1M * output_tokens / 1_000_000

    console.print()
    console.print(
        Panel.fit(
            f"[bold]💰 成本估算[/bold]\n"
            f"模型: [cyan]{m.model_name}[/cyan] ({m.provider_name})",
            border_style="blue",
        )
    )
    console.print()

    table = Table(box=box.SIMPLE_HEAD, header_style="bold cyan")
    table.add_column("项目", style="bold")
    table.add_column("详情", justify="right")

    table.add_row("模型", m.model_name)
    table.add_row("提供商", m.provider_name)
    table.add_row("输入 Token 数", f"{input_tokens:,}")
    table.add_row("输出 Token 数", f"{output_tokens:,}")
    table.add_row("输入单价 /1M", _price_str(m.input_price_per_1M))
    table.add_row("输出单价 /1M", _price_str(m.output_price_per_1M))
    table.add_row("输入成本", _price_str(input_cost))
    table.add_row("输出成本", _price_str(output_cost))
    table.add_row(
        "[bold]总成本[/bold]",
        f"[bold green]{_price_str(cost)}[/bold green]",
    )

    console.print(table)

    # 扩展估算
    console.print()
    ext_table = Table(
        title="📈 扩展估算（相同比例）",
        box=box.SIMPLE,
        header_style="bold cyan",
    )
    ext_table.add_column("规模")
    ext_table.add_column("输入 Tokens", justify="right")
    ext_table.add_column("输出 Tokens", justify="right")
    ext_table.add_column("成本", justify="right", style="green")

    for factor, label in [(10, "×10"), (100, "×100"), (1000, "×1K"), (10_000, "×10K")]:
        ext_in = input_tokens * factor
        ext_out = output_tokens * factor
        ext_cost = estimate_cost(model, ext_in, ext_out)
        ext_table.add_row(
            label,
            f"{ext_in:,}",
            f"{ext_out:,}",
            _price_str(ext_cost),
        )

    console.print(ext_table)
    console.print()


# ────────────────────────────────────────────────────────────────
# 入口
# ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
